import importlib.util
import unittest

@unittest.skipUnless(importlib.util.find_spec("pathfinding"),"Optional navigation dependency missing")
class NavigationTests(unittest.TestCase):
    def test_routes(self):
        from gameagent.navigation import MAPS,route
        for world in MAPS.values():
            path=route(world)["path"]
            self.assertEqual(path[0],list(world.start))
            self.assertEqual(path[-1],list(world.goal))
            for (x,y),(u,v) in zip(path,path[1:]):
                self.assertEqual(abs(x-u)+abs(y-v),1)
                self.assertGreater(world.cells[v][u],0)
    def test_unreachable(self):
        from gameagent.navigation import Map,route
        self.assertFalse(route(Map(((1,0,1),),(0,0),(2,0)))["reachable"])
