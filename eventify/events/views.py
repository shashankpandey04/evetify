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
        return render(request, "events/registrations.html", {"event_id":event_id})

class EventEditView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if request.user != event.organizer:
            return HttpResponseForbidden("You are not authorized to view this page.")
        all_volunteers = User.objects.filter(role="volunteer")
        return render(request, "events/edit.html", {
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
        return render(request, "events/edit.html", {
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

class DeleteEventView(View):
    def post(self, request):
        eventID = request.POST.get("eventID")
        try:
            event = Event.objects.get(
                id=eventID,
                organizer=request.user
            )
        except Event.DoesNotExist:
            return JsonResponse({"message": "Event not found."}, status=404)
        registrations = RegisterEvent.objects.filter(event=event)
        if registrations.exists():
            return JsonResponse(
                {
                    "message": "Can't delete events with active registrations!",
                },
                status=400
            )
        event.delete()
        return JsonResponse(
                {
                    "message": "Event deleted successfully."
                },
                status=200
            )

class EventAnalyticsView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        return render(request, "events/analytics.html", {"event": event})

class EventAnalyticsAPI(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        registrations = RegisterEvent.objects.filter(event=event)
        users = [reg.user for reg in registrations]

        city_host = event.cityName.strip().lower()
        city_counts = {}
        country_counts = {}
        gender_counts = {"male": 0, "female": 0, "other": 0}
        age_groups = {"under_18": 0, "18_25": 0, "26_35": 0, "36_50": 0, "over_50": 0}
        from datetime import date

        for user in users:
            city = (user.cityName or '').strip().lower()
            country = (user.countryName or '').strip().lower()
            city_counts[city] = city_counts.get(city, 0) + 1
            country_counts[country] = country_counts.get(country, 0) + 1
            # Gender (if available)
            gender = getattr(user, 'gender', None)
            if gender:
                gender_counts[gender.lower()] = gender_counts.get(gender.lower(), 0) + 1
            # Age group (if available)
            dob = getattr(user, 'date_of_birth', None)
            if dob:
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 18:
                    age_groups["under_18"] += 1
                elif age <= 25:
                    age_groups["18_25"] += 1
                elif age <= 35:
                    age_groups["26_35"] += 1
                elif age <= 50:
                    age_groups["36_50"] += 1
                else:
                    age_groups["over_50"] += 1

        same_city = city_counts.get(city_host, 0)
        diff_city = sum(v for k, v in city_counts.items() if k != city_host)

        analytics = {
            "event": event.title,
            "event_city": event.cityName,
            "event_country": event.countryName,
            "total_registrations": len(users),
            "same_city_count": same_city,
            "diff_city_count": diff_city,
            "city_distribution": city_counts,
            "country_distribution": country_counts,
            "gender_distribution": gender_counts,
            "age_groups": age_groups,
        }
        return JsonResponse(analytics)
        
        