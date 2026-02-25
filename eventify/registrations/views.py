from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import RegisterEvent
from events.models import Event
from django.http import HttpResponseForbidden, JsonResponse

class RegisterEventViewAPI(LoginRequiredMixin, View):
    def post(self, request):
        event_id = request.POST.get('eventID')
        user = request.user
        event = Event.objects.get(eventID=event_id)
        RegisterEvent.objects.get_or_create(event=event, user=user)
        return JsonResponse({"success": True})

class MyRegistrationsView(LoginRequiredMixin, View):
    def get(self, request):
        registrations = RegisterEvent.objects.filter(user=request.user)
        return render(request, 'registrations/my_registrations.html', {
            'registrations': registrations
        })
    
class UnRegisterEventViewAPI(LoginRequiredMixin, View):
    def post(self, request):
        event_id = request.POST.get('eventID')
        user = request.user
        event = Event.objects.get(eventID=event_id)
        RegisterEvent.objects.filter(
            user=user,
            event=event
        ).delete()
        return JsonResponse({"success": True})

class IsRegisteredForEventAPI(LoginRequiredMixin, View):
    def get(self, request):
        event_id = request.GET.get('eventID')
        user = request.user
        event = Event.objects.filter(eventID=event_id).first()
        is_registered = RegisterEvent.objects.filter(
            user=user,
            event=event
        ).exists()
        return JsonResponse({'is_registered': is_registered})
    
class EventRegistrationsAPI(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if request.user != event.organizer:
            return JsonResponse(
                {
                    "error": "You are not authorized to view registrations for this event."
                }
            )
        registrations = RegisterEvent.objects.filter(event=event).select_related("user")
        return JsonResponse(
            {
                "registrations": [
                    {
                        "user": registration.user.username,
                        "email": registration.user.email,
                        "registeredAt": registration.registeredAt
                    }
                    for registration in registrations
                ]
            }
        )