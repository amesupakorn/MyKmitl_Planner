from django.db import models
from planner.models import UniversityStaff, Student

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    staff = models.ForeignKey(UniversityStaff, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sender = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Message from {self.student} to {self.staff}"
    
    def mark_as_read(self):
        self.status = 'read'
        self.save()
        

     