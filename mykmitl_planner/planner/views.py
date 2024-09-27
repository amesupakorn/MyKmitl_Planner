from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CalendarForm
from django.contrib import messages


class CalendarPage(View):
    
    def get(self, request):
        student = Student.objects.get(student_user=request.user)  # ดึงข้อมูลนักเรียนที่ล็อกอินอยู่
        schedules = Schedule.objects.filter(student=student)  # ดึงข้อมูลตารางกิจกรรมของนักเรียน
        form = CalendarForm()  # สร้างฟอร์มว่างสำหรับการเพิ่มกิจกรรมใหม่

        return render(request, "calendar.html", {
            'student': student,
            'schedules': schedules,
            'form': form,  # ส่งฟอร์มไปยังเทมเพลต
        })
        
    def post(self, request):
        print("dsdfs")
        student = Student.objects.get(student_user=request.user)  # ดึงนักเรียนจาก user ที่ล็อกอิน
        form = CalendarForm(request.POST)  # รับข้อมูลจากฟอร์มที่ถูกส่งมา
        

        if form.is_valid():
            print(form.errors)
            schedule = form.save(commit=False)  # บันทึกฟอร์มแต่ยังไม่ commit
            schedule.student = student  # กำหนดนักเรียนให้กับกิจกรรม
            schedule.save()  # บันทึกกิจกรรมลงในฐานข้อมูล
            messages.success('Your event has been successfully created')
            return redirect('planner_dashboard')  # เมื่อบันทึกสำเร็จ ให้ redirect ไปที่หน้า calendar เดิม

        # ถ้าฟอร์มไม่ผ่านการ validate ให้แสดงผลเดิมพร้อมกับฟอร์มที่มี error
        messages.error('Something went wrong while creating your event')
        schedules = Schedule.objects.filter(student=student)
        return render(request, "calendar.html", {
            'student': student,
            'schedules': schedules,
            'form': form,  # ส่งฟอร์มที่มี error กลับไปให้ผู้ใช้กรอกใหม่
        })
    