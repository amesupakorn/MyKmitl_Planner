from django.shortcuts import render, redirect
from django.views import View
from .models import *

class MainView(View):
    
    def get(self, request):
        student = Student.objects.get(pk=1)
        return render(request, "index.html",{
            "student" : student,
        })
        
        