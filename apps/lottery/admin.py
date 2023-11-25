from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
import random

from .models import *


class InlineLotteryPrise(admin.TabularInline):
    model = LotteryPrizes
    extra = 0


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    inlines = [InlineLotteryPrise]
    list_display = ['owner', 'title', 'ticket_price', 'start_date', 'lottery_date', 'status', 'draw_lottery']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/draw_lottery/', self.admin_site.admin_view(self.start_draw_lottery), name='start_draw_lottery'),
        ]
        return custom_urls + urls

    def draw_lottery(self, obj):
        if obj.status == 'live':
            return format_html(
                '<a class="button" href="{}">Draw Lottery</a>&nbsp;',
                    reverse('admin:start_draw_lottery', args=[obj.pk]),
                )
        else:
            return 'Completed'
    
    draw_lottery.short_description = 'Actions'
    draw_lottery.allow_tags = True

    def start_draw_lottery(self, request, object_id):
        lottery = Lottery.objects.get(id=object_id)
        tickets = list(lottery.tickets.all())
        prises = lottery.prises.all()
        for prise in prises:
            while prise.quantity > 0:
                prise.quantity -= 1
                winning_number = random.randint(000000, 999999)
                winner = LotteryWinners.objects.create(
                        prise=prise,
                        winning_number=winning_number
                    )
                
                try:
                    winning_ticket = Ticket.objects.get(ticker_number=winning_number)
                    winner.ticket = winning_ticket
                    winner.player = winning_ticket.player
                    winner.save()
                    winning_ticket.expired = True
                    winning_ticket.save()
                except Ticket.DoesNotExist as e:
                    pass
        
        lottery.status = 'finished'
        lottery.save()

        print("Lottery draw successful")


@admin.register(LotteryPrizes)
class LotteryPrisesAdmin(admin.ModelAdmin):
    list_display = ['lottery', 'prize_money', 'prize_order', 'quantity']
    ordering = ['prize_order']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['lottery', 'player', 'ticker_number', 'purchase_date', 'expired']
    list_filter = ['player']


@admin.register(LotteryWinners)
class LotteryWinnersAdmin(admin.ModelAdmin):
    list_display = ['winning_number', 'prize_money', 'prize_order', 'lottery', 'player']
    list_filter = ['prize__lottery']

