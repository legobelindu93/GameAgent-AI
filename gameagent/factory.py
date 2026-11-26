"""Bounded research jobs, reusable output cache and GPU-free advisory retrieval."""
from pathlib import Path
from .packs import PACKS,registry,coverage,make,verify,load_json,atomic,digest,now,validate_record,install
from .research_engine import BASE
from .cloud_study import web_dossier,video_study,youtube_url
from .knowledge import Knowledge
from .profiles import ROOT,load_profiles

def build_bundle(output):
    """Produce distributable JSON packs, no network or optional dependencies."""
    output=Path(output)
    manifests=[]
    for game in sorted(load_profiles()):
        pack=make(game,"1.0.0",load_json(PACKS/game/"seed.json"))
        filename=game+".json"
        atomic(output/filename,pack)
        verify(load_json(output/filename),game)
        manifests.append({"game":game,"file":filename,"sha256":pack["sha256"],"records":len(pack["records"])})
    result={"schema":1,"packs":manifests}
    atomic(output/"manifest.json",result)
    return result

def bootstrap(output="data/packs/starter",root="data/knowledge"):
    result=build_bundle(output)
    return [install(Path(output)/m["file"],m["game"],root=root,trusted=True) for m in result["packs"]]

def dossier_candidates(dossier,version="1.0.0"):
    """Conservatively extract cited paragraphs as candidates; annotations aren't proof."""
    game=dossier["game"];registry(game)
    records=[]
    for a in dossier["citations"]:
        if len(records)>=60:break
        try:
            part=dossier["parts"][a["part"]]
            start=a["start_index"];end=a["end_index"]
            if type(start)!=int or type(end)!=int or not 0<=start<end<=len(part):continue
            left=part.rfind("\n",0,start)+1
            right=part.find("\n",end)
            if right<0:right=len(part)
            claim=part[left:right].strip()
            if not claim or len(claim)>1200:continue
            r={"category":"mechanics","title":dossier["topic"][:180],"claim":claim,
               "source":a["url"],"patch":"unverified; research candidate","locator":f"research text offsets {left}-{right}; check original",
               "review":"candidate"}
            r["id"]="web-"+digest(r)[:20];validate_record(r)
            if r not in records:records.append(r)
        except (ValueError,TypeError,KeyError,IndexError):continue
    return make(game,version,records)

def batch(game,web=False,video_file=None,authorized=False,refresh=False,max_web=1,max_video=1):
    """Single bounded run; no recurring spend, no account data sent to remote providers."""
    registry(game)
    if type(max_web)!=int or type(max_video)!=int or not 0<=max_web<=3 or not 0<=max_video<=2:raise ValueError("Limits: 0-3 web, 0-2 video")
    if (web or video_file) and not authorized:raise ValueError("Explicit permission for remote processing required")
    candidates=[]
    if video_file:
        obj=load_json(video_file)
        if not isinstance(obj,list) or len(obj)>100:raise ValueError("Expected a limited list of approved video URLs")
        candidates=[]
        for row in obj:
            if not isinstance(row,dict) or set(row)!={"url","patch","authorized"} or row["authorized"] is not True:raise ValueError("Video must have explicit authorization")
            if not isinstance(row["patch"],str) or not row["patch"].strip():raise ValueError("Patch/date required")
            candidates.append({"url":youtube_url(row["url"]),"patch":row["patch"]})
    root=BASE/game/"jobs";root.mkdir(parents=True,exist_ok=True)
    gaps=coverage(game)
    def job_path(kind,key):
        return root/(kind+"-"+digest(key)[:24]+".json")
    selected=sorted(gaps,key=lambda t:(not refresh and job_path("web",{"topic":t}).exists(),gaps[t]))[:max_web]
    report={"game":game,"started":now(),"coverage_proxy":gaps,"jobs":[]}
    def execute(kind,key,fn):
        target=job_path(kind,key)
        pack_path=target.with_name(target.stem+".pack.json")
        if target.exists() and not refresh:
            try:
                cached=load_json(target);pack=cached["pack"] if kind=="web" else cached
                verify(pack,game);atomic(pack_path,pack)
                report["jobs"].append({"kind":kind,"status":"cached","file":str(target),"pack":str(pack_path)});return
            except (ValueError,KeyError,TypeError):
                report["jobs"].append({"kind":kind,"status":"invalid_cache","file":str(target)});return
        try:
            obj=fn();pack=obj["pack"] if kind=="web" else obj
            verify(pack,game);atomic(target,obj);atomic(pack_path,pack)
            report["jobs"].append({"kind":kind,"status":"complete","file":str(target),"pack":str(pack_path)})
        except Exception as exc:
            # Do not log full third-party error payloads (they can contain credentials).
            report["jobs"].append({"kind":kind,"status":"failed","error":type(exc).__name__})
    if web:
        for topic in selected:
            def research(t=topic):
                d=web_dossier(game,t,True)
                return {"dossier":d,"pack":dossier_candidates(d)}
            execute("web",{"topic":topic},research)
    if video_file:
        ordered=sorted(candidates,key=lambda row:not refresh and job_path("video",row).exists())
        for row in ordered[:max_video]:
            execute("video",row,lambda r=row:video_study(game,r["url"],r["patch"],authorized=True))
    report["finished"]=now()
    atomic(BASE/game/"last_batch.json",report)
    return report

def offline_advice(game,question,root="data/knowledge"):
    registry(game)
    if not isinstance(question,str) or not question.strip() or len(question)>1000:raise ValueError("Question required")
    db=Knowledge(game,root=root)
    try:rows=db.search(question,limit=8)
    finally:db.close()
    # Do not invent a recommendation when retrieval is empty.
    result={"game":game,"question":question,"mode":"retrieval_only","evidence":rows,
            "answer":"Consulte les fiches et leurs versions ci-dessous ; elles ne prouvent pas une stratégie optimale." if rows else "Connaissances insuffisantes. Installe le pack initial ou approfondis ce sujet."}
    p=ROOT.parent/"data"/"accounts"/game/"account.json"
    if p.exists():
        a=load_json(p)
        if a.get("game")==game:result["account_context"]={"resources":a.get("resources",{}),"roster_count":len(a.get("roster",[])),"updated":a.get("updated")}
    return result
