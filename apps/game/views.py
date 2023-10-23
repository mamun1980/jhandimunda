from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Game


class HomeView(TemplateView):
    template_name = "game/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()
        context['title'] = 'Jhandi'
        context['games'] = games
        return context
