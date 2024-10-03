from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatListPage.as_view(), name="chat-list"),
    path("chat-detail/", views.ChatPage.as_view(), name="chat"),
    path("chat-help/", views.ChatHelpPage.as_view(), name="chat-help"),
    path("chat-detail/message/", views.MessageList.as_view(), name="message")

]
