from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from planner.models import *
from django.utils.dateparse import parse_date
from django.contrib import messages
from datetime import datetime, timedelta
from django.db import transaction
import json

# Event
class EventListPage(View):
    
    def get(self, request):
        return render(request, "event/event-list.html",{

        })
    
class EventDetailPage(View):
    
    def get(self, request):
        return render(request, "event/event-detail.html",{

        })
    
class CreateEventPage(View):
    
    def get(self, request):
        return render(request, "event/staff/create-event.html",{

        })

class EditEventPage(View):
    
    def get(self, request):
        return render(request, "event/staff/edit-event.html",{

        })
    

# Booking
class BookingListPage(View):
    def get(self, request):
        bookings = Booking.objects.all()
        # อัปเดตสถานะการจองทั้งหมด
        for booking in bookings:
            booking.update_status()

        facility = Facility.objects.filter(booking_status='available').values('location').distinct()
        

        return render(request, "booking/book-list.html",{
            'locations' : facility 
        })
    
class BookFirstPage(View):
    
    def get(self, request, location):
        facilities = Facility.objects.filter(location=location)
        return render(request, "booking/book-first.html",{
            'facility' : facilities
        })

class BookSecondPage(View):
    
    def get(self, request, id):
        facilities = Facility.objects.get(id=id)
        return render(request, "booking/book-second.html",{
            'facilities' : facilities
        })

class CheckAvailableTimes(View):

    def post(self, request):
        # โหลดข้อมูลจาก body ของ request ในรูปแบบ JSON
        body = json.loads(request.body)
        selected_date = body.get('date')
        facility_id = body.get('facility_id')


        if selected_date and facility_id:
            # แปลงวันที่จาก string เป็น date object
            selected_date = parse_date(selected_date)
            
            # Query ข้อมูลเวลาที่ถูกจองแล้ว โดยใช้ checkin_date และ facility_id
            bookings = Booking.objects.filter(checkin_date=selected_date, facility_id=facility_id).values('checkin_time')
            times = list(bookings)

            return JsonResponse(times, safe=False)
        
        return JsonResponse([], safe=False)

    
class BookThirdPage(View):
    
    def post(self, request, id):
        facilities = Facility.objects.get(id=id)
        date = request.POST.get('start_date')
        time = request.POST.get('selected_time')

        if date and time:
            try:
                # แปลงวันที่และเวลา
                date = datetime.strptime(date, '%Y-%m-%d').date()
                time = datetime.strptime(time, '%H:%M:%S')
                time_end = (time + timedelta(hours=1)).time()

                time_start = time.strftime('%H:%M')
                time_end = time_end.strftime('%H:%M')

                # ถ้าทำการจองสำเร็จ, แสดงผลในหน้า booking success
                return render(request, "booking/book-third.html", {
                    'facilities': facilities,
                    'time_start': time_start,
                    'time_end': time_end,
                    'date': date
                })

            except ValueError:
                # จัดการข้อผิดพลาดจากการแปลงข้อมูล
                messages.error(request, "Invalid date or time format.")
                return redirect('book-second', id=id)

        # กรณีที่ไม่มีข้อมูล date หรือ time
        messages.error(request, "Please fill out all required fields.")
        return redirect('book-second', id=id)

class BookConfirm(View):
    def post(self, request, id):
        try:

            facilities = Facility.objects.get(id=id)
            student = Student.objects.get(student_user=request.user)

            # รับข้อมูลจาก POST request
            checkin_date = datetime.strptime(request.POST.get('date'), '%b. %d, %Y').date()
            checkin_time = request.POST.get('start_time')  
            checkout_time = request.POST.get('end_time')  
        
            with transaction.atomic(): 
                booking = Booking.objects.create(
                    facility = facilities,
                    student = student,
                    checkin_date = checkin_date,
                    checkin_time = checkin_time,
                    checkout_time = checkout_time,
                    booking_status = 'upcoming'
                )
                
                messages.success(request, "Confirm your Booking")
                return redirect('upcoming')
        except Exception as e:
            # จัดการข้อผิดพลาดทั่วไป
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('book-third', id=id)    


class UpcomingBookPage(View):
    
    def get(self, request):
        student = Student.objects.get(student_user=request.user)
        booking = Booking.objects.filter(booking_status='upcoming', student_id=student)
        return render(request, "booking/upcoming.html",{
            'booking' : booking
        })
    
    def put(self, request):
        try:
            body = json.loads(request.body)
            booking_id = body.get('booking_id')
            booking = Booking.objects.get(id=booking_id)
            with transaction.atomic(): 
                if booking.booking_status != 'cancelled':
                    booking.booking_status = 'cancelled'
                    booking.save()
                    
                    messages.success(request, "Booking cancelled successfully")
                    return JsonResponse({'message': 'Booking cancelled successfully.'}, status=200)
        except Exception as e:
            # จัดการข้อผิดพลาดทั่วไป
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('upcoming')

class PastBookPage(View):
    
    def get(self, request):
        student = Student.objects.get(student_user=request.user)
        booking = Booking.objects.filter(booking_status='confirmed', student_id=student)
        return render(request, "booking/past-book.html",{
            'booking' : booking
        })
    
class BookDetailPage(View):
    
    def get(self, request, id):
        booking = Booking.objects.get(id=id)
        return render(request, "booking/book-detail.html",{
            'booking' : booking
        })
    
class StaffBookPage(View):
    
    def get(self, request):
        booking = Booking.objects.all().order_by('-checkin_date')
        return render(request, "booking/staff/book-staff.html",{
            'booking' : booking
        })
    
class FacilitiesPage(View):
    
    def get(self, request):
        return render(request, "facilities/facilities.html",{

        })