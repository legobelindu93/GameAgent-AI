import argparse,json
from pathlib import Path
from .profiles import load_profiles
from .catalog import Catalog
from .knowledge import Knowledge

def main():
    p=argparse.ArgumentParser()
    p.add_argument("game",choices=list(load_profiles()))
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("catalog-import");a.add_argument("file");a.add_argument("--authorized",action="store_true",required=True)
    a=sub.add_parser("catalog-search");a.add_argument("query",nargs="?",default="");a.add_argument("--patch")
    a=sub.add_parser("transcribe");a.add_argument("file");a.add_argument("--source",required=True);a.add_argument("--patch",required=True);a.add_argument("--authorized",action="store_true",required=True)
    a=sub.add_parser("frames");a.add_argument("file");a.add_argument("output");a.add_argument("--authorized",action="store_true",required=True)
    a=sub.add_parser("ask");a.add_argument("question");a.add_argument("--patch");a.add_argument("--model",default="qwen2.5:3b")
    args=p.parse_args()
    if args.cmd.startswith("catalog"):
        db=Catalog(args.game)
        try:
            result=db.ingest(json.loads(Path(args.file).read_text(encoding="utf-8-sig"))) if args.cmd=="catalog-import" else db.search(args.query,patch=args.patch)
        finally:db.close()
    elif args.cmd=="transcribe":
        from .video import transcribe
        result=transcribe(args.file)
        db=Knowledge(args.game)
        try:
            body="\n".join(f"{s['start']:.1f}s: {s['text']}" for s in result["segments"])
            result["indexed_chunks"]=db.ingest(Path(args.file).name,body,args.source,args.patch) if body.strip() else 0
        finally:db.close()
    elif args.cmd=="frames":
        from .video import frames
        result=frames(args.file,args.output)
    else:
        from .advisor import advise
        result=advise(args.game,args.question,args.model,args.patch)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
