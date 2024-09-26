from django.shortcuts import render, redirect
from django.views import View
from .models import *

# Create your views here.
class ChatListPage(View):
    
    def get(self, request):
        return render(request, "chat-list.html",{

        })

class ChatHelpPage(View):
    
    def get(self, request):
        return render(request, "chat-help.html",{

        })      

class ChatPage(View):
    
    def get(self, request):
        return render(request, "chat.html",{

        })   