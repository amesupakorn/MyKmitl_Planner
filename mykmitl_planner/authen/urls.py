from django.urls import path
from . import views

urlpatterns = [
     path("", views.SignInPage.as_view(), name="account_login"),
     path("signup", views.SignUpPage.as_view(), name="account_signup"),
     path("forgot", views.SignUpPage.as_view(), name="account_reset_password"),
     
     
     
]
