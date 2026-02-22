from django.urls import path
from .views import RegisterEventView, MyRegistrationsView, UnRegisterEventView, IsRegisteredForEvent

urlpatterns = [
    path('events/api/v1/register/', RegisterEventView.as_view(), name='register_event'),
    path('events/my-registrations/', MyRegistrationsView.as_view(), name='my_registrations'),
    path('events/api/v1/unregister', UnRegisterEventView.as_view(), name="unregister_event"),
    path('events/api/v1/is-registered/', IsRegisteredForEvent.as_view(), name="is_registered_for_event")
]