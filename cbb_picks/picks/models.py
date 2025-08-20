from django.db import models
from django.contrib.auth.models import User

# Classes to add: Venue (Game/venue)

SCHOOLS = [
    # Atlantic Coast Conference (ACC)
    ('Duke Blue Devils', 'Duke Blue Devils'),
    ('North Carolina Tar Heels', 'North Carolina Tar Heels'),
    ('Syracuse Orange', 'Syracuse Orange'),
    ('Florida State Seminoles', 'Florida State Seminoles'),
    ('Louisville Cardinals', 'Louisville Cardinals'),
    ('Virginia Cavaliers', 'Virginia Cavaliers'),
    ('Miami Hurricanes', 'Miami Hurricanes'),
    ('Clemson Tigers', 'Clemson Tigers'),
    ('Virginia Tech Hokies', 'Virginia Tech Hokies'),
    ('NC State Wolfpack', 'NC State Wolfpack'),
    
    # Big Ten Conference
    ('Michigan Wolverines', 'Michigan Wolverines'),
    ('Indiana Hoosiers', 'Indiana Hoosiers'),
    ('Ohio State Buckeyes', 'Ohio State Buckeyes'),
    ('Wisconsin Badgers', 'Wisconsin Badgers'),
    ('Purdue Boilermakers', 'Purdue Boilermakers'),
    ('Michigan State Spartans', 'Michigan State Spartans'),
    ('Minnesota Golden Gophers', 'Minnesota Golden Gophers'),
    ('Maryland Terrapins', 'Maryland Terrapins'),
    ('Illinois Fighting Illini', 'Illinois Fighting Illini'),
    ('Iowa Hawkeyes', 'Iowa Hawkeyes'),
    
    # Big 12 Conference
    ('Kansas Jayhawks', 'Kansas Jayhawks'),
    ('Baylor Bears', 'Baylor Bears'),
    ('Texas Longhorns', 'Texas Longhorns'),
    ('Oklahoma Sooners', 'Oklahoma Sooners'),
    ('Kansas State Wildcats', 'Kansas State Wildcats'),
    ('Texas Tech Red Raiders', 'Texas Tech Red Raiders'),
    ('West Virginia Mountaineers', 'West Virginia Mountaineers'),
    ('TCU Horned Frogs', 'TCU Horned Frogs'),
    ('Houston Cougars', 'Houston Cougars'),
    
    # Southeastern Conference (SEC)
    ('Kentucky Wildcats', 'Kentucky Wildcats'),
    ('Florida Gators', 'Florida Gators'),
    ('Auburn Tigers', 'Auburn Tigers'),
    ('Alabama Crimson Tide', 'Alabama Crimson Tide'),
    ('Tennessee Volunteers', 'Tennessee Volunteers'),
    ('Arkansas Razorbacks', 'Arkansas Razorbacks'),
    ('Mississippi State Bulldogs', 'Mississippi State Bulldogs'),
    ('South Carolina Gamecocks', 'South Carolina Gamecocks'),
    ('Missouri Tigers', 'Missouri Tigers'),
    ('LSU Tigers', 'LSU Tigers'),
]
CONFERENCES = [
    ('Atlantic Coast Conference', 'ACC'),
    ('Southeastern Conference', 'SEC'),
]

class Team(models.Model):
    name = models.CharField(
        max_length=100,
        choices=SCHOOLS,
        blank=True,
        null=True,
        help_text="Select if located in the United States."
    )
    logo_url = models.URLField(blank=True, null=True)

    # conference = models.CharField(
    #     max_length=100,
    #     choices=CONFERENCES,
    #     blank=True,
    #     null=True,
    #     # help_text=""
    # )
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