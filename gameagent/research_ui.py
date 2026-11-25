"""Independent desktop knowledge panel. Slow operations run outside the GUI thread."""
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import json
from .profiles import load_profiles
from .catalog import Catalog
from .knowledge import Knowledge

def main():
    root=tk.Tk()
    root.title("GameAgent | Knowledge Center")
    root.geometry("1000x650")
    profiles=load_profiles()
    game=tk.StringVar(value=next(iter(profiles)))
    query=tk.StringVar()
    patch=tk.StringVar()
    top=ttk.Frame(root,padding=12);top.pack(fill="x")
    ttk.Combobox(top,textvariable=game,values=list(profiles),state="readonly").pack(fill="x")
    ttk.Label(top,text="Question or character").pack(anchor="w")
    ttk.Entry(top,textvariable=query).pack(fill="x")
    ttk.Label(top,text="Patch (optional)").pack(anchor="w")
    ttk.Entry(top,textvariable=patch).pack(fill="x")
    out=tk.Text(root,wrap="word");out.pack(fill="both",expand=True)
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
            out.delete("1.0","end");out.insert("end",text)
        root.after(100,poll)
    for label,mode in [("Search guides","guides"),("Search characters / builds","catalog"),("Ask local AI","ask")]:
        ttk.Button(top,text=label,command=lambda m=mode:run(m)).pack(side="left",padx=4,pady=8)
    def close():
        pool.shutdown(wait=False,cancel_futures=True);root.destroy()
    root.protocol("WM_DELETE_WINDOW",close)
    root.mainloop()

if __name__=="__main__":main()
