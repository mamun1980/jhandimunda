from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import TemplateView
# from django.utils.translation import ugettext as _
from apps.dashboard.views import JMTemplateView



class HomeView(JMTemplateView):
    template_name = "game/index.html"


class AgentHomeView(JMTemplateView):
    template_name = 'agents/home.html'


class PlayerHomeView(JMTemplateView):
    template_name = 'players/home.html'
