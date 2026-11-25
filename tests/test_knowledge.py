import tempfile
import unittest
from gameagent.knowledge import Knowledge

class KnowledgeTests(unittest.TestCase):
    def test_isolation_and_dedup(self):
        with tempfile.TemporaryDirectory() as root:
            a=Knowledge("nikke",root)
            b=Knowledge("brown_dust_2",root)
            try:
                self.assertEqual(a.ingest("Guide","Burst rotation","local:test","1"),1)
                self.assertEqual(a.ingest("Guide","Burst rotation","local:test","1"),0)
                self.assertEqual(len(a.search("burst","1")),1)
                self.assertEqual(a.search("burst","2"),[])
                self.assertEqual(b.search("burst"),[])
                self.assertEqual(a.search('" OR *'),[])
            finally:a.close();b.close()
