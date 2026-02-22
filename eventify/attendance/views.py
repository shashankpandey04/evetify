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
    def get(self, request):
        return render(request, "attendance/manager.html")
    
    def post(self, request):
        if request.user.role not in ["organizer", "volunteer"]:
            return JsonResponse(
                {
                    "error": "Unauthorized access",
                }
            )
        email = request.POST.get("email")
        action = request.POST.get("action")
        eventID = request.POST.get("eventID")

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