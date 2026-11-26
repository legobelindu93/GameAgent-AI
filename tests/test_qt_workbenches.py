import os,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
try:
    from PySide6.QtWidgets import QApplication,QPushButton
except ImportError:
    QApplication=None
@unittest.skipIf(QApplication is None,"Optional Qt extra")
class WorkbenchTest(unittest.TestCase):
    def test_panels(self):
        from gameagent.qt_research import Research
        from gameagent.qt_knowledge import KnowledgePanel
        from gameagent.qt_expert import Expert
        from gameagent.qt_lab import Lab
        app=QApplication.instance() or QApplication([])
        for cls,count in [(Research,19),(KnowledgePanel,3),(Expert,3),(Lab,7)]:
            with self.subTest(panel=cls.__name__):
                w=cls()
                try:self.assertEqual(sum(b.text().endswith("  →") for b in w.findChildren(QPushButton)),count)
                finally:w.close()
