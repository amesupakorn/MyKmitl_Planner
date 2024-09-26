from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path("", views.SignInPage.as_view(), name="account_login"),
     path("signup", views.SignUpPage.as_view(), name="account_signup"),
     path("forgot", views.SignUpPage.as_view(), name="account_reset_password"),
     path("logout", views.LogOutPage.as_view(), name="account_logout"),
     path('email-confirmemail_sent/', views.EmailConfirmationSentView.as_view(), name='account_email_confirmation'),
     path('profile/', views.EditProfile.as_view(), name='profile'),
     path('password/change/', views.PasswordChangeView.as_view(), name='account_change_password')

     
]