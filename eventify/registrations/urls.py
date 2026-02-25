from django.urls import path
from .views import (
    RegisterEventViewAPI, MyRegistrationsView, 
    UnRegisterEventViewAPI, IsRegisteredForEventAPI,
    EventRegistrationsAPI
)

urlpatterns = [
    path('events/api/v1/register/', RegisterEventViewAPI.as_view(), name='register_event'),
    path('events/my-registrations/', MyRegistrationsView.as_view(), name='my_registrations'),
    path('events/api/v1/unregister/', UnRegisterEventViewAPI.as_view(), name="unregister_event"),
    path('events/api/v1/is-registered/', IsRegisteredForEventAPI.as_view(), name="is_registered_for_event"),
    path("events/api/v1/<int:event_id>/registrations/", EventRegistrationsAPI.as_view(), name="event_registrations")
]