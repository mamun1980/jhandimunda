from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.dice.views import LobbyApiView, BoardViewSet
from apps.lottery.views import LotteryViewSet, TicketViewSet
from apps.wallet.views import WalletViewSet


router = DefaultRouter()
router.register('boards', BoardViewSet, basename='game')
router.register('lotteries', LotteryViewSet, basename='lottery')
router.register('tickets', TicketViewSet, basename='ticket')
router.register('wallets', WalletViewSet, basename='wallet')

urlpatterns = router.urls

urlpatterns += [
    path('lobby/', LobbyApiView.as_view(), name='lobby'),
    # path('boards/<pk>/join/', BoardApiView.as_view(), name='dashboard')
]