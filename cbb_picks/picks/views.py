from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Pick
from .forms import PickForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, F
from django.views.generic.edit import CreateView
from datetime import timezone

def upcoming_games(request):
    today = timezone.now()
    # Get games where the date is greater than today
    upcoming = Game.objects.filter(game_time__gt=today).order_by('game_time')
    return render(request, 'picks/upcoming_games.html', {'upcoming': upcoming})

class PickCreateView(CreateView):
    model = Pick
    form_class = PickForm
    template_name = 'picks/pick_form.html'
    success_url = '/leaderboard/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def leaderboard(request):
    users = User.objects.all()
    leaderboard_data = []

    for user in users:
        picks = Pick.objects.filter(user=user)
        correct_picks = 0
        for pick in picks:
            if pick.game.winner and pick.picked_team == pick.game.winner:
                correct_picks += 1
        leaderboard_data.append({
            'user': user,
            'correct_picks': correct_picks,
        })

    leaderboard_data.sort(key=lambda x: x['correct_picks'], reverse=True)

    return render(request, 'picks/leaderboard.html', {'leaderboard_data': leaderboard_data})

def game_list(request):
    games = Game.objects.all().order_by('game_time')
    return render(request, 'picks/game_list.html', {'games': games})

@login_required
def make_pick(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = PickForm(request.POST)
        if form.is_valid():
            pick = form.save(commit=False)
            pick.user = request.user
            pick.game = game
            pick.save()
            return redirect('game_list')
    else:
        form = PickForm()
    return render(request, 'picks/make_pick.html', {'form': form, 'game': game})
