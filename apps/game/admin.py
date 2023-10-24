from django.contrib import admin
from .models import Game, Player
from .forms import GameForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = GameForm

    def get_form(self, request, *args, **kwargs):
        form = super(GameAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user']
