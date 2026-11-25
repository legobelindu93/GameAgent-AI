"""Game-first desktop launcher with explicit release selection and native interface registration."""
import tkinter as tk
from tkinter import ttk,filedialog,messagebox,simpledialog
from concurrent.futures import ThreadPoolExecutor
import subprocess,sys,webbrowser
from .profiles import load_profiles
from .theme import apply,sidebar,console
from .project_hub import project,inspect,open_folder
from .installations import releases,download
from . import native,dependencies
from .window_host import WindowHost
from .visuals import Banner
from .game_data import identity
from .bridges import describe,start_interface
from .task_catalog import inventory as task_inventory

def main():
    root=tk.Tk();root.title("GameAgent | Game Library");root.geometry("1360x850");root.minsize(1050,720);apply(root)
    profiles=load_profiles()
    selected=None
    assets=[]
    generation=0
    pool=ThreadPoolExecutor(max_workers=2)
    processes={}
    nav,pick=sidebar(root,profiles,lambda k:select(k))
    panel=ttk.Frame(root,padding=28);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="BIBLIOTHÈQUE / APPLICATIONS",style="Eyebrow.TLabel").pack(anchor="w")
    banner=Banner(panel);banner.pack(fill="x",pady=(10,8))
    status=ttk.Label(panel,style="Muted.TLabel");status.pack(anchor="w",pady=12)
    tabs=ttk.Notebook(panel);tabs.pack(fill="both",expand=True)
    home,install,details,embedded=[ttk.Frame(tabs,padding=18) for _ in range(4)]
    for page,label in [(home,"Vue d’ensemble"),(install,"Installation"),(embedded,"Interface originale"),(details,"Diagnostic")]:tabs.add(page,text=label)
    log=console(details)
    host_frame=tk.Frame(embedded,bg="#10131c")
    host=WindowHost(host_frame)
    host_status=ttk.Label(embedded,text="Ouvrez une application, puis sélectionnez sa fenêtre.")
    host_status.pack(anchor="w",pady=4)
    host_controls=ttk.Frame(embedded);host_controls.pack(fill="x")
    host_frame.pack(fill="both",expand=True,pady=8)
    def detach():
        try:host.detach();host_status.configure(text="Fenêtre détachée")
        except Exception as exc:messagebox.showerror("Fenêtre",str(exc))
    def attach():
        process=processes.get(selected)
        if process is None or process.poll() is not None:
            messagebox.showinfo("Interface","Lancez d’abord l’application depuis ce panel.");return
        try:
            windows=host.candidates(process.pid)
            if not windows:raise ValueError("Aucune fenêtre détectée pour ce processus. Les lanceurs qui créent un processus enfant restent en mode externe.")
            if len(windows)>1:
                choice=simpledialog.askinteger("Fenêtre","\n".join(f"{i+1}. {title}" for i,(_,title) in enumerate(windows)),minvalue=1,maxvalue=len(windows))
                if choice is None:return
            else:choice=1
            host.attach(windows[choice-1][0],process.pid)
            host_status.configure(text=windows[choice-1][1]+" — interface native")
        except Exception as exc:messagebox.showerror("Embarquement",str(exc))
    ttk.Button(host_controls,text="Embarquer la fenêtre",command=attach,style="Accent.TButton").pack(side="left")
    ttk.Button(host_controls,text="Détacher",command=detach).pack(side="left",padx=8)
    def write(text):
        log.insert("end",text+"\n");log.see("end")
    def refresh():
        settings=native.load(selected)
        from pathlib import Path
        exe=settings.get("executable","")
        info=describe(selected)
        ready=bool(exe and Path(exe).is_file()) or (info["entry_available"] and info["environment_available"])
        status.configure(text=("Application configurée" if ready else "Application à installer"))
        status_value.configure(text="Configurée" if ready else "Non configurée")
        launch_button.configure(state="normal" if ready else "disabled")
        path.configure(text=exe or "Aucun exécutable sélectionné")
    def select(key):
        nonlocal selected,generation,assets
        detach()
        selected=key;generation+=1;assets=[]
        meta=project(key)
        banner.show_game(key,profiles[key]["name"],meta["name"]+"  /  "+meta["interface"])
        engine_value.configure(text=meta["name"])
        interface_value.configure(text=meta["interface"])
        for child in features.winfo_children():child.destroy()
        for i,label in enumerate(identity(key)["features"]):
            tile=ttk.Frame(features,style="Card.TFrame",padding=12)
            tile.grid(row=i//2,column=i%2,sticky="nsew",padx=4,pady=4)
            ttk.Label(tile,text=label,style="Card.TLabel").pack(anchor="w")
            ttk.Label(tile,text="Dans le projet original",style="MetricCaption.TLabel").pack(anchor="w",pady=(4,0))
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
        try:processes[key]=start_interface(key);write("Application ouverte : "+key)
        except Exception as exc:messagebox.showerror("Application",str(exc))
    def web():
        if not native.load(selected).get("web_url"):web_config()
        if native.load(selected).get("web_url"):subprocess.Popen([sys.executable,"-m","gameagent.native",selected])
    cards=ttk.Frame(home);cards.pack(fill="x",pady=(0,14))
    def metric(label):
        card=ttk.Frame(cards,style="Card.TFrame",padding=13);card.pack(side="left",fill="both",expand=True,padx=(0,8))
        ttk.Label(card,text=label,style="MetricCaption.TLabel").pack(anchor="w")
        value=ttk.Label(card,text="—",style="Card.TLabel",font=("Segoe UI",13,"bold"))
        value.pack(anchor="w",pady=(5,0))
        return value
    status_value=metric("INSTALLATION")
    engine_value=metric("PROJET")
    interface_value=metric("INTERFACE")
    actions=ttk.Frame(home);actions.pack(fill="x",pady=(0,12))
    launch_button=ttk.Button(actions,text="Ouvrir l’application",command=launch,style="Accent.TButton")
    launch_button.pack(side="left",padx=(0,8))
    ttk.Button(actions,text="Installer",command=lambda:tabs.select(install)).pack(side="left",padx=(0,8))
    ttk.Button(actions,text="Configurer",command=configure).pack(side="left",padx=(0,8))
    ttk.Button(actions,text="WebUI",command=web).pack(side="left",padx=(0,8))
    ttk.Button(actions,text="Adresse WebUI",command=web_config).pack(side="left")
    path=ttk.Label(home,wraplength=780,style="Muted.TLabel");path.pack(anchor="w",pady=(0,12))
    ttk.Label(home,text="Catégories du projet original",font=("Segoe UI",14,"bold")).pack(anchor="w")
    ttk.Label(home,text="Repères informatifs — les commandes se trouvent dans l’interface originale.",style="Muted.TLabel").pack(anchor="w",pady=(3,8))
    features=ttk.Frame(home);features.pack(fill="x")
    features.columnconfigure(0,weight=1);features.columnconfigure(1,weight=1)
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
    def provision():
        key=selected
        if key in {"genshin_impact","brown_dust_2"}:
            if not messagebox.askyesno("Dépendances","Installer .NET Desktop 10 et VC++ x64 via winget ?"):return
            fn=lambda:dependencies.install_runtime(key)
        else:
            version=simpledialog.askstring("Python","Version Python requise par le dépôt (consultez sa documentation)",initialvalue="3.12")
            if not version:return
            if not messagebox.askyesno("Dépendances","Installer les requirements.txt du dépôt local dans un environnement isolé ? Vérifiez les sources avant de continuer."):return
            fn=lambda:dependencies.install_python(key,version)
        release_status.configure(text="Installation des dépendances…")
        async_job(fn,lambda result:(release_status.configure(text="Commande terminée"),write(result)))
    ttk.Button(install,text="Installer les dépendances",command=provision).pack(anchor="w",pady=4)
    ttk.Label(install,text="Après téléchargement, suivez les instructions du projet pour installer ou extraire son application, puis sélectionnez son exécutable dans Application.",wraplength=750,style="Muted.TLabel").pack(anchor="w",pady=10)
    def show_inventory():
        key=selected
        def display(rows):
            write("Inventaire des composants originaux : "+str(len(rows)))
            for row in rows:write(row["name"]+" | "+row["source"]+" | "+row["kind"])
            tabs.select(details)
        async_job(lambda:task_inventory(key),display)
    ttk.Button(home,text="Inventorier les composants réels",command=show_inventory).pack(anchor="w",pady=8)
    def diagnostic():
        key=selected
        write(str(dependencies.diagnostic(key)))
        write(str(describe(key)))
        async_job(lambda:inspect(key),lambda r:write("Révision : "+str(r["revision"])+"\nFichiers locaux : "+str(len(r["files"]))+"\nLicences : "+str(r["licenses"])))
    ttk.Button(details,text="Analyser les sources locales",command=diagnostic).pack(anchor="w")
    ttk.Button(nav,text="Expert Brown Dust 2",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.bd2_expert_ui"])).pack(fill="x",pady=4)
    ttk.Button(nav,text="Centre de connaissances",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.research_ui"])).pack(fill="x",pady=12)
    ttk.Button(nav,text="Explorateur de sources",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.hub_ui"])).pack(fill="x")
    def close():
        try:host.detach()
        except Exception as exc:
            messagebox.showerror("Interface",str(exc));return
        pool.shutdown(wait=False,cancel_futures=True);root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    if profiles:pick(next(iter(profiles)))
    root.mainloop()

if __name__=="__main__":main()
