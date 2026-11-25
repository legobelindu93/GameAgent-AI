"""Local source workbench: inspect checked-out upstream projects without running them."""
import json
import subprocess
import os
import sys
import webbrowser
from pathlib import Path
from .profiles import ROOT,load_profiles

BASE=ROOT.parent
SOURCE=BASE/"data"/"upstream"

def project(game):
    if game not in load_profiles():raise ValueError("Unknown game")
    return json.loads((ROOT/game/"project.json").read_text(encoding="utf-8"))

def inspect(game):
    meta=project(game)
    folder=SOURCE/game
    result={"project":meta,"path":str(folder),"revision":None,"files":[],"docs":[],"licenses":[]}
    if not folder.is_dir():return result
    def git(*args):
        return subprocess.run(["git","-C",str(folder),*args],capture_output=True,text=True,check=True,timeout=15).stdout.strip()
    try:
        result["revision"]=git("rev-parse","HEAD")
        paths=git("ls-files").splitlines()
    except (subprocess.SubprocessError,OSError):return result
    result["files"]=[p for p in paths if (folder/p).is_file()]
    result["docs"]=[p for p in result["files"] if Path(p).suffix.lower() in (".md",".rst",".txt") and (Path(p).name.lower().startswith("readme") or p.startswith("docs/"))]
    result["licenses"]=[p for p in result["files"] if Path(p).name.lower().startswith(("license","copying","notice"))]
    return result

def read_source(game,path):
    project(game)
    folder=(SOURCE/game).resolve()
    target=(folder/path).resolve()
    if not target.is_relative_to(folder) or not target.is_file():raise ValueError("Invalid source file")
    if target.suffix.lower() not in (".md",".txt",".rst",".json",".py",".cs",".xaml",".yaml",".yml",".ts",".tsx",".js",".vue",".html",".toml",".ini",".xml") and not target.name.lower().startswith(("license","copying","notice")):raise ValueError("Only text source files")
    with target.open("rb") as stream:
        return stream.read(200000).decode("utf-8",errors="replace")

def open_folder(game):
    project(game)
    p=SOURCE/game
    if not p.is_dir():raise ValueError("Source not downloaded")
    if sys.platform=="win32":os.startfile(p)
    else:subprocess.Popen(["xdg-open",str(p)])
