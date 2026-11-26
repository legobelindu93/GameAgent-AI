"""Compare public search results for new announcement candidates (not a patch parser)."""
from .research_engine import discover,BASE
from .packs import registry,atomic,load_json,now
def check(game):
    registry(game)
    path=BASE/game/"announcements.json"
    previous=load_json(path) if path.exists() else {"items":[]}
    result=discover(game,"official update patch notes announcements events",limit=8)
    items=[x for x in result["results"] if x.get("kind") in {"web","video"}]
    seen={x["url"] for x in previous["items"]}
    new=[x for x in items if x["url"] not in seen]
    merged={x["url"]:x for x in previous["items"]+items}
    if not result["errors"] and items:atomic(path,{"checked":now(),"items":list(merged.values())[-500:]})
    return {"new_candidates":new,"errors":result["errors"],"providers":result["providers"],"verified_patch":None}
