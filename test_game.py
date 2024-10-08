import unittest

from game import Game, Player

class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()
    
    def test_set_clubname(self):
        self.game.set_clubname("My cool Club")
        self.assertEqual(self.game.get_clubname(), "My cool Club")
    
    def test_get_assets_initial_one_hundret(self):
        self.assertEqual(self.game.get_assets(), 100)
        
    def test_draft_phase_user_picks_players(self):
        self.game.pick_player(Player("Manuel Neuer", "Goalkeeper", 1, "Bayern München", 4, 4, 0.5))
        
        self.assertEqual(self.game.get_players()[0].name, "Manuel Neuer")
        self.assertEqual(self.game.get_players()[0].position, "GOALKEEPER")
        self.assertEqual(self.game.get_players()[0].nr, 1)
        self.assertEqual(self.game.get_players()[0].club, "FCB")
        self.assertEqual(self.game.get_players()[0].status, 4)
        self.assertEqual(self.game.get_players()[0].potential, 4)
        self.assertEqual(self.game.get_players()[0].chemistry, 0.5)
    
    def test_clubs(self):
        clubs = self.game.get_clubs()
        self.assertEqual(3, len(clubs))
        self.assertEqual(clubs[0].id, "FCB")
        self.assertEqual(clubs[0].name, "FC Bayern München")
        self.assertEqual(clubs[0].stadium, "Allianz Arena")
        
    def test_draft_deck(self):
        self.assertEqual(6, len(self.game.get_draft_players()))
        
    '''
    - user starts a new game
    - user chooses name of club
    - game has 100M in funds
    - draft phase: users takes 16 players into deck
    - team:
        - max 11 players on the green
        - 1 goalkeeper
        - max 4 strikers
        - max 5 midfielders
        - max 4 defenders
        - max players on deck at all: 15 + 11 = 36
    - invest phase:
        - level up training court (1-4)
        - level up scouting (1-4)
        - level up stadion (1-4)
    - scouting phase
        - scout new player for the scouting fee (select number of player depending on scouting level)
        - scout new staff (pick 2, buy 1)
    '''
if __name__ == '__main__':
    unittest.main()
