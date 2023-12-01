from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.game.models import Player
from .models import Board, LiveBoardPlayers
from .serializers import GameSerializer, LobbySerializer, BoardSerializer, BoardLiveDataSerializer


class LobbyApiView(generics.ListAPIView):
    queryset = Board.objects.filter(status='live')
    serializer_class = LobbySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        player = {
            "player_id": user.player.player_id,
            "wallet_id": user.wallet.wallet_id, 
            "balance": user.wallet.balance,
            "wallet_status": user.wallet.status
        }
        data = {
            "profile": player,
            "boards": serializer.data
        }
        return Response(data=data)


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Board.objects.filter(status='live')
    serializer_class = BoardSerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk):
        board = Board.objects.get(pk=pk)
        boardlivedata = board.boardlivedata
        player = request.user.player
        lp, created = LiveBoardPlayers.objects.get_or_create(
            player=player,
            board=board
        )
        if created:
            boardlivedata.live_players_count += 1
            boardlivedata.save()
        
        board_serializer = BoardLiveDataSerializer(instance=boardlivedata)

        return Response(board_serializer.data)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk):
        board = Board.objects.get(pk=pk)
        boardlivedata = board.boardlivedata
        player = request.user.player
        try:
            lp = LiveBoardPlayers.objects.get(
                player=player,
                board=board
            )
            lp.delete()
            boardlivedata.live_players_count -= 1
            boardlivedata.save()
        except:
            pass
        
        boards = Board.objects.filter(status='live')
        board_serializer = BoardSerializer(instance=boards, many=True)

        return Response(board_serializer.data)
    
    @action(detail=True, methods=['post'])
    def refresh(self, request, pk):
        # import pdb; pdb.set_trace()
        req_data = request.data
        player_id = req_data.get('player_id')
        balance = req_data.get('balance')
        live_data = req_data.get('live_board_data')
        
        player = Player.objects.get(player_id=player_id)
        wallet = player.user.wallet
        board = Board.objects.get(pk=pk)
        boardlivedata = board.boardlivedata
        try:
            board_player = LiveBoardPlayers.objects.get(board=board, player=player)
        except LiveBoardPlayers.DoesNotExist:
            return Response({"error": "Not valied request", "result": "LiveBoardPlayers.DoesNotExist"})
        board_player.jhandi = live_data.get('jhandi')
        board_player.munda = live_data.get('munda')
        board_player.spade = live_data.get('spade')
        board_player.club = live_data.get('club')
        board_player.diamond = live_data.get('diamond')
        board_player.heart = live_data.get('heart')
        board_player.save()
        boardlivedata.update()
        serializer = BoardLiveDataSerializer(instance=boardlivedata)
        data = {
            "boards": serializer.data
        }
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def drawdice(self, request, pk):
        req_data = request.data
        player_id = req_data.get('player_id')
        balance = req_data.get('balance')
        live_data = req_data.get('live_board_data')
        player = Player.objects.get(id=player_id)
        board = Board.objects.get(pk=pk)
        boardlivedata = board.boardlivedata
        dice_serializer = BoardLiveDataSerializer(instance=boardlivedata)
        data = dice_serializer.data
        return Response({"result": data})
