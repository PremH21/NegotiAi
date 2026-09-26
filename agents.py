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
                model="claude-haiku-4-5-20251001",
                max_tokens=120,
                temperature=0.9,
                system=system_role,
                messages=[{"role": "user", "content": instruction}],
            )
            text = resp.content[0].text.strip()
            return text if text else fallback_text
        elif LLM_MODE == "openai":
            resp = _client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=120,
                temperature=0.9,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": instruction},
                ],
            )
            text = resp.choices[0].message.content.strip()
            return text if text else fallback_text
    except Exception as e:
        import sys
        print(f"[negotiai] LLM paraphrase failed, using template fallback: {e}", file=sys.stderr)
        return fallback_text
    return fallback_text


# ---- Agents -------------------------------------------------------------

class CounterpartyAgent:
    """Simulated company retention/claims bot with an escalation ladder."""

    def __init__(self, ladder, fill_values):
        self.ladder = ladder
        self.fill_values = fill_values
        self.turn = 0

    def respond(self, negotiation_agent_line: str) -> dict:
        if self.turn >= len(self.ladder):
            self.turn = len(self.ladder) - 1
        template = self.ladder[self.turn]
        raw_line = template.format(**self.fill_values)
        self.turn += 1

        display_line = _llm_paraphrase(
            system_role="You role-play a company retention/claims call-center bot handling a "
                        "real customer dispute. Respond in your own natural words with a distinct "
                        "personality for this conversation — vary your phrasing, tone, and sentence "
                        "structure each time. You MUST keep every number, amount, and currency symbol "
                        "exactly as given, and keep the core offer/decision unchanged. 1-2 sentences.",
            instruction=f"The customer just said: \"{negotiation_agent_line}\"\n\n"
                        f"Respond in character with this exact substance (reword naturally, keep all numbers exact): {raw_line}",
            fallback_text=raw_line,
        )
        return {"raw": raw_line, "display": display_line}


class NegotiationAgent:
    """Acts on the user's behalf: Plan -> Act -> Observe -> Adapt."""

    DISCLOSURE = "(This is an AI agent negotiating on your behalf.) "

    def __init__(self, goal_text: str):
        self.goal_text = goal_text
        self.turn = 0

    def opening(self) -> str:
        self.turn += 1
        return self.DISCLOSURE + self.goal_text

    def respond_to(self, counterparty_raw_line: str, counterparty_display_line: str) -> dict:
        """Observe the counterparty's (raw) line, detect tactic, adapt, and act."""
        tactic = detect_tactic(counterparty_raw_line)
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
            system_role="You role-play a calm, sharp consumer-advocacy negotiation AI representing "
                        "a customer. You've just detected the company used a "
                        f"'{tactic['label']}' tactic. Respond firmly and naturally in your own words — "
                        "vary your phrasing each time, you may briefly name the tactic you noticed or "
                        "reference your consumer rights if it fits naturally. Stay polite but unyielding. "
                        "1-2 sentences, under 35 words.",
            instruction=f"The company just said: \"{counterparty_display_line}\"\n\n"
                        f"Respond in character with this exact substance (reword naturally): {fallback}",
            fallback_text=fallback,
        )
        return {"line": line, "tactic": tactic, "strategy": strategy}
