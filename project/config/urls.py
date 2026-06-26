from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',   include('users.urls')),
    path('api/records/', include('records.urls')),
    path('users/',       include('users.template_urls')),
    path('',             include('users.root_urls')),
    path('',             include('records.template_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)