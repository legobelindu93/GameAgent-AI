import tempfile,unittest
from pathlib import Path
from gameagent.factory import build_bundle,dossier_candidates,offline_advice,batch
from gameagent.packs import verify,load_json
from gameagent.profiles import load_profiles
class FactoryTest(unittest.TestCase):
    def test_bundle(self):
        with tempfile.TemporaryDirectory() as d:
            r=build_bundle(d)
            self.assertEqual(len(r["packs"]),len(load_profiles()))
            for m in r["packs"]:self.assertEqual(verify(load_json(Path(d)/m["file"]),m["game"])["sha256"],m["sha256"])
    def test_cited_candidate(self):
        d={"game":"nikke","topic":"example","parts":["A synthetic fact."],"citations":[{"part":0,"start_index":0,"end_index":4,"url":"https://example.com"}]}
        p=dossier_candidates(d)
        self.assertEqual(len(p["records"]),1)
        self.assertEqual(p["records"][0]["review"],"candidate")
    def test_no_remote_without_consent(self):
        with self.assertRaises(ValueError):batch("nikke",web=True)
    def test_offline_empty(self):
        with tempfile.TemporaryDirectory() as d:
            r=offline_advice("nikke","test",root=d)
            self.assertEqual(r["evidence"],[])
