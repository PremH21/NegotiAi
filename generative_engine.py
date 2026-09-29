"""
generative_engine.py
A genuinely generative negotiation mode: the LLM decides WHAT to say each
turn based on the actual conversation so far, not just how to reword a
pre-written line from a fixed ladder. This is why every domain used to
read as "the same conversation, different numbers" — agents.py's
_llm_paraphrase() was explicitly instructed to "keep this exact substance,"
so no matter the provider, the content was always the same 4-step script
in domains.py. This module removes that constraint entirely.

This is an ADDITIVE path — orchestrator.py (the deterministic engine) is
UNCHANGED and remains the guaranteed-safe fallback. This module falls back
to it automatically:
  - if no LLM provider is configured at all, or
  - if any API call fails mid-negotiation (never returns a half-broken
    transcript — bails out to the fully deterministic path instead)

HONEST CAVEAT, read this before demoing: this file was written and syntax-
checked in a sandbox with no internet access, so the actual live multi-turn
API calls have NOT been run end to end by whoever wrote this. The single-
shot call pattern it reuses (same provider branches as agents.py's
_llm_paraphrase) IS already confirmed working in production — this file
only changes how that call is used (a real conversation history instead of
a one-line reword instruction). Test this yourself with a live key before
trusting it for the finale, and update HANDOFF.md with the result either way.
"""

import os
import sys
import random
import requests

from agents import LLM_MODE, _client
from tactics import detect_tactic
from domains import DOMAINS
from orchestrator import run_negotiation as run_negotiation_deterministic

MAX_TURNS = 8

COMPANY_SYSTEM_PROMPT = """You are an AI customer-service / retention bot for a company, handling a real customer negotiation.

The customer's request: "{goal}"

You may use realistic retention/dispute-handling tactics AS A REAL COMPANY BOT WOULD — choose whichever fits the moment yourself, don't follow a fixed script:
- Offer a discount or partial credit
- Offer a free period or bonus
- Escalate to a "specialist" or "manager"
- Cite processing delays (24-48 hours, a few business days)
- Make a loyalty/goodwill appeal
- Mention a possible fee or penalty
- Cite policy or contract terms as justification
- Eventually, if the customer holds firm through several of these attempts, genuinely concede and grant their original request in full

Stay in character. 1-3 sentences per turn. Don't repeat the same tactic twice in a row. Never break character or mention you are an AI."""

NEGOTIATION_SYSTEM_PROMPT = """You are an autonomous negotiation AI representing a consumer. Your goal: "{goal}"

Rules:
- Stay calm, firm, and polite — never rude.
- Read the company's last message and push back appropriately: reject discounts or free offers that don't fully satisfy the goal, demand immediate action against delay tactics, dispute unwarranted fees, and hold your position through escalation attempts.
- If, and only if, the company's last message fully grants the original goal with no remaining conditions, accept it and clearly state the matter is resolved.
- 1-2 sentences per turn, under 40 words. Never break character."""


def _chat(system_prompt, history, max_tokens=150):
    """Multi-turn chat completion across whichever provider agents.py already
    initialized. Returns None on any failure — caller must handle fallback.
    `history` is a list of {"role": "user"|"assistant", "content": str}."""
    if not LLM_MODE:
        return None
    try:
        if LLM_MODE == "anthropic":
            resp = _client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=max_tokens,
                system=system_prompt,
                messages=history,
            )
            return resp.content[0].text.strip()

        elif LLM_MODE == "groq":
            resp = _client.chat.completions.create(
                model="openai/gpt-oss-120b",
                reasoning_effort="low",
                max_tokens=max_tokens,
                temperature=0.9,
                messages=[{"role": "system", "content": system_prompt}] + history,
            )
            return resp.choices[0].message.content.strip()

        elif LLM_MODE == "gemini":
            contents = [
                {"role": ("model" if h["role"] == "assistant" else "user"),
                 "parts": [{"text": h["content"]}]}
                for h in history
            ]
            resp = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                params={"key": os.environ["GEMINI_API_KEY"]},
                json={
                    "system_instruction": {"parts": [{"text": system_prompt}]},
                    "contents": contents,
                    "generationConfig": {"temperature": 0.9, "maxOutputTokens": max_tokens},
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        elif LLM_MODE == "openai":
            resp = _client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=max_tokens,
                temperature=0.9,
                messages=[{"role": "system", "content": system_prompt}] + history,
            )
            return resp.choices[0].message.content.strip()

    except Exception as e:
        print(f"[negotiai:generative] LLM call failed: {e}", file=sys.stderr)
        return None
    return None


def run_negotiation_generative(domain_key: str, custom_fields: dict = None):
    """Genuinely LLM-driven negotiation — content is generated turn by turn,
    not selected from a fixed ladder and reworded. Falls back to the fully
    deterministic engine (same output shape) on any failure, including no
    LLM configured at all, so the caller never has to handle two shapes."""
    if not LLM_MODE:
        return run_negotiation_deterministic(domain_key, custom_fields)

    domain = DOMAINS[domain_key]
    fill_values = {
        "service": "streaming", "discount": random.choice([30, 40, 50]),
        "fee": random.choice([299, 499, 699]), "overcharge": random.choice([450, 650, 900]),
        "claim_amount": random.choice([12000, 18000, 25000]),
    }
    if custom_fields:
        fill_values.update(custom_fields)
    goal_text = domain["user_goal"].format(**fill_values)

    company_system = COMPANY_SYSTEM_PROMPT.format(goal=goal_text)
    negotiation_system = NEGOTIATION_SYSTEM_PROMPT.format(goal=goal_text)

    transcript = []
    opening = "(This is an AI agent negotiating on your behalf.) " + goal_text
    transcript.append({"speaker": "Negotiation Agent", "text": opening, "tactic": None})

    company_history = []
    negotiation_history = []
    last_negotiation_line = opening
    resolved = False

    for _ in range(MAX_TURNS):
        company_history.append({"role": "user", "content": last_negotiation_line})
        company_reply = _chat(company_system, company_history, max_tokens=900)
        if company_reply is None:
            return run_negotiation_deterministic(domain_key, custom_fields)
        company_history.append({"role": "assistant", "content": company_reply})

        tactic = detect_tactic(company_reply)
        transcript.append({"speaker": "Company Agent", "text": company_reply, "tactic": None})

        if tactic["key"] == "final_capitulation":
            resolved = True
            break

        negotiation_history.append({"role": "user", "content": company_reply})
        negotiation_reply = _chat(negotiation_system, negotiation_history, max_tokens=700)
        if negotiation_reply is None:
            return run_negotiation_deterministic(domain_key, custom_fields)
        negotiation_history.append({"role": "assistant", "content": negotiation_reply})

        transcript.append({
            "speaker": "Negotiation Agent",
            "text": negotiation_reply,
            "tactic": tactic["label"],
        })
        last_negotiation_line = negotiation_reply

    outcome = {
        "resolved": resolved,
        "turns": len(transcript),
        "domain": domain["title"],
        "goal": goal_text,
        "estimated_value_saved": domain["est_value_saved"],
        "tactics_faced": [t["text"] for t in transcript if t["speaker"] == "Company Agent"],
        "mode": "generative",
    }
    return transcript, outcome
