"""Explicit review and retrieval benchmark for versioned packs."""
import tempfile
from pathlib import Path
from .packs import PACKS,make,verify,load_json,atomic,install,registry
from .knowledge import Knowledge
def review(pack,ids,version):
    verify(pack)
    wanted=set(ids)
    if not wanted or not wanted.issubset({r["id"] for r in pack["records"]}):raise ValueError("Unknown or empty review selection")
    if tuple(map(int,version.split(".")))<=tuple(map(int,pack["version"].split("."))):raise ValueError("New version must increase")
    records=[dict(r,review="approved") if r["id"] in wanted else dict(r) for r in pack["records"]]
    return make(pack["game"],version,records)
def benchmark(game):
    """Smoke test: retrieve the exact seed source by title, not gameplay intelligence."""
    registry(game)
    records=load_json(PACKS/game/"seed.json")
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"pack.json"
        atomic(path,make(game,"1.0.0",records));install(path,game,root=d,trusted=True)
        db=Knowledge(game,root=d)
        try:
            rows=[]
            for record in records:
                found=db.search(record["title"],limit=5)
                hit=any(x["source"]==record["source"] and x["title"]==record["title"] for x in found)
                rows.append({"title":record["title"],"retrieved":hit})
        finally:db.close()
    return {"game":game,"test":"seed retrieval@5","passed":sum(r["retrieved"] for r in rows),"total":len(rows),"rows":rows}
