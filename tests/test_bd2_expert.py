import unittest
from gameagent.bd2_expert import Account,plan
class TestExpert(unittest.TestCase):
    def test_budget(self):
        p=plan(Account(minutes=5))
        self.assertLessEqual(sum(t["minutes"] for t in p if t["fits_budget"]),5)
    def test_invalid(self):
        with self.assertRaises(ValueError):Account(diamonds=-1)
    def test_physical(self):
        self.assertTrue(any("Arines" in t["title"] for t in plan(Account(damage="physical"))))
    def test_magic(self):
        self.assertFalse(any("Arines" in t["title"] for t in plan(Account(damage="magic"))))
