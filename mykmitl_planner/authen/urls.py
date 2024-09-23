from django.urls import path
from . import views

urlpatterns = [
     path("", views.SignInPage.as_view(), name="signin"),
     path("signup", views.SignUpPage.as_view(), name="signup"),
     
]
