"""Modern Qt library; the original launcher remains available for full native hosting."""
import sys,subprocess
from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QPixmap,QImage
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QFrame,QScrollArea,QStackedWidget,QSizePolicy)
from .profiles import load_profiles
from .game_data import identity
from .project_hub import project
from .obsidian_art import cover
from . import native
from .bridges import describe
from pathlib import Path

STYLE="""
QWidget {background:#0a0b0e;color:#f5f5f7;font-family:'Segoe UI';font-size:13px;}
QFrame#sidebar {background:#101116;border-right:1px solid #262930;}
QFrame#card {background:#15171d;border:1px solid #262930;border-radius:12px;}
QFrame#card QLabel,QFrame#sidebar QLabel {background:transparent;}
QLabel#title {font-size:32px;font-weight:700;}
QLabel#subtitle {color:#969ca8;font-size:13px;}
QLabel#eyebrow {color:#c5f36b;font-size:11px;font-weight:700;}
QLabel#section {font-size:20px;font-weight:600;}
QPushButton {background:#1b1e25;border:1px solid #30333b;border-radius:7px;padding:10px 14px;text-align:left;}
QPushButton:hover {background:#292e35;border-color:#646c58;}
QPushButton:focus {border:2px solid #c5f36b;}
QPushButton#primary {background:#c5f36b;color:#141a0d;font-weight:700;border:0;}
QPushButton#primary:hover {background:#dcff99;}
QPushButton#nav {background:transparent;border:0;color:#a6abb5;}
QPushButton#nav:hover {background:#22291b;color:#c5f36b;}
QScrollArea {border:0;} QScrollBar:vertical {background:#101116;width:9px;} QScrollBar::handle:vertical {background:#424650;border-radius:4px;min-height:24px;}
"""
TOOLS=[("Research Factory","gameagent.research_center_ui"),("Connaissances","gameagent.research_ui"),("Expert F2P","gameagent.bd2_expert_ui"),("Laboratoire tactique","gameagent.bd2_lab_ui"),("Explorateur de sources","gameagent.hub_ui"),("Simulation","gameagent.simulation_ui")]
def label(text,kind=""):
    w=QLabel(text);w.setObjectName(kind);w.setWordWrap(True);return w
def button(text,fn,kind=""):
    b=QPushButton(text);b.setObjectName(kind);b.clicked.connect(fn);b.setCursor(Qt.CursorShape.PointingHandCursor);return b
def image(game,w,h):
    im=cover(game,w,h)
    q=QImage(im.tobytes(),im.width,im.height,im.width*3,QImage.Format.Format_RGB888).copy()
    a=QLabel();a.setPixmap(QPixmap.fromImage(q));a.setScaledContents(True);a.setFixedHeight(h);a.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Fixed);return a
class Studio(QMainWindow):
    def __init__(self):
        super().__init__();self.setWindowTitle("GameAgent — Obsidian Studio");self.resize(1400,900);self.setMinimumSize(1000,690)
        self.profiles=load_profiles()
        root=QWidget();self.setCentralWidget(root);layout=QHBoxLayout(root);layout.setContentsMargins(0,0,0,0);layout.setSpacing(0)
        side=QFrame();side.setObjectName("sidebar");side.setFixedWidth(238);nav=QVBoxLayout(side);nav.setContentsMargins(16,24,16,18);nav.setSpacing(5)
        nav.addWidget(label("GAMEAGENT","section"));nav.addWidget(label("RESEARCH STUDIO","eyebrow"));nav.addSpacing(20)
        nav.addWidget(button("Bibliothèque",self.library,"nav"))
        for title,module in TOOLS:nav.addWidget(button(title,lambda checked=False,m=module:self.open_module(m),"nav"))
        nav.addSpacing(18);nav.addWidget(label("PROFILS","eyebrow"))
        for game,p in self.profiles.items():nav.addWidget(button(p["name"],lambda checked=False,g=game:self.profile(g),"nav"))
        nav.addStretch();nav.addWidget(button("Launcher complet / classique",lambda:self.open_module("gameagent.launcher_ui"),"nav"));nav.addWidget(label("v0.13 · Prototype","subtitle"))
        layout.addWidget(side)
        self.scroll=QScrollArea();self.scroll.setWidgetResizable(True);layout.addWidget(self.scroll,1);self.library()
    def open_module(self,module,game=None):
        args=[sys.executable,"-m",module]
        if game and module=="gameagent.launcher_ui":args.extend(["--game",game])
        subprocess.Popen(args)
    def page(self,title,desc):
        w=QWidget();l=QVBoxLayout(w);l.setContentsMargins(28,26,28,30);l.setSpacing(16)
        l.addWidget(label("LOCAL WORKSPACE  /  RESEARCH","eyebrow"));l.addWidget(label(title,"title"));l.addWidget(label(desc,"subtitle"));self.scroll.setWidget(w);return l
    def library(self):
        l=self.page("Bibliothèque","Vos six profils, projets communautaires et outils de recherche.")
        hero=QFrame();hero.setObjectName("card");row=QHBoxLayout(hero);row.setContentsMargins(20,20,20,20)
        left=QVBoxLayout();left.addWidget(label("PROFIL À LA UNE","eyebrow"));left.addWidget(label("Brown Dust 2","title"));left.addWidget(label("RPG tactique · MFABD2 · 20 fiches initiales","subtitle"));left.addWidget(button("Ouvrir le profil",lambda:self.profile("brown_dust_2"),"primary"));row.addLayout(left,1);row.addWidget(image("brown_dust_2",500,160),1);l.addWidget(hero)
        l.addWidget(label("Tous les jeux","section"));grid=QGridLayout();grid.setSpacing(14)
        for i,(g,p) in enumerate(self.profiles.items()):
            card=QFrame();card.setObjectName("card");cl=QVBoxLayout(card);cl.setContentsMargins(12,12,12,12);cl.setSpacing(8)
            cl.addWidget(image(g,480,135));cl.addWidget(label(p["name"],"section"));cl.addWidget(label(identity(g)["genre"],"subtitle"));cl.addWidget(button("Voir le profil  →",lambda checked=False,k=g:self.profile(k)))
            grid.addWidget(card,i//3,i%3)
        for i in range(3):grid.setColumnStretch(i,1)
        l.addLayout(grid);l.addStretch()
    def profile(self,g):
        p=self.profiles[g];meta=project(g);l=self.page(p["name"],meta["name"]+" · "+meta["interface"])
        l.addWidget(image(g,1100,210))
        settings=native.load(g);info=describe(g);exe=settings.get("executable","")
        ready=bool(exe and Path(exe).is_file()) or (info["entry_available"] and info["environment_available"])
        l.addWidget(label("Application configurée" if ready else "Configuration requise","eyebrow"))
        l.addWidget(label(exe or "Aucun exécutable sélectionné","subtitle"))
        l.addWidget(button("Ouvrir le panel complet du jeu",lambda:self.open_module("gameagent.launcher_ui",g),"primary"))
        l.addWidget(label("Installation · configuration · WebUI · fenêtre native · diagnostic sont disponibles dans le panel complet.","subtitle"))
        l.addWidget(label("Fonctions du projet original","section"))
        for f in identity(g)["features"]:l.addWidget(label("•  "+f))
        l.addStretch()
def main():
    app=QApplication.instance() or QApplication(sys.argv);app.setStyleSheet(STYLE);window=Studio();window.show();return app.exec()
if __name__=="__main__":main()
