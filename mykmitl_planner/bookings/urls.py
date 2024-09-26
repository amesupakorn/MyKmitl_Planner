from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecommendListPage.as_view(), name="recommend-list"),
     
]
