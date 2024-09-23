from django.db import models
from planner.models import Facility    

class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    student = models.ForeignKey('planner.Student', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField()
    booking_status = models.CharField(max_length=20)

    def __str__(self):
        return f"Booking by {self.student} at {self.facility}"