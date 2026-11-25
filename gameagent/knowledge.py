"""Local, game-isolated evidence index for authorized notes and transcripts."""
import sqlite3
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from .profiles import load_profiles

class Knowledge:
    def __init__(self, game, root="data/knowledge"):
        if game not in load_profiles():
            raise ValueError("Unknown game")
        path=Path(root)/game/"knowledge.sqlite"
        path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path)
        self.db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS evidence USING fts5(title, body, source UNINDEXED, patch UNINDEXED, digest UNINDEXED, added UNINDEXED)")
    def ingest(self,title,body,source,patch):
        if not all(x.strip() for x in (title,body,source,patch)):
            raise ValueError("Metadata and content required")
        if len(body)>2_000_000:
            raise ValueError("Document too large")
        count=0
        with self.db:
            for start in range(0,len(body),1500):
                chunk=body[max(0,start-150):start+1500].strip()
                if not chunk:continue
                digest=hashlib.sha256((source+"\0"+patch+"\0"+chunk).encode()).hexdigest()
                if self.db.execute("SELECT 1 FROM evidence WHERE digest=?",(digest,)).fetchone():continue
                self.db.execute("INSERT INTO evidence VALUES(?,?,?,?,?,?)",(title,chunk,source,patch,digest,datetime.now(timezone.utc).isoformat()))
                count+=1
        return count
    def search(self,query,patch=None,limit=8):
        if not 1<=limit<=30:raise ValueError("Invalid limit")
        words=re.findall(r"[^\W_]+",query)[:30]
        if not words:return []
        term=" OR ".join('"'+w+'"' for w in words)
        sql="SELECT title,body,source,patch FROM evidence WHERE evidence MATCH ?"
        params=[term]
        if patch:
            sql+=" AND patch=?"
            params.append(patch)
        sql+=" ORDER BY bm25(evidence) LIMIT ?"
        return [dict(zip(("title","body","source","patch"),row)) for row in self.db.execute(sql,(*params,limit))]
    def close(self):
        self.db.close()
