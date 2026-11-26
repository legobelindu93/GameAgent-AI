"""Read-only normalized account imports, no credentials or private APIs."""
from .packs import game_check,load_json,atomic,now
from .profiles import ROOT
def import_account(game,path,confirmed=False):
    game_check(game)
    if not confirmed:raise ValueError("Confirm import of account data")
    obj=load_json(path)
    if not isinstance(obj,dict) or set(obj)!={"game","resources","roster"} or obj["game"]!=game:raise ValueError("Expected normalized account export")
    resources=obj["resources"];roster=obj["roster"]
    if not isinstance(resources,dict) or len(resources)>100 or not isinstance(roster,list) or len(roster)>1000:raise ValueError("Invalid account data")
    for k,v in resources.items():
        if not isinstance(k,str) or not k.strip() or len(k)>80 or type(v)!=int or not 0<=v<=10**12:raise ValueError("Invalid resource")
    for row in roster:
        if not isinstance(row,dict) or set(row)!={"character","costume","level","upgrade"}:raise ValueError("Invalid roster entry")
        if any(not isinstance(row[k],str) or not row[k].strip() or len(row[k])>120 for k in ("character","costume")):raise ValueError("Invalid names")
        if any(type(row[k])!=int or not 0<=row[k]<=1000 for k in ("level","upgrade")):raise ValueError("Invalid levels")
    result=dict(obj,updated=now())
    atomic(ROOT.parent/"data"/"accounts"/game/"account.json",result)
    return {"game":game,"resources":len(resources),"roster":len(roster)}
