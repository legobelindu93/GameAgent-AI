"""Isolated upstream source retrieval and static inventory. Never executes upstream code."""
import argparse
import json
import subprocess
from pathlib import Path
from .profiles import ROOT, load_profiles

def source(game):
    if game not in load_profiles():
        raise ValueError("Unknown game")
    return json.loads((ROOT/game/"upstream.json").read_text(encoding="utf-8"))

def git(*args):
    return subprocess.run(["git","-c","core.hooksPath=/dev/null",*args],check=True,capture_output=True,text=True,timeout=300).stdout.strip()

def acquire(game, root="data/upstream"):
    spec=source(game)
    dest=Path(root).resolve()/game
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        raise FileExistsError("Source already exists; review before replacing")
    git("clone","--no-checkout","--depth","1","--",spec["repository"],str(dest))
    revision=git("-C",str(dest),"rev-parse","HEAD")
    return {"game":game,"revision":revision,"repository":spec["repository"],"path":str(dest)}

def inventory(game, root="data/upstream"):
    source(game)
    dest=Path(root).resolve()/game
    revision=git("-C",str(dest),"rev-parse","HEAD")
    paths=git("-C",str(dest),"ls-tree","-r","--name-only","HEAD").splitlines()
    return {"game":game,"revision":revision,"license_files":[p for p in paths if Path(p).name.lower().startswith(("license","copying","notice"))],"image_files":sum(Path(p).suffix.lower() in (".png",".jpg",".jpeg",".webp") for p in paths),"python_files":sum(p.endswith(".py") for p in paths),"csharp_files":sum(p.endswith(".cs") for p in paths),"json_files":sum(p.endswith(".json") for p in paths)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("operation",choices=["acquire","inventory"])
    p.add_argument("game",choices=list(load_profiles()))
    a=p.parse_args()
    print(json.dumps((acquire if a.operation=="acquire" else inventory)(a.game),indent=2))

if __name__=="__main__":
    main()
