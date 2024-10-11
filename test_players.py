import unittest

from players import Players, Player

class TestPlayers(unittest.TestCase):
    
    def setUp(self):
        self.players = Players()
    
    def test_get_players(self):
        self.assertEqual(len(self.players.get_players()), 534)
        
if __name__ == '__main__':
    unittest.main()