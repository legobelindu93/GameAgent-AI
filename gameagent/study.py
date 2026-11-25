"""Import authorized local documents and search the game knowledge base."""
import argparse
import json
from pathlib import Path
from .knowledge import Knowledge
from .profiles import load_profiles

def main():
    p=argparse.ArgumentParser()
    p.add_argument("game",choices=list(load_profiles()))
    sub=p.add_subparsers(dest="command",required=True)
    add=sub.add_parser("import")
    add.add_argument("file")
    for key in ("title","source","patch"):add.add_argument("--"+key,required=True)
    add.add_argument("--authorized",action="store_true",required=True)
    search=sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--patch")
    sub.add_parser("sources")
    args=p.parse_args()
    if args.command=="sources":
        from .profiles import ROOT
        print((ROOT/args.game/"knowledge_sources.json").read_text(encoding="utf-8"))
        return
    store=Knowledge(args.game)
    try:
        if args.command=="import":
            path=Path(args.file)
            if path.suffix.lower() not in (".txt",".md",".srt",".vtt"):p.error("Supported: TXT, MD, SRT, VTT")
            if path.stat().st_size>8_000_000:p.error("File too large")
            print(json.dumps({"chunks_added":store.ingest(args.title,path.read_text(encoding="utf-8-sig"),args.source,args.patch)}))
        else:
            print(json.dumps(store.search(args.query,args.patch),ensure_ascii=False,indent=2))
    finally:store.close()

if __name__=="__main__":main()
