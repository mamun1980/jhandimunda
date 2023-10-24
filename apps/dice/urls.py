from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LobbyApiView, BoardViewSet


router = DefaultRouter()
router.register('boards', BoardViewSet, basename='game')
urlpatterns = router.urls


urlpatterns += [
    path('lobby/', LobbyApiView.as_view(), name='lobby'),
    # path('boards/<pk>/join/', BoardApiView.as_view(), name='dashboard')
]