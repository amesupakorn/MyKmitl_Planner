from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatPage.as_view(), name="chat")
]
