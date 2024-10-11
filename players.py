import json
from typing import List

class Player():
    
    def __init__(self, id, name, position, club, status, potential, chemistry, price, scouting_price) -> None:
        self.id = id
        self.name = name
        self.position = position
        self.club = club
        self.status = status
        self.potential = potential
        self.chemistry = chemistry
        self.price = price
        self.scouting_price = scouting_price

    def __eq__(self, other: object) -> bool:
        return self.id == other.id
    
class Players():
    def __init__(self):
         with open('players_2024_2025.json', 'r') as file:
            data = json.load(file)
            players = [Player(**player_data) for player_data in data]
            self.players = players
    
    def get_players(self):
        return self.players

    def get_player_by_id(self, id: str) -> Player | None:
        for player in self.get_players():
            if id == player.id:
                return player
        return None
        
    def get_players_without(self, ids: str):
        exclude_players = self.get_players_for_ids(ids)
        id_list = ids.split(',')
        players =self.get_players()
        for player in exclude_players:
            players.pop(players.index(player))
        return players

    def get_players_for_ids(self,ids: str):
        players = []
        id_list = ids.split(',')
        for player in self.get_players():
            for id in id_list:
                if id == player.id:
                    players.append(player)
        return players
    
