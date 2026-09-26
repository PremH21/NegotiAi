"""
langgraph_orchestrator.py
Real LangGraph implementation of the Plan -> Act -> Observe -> Adapt loop.
This makes the deck's claim ("LangGraph manages the agent's stateful,
multi-turn decision loop end to end") literally backed by code, not just
a slide bullet.

Requires: pip install langgraph
Falls back gracefully (raises ImportError with a clear message) if not
installed -- app.py / orchestrator.py (the plain-Python version) remain
the guaranteed-safe path for your live demo.
"""

from typing import TypedDict, List, Optional
from domains import DOMAINS
from agents import NegotiationAgent, CounterpartyAgent

try:
    from langgraph.graph import StateGraph, END
except ImportError as e:
    raise ImportError(
        "langgraph is not installed. Run `pip install langgraph` to use this "
        "module. The offline-safe demo (orchestrator.py + app.py) does not "
        "require it."
    ) from e


class NegotiationState(TypedDict):
    domain_key: str
    fill_values: dict
    transcript: List[dict]
    turn: int
    max_turns: int
    resolved: bool
    neg_agent: NegotiationAgent
    cp_agent: CounterpartyAgent
    last_line: str
    last_raw_line: str


def plan_node(state: NegotiationState) -> NegotiationState:
    """PLAN: on turn 0, the negotiation agent states its opening goal."""
    if state["turn"] == 0:
        opening = state["neg_agent"].opening()
        state["transcript"].append({"speaker": "Negotiation Agent", "text": opening, "tactic": None})
        state["last_line"] = opening
    return state


def act_node(state: NegotiationState) -> NegotiationState:
    """ACT: the counterparty agent reacts to the last line (its escalation ladder)."""
    cp_result = state["cp_agent"].respond(state["last_line"])
    state["transcript"].append({"speaker": "Company Agent", "text": cp_result["display"], "tactic": None})
    state["last_line"] = cp_result["display"]
    state["last_raw_line"] = cp_result["raw"]
    return state


def observe_adapt_node(state: NegotiationState) -> NegotiationState:
    """OBSERVE + ADAPT: negotiation agent detects the tactic and counters it."""
    result = state["neg_agent"].respond_to(state["last_raw_line"], state["last_line"])
    state["transcript"].append({
        "speaker": "Negotiation Agent",
        "text": result["line"],
        "tactic": result["tactic"]["label"],
    })
    state["last_line"] = result["line"]
    state["turn"] += 1
    if result["tactic"]["key"] == "final_capitulation":
        state["resolved"] = True
    return state


def should_continue(state: NegotiationState) -> str:
    if state["resolved"] or state["turn"] >= state["max_turns"]:
        return END
    return "act"


def build_graph():
    graph = StateGraph(NegotiationState)
    graph.add_node("plan", plan_node)
    graph.add_node("act", act_node)
    graph.add_node("observe_adapt", observe_adapt_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "act")
    graph.add_edge("act", "observe_adapt")
    graph.add_conditional_edges("observe_adapt", should_continue, {"act": "act", END: END})

    return graph.compile()


def run_negotiation_langgraph(domain_key: str, custom_fields: dict = None):
    """Same signature/output shape as orchestrator.run_negotiation, but driven by a real LangGraph graph."""
    import random
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
    initial_state: NegotiationState = {
        "domain_key": domain_key,
        "fill_values": fill_values,
        "transcript": [],
        "turn": 0,
        "max_turns": len(domain["ladder"]),
        "resolved": False,
        "neg_agent": NegotiationAgent(goal_text),
        "cp_agent": CounterpartyAgent(domain["ladder"], fill_values),
        "last_line": "",
        "last_raw_line": "",
    }

    app_graph = build_graph()
    final_state = app_graph.invoke(initial_state)

    outcome = {
        "resolved": final_state["resolved"],
        "turns": len(final_state["transcript"]),
        "domain": domain["title"],
        "goal": goal_text,
        "estimated_value_saved": domain["est_value_saved"],
        "tactics_faced": [t["text"] for t in final_state["transcript"] if t["speaker"] == "Company Agent"],
    }
    return final_state["transcript"], outcome
