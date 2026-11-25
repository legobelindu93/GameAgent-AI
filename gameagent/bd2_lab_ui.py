"""Research workbench for offline BD2 analysis."""
import tkinter as tk
from tkinter import ttk,filedialog,simpledialog,messagebox
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from .theme import apply,console
from .bd2_data import seed_characters,import_catalog,save_snapshot,study_video
from .bd2_tactics import Skill,optimize
from .bd2_observe import screenshot,resource_candidates,mfabd2_status
from .bd2_news import sync

def main():
    root=tk.Tk();root.title("BD2 | Laboratoire expert");root.geometry("1100x760");apply(root)
    panel=ttk.Frame(root,padding=20);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="Brown Dust 2 — Analyse experte",style="Title.TLabel").pack(anchor="w")
    ttk.Label(panel,text="Analyse locale, résultats à vérifier. Aucun contrôle du jeu.",style="Muted.TLabel").pack(anchor="w",pady=8)
    bar=ttk.Frame(panel);bar.pack(fill="x")
    out=None;pool=ThreadPoolExecutor(max_workers=1);busy=False
    def show(result):
        out.delete("1.0","end");out.insert("end",json.dumps(result,ensure_ascii=False,indent=2))
    def job(fn,done=show):
        nonlocal busy
        if busy:return
        busy=True;show({"status":"Analyse en cours"})
        f=pool.submit(fn)
        def poll():
            nonlocal busy
            if not f.done():root.after(150,poll);return
            busy=False
            try:done(f.result())
            except Exception as e:show({"error":str(e)})
        root.after(150,poll)
    def catalog():
        p=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if p:job(lambda:import_catalog(p))
    def teams():
        p=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not p:return
        def work():
            data=json.loads(Path(p).read_text(encoding="utf-8"))
            return optimize([Skill(**s) for s in data["skills"]],data["sp"],data.get("slots",5))
        job(work)
    def image():
        p=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.webp")])
        if not p:return
        def done(rows):
            candidates=resource_candidates(rows)
            show({"ocr":rows,"resource_candidates":candidates})
            if candidates and messagebox.askyesno("Vérification",str(candidates)+"\nCes valeurs sont-elles exactes ?"):
                save_snapshot(candidates)
        job(lambda:screenshot(p),done)
    def video():
        p=filedialog.askopenfilename()
        if not p:return
        source=simpledialog.askstring("Source","URL ou référence du contenu autorisé")
        if not source:return
        patch=simpledialog.askstring("Version","Version du jeu / date du guide")
        if patch:job(lambda:study_video(p,source,patch))
    for i,(name,fn) in enumerate([
        ("Indexer personnages",lambda:job(seed_characters)),("Importer catalogue JSON",catalog),
        ("Optimiser une équipe JSON",teams),("Analyser une capture",image),
        ("Étudier une vidéo locale",video),("Actualiser les annonces",lambda:job(sync)),
        ("Diagnostic MFABD2",lambda:job(mfabd2_status))]):
        ttk.Button(bar,text=name,command=fn).grid(row=i//3,column=i%3,sticky="ew",padx=4,pady=4)
    for i in range(3):bar.columnconfigure(i,weight=1)
    out=console(panel)
    root.protocol("WM_DELETE_WINDOW",lambda:(pool.shutdown(wait=False,cancel_futures=True),root.destroy()))
    root.mainloop()
if __name__=="__main__":main()
