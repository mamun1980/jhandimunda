from django.contrib import admin
from .models import *


class InlineLotteryPrise(admin.TabularInline):
    model = LotteryPrises


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    inlines = [InlineLotteryPrise]
    list_display = ['owner', 'title', 'ticket_price', 'start_date', 'lottery_date', 'status']


@admin.register(LotteryPrises)
class LotteryPrisesAdmin(admin.ModelAdmin):
    list_display = ['lottery', 'prise_money', 'prise_order', 'quantity']
    ordering = ['prise_order']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['lottery', 'player', 'ticker_number', 'purchase_date', 'expired']


@admin.register(LotteryWinners)
class LotteryWinnersAdmin(admin.ModelAdmin):
    list_display = ['ticket']

