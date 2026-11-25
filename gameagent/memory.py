import sqlite3
import json
from pathlib import Path
from dataclasses import asdict

class Memory:
    def __init__(self, root, game_id):
        if not game_id or not game_id.replace("_", "").isalnum():
            raise ValueError("Invalid profile")
        path = Path(root) / game_id / "memory.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, session TEXT NOT NULL, state TEXT NOT NULL, action TEXT NOT NULL, next_state TEXT NOT NULL)")
        self.db.commit()

    def record(self, session, state, action, next_state):
        self.db.execute("INSERT INTO events(session,state,action,next_state) VALUES(?,?,?,?)", (session,json.dumps(asdict(state)),action.value,json.dumps(asdict(next_state))))
        self.db.commit()

    def rows(self):
        return self.db.execute("SELECT session,state,action,next_state FROM events ORDER BY id").fetchall()

    def close(self):
        self.db.close()
