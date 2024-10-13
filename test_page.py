import unittest

from players import Page

class TestPlayers(unittest.TestCase):
    
    def test_init(self):
        p = Page('/players.html', 1, 16, [])
        self.assertEqual(p.page, 1)
        self.assertEqual(p.size, 16)
        self.assertEqual(len(p.items), 0)
        self.assertEqual(p.previous, None)
        self.assertEqual(p.next, None)
        
    def test_next(self):
        p = Page('/players.html', 2, 1, [{"id":1}, {"id": 2},{"id": 3}])
        self.assertEqual(p.previous, '/players.html?page=1&size=1')
        self.assertEqual(p.next, '/players.html?page=3&size=1')
        
    def test_pages(self):
        p = Page('/players.html', 1, 1, [{"id":1}, {"id": 2},{"id": 3}])
        self.assertEqual(p.pages, 3)
        p = Page('/players.html', 1, 2, [{"id":1}, {"id": 2},{"id": 3}])
        self.assertEqual(p.pages, 2)
        p = Page('/players.html', 1, 3, [{"id":1}, {"id": 2},{"id": 3}])
        self.assertEqual(p.pages, 1)
        p = Page('/players.html', 1, 3, [])
        self.assertEqual(p.pages, 0)
        
if __name__ == '__main__':
    unittest.main()