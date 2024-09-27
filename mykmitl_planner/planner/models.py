from django.db import models

from django.contrib.auth.models import User

# models.py
class Student(models.Model):
    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Year 5'),
        (6, 'Year 6'),
    ]

    student_user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, blank=True)
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    major = models.CharField(max_length=30, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UniversityStaff(models.Model):
    staff_user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    event_image = models.ImageField(upload_to='event_pics/', null=True, blank=True)

    
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
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.title

