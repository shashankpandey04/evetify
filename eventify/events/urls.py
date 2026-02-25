from django.urls import path
from .views import (
    EventListView, EventCreateView,
    ViewEventDetails, EventEditView,
    ManageEvents, EventRegistrationsView,
    DeleteEventView, EventAnalyticsAPI,
    EventAnalyticsView
)

urlpatterns = [
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:event_id>/", ViewEventDetails.as_view(), name="view_event"),
    path("events/<int:event_id>/edit/", EventEditView.as_view(), name="event_edit"),
    path("events/<int:event_id>/registrations/", EventRegistrationsView.as_view(), name="view_event_registrations"),
    path("events/manage/", ManageEvents.as_view(), name="manage_events"),
    path("events/delete", DeleteEventView.as_view(), name="delete_event"),
    path("events/<int:event_id>/analytics/", EventAnalyticsView.as_view(), name="event_analytics_view"),
    path("events/api/v1/<int:event_id>/analytics/", EventAnalyticsAPI.as_view(), name="event_analytics"),
]