import unittest
from gameagent.scenarios import SCENARIOS,initial,evaluate
from gameagent.profiles import load_profiles

class ScenarioTests(unittest.TestCase):
    def test_profiles(self):
        self.assertEqual(set(SCENARIOS),set(load_profiles()))
    def test_distinct(self):
        self.assertEqual(len({initial(k) for k in SCENARIOS}),6)
    def test_bounded(self):
        for key in SCENARIOS:
            r=evaluate(key,3)
            self.assertLessEqual(r["turns"],3)
            self.assertEqual(len(r["trace"]),r["turns"])
    def test_reproducible(self):
        self.assertEqual(evaluate("nikke"),evaluate("nikke"))
