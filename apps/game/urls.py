from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import HomeView, AgentHomeView, PlayerHomeView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    # path('agents/', AgentHomeView.as_view(), name='agents-home'),
    # path('players/', PlayerHomeView.as_view(), name='players-home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)