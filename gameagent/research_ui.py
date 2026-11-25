"""Independent desktop knowledge panel. Slow operations run outside the GUI thread."""
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import json
from .profiles import load_profiles
from .catalog import Catalog
from .knowledge import Knowledge
from .theme import apply,console,sidebar

def main():
    root=tk.Tk()
    root.title("GameAgent | Knowledge Center")
    root.geometry("1220x780")
    root.minsize(850,520)
    apply(root)
    profiles=load_profiles()
    game=tk.StringVar(value=next(iter(profiles)))
    query=tk.StringVar()
    patch=tk.StringVar()
    nav,pick=sidebar(root,profiles,lambda key:select_game(key))
    panel=ttk.Frame(root,padding=28);panel.pack(side="right",fill="both",expand=True)
    ttk.Label(panel,text="RECHERCHE  /  IA LOCALE",style="Eyebrow.TLabel").pack(anchor="w")
    heading=ttk.Label(panel,text="Centre de connaissances",style="Title.TLabel");heading.pack(anchor="w",pady=8)
    top=ttk.Frame(panel);top.pack(fill="x",pady=(8,12))
    ttk.Label(top,text="Question ou personnage",style="Muted.TLabel").pack(anchor="w")
    ttk.Entry(top,textvariable=query).pack(fill="x",pady=(4,10))
    ttk.Label(top,text="Version du jeu (facultatif)",style="Muted.TLabel").pack(anchor="w")
    ttk.Entry(top,textvariable=patch).pack(fill="x",pady=4)
    out=console(panel)
    def select_game(key):
        game.set(key)
        heading.configure(text=profiles[key]["name"]+" / Connaissances")
        out.delete("1.0","end")
        out.insert("end","Sélectionnez une recherche pour ce jeu.")
    pool=ThreadPoolExecutor(max_workers=1)
    busy=False
    def worker(mode,g,q,p):
        if mode=="ask":
            from .advisor import advise
            return advise(g,q,patch=p)
        db=Catalog(g) if mode=="catalog" else Knowledge(g)
        try:return db.search(q,patch=p)
        finally:db.close()
    def run(mode):
        nonlocal busy
        if busy:return
        busy=True
        g,q,p=game.get(),query.get(),patch.get() or None
        out.delete("1.0","end");out.insert("end","Processing "+g)
        f=pool.submit(worker,mode,g,q,p)
        def poll():
            nonlocal busy
            if not f.done():root.after(100,poll);return
            busy=False
            try:text=json.dumps(f.result(),ensure_ascii=False,indent=2)
            except Exception as exc:text=str(exc)
            if game.get()==g:
                out.delete("1.0","end");out.insert("end",text)
        root.after(100,poll)
    for label,mode in [("Guides","guides"),("Personnages / builds","catalog"),("Interroger l’IA","ask")]:
        ttk.Button(top,text=label,command=lambda m=mode:run(m),style="Accent.TButton" if mode=="ask" else "TButton").pack(side="left",padx=4,pady=8)
    def close():
        pool.shutdown(wait=False,cancel_futures=True);root.destroy()
    pick(game.get())
    root.protocol("WM_DELETE_WINDOW",close)
    root.mainloop()

if __name__=="__main__":main()
