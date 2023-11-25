from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView, CreateView
from django.contrib import messages

from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from .forms import SendCoinForm


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]


class TransactionsListView(TemplateView):
    template_name = 'wallet/transactions.html'

    def get(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect("/accounts/login/")
        
        if user.is_staff:
            return HttpResponseRedirect("/admin/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        transactions_from = Transaction.objects.filter(from_wallet=wallet)
        transactions_to = Transaction.objects.filter(to_wallet=wallet)
        data = {
            "wallet": wallet,
            "transactions_from": transactions_from,
            "transactions_to": transactions_to
        }
        context.update(data)
        
        return context


class SendCoinView(CreateView):
    template_name = 'wallet/send-coin.html'
    form_class = SendCoinForm

    def get(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect("/accounts/login/")
        if user.is_staff:
            return HttpResponseRedirect("/admin/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet,
        }
        context.update(data)
        
        return context
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        from_wallet = user.wallet
        amount = int(data.get('amount'))

        if from_wallet.balance < amount:
            messages.error(request, 'You dont have enough balance!')
            return HttpResponseRedirect("/wallets/send-coin/")
        
        receiver_wallet_id = data.get('to_wallet')
        try:
            receiver_wallet = Wallet.objects.get(wallet_id=receiver_wallet_id)
            Transaction.objects.create(
                from_wallet=from_wallet,
                to_wallet=receiver_wallet,
                transaction_by_user=user,
                amount=amount
            )
            messages.success(request, 'You coin sent successfully!')
            
        except Exception as e:
            raise ValueError(e)

        return HttpResponseRedirect("/wallets/send-coin/")
