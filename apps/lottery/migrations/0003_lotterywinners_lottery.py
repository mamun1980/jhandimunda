# Generated by Django 4.2.6 on 2023-11-26 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_ticket_is_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotterywinners',
            name='lottery',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='winners', to='lottery.lottery'),
            preserve_default=False,
        ),
    ]
