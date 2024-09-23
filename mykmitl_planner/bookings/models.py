from django.db import models
from planner.models import UniversityStaff, Student

class Facility(models.Model):
    staff = models.ForeignKey(UniversityStaff, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    opening = models.DateTimeField()
    closing = models.DateTimeField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    staff = models.ForeignKey(UniversityStaff, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    facility = models.ManyToManyField(Facility)
    
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField()
    booking_status = models.CharField(max_length=20)

    def __str__(self):
        return f"Booking by {self.student} at {self.facility}"