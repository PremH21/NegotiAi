import time
import streamlit as st
from domains import DOMAINS
from orchestrator import run_negotiation

st.set_page_config(page_title="NegotiAI — Live Demo", page_icon="🤝", layout="centered")

# ---- Theme (matches deck: navy bg, orange accent) ----------------------
st.markdown("""
<style>
.stApp { background-color: #0d1224; color: #e8e8f0; }
.bubble-user { background:#e8a23a; color:#1a1a2e; padding:12px 16px; border-radius:12px;
    margin:8px 0; max-width:80%; font-weight:500; }
.bubble-cp { background:#e8615a; color:white; padding:12px 16px; border-radius:12px;
    margin:8px 0 8px auto; max-width:80%; text-align:right; }
.tactic-badge { display:inline-block; background:#1e2440; color:#e8a23a; font-size:11px;
    padding:2px 8px; border-radius:10px; margin-top:4px; }
.outcome-card { background:#e8a23a; color:#1a1a2e; padding:20px; border-radius:10px; margin-top:16px; }
</style>
""", unsafe_allow_html=True)

st.title("🤝 NegotiAI")
st.caption("Autonomous Agent-to-Agent Negotiation — Live Demo | Team Kindralis")

with st.sidebar:
    st.header("Setup")
    domain_key = st.selectbox(
        "Negotiation domain",
        options=list(DOMAINS.keys()),
        format_func=lambda k: DOMAINS[k]["title"],
    )
    st.divider()
    from agents import LLM_MODE
    if LLM_MODE:
        st.success(f"LLM enhancement: ON ({LLM_MODE})")
    else:
        st.info("LLM enhancement: OFF — running fully offline, zero-cost engine.")
    st.caption("Set ANTHROPIC_API_KEY or OPENAI_API_KEY as an env var to enable natural-language mode.")
    run_btn = st.button("▶ Run Negotiation", use_container_width=True)

if run_btn:
    transcript, outcome = run_negotiation(domain_key)
    st.subheader(f"Goal: {outcome['goal']}")

    placeholder = st.container()
    for turn in transcript:
        with placeholder:
            if turn["speaker"] == "Negotiation Agent":
                st.markdown(f'<div class="bubble-user"><b>Negotiation Agent</b><br>{turn["text"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bubble-cp"><b>Company Agent</b><br>{turn["text"]}</div>',
                            unsafe_allow_html=True)
            if turn.get("tactic"):
                st.markdown(f'<span class="tactic-badge">⚡ Tactic countered: {turn["tactic"]}</span>',
                            unsafe_allow_html=True)
        time.sleep(0.5)

    st.markdown(f"""
    <div class="outcome-card">
    <h4>✅ Outcome</h4>
    <b>Status:</b> {"Goal achieved" if outcome["resolved"] else "Best achievable outcome reached"}<br>
    <b>Turns taken:</b> {outcome["turns"]}<br>
    <b>Estimated value protected:</b> ₹{outcome["estimated_value_saved"]}<br>
    <b>Domain:</b> {outcome["domain"]}
    </div>
    """, unsafe_allow_html=True)

    transcript_text = "\n".join(f"{t['speaker']}: {t['text']}" for t in transcript)
    st.download_button("⬇ Download transcript", transcript_text, file_name="negotiai_transcript.txt")
else:
    st.info("Pick a domain in the sidebar and click **Run Negotiation** to see NegotiAI in action.")
    st.markdown("""
    **What judges will see:**
    - Live multi-turn negotiation (Plan → Act → Observe → Adapt)
    - Real-time tactic detection & counter-strategy labels
    - Domain-agnostic engine (try switching domains — same engine, no retraining)
    - Auto-generated outcome report with estimated value protected
    """)
