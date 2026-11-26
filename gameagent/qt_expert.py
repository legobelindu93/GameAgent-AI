import subprocess,sys
from PySide6.QtWidgets import QComboBox,QLineEdit,QFormLayout
from .qt_workbench import Workbench,launch
from .bd2_expert import Account,plan,ask,seed
class Expert(Workbench):
    def __init__(self):
        super().__init__("Expert Brown Dust 2","Planification F2P · Conseil local · Aucun contrôle du jeu",select_game=False)
        form=QFormLayout();self.fields={}
        for key,title,default,options in [
            ("stage","Progression","beginner",["beginner","midgame","endgame"]),
            ("damage","Équipe","unknown",["physical","magic","unknown"]),
            ("bottleneck","Blocage","unknown",["gear","gold","level","combat","unknown"]),
            ("goal","Objectif","story",["story","resources","boss","general"]),
            ("minutes","Minutes","30",None),("diamonds","Diamants","0",None),("tickets","Tickets","0",None),("costumes","Costumes (+niveau)","",None)]:
            if options:w=QComboBox();w.addItems(options);w.setCurrentText(default)
            else:w=QLineEdit(default)
            self.fields[key]=w;form.addRow(title,w)
        self.question=QLineEdit("Quelle progression privilégier avec ce compte ?");self.model=QLineEdit("qwen2.5:3b");form.addRow("Question",self.question);form.addRow("Modèle Ollama",self.model);self.controls.addLayout(form)
        self.section("Conseiller",[("Plan de progression F2P","Heuristique locale",self.planning),("Interroger l’IA locale","Conseil sourcé via Ollama",self.query),("Laboratoire expert","Ouvrir les outils tactiques",lambda:subprocess.Popen([sys.executable,"-m","gameagent.qt_lab"]))]);self.controls.addStretch()
    def account(self):
        d={k:(w.currentText() if isinstance(w,QComboBox) else w.text()) for k,w in self.fields.items()}
        for k in ("minutes","diamonds","tickets"):d[k]=int(d[k])
        return Account(**d)
    def planning(self):
        try:a=self.account()
        except Exception as exc:self.show_result(str(exc));return
        self.run(lambda:{"new_evidence":seed(),"plan":plan(a),"mode":"heuristique"})
    def query(self):
        try:a=self.account()
        except Exception as exc:self.show_result(str(exc));return
        q,m=self.question.text(),self.model.text();self.run(lambda:ask(a,q,m))
if __name__=="__main__":launch(Expert)
