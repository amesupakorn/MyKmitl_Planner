from django.shortcuts import render
from django.views import View
from planner.models import *


class SignInPage(View):
    
    def get(self, request):
        return render(request, "login.html",{

        })
        

class SignUpPage(View):
    
    def get(self, request):
        return render(request, "register.html",{

        })