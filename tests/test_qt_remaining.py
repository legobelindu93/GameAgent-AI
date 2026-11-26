import os,tempfile,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    QApplication=None
@unittest.skipIf(QApplication is None,"Optional Qt extra")
class RemainingTest(unittest.TestCase):
    def test_console(self):
        from gameagent.qt_console import Console
        app=QApplication.instance() or QApplication([])
        w=Console()
        try:
            self.assertEqual(w.tabs.count(),4)
            self.assertEqual(w.game,"brown_dust_2")
            w.gamebox.setCurrentIndex(w.gamebox.findData("nikke"))
            self.assertEqual(w.last_game,"nikke")
            self.assertIsNone(w.host.window)
        finally:w.close()
    def test_sources(self):
        from gameagent.qt_sources import Sources
        app=QApplication.instance() or QApplication([])
        w=Sources()
        try:
            w.current=["README.md","src/main.py"];w.filter.setText("readme")
            self.assertEqual(w.listing.count(),1)
        finally:w.close()
    def test_simulation(self):
        from gameagent.qt_simulation import Simulation
        from gameagent.engine import Action
        app=QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as d:
            w=Simulation(d)
            try:
                w.act(Action.ATTACK,True)
                self.assertEqual(w.state.turn,1)
                self.assertEqual(len(w.memory.rows()),1)
                w.reset();self.assertEqual(w.state.turn,0)
            finally:w.close()
