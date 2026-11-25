import tkinter as tk
from tkinter import ttk,messagebox
from concurrent.futures import ThreadPoolExecutor
from .theme import apply,console
from .bd2_expert import Account,plan,ask,seed

def main():
    root=tk.Tk();root.title("Brown Dust 2 | Expert F2P");root.geometry("1050x800");apply(root)
    panel=ttk.Frame(root,padding=20);panel.pack(fill="both",expand=True)
    ttk.Label(panel,text="Expert Brown Dust 2",style="Title.TLabel").pack(anchor="w")
    ttk.Label(panel,text="Conseiller stratégique — aucun contrôle du jeu ni achat automatique.",style="Muted.TLabel").pack(anchor="w",pady=6)
    form=ttk.Frame(panel);form.pack(fill="x")
    fields={}
    for i,(key,label,default,options) in enumerate([
        ("stage","Progression","beginner",["beginner","midgame","endgame"]),
        ("damage","Équipe","unknown",["physical","magic","unknown"]),
        ("bottleneck","Blocage","unknown",["gear","gold","level","combat","unknown"]),
        ("goal","Objectif","story",["story","resources","boss","general"]),
        ("minutes","Minutes","30",None),("diamonds","Diamants","0",None),("tickets","Tickets","0",None),
        ("costumes","Costumes (+niveau)","",None)]):
        row,col=divmod(i,2);box=ttk.Frame(form);box.grid(row=row,column=col,sticky="ew",padx=4,pady=4)
        ttk.Label(box,text=label).pack(anchor="w")
        v=tk.StringVar(value=default);fields[key]=v
        if options:ttk.Combobox(box,textvariable=v,values=options,state="readonly").pack(fill="x")
        else:ttk.Entry(box,textvariable=v).pack(fill="x")
    form.columnconfigure(0,weight=1);form.columnconfigure(1,weight=1)
    def account():
        d={k:v.get() for k,v in fields.items()}
        for k in ("minutes","diamonds","tickets"):d[k]=int(d[k])
        return Account(**d)
    question=tk.StringVar(value="Quelle progression privilégier avec ce compte ?")
    model=tk.StringVar(value="qwen2.5:3b")
    ttk.Label(panel,text="Question").pack(anchor="w")
    ttk.Entry(panel,textvariable=question).pack(fill="x")
    ttk.Label(panel,text="Modèle Ollama local").pack(anchor="w")
    ttk.Entry(panel,textvariable=model).pack(fill="x")
    bar=ttk.Frame(panel);bar.pack(fill="x",pady=8)
    pool=ThreadPoolExecutor(max_workers=1)
    def show(s):
        out.delete("1.0","end");out.insert("end",s)
    def planning():
        try:
            a=account();count=seed()
            show("Plan heuristique F2P — aucune garantie d'optimalité.\n"+f"{count} nouveaux extraits indexés.\n\n"+"\n\n".join(("À faire" if t["fits_budget"] else "Reporter")+" | "+str(t["minutes"])+" min | "+t["title"]+"\n"+t["reason"] for t in plan(a)))
        except Exception as exc:messagebox.showerror("Expert",str(exc))
    def query():
        try:a=account()
        except Exception as exc:messagebox.showerror("Compte",str(exc));return
        q,m=question.get(),model.get()
        button.configure(state="disabled");show("Analyse locale…")
        future=pool.submit(ask,a,q,m)
        def poll():
            if not future.done():root.after(150,poll);return
            button.configure(state="normal")
            try:
                r=future.result();show(r["answer"]+"\n\nSources :\n"+"\n".join(f"[{s['id']}] {s['source']} — {s['patch']}" for s in r["sources"]))
            except Exception as exc:show("Erreur Ollama : "+str(exc)+"\nLe plan hors ligne reste disponible.")
        root.after(150,poll)
    ttk.Button(bar,text="Plan de progression F2P",command=planning,style="Accent.TButton").pack(side="left")
    button=ttk.Button(bar,text="Interroger l’IA locale",command=query);button.pack(side="left",padx=8)
    out=console(panel)
    root.protocol("WM_DELETE_WINDOW",lambda:(pool.shutdown(wait=False,cancel_futures=True),root.destroy()))
    root.mainloop()

if __name__=="__main__":main()
