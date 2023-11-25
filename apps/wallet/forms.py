from django import forms
from .models import Wallet, Transaction


class SendCoinForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'to_wallet']

        # widgets = {
        #     'amount': forms.NumberInput(attrs={'class': 'mdl-textfield__input'})
        # }