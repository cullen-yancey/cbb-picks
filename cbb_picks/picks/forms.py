from django import forms
from .models import Pick, Team, Game

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ['game', 'team']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get('game')

        if self.user and game:
            existing_pick = Pick.objects.filter(user=self.user, game=game).exists()
            if existing_pick and not self.instance.pk:
                raise forms.ValidationError("You have already made a pick for this game.")
        return cleaned_data