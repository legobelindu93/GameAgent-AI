"""Fetch public RSS headline metadata; no inferred event dates."""
from urllib.request import urlopen,Request
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from datetime import datetime,timezone
import json
from .bd2_data import STATE

FEED="https://dotgg.gg/brown-dust-2/news/feed/"
def sync():
    with urlopen(Request(FEED,headers={"User-Agent":"GameAgent/0.11 (RSS reader)"}),timeout=20) as r:
        if urlsplit(r.geturl()).hostname!="dotgg.gg":raise ValueError("Unexpected feed host")
        raw=r.read(2_000_001)
    if len(raw)>2_000_000 or b"<!DOCTYPE" in raw.upper():raise ValueError("Invalid feed")
    tree=ET.fromstring(raw)
    rows=[]
    for item in tree.findall("./channel/item")[:50]:
        title=item.findtext("title","").strip();url=item.findtext("link","").strip()
        if title and urlsplit(url).hostname=="dotgg.gg":
            rows.append({"title":title,"url":url,"published":item.findtext("pubDate",""),"event_end":None})
    if not rows:raise ValueError("No RSS items; check source manually")
    result={"fetched":datetime.now(timezone.utc).isoformat(),"items":rows}
    STATE.mkdir(parents=True,exist_ok=True)
    (STATE/"news.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result
