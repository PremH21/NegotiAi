# NegotiAI — Business Model: Dual Revenue, Zero Harm to the User

The design constraint you asked for — **profit on both B2C and B2B sides,
without the B2B side undercutting the person NegotiAI exists to protect** —
shapes every choice below. The two revenue streams are kept structurally
separate so a B2B deal can never create an incentive to negotiate worse for
a consumer.

---

## Side 1 — B2C (individual / consumer, India-first pricing in INR)

Two models offered side by side; **the app recommends whichever is cheaper
for that user's actual usage**, shown transparently before they pay — this
one design choice is your strongest answer to "how do you avoid becoming
the same kind of exploitative business you're fighting."

### Option A — Pay-per-success (default for new users)
- **No subscription, no fee if the negotiation doesn't succeed.**
- **12% of value recovered or protected, capped at ₹500 per negotiation**
  regardless of the claim size — the cap exists specifically so a large
  insurance dispute can't produce a disproportionate fee.
- Shown to the user *before* they confirm: *"If we succeed, you pay ₹54
  (12% of ₹450). If we don't, you pay nothing."* — full transparency, no fee
  discovered after the fact.

### Option B — Subscription (for frequent users)
| Plan | Price | Who it's for |
|---|---|---|
| Individual Monthly | ₹99/month | Unlimited negotiations, no per-success fee |
| Individual Yearly | ₹899/year (~25% off monthly) | Same, discounted for annual commitment |
| Family/Group | ₹199/month or ₹1,799/year, up to 5 members | Households managing shared subscriptions, family insurance, joint accounts |

### Free tier
**First negotiation is always free**, no card required — the way to build
trust with a skeptical first-time user is to let the product prove itself
before asking for money, which also directly strengthens your GTM "why will
they adopt" answer.

### Payment methods (India-first, expandable)
Integrate a payment gateway that natively supports the full spread of how
Indians actually pay — **UPI, debit/credit cards (Visa/Mastercard/RuPay),
net banking, and wallets** — via a standard Indian payment gateway
(Razorpay or Cashfree are the common choices; either supports all of the
above out of the box, so this is a configuration choice, not new
engineering). International cards via Stripe is a natural later addition
once/if you expand beyond India — say this as roadmap, not current scope.

---

## Side 2 — B2B (the dual income side) — reframed so it's not adversarial

The naive B2B pitch — "we help consumers beat your retention bots" — is a
hard, adversarial sell to any company. The stronger, honest reframe:

### B2B Model 1 — Embedded feature licensing (fintech/neobank partners)
License the engine as a "negotiate this for me" button inside an existing
app that already tracks a user's subscriptions or bills (a bill-tracking
app, a neobank, a budgeting app). **Revenue: monthly per-active-user
licensing fee or a smaller revenue share on successful negotiations run
through their app.** The partner gets a sticky, differentiated feature;
you get distribution without owning acquisition cost.

### B2B Model 2 — Dispute-resolution-as-a-service for the companies themselves
This is the least obvious and most defensible angle: **sell the same engine
to the companies on the other side, positioned as a faster, fairer
first-line dispute resolver.** Companies face real cost from unresolved
disputes escalating to consumer courts, ombudsman bodies, or regulators —
NegotiAI-as-a-service can resolve legitimate disputes at the first contact,
reducing escalation cost and regulatory risk for the company, while the
consumer still gets a fair, fast outcome. **Revenue: enterprise licensing
fee**, priced per ticket/dispute handled.

**Why this doesn't compromise the user**: this offering only ever resolves
*legitimate* disputes fairly and fast — it is never sold as "helping you
deny more claims," and that line should never be crossed even if a
prospective B2B customer asks for it. If a judge asks about this tension,
the honest answer is: *"we'd walk away from a B2B deal that wanted the
engine to negotiate against consumers rather than for them — that's a hard
line, not a pricing decision."*

### B2B Model 3 — Subsidized access for consumer-rights NGOs and ombudsman offices
Free or heavily discounted API access for verified nonprofits and
consumer-protection bodies. Low/no revenue here, but it's the credibility
anchor for your SDG 10/16 claims — a jury can tell the difference between a
CSR slide and an actual subsidized-access line item in the business model.

---

## Why dual revenue doesn't create a conflict of interest

The two sides are kept **structurally separate**, not just described that
way:
- B2C revenue depends entirely on negotiation *success* — the incentive is
  aligned with the consumer winning.
- B2B Model 1 revenue is a flat licensing/usage fee, not tied to negotiation
  outcomes — the partner has no lever to make the engine negotiate worse.
- B2B Model 2 revenue is per-dispute-handled, not per-dispute-denied — the
  engine's job is resolution quality, not denial rate, and that's the term
  you'd insist on in any such contract.

If a jury member asks "what stops you from being paid by both sides to
work against each other," this structural separation — plus the explicit
walk-away line above — is the actual answer, not a values statement alone.

---

## Where this sits in your pitch

Use this as the answer to criterion #10 (Business Model, Adoption &
Competitive Advantage) and as backup for the "who will pay for your
solution" GTM question in `GRAND_FINALE_PREP.md`. Lead with the B2C
success-fee model in your main pitch — it's the most intuitive and
defensible; introduce the B2B angle only if asked about scaling revenue or
a jury member specifically probes monetization depth, since it's a more
nuanced argument that rewards a direct question rather than an unprompted
info-dump.
