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

    def test_batch_cache_and_standalone_pack(self):
        from unittest.mock import patch
        from gameagent.factory import BASE
        from gameagent.packs import registry
        calls=[]
        def fake(game,topic,authorized):
            calls.append(topic)
            return {"game":game,"topic":topic,"parts":["Synthetic evidence."],"citations":[{"part":0,"start_index":0,"end_index":9,"url":"https://example.com"}]}
        with tempfile.TemporaryDirectory() as d:
            gaps={t:0 for t in registry("nikke")["topics"]}
            with patch("gameagent.factory.BASE",Path(d)),patch("gameagent.factory.coverage",return_value=gaps),patch("gameagent.factory.web_dossier",side_effect=fake):
                a=batch("nikke",web=True,authorized=True)
                b=batch("nikke",web=True,authorized=True)
                self.assertEqual(len(set(calls)),2)
                for r in (a,b):
                    job=r["jobs"][0]
                    self.assertEqual(job["status"],"complete")
                    self.assertEqual(verify(load_json(job["pack"]))["records"][0]["review"],"candidate")
    def test_invalid_video_list_before_remote_call(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"invalid.json";p.write_text("[]",encoding="utf-8")
            p.write_text('[{"url":"https://youtu.be/9hE5-98ZeCg","patch":"test","authorized":false}]',encoding="utf-8")
            with patch("gameagent.factory.web_dossier") as remote:
                with self.assertRaises(ValueError):batch("nikke",web=True,video_file=p,authorized=True)
                remote.assert_not_called()
