from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'user', 'balance', 'status']
    filter_list = ['user']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'from_wallet', 'to_wallet', 'amount', 'transaction_date']
    list_filter = ['from_wallet', 'to_wallet', 'transaction_date']
    