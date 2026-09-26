# NegotiAI — TSM TECHNOVA 2026 Grand Finale Prep
**Team Kindralis** — this document exists because the Grand Finale rubric is
materially different from the zonal round: GTM/business strategy is now
criterion #10 with equal weight to your prototype, not a nice-to-have. Read
this alongside README.md (technical) — this one is the business/strategy
layer the jury is now explicitly asking for.

---

## The narrative arc the jury wants to see

> Problem → Evidence → Solution → AI Application → Prototype → Validation →
> Impact → Commercialisation → Team Capability

Structure your 10-12 minutes around this spine, not around your slide deck's
original order. Suggested pacing for a 12-minute demo slot:

| Time | Beat | What to show |
|---|---|---|
| 0:00-1:30 | Problem + Evidence | The AI-vs-AI imbalance, made concrete with a real number (see "Evidence" below) |
| 1:30-2:30 | Solution + Why AI | One sentence each — don't over-explain before showing it |
| 2:30-8:30 | Live prototype | Run 2 domains, switch live, point out tactic badges as they appear |
| 8:30-10:30 | Validation + Impact | Your 14 passing tests, the numbers, who benefits |
| 10:30-12:00 | Business + Roadmap | GTM slide, 12-month plan, close |

---

## Criterion-by-criterion: what to say, and where you're weakest

### 1. Problem Identification & National Relevance — strong, sharpen the evidence
Say: subscription commerce, EMI/BNPL, and insurance dispute volume in India
are large and growing categories; every one of them involves an automated
retention or claims-handling layer on the company side today. Don't state a
market-size number you can't defend — instead cite the **pattern**: mention
that consumer complaint volume with telecom/OTT/insurance ombudsman bodies in
India has been rising year over year (a verifiable, searchable public fact,
not an invented statistic) as your evidence anchor, rather than a number you'd
struggle to source if asked "where did you get that?"

### 2. User Understanding & Problem Validation — your genuine gap, fix this first
The rubric explicitly says "user interviews, survey insights... move beyond
assumptions." If you haven't done this yet, do a **lightweight version
tonight or tomorrow**: message 10-15 people (classmates, family, friends) one
question — *"Have you ever tried to cancel a subscription or dispute a
charge and been given the runaround? What happened?"* Collect even 8-10
real responses. This becomes a slide: *"We surveyed 12 people — 9 had been
offered a retention discount when trying to cancel; none felt equipped to
push back."* A jury cannot fault you for a small informal survey the way
they can fault you for having none at all — the criterion rewards *evidence
of the practice*, not sample size.

### 3. Solution Concept & Innovation — strong, already well-argued
Your innovation-comparison slide (complaint templates / review sites /
generic chatbots vs. NegotiAI) already does this well. Keep it.

### 4. Relevance & Depth of AI Application — the sharpest new scrutiny point
The jury will explicitly ask **"why can't this be simple automation or an
API call?"** Your answer, rehearsed word-for-word:

> "A rules-only bot can't handle a counterparty that adapts — it would need
> a pre-written response for every possible thing the company bot says. What
> makes this AI, not automation, is that the agent has to *interpret* an
> open-ended reply it's never seen phrased that exact way before, classify
> which tactic it represents, and select a counter-strategy — that's a
> reasoning task, not a lookup table. Our core tactic-engine is deterministic
> by design for auditability, but the paraphrasing layer is genuinely
> generative, and the roadmap item — reading a *real* company chatbot's
> live, unscripted responses — is exactly where the reasoning has to
> generalize beyond anything we hand-wrote."

Be honest about where you are: today's tactic-classifier is rule-based
pattern matching (auditable, explainable — a genuine strength for criterion
8), with LLM-generated language on top. If pushed on "is the classification
itself AI," the honest answer is: *"today it's deterministic by design, for
auditability; a learned classifier is the natural next step once we have
real conversation data to train on — and we chose deterministic first
specifically so behavior is explainable, which matters for criterion 8."*
Don't claim more than what's built — a jury that catches an oversold claim
scores every other answer more skeptically afterward.

