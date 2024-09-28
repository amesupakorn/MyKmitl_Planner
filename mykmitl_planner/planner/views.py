from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CalendarForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.messages import get_messages


class CalendarPage(View):
    
    def get(self, request):
        student = Student.objects.get(student_user=request.user)  # ดึงข้อมูลนักเรียนที่ล็อกอินอยู่
        schedules = Schedule.objects.filter(student=student)  # ดึงข้อมูลตารางกิจกรรมของนักเรียน
        form = CalendarForm()  # สร้างฟอร์มว่างสำหรับการเพิ่มกิจกรรมใหม่

        events_list = []
        for event in schedules:
            events_list.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(), 
                'end': event.end_time.isoformat(),
                'description': event.description,
                'location': event.facility.id if event.facility else None,  # ใช้ชื่อของ facility แทน
                'activity': event.event.id if event.event else None, 
                'color': event.color,
            })
        return render(request, "calendar.html", {
            'student': student,
            'form': CalendarForm(),
            'events': json.dumps(events_list)  # แปลง events เป็น JSON string เพื่อใช้ใน JavaScript
        })
        
    def post(self, request):
        
        try:
            student = Student.objects.get(student_user=request.user)

            # อ่านข้อมูล JSON จาก request.body
            data = json.loads(request.body)
            event_id = data.get('event_id')
            location_id = data.get('location') 
            activity_id = data.get('activity')
            location = None 
            activity = None
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error','message': 'Invalid JSON data'
            }, status=400)
                    
        if event_id:
            try:
                schedule = Schedule.objects.get(id=event_id, student=student)
            except Schedule.DoesNotExist:
                return JsonResponse({'status': 'error','message': 'Event not found'
                }, status=404)
        else:
            # ถ้าไม่มี event_id แสดงว่าสร้างกิจกรรมใหม่
            schedule = Schedule()

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
            
        # ใช้ข้อมูล JSON ในการสร้างหรืออัปเดตฟอร์ม
        form = CalendarForm(data, instance=schedule)  # ถ้ามี instance จะเป็นการอัปเดต
        
        if form.is_valid():
            schedule = form.save(commit=False)
            
            if location:  # ตรวจสอบว่ามี location หรือไม่
                schedule.facility = location

            if activity:  # ตรวจสอบว่ามี activity หรือไม่
                schedule.event = activity

            schedule.student = student 
            
            schedule.save()  # บันทึกกิจกรรมลงในฐานข้อมูล

            # แสดงข้อความตามการทำงาน create หรือ update

            return JsonResponse({
                'status': 'success',
                'event_id': schedule.id,
                'message': 'Event updated successfully!' # ส่งข้อความกลับไป
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }, status=400)

            
            
    def delete(self, request, event_id):
        try:
            student = Student.objects.get(student_user=request.user)
        except Student.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Student not found'
            }, status=404)

        try:
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