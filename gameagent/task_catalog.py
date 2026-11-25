"""Read-only inspection of upstream task definitions and feature inventory."""
import json
from pathlib import Path
from .project_hub import SOURCE
from .profiles import load_profiles

def inventory(game):
    if game not in load_profiles():raise ValueError("Unknown game")
    root=SOURCE/game
    if not root.is_dir():return []
    if game=="brown_dust_2":
        path=root/"assets"/"interface.json"
        if not path.is_file():return []
        data=json.loads(path.read_text(encoding="utf-8-sig"))
        tasks=data.get("task",data.get("tasks",[]))
        if not isinstance(tasks,list):return []
        return [{"name":str(t.get("name",t.get("label","Unnamed"))),"source":"assets/interface.json","kind":"upstream task definition"} for t in tasks if isinstance(t,dict)]
    paths={
        "nikke":("module","scripts"),
        "honkai_star_rail":("tasks","route"),
        "genshin_impact":("BetterGenshinImpact/GameTask",),
        "wuthering_waves":("src",),
        "neverness_to_everness":("src",),
    }[game]
    result=[]
    for relative in paths:
        folder=root/relative
        if not folder.is_dir():continue
        for path in sorted(folder.iterdir()):
            if path.name.startswith(("_",".")):continue
            if path.is_dir() or path.suffix in (".py",".cs"):
                result.append({"name":path.stem,"source":path.relative_to(root).as_posix(),"kind":"source component; not a runnable task"})
    return result
