# Generated by Django 4.2.6 on 2023-11-24 20:51

import datetime
from django.conf import settings
import django.core.validators
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
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('min_bet', models.PositiveSmallIntegerField(default=5)),
                ('max_bet', models.PositiveSmallIntegerField(default=100)),
                ('bet_increment', models.PositiveSmallIntegerField(default=5)),
                ('auto_draw', models.BooleanField(default=True)),
                ('auto_draw_cycle', models.DurationField(default=datetime.timedelta(seconds=120))),
                ('betting_off_time', models.DurationField(default=datetime.timedelta(seconds=10))),
                ('status', models.CharField(choices=[('stop', 'Stop'), ('live', 'Live')], default=('stop', 'Stop'), max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='board_agent', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DicePlayerBettingCoins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spade', models.PositiveIntegerField(default=0)),
                ('club', models.PositiveIntegerField(default=0)),
                ('diamond', models.PositiveIntegerField(default=0)),
                ('heart', models.PositiveIntegerField(default=0)),
                ('munda', models.PositiveIntegerField(default=0)),
                ('jhandi', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DrawAlgo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='JhandiDraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spade', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('club', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('diamond', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('heart', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('munda', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('jhandi', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('draw_datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('1', 'Live'), ('2', 'Finished')], max_length=20)),
                ('betting_players', models.ManyToManyField(related_name='betting_players', through='dice.DicePlayerBettingCoins', to='game.player')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dice.board')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerDiceBettingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spade', models.SmallIntegerField(default=0)),
                ('club', models.SmallIntegerField(default=0)),
                ('diamond', models.SmallIntegerField(default=0)),
                ('heart', models.SmallIntegerField(default=0)),
                ('munda', models.SmallIntegerField(default=0)),
                ('jhandi', models.SmallIntegerField(default=0)),
                ('resulted_coins', models.IntegerField(default=0, editable=False)),
                ('draw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dice.jhandidraw')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
            ],
        ),
        migrations.CreateModel(
            name='LiveBoardPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spade', models.PositiveIntegerField(default=0)),
                ('club', models.PositiveIntegerField(default=0)),
                ('diamond', models.PositiveIntegerField(default=0)),
                ('heart', models.PositiveIntegerField(default=0)),
                ('munda', models.PositiveIntegerField(default=0)),
                ('jhandi', models.PositiveIntegerField(default=0)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dice.board')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player')),
            ],
            options={
                'unique_together': {('player', 'board')},
            },
        ),
        migrations.AddField(
            model_name='jhandidraw',
            name='draw_result',
            field=models.ManyToManyField(through='dice.PlayerDiceBettingResult', to='game.player'),
        ),
        migrations.AddField(
            model_name='diceplayerbettingcoins',
            name='draw',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dice.jhandidraw'),
        ),
        migrations.AddField(
            model_name='diceplayerbettingcoins',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.player'),
        ),
        migrations.CreateModel(
            name='BoardLiveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('live_players_count', models.PositiveIntegerField(default=0, editable=False)),
                ('total_betting_on_jhandi', models.PositiveBigIntegerField(default=0, editable=False)),
                ('total_betting_on_munda', models.PositiveBigIntegerField(default=0, editable=False)),
                ('total_betting_on_spade', models.PositiveBigIntegerField(default=0, editable=False)),
                ('total_betting_on_club', models.PositiveBigIntegerField(default=0, editable=False)),
                ('total_betting_on_diamond', models.PositiveBigIntegerField(default=0, editable=False)),
                ('total_betting_on_heart', models.PositiveBigIntegerField(default=0, editable=False)),
                ('board', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dice.board')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='draw_algo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dice.drawalgo'),
        ),
        migrations.AddField(
            model_name='board',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.game'),
        ),
        migrations.AddField(
            model_name='board',
            name='live_players',
            field=models.ManyToManyField(related_name='live_players', through='dice.LiveBoardPlayers', to='game.player'),
        ),
        migrations.AlterUniqueTogether(
            name='diceplayerbettingcoins',
            unique_together={('player', 'draw')},
        ),
    ]
