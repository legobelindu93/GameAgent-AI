"""Discover official release assets and manage user-selected local installations."""
import json
import hashlib
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit
from .project_hub import project,BASE

def releases(game):
    slug=urlsplit(project(game)["repository"]).path.strip("/")
    req=Request("https://api.github.com/repos/"+slug+"/releases/latest",headers={"Accept":"application/vnd.github+json","User-Agent":"GameAgent-AI"})
    with urlopen(req,timeout=20) as r:
        data=json.load(r)
    return {"tag":data["tag_name"],"assets":[{"name":a["name"],"url":a["browser_download_url"],"size":a["size"],"digest":a.get("digest")} for a in data.get("assets",[]) if a["name"].lower().endswith((".zip",".exe",".7z",".msi"))]}

def download(game,asset):
    slug=urlsplit(project(game)["repository"]).path.strip("/")
    u=urlsplit(asset["url"])
    if u.scheme!="https" or u.hostname!="github.com" or not u.path.startswith("/"+slug+"/releases/download/"):
        raise ValueError("Unexpected release URL")
    name=asset["name"]
    if Path(name).name!=name or "/" in name or "\\" in name or ":" in name:
        raise ValueError("Invalid asset name")
    folder=BASE/"data"/"downloads"/game
    folder.mkdir(parents=True,exist_ok=True)
    target=folder/name
    if target.exists():raise FileExistsError(str(target))
    partial=target.with_suffix(target.suffix+".part")
    h=hashlib.sha256()
    size=0
    try:
        with urlopen(Request(asset["url"],headers={"User-Agent":"GameAgent-AI"}),timeout=60) as r,partial.open("xb") as f:
            while chunk:=r.read(1024*1024):
                size+=len(chunk)
                if size>asset["size"]:raise ValueError("Unexpected size")
                h.update(chunk);f.write(chunk)
        if size!=asset["size"]:raise ValueError("Incomplete download")
        digest=asset.get("digest")
        if digest and digest!="sha256:"+h.hexdigest():raise ValueError("Checksum mismatch")
        partial.rename(target)
        return {"path":str(target),"sha256":h.hexdigest(),"publisher_digest_verified":bool(digest)}
    except Exception:
        partial.unlink(missing_ok=True)
        raise
