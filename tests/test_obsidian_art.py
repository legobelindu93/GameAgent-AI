import unittest
from gameagent.obsidian_art import cover
from gameagent.profiles import load_profiles
class ArtTest(unittest.TestCase):
    def test_all_covers(self):
        for game in load_profiles():
            with self.subTest(game=game):
                img=cover(game,320,140)
                self.assertEqual(img.size,(320,140))
                self.assertEqual(img.mode,"RGB")
                self.assertGreater(len(img.getcolors(100000)),10)
