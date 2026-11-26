"""Original procedural landscape covers, no downloads or publisher artwork."""
from functools import lru_cache
import random, math
from PIL import Image,ImageDraw,ImageFilter
from .game_data import identity,artwork

@lru_cache(maxsize=24)
def cover(game,w=640,h=280):
    w=max(32,min(1600,int(w)));h=max(32,min(900,int(h)))
    from PIL import ImageOps
    path=artwork(game,"banner")
    if path:
        try:
            with Image.open(path) as src:
                return ImageOps.fit(src.convert("RGB"),(w,h))
        except (OSError,ValueError):pass
    rng=random.Random(game)
    hexcolor=identity(game)["accent"]
    accent=tuple(int(hexcolor[i:i+2],16) for i in (1,3,5))
    im=Image.new("RGB",(w,h));d=ImageDraw.Draw(im)
    for y in range(h):
        f=y/h
        color=tuple(int(10+(c*.34)*math.sin(f*math.pi)+c*.08*(1-f)) for c in accent)
        d.line((0,y,w,y),fill=color)
    glow=Image.new("RGB",(w,h));g=ImageDraw.Draw(glow)
    r=int(h*.33);cx=int(w*.72);cy=int(h*.38)
    g.ellipse((cx-r,cy-r,cx+r,cy+r),fill=accent)
    glow=glow.filter(ImageFilter.GaussianBlur(max(8,h//10)))
    from PIL import ImageChops
    im=ImageChops.screen(im,glow);d=ImageDraw.Draw(im)
    for _ in range(75):
        x=rng.randrange(w);y=rng.randrange(max(1,int(h*.65)))
        c=tuple(int(a*.35+40) for a in accent)
        d.point((x,y),fill=c)
    for j in range(3):
        base=h*(.68+j*.14)
        color=tuple(int(10+a*(.23-j*.065)) for a in accent)
        pts=[(0,h)]
        for x in range(0,w+max(8,w//14),max(8,w//14)):
            pts.append((x,int(base-rng.uniform(0,h*.22))))
        pts.extend([(w,h)])
        d.polygon(pts,fill=color)
    if game in {"nikke","neverness_to_everness","honkai_star_rail"}:
        for i in range(16):
            x=int(w*.35+i*w*.045);bw=max(5,int(w*.025));top=int(h*rng.uniform(.36,.79))
            d.rectangle((x,top,x+bw,h),fill=(14,16,24))
            for yy in range(top+7,h-8,12):
                if rng.random()>.35:d.line((x+3,yy,x+bw-2,yy),fill=tuple(int(a*.45) for a in accent))
    else:
        for i in range(3):
            x=int(w*(.58+i*.12));top=int(h*(.33+i*.09));bw=max(5,int(w*.025))
            d.polygon([(x-bw,top+18),(x,top-12),(x+bw,top+18),(x+bw,h),(x-bw,h)],fill=(16,18,26))
    return im
