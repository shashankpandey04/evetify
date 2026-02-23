from django.urls import path
from .views import AttendanceManagerView, MyAttendanceView, ViewEventAttendanceView
urlpatterns = [
    path('attendance/manager/', AttendanceManagerView.as_view(), name='attendance_manager'),
    path('attendance/my/', MyAttendanceView.as_view(), name='my_attendance'),
    path('attendance/<int:eventID>/view/', ViewEventAttendanceView.as_view(), name='view_event_attendance'),
]