from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from picks.models import Team, Location, Game
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Quickly set up superuser, teams, locations, and games'

    def handle(self, *args, **kwargs):
        # Create superuser if not exists
        if not User.objects.filter(username='cullen').exists():
            User.objects.create_superuser('cullen', 'cullenyancey@gmail.com', 'TimTebow15!')
            self.stdout.write(self.style.SUCCESS('Superuser "cullen" created (TimTebow15!:TimTebow15!)'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "cullen" already exists'))

        # Create sample teams
        team1, _ = Team.objects.get_or_create(name="Duke Blue Devils")
        team2, _ = Team.objects.get_or_create(name="Florida Gators")
        team3, _ = Team.objects.get_or_create(name="Auburn Tigers")
        team4, _ = Team.objects.get_or_create(name="Houston Cougars")

        # Create sample location
        location, _ = Location.objects.get_or_create(city="San Antonio", state_or_country="TX")

        # Create sample games
        now = timezone.now()
        Game.objects.get_or_create(
            home_team=team1,
            away_team=team2,
            game_time=now + timedelta(days=1),
            location=location
        )
        Game.objects.get_or_create(
            home_team=team3,
            away_team=team4,
            game_time=now + timedelta(days=2),
            location=location
        )

        self.stdout.write(self.style.SUCCESS('Sample teams, locations, and games created!'))
