from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),
    path("auth/", include("authen.urls")),
    path("booking/", include("bookings.urls")),
    path("chat/", include("chat.urls")),
    path("planner/", include("planner.urls")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)