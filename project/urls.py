
from django.urls import include, path
from django.conf.urls.static import static
from project.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
