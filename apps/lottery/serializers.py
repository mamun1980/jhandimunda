from rest_framework import serializers

from .models import Lottery, Ticket


class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = ['id', 'title', 'ticket_price', 'ticket_number_digits', 'start_date', 'lottery_date', 'status']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'lottery', 'player', 'ticker_number', 'purchase_date', 'expired']