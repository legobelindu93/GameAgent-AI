"""Manage user-installed upstream interfaces as separate processes."""
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from .profiles import load_profiles,ROOT

CONFIG=ROOT.parent/"data"/"native_interfaces.json"

def validate(game):
    if game not in load_profiles():raise ValueError("Unknown game")

def load(game):
    validate(game)
    return json.loads(CONFIG.read_text(encoding="utf-8")).get(game,{}) if CONFIG.exists() else {}

def save(game, executable, web_url=""):
    validate(game)
    p=Path(executable).resolve() if executable else None
    if p and (not p.is_file() or p.suffix.lower()!=".exe"):raise ValueError("Select an installed Windows executable")
    if web_url:
        u=urlsplit(web_url)
        if u.scheme!="http" or u.hostname not in ("localhost","127.0.0.1") or u.username or u.password:raise ValueError("Only local HTTP interfaces are supported")
        if not u.port:raise ValueError("Specify the local port")
    records=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    records[game]={"executable":str(p) if p else "","web_url":web_url}
    CONFIG.parent.mkdir(parents=True,exist_ok=True)
    tmp=CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(records,indent=2),encoding="utf-8")
    tmp.replace(CONFIG)

def launch(game):
    settings=load(game)
    p=Path(settings.get("executable",""))
    if not p.is_file() or p.suffix.lower()!=".exe":raise ValueError("Configure the installed executable first")
    return subprocess.Popen([str(p)],cwd=str(p.parent),shell=False)

def web_panel(game):
    url=load(game).get("web_url","")
    u=urlsplit(url)
    if u.scheme!="http" or u.hostname not in ("localhost","127.0.0.1") or u.username or u.password or not u.port:raise ValueError("Configure a local web interface first")
    import webview
    webview.create_window(load_profiles()[game]["name"],url,width=1200,height=800)
    webview.start()

if __name__=="__main__":
    import sys
    web_panel(sys.argv[1])
