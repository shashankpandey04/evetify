from django.urls import path
from .views import EventListView, EventCreateView, ViewEventDetails, EventAnalyticsView, ManageEvents, EventRegistrationsView
urlpatterns = [
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:event_id>/", ViewEventDetails.as_view(), name="view_event"),
    path("events/<int:event_id>/analytics/", EventAnalyticsView.as_view(), name="event_analytics"),
    path("events/<int:event_id>/registrations/", EventRegistrationsView.as_view(), name="event_registrations"),
    path("evnts/manage/", ManageEvents.as_view(), name="manage_events"),
]