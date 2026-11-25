import unittest
from gameagent.bd2_tactics import Skill,estimate,optimize
from gameagent.bd2_observe import resource_candidates
class TacticsTest(unittest.TestCase):
    def test_chain(self):
        s=Skill("A","X",100,1,2,1)
        self.assertAlmostEqual(estimate(s),210)
    def test_order(self):
        a=Skill("A","X",100,.5,4,2)
        b=Skill("B","Y",200,2,1,3)
        r=optimize([a,b],5)
        self.assertEqual(r["order"][0]["character"],"A")
        self.assertEqual(r["sp_used"],5)
    def test_budget(self):
        self.assertEqual(optimize([Skill("A","X",100,1,1,2)],1)["order"],[])
    def test_ocr(self):
        self.assertEqual(resource_candidates([{"text":"Gold: 1,200","confidence":.99},{"text":"Diamonds: 8","confidence":.2}]),{"gold":1200})
