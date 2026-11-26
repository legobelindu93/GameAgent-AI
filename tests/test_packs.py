import unittest,tempfile
from pathlib import Path
from gameagent.packs import make,verify,install,atomic,compare,registry
from gameagent.knowledge import Knowledge
class PacksTest(unittest.TestCase):
    def record(self,status="approved"):
        return dict(id="test",category="combat",title="Test chain",claim="Synthetic chain rule",source="https://example.com/guide",patch="test",locator="section 1",review=status)
    def test_hash_and_game(self):
        pack=make("brown_dust_2","1.0.0",[self.record()])
        self.assertEqual(verify(pack),pack)
        with self.assertRaises(ValueError):verify(pack,"nikke")
        pack["records"][0]["claim"]="changed"
        with self.assertRaises(ValueError):verify(pack)
    def test_import_candidates_and_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"pack.json"
            atomic(p,make("brown_dust_2","1.0.0",[self.record(),dict(self.record("candidate"),id="candidate",claim="unverified")]))
            with self.assertRaises(ValueError):install(p,"brown_dust_2",root=d)
            self.assertEqual(install(p,"brown_dust_2",root=d,trusted=True)["indexed_chunks"],1)
            self.assertEqual(install(p,"brown_dust_2",root=d,trusted=True)["indexed_chunks"],0)
            db=Knowledge("brown_dust_2",root=d)
            try:self.assertEqual(db.search("unverified"),[])
            finally:db.close()
    def test_conflict(self):
        self.assertEqual(len(compare([self.record(),dict(self.record(),id="other",claim="different")])),1)
    def test_registry(self):
        self.assertTrue(registry("nikke")["sources"])
