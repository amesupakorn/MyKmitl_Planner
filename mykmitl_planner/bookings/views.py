from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from planner.models import *
from django.utils.dateparse import parse_date
from django.contrib import messages
from datetime import datetime, timedelta
from django.db import transaction
import json
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Event
class EventListPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_event"]
    
    def get(self, request):
        event = Event.objects.filter(status__in = ['upcoming', 'ongoing']).order_by('-start_time')
        for e in event:
            e.check_and_update_status()
            
        return render(request, "event/event-list.html",{
            'event' : event
        })
        
    

class EventDetailPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_event"]
    
    def get(self, request, id):
        event = Event.objects.get(id=id)
        return render(request, "event/event-detail.html",{
            'event' : event
        })
    
    def delete(self, request, id):
        if not request.user.has_perm('planner.delete_event'):
            return HttpResponseForbidden("You do not have permission to delete this event.")
        try:
            body = json.loads(request.body)
            event_id = body.get('event_id')
            event = Event.objects.get(id=event_id)

            with transaction.atomic(): 
                event.facility.clear()
                event.delete()
                messages.success(request, "Delete event successfully")
                return JsonResponse({'message': 'Delete event successfully.'}, status=200)
  
            
        except Exception as e:
            # จัดการข้อผิดพลาดทั่วไป
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('event-detail')  
    

class CreateEventPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.add_event"]
    
    def get(self, request):
        form = CreateEventForm()
        return render(request, "event/staff/create-event.html", {
            'form': form
        })
    
    def post(self, request):
        form = CreateEventForm(request.POST, request.FILES)
        try:
            with transaction.atomic(): 

                if form.is_valid():
                    event = form.save(commit=False)
                    staff_member = UniversityStaff.objects.get(staff_user=request.user)

                    event.staff = staff_member
                    event.save()
                    form.save_m2m() 
                    
                    messages.success(request, "Event created successfully")
                    return redirect('event-list')

        except Exception as e:
            # จัดการข้อผิดพลาดทั่วไป
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('event-list') 
        

class EditEventPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.change_event"]
    
    def get(self, request, id):
        event = Event.objects.get(id=id)
        form = CreateEventForm(instance=event)
        return render(request, 'event/staff/edit-event.html', {
            'event': event,
            'form' : form
        })

    def post(self, request, id):
        event = Event.objects.get(id=id)
        form = CreateEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', id=event.id)
        
        return render(request, 'event/staff/edit-event.html', {
            'event': event
        })
    

# Booking
class BookingListPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    
    def get(self, request):
        bookings = Booking.objects.all()
        # อัปเดตสถานะการจองทั้งหมด
        for booking in bookings:
            booking.update_status()

        facility = Facility.objects.filter(booking_status='available').values('location').distinct()

        return render(request, "booking/book-list.html",{
            'locations' : facility 
        })
    

class BookFirstPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    def get(self, request, location):
        facilities = Facility.objects.filter(location=location, status = 'opening').order_by('id')
        return render(request, "booking/book-first.html",{
            'facility' : facilities
        })


class BookSecondPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    def get(self, request, id):
        facilities = Facility.objects.get(id=id)
        return render(request, "booking/book-second.html",{
            'facilities' : facilities
        })


class CheckAvailableTimes(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.add_booking"]
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
    

class BookThirdPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.add_booking"]
    
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


class BookConfirm(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.add_booking"]
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

class UpcomingBookPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking", "bookings.change_booking"]
    
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


class PastBookPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    
    def get(self, request):
        student = Student.objects.get(student_user=request.user)
        booking = Booking.objects.filter(booking_status='confirmed', student_id=student)
        return render(request, "booking/past-book.html",{
            'booking' : booking
        })
    

class BookDetailPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    
    def get(self, request, id):
        booking = Booking.objects.get(id=id)
        return render(request, "booking/book-detail.html",{
            'booking' : booking
        })
    

class StaffBookPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["bookings.view_booking"]
    
    def get(self, request):
        booking = Booking.objects.all().order_by('-checkin_date')
        return render(request, "booking/staff/book-staff.html",{
            'booking' : booking
        })


# Facility
class FacilitiesPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_facility"]
    
    def get(self, request):
        facility = Facility.objects.all().order_by('id')
        form = FacilityForm()
        return render(request, "facilities/facilities.html",{
            'facilities' : facility,
            'form': form
        })
    
    def post(self, request):
        form = FacilityForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save() 
                messages.success(request, "Event created successfully")
                return redirect('facilities')
            
            except Exception as e:
                print(f"Error saving facility: {e}")
        
        facility = Facility.objects.all()
        return render(request, "facilities/facilities.html", {
            'facilities': facility,
            'form': form,
        })
    
    def delete(self, request):
        try:
            body = json.loads(request.body)
            facility_id = body.get('facility_id')
            Facilities = Facility.objects.get(id=facility_id)

            with transaction.atomic(): 
                Facilities.delete()
                messages.success(request, "Delete facility successfully")
                return JsonResponse({'message': 'Delete facility successfully.'}, status=200)
  
        except Exception as e:
            # จัดการข้อผิดพลาดทั่วไป
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('facilities')  
        

class EditFacilities(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_facility", "planner.change_facility"]
    
    def get(self, request, id):
        facility = Facility.objects.get(id=id)
        
        data = {
            'name': facility.name,
            'location': facility.location,
            'description': facility.description,
            'opening': facility.opening.strftime('%H:%M'),
            'closing': facility.closing.strftime('%H:%M'),
            'status': facility.status,
            'booking_status': facility.booking_status,
            'capacity': facility.capacity,
        }
        
        return JsonResponse(data)

    def post(self, request, id):
        facility = Facility.objects.get(id=id)
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return redirect('facilities')
        
        return render(request, 'facilities/facilities.html', {
            'facility': facility,
            'form': form
        })
    
class ViewFacilities(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_facility"]

    def get(self, request, id):
        facility = Facility.objects.get(id=id)
        
        data = {
            'name': facility.name,
            'location': facility.location,
            'description': facility.description,
            'opening': facility.opening.strftime('%H:%M'),
            'closing': facility.closing.strftime('%H:%M'),
            'status': facility.status,
            'booking_status': facility.booking_status,
            'capacity': facility.capacity,
        }
        
        return JsonResponse(data)
