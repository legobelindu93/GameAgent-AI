import tempfile
import unittest
from gameagent.engine import State, Action, step
from gameagent.planner import plan
from gameagent.memory import Memory
from gameagent.imitation import Imitation

class ResearchTests(unittest.TestCase):
    def test_plan(self):
        action,scores=plan(State())
        self.assertIn(action.value,scores)
    def test_terminal(self):
        with self.assertRaises(ValueError):
            plan(State(enemy=0))
    def test_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Memory(tmp,"nikke"),Memory(tmp,"brown_dust_2")
            try:
                a.record("session",State(),Action.ATTACK,step(State(),Action.ATTACK))
                self.assertEqual(len(a.rows()),1)
                self.assertEqual(b.rows(),[])
            finally:
                a.close()
                b.close()
    def test_imitation(self):
        model=Imitation()
        model.teach(State(),Action.ATTACK)
        self.assertEqual(model.predict(State()),Action.ATTACK)
