import unittest
from gameagent.upstream import source
from gameagent.profiles import load_profiles

class UpstreamTests(unittest.TestCase):
    def test_all_profiles(self):
        urls=set()
        for game in load_profiles():
            s=source(game)
            self.assertTrue(s["repository"].startswith("https://github.com/"))
            self.assertFalse(s["execution"])
            urls.add(s["repository"])
        self.assertEqual(len(urls),6)
    def test_unknown(self):
        with self.assertRaises(ValueError):
            source("../bad")
