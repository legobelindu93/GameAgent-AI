"""Read-only OCR of explicit screenshots and local MFABD2 diagnostics."""
import re
from pathlib import Path
from .native import load

def screenshot(path):
    from rapidocr import RapidOCR
    from PIL import Image
    import numpy as np
    with Image.open(path) as img:
        if img.width*img.height>20_000_000:raise ValueError("Image too large")
        rgb=np.asarray(img.convert("RGB"))
    output=RapidOCR()(rgb)
    texts=getattr(output,"txts",None)
    scores=getattr(output,"scores",None)
    rows=[{"text":str(t),"confidence":float(s)} for t,s in zip(texts or [],scores if scores is not None else [])]
    return rows

def resource_candidates(rows):
    """Only explicit label/value lines; never silently overwrite account."""
    result={}
    labels={"diamonds":r"(?:diamonds?|diamants?|dia)","tickets":r"(?:draw tickets?|tickets?)","gold":r"(?:gold|or)"}
    for row in rows:
        if row["confidence"]<0.85:continue
        for key,pattern in labels.items():
            m=re.fullmatch(pattern+r"\s*[:：]?\s*(\d[\d ,.]*)",row["text"].strip(),re.I)
            if m:
                raw=m.group(1).replace(" ","").replace(",","").replace(".","")
                if raw.isdigit():result[key]=int(raw)
    return result

def mfabd2_status():
    exe=load("brown_dust_2").get("executable")
    if not exe:return {"configured":False,"logs":[]}
    p=Path(exe)
    if not p.is_file():return {"configured":False,"logs":[]}
    logs=[]
    for name in ("log","logs","debug"):
        folder=p.parent/name
        if not folder.is_dir():continue
        for f in folder.glob("*.log"):
            if f.is_file() and f.resolve().is_relative_to(p.parent.resolve()):logs.append(f)
    logs=sorted(logs,key=lambda f:f.stat().st_mtime,reverse=True)[:3]
    rows=[]
    for f in logs:
        with f.open("rb") as stream:
            stream.seek(max(0,f.stat().st_size-16000))
            rows.append({"file":f.name,"tail":stream.read(16000).decode("utf-8",errors="replace")})
    return {"configured":True,"executable":str(p),"logs":rows,"connection":"unknown; no verified status API"}
