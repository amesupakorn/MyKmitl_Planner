from django.shortcuts import render, redirect
from django.views import View
from .models import *

# Create your views here.
class EventListPage(View):
    
    def get(self, request):
        return render(request, "event/event-list.html",{

        })
    
class CreateEventPage(View):
    
    def get(self, request):
        return render(request, "event/create-event.html",{

        })

class EditEventPage(View):
    
    def get(self, request):
        return render(request, "event/edit-event.html",{

        })
    
class EventDetailPage(View):
    
    def get(self, request):
        return render(request, "event/event-detail.html",{

        })
    

class BookingListPage(View):
    
    def get(self, request):
        return render(request, "booking/book-list.html",{

        })
    
class BookFirstPage(View):
    
    def get(self, request):
        return render(request, "booking/book-first.html",{

        })

class BookSecondPage(View):
    
    def get(self, request):
        return render(request, "booking/book-second.html",{

        })
    
class BookThirdPage(View):
    
    def get(self, request):
        return render(request, "booking/book-third.html",{

        })
    
class UpcomingBookPage(View):
    
    def get(self, request):
        return render(request, "booking/upcoming.html",{

        })

class PastBookPage(View):
    
    def get(self, request):
        return render(request, "booking/past-book.html",{

        })
    
class PastDetailPage(View):
    
    def get(self, request):
        return render(request, "booking/past-detail.html",{

        })