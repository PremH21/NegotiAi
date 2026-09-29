"""
tactics.py
Detects retention/negotiation tactics used by a counterparty, and maps
each tactic to a counter-strategy. This is the "reads & counters tactics"
engine referenced in the pitch deck.
"""

import re

# Each tactic: keyword patterns to detect it + a human label + a counter move
TACTIC_LIBRARY = {
    "discount_offer": {
        "label": "Discount Offer",
        "patterns": [r"\d+%\s*off", r"discount", r"reduced rate", r"special price", r"credit", r"goodwill"],
        "counter": "decline_and_restate",
    },
    "policy_defense": {
        "label": "Policy Defense",
        "patterns": [r"valid per", r"per your plan", r"per the policy", r"terms and conditions"],
        "counter": "dispute_fee",
    },
    "free_period": {
        "label": "Free Period / Bonus",
        "patterns": [r"free month", r"free for", r"complimentary", r"on us"],
        "counter": "decline_and_restate",
    },
    "escalation": {
        "label": "Escalation to Specialist",
        "patterns": [r"specialist", r"manager", r"escalat", r"supervisor"],
        "counter": "hold_firm",
    },
    "delay_tactic": {
        "label": "Delay / Process Friction",
        "patterns": [r"24.?48 hours", r"business days", r"processing time", r"review your request"],
        "counter": "demand_immediate_action"
    },
    "guilt_trip": {
        "label": "Guilt / Loyalty Appeal",
        "patterns": [r"sorry to see you go", r"valued customer", r"loyal", r"miss you"],
        "counter": "acknowledge_and_restate",
    },
    "fee_threat": {
        "label": "Fee / Penalty Threat",
        "patterns": [r"cancellation fee", r"early termination", r"penalty", r"charge you", r"admin fee", r"incur a"],
        "counter": "dispute_fee",
    },
    "final_capitulation": {
        "label": "Final Concession",
        "patterns": [r"confirmed", r"processed", r"no further offers", r"has been cancelled",
                     r"approved in full", r"refund", r"fully refunded",
                     r"i.ve (just )?(completed|applied|processed|done)", r"effective immediately"],
        "counter": "confirm_and_close",
    },
}

COUNTER_STRATEGY_TEXT = {
    "decline_and_restate": "Decline. Restate the original goal clearly and firmly.",
    "hold_firm": "Acknowledge the escalation but hold the original position; do not soften the ask.",
    "demand_immediate_action": "Reject the delay; request immediate confirmation in writing.",
    "acknowledge_and_restate": "Acknowledge the sentiment briefly, then restate the goal without being swayed.",
    "dispute_fee": "Challenge the legitimacy of the fee and request a waiver citing terms/consumer rights.",
    "confirm_and_close": "Confirm the outcome in writing and end the negotiation.",
}


def detect_tactic(counterparty_text: str) -> dict:
    """Return the first matching tactic dict for a piece of counterparty text.

    final_capitulation is checked first: a closing line like "Confirmed, the
    penalty has been waived" would otherwise get misread as a fee_threat
    (because of the word "penalty") purely due to dict ordering. A genuine
    resolution should never be shadowed by an incidental keyword match.
    """
    text = counterparty_text.lower()

    final = TACTIC_LIBRARY["final_capitulation"]
    for pattern in final["patterns"]:
        if re.search(pattern, text):
            return {"key": "final_capitulation", "label": final["label"], "counter": final["counter"]}

    for key, tactic in TACTIC_LIBRARY.items():
        if key == "final_capitulation":
            continue
        for pattern in tactic["patterns"]:
            if re.search(pattern, text):
                return {"key": key, "label": tactic["label"], "counter": tactic["counter"]}
    return {"key": "unknown", "label": "Unrecognized tactic", "counter": "hold_firm"}
