from django.urls import path
from .views import (
    AttendanceManagerView,
    MyAttendanceView,
    ViewEventAttendanceViewAPI,
    ViewEventAttendanceView,
    MyAttendanceAPI,
)

urlpatterns = [
    path('attendance/manager/<int:eventID>/', AttendanceManagerView.as_view(), name='attendance_manager'),
    path('attendance/my/', MyAttendanceView.as_view(), name='my_attendance'),
    path('attendance/api/v1/<int:eventID>/view/', ViewEventAttendanceViewAPI.as_view(), name='view_event_attendance_api'),
    path('attendance/api/v1/my/', MyAttendanceAPI.as_view(), name='my_attendance_api'),
    path('attendance/<int:eventID>/view/', ViewEventAttendanceView.as_view(), name='view_event_attendance')
]