### 5. Technical Feasibility & Architecture — strong, you have real proof
You have: a working FastAPI backend, SQLite persistence, a tested engine,
and a LangGraph implementation in the repo. Lead with **"deployed and
working, not a mockup"** — offer the GitHub link unprompted if there's a lull
in Q&A.

### 6. Prototype / PoC & Demonstration — your strongest category
Live demo across domains, tactic badges, step ticker, outcome card, confetti.
Nothing to add here except: **rehearse the live switch between two domains
without narrating every click** — smoothness reads as competence.

### 7. Testing, Accuracy & Performance Evidence — now provably strong
This criterion literally asks for what `test_engine.py` gives you. Say:
*"We have an automated test suite — 14 tests, all passing — covering
tactic-detection accuracy across every domain, response time under load,
and a specific test that proves domain-agnosticism by injecting a brand-new
negotiation domain at runtime with zero code changes."* Offer to show the
test run live if asked — 3 milliseconds, it will not embarrass you.

### 8. Responsible AI, Privacy, Security, Inclusiveness — prepared, say it plainly
- Every negotiation opens with an explicit AI disclosure (enforced by a test)
- Never handles account credentials — operates only on the negotiation
  transcript
- Deterministic core logic is auditable/explainable by design (this is your
  answer to "bias management" — a rule-based classifier's failure modes are
  inspectable line-by-line, unlike an opaque model)
- Runs fully local/offline by default — no consumer data leaves the device
  unless the optional cloud LLM layer is explicitly turned on
- **Inclusiveness gap to name honestly**: currently English-only. Say so,
  and say it's a scoped roadmap item (multi-language support via the same
  swappable LLM layer) rather than pretending it's already solved.

### 9. Impact, Scalability & Sustainability — good bones, needs one more layer
Add a **non-financial impact angle** beyond money recovered: time saved (a
negotiation that takes a person 20-40 minutes on hold happens in seconds),
and accessibility for people who find phone negotiation itself stressful or
difficult (elderly users, non-native speakers, people with social anxiety —
frame carefully, as a benefit, not a diagnosis of any user group).

### 10. Business Model, Adoption & Competitive Advantage — build this now, see GTM section below

### 11. Presentation & Team Capability — logistics, not content
Assign one person per failure mode during Q&A: one person answers technical
questions, one answers business questions, so no one is visibly guessing
outside their area. Decide this now, not on stage.

---

## Go-To-Market strategy — answer every bullet the email lists

**Who is the target user/customer?**
Primary: individual consumers in India who hold subscriptions, EMI/BNPL
accounts, or insurance policies and want to cancel/dispute/renegotiate but
find the process adversarial or time-consuming. First segment to target:
**urban, digitally-active 22-35 year-olds** who already manage most
finances via apps — highest willingness to try a new tool, easiest to reach
online, and the segment most likely to already be frustrated by OTT/EMI
retention tactics specifically.

**What problem are you solving for them?**
Time, confidence, and negotiation leverage they don't otherwise have against
a company's automated retention system.

