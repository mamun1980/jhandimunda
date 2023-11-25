# Generated by Django 4.2.6 on 2023-11-24 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ticket_price', models.PositiveSmallIntegerField(default=0)),
                ('ticket_number_digits', models.PositiveSmallIntegerField(default=6)),
                ('start_date', models.DateTimeField(auto_now=True, null=True)),
                ('lottery_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('live', 'Live'), ('hold', 'Hold'), ('finished', 'Finished'), ('stop', 'Stop')], default='stop', max_length=20)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LotteryPrizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize_order', models.PositiveSmallIntegerField(default=1)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('prize_money', models.PositiveIntegerField(default=0)),
                ('lottery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prizes', to='lottery.lottery')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_number', models.PositiveIntegerField(default=0)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('expired', models.BooleanField(default=False, editable=False)),
                ('lottery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='lottery.lottery')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_buyers', to='game.player')),
            ],
            options={
                'unique_together': {('lottery', 'ticker_number')},
            },
        ),
        migrations.CreateModel(
            name='LotteryWinners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winning_number', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.player')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lottery.lotteryprizes')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lottery.ticket')),
            ],
        ),
    ]
