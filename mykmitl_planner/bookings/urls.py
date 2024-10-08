from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("event-list/", views.EventListPage.as_view(), name="event-list"),
    path("create-event/", views.CreateEventPage.as_view(), name="create-event"),
    path('event/<int:id>', views.EventDetailPage.as_view(), name='event-detail'),
    path('edit-event/<int:id>', views.EditEventPage.as_view(), name='edit-event'),

    path("", views.BookingListPage.as_view(), name="book-list"),
    path("book-first/<str:location>", views.BookFirstPage.as_view(), name="book-first"),
    path('book-second/<int:id>', views.BookSecondPage.as_view(), name='book-second'),
    path('book-second/check-available-times/', views.CheckAvailableTimes.as_view(), name='check-available-times'),
    path('book-third/<int:id>', views.BookThirdPage.as_view(), name='book-third'),
    path('book-confirm/<int:id>', views.BookConfirm.as_view(), name='book-confirm'),

    path('upcoming/', views.UpcomingBookPage.as_view(), name='upcoming'),
    path('past-book/', views.PastBookPage.as_view(), name='past-book'),
    path('book-detail/<int:id>', views.BookDetailPage.as_view(), name='book-detail'),
    path('book-staff/', views.StaffBookPage.as_view(), name='book-staff'),

    path('facilities/', views.FacilitiesPage.as_view(), name='facilities'),
    path('facilities/edit/<int:id>/', views.EditFacilities.as_view(), name='edit-facility'),
    path('facilities/view/<int:id>/', views.ViewFacilities.as_view(), name='view-facility'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)