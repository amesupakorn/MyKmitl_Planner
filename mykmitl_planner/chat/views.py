from django.shortcuts import render, redirect
from django.views import View
from .models import *

# Create your views here.
class ChatPage(View):
    
    def get(self, request):
        return render(request, "chat.html",{

        })   