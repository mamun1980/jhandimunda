from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import TemplateView
# from django.utils.translation import ugettext as _
from apps.dashboard.views import JMTemplateView



class HomeView(JMTemplateView):
    template_name = "game/index.html"


class MyAccountView(JMTemplateView):
    template_name = 'game/my-account.html'


class PlayerHomeView(JMTemplateView):
    template_name = 'players/home.html'
