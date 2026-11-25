import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from uuid import uuid4
from .profiles import load_profiles
from .engine import State, Action, step
from .planner import plan, legal
from .memory import Memory
from .imitation import Imitation

def main():
    root=tk.Tk()
    root.title("GameAgent AI | Research Studio")
    root.geometry("1050x680")
    root.minsize(850,520)
    profiles=load_profiles()
    sidebar=ttk.Frame(root,padding=16)
    sidebar.pack(side="left",fill="y")
    ttk.Label(sidebar,text="GAMEAGENT AI",font=("Segoe UI",16,"bold")).pack(pady=12)
    panel=ttk.Frame(root,padding=20)
    panel.pack(side="right",fill="both",expand=True)
    title=ttk.Label(panel,text="Select a game",font=("Segoe UI",24))
    title.pack(anchor="w")
    info=ttk.Label(panel,wraplength=650)
    info.pack(anchor="w",pady=8)
    tabs=ttk.Notebook(panel)
    tabs.pack(fill="both",expand=True)
    sim,vision,logs=ttk.Frame(tabs,padding=12),ttk.Frame(tabs,padding=12),ttk.Frame(tabs,padding=12)
    for page,label in [(sim,"Simulation / AI"),(vision,"Offline vision"),(logs,"History")]:
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
    ttk.Label(sim,textvariable=status,font=("Segoe UI",14)).pack(anchor="w",pady=8)
    ttk.Combobox(sim,textvariable=style,values=["careful","balanced","aggressive"],state="readonly").pack(anchor="w")
    trace=tk.Text(logs,state="disabled")
    trace.pack(fill="both",expand=True)
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
        status.set(f"Turn {state.turn} | HP {state.hp} | Enemy {state.enemy} | Potions {state.potions}")
    def select(key):
        nonlocal selected,state,memory,session,imitation
        stop()
        if memory:
            memory.close()
        selected,state,session,imitation=key,State(),uuid4().hex,Imitation()
        memory=Memory("data",key)
        title.configure(text=profiles[key]["name"])
        info.configure(text="Synthetic research profile — "+", ".join(profiles[key]["targets"]))
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
    for label,fn in [("Plan one turn",act),("Run simulation",start),("Stop",stop),("Reset",lambda:select(selected) if selected else None),("Imitate demonstration",imitate)]:
        ttk.Button(sim,text=label,command=fn).pack(anchor="w",pady=3)
    ttk.Label(sim,text="Demonstrate an action:").pack(anchor="w",pady=6)
    for a in Action:
        ttk.Button(sim,text=a.value,command=lambda a=a:act(a,True)).pack(anchor="w")
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
    ttk.Button(vision,text="Match template in saved screenshot",command=analyze).pack(anchor="w")
    for key,p in profiles.items():
        ttk.Button(sidebar,text=p["name"],command=lambda k=key:select(k)).pack(fill="x",pady=4)
    def close():
        stop()
        if memory:memory.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    root.mainloop()

if __name__=="__main__":
    main()
