import calendar
from datetime import timedelta
from time import localtime
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CalendarForm
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
import json
from django.contrib.messages import get_messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from bookings.models import Booking
from django.db.models import Count
from chat.models import Message

class CalendarPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.view_schedule", "planner.add_schedule", "planner.change_schedule", "planner.delete_schedule"]
    
    def get(self, request):
        try:
            student = Student.objects.get(student_user=request.user)
            
            schedules = Schedule.objects.filter(student=student)
            
            events_list = []
            if schedules.exists():  
                for event in schedules:
                    start_time = event.start_time + timedelta(hours=7)
                    end_time = event.end_time + timedelta(hours=7)
                    events_list.append({
                        'id': event.id,
                        'title': event.title,
                        'start': start_time.isoformat(), 
                        'end': end_time.isoformat(),
                        'description': event.description,
                        'location': event.facility.id if event.facility else None,  
                        'activity': event.event.id if event.event else None, 
                        'color': event.color,
                    })
            else:
                pass

            return render(request, "calendar.html", {
                'student': student,
                'form': CalendarForm(),
                'events': json.dumps(events_list) 
            })
        
        except Student.DoesNotExist:
            # Handle the case where no student record is found for the user
            return render(request, "calendar.html", {
                'student': None,  # No student record
                'form': CalendarForm(),
                'events': json.dumps([])  # Return empty events list
            })
        
        
    def post(self, request):
        try:
            student = Student.objects.get(student_user=request.user)
            data = json.loads(request.body)
            location_id = data.get('location')
            activity_id = data.get('activity')
            location = None
            activity = None
            
            if location_id:
                try:
                    location = Facility.objects.get(pk=location_id)
                except Facility.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Facility not found'}, status=404)
            
            if activity_id:
                try:
                    activity = Event.objects.get(pk=activity_id)
                except Event.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
            
            # สร้างกิจกรรมใหม่
            schedule = Schedule(student=student)
            
            form = CalendarForm(data, instance=schedule)
            if form.is_valid():
                schedule = form.save(commit=False)
                if location:
                    schedule.facility = location
                if activity:
                    schedule.event = activity
                                    
                schedule.save()
                
                return JsonResponse({
                    'status': 'success',
                    'event_id': schedule.id,
                    'message': 'Event created successfully!'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    def put(self, request):
        try:
            student = Student.objects.get(student_user=request.user)
            data = json.loads(request.body)
            event_id = data.get('event_id')
            location_id = data.get('location')
            activity_id = data.get('activity')
            location = None
            activity = None

            if not event_id:
                return JsonResponse({'status': 'error', 'message': 'Event ID is required for update'}, status=400)

            try:
                schedule = Schedule.objects.get(id=event_id, student=student)
            except Schedule.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)

            if location_id:
                try:
                    location = Facility.objects.get(pk=location_id)
                except Facility.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Facility not found'}, status=404)
            
            if activity_id:
                try:
                    activity = Event.objects.get(pk=activity_id)
                except Event.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)

            form = CalendarForm(data, instance=schedule)
            if form.is_valid():
                schedule = form.save(commit=False)
                if location:
                    schedule.facility = location
                if activity:
                    schedule.event = activity
                schedule.save()
                
                return JsonResponse({
                    'status': 'success',
                    'event_id': schedule.id,
                    'message': 'Event updated successfully!'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

            
            
    def delete(self, request, event_id):
        try:
            student = Student.objects.get(student_user=request.user)
            
            schedule = Schedule.objects.get(id=event_id, student=student)
            schedule.delete()  # ลบกิจกรรมจากฐานข้อมูล
            
            return JsonResponse({
                'status': 'success',
                'message': 'Event deleted successfully!'
            })
        except Schedule.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Event not found'
            }, status=404)
            
            

class DashboardView(LoginRequiredMixin, View):
    login_url = '/auth'
    
    def get(self, request):
        try:
            staff = UniversityStaff.objects.get(staff_user=request.user)
        except UniversityStaff.DoesNotExist:
            return HttpResponseForbidden("You are not authorized to view this page.")  

        student = Student.objects.all().count()
        booking = Booking.objects.filter(booking_status = 'upcoming').count()
        bookings = Booking.objects.all()
        event = Event.objects.filter(status = 'upcoming').count()
        booking_confirm = Booking.objects.filter(booking_status = 'confirmed').count()
        staff = UniversityStaff.objects.get(staff_user=request.user)
        student_ids = Message.objects.filter(staff=staff).values_list('student', flat=True).distinct()
        
        # ดึงข้อความล่าสุดสำหรับแต่ละ student ที่สนทนากับ staff
        message_info = []
        for student_id in student_ids:
            last_message = Message.objects.filter(staff=staff, student_id=student_id).order_by('-timestamp').first()
            message_sent = Message.objects.filter(staff=staff, student_id=student_id, status='sent').count()
            message_info.append({
                'last_message': last_message,
                'message_sent': message_sent,
                'student_id' : student_id
            })
        
        return render(request, 'dashboard.html',{
            'student': student,
            'booking':booking,
            'bookings': bookings,
            'event': event,
            'booking_confirm': booking_confirm,
            'message_info': message_info
        })
        
class confirmed_bookings_chart_data(LoginRequiredMixin, View):
    login_url = '/auth'
    def get(self, request):
        confirmed_bookings = Booking.objects.filter(booking_status='confirmed').extra(
            select={'month': "EXTRACT(month FROM checkin_date)"}
        ).values('month').annotate(total=Count('id')).order_by('month')
        
        data_dict = {month: 0 for month in range(1, 13)} 
        
        # ใส่ข้อมูลจำนวนการจองที่มีในแต่ละเดือน
        for booking in confirmed_bookings:
            data_dict[booking['month']] = booking['total']
        
        # สร้าง labels และ data
        labels = [calendar.month_abbr[month] for month in data_dict.keys()]  #
        data = list(data_dict.values())
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })