from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
from apps.game.models import  Game, Player

User = get_user_model()

auto_draw_cycle_duration = timedelta(minutes=2)
betting_off_time_duration = timedelta(seconds=10)
SIDES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6)
)
BOARD_STATUS = (
    ('stop', 'Stop'),
    ('live', "Live")
)


class Dice:
    jhandi = 1
    munda = 2
    spade = 3
    club = 4
    diamond = 5
    heart = 6

    def draw(self):
        pass

    
class DrawAlgo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class Board(models.Model):
    title = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE,  blank=True, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='board_agent')
    min_bet = models.PositiveSmallIntegerField(default=5)
    max_bet = models.PositiveSmallIntegerField(default=100)
    bet_increment = models.PositiveSmallIntegerField(default=5)
    auto_draw = models.BooleanField(default=True)
    auto_draw_cycle = models.DurationField(default=auto_draw_cycle_duration)
    draw_algo = models.OneToOneField(DrawAlgo, blank=True, null=True, on_delete=models.CASCADE)
    betting_off_time = models.DurationField(default=betting_off_time_duration)
    live_players = models.ManyToManyField(to=Player, through='LiveBoardPlayers', related_name='live_players')
    status = models.CharField(max_length=20, choices=BOARD_STATUS, default=BOARD_STATUS[0])

    created_by = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            boardlivedata = self.boardlivedata
        except:
            BoardLiveData.objects.create(board=self)
        
        return super().save(*args, **kwargs)
    
    @property
    def live_players_count(self):
        return self.boardlivedata.live_players_count


class BoardLiveData(models.Model):
    board = models.OneToOneField(Board, on_delete=models.CASCADE)
    live_players_count = models.PositiveIntegerField(default=0, editable=False)
    total_betting_on_jhandi = models.PositiveBigIntegerField(default=0, editable=False)
    total_betting_on_munda = models.PositiveBigIntegerField(default=0, editable=False)
    total_betting_on_spade = models.PositiveBigIntegerField(default=0, editable=False)
    total_betting_on_club = models.PositiveBigIntegerField(default=0, editable=False)
    total_betting_on_diamond = models.PositiveBigIntegerField(default=0, editable=False)
    total_betting_on_heart = models.PositiveBigIntegerField(default=0, editable=False)

    def update(self):
        betting_players = self.board.live_players.all()
        dice = {
            "jhandi": 0,
            "munda": 0,
            "spade": 0,
            "club": 0,
            "diamond": 0,
            "heart": 0
        }
        liveboardplayers = LiveBoardPlayers.objects.filter(board=self.board)
        for liveboardplayer in liveboardplayers:
            
            dice['jhandi'] = dice['jhandi'] + liveboardplayer.jhandi
            dice['munda'] = dice['munda'] + liveboardplayer.munda
            dice['spade'] = dice['spade'] + liveboardplayer.spade
            dice['club'] = dice['club'] + liveboardplayer.club
            dice['diamond'] = dice['diamond'] + liveboardplayer.diamond
            dice['heart'] = dice['heart'] + liveboardplayer.heart
        
        self.total_betting_on_jhandi = dice.get('jhandi')
        self.total_betting_on_munda = dice.get('munda')
        self.total_betting_on_spade = dice.get('spade')
        self.total_betting_on_club = dice.get('club')
        self.total_betting_on_diamond = dice.get('diamond')
        self.total_betting_on_heart = dice.get('heart')
        self.save()


class LiveBoardPlayers(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    spade = models.PositiveIntegerField(default=0)
    club = models.PositiveIntegerField(default=0)
    diamond = models.PositiveIntegerField(default=0)
    heart = models.PositiveIntegerField(default=0)
    munda = models.PositiveIntegerField(default=0)
    jhandi = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['player', 'board']


class JhandiDraw(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    betting_players = models.ManyToManyField(to=Player, through='DicePlayerBettingCoins', related_name='betting_players')
    draw_result = models.ManyToManyField(to=Player, through='PlayerDiceBettingResult')
    # following fields hold the result after draw
    spade = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    club = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    diamond = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    heart = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    munda = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    jhandi = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    draw_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('1', 'Live'), ('2', 'Finished')))

    def draw_board_coins(self):
        betting_players = self.betting_players
        dice = {
            "jhandi": 0,
            "munda": 0,
            "spade": 0,
            "club": 0,
            "diamond": 0,
            "heart": 0
        }
        for bet in betting_players:
            dice['jhandi'] = dice['jhandi'] + bet.jhandi
            dice['munda'] = dice['munda'] + bet.munda
            dice['spade'] = dice['spade'] + bet.spade
            dice['club'] = dice['club'] + bet.club
            dice['diamond'] = dice['diamond'] + bet.diamond
            dice['heart'] = dice['heart'] + bet.heart
        return dice


class DicePlayerBettingCoins(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draw = models.ForeignKey(JhandiDraw, on_delete=models.CASCADE)
    spade = models.PositiveIntegerField(default=0)
    club = models.PositiveIntegerField(default=0)
    diamond = models.PositiveIntegerField(default=0)
    heart = models.PositiveIntegerField(default=0)
    munda = models.PositiveIntegerField(default=0)
    jhandi = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['player', 'draw']


# class DiceDrawResult(models.Model):
#     draw = models.ForeignKey(JhandiDraw, on_delete=models.CASCADE)
#     spade = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
#     club = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
#     diamond = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
#     heart = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
#     munda = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
#     jhandi = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])



class PlayerDiceBettingResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    draw = models.ForeignKey(JhandiDraw, on_delete=models.CASCADE)
    spade = models.SmallIntegerField(default=0)
    club = models.SmallIntegerField(default=0)
    diamond = models.SmallIntegerField(default=0)
    heart = models.SmallIntegerField(default=0)
    munda = models.SmallIntegerField(default=0)
    jhandi = models.SmallIntegerField(default=0)
    resulted_coins = models.IntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        amount = [self.spade, self.club, self.diamond, self.heart, self.munda, self.jhandi]
        self.resulted_coins = sum(amount)
        return super().save(*args, **kwargs)