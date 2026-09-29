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

**Last known state: fully working prototype, deployed end-to-end and
verified live — backend on Render (negotiai-backend.onrender.com), frontend
on Netlify (public URL claimed, not the 1-hour temp link). Domains expanded
from 3 to 20 (see `domains.py`); a real classification-order bug was found
and fixed in `tactics.py` (a closing line could be misread as a mid-negotiation
tactic due to dict-iteration order — final_capitulation patterns are now
checked first). Frontend polish: hardcoded hackathon banner removed, health
indicator now shows a real "Rule-based engine" vs "Live LLM reasoning" badge,
per-turn thinking animation added so responses don't dump instantly. ML
dataset expanded from 117 to 215 examples and the classifier pipeline was
tuned via GridSearchCV (cross-validation only, no test-set leakage) — now
78.6% CV / 79.6% held-out, up from 73.5%/73.3%. `langgraph_orchestrator.py`
has been genuinely installed and executed — 19/19 tests passing across 20
domains. See `ML_CLASSIFIER.md` for the honest before/after and the
weakest-class caveat (`delay_tactic`, 33% recall).**

**STILL OPEN — highest priority for whoever picks this up next:**
`ANTHROPIC_API_KEY` is already set on Render, but until 2026-09-26 it was
having zero effect (see the model-name bug above) — every deployed run was
silently 100% template text. That's now fixed in code; **the fix must be
pushed and Render must be redeployed** for the live site to actually show
real LLM-generated dialogue. After confirming that live, the two remaining
items are the user survey (`GRAND_FINALE_PREP.md` criterion #2) and fixing
the deck's Slide 4, which still describes Ollama/Llama/LangGraph-as-primary-
loop inaccurately — it needs a rewrite to match this file's table.

## What is REAL and TESTED — do not casually rewrite these

| File | What it does | Verified how |
|---|---|---|
| `tactics.py` | Rule-based tactic detection + counter-strategy | `test_engine.py` — 100% of counterparty lines classified correctly across all domains |
| `domains.py` | Escalation ladders per negotiation domain | Tested for required shape + domain-injection test |
| `agents.py` | NegotiationAgent + CounterpartyAgent, safe LLM fallback | Ran live on author's machine, LLM fallback confirmed working with no key set |
| `orchestrator.py` | Plan→Act→Observe→Adapt loop | All 20 domains reach resolved outcome, confirmed live |
| `backend/main.py` | FastAPI + SQLite REST API | Health check, domain list, and full negotiation run all confirmed working live via browser |
| `frontend/index.html` | Web UI | Confirmed working live — screenshot evidence exists of a full negotiation run with correct tactic badges |
| `app.py` | Streamlit fallback demo | Confirmed working live — screenshot evidence of a successful run |
| `langgraph_orchestrator.py` | Real LangGraph implementation of the Plan→Act→Observe→Adapt loop | **Now actually installed and run** — 19/19 tests passing including 2 dedicated LangGraph tests; 15/15 stress-test runs resolved across all 3 domains. Previously flagged as untested; that gap is closed |
| `ml_classifier.py` + `tactic_training_data.py` | Real trained TF-IDF+LogReg classifier | Cross-validated accuracy genuinely computed: **78.6% (± 3.7%)** CV / **79.6%** held-out, on 215 synthetic examples across 9 balanced classes — NOT yet validated on real transcripts |

## What is NOT yet verified — say so honestly if asked

- **Deployment is done and public** (Render backend + Netlify frontend, claimed/permanent URL, not the 1-hour temp link) — this earlier caveat is resolved.
- **A real bug was found and fixed 2026-09-26: the Anthropic model string was
  invalid (`claude-sonnet-4-6`, not a real model), so every LLM paraphrase
  call was silently throwing and falling back to the raw template — meaning
  every "AI" line was word-for-word identical to the deterministic template
  even with a valid API key configured.** Fixed to a real current model
  (`claude-haiku-4-5-20251001`), added temperature for natural variation, and
  logged failures to stderr instead of swallowing them silently, so this
  class of bug is visible in Render logs next time. Also fixed a related
  correctness risk: tactic detection now runs on the raw template text
  (`respond()` returns `{"raw", "display"}`), not the LLM-paraphrased text —
  otherwise natural rewording could accidentally drop a keyword the regex
  patterns depend on and silently misclassify. If you add more LLM
  paraphrasing anywhere, keep this raw/display separation.
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

---

## UPDATE — Generative mode added (root-cause fix for "it looks templated")

**Diagnosis:** `agents.py` `_llm_paraphrase()` told the LLM to "keep this exact substance" of a
pre-written line from the fixed 4-step ladder in `domains.py`. So every domain was the same
script (discount → escalate → fee threat → concede) with reworded text. Switching LLM provider
could never fix that — the LLM never decided content.

**Fix:** new `generative_engine.py` — two LLM personas hold a real multi-turn conversation
(company bot chooses its own tactics from conversation history; negotiation agent decides its
own counter). The existing tactic detector runs on the *generated* company text (drives the
tactic badge and detects resolution). `orchestrator.py` / ladder are UNCHANGED and remain the
fallback.
- `backend/main.py`: `POST /api/negotiate/run` accepts `mode`: `auto` (default; generative if an
  LLM key is set, else deterministic), `generative`, `deterministic`. `outcome.mode` always
  reports the mode that ACTUALLY ran (falls back honestly if an API call fails mid-run).
- `frontend/index.html`: outcome card shows "Live generative AI" vs "Deterministic mode".
- `test_engine.py`: 22 tests (mocked-LLM tests cover generative path + both fallbacks).

**VERIFIED:** 22 tests pass; fallback paths; routing logic.
**NOT VERIFIED (needs a machine with internet + key):** real multi-turn calls to Gemini/Groq/
Anthropic. Provider call patterns are copied from the already-working single-shot code, but
the multi-turn flow has never hit a live API. First action for the next session: run a
negotiation with mode=generative on the deployed backend and record the result here.
**Known risk:** free-tier rate limits (a run makes up to ~16 calls). On a 429 the run falls back
to deterministic and the badge will say so. Prefer Groq (higher free limits) as primary.
**Honest limitation to state to judges:** tactic *detection* is still rule-based/ML hybrid
(76–79% CV on synthetic data); the *dialogue* is now genuinely LLM-generated.

---

## UPDATE — Generative mode: root cause found and FIXED

**Bug:** `generative_engine.py` used Groq model `llama-3.3-70b-versatile`, which no
longer exists on Groq's API (confirmed via `GET /openai/v1/models` — not in the
account's model list at all). Every call was failing with `404 model_not_found`,
silently falling back to the deterministic path for the ENTIRE negotiation. This is
why generative mode looked identical to the old scripted demo — it was quietly never
running.

**Fix applied and confirmed working via curl:**
- Model changed to `openai/gpt-oss-120b` in both `agents.py` and
  `generative_engine.py` (`sed -i '' 's/llama-3.3-70b-versatile/openai\/gpt-oss-120b/g' agents.py generative_engine.py`)
- Added `reasoning_effort="low"` to the Groq call in `generative_engine.py` — this
  model is a reasoning model that "thinks" before answering, consuming the same
  token budget as the reply itself. Without this, and without enough max_tokens,
  replies came back blank or cut off mid-word.
- Raised `max_tokens` for the Groq call: company turn 900, negotiation-agent turn 700
  (was 120/100 — far too low for a reasoning model).

**CONFIRMED via curl** (`mode:"generative"`, `bill_dispute` domain): fully natural,
non-repeating dialogue on both sides, resolved in 6 turns (vs. the fixed 9 the old
scripted ladder always took), no truncation.

**NOT YET CONFIRMED as of this note** (next session should do these, in order):
1. Sweep 3-4 more domains via curl, watch for truncated/empty replies — if any
   appear, raise max_tokens further (900/700 has headroom to go higher, it's free).
2. Test through the actual browser at localhost:5500 (hard refresh Cmd+Shift+R
   first — a stale cached frontend was mistaken for a backend bug earlier this
   session, wasted significant time). Confirm the "🧠 Live generative AI" badge
   renders on the outcome card.
3. `git add agents.py generative_engine.py && git commit -m "..." && git push`
4. Add `GROQ_API_KEY` (the real one, starts with `gsk_`, not the `AQ.`-prefixed
   Google AI Studio key that caused an earlier 401 — those got mixed up once
   already this session) to Render's Environment tab. Render auto-redeploys.
5. Test the live Netlify+Render URL end to end — that's what judges will actually see.

**Known risk to flag before demoing:** a full generative negotiation makes up to
~16 Groq API calls with reasoning overhead — meaningfully slower than the old
instant scripted version. Time a full run. If it's too slow for the demo window,
`MAX_TURNS` in `generative_engine.py` (currently 8) can be reduced to 5-6 as a
safety valve — this shortens worst-case negotiations without touching the
model/token fixes above.

**Environment gotchas hit repeatedly this session, avoid repeating them:**
- A fresh terminal tab has NO env vars and NO activated venv from other tabs.
  Always run this as ONE pasted block, every time, never split across separate
  commands: `cd ~/negotiai && source venv/bin/activate && export GROQ_API_KEY=... && uvicorn backend.main:app --port 8000`
- `Address already in use` on port 8000 means an old server is still alive in
  another tab — `lsof -ti:8000 | xargs kill -9` clears it before restarting.
- The browser aggressively caches `frontend/index.html` — after ANY frontend
  change, hard refresh (Cmd+Shift+R) before concluding something didn't work.

---

## UPDATE — Generative mode CONFIRMED working end-to-end in real browser

Tested live via http://localhost:5500 across multiple domains (gym membership,
subscription downgrade, billing dispute). Results: genuinely varied, non-repeating,
naturally-written dialogue on both sides every run. Correct tactic badges rendered
on real LLM-generated text (Discount Offer, Free Period/Bonus, Escalation to
Specialist all correctly detected). This is real, not scripted — confirmed by eye,
not just by the "mode":"generative" field.

**Minor known polish item (not blocking):** tactic detector's final_capitulation
regex doesn't yet catch natural resolution phrasings like "I've just completed the
downgrade... effective immediately" — conversation sometimes runs a couple of extra
pleasant-but-unnecessary turns after the real resolution instead of stopping
cleanly. Optional fix (safe, data-only, no restart needed):
`sed -i '' 's/r"has been cancelled", r"approved in full", r"refund", r"fully refunded"/r"has been cancelled", r"approved in full", r"refund", r"fully refunded", r"i.ve (just )?(completed|applied|processed|done)", r"effective immediately"/' tactics.py`

**REMAINING STEPS, in order, next session should do these:**
1. `git add agents.py generative_engine.py tactics.py && git commit -m "Fix Groq model to gpt-oss-120b, raise token limits, broaden resolution detection" && git push`
2. Add `GROQ_API_KEY` (the real `gsk_...` one) to Render dashboard → negotiai-backend
   → Environment tab. Render auto-redeploys on save.
3. Wait for Render redeploy to finish, then test the LIVE Netlify+Render URL
   end-to-end (not just localhost) — confirm generative mode works there too,
   since Render's environment is separate from local.
4. Time a full negotiation run — reasoning model + up to ~16 calls means this is
   slower than the old instant scripted version. If it's too slow for the demo
   slot, reduce `MAX_TURNS` in generative_engine.py from 8 to 5-6.

---
## UPDATE 30 Sep (pre-finale)
- Generative mode verified real locally (Groq gpt-oss-120b, clean logs, varied dialogue).
- Agent-side resolution check added (_agent_declares_resolution, prompt asks for
  exact sentence "The matter is resolved."). Tests: 22 pass.
- KNOWN ISSUE: company-side final_capitulation keyword check can falsely mark
  resolved when company stalls. Left as-is before demo. Cleaner fix: remove that
  block, rely on agent statement only; test 3 runs first.
- TODO: verify Render GROQ_API_KEY + live URL is generative; time a full run
  (MAX_TURNS 8 -> 6 if slow); backup video; rehearse; write pitch (11 criteria).
- Rotate Groq key after the ceremony (exposed in chat).

---

## UPDATE (Sep 30, pre-showcase) - read first

Verified locally: generative mode is real (no 401s, varied dialogue). Agent-side
resolution check applied in generative_engine.py (RESOLUTION_PHRASES,
_agent_declares_resolution); prompt asks for exact sentence "The matter is resolved."
MAX_TURNS still 8. Tests: 22 passing. Tag demo-safe = last pushed-known-good state.

Known limitation: company-side final_capitulation keyword check in tactics.py can
false-positive on stalling replies containing "confirm"/"processed" (seen in 1 of 3
runs). Cleaner fix (not applied): remove the company-side stop block in
generative_engine.py so only the agent's statement resolves; then update any tests
asserting the old behavior.

Remaining: 1) git status / push. 2) Render: valid GROQ_API_KEY, redeploy, live test,
check logs for 401. 3) Time a full live run; lower MAX_TURNS to 6 if slow.
4) Backup video, warm up Render before presenting. 5) Rotate Groq key after event.
Never present a "template fallback" run as live AI.
