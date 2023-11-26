from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from apps.game.models import Player
import random

User = get_user_model()


LOTTERY_STATUS = (('live', 'Live'), ('hold', 'Hold'), ('finished', 'Finished'), ('stop', 'Stop'))


class Lottery(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    ticket_price = models.PositiveSmallIntegerField(default=0)
    ticket_number_digits = models.PositiveSmallIntegerField(default=6)
    start_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    lottery_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LOTTERY_STATUS, default='stop')

    def __str__(self):
        return f"{self.title}"

    def get_short_description(self):
        # import pdb; pdb.set_trace()
        prizes = self.prizes.all()
        first_prize = 0
        total_prize_money = 0
        total_prize_count = 0
        for prize in prizes:
            if prize.prize_order == 1:
                first_prize = prize.prize_money
            total_prize_count += prize.quantity
            total_prize_money += prize.prize_money * prize.quantity

        short_desc = f"{first_prize} টাকার প্রথম পুরষ্কার সহ সর্বমোট {total_prize_money} টাকার {total_prize_count} টি পুরস্কার"

        return short_desc


class LotteryPrizes(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='prizes')
    prize_order = models.PositiveSmallIntegerField(default=1)
    quantity = models.PositiveSmallIntegerField(default=1)
    prize_money = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prize_money}"


class Ticket(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='tickets')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ticket_buyers')
    ticker_number = models.PositiveIntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False, editable=False)
    is_winner = models.BooleanField(default=False, editable=False)

    # def save(self, *args, **kwargs):
    #     six_digit_random_number = random.randint(100000, 999999)
    #     self.ticker_number = six_digit_random_number
    #     return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['lottery', 'ticker_number']

    def __str__(self):
        return f"{self.ticker_number}"


class LotteryWinners(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='winners')
    prize = models.ForeignKey(LotteryPrizes, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    winning_number = models.PositiveIntegerField(default=0)

    @property
    def prize_money(self):
        return self.prize.prize_money
    
    @property
    def prize_order(self):
        return self.prize.prize_order
