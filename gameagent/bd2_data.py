"""Local character catalog, account snapshots and user-authorized study imports."""
import json
from pathlib import Path
from datetime import datetime,timezone
from .profiles import ROOT
from .project_hub import BASE
from .catalog import Catalog
from .knowledge import Knowledge
from .video import transcribe

GAME="brown_dust_2"
STATE=BASE/"data"/"expert"/GAME

def seed_characters():
    return import_catalog(ROOT/GAME/"characters_seed.json")

def import_catalog(path):
    db=Catalog(GAME)
    try:return db.ingest(json.loads(Path(path).read_text(encoding="utf-8-sig")))
    finally:db.close()

def save_snapshot(fields):
    allowed={"diamonds","tickets","gold"}
    if not fields or any(k not in allowed or type(v)!=int or v<0 for k,v in fields.items()):raise ValueError("Confirm nonnegative integer resource fields")
    STATE.mkdir(parents=True,exist_ok=True)
    path=STATE/"account.json"
    old=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    old.setdefault("resources",{}).update(fields)
    old["updated"]=datetime.now(timezone.utc).isoformat()
    tmp=path.with_suffix(".tmp");tmp.write_text(json.dumps(old,indent=2),encoding="utf-8");tmp.replace(path)
    return old

def study_video(path,source,patch):
    if not source.strip() or not patch.strip():raise ValueError("Source and patch required")
    result=transcribe(path)
    body="\n".join(f"[{s['start']:.1f}-{s['end']:.1f}s] {s['text']}" for s in result["segments"])
    db=Knowledge(GAME)
    try:return db.ingest(Path(path).stem,body,source,patch)
    finally:db.close()
