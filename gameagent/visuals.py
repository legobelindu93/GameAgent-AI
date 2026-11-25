"""Responsive original geometric banners with optional user-provided artwork."""
import tkinter as tk
from .game_data import identity,artwork

class Banner(tk.Canvas):
    def __init__(self,parent,**kw):
        super().__init__(parent,height=144,bg="#18202d",highlightthickness=0,**kw)
        self.game=None
        self.title=""
        self.subtitle=""
        self.photo=None
        self.bind("<Configure>",lambda _:self.draw())
    def show_game(self,game,title,subtitle):
        self.game,self.title,self.subtitle=game,title,subtitle
        self.draw()
    def draw(self):
        if not self.game:return
        self.delete("all")
        w,h=max(1,self.winfo_width()),max(1,self.winfo_height())
        data=identity(self.game);accent=data["accent"]
        self.create_rectangle(0,0,w,h,fill="#192333",outline="")
        self.photo=None
        path=artwork(self.game,"banner")
        if path:
            try:
                from PIL import Image,ImageOps,ImageTk
                with Image.open(path) as src:
                    image=ImageOps.fit(src.convert("RGB"),(w,h))
                    shade=Image.new("RGB",(w,h),"#10151f")
                    image=Image.blend(image,shade,0.58)
                    self.photo=ImageTk.PhotoImage(image)
                self.create_image(0,0,image=self.photo,anchor="nw")
            except (ImportError,OSError,ValueError):pass
        if self.photo is None:
            self.create_polygon(w*.61,0,w,0,w,h,w*.43,h,fill="#253346",outline="")
            self.create_polygon(w*.88,0,w,0,w*.72,h,w*.60,h,fill=accent,outline="")
            self.create_oval(w-180,-55,w+35,160,outline=accent,width=2)
            self.create_text(w-88,h/2,text=data["initials"],fill="#e7ecf5",font=("Segoe UI",36,"bold"))
        self.create_rectangle(0,0,5,h,fill=accent,outline="")
        self.create_text(24,25,text=data["genre"].upper(),fill="#c5d1e4",anchor="w",font=("Segoe UI",10))
        self.create_text(24,66,text=self.title,fill="#ffffff",anchor="w",font=("Segoe UI",27,"bold"))
        self.create_text(25,110,text=self.subtitle,fill="#d3dbea",anchor="w",font=("Segoe UI",11))
