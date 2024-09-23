from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    year_of_study = models.DateField()
    major = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UniversityStaff(models.Model):
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Facility(models.Model):
    staff = models.ForeignKey('planner.UniversityStaff', on_delete=models.CASCADE)
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
    staff = models.ForeignKey('planner.UniversityStaff', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    facility = models.ManyToManyField(Facility)
    
    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

