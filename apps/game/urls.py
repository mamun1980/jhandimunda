from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)