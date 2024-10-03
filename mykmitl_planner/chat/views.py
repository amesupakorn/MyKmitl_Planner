from django.shortcuts import render, redirect
from django.views import View
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import MessageSerializer
import random


# Create your views here.
class ChatListPage(View):
    
    def get(self, request):
        return render(request, "staff/chat-list.html",{

        })
        

class ChatHelpPage(View):
    
    def get(self, request):
        return render(request, "chat-help.html",{

        })      


class ChatPage(APIView):
    def get(self, request):
        
         # ตรวจสอบว่าผู้ใช้เป็น student หรือ staff
        if hasattr(request.user, 'student'):
            user_role = 'student'
            sender = Student.objects.get(student_user = request.user)
        elif hasattr(request.user, 'staff'):
            user_role = 'staff'
            sender = UniversityStaff.objects.get(staff_user = request.user)
        else:
            user_role = 'unknown'

            
        return render(request, "chat.html", {
            'user_role': user_role,
            'sender' : sender
        })
    

class MessageList(APIView):
    def get(self, request, format=None):
        student = Student.objects.get(student_user=request.user)
        messages = Message.objects.filter(student_id=student)# ดึงข้อความทั้งหมด
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

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


        data = request.data.copy()
        data['student'] = student.id  
        data['staff'] = selected_staff.id 
        print(data)
        serializer = MessageSerializer(data=data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
