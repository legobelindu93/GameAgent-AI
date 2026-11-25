import tkinter as tk
from tkinter import ttk,messagebox
from concurrent.futures import ThreadPoolExecutor
import webbrowser, subprocess,sys
from .profiles import load_profiles
from .theme import apply,sidebar,console
from .project_hub import project,inspect,read_source,open_folder

def main():
    root=tk.Tk()
    root.geometry("1280x800");root.minsize(950,600)
    root.title("GameAgent | Project Hub");apply(root)
    profiles=load_profiles()
    selected=None
    current=[]
    pool=ThreadPoolExecutor(max_workers=1)
    generation=0
    nav,pick=sidebar(root,profiles,lambda k:select(k))
    panel=ttk.Frame(root,padding=24);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="BIBLIOTHÈQUE / PROJETS OPEN SOURCE",style="Eyebrow.TLabel").pack(anchor="w")
    title=ttk.Label(panel,style="Title.TLabel");title.pack(anchor="w",pady=8)
    subtitle=ttk.Label(panel,style="Muted.TLabel");subtitle.pack(anchor="w",pady=(0,12))
    buttons=ttk.Frame(panel);buttons.pack(fill="x",pady=6)
    def link(field):
        if selected:webbrowser.open(project(selected)[field])
    for label,field in [("Dépôt GitHub","repository"),("Documentation originale","documentation"),("Versions publiées","releases")]:
        ttk.Button(buttons,text=label,command=lambda f=field:link(f)).pack(side="left",padx=(0,6))
    def folder():
        try:open_folder(selected)
        except Exception as exc:messagebox.showerror("Sources",str(exc))
    ttk.Button(buttons,text="Dossier local",command=folder,style="Accent.TButton").pack(side="left")
    status=ttk.Label(panel,style="Muted.TLabel");status.pack(anchor="w",pady=10)
    search=tk.StringVar()
    ttk.Entry(panel,textvariable=search).pack(fill="x",pady=(0,8))
    split=ttk.Panedwindow(panel,orient="horizontal");split.pack(fill="both",expand=True)
    left=ttk.Frame(split);right=ttk.Frame(split)
    split.add(left,weight=1);split.add(right,weight=3)
    listing=tk.Listbox(left,bg="#191e2b",fg="#eef2ff",selectbackground="#7658e8",relief="flat",width=38)
    scroll=ttk.Scrollbar(left,command=listing.yview);listing.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right",fill="y");listing.pack(fill="both",expand=True)
    preview=console(right)
    def show(text):
        preview.configure(state="normal");preview.delete("1.0","end");preview.insert("end",text);preview.configure(state="disabled")
    def filter_files(*_):
        listing.delete(0,"end")
        q=search.get().casefold()
        for p in current:
            if q in p.casefold():listing.insert("end",p)
    search.trace_add("write",filter_files)
    def display(_):
        if not listing.curselection():return
        try:show(read_source(selected,listing.get(listing.curselection()[0])))
        except Exception as exc:show(str(exc))
    listing.bind("<<ListboxSelect>>",display)
    def select(game):
        nonlocal selected,generation,current
        selected=game;generation+=1;token=generation
        meta=project(game)
        title.configure(text=profiles[game]["name"])
        subtitle.configure(text=meta["name"]+"  /  "+meta["interface"]+"  •  Interface tierce non intégrée")
        status.configure(text="Lecture des sources locales…")
        current=[];search.set("");show("Chargement…")
        future=pool.submit(inspect,game)
        def poll():
            nonlocal current
            if token!=generation:return
            if not future.done():root.after(100,poll);return
            try:r=future.result()
            except Exception as exc:status.configure(text=str(exc));return
            current=list(dict.fromkeys(r["licenses"]+r["docs"]+r["files"]))
            filter_files()
            status.configure(text=f"{len(r['files'])} fichiers locaux  |  Révision : {r['revision'] or 'non disponible'}")
            show("Sources originales : "+r["path"]+"\n\nSélectionnez un fichier pour le consulter. Aucun script tiers n’est exécuté.")
        root.after(100,poll)
    ttk.Button(nav,text="Centre de connaissances",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.research_ui"])).pack(fill="x",pady=10)
    ttk.Button(nav,text="Laboratoire simulation",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.simulation_ui"])).pack(fill="x")
    def close():
        pool.shutdown(wait=False,cancel_futures=True);root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    if profiles:pick(next(iter(profiles)))
    root.mainloop()

if __name__=="__main__":main()
