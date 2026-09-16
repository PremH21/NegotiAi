# NegotiAI — Master Build Prompt
Paste the block below into Claude Code, Cursor, ChatGPT, or any coding agent,
run from inside the `negotiai/` folder you already have (with `tactics.py`,
`domains.py`, `agents.py`, `orchestrator.py`, `langgraph_orchestrator.py`,
`backend/main.py` (including `/api/health`), `frontend/index.html`, and
`app.py` already in place — do not ask it to rebuild those, only to extend
around them).

---

## ⚠️ Read this before you paste anything

Everything below `PROMPT START` is for *further* polish on a stack that is
not just built, but **confirmed working end-to-end on the author's own
machine and used as the live demo at judging**: Streamlit app tested across
all 3 domains, FastAPI backend health check returned
`{"status":"ok","llm_mode":false}`, and `frontend/index.html` ran a full
negotiation live with correct tactic badges and outcome reporting. There is
no "run it first" step left — that already happened. Everything below is
optional post-competition polish, not pre-demo setup.

---

## PROMPT START — copy everything below this line

```
You are extending an existing, fully working, end-to-end tested prototype
called NegotiAI, a consumer-negotiation AI agent. The core engine, backend,
and frontend all already exist and were verified running together on the
author's own machine (macOS, confirmed live: offline Streamlit demo working
across all 3 domains, FastAPI backend health check returning
{"status":"ok"}, and the web frontend showing live tactic badges, the
Plan/Act/Observe/Adapt step ticker, and a completed negotiation with an
outcome card) — this was used as the live demo at the TECHNOVA 2026 Online
Zonal Evaluation. Do not rewrite any of it. Your job is polish and
extension only, per the numbered requirements below.

CONTEXT — files that already exist and must NOT be modified:
- tactics.py        (tactic detection + counter-strategy library)
- domains.py         (escalation ladders per negotiation domain)
- agents.py           (NegotiationAgent + CounterpartyAgent, with optional
                       LLM paraphrasing layer that falls back safely offline)
- orchestrator.py     (plain-Python Plan->Act->Observe->Adapt loop)
- langgraph_orchestrator.py (same loop, implemented as a real LangGraph
                       StateGraph — requires `pip install langgraph`)
- backend/main.py     (FastAPI backend, SQLite persistence, endpoints:
                       POST /api/negotiate/run, GET /api/negotiate/{id},
                       GET /api/history, GET /api/domains, GET /api/health)
- frontend/index.html (working zero-build vanilla HTML/CSS/JS frontend —
                       chat bubbles, step ticker, tactic badges, confetti,
                       auto-demo mode, history dashboard — already wired
                       to the backend and verified against its real JSON
                       response shape)
- app.py              (existing Streamlit demo UI — keep this working
                       as the guaranteed fallback, do not delete it)

REQUIREMENTS — every one of these must be satisfied, because each maps
directly to a claim made in our pitch deck and must be demonstrably true
if a judge asks to see the code:

1. FRONTEND (already built in frontend/index.html — extend, don't replace)
   - It already has: chat-style bubbles in brand colors, live domain selector
     from GET /api/domains, animated turn-by-turn reveal, tactic badges per
     turn, outcome card, a Plan/Act/Observe/Adapt step ticker, an always-visible
     AI-disclosure line, confetti on success, an auto-demo mode that cycles
     all domains, and a live history dashboard.
   - Your job here is only: (a) verify it actually renders and functions
     against the real backend on my machine, fixing anything that doesn't;
     (b) optionally port it to React/Vite if I explicitly ask for that —
     do NOT do this unprompted, the vanilla version has zero build-step
     risk and that matters more than framework choice two hours before
     judging.

2. BACKEND (extend, don't replace, backend/main.py)
   - Add a WebSocket endpoint `/ws/negotiate` that streams each turn as it
     is generated (instead of waiting for the full run) so the frontend
     can animate turns from real server events rather than faking the
     delay client-side. Keep the existing REST endpoints working too.
   - Input validation for unknown domain_key (HTTP 400) already exists —
     extend test coverage rather than rewriting it.
   - `/api/health` (status + llm_mode) already exists and is already
     wired to a live indicator dot in frontend/index.html — verify it
     still works after any of your changes, don't recreate it.

3. DATABASE (already SQLite via backend/main.py — extend, don't replace)
   - Add a migration-safe schema note at the top of backend/main.py's
     init_db() describing the sessions table shape, so anyone opening
     the file understands the schema without reading the code line by
     line.
   - Do not switch to Postgres/MySQL unless I explicitly ask — SQLite
     with zero setup is the correct choice for a hackathon demo on a
     personal laptop, on both macOS and Windows.

4. AI / ML LAYER (already exists — verify and extend)
   - Confirm langgraph_orchestrator.py actually runs against a real
     `pip install langgraph` environment; fix any API mismatches against
     the currently installed LangGraph version (LangGraph's API has
     changed across versions — reconcile StateGraph/add_conditional_edges
     signatures against whatever version actually installs).
   - Wire an optional local model path via Ollama (`ollama pull llama3.1`)
     as an alternative to the existing Anthropic/OpenAI cloud paraphrase
     layer in agents.py, so the "open-source LLMs run locally via Ollama
     at zero cost" claim in the deck is literally true end-to-end, not
     just for cloud-hosted models. Keep the existing safe fallback logic
     — if Ollama isn't running, fall back to the offline template exactly
     like the cloud path does.

5. DEPLOYMENT — must work from a completely clean machine, both OSes
   MACOS:
   - Assume Homebrew is available. Provide exact commands:
     `brew install python@3.11`
     `python3.11 -m venv venv && source venv/bin/activate`
     `pip install -r requirements.txt`
     `uvicorn backend.main:app --reload --port 8000` (terminal 1)
     `cd frontend && python3 -m http.server 5500` (terminal 2)
     No Node/npm needed — the frontend is plain HTML/CSS/JS by design, to
     remove build-step risk before judging. Only introduce a Node build
     step if I explicitly ask for a React port.
   WINDOWS:
   - Assume PowerShell. Provide exact commands using `py -3.11 -m venv venv`,
     `venv\Scripts\Activate.ps1`, and note that SQLite and Streamlit both work
     natively on Windows with no extra system dependencies.
   - Note any Windows-specific gotcha (e.g. long path issues, PowerShell
     execution policy for venv activation — `Set-ExecutionPolicy` if
     needed) explicitly, don't assume it "just works."
   - Provide a one-command dev launch script for each OS (`run_dev.sh` for
     macOS, `run_dev.ps1` for Windows) that starts backend + frontend
     server together.
   - Provide free-tier deployment steps for a public URL: static frontend on
     Vercel/Netlify/GitHub Pages (it's a single static file, no build),
     backend on Render or Railway (free tier), with exact environment
     variable names needed (ANTHROPIC_API_KEY / OPENAI_API_KEY optional,
     none required for offline mode). If deployed, update the `API` constant
     at the top of frontend/index.html's script from localhost to the
     deployed backend URL.

6. TESTING — before telling me it's done
   - Run through all three domains end-to-end via frontend/index.html in an
     actual browser (not just curl) and confirm every counterparty line
     gets a non-"Unrecognized tactic" label — if any line is unrecognized,
     add a pattern to tactics.py's TACTIC_LIBRARY rather than silently
     shipping a gap.
   - Confirm the app still works with zero environment variables set (no
     API keys) — this must never break, it is the demo's safety net.
   - Confirm the health dot in the frontend header goes green within a
     few seconds of the backend starting, and correctly shows offline/red
     if the backend is stopped.
   - Confirm the History dashboard's totals match a manual count after 3
     test runs, and that the auto-demo mode can run unattended for at
     least 2 full cycles without erroring.

7. DO NOT
   - Do not remove or weaken the offline fallback anywhere in the stack.
   - Do not introduce a required paid API key anywhere in the critical
     demo path.
   - Do not change the tactic-detection or escalation-ladder logic
     without telling me — those are the parts judges may ask about
     directly and I need to be able to explain every line.

Work through requirements 1-6 in order, showing me each piece working
(with actual command output, not just "done") before moving to the next.
Stop and flag anything from section 5 (deployment) that doesn't work
identically on macOS and Windows so I can decide how to handle it.
```

## PROMPT END
