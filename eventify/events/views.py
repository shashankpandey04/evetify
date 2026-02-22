from django.shortcuts import render, redirect
from django.views import View
from .models import Event

class EventListView(View):
    def get(self, request):
        events = Event.objects.filter(
            status="published"
        )
        return render(request, "events/list.html", {"events": events})
