from django.urls import path
from . import views

urlpatterns = [
     path("calendar", views.CalendarPage.as_view(), name="calendar")
     
]
