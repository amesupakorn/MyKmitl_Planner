from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View

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
            message_sent = Message.objects.filter(staff=staff, student_id=student_id, status='sent').count()
            message_info.append({
                'last_message': last_message,
                'message_sent': message_sent,
                'student_id' : student_id
            })

        return render(request, "staff/chat-list.html", {
            'message_info': message_info,  
        })
class ChatDetailStudent(APIView):
    authentication_classes = [SessionAuthentication] 
    permission_classes = [IsAuthenticated, ChatMessagePermission]

    def get(self, request, id):
        

        try:
            staff = UniversityStaff.objects.get(staff_user=request.user)
        except UniversityStaff.DoesNotExist:
            return Response({"error": "You are not authorized to view this content."}, status=403)
        
        student = Student.objects.get(student_user=id)
        

        if request.headers.get('Accept') == 'application/json':
            messages = Message.objects.filter(student_id=student).order_by('timestamp')
            for message in messages:
                self.check_object_permissions(request, message)


            serializer = MessageSerializer(messages, many=True)

            data = {
                "user_role": 'staff',
                "studentId": student.id,
                "student_name": student.first_name,
                "messages": serializer.data
            }
            return Response(data) 

        return render(request, "staff/chat-student.html", {
            'student': student
        })
    
    def post(self, request, id, format=None):
        student = Student.objects.get(student_user_id=id)
        previous_message = Message.objects.filter(student=student).first()
        selected_staff = previous_message.staff

        try:
            with transaction.atomic():
                data = request.data.copy()
                data['student'] = student.id
                data['staff'] = selected_staff.id
                
                # Mark previous message as read
                if previous_message:
                    previous_message.mark_as_read()

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
            data = {
                "user_role": 'student',
                "messages": serializer.data
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
    

