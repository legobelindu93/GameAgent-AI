import unittest
from gameagent.cloud_study import youtube_url,candidate_pack,video_study
from gameagent.pack_review import benchmark,review
from gameagent.profiles import load_profiles
class CloudStudyTest(unittest.TestCase):
    def test_video_url(self):
        self.assertEqual(youtube_url("https://youtu.be/9hE5-98ZeCg"),"https://www.youtube.com/watch?v=9hE5-98ZeCg")
        for url in ("http://youtube.com/watch?v=9hE5-98ZeCg","https://youtube.com.evil/watch?v=9hE5-98ZeCg"):
            with self.assertRaises(ValueError):youtube_url(url)
    def test_permission(self):
        with self.assertRaises(ValueError):video_study("nikke","https://youtu.be/9hE5-98ZeCg","test")
    def test_review(self):
        p=candidate_pack("nikke","1.0.0",[dict(category="video",title="Test",claim="Synthetic",locator="00:00-00:10")],"https://youtu.be/9hE5-98ZeCg","test")
        self.assertEqual(p["records"][0]["review"],"candidate")
        q=review(p,[p["records"][0]["id"]],"1.0.1")
        self.assertEqual(q["records"][0]["review"],"approved")
        with self.assertRaises(ValueError):review(p,["missing"],"1.0.1")
    def test_all_seed_retrieval(self):
        for game in load_profiles():
            with self.subTest(game=game):
                r=benchmark(game)
                self.assertEqual(r["passed"],r["total"])
