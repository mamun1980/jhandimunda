from rest_framework import serializers
from .models import Game, Board, BoardLiveData


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['name']


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'min_bet', 'max_bet', 'auto_draw', 'live_players_count']
    
    def to_representation(self, instance):
        data = {
            "data": "Mamun"
        }
        # return data
        return super().to_representation(instance)


class BoardLiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardLiveData
        fields = '__all__'
    
    def to_representation(self, instance):
        data = {
            "jhandi": instance.total_betting_on_jhandi,
            "munda": instance.total_betting_on_munda,
            "spade": instance.total_betting_on_spade,
            "club": instance.total_betting_on_club,
            "diamond": instance.total_betting_on_diamond,
            "heart": instance.total_betting_on_heart,
            "live_players_count": instance.live_players_count
        }
        return data
        


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'min_bet', 'max_bet', 'auto_draw', 'live_players_count']