from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from apps.game.models import Player
import random

User = get_user_model()


LOTTERY_STATUS = (('live', 'Live'), ('hold', 'Hold'), ('finished', 'Finished'), ('stop', 'Stop'))


class Lottery(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ticket_price = models.PositiveSmallIntegerField(default=0)
    ticket_number_digits = models.PositiveSmallIntegerField(default=6)
    start_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    lottery_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LOTTERY_STATUS, default='stop')

    def __str__(self):
        return f"{self.title}"


class LotteryPrises(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='prises')
    prise_order = models.PositiveSmallIntegerField(default=1)
    quantity = models.PositiveSmallIntegerField(default=1)
    prise_money = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prise_money}"


class Ticket(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='tickets')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ticket_buyers')
    ticker_number = models.PositiveIntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        six_digit_random_number = random.randint(100000, 999999)
        self.ticker_number = six_digit_random_number
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['lottery', 'ticker_number']

    def __str__(self):
        return f"{self.ticker_number}"


class LotteryWinners(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

