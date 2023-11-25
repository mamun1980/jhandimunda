from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.contrib import messages

from apps.dashboard.views import JMTemplateView
from apps.game.models import Player
from apps.wallet.models import Wallet
from .models import Lottery, Ticket
from .serializers import LotterySerializer, TicketSerializer
from .forms import TicketForm


class LotteryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    serializer_class = LotterySerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            queryset = Lottery.objects.filter(status=status).order_by('lottery_date')
        else:
            queryset = Lottery.objects.all().order_by('lottery_date')
        return queryset
    
    @action(detail=True, methods=['post'])
    def buy_ticket(self, request, pk):
        lottery = Lottery.objects.get(pk=pk)
        player = request.user.player
        ticker_number = request.data.get('ticker_number')

        ticket = Ticket.objects.filter(
            lottery=lottery,
            ticker_number=ticker_number
        ).exists()
        
        if ticket:
            return Response({"error": f"This number '{ticker_number}' already purchased"})
        
        ticket = Ticket.objects.create(
            lottery=lottery,
            player=player,
            ticker_number=ticker_number
        )
        ticket_serializer = TicketSerializer(instance=ticket)

        return Response(ticket_serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        player = self.request.user.player
        qs = Ticket.objects.filter(
            player=player
        )
        return qs


class LotteryListView(ListView):
    template_name = "lottery/index.html"

    class Meta:
        model = Lottery
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect("/accounts/login/")
        
        if user.is_staff:
            return HttpResponseRedirect("/admin/")
        
        if user.is_agent:
            return HttpResponseRedirect("/")
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Lottery.objects.filter(status='live')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet,
        }
        context.update(data)
        
        return context


class LotteryDetailView(DetailView):
    template_name = "lottery/lottery_detail.html"
    queryset = Lottery.objects.all()

    class Meta:
        model = Lottery
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet,
        }
        context.update(data)
        
        return context


class MyTicketListView(ListView):
    template_name = "lottery/ticket_list.html"

    class Meta:
        model = Ticket
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet
        }
        context.update(data)
        return context

    def get_queryset(self):
        user = self.request.user
        player = user.player
        qs = Ticket.objects.filter(player=player, expired=False)
        return qs


class TicketListView(ListView):
    template_name = "lottery/ticket_list.html"

    class Meta:
        model = Ticket

    def get_queryset(self):
        qs = Ticket.objects.all()
        return qs


class TicketDetailView(DetailView):
    template_name = "lottery/ticket_detail.html"
    queryset = Ticket.objects.all()

    class Meta:
        model = Ticket
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet
        }
        context.update(data)
        return context


class TicketCreateView(CreateView):
    template_name = "lottery/ticket_create.html"
    model = Ticket
    fields = ['ticker_number']

    def get(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {}
        lottery_id = self.kwargs['lottery_id']
        lottery = Lottery.objects.get(id=lottery_id)
        player = Player.objects.get(user=request.user)
        data['player_id'] = player.player_id
        data['wallet'] = wallet
        data['lottery'] = lottery
        
        return render(request, "lottery/ticket_create.html", context=data)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import pdb; pdb.set_trace()
            data = form.data
            try:
                ticker_number = data.get('ticker_number')
                lottery = Lottery.objects.get(id=data.get('lottery_id'))
                player = Player.objects.get(player_id=data.get('player_id'))
                wallet = player.user.wallet
                ticket_price = lottery.ticket_price

                if wallet.balance < ticket_price:
                    messages.error(request, f"আপনার একাউন্টে পর্যাপ্ত কয়েন নাই! এই লটারির টিকেটের মূল্য {lottery.ticket_price}")
                    return HttpResponseRedirect(reverse_lazy("lottery:tickets-buy", kwargs={'lottery_id': lottery.id}))

                ticket = Ticket.objects.create(
                    lottery=lottery,
                    player=player,
                    ticker_number=ticker_number
                )
                
                wallet.balance -= lottery.ticket_price
                wallet.save()
                return HttpResponseRedirect("/lotteries/my-tickets/")
            except Exception as e:
                messages.error(request, f"{ticker_number} নাম্বারটি নেয়া হয়েগেছে! দয়াকরে আবার অন্য নাম্বার চেষ্টা করুন!")
                return HttpResponseRedirect(reverse_lazy("lottery:tickets-buy", kwargs={'lottery_id': lottery.id}))
        else:
            return self.form_invalid(form)

