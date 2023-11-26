from django.urls import path, include
from .views import LotteryListView, LotteryDetailView, TicketListView, TicketDetailView, TicketCreateView, MyTicketListView, LotteryWinnersList

app_name = "lottery"


urlpatterns = [
    path("", LotteryListView.as_view(), name="lottery-list"),
    path("my-results/", MyTicketListView.as_view(), name="my-results"),
    path("all-results/", LotteryWinnersList.as_view(), name="all-results"),
    path("tickets/", TicketListView.as_view(), name="tickets"),
    path("my-tickets/", MyTicketListView.as_view(), name="my-tickets"),
    path("<pk>/", LotteryDetailView.as_view(), name="lottery-detail"),
    path("tickets/<pk>/", TicketDetailView.as_view(), name="tickets-detail"),
    path("<lottery_id>/tickets-buy/", TicketCreateView.as_view(), name="tickets-buy"),
    
]
