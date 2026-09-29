"""
backend/main.py
FastAPI backend exposing the negotiation engine over HTTP, with SQLite
persistence (zero external DB setup needed — works on Mac and Windows
with no extra install beyond Python's stdlib sqlite3).

Run:
    cd negotiai
    pip install fastapi uvicorn
    uvicorn backend.main:app --reload --port 8000

Endpoints:
    POST /api/negotiate/run          -> run a full negotiation, persist it
    GET  /api/negotiate/{session_id} -> fetch one saved transcript+outcome
    GET  /api/history                -> list all past sessions (extra feature:
                                         judges can see a running total of
                                         value protected across every demo run)
    GET  /api/domains                -> list available domains
"""

import json
import sqlite3
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))  # import sibling modules

from domains import DOMAINS
from orchestrator import run_negotiation as run_negotiation_offline
from generative_engine import run_negotiation_generative

DB_PATH = Path(__file__).resolve().parent / "negotiai.db"

app = FastAPI(title="NegotiAI API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before any real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            domain_key TEXT,
            domain_title TEXT,
            goal TEXT,
            resolved INTEGER,
            turns INTEGER,
            value_saved INTEGER,
            transcript_json TEXT,
            created_at REAL
        )
    """)
    conn.commit()
    conn.close()


init_db()


class RunRequest(BaseModel):
    domain_key: str
    mode: str = "auto"  # "auto" (generative if an LLM is configured, else deterministic),
                        # "generative" (force it, errors if no LLM configured),
                        # "deterministic" (force the rule-based ladder, ignores any LLM)


@app.get("/api/health")
def health():
    from agents import LLM_MODE
    return {"status": "ok", "llm_mode": LLM_MODE if LLM_MODE else False}


@app.get("/api/domains")
def list_domains():
    return {k: {"title": v["title"]} for k, v in DOMAINS.items()}


@app.post("/api/negotiate/run")
def run_negotiation(req: RunRequest):
    if req.domain_key not in DOMAINS:
        raise HTTPException(status_code=400, detail="Unknown domain")

    from agents import LLM_MODE

    if req.mode == "deterministic":
        transcript, outcome = run_negotiation_offline(req.domain_key)
        outcome["mode"] = "deterministic"
    elif req.mode == "generative":
        if not LLM_MODE:
            raise HTTPException(
                status_code=400,
                detail="Generative mode requested but no LLM provider is configured "
                       "(set GROQ_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY)."
            )
        transcript, outcome = run_negotiation_generative(req.domain_key)
        # If the generative call failed mid-negotiation, run_negotiation_generative
        # silently falls back — reflect that honestly rather than claiming generative.
        outcome.setdefault("mode", "deterministic")
    else:  # "auto"
        if LLM_MODE:
            transcript, outcome = run_negotiation_generative(req.domain_key)
            outcome.setdefault("mode", "deterministic")
        else:
            transcript, outcome = run_negotiation_offline(req.domain_key)
            outcome["mode"] = "deterministic"

    session_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?)",
        (
            session_id,
            req.domain_key,
            outcome["domain"],
            outcome["goal"],
            int(outcome["resolved"]),
            outcome["turns"],
            outcome["estimated_value_saved"],
            json.dumps(transcript),
            time.time(),
        ),
    )
    conn.commit()
    conn.close()

    return {"session_id": session_id, "transcript": transcript, "outcome": outcome}


@app.get("/api/negotiate/{session_id}")
def get_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": row[0],
        "domain_key": row[1],
        "domain_title": row[2],
        "goal": row[3],
        "resolved": bool(row[4]),
        "turns": row[5],
        "value_saved": row[6],
        "transcript": json.loads(row[7]),
        "created_at": row[8],
    }


@app.get("/api/history")
def get_history():
    """Extra feature: aggregate dashboard across every negotiation run so far."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, domain_title, resolved, turns, value_saved, created_at FROM sessions ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    sessions = [
        {
            "session_id": r[0],
            "domain_title": r[1],
            "resolved": bool(r[2]),
            "turns": r[3],
            "value_saved": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]
    return {
        "total_sessions": len(sessions),
        "total_value_protected": sum(s["value_saved"] for s in sessions),
        "resolved_rate": (sum(1 for s in sessions if s["resolved"]) / len(sessions)) if sessions else 0,
        "sessions": sessions,
    }
