from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import TemplateView
# from django.utils.translation import ugettext as _
from apps.wallet.models import Wallet


class JMTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect("/accounts/login/")
        return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = Wallet.objects.get(user=user)
        data = {
            "wallet": wallet
        }
        context.update(data)
        return context
