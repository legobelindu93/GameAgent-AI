import tempfile,unittest
from gameagent.catalog import Catalog

class CatalogTests(unittest.TestCase):
    def test_import_and_isolation(self):
        with tempfile.TemporaryDirectory() as root:
            a,b=Catalog("nikke",root),Catalog("brown_dust_2",root)
            try:
                r={"kind":"character","name":"Example","patch":"test","source":"local:test","data":{"role":"support"}}
                a.ingest([r,r])
                self.assertEqual(len(a.search("Example")),1)
                self.assertEqual(a.search("Example",patch="other"),[])
                self.assertEqual(b.search(),[])
            finally:a.close();b.close()
