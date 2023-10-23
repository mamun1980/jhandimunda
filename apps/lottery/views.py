from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
# from django.views.generic.edit import CreateView, DeleteView


from .models import *


class LotteryListView(ListView):
    template_name = "lottery/index.html"

    class Meta:
        model = Lottery

    def get_queryset(self):
        qs = Lottery.objects.filter(status='live')
        return qs


class LotteryDetailView(DetailView):
    template_name = "lottery/lottery_detail.html"
    queryset = Lottery.objects.all()

    class Meta:
        model = Lottery


class TicketListView(ListView):
    template_name = "lottery/ticket_list.html"

    class Meta:
        model = Ticket

    def get_queryset(self):
        user = self.request.user
        player = user.player
        qs = Ticket.objects.filter(player=player, expired=False)
        return qs


class TicketDetailView(DetailView):
    template_name = "lottery/ticket_detail.html"
    queryset = Ticket.objects.all()

    class Meta:
        model = Ticket


class TicketCreateView(CreateView):
    template_name = "lottery/ticket_create.html"
    model = Ticket
    fields = ['ticker_number']

    def get(self, request, *args, **kwargs):
        print(kwargs)
        kwargs['lottery_id'] = self.kwargs['lottery_id']
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     import pdb; pdb.set_trace()
    #     context['lottery_id'] = kwargs['lottery_id']
    #     return context