**Why will they adopt your solution?**
No cost unless it works (see revenue model), no behavior change required
(they already message support today — this just does it for them), and a
visible, auditable transcript of what was said on their behalf (builds
trust that a black-box tool wouldn't).

**Who will pay for your solution?**
Two-sided, be ready to explain both:
- **Consumer-paid, success-fee model** (your strongest, most defensible
  answer): 10-15% of the value recovered or protected, zero fee if the
  negotiation doesn't succeed. This directly answers "how will you make
  money without exploiting the same users you're protecting" — you only get
  paid when they win.
- **B2B2C, later stage**: license the engine as an embedded feature to a
  fintech app, bill-tracking app, or bank app (e.g., an app that already
  tracks a user's subscriptions could add a "negotiate this for me" button).
  This is the scaling path, not the launch path — say so explicitly, don't
  present it as day-one.

**How will you reach your users?**
Launch path, in order:
1. **College and young-professional communities first** — exactly the
   audience in the room at TECHNOVA, and the easiest to reach through
   existing student/alumni networks and word of mouth from a working
   product they can try immediately.
2. **Content-led acquisition** — the negotiation transcripts themselves are
   shareable proof ("AI saved me ₹1200 on my subscription cancellation") —
   this is organic, low-cost distribution that doesn't require ad spend.
3. **Partnership channel later** — consumer-rights NGOs, personal-finance
   influencers/communities, as trust-building distribution once there's a
   track record.

**How will your solution scale beyond the pilot stage?**
Technically: the domain-agnostic architecture already proves this (new
domain = new dict entry, not a retrain — you have a passing test for this
exact claim). Commercially: each new domain (bill disputes → insurance →
travel refunds → e-commerce returns) is a new addressable market using the
same core engine, which keeps marginal engineering cost low as you scale.

---

## Rehearsed answers — "Be Ready for Jury Questions" list

**"What makes your solution different from existing solutions?"**
*"Existing tools are passive — templates and review sites inform or vent,
they never act. Generic chatbots draft a message for you to send yourself.
NegotiAI is the only one of these that autonomously conducts the entire
multi-turn negotiation and delivers a final outcome, not just a draft."*

**"What happens if your AI model fails?"**
*"Two separate answers, because we split the risk deliberately. If the
paraphrasing layer fails — bad API key, no internet, timeout — it silently
falls back to a plain-template response with identical meaning, so the
negotiation never breaks. If the negotiation itself can't reach the user's
full goal — the company won't budge past a certain point — the agent reports
'best achievable outcome' honestly rather than pretending success. It never
fails silently or lies about the result."*

**"What data is required?"**
*"None from the user beyond their goal and account-level details they'd
type into any support chat anyway — we never touch login credentials. On
the training/tuning side, the tactic-detection library is currently
hand-authored from common, publicly-documented retention tactics; the next
step is aggregating anonymized negotiation transcripts (with consent) to
refine it."*

**"How accurate is your solution?"**
*"Our test suite verifies 100% of counterparty lines across every current
domain are correctly classified — that's not an accuracy percentage in the
ML-benchmark sense, since the classifier is currently rule-based, but it is
a concrete, testable correctness claim we can show you running live in
under a second."* (Don't invent an ML accuracy percentage for a system
that isn't a trained classifier yet — a jury member who knows ML will ask
what the number is measuring, and an invented figure is the single fastest
way to lose credibility with a technical judge.)

**"What is your implementation cost?"**
*"Near-zero marginal cost per negotiation when running the offline/local
model path — our own live demo tonight cost nothing to run. Infrastructure
cost at scale is a standard web-hosting cost (FastAPI + Postgres), which
is small relative to the value protected per negotiation."*

**"Who are your competitors?"**
*"Indirectly: complaint-template sites, review platforms, and generic
customer-service chatbots — none of which act autonomously or complete a
negotiation end-to-end, which is the gap we're addressing directly."* Don't
claim zero competitors — claim a clear, specific gap versus named categories.

**"How will you acquire your first 1,000 users?"**
*"Student and young-professional networks first — the highest-frustration,
highest-tech-comfort segment — supported by organic sharing of negotiation
outcomes, which double as word-of-mouth proof."*

**"What is your roadmap for the next 12 months?"**
Give three concrete phases (matches your existing roadmap slide — reuse it):
1. **Months 1-3**: Real-world integration — connect the engine to actual
   chat widgets via browser automation, pilot with a small group of real
   users on the subscription-cancellation use case specifically.
2. **Months 4-8**: Expand to bill disputes and insurance claims with real
   users; begin the success-fee monetization pilot.
3. **Months 9-12**: B2B2C conversations with one fintech/bill-tracking
   partner; multi-language support.

---

## The one thing that separates a good Grand Finale team from a winning one

Every team at this stage will have *a* prototype and *a* business slide.
What's harder to fake, and what the rubric is visibly designed to surface,
is **knowing the difference between what you've proven and what you're
projecting** — say "our test suite proves X" where you have a test, and
"our plan is to validate Y in the next pilot" where you don't, in the same
breath, without either overclaiming or undercutting your own strengths. That
calibration is what "Team Capability" (#11) is actually scoring, more than
confidence alone.
