import json
from pathlib import Path
from .qt_workbench import Workbench,launch
from .bd2_data import seed_characters,import_catalog,save_snapshot,study_video
from .bd2_tactics import Skill,optimize
from .bd2_observe import screenshot,resource_candidates,mfabd2_status
from .bd2_news import sync
class Lab(Workbench):
    def __init__(self):
        super().__init__("Laboratoire Brown Dust 2","Analyse tactique expérimentale · OCR · Catalogue",select_game=False)
        self.section("Analyse tactique",[("Indexer personnages","Catalogue initial",lambda:self.run(seed_characters)),("Importer catalogue JSON","Données normalisées",self.catalog),("Optimiser une équipe JSON","Estimation sur un tour",self.teams),("Analyser une capture","OCR et ressources à confirmer",self.capture)])
        self.section("Recherche & diagnostic",[("Étudier une vidéo locale","Transcription autorisée",self.video),("Actualiser les annonces","Flux RSS expérimental",lambda:self.run(sync)),("Diagnostic MFABD2","Journaux locaux",lambda:self.run(mfabd2_status))]);self.controls.addStretch()
    def catalog(self):
        p=self.file("JSON (*.json)")
        if p:self.run(lambda:import_catalog(p))
    def teams(self):
        p=self.file("JSON (*.json)")
        if p:
            def work():
                d=json.loads(Path(p).read_text(encoding="utf-8"));return optimize([Skill(**s) for s in d["skills"]],d["sp"],d.get("slots",5))
            self.run(work)
    def capture(self):
        p=self.file("Images (*.png *.jpg *.jpeg *.webp)")
        if p:
            def done(rows):
                candidates=resource_candidates(rows);self.show_result({"ocr":rows,"resource_candidates":candidates})
                if candidates and self.confirm("Vérification","Ces valeurs sont-elles exactes ?\n"+str(candidates)):save_snapshot(candidates)
            self.run(lambda:screenshot(p),done)
    def video(self):
        p=self.file()
        if not p:return
        s=self.ask("Source","URL ou référence du contenu autorisé");v=self.ask("Version","Patch ou date") if s else ""
        if v and self.confirm("Autorisation","Confirmer le droit d’analyser cette vidéo ?"):self.run(lambda:study_video(p,s,v))
if __name__=="__main__":launch(Lab)
