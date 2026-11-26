"""Read-only local source explorer with the existing configuration actions."""
import subprocess,sys,webbrowser
from PySide6.QtWidgets import QLineEdit,QListWidget,QInputDialog
from .qt_workbench import Workbench,launch
from .obsidian_ui import label,button
from .project_hub import project,inspect,read_source,open_folder
from . import native
class Sources(Workbench):
    def __init__(self):
        super().__init__("Explorateur de sources","Projets communautaires · lecture seule · licences et documentation")
        self.current=[]
        self.section("Dépôt",[("Dépôt GitHub","Page originale",lambda:self.link("repository")),("Documentation originale","Instructions",lambda:self.link("documentation")),("Versions publiées","Releases",lambda:self.link("releases")),("Dossier local","Ouvrir le dossier",self.folder_open),("Actualiser","Inventaire local",self.refresh)])
        self.section("Interface originale",[("Configurer interface","Exécutable et URL locale",self.configure),("Ouvrir interface originale","Programme tiers",self.start),("Afficher WebUI","Interface HTTP locale",self.web)])
        self.filter=QLineEdit();self.filter.setPlaceholderText("Filtrer les fichiers…");self.controls.addWidget(self.filter)
        self.listing=QListWidget();self.listing.setMinimumHeight(240);self.controls.addWidget(self.listing)
        self.filter.textChanged.connect(self.filter_files);self.listing.currentTextChanged.connect(self.preview)
        self.section("Autres espaces",[("Centre de connaissances","Index documentaire",lambda:self.open_module("qt_knowledge")),("Laboratoire simulation","Environnement synthétique",lambda:self.open_module("qt_simulation"))])
        self.gamebox.currentIndexChanged.connect(self.reset);self.reset()
    def reset(self):
        self.current=[];self.filter.clear();self.listing.clear();self.show_result("Sélectionnez Actualiser pour inventorier les sources locales.")
    def refresh(self):
        g=self.game
        def done(r):
            self.current=list(dict.fromkeys(r["licenses"]+r["docs"]+r["files"]));self.filter_files();self.show_result({"path":r["path"],"revision":r["revision"],"files":len(r["files"]),"licenses":r["licenses"]})
        self.run(lambda:inspect(g),done)
    def filter_files(self):
        q=self.filter.text().casefold();self.listing.clear();self.listing.addItems([p for p in self.current if q in p.casefold()])
    def preview(self,p):
        if not p:return
        try:self.show_result(read_source(self.game,p))
        except Exception as exc:self.show_result(str(exc))
    def link(self,k):webbrowser.open(project(self.game)[k])
    def folder_open(self):
        try:open_folder(self.game)
        except Exception as exc:self.show_result(str(exc))
    def configure(self):
        p=self.file("Exécutables Windows (*.exe)")
        if not p:return
        try:
            u,ok=QInputDialog.getText(self,"WebUI","URL locale facultative",text=native.load(self.game).get("web_url",""))
            if ok:native.save(self.game,p,u);self.show_result("Interface configurée")
        except Exception as exc:self.show_result(str(exc))
    def start(self):
        if self.confirm("Application tierce","Ouvrir le programme sélectionné dans un environnement autorisé ?"):
            try:native.launch(self.game)
            except Exception as exc:self.show_result(str(exc))
    def web(self):
        try:
            if not native.load(self.game).get("web_url"):raise ValueError("Configurez d’abord la WebUI.")
            subprocess.Popen([sys.executable,"-m","gameagent.native",self.game])
        except Exception as exc:self.show_result(str(exc))
    def open_module(self,name):subprocess.Popen([sys.executable,"-m","gameagent."+name])
if __name__=="__main__":launch(Sources)
