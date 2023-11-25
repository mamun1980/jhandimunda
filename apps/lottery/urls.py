from django.urls import path, include
from .views import LotteryListView, LotteryDetailView, TicketListView, TicketDetailView, TicketCreateView, MyTicketListView

app_name = "lottery"


urlpatterns = [
    path("", LotteryListView.as_view(), name="lottery-list"),
    path("tickets/", TicketListView.as_view(), name="tickets"),
    path("my-tickets/", MyTicketListView.as_view(), name="my-tickets"),
    path("<pk>/", LotteryDetailView.as_view(), name="lottery-detail"),
    path("tickets/<pk>/", TicketDetailView.as_view(), name="tickets-detail"),
    path("<lottery_id>/tickets-buy/", TicketCreateView.as_view(), name="tickets-buy")
]
