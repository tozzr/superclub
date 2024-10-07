
class Game():
    
    def __init__(self):
        self.clubname = ''
        self.assets = 100
        self.players = []
    
    def get_assets(self):
        return self.assets
    
    def set_clubname(self, clubname):
        self.clubname = clubname
        
    def get_clubname(self):
        return self.clubname
    
    def pick_player(self, player):
        self.players.append(player)
    
    def get_players(self):
        return self.players
    
    def get_draft_players(self):
        return []
        
class Player():
    
    def __init__(self, name, position, club, status, potential, chemistry) -> None:
        self.name = name
        self.position = position
        self.club = club
        self.status = status
        self.potential = potential
        self.chemistry = chemistry