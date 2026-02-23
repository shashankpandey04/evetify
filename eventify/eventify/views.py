from django.shortcuts import render
from events.models import Event

def landing_page(request):
    upcomingEvents = Event.objects.filter(status="published")
    return render(request, 'index.html', {'upcomingEvents': upcomingEvents})

def aboutUsPage(request):
    return render(request, 'about.html')