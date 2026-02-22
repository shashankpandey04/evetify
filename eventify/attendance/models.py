from django.db import models

class Attendance(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    checkedIn = models.BooleanField(default=False)
    checkedInAt = models.DateTimeField(auto_now_add=True)
    checkedInBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name="checked_in_attendance")
    checkedOut = models.BooleanField(default=False)
    checkedOutAt = models.DateTimeField(auto_now_add=True)
    checkedOutBy = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name="checked_out_attendance")
