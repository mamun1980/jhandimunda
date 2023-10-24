from django import forms
from .models import Game


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['name']
    
    def save(self, commit: True):
        instance = super().save(commit=False)
        instance.created_by = self.request.user
        return super().save(commit)