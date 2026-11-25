import argparse
import json
from .profiles import load_profiles

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("profiles")
    nav=sub.add_parser("route")
    nav.add_argument("game")
    rec=sub.add_parser("inspect")
    rec.add_argument("game")
    rec.add_argument("image")
    training=sub.add_parser("train-navigation")
    training.add_argument("--steps",type=int,default=10000)
    training.add_argument("--output",default="data/navigation/ppo")
    args=parser.parse_args()
    profiles=load_profiles()
    if args.command=="profiles":
        print(json.dumps(profiles,indent=2))
    elif args.command=="route":
        from .navigation import MAPS,route
        if args.game not in MAPS:parser.error("No synthetic navigation map for this profile")
        print(json.dumps(route(MAPS[args.game]),indent=2))
    elif args.command=="inspect":
        from .pipeline import inspect
        from .profiles import ROOT
        if args.game not in profiles:parser.error("Unknown profile")
        print(json.dumps(inspect(args.image,ROOT/args.game/"recognition.json"),indent=2))
    else:
        from .minigrid_lab import train
        train(args.steps,args.output)

if __name__=="__main__":
    main()
