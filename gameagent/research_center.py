"""CLI for the lightweight research and pack workflow."""
import argparse,json
from pathlib import Path
from .profiles import load_profiles
from .packs import PACKS,registry,make,verify,load_json,atomic,install,coverage,compare
from .research_engine import discover,research_cycle,import_notes,compile_candidates
from .account_import import import_account
def main():
    p=argparse.ArgumentParser()
    p.add_argument("game",choices=list(load_profiles()))
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("sources");sub.add_parser("coverage")
    a=sub.add_parser("discover");a.add_argument("--topic")
    a=sub.add_parser("cycle");a.add_argument("--max-queries",type=int,default=2)
    a=sub.add_parser("build");a.add_argument("records");a.add_argument("output");a.add_argument("--version",required=True)
    a=sub.add_parser("verify");a.add_argument("file")
    a=sub.add_parser("install");a.add_argument("file");a.add_argument("--trusted",action="store_true")
    a=sub.add_parser("seed")
    a=sub.add_parser("notes");a.add_argument("file");a.add_argument("--source",required=True);a.add_argument("--patch",required=True);a.add_argument("--authorized",action="store_true")
    a=sub.add_parser("compile");a.add_argument("file");a.add_argument("output");a.add_argument("--source",required=True);a.add_argument("--patch",required=True);a.add_argument("--version",required=True);a.add_argument("--authorized",action="store_true")
    a=sub.add_parser("account");a.add_argument("file");a.add_argument("--confirmed",action="store_true")
    a=sub.add_parser("conflicts");a.add_argument("file")
    args=p.parse_args();g=args.game;c=args.cmd
    if c=="sources":result=registry(g)
    elif c=="coverage":result=coverage(g)
    elif c=="discover":result=discover(g,args.topic)
    elif c=="cycle":result=research_cycle(g,args.max_queries)
    elif c=="build":
        pack=make(g,args.version,load_json(args.records));atomic(args.output,pack);result={"sha256":pack["sha256"],"records":len(pack["records"])}
    elif c=="verify":
        pack=verify(load_json(args.file),g);result={"valid":True,"version":pack["version"],"records":len(pack["records"])}
    elif c=="install":result=install(args.file,g,trusted=args.trusted)
    elif c=="seed":
        path=PACKS/g/"seed.json"
        if not path.exists():raise ValueError("No reviewed seed for this game yet")
        target=Path("data/packs")/g/"seed-v1.json";atomic(target,make(g,"1.0.0",load_json(path)));result=install(target,g,trusted=True)
    elif c=="notes":result=import_notes(g,args.file,args.source,args.patch,args.authorized)
    elif c=="compile":
        pack=compile_candidates(g,args.file,args.version,args.source,args.patch,args.authorized);atomic(args.output,pack);result={"candidates":len(pack["records"]),"output":args.output}
    elif c=="account":result=import_account(g,args.file,args.confirmed)
    elif c=="conflicts":result=compare(verify(load_json(args.file),g)["records"])
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
