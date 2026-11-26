import tkinter as tk
from tkinter import ttk

BG="#0a0b0e"
PANEL="#15171d"
SURFACE="#1b1e25"
TEXT="#f5f5f7"
MUTED="#969ca8"
ACCENT="#c5f36b"
GREEN="#64dbaf"

def apply(root):
    root.configure(bg=BG)
    from tkinter import font
    for name in ("TkDefaultFont","TkTextFont","TkMenuFont","TkHeadingFont"):
        font.nametofont(name,root=root).configure(family="Segoe UI",size=11)
    root.option_add("*Font", "{Segoe UI} 11")
    s=ttk.Style(root)
    s.theme_use("clam")
    s.configure(".",background=BG,foreground=TEXT,font=("Segoe UI",10))
    s.configure("TFrame",background=BG)
    s.configure("Card.TFrame",background=PANEL)
    s.configure("TLabel",background=BG,foreground=TEXT,font=("Segoe UI",11))
    s.configure("Card.TLabel",background=PANEL,foreground=TEXT)
    s.configure("Muted.TLabel",foreground=MUTED)
    s.configure("Eyebrow.TLabel",foreground=GREEN,font=("Segoe UI",9,"bold"))
    s.configure("Title.TLabel",font=("Segoe UI",25,"bold"))
    s.configure("Metric.TLabel",background=PANEL,foreground=TEXT,font=("Segoe UI",24,"bold"))
    s.configure("MetricCaption.TLabel",background=PANEL,foreground=MUTED,font=("Segoe UI",10))
    s.configure("TButton",background=SURFACE,foreground=TEXT,borderwidth=0,padding=(14,10))
    s.map("TButton",background=[("disabled",PANEL),("active","#292e35")],foreground=[("disabled",MUTED)])
    s.configure("Accent.TButton",background=ACCENT,foreground="#141a0d")
    s.map("Accent.TButton",background=[("active","#dcff99"),("disabled",PANEL)])
    s.configure("Nav.TButton",anchor="w",padding=(12,11),background=PANEL)
    s.map("Selected.Nav.TButton",background=[("active",ACCENT),("!disabled",ACCENT)])
    s.configure("Selected.Nav.TButton",anchor="w",padding=(14,12),background=ACCENT,foreground="#141a0d")
    s.configure("TNotebook",background=BG,borderwidth=0,tabmargins=(0,4,0,0),bordercolor=BG,lightcolor=BG,darkcolor=BG)
    s.configure("TNotebook.Tab",bordercolor=BG,lightcolor=BG,darkcolor=BG)
    s.configure("TNotebook.Tab",background=PANEL,foreground=MUTED,padding=(18,10),borderwidth=0)
    s.map("TNotebook.Tab",background=[("selected",SURFACE)],foreground=[("selected",TEXT)])
    s.configure("TEntry",fieldbackground=SURFACE,foreground=TEXT,insertcolor=TEXT,padding=8)
    s.configure("TCombobox",fieldbackground=SURFACE,foreground=TEXT,arrowcolor=TEXT,padding=7)
    s.map("TCombobox",fieldbackground=[("readonly",SURFACE)],foreground=[("readonly",TEXT)])
    root.option_add("*TCombobox*Listbox.background",SURFACE)
    root.option_add("*TCombobox*Listbox.foreground",TEXT)

def console(parent):
    frame=ttk.Frame(parent,style="Card.TFrame")
    ttk.Label(frame,text="RÉSULTATS  /  JOURNAL LOCAL",style="MetricCaption.TLabel",padding=(14,8)).pack(side="top",anchor="w")
    text=tk.Text(frame,bg=PANEL,fg=TEXT,insertbackground=TEXT,selectbackground=ACCENT,
                 relief="flat",borderwidth=0,padx=16,pady=16,font=("Consolas",10),wrap="word")
    bar=ttk.Scrollbar(frame,command=text.yview)
    text.configure(yscrollcommand=bar.set)
    bar.pack(side="right",fill="y")
    text.pack(fill="both",expand=True)
    frame.pack(fill="both",expand=True)
    return text

def sidebar(parent,profiles,on_select):
    frame=ttk.Frame(parent,padding=18,style="Card.TFrame",width=255)
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
    ttk.Label(frame,text="GAME LIBRARY  /  LOCAL",style="MetricCaption.TLabel").pack(side="bottom",anchor="w")
    return frame,select
