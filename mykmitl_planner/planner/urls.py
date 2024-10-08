from django.urls import path
from . import views

urlpatterns = [
     path("", views.CalendarPage.as_view(), name="planner_dashboard"),
     path('delete/<int:event_id>/', views.CalendarPage.as_view(), name='delete_event'),
     
     path('dashboard/', views.DashboardView.as_view(), name='staff_dashboard'),
     path('dashboard/confirmed_bookings/', views.confirmed_bookings_chart_data.as_view(), name='confirm_dashboard'),

]
