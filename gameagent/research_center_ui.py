import tkinter as tk
from tkinter import ttk,filedialog,messagebox,simpledialog
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from .theme import apply,console
from .profiles import load_profiles
from .packs import PACKS,registry,coverage,load_json,make,atomic,install,verify,compare
from .research_engine import discover,research_cycle,import_notes,compile_candidates
from .account_import import import_account
from .cloud_study import video_study,web_dossier
from .pack_review import benchmark
from .patch_watch import check
from .factory import batch,offline_advice,build_bundle,bootstrap,dossier_candidates
from .pack_review import review
import webbrowser

def main():
    root=tk.Tk();root.title("GameAgent | Research Center");root.geometry("1050x760");apply(root)
    panel=ttk.Frame(root,padding=20);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="Research & Knowledge Factory",style="Title.TLabel").pack(anchor="w")
    ttk.Label(panel,text="Packs hors ligne · recherche facultative · aucun modèle GPU obligatoire",style="Muted.TLabel").pack(anchor="w",pady=8)
    game=tk.StringVar(value="brown_dust_2")
    ttk.Combobox(panel,textvariable=game,values=list(load_profiles()),state="readonly").pack(fill="x")
    bar=ttk.Frame(panel);bar.pack(fill="x",pady=8)
    pool=ThreadPoolExecutor(max_workers=1);busy=False
    def show(obj):
        out.delete("1.0","end");out.insert("end",json.dumps(obj,ensure_ascii=False,indent=2))
    def job(fn):
        nonlocal busy
        if busy:return
        busy=True;show({"status":"En cours"})
        f=pool.submit(fn)
        def poll():
            nonlocal busy
            if not f.done():root.after(200,poll);return
            busy=False
            try:show(f.result())
            except Exception as exc:show({"error":str(exc)})
        root.after(200,poll)
    def sources():
        g=game.get();job(lambda:registry(g))
    def search():
        g=game.get();topic=simpledialog.askstring("Recherche","Sujet à étudier")
        if topic:job(lambda:discover(g,topic))
    def cycle():
        g=game.get();job(lambda:research_cycle(g))
    def gaps():
        g=game.get();job(lambda:coverage(g))
    def seed():
        g=game.get();p=PACKS/g/"seed.json"
        if not p.exists():show({"status":"Pas encore de pack approuvé"});return
        def run():
            target=Path("data/packs")/g/"seed-v1.json";atomic(target,make(g,"1.0.0",load_json(p)));return install(target,g,trusted=True)
        job(run)
    def pack():
        g=game.get();p=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not p:return
        try:
            data=verify(load_json(p),g);show(data)
            if messagebox.askyesno("Importer","Importer uniquement les fiches approved après vérification de leur provenance ?"):
                job(lambda:install(p,g,trusted=True))
        except Exception as exc:show({"error":str(exc)})
    def notes():
        g=game.get();p=filedialog.askopenfilename(filetypes=[("Textes","*.txt *.md *.srt *.vtt")])
        if not p:return
        source=simpledialog.askstring("Source","URL HTTPS");patch=simpledialog.askstring("Version","Patch ou date")
        if source and patch and messagebox.askyesno("Autorisation","Tu as le droit d'utiliser ce document ?"):
            job(lambda:import_notes(g,p,source,patch,True))
    def account():
        g=game.get();p=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if p and messagebox.askyesno("Compte","Importer ce fichier local normalisé ?"):job(lambda:import_account(g,p,True))
    def compile_remote():
        g=game.get();p=filedialog.askopenfilename(filetypes=[("Textes","*.txt *.md *.srt *.vtt")])
        if not p:return
        s=simpledialog.askstring("Source","URL HTTPS");v=simpledialog.askstring("Version","Patch ou date")
        if not s or not v:return
        target=filedialog.asksaveasfilename(defaultextension=".json")
        if target and messagebox.askyesno("Service distant","Envoyer ce document à l'API OpenAI configurée ? Des frais peuvent s'appliquer."):
            def run():
                pack=compile_candidates(g,p,"1.0.0",s,v,True);atomic(target,pack);return {"candidates":len(pack["records"]),"output":target}
            job(run)
    def video_url():
        g=game.get();url=simpledialog.askstring("Vidéo","URL YouTube publique autorisée")
        if not url:return
        patch=simpledialog.askstring("Version","Version du guide ou date")
        if not patch:return
        target=filedialog.asksaveasfilename(defaultextension=".json")
        if target and messagebox.askyesno("Analyse distante","Confirmer les droits d'utilisation et l'analyse via Gemini ? Des frais peuvent s'appliquer."):
            def run():
                pack=video_study(g,url,patch,authorized=True);atomic(target,pack);return {"candidates":len(pack["records"]),"output":target}
            job(run)
    def web_study():
        g=game.get();topic=simpledialog.askstring("Recherche IA","Sujet")
        if not topic:return
        target=filedialog.asksaveasfilename(defaultextension=".json")
        if target and messagebox.askyesno("Recherche distante","Autoriser une recherche API (frais possibles) ?"):
            def run():
                result=web_dossier(g,topic,True);atomic(target,result)
                candidate=Path(target).with_name(Path(target).stem+".pack.json")
                atomic(candidate,dossier_candidates(result));return dict(result,candidate_pack=str(candidate))
            job(run)
    def open_source():
        from .packs import https_url
        url=simpledialog.askstring("Source","Coller une URL HTTPS du résultat")
        if url and https_url(url):webbrowser.open(url)
    def patch_check():
        g=game.get();job(lambda:check(g))
    def bench():
        g=game.get();job(lambda:benchmark(g))
    def offline():
        g=game.get();q=simpledialog.askstring("Consultation hors ligne","Question")
        if q:job(lambda:offline_advice(g,q))
    def batch_web():
        g=game.get()
        if messagebox.askyesno("Recherche ciblée","Autoriser une recherche IA sur le sujet le moins couvert ? Une requête distante, frais possibles."):
            job(lambda:batch(g,web=True,authorized=True))
    def bundle():
        target=filedialog.askdirectory()
        if target:job(lambda:build_bundle(target))
    def review_pack():
        g=game.get();p=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not p:return
        try:
            obj=verify(load_json(p),g);show(obj)
            ids=simpledialog.askstring("Validation manuelle","Identifiants des fiches vérifiées, séparés par des espaces")
            if not ids:return
            version=simpledialog.askstring("Version","Nouvelle version (ex. 1.0.1)")
            if not version:return
            target=filedialog.asksaveasfilename(defaultextension=".json")
            if target and messagebox.askyesno("Validation","Confirmer que tu as vérifié chaque fiche auprès de sa source ?"):
                def run():
                    pack=review(obj,ids.split(),version);atomic(target,pack);return {"output":target,"approved":sum(r["review"]=="approved" for r in pack["records"])}
                job(run)
        except Exception as exc:show({"error":str(exc)})
    def all_seeds():
        if messagebox.askyesno("Packs","Installer les six packs initiaux fournis avec GameAgent ?"):job(bootstrap)
    tabs=ttk.Notebook(bar);tabs.pack(fill="x")
    groups=[
        ("Découvrir",[("Sources",sources),("Rechercher",search),("Cycle de recherche",cycle),("Couverture indicative",gaps),("Recherche autonome ciblée",batch_web),("Vérifier annonces",patch_check)]),
        ("Étudier",[("Étudier vidéo YouTube",video_url),("Recherche IA web",web_study),("Importer notes / sous-titres",notes),("Compiler via API",compile_remote),("Ouvrir une source",open_source)]),
        ("Packs",[("Installer pack initial",seed),("Installer les six packs",all_seeds),("Importer pack",pack),("Exporter les six packs",bundle),("Valider un pack",review_pack)]),
        ("Compte & analyse",[("Importer compte",account),("Conseil hors ligne",offline),("Benchmark local",bench)])]
    for title,items in groups:
        page=ttk.Frame(tabs,padding=10);tabs.add(page,text=title)
        for i,(name,fn) in enumerate(items):
            ttk.Button(page,text=name,command=fn).grid(row=i//2,column=i%2,sticky="ew",padx=4,pady=4)
        for i in range(2):page.columnconfigure(i,weight=1)
    out=console(panel)
    root.protocol("WM_DELETE_WINDOW",lambda:(pool.shutdown(wait=False,cancel_futures=True),root.destroy()))
    root.mainloop()
if __name__=="__main__":main()
