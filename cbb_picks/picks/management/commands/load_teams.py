from django.core.management.base import BaseCommand
from picks.models import Conference, Team

CONFERENCES = {
    # Atlantic Coast Conference (ACC)
    'Atlantic Coast Conference': [
        'Boston College Eagles',
        'Clemson Tigers',
        'Duke Blue Devils',
        'Florida State Seminoles',
        'Georgia Tech Yellow Jackets',
        'Louisville Cardinals',
        'Miami Hurricanes',
        'North Carolina Tar Heels',
        'NC State Wolfpack',
        'Notre Dame Fighting Irish',
        'Pittsburgh Panthers',
        'Syracuse Orange',
        'Virginia Cavaliers',
        'Virginia Tech Hokies',
        'Wake Forest Demon Deacons',
        'California Golden Bears',
        'Stanford Cardinal',
    ],
    # American Athletic Conference (AAC)
    'American Athletic Conference': [
        'Cincinnati Bearcats',
        'East Carolina Pirates',
        'Florida Atlantic Owls',
        'Houston Cougars',
        'Memphis Tigers',
        'Navy Midshipmen',
        'SMU Mustangs',
        'South Florida Bulls',
        'Temple Owls',
        'Tulane Green Wave',
        'Tulsa Golden Hurricane',
        'UAB Blazers',
        'UCF Knights',
        'Wichita State Shockers',
    ],
    # Atlantic 10 Conference (A-10)
    'Atlantic 10 Conference': [
        'Davidson Wildcats',
        'Dayton Flyers',
        'Duquesne Dukes',
        'Fordham Rams',
        'George Mason Patriots',
        'George Washington Colonials',
        'La Salle Explorers',
        'Loyola Chicago Ramblers',
        'Massachusetts Minutemen',
        'Rhode Island Rams',
        'Richmond Spiders',
        'Saint Joseph\'s Hawks',
        'Saint Louis Billikens',
        'Saint Bonaventure Bonnies',
        'VCU Rams',
    ],
    # Atlantic Sun Conference (ASUN)
    'ASUN Conference': [
        'Austin Peay Governors',
        'Bellarmine Knights',
        'Central Arkansas Bears',
        'Eastern Kentucky Colonels',
        'Florida Gulf Coast Eagles',
        'Jacksonville Dolphins',
        'Kennesaw State Owls',
        'Lipscomb Bisons',
        'North Florida Ospreys',
        'North Alabama Lions',
        'Stetson Hatters',
        'Liberty Flames',
        'Queens Royals',
        'Jacksonville State Gamecocks',
    ],
    # Big 12 Conference
    'Big 12 Conference': [
        'Baylor Bears',
        'Iowa State Cyclones',
        'Kansas Jayhawks',
        'Kansas State Wildcats',
        'Oklahoma Sooners',
        'Oklahoma State Cowboys',
        'TCU Horned Frogs',
        'Texas Longhorns',
        'Texas Tech Red Raiders',
        'West Virginia Mountaineers',
        'Arizona Wildcats',
        'Arizona State Sun Devils',
        'Colorado Buffaloes',
        'Utah Utes',
    ],
    # Big East Conference
    'Big East Conference': [
        'Butler Bulldogs',
        'Creighton Bluejays',
        'DePaul Blue Demons',
        'Georgetown Hoyas',
        'Marquette Golden Eagles',
        'Providence Friars',
        'St. John\'s Red Storm',
        'Seton Hall Pirates',
        'Villanova Wildcats',
        'Xavier Musketeers',
    ],
    # Big Sky Conference
    'Big Sky Conference': [
        'Eastern Washington Eagles',
        'Idaho Vandals',
        'Idaho State Bengals',
        'Montana Grizzlies',
        'Montana State Bobcats',
        'Northern Arizona Lumberjacks',
        'Northern Colorado Bears',
        'Portland State Vikings',
        'Sacramento State Hornets',
        'Southern Utah Thunderbirds',
        'Weber State Wildcats',
    ],
    # Big South Conference
    'Big South Conference': [
        'Campbell Fighting Camels',
        'Charleston Southern Buccaneers',
        'Gardner-Webb Runnin\' Bulldogs',
        'High Point Panthers',
        'Longwood Lancers',
        'Radford Highlanders',
        'UNC Asheville Bulldogs',
        'USC Upstate Spartans',
        'Presbyterian Blue Hose',
        'Winthrop Eagles',
    ],
    # Big Ten Conference
    'Big Ten Conference': [
        'Illinois Fighting Illini',
        'Indiana Hoosiers',
        'Iowa Hawkeyes',
        'Maryland Terrapins',
        'Michigan Wolverines',
        'Michigan State Spartans',
        'Minnesota Golden Gophers',
        'Nebraska Cornhuskers',
        'Northwestern Wildcats',
        'Ohio State Buckeyes',
        'Penn State Nittany Lions',
        'Purdue Boilermakers',
        'Rutgers Scarlet Knights',
        'Wisconsin Badgers',
        'Washington Huskies',
        'USC Trojans',
        'UCLA Bruins',
        'Oregon Ducks',
    ],
    # Big West Conference
    'Big West Conference': [
        'Cal Poly Mustangs',
        'Cal State Bakersfield Roadrunners',
        'Cal State Fullerton Titans',
        'Cal State Northridge Matadors',
        'Cal State Sacramento Hornets',
        'Hawaii Rainbow Warriors',
        'Long Beach State Beach',
        'UC Davis Aggies',
        'UC Irvine Anteaters',
        'UC Riverside Highlanders',
        'UC Santa Barbara Gauchos',
        'UC San Diego Tritons',
    ],
    # Coastal Athletic Association (CAA)
    'Coastal Athletic Association': [
        'Delaware Fightin\' Blue Hens',
        'Drexel Dragons',
        'Hampton Pirates',
        'Hofstra Pride',
        'James Madison Dukes',
        'Monmouth Hawks',
        'UNC Wilmington Seahawks',
        'Northeastern Huskies',
        'Towson Tigers',
        'William & Mary Tribe',
    ],
    # Conference USA (C-USA)
    'Conference USA': [
        'Charlotte 49ers',
        'Florida International Panthers',
        'Louisiana Tech Bulldogs',
        'Marshall Thundering Herd',
        'Middle Tennessee Blue Raiders',
        'North Texas Mean Green',
        'Old Dominion Monarchs',
        'Rice Owls',
        'Southern Miss Golden Eagles',
        'UTEP Miners',
        'Western Kentucky Hilltoppers',
    ],
    # Horizon League
    'Horizon League': [
        'Cleveland State Vikings',
        'Detroit Mercy Titans',
        'Green Bay Phoenix',
        'IUPUI Jaguars',
        'Milwaukee Panthers',
        'Northern Kentucky Norse',
        'Oakland Golden Grizzlies',
        'Purdue Fort Wayne Mastodons',
        'Robert Morris Colonials',
        'Youngstown State Penguins',
    ],
    # Ivy League
    'Ivy League': [
        'Brown Bears',
        'Columbia Lions',
        'Cornell Big Red',
        'Dartmouth Big Green',
        'Harvard Crimson',
        'Penn Quakers',
        'Princeton Tigers',
        'Yale Bulldogs',
    ],
    # Metro Atlantic Athletic Conference (MAAC)
    'Metro Atlantic Athletic Conference': [
        'Canisius Golden Griffins',
        'Fairfield Stags',
        'Iona Gaels',
        'Manhattan Jaspers',
        'Marist Red Foxes',
        'Niagara Purple Eagles',
        'Rider Broncs',
        'Saint Peter\'s Peacocks',
        'Siena Saints',
        'Quinnipiac Bobcats',
    ],
    # Mid-American Conference (MAC)
    'Mid-American Conference': [
        'Akron Zips',
        'Ball State Cardinals',
        'Bowling Green Falcons',
        'Buffalo Bulls',
        'Central Michigan Chippewas',
        'Eastern Michigan Eagles',
        'Kent State Golden Flashes',
        'Miami RedHawks',
        'Northern Illinois Huskies',
        'Ohio Bobcats',
        'Toledo Rockets',
        'Western Michigan Broncos',
    ],
    # Mid-Eastern Athletic Conference (MEAC)
    'Mid-Eastern Athletic Conference': [
        'Coppin State Eagles',
        'Delaware State Hornets',
        'Florida A&M Rattlers',
        'Howard Bison',
        'Maryland Eastern Shore Hawks',
        'Morgan State Bears',
        'Norfolk State Spartans',
        'North Carolina Central Eagles',
        'North Carolina A&T Aggies',
        'South Carolina State Bulldogs',
        'Savannah State Tigers',
    ],
    # Missouri Valley Conference (MVC)
    'Missouri Valley Conference': [
        'Bradley Braves',
        'Drake Bulldogs',
        'Evansville Purple Aces',
        'Illinois State Redbirds',
        'Indiana State Sycamores',
        'Missouri State Bears',
        'Northern Iowa Panthers',
        'Southern Illinois Salukis',
        'Valparaiso Crusaders',
    ],
    # Mountain West Conference (MWC)
    'Mountain West Conference': [
        'Air Force Falcons',
        'Boise State Broncos',
        'Colorado State Rams',
        'Fresno State Bulldogs',
        'Nevada Wolf Pack',
        'New Mexico Lobos',
        'San Diego State Aztecs',
        'San Jose State Spartans',
        'UNLV Runnin\' Rebels',
        'Utah State Aggies',
        'Wyoming Cowboys',
    ],
    # Northeast Conference (NEC)
    'Northeast Conference': [
        'Central Connecticut State Blue Devils',
        'Fairleigh Dickinson Knights',
        'LIU Sharks',
        'Merrimack Warriors',
        'Mount St. Mary\'s Mountaineers',
        'Sacred Heart Pioneers',
        'Saint Francis Red Flash',
        'St. Francis Brooklyn Terriers',
        'Wagner Seahawks',
    ],
    # Ohio Valley Conference (OVC)
    'Ohio Valley Conference': [
        'Belmont Bruins',
        'Eastern Illinois Panthers',
        'Morehead State Eagles',
        'Murray State Racers',
        'Southeast Missouri State Redhawks',
        'Southern Indiana Screaming Eagles',
        'Tennessee State Tigers',
        'Tennessee Tech Golden Eagles',
        'UT Martin Skyhawks',
    ],
    # Pac-12 Conference
    'Pac-12 Conference': [
        'Oregon State Beavers',
        'Washington State Cougars',
    ],
    # Patriot League
    'Patriot League': [
        'American Eagles',
        'Army Black Knights',
        'Boston University Terriers',
        'Colgate Raiders',
        'Holy Cross Crusaders',
        'Loyola Maryland Greyhounds',
    ],
}

all_teams = []
for teams in CONFERENCES.values():
    all_teams.extend(teams)

duplicates = set([x for x in all_teams if all_teams.count(x) > 1])
print("Duplicate team names:", duplicates)

class Command(BaseCommand):
    help = "Load conferences and teams into the database"

    def handle(self, *args, **kwargs):
        for conf_name, teams in CONFERENCES.items():
            conference, created = Conference.objects.get_or_create(name=conf_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created conference: {conf_name}"))
            for team_name in teams:
                team, t_created = Team.objects.get_or_create(
                    name=team_name, conference=conference
                )
                if t_created:
                    self.stdout.write(f"  Added team: {team_name}")
        self.stdout.write(self.style.SUCCESS("Finished loading all teams!"))
