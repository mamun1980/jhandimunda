from django.urls import path
from .views import *

app_name='wallet'

urlpatterns = [
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('send-coin/', SendCoinView.as_view(), name='send-coin')
]