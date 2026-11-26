"""Shared Qt workbench: responsive split panes and bounded background jobs."""
import json,sys
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QFrame,QComboBox,QLineEdit,QPlainTextEdit,QSplitter,QScrollArea,QPushButton,QFileDialog,QInputDialog,QMessageBox,QTabWidget)
from .obsidian_ui import STYLE,label,button,image
from .profiles import load_profiles
EXTRA="""
QLineEdit,QComboBox,QPlainTextEdit {background:#15171d;border:1px solid #30333b;border-radius:8px;padding:9px;color:#f5f5f7;selection-background-color:#536b30;}
QPlainTextEdit {font-family:Consolas;font-size:13px;}
QTabWidget::pane {border:1px solid #262930;border-radius:8px;}
QTabBar::tab {background:#15171d;color:#969ca8;padding:12px 16px;margin-right:3px;}
QTabBar::tab:selected {color:#c5f36b;background:#22291b;}
QPushButton:disabled {color:#777d86;background:#121318;}
QSplitter::handle {background:#262930;width:4px;}
"""
class Workbench(QMainWindow):
    def __init__(self,title,subtitle,game="brown_dust_2",select_game=True):
        super().__init__();self.setWindowTitle("GameAgent — "+title);self.resize(1360,850);self.setMinimumSize(980,650)
        self.pool=ThreadPoolExecutor(max_workers=1);self.future=None;self.callback=None
        root=QWidget();self.setCentralWidget(root);outer=QVBoxLayout(root);outer.setContentsMargins(26,22,26,22);outer.setSpacing(14)
        top=QHBoxLayout();head=QVBoxLayout();head.addWidget(label("GAMEAGENT  /  OBSIDIAN WORKSPACE","eyebrow"));head.addWidget(label(title,"title"));head.addWidget(label(subtitle,"subtitle"));top.addLayout(head,1)
        self.gamebox=QComboBox()
        for k,p in load_profiles().items():self.gamebox.addItem(p["name"],k)
        self.gamebox.setCurrentIndex(self.gamebox.findData(game));self.gamebox.setVisible(select_game);top.addWidget(self.gamebox)
        outer.addLayout(top)
        self.banner=QHBoxLayout();self.banner.addWidget(image(game,1100,110));outer.addLayout(self.banner)
        self.gamebox.currentIndexChanged.connect(self.change_banner)
        split=QSplitter(Qt.Orientation.Horizontal);outer.addWidget(split,1)
        scroll=QScrollArea();scroll.setWidgetResizable(True);left=QWidget();self.controls=QVBoxLayout(left);self.controls.setContentsMargins(0,0,10,0);self.controls.setSpacing(10);scroll.setWidget(left);split.addWidget(scroll)
        right=QFrame();right.setObjectName("card");r=QVBoxLayout(right);header=QHBoxLayout();header.addWidget(label("Résultats & journal","section"),1);header.addWidget(button("Copier",lambda:QApplication.clipboard().setText(self.output.toPlainText())));r.addLayout(header)
        self.status=label("Prêt · aucun traitement lancé","subtitle");r.addWidget(self.status)
        self.output=QPlainTextEdit();self.output.setReadOnly(True);self.output.setPlaceholderText("Les résultats apparaîtront ici.");r.addWidget(self.output,1);split.addWidget(right);split.setSizes([510,760])
        self.timer=QTimer(self);self.timer.setInterval(100);self.timer.timeout.connect(self.poll)
    @property
    def game(self):return self.gamebox.currentData()
    def change_banner(self):
        old=self.banner.takeAt(0)
        if old:old.widget().deleteLater()
        self.banner.addWidget(image(self.game,1100,110))
    def show_result(self,obj):
        self.output.setPlainText(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2,default=str))
    def run(self,fn,done=None):
        if self.future is not None:return
        self.controls.parentWidget().setEnabled(False);self.gamebox.setEnabled(False);self.status.setText("Traitement en cours…")
        self.callback=done;self.future=self.pool.submit(fn);self.timer.start()
    def poll(self):
        if self.future is None or not self.future.done():return
        self.timer.stop();future=self.future;self.future=None
        self.controls.parentWidget().setEnabled(True);self.gamebox.setEnabled(True)
        try:
            result=future.result()
            if self.callback:self.callback(result)
            else:self.show_result(result)
            self.status.setText("Traitement terminé")
        except Exception as exc:self.show_result("Erreur : "+str(exc));self.status.setText("Échec du traitement")
    def ask(self,title,prompt,default=""):
        value,ok=QInputDialog.getText(self,title,prompt,QLineEdit.EchoMode.Normal,default)
        return value if ok else ""
    def confirm(self,title,prompt):
        return QMessageBox.question(self,title,prompt,QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)==QMessageBox.StandardButton.Yes
    def file(self,kind="Tous les fichiers (*)"):
        return QFileDialog.getOpenFileName(self,"Choisir un fichier","",kind)[0]
    def save(self):return QFileDialog.getSaveFileName(self,"Enregistrer","","JSON (*.json)")[0]
    def folder(self):return QFileDialog.getExistingDirectory(self,"Choisir un dossier")
    def section(self,title,actions):
        card=QFrame();card.setObjectName("card");l=QVBoxLayout(card);l.setContentsMargins(14,14,14,14);l.addWidget(label(title,"section"))
        for name,description,fn in actions:
            b=button(name+"  →",fn);b.setToolTip(description);l.addWidget(b);l.addWidget(label(description,"subtitle"))
        self.controls.addWidget(card)
    def closeEvent(self,event):
        if self.future is not None and not self.future.done():
            QMessageBox.information(self,"Traitement actif","Attendez la fin du traitement avant de fermer cette fenêtre.");event.ignore();return
        self.timer.stop();self.pool.shutdown(wait=False,cancel_futures=True);event.accept()
def launch(cls):
    app=QApplication.instance() or QApplication(sys.argv);app.setStyleSheet(STYLE+EXTRA);w=cls();w.show();return app.exec()
