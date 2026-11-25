"""Launch reviewed upstream applications from their own environments.
No task injection, automatic startup tasks, or anti-cheat modifications.
"""
import subprocess,os,socket
from pathlib import Path
from .project_hub import BASE,SOURCE
from .profiles import load_profiles
from . import native

RECIPES={
    "nikke":{"entry":"gui.py","port":12271,"python":"review upstream requirements"},
    "honkai_star_rail":{"entry":"gui.py","port":22367,"python":"review upstream installer"},
    "wuthering_waves":{"entry":"main.py","python":">=3.11"},
    "neverness_to_everness":{"entry":"main.py","python":"3.12"},
    "brown_dust_2":{"entry":None,"python":None},
    "genshin_impact":{"entry":None,"python":None},
}

def describe(game):
    if game not in load_profiles():raise ValueError("Unknown game")
    recipe=RECIPES[game]
    source=SOURCE/game
    env=BASE/"data"/"environments"/game/"Scripts"/"python.exe"
    entry=source/recipe["entry"] if recipe["entry"] else None
    installed=native.load(game).get("executable","")
    return {"game":game,"source":str(source),"entry":str(entry) if entry else None,
            "entry_available":bool(entry and entry.is_file()),"python":str(env),
            "environment_available":env.is_file(),"python_requirement":recipe["python"],
            "installed_application":installed,"port":recipe.get("port")}

def start_interface(game):
    info=describe(game)
    if info["installed_application"]:
        return native.launch(game)
    if not info["entry_available"] or not info["environment_available"]:
        raise ValueError("Install the original application or provision its reviewed source environment first.")
    args=[info["python"],info["entry"]]
    port=info["port"]
    if port:
        with socket.socket() as sock:
            try:sock.bind(("127.0.0.1",port))
            except OSError as exc:raise ValueError("Local WebUI port already occupied") from exc
        args+=["--host","127.0.0.1","--port",str(port)]
    logs=BASE/"data"/"runtime_logs"/game
    logs.mkdir(parents=True,exist_ok=True)
    with (logs/"interface.log").open("ab") as log:
        process=subprocess.Popen(args,cwd=info["source"],stdout=log,stderr=subprocess.STDOUT,shell=False)
    if port:native.save(game,"",f"http://127.0.0.1:{port}")
    return process
