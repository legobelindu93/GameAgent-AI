"""Full Qt game console using the original installation and process APIs."""
import sys,subprocess,webbrowser,json
from pathlib import Path
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QTabWidget,QListWidget,QInputDialog,QLineEdit,QMessageBox)
from .qt_workbench import Workbench,launch
from .obsidian_ui import label,button
from .game_data import identity
from .project_hub import project,inspect
from .installations import releases,download
from .bridges import describe,start_interface
from .task_catalog import inventory
from . import native,dependencies
from .qt_native_host import make_host

class Console(Workbench):
    def __init__(self,game="brown_dust_2"):
        super().__init__("Console des jeux","Installation · configuration · interface originale · diagnostic",game)
        self.processes={};self.assets=[];self.last_game=game
        self.tabs=QTabWidget();self.controls.addWidget(self.tabs)
        self.home,self.install,self.embed,self.diagnostics=[QVBoxLayout(QWidget()) for _ in range(4)]
        for title,layout in zip(("Application","Installation","Interface native","Diagnostic"),(self.home,self.install,self.embed,self.diagnostics)):
            self.tabs.addTab(layout.parentWidget(),title)
        self.info=label("","section");self.home.addWidget(self.info)
        self.path=label("","subtitle");self.home.addWidget(self.path)
        self.start_button=button("Ouvrir l’application",self.start,"primary");self.home.addWidget(self.start_button)
        for title,fn in [("Configurer l’exécutable",self.configure),("Adresse WebUI",self.configure_web),("Ouvrir WebUI",self.web),("Inventorier les composants réels",self.inventory),("Launcher classique (secours)",self.classic)]:
            self.home.addWidget(button(title,fn))
        self.features=label("","subtitle");self.home.addWidget(self.features);self.home.addStretch()
        self.install.addWidget(button("Rechercher les versions",self.search,"primary"))
        self.release_status=label("Sélectionnez une version","subtitle");self.install.addWidget(self.release_status)
        self.listing=QListWidget();self.install.addWidget(self.listing)
        self.install.addWidget(button("Télécharger le fichier sélectionné",self.fetch))
        self.install.addWidget(button("Installer les dépendances",self.provision))
        self.install.addWidget(button("Instructions officielles",lambda:self.link("documentation")))
        self.install.addWidget(button("Toutes les versions GitHub",lambda:self.link("releases")))
        self.install.addWidget(label("Après téléchargement, suivez les instructions du projet d’origine. Aucun fichier téléchargé n’est exécuté automatiquement.","subtitle"))
        self.install.addStretch()
        self.host_status=label("Lancez l’application depuis cette console avant de sélectionner sa fenêtre.","subtitle");self.embed.addWidget(self.host_status)
        bar=QHBoxLayout();bar.addWidget(button("Embarquer la fenêtre",self.attach,"primary"));bar.addWidget(button("Détacher",self.detach));self.embed.addLayout(bar)
        self.surface,self.host=make_host();self.embed.addWidget(self.surface,1)
        self.diagnostics.addWidget(button("Analyser les sources locales",self.diagnostic))
        self.diagnostics.addWidget(button("Inventorier les composants réels",self.inventory))
        self.diagnostics.addStretch()
        self.gamebox.currentIndexChanged.connect(self.select_game)
        self.refresh()
    def error(self,exc):
        self.show_result("Erreur : "+str(exc))
    def refresh(self):
        try:
            g=self.game;m=project(g);s=native.load(g);d=describe(g);exe=s.get("executable","")
            ready=bool(exe and Path(exe).is_file()) or (d["entry_available"] and d["environment_available"])
            self.info.setText(m["name"]+" · "+m["interface"]+" · "+("Configurée" if ready else "À configurer"))
            self.path.setText(exe or "Aucun exécutable sélectionné")
            self.start_button.setEnabled(ready);self.features.setText("Fonctions du projet original (informatif)\n"+ "\n".join("• "+x for x in identity(g)["features"]))
        except Exception as exc:self.error(exc)
    def select_game(self):
        try:self.host.detach()
        except Exception as exc:
            self.error(exc);self.gamebox.blockSignals(True);self.gamebox.setCurrentIndex(self.gamebox.findData(self.last_game));self.gamebox.blockSignals(False);self.change_banner();return
        self.last_game=self.game;self.assets=[];self.listing.clear();self.release_status.setText("Sélectionnez une version");self.host_status.setText("Fenêtre détachée");self.refresh()
    def configure(self):
        p=self.file("Exécutables Windows (*.exe)")
        if p:
            try:native.save(self.game,p,native.load(self.game).get("web_url",""));self.refresh()
            except Exception as exc:self.error(exc)
    def configure_web(self):
        try:
            old=native.load(self.game);url,ok=QInputDialog.getText(self,"WebUI","Adresse HTTP locale et port",QLineEdit.EchoMode.Normal,old.get("web_url",""))
            if ok:native.save(self.game,old.get("executable",""),url)
        except Exception as exc:self.error(exc)
    def web(self):
        try:
            if not native.load(self.game).get("web_url"):self.configure_web()
            if native.load(self.game).get("web_url"):subprocess.Popen([sys.executable,"-m","gameagent.native",self.game])
        except Exception as exc:self.error(exc)
    def start(self):
        g=self.game
        if g in self.processes and self.processes[g].poll() is None:self.show_result("Une instance ouverte depuis cette console existe déjà.");return
        if not self.confirm("Application tierce","Ouvrir l’application originale ? Utilisez-la uniquement dans un environnement autorisé."):return
        try:self.processes[g]=start_interface(g);self.show_result("Application ouverte : "+g)
        except Exception as exc:self.error(exc)
    def attach(self):
        try:
            p=self.processes.get(self.game)
            if p is None or p.poll() is not None:raise ValueError("Lancez d’abord l’application depuis cette console.")
            windows=self.host.candidates(p.pid)
            if not windows:raise ValueError("Aucune fenêtre de ce processus détectée. Les processus enfants restent en mode externe.")
            names=[f"{i+1}. {title}" for i,(_,title) in enumerate(windows)]
            selected,ok=QInputDialog.getItem(self,"Fenêtre","Sélectionner la fenêtre",names,0,False)
            if not ok:return
            hwnd,title=windows[names.index(selected)];self.host.attach(hwnd,p.pid);self.host_status.setText(title+" · intégration expérimentale")
        except Exception as exc:self.error(exc)
    def detach(self):
        try:self.host.detach();self.host_status.setText("Fenêtre détachée")
        except Exception as exc:self.error(exc)
    def search(self):
        g=self.game
        def done(r):
            self.assets=r["assets"];self.listing.clear()
            for a in self.assets:self.listing.addItem(a["name"]+" · "+str(round(a["size"]/1048576,1))+" Mo")
            self.release_status.setText(r["tag"]+" · "+str(len(self.assets))+" fichiers")
        self.run(lambda:releases(g),done)
    def fetch(self):
        i=self.listing.currentRow()
        if not 0<=i<len(self.assets):return
        g=self.game;a=self.assets[i]
        if self.confirm("Téléchargement","Télécharger "+a["name"]+" sans l’exécuter ?"):self.run(lambda:download(g,a))
    def provision(self):
        g=self.game
        if g in {"genshin_impact","brown_dust_2"}:
            if self.confirm("Dépendances","Installer .NET Desktop 10 et VC++ x64 via winget ?"):self.run(lambda:dependencies.install_runtime(g))
        else:
            v=self.ask("Python","Version Python exigée par le dépôt","3.12")
            if v and self.confirm("Dépendances","Installer les requirements.txt du dépôt local dans un environnement isolé après vérification des sources ?"):self.run(lambda:dependencies.install_python(g,v))
    def link(self,field):webbrowser.open(project(self.game)[field])
    def inventory(self):
        g=self.game;self.run(lambda:inventory(g))
    def diagnostic(self):
        g=self.game
        def work():
            r=inspect(g);return {"dependencies":dependencies.diagnostic(g),"bridge":describe(g),"revision":r["revision"],"files":len(r["files"]),"licenses":r["licenses"]}
        self.run(work)
    def classic(self):subprocess.Popen([sys.executable,"-m","gameagent.launcher_ui","--game",self.game])
    def closeEvent(self,event):
        try:self.host.detach()
        except Exception as exc:self.error(exc);event.ignore();return
        super().closeEvent(event)
if __name__=="__main__":
    from .profiles import load_profiles
    g=sys.argv[sys.argv.index("--game")+1] if "--game" in sys.argv and sys.argv.index("--game")+1<len(sys.argv) else "brown_dust_2"
    launch(lambda:Console(g if g in load_profiles() else "brown_dust_2"))
