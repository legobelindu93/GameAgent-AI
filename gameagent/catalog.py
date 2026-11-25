"""Patch-aware structured character and build catalog; import normalized, authorized JSON."""
import sqlite3,json
from pathlib import Path
from .profiles import load_profiles

class Catalog:
    def __init__(self,game,root="data/catalog"):
        if game not in load_profiles():raise ValueError("Unknown game")
        path=Path(root)/game/"catalog.sqlite"
        path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS entries (kind TEXT, name TEXT, patch TEXT, source TEXT, payload TEXT, PRIMARY KEY(kind,name,patch,source))")
    def ingest(self,records):
        if not isinstance(records,list):raise ValueError("Expected a JSON array")
        rows=[]
        for r in records:
            if r["kind"] not in {"character","build","team","weapon","enemy","mechanic"}:raise ValueError("Invalid kind")
            if not all(isinstance(r[k],str) and r[k].strip() for k in ("name","patch","source")):raise ValueError("Missing metadata")
            if not isinstance(r["data"],dict):raise ValueError("Invalid data")
            rows.append((r["kind"],r["name"],r["patch"],r["source"],json.dumps(r["data"],ensure_ascii=False)))
        with self.db:self.db.executemany("INSERT OR REPLACE INTO entries VALUES(?,?,?,?,?)",rows)
        return len(rows)
    def search(self,query="",kind=None,patch=None):
        sql="SELECT kind,name,patch,source,payload FROM entries WHERE instr(lower(name),lower(?))>0"
        args=[query] if query else []
        if not query:sql="SELECT kind,name,patch,source,payload FROM entries WHERE 1=1"
        if kind:sql+=" AND kind=?";args.append(kind)
        if patch:sql+=" AND patch=?";args.append(patch)
        sql+=" ORDER BY name,patch LIMIT 200"
        return [{"kind":k,"name":n,"patch":p,"source":s,"data":json.loads(d)} for k,n,p,s,d in self.db.execute(sql,args)]
    def close(self):self.db.close()
