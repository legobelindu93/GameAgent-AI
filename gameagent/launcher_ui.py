"""Game-first desktop launcher with explicit release selection and native interface registration."""
import tkinter as tk
from tkinter import ttk,filedialog,messagebox,simpledialog
from concurrent.futures import ThreadPoolExecutor
import subprocess,sys,webbrowser
from .profiles import load_profiles
from .theme import apply,sidebar,console
from .project_hub import project,inspect,open_folder
from .installations import releases,download
from . import native

def main():
    root=tk.Tk();root.title("GameAgent | Game Library");root.geometry("1280x800");root.minsize(950,600);apply(root)
    profiles=load_profiles()
    selected=None
    assets=[]
    generation=0
    pool=ThreadPoolExecutor(max_workers=2)
    processes={}
    nav,pick=sidebar(root,profiles,lambda k:select(k))
    panel=ttk.Frame(root,padding=28);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="BIBLIOTHÈQUE / APPLICATIONS",style="Eyebrow.TLabel").pack(anchor="w")
    title=ttk.Label(panel,style="Title.TLabel");title.pack(anchor="w",pady=8)
    subtitle=ttk.Label(panel,style="Muted.TLabel");subtitle.pack(anchor="w")
    status=ttk.Label(panel,style="Muted.TLabel");status.pack(anchor="w",pady=12)
    tabs=ttk.Notebook(panel);tabs.pack(fill="both",expand=True)
    home,install,details=[ttk.Frame(tabs,padding=18) for _ in range(3)]
    for page,label in [(home,"Application"),(install,"Installation"),(details,"Diagnostic")]:tabs.add(page,text=label)
    log=console(details)
    def write(text):
        log.insert("end",text+"\n");log.see("end")
    def refresh():
        settings=native.load(selected)
        from pathlib import Path
        exe=settings.get("executable","")
        status.configure(text=("Application configurée" if exe and Path(exe).is_file() else "Installation ou sélection de l’exécutable nécessaire"))
        path.configure(text=exe or "Aucun exécutable sélectionné")
    def select(key):
        nonlocal selected,generation,assets
        selected=key;generation+=1;assets=[]
        meta=project(key)
        title.configure(text=profiles[key]["name"]);subtitle.configure(text=meta["name"]+"  /  "+meta["interface"])
        listing.delete(0,"end");release_status.configure(text="Sélectionnez Rechercher les versions.")
        log.delete("1.0","end")
        refresh()
    def configure():
        key=selected
        exe=filedialog.askopenfilename(title="Sélectionner l’application originale installée",filetypes=[("Windows executable","*.exe")])
        if not exe:return
        try:native.save(key,exe,native.load(key).get("web_url",""));refresh()
        except Exception as exc:messagebox.showerror("Configuration",str(exc))
    def web_config():
        key=selected
        url=simpledialog.askstring("WebUI","Adresse HTTP locale et port",initialvalue=native.load(key).get("web_url",""))
        if url is None:return
        try:native.save(key,native.load(key).get("executable",""),url)
        except Exception as exc:messagebox.showerror("WebUI",str(exc))
    def launch():
        key=selected
        if key in processes and processes[key].poll() is None:
            messagebox.showinfo("Application","Une instance lancée par GameAgent est déjà ouverte.");return
        try:processes[key]=native.launch(key);write("Application ouverte : "+key)
        except Exception as exc:messagebox.showerror("Application",str(exc))
    def web():
        if not native.load(selected).get("web_url"):web_config()
        if native.load(selected).get("web_url"):subprocess.Popen([sys.executable,"-m","gameagent.native",selected])
    ttk.Label(home,text="Interface originale",style="Title.TLabel").pack(anchor="w")
    ttk.Label(home,text="Conservez les fonctionnalités et les paramètres du programme tiers.",style="Muted.TLabel").pack(anchor="w",pady=10)
    path=ttk.Label(home,wraplength=700);path.pack(anchor="w",pady=10)
    for label,fn,style in [("Ouvrir l’application",launch,"Accent.TButton"),("Sélectionner l’exécutable installé",configure,"TButton"),("Configurer WebUI",web_config,"TButton"),("Afficher WebUI locale",web,"TButton")]:
        ttk.Button(home,text=label,command=fn,style=style).pack(anchor="w",pady=4)
    ttk.Label(home,text="Les activités restent gérées par l’interface originale. Utilisation dans les environnements autorisés uniquement.",wraplength=700,style="Muted.TLabel").pack(anchor="w",pady=20)
    def async_job(fn,done):
        token=generation
        future=pool.submit(fn)
        def poll():
            if not future.done():root.after(150,poll);return
            if token!=generation:return
            try:done(future.result())
            except Exception as exc:messagebox.showerror("GameAgent",str(exc))
        root.after(150,poll)
    def search():
        key=selected
        release_status.configure(text="Recherche GitHub…")
        def done(result):
            nonlocal assets
            assets=result["assets"];listing.delete(0,"end")
            for asset in assets:listing.insert("end",asset["name"]+"  |  "+str(round(asset["size"]/1048576,1))+" Mo")
            release_status.configure(text=result["tag"]+" — "+str(len(assets))+" fichiers Windows ou archives")
        async_job(lambda:releases(key),done)
    def fetch():
        choice=listing.curselection()
        if not choice:return
        asset=assets[choice[0]];key=selected
        if not messagebox.askyesno("Téléchargement","Télécharger "+asset["name"]+" depuis GitHub ? Aucun fichier ne sera exécuté."):return
        release_status.configure(text="Téléchargement en cours…")
        def done(r):
            release_status.configure(text="Téléchargé : "+r["path"]);write(str(r))
        async_job(lambda:download(key,asset),done)
    ttk.Button(install,text="Rechercher les versions",command=search,style="Accent.TButton").pack(anchor="w")
    release_status=ttk.Label(install,wraplength=750,style="Muted.TLabel");release_status.pack(anchor="w",pady=12)
    listing=tk.Listbox(install,bg="#191e2b",fg="#eef2ff",selectbackground="#7658e8",height=8);listing.pack(fill="x")
    ttk.Button(install,text="Télécharger le fichier sélectionné",command=fetch).pack(anchor="w",pady=8)
    ttk.Button(install,text="Instructions officielles",command=lambda:webbrowser.open(project(selected)["documentation"])).pack(anchor="w")
    ttk.Button(install,text="Toutes les versions GitHub",command=lambda:webbrowser.open(project(selected)["releases"])).pack(anchor="w",pady=4)
    ttk.Label(install,text="Après téléchargement, suivez les instructions du projet pour installer ou extraire son application, puis sélectionnez son exécutable dans Application.",wraplength=750,style="Muted.TLabel").pack(anchor="w",pady=10)
    def diagnostic():
        key=selected
        async_job(lambda:inspect(key),lambda r:write("Révision : "+str(r["revision"])+"\nFichiers locaux : "+str(len(r["files"]))+"\nLicences : "+str(r["licenses"])))
    ttk.Button(details,text="Analyser les sources locales",command=diagnostic).pack(anchor="w")
    ttk.Button(nav,text="Centre de connaissances",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.research_ui"])).pack(fill="x",pady=12)
    ttk.Button(nav,text="Explorateur de sources",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.hub_ui"])).pack(fill="x")
    def close():
        pool.shutdown(wait=False,cancel_futures=True);root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    if profiles:pick(next(iter(profiles)))
    root.mainloop()

if __name__=="__main__":main()
