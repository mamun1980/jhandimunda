from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Game


class HomeView(TemplateView):
    template_name = "game/index.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/accounts/login/")
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()
        context['games'] = games
        return context
