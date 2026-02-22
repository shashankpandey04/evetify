from django.urls import path
from .views import AttendanceManagerView, MyAttendanceView
urlpatterns = [
    path('attendance/manager/', AttendanceManagerView.as_view(), name='attendance_manager'),
    path('attendance/my/', MyAttendanceView.as_view(), name='my_attendance'),
]