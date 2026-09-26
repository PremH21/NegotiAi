# HANDOFF — Read This First (for a new Claude session or new team member)

If you are a fresh Claude session being asked to continue this project:
**read this file completely before writing or changing anything.** It tells
you what's real, what's tested, what's aspirational, and what NOT to touch
without asking first. If you are a human teammate picking this up, same
advice applies.

---

## What this project is, in one paragraph

NegotiAI is an autonomous negotiation agent for TSM TECHNOVA 2026 (National
AI Innovation Challenge), built by Team Kindralis. It negotiates on a
consumer's behalf against company retention/claims bots (subscription
cancellations, billing disputes, insurance claims), detecting the
counterparty's tactic each turn and adapting its counter-strategy. The team
reached the **National Grand Finale** using this prototype.

## Current status (update this line when you make major changes)

**Last known state: fully working prototype, tested end to end on the
author's own MacBook, used as the live demo at the Zonal Evaluation. Grand
Finale prep in progress. ML dataset expanded from 117 to 215 examples and
the classifier pipeline was tuned via GridSearchCV (cross-validation only,
no test-set leakage) — now 78.6% CV / 79.6% held-out, up from 73.5%/73.3%.
`langgraph_orchestrator.py` has now been genuinely installed and executed
(previously it was untested) — 19/19 tests passing, 15/15 stress-test runs
resolved across all 3 domains. See `ML_CLASSIFIER.md` for the honest
before/after and the weakest-class caveat (`delay_tactic`, 33% recall). The
deck's Slide 4 still describes Ollama/Llama/LangGraph-as-primary-loop
inaccurately — needs a rewrite to match this table before presenting.**

## What is REAL and TESTED — do not casually rewrite these

| File | What it does | Verified how |
|---|---|---|
| `tactics.py` | Rule-based tactic detection + counter-strategy | `test_engine.py` — 100% of counterparty lines classified correctly across all domains |
| `domains.py` | Escalation ladders per negotiation domain | Tested for required shape + domain-injection test |
| `agents.py` | NegotiationAgent + CounterpartyAgent, safe LLM fallback | Ran live on author's machine, LLM fallback confirmed working with no key set |
| `orchestrator.py` | Plan→Act→Observe→Adapt loop | All 3 domains reach resolved outcome, confirmed live |
| `backend/main.py` | FastAPI + SQLite REST API | Health check, domain list, and full negotiation run all confirmed working live via browser |
| `frontend/index.html` | Web UI | Confirmed working live — screenshot evidence exists of a full negotiation run with correct tactic badges |
| `app.py` | Streamlit fallback demo | Confirmed working live — screenshot evidence of a successful run |
| `langgraph_orchestrator.py` | Real LangGraph implementation of the Plan→Act→Observe→Adapt loop | **Now actually installed and run** — 19/19 tests passing including 2 dedicated LangGraph tests; 15/15 stress-test runs resolved across all 3 domains. Previously flagged as untested; that gap is closed |
| `ml_classifier.py` + `tactic_training_data.py` | Real trained TF-IDF+LogReg classifier | Cross-validated accuracy genuinely computed: **78.6% (± 3.7%)** CV / **79.6%** held-out, on 215 synthetic examples across 9 balanced classes — NOT yet validated on real transcripts |

## What is NOT yet verified — say so honestly if asked

- **Deployment** (Render/GitHub Pages/Netlify, per `DEPLOYMENT.md`) has
  **not been executed** — the files (`render.yaml`, deploy instructions)
  are prepared but no live public URL has been confirmed working yet.
- **The ML classifier's training data is synthetic** (hand-written by the
  team), not real negotiation transcripts. The 78.6%/79.6% figures are real
  and reproducible, but say nothing about real-world accuracy yet. One
  class (`delay_tactic`) is a known weak point at 33% recall — don't quietly
  drop this caveat if you regenerate the numbers again.
- **No real user research has been conducted** as of this writing — this is
  flagged as the biggest gap in `GRAND_FINALE_PREP.md` criterion #2.
- **The deck (slide 4) describes Ollama/Llama/Mistral running locally.**
  This is NOT what's implemented — the actual LLM path is Anthropic/OpenAI
  cloud APIs with automatic offline fallback (see `agents.py`). Fix the
  slide to match the code before presenting; do not attempt to actually
  swap in Ollama under time pressure just to match the slide — it's the
  slide that's wrong, not the code.

## Key design decisions — and why, so you don't accidentally reverse them

1. **Offline-first, LLM-optional.** The negotiation logic never depends on
   an LLM call succeeding. This was a deliberate reliability choice for live
   demos, not a limitation to "fix" by making the LLM mandatory.
2. **Rule-based core stays as the safety net even after adding ML.** The
   hybrid classifier (`ml_classifier.py`) falls back to `tactics.py` on low
   confidence — do not remove the fallback to "simplify" the code.
3. **Vanilla HTML/CSS/JS frontend, no Node/npm.** This was chosen
   specifically to remove build-step risk before a live demo. Don't port to
   React unless explicitly asked — see `MASTER_BUILD_PROMPT.md` for the
   full reasoning if someone wants that later.
4. **Success-fee capped at ₹500/negotiation, family plan capped at 5
   members.** These caps exist specifically so the pricing model can't be
   read as exploitative — don't remove them to "increase revenue" without
   understanding this was a deliberate ethical design choice tied to
   Grand Finale criterion #8 (Responsible AI).

## If you're asked to pick up work, here are concrete next steps in priority order

1. **Conduct the lightweight user survey** described in
   `GRAND_FINALE_PREP.md` criterion #2 — even 10-15 informal responses closes
   the single biggest evaluation gap identified so far. This is the highest
   remaining priority: everything else (LangGraph, ML tuning) is now done.
2. **Execute the deployment steps in `DEPLOYMENT.md`** and get one real,
   confirmed-working public URL — then update this file with the actual
   URL and remove the "not executed" caveat above.
3. **Fix Slide 4 of the deck** to match this file's table (deterministic
   core + hybrid ML + optional cloud LLM fallback + a genuinely-run
   LangGraph implementation) instead of the current Ollama/Llama framing,
   which the code does not support.
4. **If time allows**, collect a small number of real (anonymized, consented)
   negotiation-style transcripts and retrain `ml_classifier.py` on them
   instead of synthetic data — update `ML_CLASSIFIER.md`'s honesty section
   with the new, real-data accuracy number.

## Ground rules for whoever (or whichever Claude session) picks this up

- **Never inflate a number that hasn't been computed.** Every accuracy,
  cost, or performance figure in this repo was either genuinely run and
  measured, or explicitly marked as a projection/roadmap item. Keep that
  discipline — it is the single thing this project has been most careful
  about, and it is a stated jury-scoring criterion (see
  `GRAND_FINALE_PREP.md`'s closing section).
- **Run `python3 test_engine.py` before and after any change** to the core
  engine files. If a test that used to pass starts failing, that's a
  regression to fix, not a test to delete.
- **Update this file's "Current status" line** before ending your session,
  so the next person (or next Claude session) doesn't have to reconstruct
  what happened by reading git history.
