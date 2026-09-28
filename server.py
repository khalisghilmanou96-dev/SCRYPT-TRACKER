from flask import Flask, request, jsonify, send_from_directory, session
import sqlite3, os, json
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,"pulsetrack.db")
app=Flask(__name__, static_folder=None)
app.secret_key=os.environ.get("PULSETRACK_SECRET","change-this-secret-before-production")
app.permanent_session_lifetime=timedelta(hours=8)

def db():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    c=db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS admins(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sessions(
      id TEXT PRIMARY KEY,
      created_at TEXT NOT NULL,
      duration INTEGER NOT NULL DEFAULT 0,
      max_scroll INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id TEXT NOT NULL,
      type TEXT NOT NULL,
      t INTEGER NOT NULL DEFAULT 0,
      target TEXT,
      x REAL,
      y REAL,
      depth INTEGER,
      state TEXT,
      FOREIGN KEY(session_id) REFERENCES sessions(id)
    );
    """)
    if not c.execute("SELECT 1 FROM admins WHERE username=?",("admin",)).fetchone():
        c.execute("INSERT INTO admins(username,password_hash) VALUES(?,?)",
                  ("admin",generate_password_hash("PulseTrackV1!")))
    c.commit(); c.close()

@app.before_request
def setup():
    if not os.path.exists(DB): init_db()

@app.get("/")
def home(): return send_from_directory(BASE,"index.html")

@app.get("/<path:name>")
def static_files(name):
    if name.endswith((".html",".js",".css")):
        return send_from_directory(BASE,name)
    return ("Not found",404)

@app.post("/api/login")
def login():
    data=request.get_json(silent=True) or {}
    c=db(); row=c.execute("SELECT * FROM admins WHERE username=?",(data.get("username",""),)).fetchone(); c.close()
    if row and check_password_hash(row["password_hash"],data.get("password","")):
        session.permanent=True; session["admin_id"]=row["id"]; session["username"]=row["username"]
        return jsonify(ok=True)
    return jsonify(ok=False,error="Identifiants incorrects"),401

@app.post("/api/logout")
def logout():
    session.clear(); return jsonify(ok=True)

@app.get("/api/me")
def me():
    if "admin_id" not in session: return jsonify(authenticated=False),401
    return jsonify(authenticated=True,username=session.get("username"))

@app.post("/api/sessions")
def ingest():
    data=request.get_json(silent=True) or {}
    sid=str(data.get("id",""))[:64]
    if not sid: return jsonify(error="session id required"),400
    events=data.get("events",[])
    if not isinstance(events,list) or len(events)>2000: return jsonify(error="invalid events"),400
    c=db()
    c.execute("INSERT OR REPLACE INTO sessions(id,created_at,duration,max_scroll) VALUES(?,?,?,?)",
              (sid,str(data.get("createdAt",""))[:64],int(data.get("duration",0)),int(data.get("maxScroll",0))))
    c.execute("DELETE FROM events WHERE session_id=?",(sid,))
    for e in events:
        c.execute("""INSERT INTO events(session_id,type,t,target,x,y,depth,state)
                     VALUES(?,?,?,?,?,?,?,?)""",
                  (sid,str(e.get("type",""))[:40],int(e.get("t",0)),
                   str(e.get("target",""))[:300] if e.get("target") is not None else None,
                   e.get("x"),e.get("y"),e.get("depth"),
                   str(e.get("state",""))[:40] if e.get("state") is not None else None))
    c.commit(); c.close()
    return jsonify(ok=True)

def auth():
    return "admin_id" in session

@app.get("/api/data")
def data():
    if not auth(): return jsonify(error="unauthorized"),401
    c=db()
    ss=[dict(r) for r in c.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()]
    for s in ss:
        s["createdAt"]=s.pop("created_at"); s["maxScroll"]=s.pop("max_scroll")
        ev=[dict(r) for r in c.execute("SELECT type,t,target,x,y,depth,state FROM events WHERE session_id=? ORDER BY t",(s["id"],)).fetchall()]
        s["events"]=ev
    c.close(); return jsonify(ss)

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=8086,debug=False)
