import argparse
import json
from .scenarios import SCENARIOS,evaluate

def main():
    p=argparse.ArgumentParser(description="Evaluate synthetic scenarios")
    p.add_argument("--game",choices=list(SCENARIOS)+["all"],default="all")
    args=p.parse_args()
    keys=SCENARIOS if args.game=="all" else [args.game]
    print(json.dumps([evaluate(k) for k in keys],indent=2))

if __name__=="__main__":
    main()
