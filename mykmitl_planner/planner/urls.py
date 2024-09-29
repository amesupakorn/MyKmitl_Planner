from django.urls import path
from . import views

urlpatterns = [
     path("", views.CalendarPage.as_view(), name="planner_dashboard"),
     path('delete/<int:event_id>/', views.CalendarPage.as_view(), name='delete_event'),

]
