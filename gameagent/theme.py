import tkinter as tk
from tkinter import ttk

BG="#10131c"
PANEL="#191e2b"
SURFACE="#22293a"
TEXT="#eef2ff"
MUTED="#a0abc3"
ACCENT="#7658e8"
GREEN="#45d6ad"

def apply(root):
    root.configure(bg=BG)
    root.option_add("*Font", "SegoeUI 10")
    s=ttk.Style(root)
    s.theme_use("clam")
    s.configure(".",background=BG,foreground=TEXT,font=("Segoe UI",10))
    s.configure("TFrame",background=BG)
    s.configure("Card.TFrame",background=PANEL)
    s.configure("TLabel",background=BG,foreground=TEXT)
    s.configure("Card.TLabel",background=PANEL,foreground=TEXT)
    s.configure("Muted.TLabel",foreground=MUTED)
    s.configure("Eyebrow.TLabel",foreground=GREEN,font=("Segoe UI",9,"bold"))
    s.configure("Title.TLabel",font=("Segoe UI",25,"bold"))
    s.configure("Metric.TLabel",background=PANEL,foreground=TEXT,font=("Segoe UI",24,"bold"))
    s.configure("MetricCaption.TLabel",background=PANEL,foreground=MUTED,font=("Segoe UI",10))
    s.configure("TButton",background=SURFACE,foreground=TEXT,borderwidth=0,padding=(14,10))
    s.map("TButton",background=[("disabled",PANEL),("active","#343e55")],foreground=[("disabled",MUTED)])
    s.configure("Accent.TButton",background=ACCENT,foreground="#ffffff")
    s.map("Accent.TButton",background=[("active","#896ef4"),("disabled",PANEL)])
    s.configure("Nav.TButton",anchor="w",padding=(14,12),background=PANEL)
    s.configure("Selected.Nav.TButton",anchor="w",padding=(14,12),background=ACCENT)
    s.configure("TNotebook",background=BG,borderwidth=0)
    s.configure("TNotebook.Tab",background=PANEL,foreground=MUTED,padding=(20,11),borderwidth=0)
    s.map("TNotebook.Tab",background=[("selected",SURFACE)],foreground=[("selected",TEXT)])
    s.configure("TEntry",fieldbackground=SURFACE,foreground=TEXT,insertcolor=TEXT,padding=8)
    s.configure("TCombobox",fieldbackground=SURFACE,foreground=TEXT,arrowcolor=TEXT,padding=7)
    s.map("TCombobox",fieldbackground=[("readonly",SURFACE)],foreground=[("readonly",TEXT)])
    root.option_add("*TCombobox*Listbox.background",SURFACE)
    root.option_add("*TCombobox*Listbox.foreground",TEXT)

def console(parent):
    frame=ttk.Frame(parent,style="Card.TFrame")
    text=tk.Text(frame,bg=PANEL,fg=TEXT,insertbackground=TEXT,selectbackground=ACCENT,
                 relief="flat",borderwidth=0,padx=16,pady=16,font=("Consolas",10),wrap="word")
    bar=ttk.Scrollbar(frame,command=text.yview)
    text.configure(yscrollcommand=bar.set)
    bar.pack(side="right",fill="y")
    text.pack(fill="both",expand=True)
    frame.pack(fill="both",expand=True)
    return text

def sidebar(parent,profiles,on_select):
    frame=ttk.Frame(parent,padding=18,style="Card.TFrame",width=245)
    frame.pack(side="left",fill="y")
    frame.pack_propagate(False)
    ttk.Label(frame,text="GAMEAGENT",style="Card.TLabel",font=("Segoe UI",19,"bold")).pack(anchor="w")
    ttk.Label(frame,text="AI  /  RESEARCH STUDIO",style="MetricCaption.TLabel").pack(anchor="w",pady=(0,28))
    ttk.Label(frame,text="BIBLIOTHÈQUE",style="MetricCaption.TLabel").pack(anchor="w",pady=(0,8))
    buttons={}
    def select(key):
        for k,b in buttons.items():b.configure(style="Selected.Nav.TButton" if k==key else "Nav.TButton")
        on_select(key)
    for key,p in profiles.items():
        b=ttk.Button(frame,text=p["name"],style="Nav.TButton",command=lambda k=key:select(k))
        b.pack(fill="x",pady=3)
        buttons[key]=b
    ttk.Label(frame,text="LOCAL  /  SIMULATION",style="MetricCaption.TLabel").pack(side="bottom",anchor="w")
    return frame,select
