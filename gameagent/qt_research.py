"""Qt Research Factory: all 19 existing operations, with grouped workspaces."""
from pathlib import Path
import webbrowser
from .qt_workbench import Workbench,launch
from .packs import PACKS,registry,coverage,load_json,make,atomic,install,verify,https_url
from .research_engine import discover,research_cycle,import_notes,compile_candidates
from .account_import import import_account
from .cloud_study import video_study,web_dossier
from .pack_review import benchmark,review
from .patch_watch import check
from .factory import batch,offline_advice,build_bundle,bootstrap,dossier_candidates
JSON="JSON (*.json)"
TEXT="Documents (*.txt *.md *.srt *.vtt)"
class Research(Workbench):
    def __init__(self):
        super().__init__("Research Factory","Découvrir, étudier et valider des connaissances · Local + Cloud")
        self.section("01 / Découvrir",[
            ("Sources","Registre de sources du profil",lambda:self.simple(registry)),
            ("Rechercher","Découverte de ressources par sujet",self.search),
            ("Cycle de recherche","Recherche guidée par la couverture",lambda:self.simple(research_cycle)),
            ("Couverture indicative","Mesurer les résultats indexés",lambda:self.simple(coverage)),
            ("Recherche autonome ciblée","Recherche distante avec confirmation",self.batch_web),
            ("Vérifier annonces","Comparer les nouvelles URL",lambda:self.simple(check))])
        self.section("02 / Étudier",[
            ("Étudier vidéo YouTube","Analyse distante autorisée",self.video),
            ("Recherche IA web","Dossier cité et pack candidat",self.web),
            ("Importer notes / sous-titres","Index local de documents autorisés",self.notes),
            ("Compiler via API","Transformer un document en fiches candidates",self.compile),
            ("Ouvrir une source","Ouvrir une URL HTTPS",self.source)])
        self.section("03 / Packs",[
            ("Installer pack initial","Installer les fiches fournies pour ce jeu",self.seed),
            ("Installer les six packs","Installer toutes les fiches initiales",self.all_seeds),
            ("Importer pack","Vérifier et importer les fiches approuvées",self.pack),
            ("Exporter les six packs","Créer un bundle portable",self.bundle),
            ("Valider un pack","Validation explicite des identifiants",self.review)])
        self.section("04 / Compte & analyse",[
            ("Importer compte","Importer un export JSON normalisé",self.account),
            ("Conseil hors ligne","Retrouver les preuves locales",self.offline),
            ("Benchmark local","Tester la recherche des fiches initiales",lambda:self.simple(benchmark))])
        self.controls.addStretch()
    def simple(self,fn):
        g=self.game;self.run(lambda:fn(g))
    def search(self):
        g=self.game;q=self.ask("Recherche","Sujet à étudier")
        if q:self.run(lambda:discover(g,q))
    def batch_web(self):
        g=self.game
        if self.confirm("Recherche distante","Autoriser une requête distante ciblée ? Des frais peuvent s’appliquer."):self.run(lambda:batch(g,web=True,authorized=True))
    def video(self):
        g=self.game;url=self.ask("Vidéo","URL YouTube publique autorisée")
        if not url:return
        p=self.ask("Version","Patch ou date");target=self.save() if p else ""
        if target and self.confirm("Gemini","Confirmer les droits et l’analyse distante ? Frais possibles."):
            def work():
                pack=video_study(g,url,p,authorized=True);atomic(target,pack);return {"candidates":len(pack["records"]),"output":target}
            self.run(work)
    def web(self):
        g=self.game;q=self.ask("Recherche IA","Sujet");target=self.save() if q else ""
        if target and self.confirm("API distante","Autoriser la recherche web ? Frais possibles."):
            def work():
                d=web_dossier(g,q,True);atomic(target,d);candidate=Path(target).with_name(Path(target).stem+".pack.json");atomic(candidate,dossier_candidates(d));return dict(d,candidate_pack=str(candidate))
            self.run(work)
    def document(self):
        p=self.file(TEXT)
        if not p:return None
        s=self.ask("Source","URL HTTPS");v=self.ask("Version","Patch ou date") if s else ""
        return (p,s,v) if v else None
    def notes(self):
        g=self.game;d=self.document()
        if d and self.confirm("Autorisation","Confirmer le droit d’utiliser ce document ?"):self.run(lambda:import_notes(g,*d,True))
    def compile(self):
        g=self.game;d=self.document();target=self.save() if d else ""
        if target and self.confirm("API distante","Envoyer le document sélectionné à OpenAI ? Frais possibles."):
            def work():
                p,s,v=d;pack=compile_candidates(g,p,"1.0.0",s,v,True);atomic(target,pack);return {"candidates":len(pack["records"]),"output":target}
            self.run(work)
    def source(self):
        url=self.ask("Source","URL HTTPS")
        if url and https_url(url):webbrowser.open(url)
    def seed(self):
        g=self.game
        def work():
            target=Path("data/packs")/g/"seed-v1.json";atomic(target,make(g,"1.0.0",load_json(PACKS/g/"seed.json")));return install(target,g,trusted=True)
        self.run(work)
    def all_seeds(self):
        if self.confirm("Packs","Installer les six packs fournis ?"):self.run(bootstrap)
    def pack(self):
        g=self.game;p=self.file(JSON)
        if not p:return
        try:self.show_result(verify(load_json(p),g))
        except Exception as exc:self.show_result(str(exc));return
        if self.confirm("Import","Confirmer la provenance et importer uniquement les fiches approuvées ?"):self.run(lambda:install(p,g,trusted=True))
    def bundle(self):
        p=self.folder()
        if p:self.run(lambda:build_bundle(p))
    def review(self):
        g=self.game;p=self.file(JSON)
        if not p:return
        try:obj=verify(load_json(p),g);self.show_result(obj)
        except Exception as exc:self.show_result(str(exc));return
        ids=self.ask("Validation","Identifiants vérifiés séparés par des espaces")
        if not ids:return
        version=self.ask("Version","Nouvelle version","1.0.1");target=self.save() if version else ""
        if target and self.confirm("Validation","Confirmer la vérification de chaque fiche auprès de sa source ?"):
            def work():
                pack=review(obj,ids.split(),version);atomic(target,pack);return {"output":target,"approved":sum(r["review"]=="approved" for r in pack["records"])}
            self.run(work)
    def account(self):
        g=self.game;p=self.file(JSON)
        if p and self.confirm("Compte","Importer ce fichier normalisé ?"):self.run(lambda:import_account(g,p,True))
    def offline(self):
        g=self.game;q=self.ask("Conseil hors ligne","Question")
        if q:self.run(lambda:offline_advice(g,q))
if __name__=="__main__":launch(Research)
