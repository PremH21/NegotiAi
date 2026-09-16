"""
orchestrator.py
Runs the full multi-turn negotiation loop (Plan -> Act -> Observe -> Adapt)
between NegotiationAgent and CounterpartyAgent, and produces a transcript
plus an outcome report.
"""

import random
from domains import DOMAINS
from agents import NegotiationAgent, CounterpartyAgent


def run_negotiation(domain_key: str, custom_fields: dict = None):
    domain = DOMAINS[domain_key]
    fill_values = {
        "service": "streaming",
        "discount": random.choice([30, 40, 50]),
        "fee": random.choice([299, 499, 699]),
        "overcharge": random.choice([450, 650, 900]),
        "claim_amount": random.choice([12000, 18000, 25000]),
    }
    if custom_fields:
        fill_values.update(custom_fields)

    goal_text = domain["user_goal"].format(**fill_values)
    neg_agent = NegotiationAgent(goal_text)
    cp_agent = CounterpartyAgent(domain["ladder"], fill_values)

    transcript = []

    opening = neg_agent.opening()
    transcript.append({"speaker": "Negotiation Agent", "text": opening, "tactic": None})

    last_line = opening
    resolved = False
    for _ in range(len(domain["ladder"])):
        cp_line = cp_agent.respond(last_line)
        transcript.append({"speaker": "Company Agent", "text": cp_line, "tactic": None})

        result = neg_agent.respond_to(cp_line)
        transcript.append({
            "speaker": "Negotiation Agent",
            "text": result["line"],
            "tactic": result["tactic"]["label"],
        })
        last_line = result["line"]

        if result["tactic"]["key"] == "final_capitulation":
            resolved = True
            break

    outcome = {
        "resolved": resolved,
        "turns": len(transcript),
        "domain": domain["title"],
        "goal": goal_text,
        "estimated_value_saved": domain["est_value_saved"],
        "tactics_faced": [t["text"] for t in transcript if t["speaker"] == "Company Agent"],
    }
    return transcript, outcome
