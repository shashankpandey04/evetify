from django.http import HttpResponseForbidden, JsonResponse
from registrations.models import RegisterEvent
from django.shortcuts import render, redirect
from django.views import View
from .models import Event
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from .models import Event

class EventListView(View):
    def get(self, request):
        events = Event.objects.filter(
            status="published"
        )
        return render(request, "events/list.html", {"events": events})

class ManageEvents(LoginRequiredMixin, View):
    def get(self, request):
        events = Event.objects.filter(organizer=request.user)
        return render(request, "events/manage.html", {"events": events})

class EventRegistrationsView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        if request.user != event.organizer:
            return HttpResponseForbidden("You are not authorized to view this page.")
        event = Event.objects.get(id=event_id)
        registrations = RegisterEvent.objects.filter(event=event).select_related("user")
        return render(request, "events/registrations.html", {
            "event": event,
            "registrations": registrations
        })

class EventAnalyticsView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if request.user != event.organizer:
            return HttpResponseForbidden("You are not authorized to view this page.")
        all_volunteers = User.objects.filter(role="volunteer")
        return render(request, "events/analytics.html", {
            "event": event,
            "all_volunteers": all_volunteers,
        })

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if request.user != event.organizer:
            return HttpResponseForbidden("You are not authorized to edit this event.")
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.date = request.POST.get("date")
        event.startTime = request.POST.get("startTime")
        event.endTime = request.POST.get("endTime")
        event.location = request.POST.get("location")
        capacity_raw = request.POST.get("capacity")
        event.capacity = int(capacity_raw) if capacity_raw else None
        event.status = request.POST.get("status")
        volunteers_ids = request.POST.getlist("volunteers")
        event.volunteers.set(volunteers_ids)
        event.save()
        all_volunteers = User.objects.filter(role="volunteer")
        registrations = RegisterEvent.objects.filter(event=event).select_related("user")
        return render(request, "events/analytics.html", {
            "event": event,
            "all_volunteers": all_volunteers,
            "registrations": registrations,
            "success": True
        })

class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != "organizer":
            return redirect("event_list")
        allVolunteers = User.objects.filter(
            role="volunteer"
        )
        context = {
            "allVolunteers": allVolunteers,
        }
        return render(request, "events/create.html", context)

    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        startTime = request.POST.get("startTime")
        endTime = request.POST.get("endTime")
        registrationDeadline = request.POST.get("registrationDeadline")
        capacity_raw = request.POST.get("capacity")
        status = request.POST.get("status")
        attendanceEnabled = request.POST.get("attendanceEnabled") == "on"
        volunteers = request.POST.getlist("volunteers")
        date = request.POST.get("date")

        capacity = int(capacity_raw) if capacity_raw else None

        event = Event.objects.create(
            title=title,
            description=description,
            startTime=startTime,
            endTime=endTime,
            registrationDeadline=registrationDeadline,
            location=location,
            capacity=capacity,
            status=status,
            attendanceEnabled=attendanceEnabled,
            organizer=request.user,
            date=date,
        )
        event.volunteers.set(volunteers)
        return redirect("view_event", event_id=event.id)

class ViewEventDetails(View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        return render(request, "events/detail.html", {"event": event, "user": request.user})