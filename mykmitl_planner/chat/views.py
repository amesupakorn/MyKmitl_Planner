import json
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from datetime import timedelta
from django.utils import timezone

from .permissions import ChatMessagePermission
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import MessageSerializer
import random
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


# Create your views here.
class ChatListPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["chat.view_message"]
    
    def get(self, request):
        try:
            staff = UniversityStaff.objects.get(staff_user=request.user)
        except UniversityStaff.DoesNotExist:
            return HttpResponseForbidden("You are not authorized to view this page.")  
        
        staff = UniversityStaff.objects.get(staff_user=request.user)
        student_ids = Message.objects.filter(staff=staff).values_list('student', flat=True).distinct()

        # ดึงข้อความล่าสุดสำหรับแต่ละ student ที่สนทนากับ staff
        message_info = []
        for student_id in student_ids:
            last_message = Message.objects.filter(staff=staff, student_id=student_id).order_by('-timestamp').first()
            if last_message and last_message.timestamp:
                timestamp_utc = last_message.timestamp 
                timestamp_bangkok = timestamp_utc + timedelta(hours=7)
            message_sent = Message.objects.filter(staff=staff, student_id=student_id, status='sent').count()
            message_info.append({
                'last_message': last_message,
                'message_sent': message_sent,
                'student_id' : student_id,
                'timestamp': timestamp_bangkok
            })

        return render(request, "staff/chat-list.html", {
            'message_info': message_info,  
        })
class ChatDetailStudent(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, ChatMessagePermission]

    def get(self, request, id):
        # ตรวจสอบว่า user เป็น staff ที่ได้รับอนุญาตหรือไม่
        try:
            staff = UniversityStaff.objects.get(staff_user=request.user)
        except UniversityStaff.DoesNotExist:
            return Response({"error": "You are not authorized to view this content."}, status=403)

        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({"error": "Student does not exist."}, status=404)

        # ตรวจสอบว่า request มาจาก JSON หรือไม่
        if request.headers.get('Accept') == 'application/json':
            messages = Message.objects.filter(student_id=student).order_by('timestamp')

            # ตรวจสอบ permission ของแต่ละ message
            for message in messages:
                self.check_object_permissions(request, message)

            # Serialize ข้อมูล messages
            serializer = MessageSerializer(messages, many=True)
            serialized_data = serializer.data

            # ปรับ timestamp ให้เป็นเวลาท้องถิ่น (UTC+7)
            for message in serialized_data:
                timestamp = message.get('timestamp')
                if timestamp:
                    utc_time = timezone.datetime.fromisoformat(timestamp)
                    updated_time = utc_time + timedelta(hours=7)
                    message['timestamp'] = updated_time.isoformat()

            # เตรียมข้อมูล JSON response
            data = {
                "user_role": 'staff',
                "studentId": student.id,
                "student_name": student.first_name,
                "messages": serialized_data
            }
            return Response(data)

        # ถ้าไม่ใช่ JSON, render หน้า HTML
        return render(request, "staff/chat-student.html", {
            'student': student,
            'staff': staff,
        })
    
    def post(self, request, id, format=None):
        student = Student.objects.get(student_user_id=id)
        previous_message = Message.objects.filter(student=student, status='sent')
        staff = UniversityStaff.objects.get(staff_user = request.user)
        try:
            with transaction.atomic():
                data = request.data.copy()
                data['student'] = student.id
                data['staff'] = staff.id


                if previous_message:
                    for p in previous_message:
                        p.mark_as_read()

                # สร้างและ validate ข้อมูลใหม่
                serializer = MessageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChatHelpPage(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["chat.view_message"]
    
    def get(self, request):
        return render(request, "chat-help.html",{

        })      


class MessageList(APIView):
    authentication_classes = [SessionAuthentication]  
    permission_classes = [IsAuthenticated, ChatMessagePermission]

    def get(self, request, format=None):
        
        student = Student.objects.get(student_user=request.user)
        
        if request.headers.get('Accept') == 'application/json':
            messages = Message.objects.filter(student_id=student).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            serialized_data = serializer.data
            
            for message in serialized_data:
                timestamp = message['timestamp'] 
                if timestamp:
                    utc_time = timezone.datetime.fromisoformat(timestamp)
                    updated_time = utc_time + timedelta(hours=7)
                    
                    message['timestamp'] = updated_time.isoformat()

            # เตรียมข้อมูลสำหรับ Response
            data = {
                "user_role": 'student',
                "messages": serialized_data
            }
            return Response(data)
                
        return render(request, "chat.html", { })

        
    def post(self, request, format=None):
        student = Student.objects.get(student_user=request.user)
        
          # ตรวจสอบว่ามีข้อความที่เกี่ยวข้องกับ student นี้อยู่ในระบบแล้วหรือไม่
        previous_message = Message.objects.filter(student=student).first()

        if previous_message:
            selected_staff = previous_message.staff
        else:
            # ถ้าไม่มีข้อความ ให้สุ่มเลือกเจ้าหน้าที่ใหม่
            all_staff = UniversityStaff.objects.all()        
            selected_staff = random.choice(all_staff)
            
        try:
            with transaction.atomic():
                data = request.data.copy()
                data['student'] = student.id  
                data['staff'] = selected_staff.id
                
                serializer = MessageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

