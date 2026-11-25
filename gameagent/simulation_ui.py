import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from uuid import uuid4
from .profiles import load_profiles
from .engine import State, Action, step
from .planner import plan, legal
from .memory import Memory
from .imitation import Imitation
from .theme import apply, console, sidebar as make_sidebar
from .scenarios import initial
import subprocess, sys

def main():
    root=tk.Tk()
    root.title("GameAgent AI | Research Studio")
    root.geometry("1220x780")
    apply(root)
    root.minsize(850,520)
    profiles=load_profiles()
    navigation=ttk.Frame(root)
    navigation.pack(side="left",fill="y")
    panel=ttk.Frame(root,padding=28)
    panel.pack(side="right",fill="both",expand=True)
    ttk.Label(panel,text="ESPACE DE TRAVAIL  /  SIMULATION",style="Eyebrow.TLabel").pack(anchor="w",pady=(0,8))
    title=ttk.Label(panel,text="Sélectionner un jeu",style="Title.TLabel")
    title.pack(anchor="w")
    info=ttk.Label(panel,wraplength=720,style="Muted.TLabel")
    info.pack(anchor="w",pady=8)
    tabs=ttk.Notebook(panel)
    tabs.pack(fill="both",expand=True)
    sim,vision,logs=ttk.Frame(tabs,padding=12),ttk.Frame(tabs,padding=12),ttk.Frame(tabs,padding=12)
    for page,label in [(sim,"Simulation / IA"),(vision,"Vision hors ligne"),(logs,"Journal")]:
        tabs.add(page,text=label)
    state=State()
    selected=None
    memory=None
    session=""
    imitation=Imitation()
    running=False
    pending=None
    style=tk.StringVar(value="balanced")
    status=tk.StringVar(value="No session")
    metrics=ttk.Frame(sim)
    metrics.pack(fill="x",pady=(8,20))
    values={}
    for name in ("TOUR","VIE","ENNEMI","POTIONS"):
        tile=ttk.Frame(metrics,style="Card.TFrame",padding=16)
        tile.pack(side="left",fill="x",expand=True,padx=(0,8))
        ttk.Label(tile,text=name,style="MetricCaption.TLabel").pack(anchor="w")
        values[name]=ttk.Label(tile,text="—",style="Metric.TLabel")
        values[name].pack(anchor="w")
    ttk.Label(sim,textvariable=status,style="Muted.TLabel").pack(anchor="w",pady=8)
    ttk.Label(sim,text="STRATÉGIE",style="Eyebrow.TLabel").pack(anchor="w",pady=(6,4))
    ttk.Combobox(sim,textvariable=style,values=["careful","balanced","aggressive"],state="readonly").pack(anchor="w")
    trace=console(logs)
    trace.configure(state="disabled")
    def log(msg):
        trace.configure(state="normal")
        trace.insert("end",msg+"\n")
        trace.see("end")
        trace.configure(state="disabled")
    def stop():
        nonlocal running,pending
        running=False
        if pending is not None:
            root.after_cancel(pending)
            pending=None
    def refresh():
        for name,v in zip(values,(state.turn,state.hp,state.enemy,state.potions)):
            values[name].configure(text=str(v))
        status.set("Simulation synthétique · aucune action envoyée au jeu")
    def select(key):
        nonlocal selected,state,memory,session,imitation
        stop()
        if memory:
            memory.close()
        selected,state,session,imitation=key,initial(key),uuid4().hex,Imitation()
        memory=Memory("data",key)
        title.configure(text=profiles[key]["name"])
        info.configure(text="Profil de recherche — "+", ".join(profiles[key]["targets"]))
        trace.configure(state="normal")
        trace.delete("1.0","end")
        trace.configure(state="disabled")
        log(f"Profile {key} | isolated session {session}")
        refresh()
    def act(action=None, demonstrate=False):
        nonlocal state
        if selected is None or not legal(state) or state.turn>=30:
            stop()
            return False
        if action is None:
            action,scores=plan(state,style.get())
            log(f"Scores: {scores}")
        if action not in legal(state):
            log("Action unavailable")
            return False
        if demonstrate:
            imitation.teach(state,action)
        new=step(state,action)
        memory.record(session,state,action,new)
        state=new
        log(f"{action.value}: HP {state.hp}, enemy {state.enemy}")
        refresh()
        return bool(legal(state) and state.turn<30)
    def cycle():
        nonlocal pending,running
        pending=None
        if running and act():
            pending=root.after(250,cycle)
        else:
            running=False
    def start():
        nonlocal running
        if not running and selected is not None:
            running=True
            cycle()
    def imitate():
        try:
            act(imitation.predict(state))
        except ValueError as exc:
            log(str(exc))
    controls=ttk.Frame(sim)
    controls.pack(fill="x",pady=16)
    for label,fn in [("Un tour",act),("Lancer la simulation",start),("Arrêter",stop),("Réinitialiser",lambda:select(selected) if selected else None)]:
        ttk.Button(controls,text=label,command=fn,style="Accent.TButton" if fn==start else "TButton").pack(side="left",padx=(0,6))
    ttk.Label(sim,text="APPRENTISSAGE PAR DÉMONSTRATION",style="Eyebrow.TLabel").pack(anchor="w",pady=(12,8))
    demos=ttk.Frame(sim)
    demos.pack(fill="x")
    for a in Action:
        ttk.Button(demos,text=a.value,command=lambda a=a:act(a,True)).pack(side="left",padx=(0,6))
    ttk.Button(demos,text="Imiter",command=imitate).pack(side="left")
    def analyze():
        image=filedialog.askopenfilename(title="Choose screenshot")
        if not image:return
        template=filedialog.askopenfilename(title="Choose template")
        if not template:return
        try:
            from .vision import match_template
            log(str(match_template(image,template)))
            tabs.select(logs)
        except (ImportError,ValueError) as exc:
            messagebox.showerror("Vision",str(exc))
    ttk.Label(vision,text="Analyser une capture",style="Title.TLabel").pack(anchor="w",pady=12)
    ttk.Label(vision,text="Comparer une image enregistrée avec un modèle visuel.",style="Muted.TLabel").pack(anchor="w",pady=8)
    ttk.Button(vision,text="Choisir les images",command=analyze,style="Accent.TButton").pack(anchor="w")
    nav,pick=make_sidebar(navigation,profiles,select)
    ttk.Button(nav,text="Centre de connaissances",command=lambda:subprocess.Popen([sys.executable,"-m","gameagent.research_ui"]),style="Accent.TButton").pack(fill="x",pady=20)
    if profiles:pick(next(iter(profiles)))
    def close():
        stop()
        if memory:memory.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    root.mainloop()

if __name__=="__main__":
    main()
