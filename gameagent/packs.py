"""Versioned, non-executable knowledge packs. No GPU or network required."""
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
from .profiles import ROOT,load_profiles
from .knowledge import Knowledge

PACKS=ROOT.parent/"knowledge_packs"
MAX_BYTES=8_000_000
CATEGORIES={"progression","economy","combat","characters","equipment","events","video","mechanics","teams"}
def now():
    return datetime.now(timezone.utc).isoformat()
def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()
def load_json(path):
    with Path(path).open("rb") as f:raw=f.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise ValueError("JSON too large")
    return json.loads(raw.decode("utf-8-sig"))
def game_check(game):
    if game not in load_profiles():raise ValueError("Unknown game")
def https_url(url):
    u=urlsplit(url)
    return u.scheme=="https" and bool(u.hostname) and not u.username and not u.password
def atomic(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    import tempfile,os
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix=".pack-")
    try:
        with os.fdopen(fd,"wb") as stream:stream.write(canonical(obj))
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def validate_record(r):
    if not isinstance(r,dict):raise ValueError("Expected object")
    if set(r)!={"id","category","title","claim","source","patch","review","locator"}:raise ValueError("Unexpected record fields")
    for k in r:
        if not isinstance(r[k],str) or not r[k].strip():raise ValueError("Missing "+k)
    if not re.fullmatch(r"[a-z0-9_-]{1,100}",r["id"]):raise ValueError("Invalid id")
    if r["category"] not in CATEGORIES or r["review"] not in {"candidate","approved"}:raise ValueError("Invalid status/category")
    if not https_url(r["source"]):raise ValueError("HTTPS source required")
    if len(r["claim"])>1200 or len(r["title"])>200 or len(r["locator"])>300 or len(r["source"])>2000 or len(r["patch"])>120:raise ValueError("Field too long")
def make(game,version,records):
    game_check(game)
    if not isinstance(version,str) or not re.fullmatch(r"\d+\.\d+\.\d+",version):raise ValueError("Expected semantic version")
    if not isinstance(records,list) or len(records)>3000:raise ValueError("Invalid records")
    ids=set()
    for r in records:
        validate_record(r)
        if r["id"] in ids:raise ValueError("Duplicate record id")
        ids.add(r["id"])
    payload={"schema":1,"game":game,"version":version,"records":records}
    return dict(payload,sha256=digest(payload))
def verify(pack,game=None):
    if not isinstance(pack,dict) or set(pack)!={"schema","game","version","records","sha256"} or pack["schema"]!=1:raise ValueError("Unsupported pack schema")
    if game and game!=pack["game"]:raise ValueError("Wrong game")
    expected=make(pack["game"],pack["version"],pack["records"])
    if expected["sha256"]!=pack["sha256"]:raise ValueError("Pack integrity mismatch")
    return pack
def install(path,game,root="data/knowledge",trusted=False):
    """Only explicit reviewed imports. Hash checks integrity, not authenticity."""
    pack=verify(load_json(path),game)
    if not trusted:raise ValueError("Review pack and explicitly confirm trusted import")
    db=Knowledge(game,root=root)
    count=0
    try:
        for r in pack["records"]:
            if r["review"]=="approved":
                count+=db.ingest(r["title"],r["claim"]+"\nSource locator: "+r["locator"],r["source"],r["patch"])
    finally:db.close()
    return {"game":game,"version":pack["version"],"indexed_chunks":count,"approved":sum(r["review"]=="approved" for r in pack["records"])}
def registry(game):
    game_check(game)
    return load_json(PACKS/"registry.json")[game]
def coverage(game,root="data/knowledge"):
    db=Knowledge(game,root=root)
    try:return {topic:len(db.search(topic,limit=8)) for topic in registry(game)["topics"]}
    finally:db.close()
def compare(records):
    """Surface conflicting claims with same category/title/patch; never resolve automatically."""
    groups={}
    for r in records:
        validate_record(r)
        key=(r["category"],r["title"].casefold().strip(),r["patch"])
        groups.setdefault(key,[]).append(r)
    return [{"topic":k[1],"patch":k[2],"claims":v} for k,v in groups.items() if len({r["claim"].casefold().strip() for r in v})>1]
