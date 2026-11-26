import os,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
try:
    from PySide6.QtWidgets import QApplication,QPushButton
except ImportError:
    QApplication=None
@unittest.skipIf(QApplication is None,"Optional Qt extra")
class StudioTest(unittest.TestCase):
    def test_library_and_profiles(self):
        from gameagent.obsidian_ui import Studio,TOOLS
        app=QApplication.instance() or QApplication([])
        w=Studio()
        try:
            self.assertEqual(len(w.profiles),6)
            for game in w.profiles:
                w.profile(game)
                self.assertTrue(any("panel complet" in b.text() for b in w.findChildren(QPushButton)))
            w.library()
            self.assertEqual(sum("Voir le profil" in b.text() for b in w.findChildren(QPushButton)),6)
        finally:w.close()
