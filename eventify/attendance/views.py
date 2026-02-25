from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
from events.models import Event
from accounts.models import User
from django.http import JsonResponse

class MyAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "attendance/my_attendance.html")

class AttendanceManagerView(LoginRequiredMixin, View):
    def get(self, request, eventID):
        if request.user.role not in ["organizer", "volunteer"]:
            return render(request, "unauthorized.html")
        return render(request, "attendance/manager.html", {
            "eventID": eventID
        })
    
    def post(self, request, eventID=None):
        if request.user.role not in ["organizer", "volunteer"]:
            return JsonResponse(
                {
                    "error": "Unauthorized access",
                }
            )
        email = request.POST.get("email")
        action = request.POST.get("action")
        eventID = eventID or request.POST.get("eventID")

        if action == 'checkin':
            Attendance.objects.create(
                event=Event.objects.get(eventID=eventID),
                user = User.objects.get(email=email),
                checkedIn = True,
                checkedInBy = request.user
            )
        elif action == 'checkout':
            attendance = Attendance.objects.get(event=Event.objects.get(eventID=eventID), user=User.objects.get(email=email))
            attendance.checkedOut = True
            attendance.checkedOutBy = request.user
            attendance.save()

        return JsonResponse({"success": True})

class ViewEventAttendanceView(LoginRequiredMixin, View):
    def get(self, request, eventID):
        if request.user.role not in ["organizer", "volunteer"]:
            return render(request, "unauthorized.html")
        return render(request, "attendance/view_event_attendance.html", {
            "eventID": eventID
        })


class MyAttendanceAPI(LoginRequiredMixin, View):
    def get(self, request):
        attendances = Attendance.objects.filter(user=request.user).select_related('event')
        data = {
            "attendances": [
                {
                    "event": a.event.title,
                    "eventID": str(a.event.eventID),
                    "checkedIn": a.checkedIn,
                    "checkedOut": a.checkedOut,
                    "checkedInAt": a.checkedInAt.isoformat() if getattr(a, 'checkedInAt', None) else None,
                    "checkedOutAt": a.checkedOutAt.isoformat() if getattr(a, 'checkedOutAt', None) else None,
                }
                for a in attendances
            ]
        }
        return JsonResponse(data)

class ViewEventAttendanceViewAPI(LoginRequiredMixin, View):
    def get(self, request, eventID):
        if request.user.role not in ["organizer", "volunteer"]:
            return JsonResponse(
                {
                    "error": "You are not authorized to view attendance for this event."
                }
            )
        event = Event.objects.get(eventID=eventID)
        attendances = Attendance.objects.filter(event=event)
        data = {
            "attendances": [
                {
                    "user": attendance.user.email,
                    "checkedIn": attendance.checkedIn,
                    "checkedOut": attendance.checkedOut,
                    "checkedInBy": attendance.checkedInBy.email if attendance.checkedInBy else None,
                    "checkedOutBy": attendance.checkedOutBy.email if attendance.checkedOutBy else None
                }
                for attendance in attendances
            ]
        }
        return JsonResponse(data)