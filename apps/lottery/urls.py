from django.urls import path, include
from .views import LotteryListView, LotteryDetailView, TicketListView, TicketDetailView, TicketCreateView

app_name = "lottery"


urlpatterns = [
    path("", LotteryListView.as_view(), name="lottery-list"),
    path("<pk>/", LotteryDetailView.as_view(), name="lottery-detail"),
    path("tickets/", TicketListView.as_view(), name="tickets"),
    path("tickets/<pk>/", TicketDetailView.as_view(), name="tickets-detail"),
    path("<lottery_id>/tickets-buy/", TicketCreateView.as_view(), name="tickets-buy")
]
