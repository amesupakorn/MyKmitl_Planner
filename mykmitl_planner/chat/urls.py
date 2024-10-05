from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatListPage.as_view(), name="chat-list"),
    path("chat-help/", views.ChatHelpPage.as_view(), name="chat-help"),
    path("chat-detail/message/", views.MessageList.as_view(), name="message"),
    path("chat-detail/<int:id>", views.ChatDetailStudent.as_view(), name="chat-student")
]
