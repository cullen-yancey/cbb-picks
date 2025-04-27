from django import forms
from .models import Pick, Team, Game

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ['game', 'picked_team']

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get('game')
        team = cleaned_data.get('picked_team')

        if game and team:
            if team not in [game.home_team, game.away_team]:
                raise forms.ValidationError("Selected team is not playing in the selected game.")

        return cleaned_data
