from django.shortcuts import render, redirect
from django.views import View
from .models import *

class SignInPage(View):
    
    def get(self, request):
        return render(request, "login.html",{

        })
        

class SignUpPage(View):
    
    def get(self, request):
        return render(request, "register.html",{

        })

class CalendarPage(View):
    
    def get(self, request):
        return render(request, "calendar.html",{

        })   