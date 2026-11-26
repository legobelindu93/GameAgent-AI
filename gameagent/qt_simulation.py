"""Qt synthetic combat research panel, not a game controller."""
from uuid import uuid4
import subprocess,sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QComboBox,QHBoxLayout,QProgressBar
from .qt_workbench import Workbench,launch
from .obsidian_ui import label,button
from .engine import Action,step
from .planner import plan,legal
from .memory import Memory
from .imitation import Imitation
from .scenarios import initial
class Simulation(Workbench):
    def __init__(self,memory_root="data"):
        super().__init__("Laboratoire de simulation","Combat synthétique · planification · démonstrations · aucune action envoyée au jeu")
        self.memory_root=memory_root;self.memory=None;self.loop=QTimer(self);self.loop.setInterval(250);self.loop.timeout.connect(self.cycle)
        self.metrics=label("","section");self.controls.addWidget(self.metrics)
        self.health=QProgressBar();self.health.setRange(0,100);self.controls.addWidget(self.health)
        self.enemy=QProgressBar();self.enemy.setRange(0,100);self.controls.addWidget(self.enemy)
        self.style=QComboBox();self.style.addItems(["careful","balanced","aggressive"]);self.style.setCurrentText("balanced");self.controls.addWidget(self.style)
        self.section("Simulation",[("Un tour","Choisir une action avec le planificateur",self.one),("Lancer la simulation","Boucle synthétique limitée à 30 tours",self.start),("Arrêter","Suspendre la simulation",self.stop),("Réinitialiser","Nouvelle session isolée",self.reset)])
        self.section("Démonstrations",[(a.value,"Enregistrer un exemple",lambda checked=False,x=a:self.act(x,True)) for a in Action]+[("Imiter","Prédire à partir des démonstrations",self.imitate)])
        self.section("Vision hors ligne",[("Choisir les images","Comparer une capture enregistrée et un modèle",self.vision),("Centre de connaissances","Ouvrir l’index",lambda:subprocess.Popen([sys.executable,"-m","gameagent.qt_knowledge"]))])
        self.controls.addStretch();self.gamebox.currentIndexChanged.connect(self.reset);self.reset()
    def log(self,msg):self.output.appendPlainText(str(msg))
    def reset(self):
        self.stop()
        if self.memory:self.memory.close()
        self.state=initial(self.game);self.session=uuid4().hex;self.imitation=Imitation();self.memory=Memory(self.memory_root,self.game);self.output.clear();self.log("Session synthétique "+self.session);self.refresh()
    def refresh(self):
        s=self.state;self.metrics.setText(f"Tour {s.turn}  ·  Vie {s.hp}  ·  Ennemi {s.enemy}  ·  Potions {s.potions}");self.health.setValue(s.hp);self.enemy.setValue(s.enemy)
    def act(self,a=None,demonstrate=False):
        if not legal(self.state) or self.state.turn>=30:self.stop();return False
        if a is None:
            a,scores=plan(self.state,self.style.currentText());self.log("Scores : "+str(scores))
        if a not in legal(self.state):self.log("Action indisponible");return False
        if demonstrate:self.imitation.teach(self.state,a)
        new=step(self.state,a);self.memory.record(self.session,self.state,a,new);self.state=new;self.refresh();self.log(a.value+" : "+str(new));return bool(legal(new) and new.turn<30)
    def one(self):self.act()
    def cycle(self):
        if not self.act():self.stop()
    def start(self):
        if self.future is None and not self.loop.isActive():self.loop.start()
    def stop(self):self.loop.stop()
    def imitate(self):
        try:self.act(self.imitation.predict(self.state))
        except ValueError as exc:self.log(exc)
    def vision(self):
        self.stop();p=self.file("Images (*.png *.jpg *.jpeg *.webp)")
        if not p:return
        t=self.file("Images (*.png *.jpg *.jpeg *.webp)")
        if t:
            def work():
                from .vision import match_template
                return match_template(p,t)
            self.run(work,self.log)
    def closeEvent(self,event):
        self.stop();super().closeEvent(event)
        if event.isAccepted() and self.memory:self.memory.close();self.memory=None
if __name__=="__main__":launch(Simulation)
