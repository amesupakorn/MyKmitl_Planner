from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecommendListPage.as_view(), name="event-list"),
    path("create-event/", views.CreateEventPage.as_view(), name="create-event"),
    path('event/', views.EventDetailPage.as_view(), name='event-detail'),
]
