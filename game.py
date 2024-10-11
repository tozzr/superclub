import json
from typing import List

class Game():
    
    def __init__(self):
        self.clubname = ''
        self.assets = 100
    
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