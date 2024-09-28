from django.urls import path
from . import views

urlpatterns = [
    path("event-list/", views.EventListPage.as_view(), name="event-list"),
    path("create-event/", views.CreateEventPage.as_view(), name="create-event"),
    path('event/', views.EventDetailPage.as_view(), name='event-detail'),
    path('edit-event/', views.EditEventPage.as_view(), name='edit-event'),

    path("", views.BookingListPage.as_view(), name="book-list"),
    path("book-first/", views.BookFirstPage.as_view(), name="book-first"),
    path('book-second/', views.BookSecondPage.as_view(), name='book-second'),
    path('book-third/', views.BookThirdPage.as_view(), name='book-third'),
    path("upcoming/", views.UpcomingBookPage.as_view(), name="upcoming"),
    path('past-book/', views.PastBookPage.as_view(), name='past-book'),
    path('book-detail/', views.BookDetailPage.as_view(), name='book-detail'),
    path('book-staff/', views.StaffBookPage.as_view(), name='book-staff'),

    path('facilities/', views.FacilitiesPage.as_view(), name='facilities'),
]
