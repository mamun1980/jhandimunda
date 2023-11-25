from django.contrib import admin
from .models import (
    Board, LiveBoardPlayers, JhandiDraw, DrawAlgo,
    DicePlayerBettingCoins, PlayerDiceBettingResult, BoardLiveData
)



@admin.register(DrawAlgo)
class DrarAlgoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_bet', 'max_bet', 'status']


@admin.register(BoardLiveData)
class BoardLiveDataAdmin(admin.ModelAdmin):
    list_display = [
        'board', 'live_players_count', 'total_betting_on_jhandi', 'total_betting_on_munda',
        'total_betting_on_spade', 'total_betting_on_club', 'total_betting_on_diamond', 'total_betting_on_heart'
        ]


@admin.register(LiveBoardPlayers)
class LiveBoardPlayersAdmin(admin.ModelAdmin):
    list_display = ['player', 'board']


@admin.register(JhandiDraw)
class JhandiDrawAdmin(admin.ModelAdmin):
    list_display = ['board', 'draw_datetime']


@admin.register(DicePlayerBettingCoins)
class DicePlayerBettingCoinsAdmin(admin.ModelAdmin):
    list_display = ['player', 'draw', 'spade', 'club', 'diamond', 'heart', 'munda', 'jhandi']


@admin.register(PlayerDiceBettingResult)
class PlayerDiceBettingResultAdmin(admin.ModelAdmin):
    list_display = ['player', 'draw', 'spade', 'club', 'diamond', 'heart', 'munda', 'jhandi', 'resulted_coins']