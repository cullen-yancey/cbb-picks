from django.db import models
from django.contrib.auth.models import User

# Classes to add: Venue (Game/venue)

class Conference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    blank=True
    null=True

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="teams")
    logo_url = models.URLField(blank=True, null=True)  # optional field for logos later
    blank=True
    null=True

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

STATE_CHOICES = [
    # US States
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]

COUNTRIES = [
    # Western Countries
    ('UK', 'United Kingdom'),
    ('CA', 'Canada'),
    ('AU', 'Australia'),
    ('NZ', 'New Zealand'),
    ('IE', 'Ireland'),
    ('FR', 'France'),
    ('DE', 'Germany'),
    ('NL', 'Netherlands'),
    ('IT', 'Italy'),
    ('ES', 'Spain'),
]

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        blank=True,
        null=True,
        help_text="Select if located in the United States."
    )
    country = models.CharField(
        max_length=2,
        choices=COUNTRIES,
        blank=True,
        null=True,
        help_text="Select if located outside the United States."
    )

    def save(self, *args, **kwargs):
        # Ensure only one field (state or country) is filled
        if self.state:
            self.country = None  # Nullify country if state is provided
        if self.country:
            self.state = None  # Nullify state if country is provided
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.city]
        if self.state:
            parts.append(self.get_state_display())
        if self.country:
            parts.append(self.get_country_display())
        return ", ".join(parts)

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    game_time = models.DateTimeField()
    location = models.ForeignKey(Location, related_name="location", on_delete=models.CASCADE, blank=True, null=True)
    winner = models.ForeignKey(Team, related_name="won_games", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team}"

class Pick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')