from datetime import datetime
from django.db import models
from planner.models import Facility    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming Bookings'),
        ('confirmed', 'Past Bookings'),
        ('cancelled', 'Cancelled Bookings'),
    ]
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    student = models.ForeignKey('planner.Student', on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()
    booking_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        return f"Booking by {self.student} at {self.facility}"
    
    def update_status(self):

            now = datetime.now()
            checkin_datetime = datetime.combine(self.checkin_date, self.checkin_time)
            
            checkout_datetime = datetime.combine(self.checkin_date, self.checkout_time)
            
            # ตรวจสอบและอัปเดตสถานะ
            if self.booking_status != 'cancelled':
                if now >= checkout_datetime:
                    self.booking_status = 'confirmed' 
                elif now < checkin_datetime:
                    self.booking_status = 'upcoming'  
                self.save()