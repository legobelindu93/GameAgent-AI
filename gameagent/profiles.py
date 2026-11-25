import json
from pathlib import Path

ROOT = Path(__file__).parent.parent / "games"

def load_profiles():
    profiles = {}
    for path in sorted(ROOT.glob("*/manifest.json")):
        p = json.loads(path.read_text(encoding="utf-8"))
        if p["id"] != path.parent.name or p["id"] in profiles:
            raise ValueError(f"Invalid profile: {path}")
        profiles[p["id"]] = p
    return profiles
