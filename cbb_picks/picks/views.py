from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Pick, Team
from .forms import PickForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, F
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.contrib import messages
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect

class PickUpdateView(UpdateView):
    model = Pick
    fields = ['team']
    template_name = 'picks/pick_form.html'
    success_url = '/leaderboard/'

    def form_valid(self, form):
        pick = form.instance
        if pick.game.game_time <= timezone.now():
            messages.error(self.request, "You cannot update your pick after the game has started.")
            return redirect('leaderboard')

        return super().form_valid(form)


class PickCreateView(CreateView):
    model = Pick
    fields = ['game']  # Only include the game, since we're handling the team via JS
    template_name = 'picks/pick_form.html'
    success_url = '/leaderboard/'

    def form_valid(self, form):
        game = form.cleaned_data['game']
        team_id = self.request.POST.get('team')  # Grab the selected team from POST data

        if game.game_time <= timezone.now():
            messages.error(self.request, "You cannot make a pick after the game has started.")
            return redirect('upcoming_games')

        # Check if the user has already made a pick for this game
        existing_pick = Pick.objects.filter(user=self.request.user, game=game).first()
        if existing_pick:
            # Update the existing pick with the new team choice
            existing_pick.team = Team.objects.get(id=team_id)
            existing_pick.save()
            messages.success(self.request, "Your pick has been updated!")
            return redirect(self.success_url)
        
        # If no existing pick, create a new pick
        try:
            team = Team.objects.get(id=team_id)  # Ensure a valid team is selected
            form.instance.team = team  # Assign the team to the pick instance
        except Team.DoesNotExist:
            messages.error(self.request, "Invalid team selection.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

        form.instance.user = self.request.user  # Set the user
        return super().form_valid(form)

def upcoming_games(request):
    today = timezone.now()
    # Get games where the date is greater than today
    upcoming = Game.objects.filter(game_time__gt=today).order_by('game_time')
    return render(request, 'picks/upcoming_games.html', {'upcoming': upcoming})

def leaderboard(request):
    users = User.objects.annotate(
        total_picks=Count('pick')
    )

    # Manually calculate correct picks
    user_stats = []
    for user in users:
        picks = user.pick_set.all()
        correct_picks = 0
        total_picks = 0
        for pick in picks:
            if pick.game.winner and pick.team == pick.game.winner:
                correct_picks += 1
            if pick.game.winner:
                total_picks += 1
        correct_percentage = round((correct_picks / total_picks) * 100, 1) if total_picks > 0 else 0.0
        user_stats.append({
            'username': user.username,
            'correct_picks': correct_picks,
            'total_picks': total_picks,
            'correct_percentage': correct_percentage,
        })

    return render(request, 'picks/leaderboard.html', {'user_stats': user_stats})


def game_list(request):
    games = Game.objects.all().order_by('game_time')
    return render(request, 'picks/game_list.html', {'games': games})

@login_required
def make_pick(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = PickForm(request.POST or None, user=request.user)
        if form.is_valid():
            pick = form.save(commit=False)
            pick.user = request.user
            pick.game = game
            pick.save()
            return redirect('game_list')
    else:
        form = PickForm()
    return render(request, 'picks/make_pick.html', {'form': form, 'game': game})

def make_picks(request):
    # Get all upcoming games, ordered by game time
    upcoming_games = Game.objects.filter(game_time__gt=timezone.now()).order_by('game_time')

    context = {
        'upcoming_games': upcoming_games,
    }
    return render(request, 'picks/make_picks.html', context)