from django.shortcuts import render, redirect
from django.views import View
from .models import *

# Create your views here.
class RecommendListPage(View):
    
    def get(self, request):
        return render(request, "recommend-list.html",{

        })