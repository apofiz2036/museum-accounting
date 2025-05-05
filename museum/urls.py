from django.contrib import admin
from django.urls import path
from events.views import main
from django.conf import settings
from django.conf.urls.static import static

from events.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
