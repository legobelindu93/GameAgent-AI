"""Explicit, isolated dependency provisioning for locally reviewed upstream sources."""
import subprocess
import shutil
from pathlib import Path
from .project_hub import SOURCE,BASE
from .profiles import load_profiles

PYTHON_GAMES={"nikke","brown_dust_2","wuthering_waves","neverness_to_everness","honkai_star_rail"}
RUNTIMES=["Microsoft.DotNet.DesktopRuntime.10","Microsoft.VCRedist.2015+.x64"]

def run(args,cwd=None):
    p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors="replace",timeout=1800)
    if p.returncode:raise RuntimeError(p.stdout[-6000:])
    return p.stdout[-6000:]

def install_runtime(game):
    if game not in {"genshin_impact","brown_dust_2"}:raise ValueError("No .NET runtime recipe")
    winget=shutil.which("winget")
    if not winget:raise ValueError("winget is required")
    return "\n".join(run([winget,"install","--id",r,"--exact","--accept-source-agreements","--accept-package-agreements"]) for r in RUNTIMES)

def install_python(game,version="3.12"):
    if game not in PYTHON_GAMES or game not in load_profiles():raise ValueError("No Python recipe")
    src=SOURCE/game
    requirements=src/"requirements.txt"
    if not requirements.is_file():raise ValueError("No root requirements.txt: use upstream installation instructions")
    uv=shutil.which("uv")
    if not uv:raise ValueError("uv is required")
    env=BASE/"data"/"environments"/game
    env.parent.mkdir(parents=True,exist_ok=True)
    if not (env/"Scripts"/"python.exe").is_file():
        run([uv,"venv","--python",version,str(env)])
    return run([uv,"pip","install","--python",str(env/"Scripts"/"python.exe"),"-r",str(requirements)],cwd=src)

def diagnostic(game):
    if game not in load_profiles():raise ValueError("Unknown game")
    src=SOURCE/game
    return {"source":str(src),"requirements":(src/"requirements.txt").is_file(),"pyproject":(src/"pyproject.toml").is_file(),"isolated_python":(BASE/"data"/"environments"/game/"Scripts"/"python.exe").is_file(),"uv":bool(shutil.which("uv")),"winget":bool(shutil.which("winget"))}
