"""
agents.py
NegotiationAgent  -> acts on the user's behalf (Plan -> Act)
CounterpartyAgent -> simulates the company retention bot (Observe -> react)

Both work fully offline (deterministic templates), which guarantees the
live demo never breaks. If an LLM API key is present in the environment,
each agent will try to paraphrase its line through the LLM for more
natural language, and silently falls back to the template on any error
(timeout, no internet, bad key) -- so the demo is never at risk.
"""

import os
import random
from tactics import detect_tactic, COUNTER_STRATEGY_TEXT

# ---- Optional LLM layer -----------------------------------------------
LLM_MODE = False
_client = None

def _try_init_llm():
    """Attempt to initialize an LLM client. Never raises."""
    global LLM_MODE, _client
    try:
        if os.environ.get("ANTHROPIC_API_KEY"):
            import anthropic
            _client = anthropic.Anthropic()
            LLM_MODE = "anthropic"
        elif os.environ.get("OPENAI_API_KEY"):
            import openai
            _client = openai.OpenAI()
            LLM_MODE = "openai"
    except Exception:
        LLM_MODE = False

_try_init_llm()


def _llm_paraphrase(system_role: str, instruction: str, fallback_text: str) -> str:
    """Try to get a natural-language line from the LLM; fall back safely."""
    if not LLM_MODE:
        return fallback_text
    try:
        if LLM_MODE == "anthropic":
            resp = _client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=80,
                system=system_role,
                messages=[{"role": "user", "content": instruction}],
            )
            return resp.content[0].text.strip()
        elif LLM_MODE == "openai":
            resp = _client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=80,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": instruction},
                ],
            )
            return resp.choices[0].message.content.strip()
    except Exception:
        return fallback_text
    return fallback_text


# ---- Agents -------------------------------------------------------------

class CounterpartyAgent:
    """Simulated company retention/claims bot with an escalation ladder."""

    def __init__(self, ladder, fill_values):
        self.ladder = ladder
        self.fill_values = fill_values
        self.turn = 0

    def respond(self, negotiation_agent_line: str) -> str:
        if self.turn >= len(self.ladder):
            self.turn = len(self.ladder) - 1
        template = self.ladder[self.turn]
        line = template.format(**self.fill_values)
        self.turn += 1

        paraphrased = _llm_paraphrase(
            system_role="You role-play a company retention/claims bot. Stay in character, "
                        "keep it under 30 words, keep the same meaning and any numbers exactly.",
            instruction=f"Rewrite this line naturally, same meaning and numbers: {line}",
            fallback_text=line,
        )
        return paraphrased


class NegotiationAgent:
    """Acts on the user's behalf: Plan -> Act -> Observe -> Adapt."""

    DISCLOSURE = "(This is an AI agent negotiating on your behalf.) "

    def __init__(self, goal_text: str):
        self.goal_text = goal_text
        self.turn = 0

    def opening(self) -> str:
        self.turn += 1
        return self.DISCLOSURE + self.goal_text

    def respond_to(self, counterparty_line: str) -> dict:
        """Observe the counterparty's line, detect tactic, adapt, and act."""
        tactic = detect_tactic(counterparty_line)
        strategy = COUNTER_STRATEGY_TEXT[tactic["counter"]]

        if tactic["key"] == "final_capitulation":
            fallback = "Confirmed. Thank you — no further action needed."
        elif tactic["counter"] == "decline_and_restate":
            fallback = f"Decline. Proceed with the original request: {self.goal_text}"
        elif tactic["counter"] == "hold_firm":
            fallback = "Understood, but my position is unchanged. Please proceed as requested."
        elif tactic["counter"] == "demand_immediate_action":
            fallback = "I'd like this actioned immediately, not deferred — please confirm now."
        elif tactic["counter"] == "acknowledge_and_restate":
            fallback = f"I appreciate that, but I'd still like to proceed: {self.goal_text}"
        elif tactic["counter"] == "dispute_fee":
            fallback = "I dispute that fee — please waive it and proceed with my original request."
        else:
            fallback = f"Please proceed with the original request: {self.goal_text}"

        self.turn += 1
        line = _llm_paraphrase(
            system_role="You role-play a calm, firm consumer-advocacy negotiation AI. "
                        "Keep it under 30 words, polite but unyielding.",
            instruction=f"Rewrite this line naturally, same meaning: {fallback}",
            fallback_text=fallback,
        )
        return {"line": line, "tactic": tactic, "strategy": strategy}
