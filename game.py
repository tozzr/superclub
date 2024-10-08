import json
from typing import List

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
    
    def __init__(self, id, name, position, nr, club, status, potential, chemistry) -> None:
        self.id = id
        self.name = name
        self.position = position
        self.nr = nr
        self.club = club
        self.status = status
        self.potential = potential
        self.chemistry = chemistry

    def __eq__(self, other: object) -> bool:
        return self.id == other.id
    
def get_players():
    with open('players.json', 'r') as file:
        data = json.load(file)
        players = [Player(**player_data) for player_data in data]
        return players
    return []

def get_players_without(ids: str):
    exclude_players = get_players_for_ids(ids)
    id_list = ids.split(',')
    players = get_players()
    for player in exclude_players:
        players.pop(players.index(player))
    return players

def get_players_for_ids(ids: str):
    players = []
    id_list = ids.split(',')
    for player in get_players():
        for id in id_list:
            if id == player.id:
                players.append(player)
    return players