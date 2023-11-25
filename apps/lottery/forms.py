from django import forms
from .models import Ticket, Lottery


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticker_number']

        widgets = {
            'ticker_number': forms.TextInput(attrs={'class': 'form-control'})
        }
