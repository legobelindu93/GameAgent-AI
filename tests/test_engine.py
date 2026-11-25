import unittest
from gameagent.engine import State, Action, choose, step
from gameagent.profiles import load_profiles

class EngineTests(unittest.TestCase):
    def test_attack(self):
        self.assertEqual(step(State(), Action.ATTACK).enemy, 75)
    def test_heal(self):
        self.assertEqual(choose(State(hp=20))[0], Action.HEAL)
    def test_terminal(self):
        s = State(enemy=0)
        self.assertEqual(step(s, Action.ATTACK), s)
    def test_profiles(self):
        self.assertEqual(len(load_profiles()), 6)
    def test_invalid_heal(self):
        with self.assertRaises(ValueError):
            step(State(potions=0), Action.HEAL)
