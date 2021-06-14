from django.urls import include, path
from django.conf.urls.static import static
from project.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('api/', include('api.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
