import json

class Game():
    
    def __init__(self):
        self.clubname = ''
        self.assets = 100
        with open('clubs.json', 'r') as file:
            data = json.load(file)
            self.clubs = [Club(**club_data) for club_data in data]
        with open('players.json', 'r') as file:
            data = json.load(file)
            self.players = [Player(**player_data) for player_data in data]
    
    def get_assets(self):
        return self.assets
    
    def set_clubname(self, clubname):
        self.clubname = clubname
        
    def get_clubname(self):
        return self.clubname
    
    def pick_player(self, player):
        self.players.append(player)
    
    def get_clubs(self):
        return self.clubs
    
    def get_players(self):
        return self.players
    
    def get_draft_players(self):
        return self.players
        
class Club():
    
     def __init__(self, id, name, stadium, logo) -> None:
        self.id = id
        self.name = name
        self.stadium = stadium
        self.logo = logo
class Player():
    
    def __init__(self, name, position, nr, club, status, potential, chemistry) -> None:
        self.name = name
        self.position = position
        self.nr = nr
        self.club = club
        self.status = status
        self.potential = potential
        self.chemistry = chemistry