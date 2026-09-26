# The ML Tactic Classifier — what it is, honestly

This answers a direct question a technical judge is likely to ask: *"is
there real machine learning in here, or is it all rule-based?"*

## What's actually built

`ml_classifier.py` is a **real, trained model** — TF-IDF vectorization +
Logistic Regression — trained on `tactic_training_data.py`, a hand-authored
dataset of **215** example counterparty lines across 9 classes (the 8
tactics plus an "unknown" negative class), balanced to roughly 19-37
examples per class.

Run it yourself and see the number, not a claim:
```bash
python3 ml_classifier.py
```

**Current honest result (215 examples, 9 classes):**
- 5-fold cross-validated accuracy: **78.6% (± 3.7%)**
- Held-out test split accuracy: **79.6%**

### How this number was reached, honestly

This went through two real, disclosable steps, in this order:

1. **Started at 117 examples, 73.5% CV accuracy.** The dataset was then
   expanded to 215 examples, rebalanced so every class has enough support
   (the earlier set had classes with as few as 9-10 examples). Expanding
   alone actually brought accuracy down slightly, to 71.2% — a real and
   informative result, not a mistake to hide: more data, more honest
   phrasing variety, and a tighter variance band (±3.5% vs ±5.7%) is a
   *more* trustworthy measurement even though the headline number dipped.
2. **Hyperparameter tuning via `GridSearchCV`, using cross-validation folds
   only** — never touching the held-out test split — found that unigrams
   (not bigrams), `sublinear_tf=True`, and `C=3.0` outperform the original
   defaults. That tuning step, done correctly, raised accuracy to 78.6% CV /
   79.6% held-out, with CV and held-out numbers close together (a good sign
   against overfitting — see `_build_pipeline()` in `ml_classifier.py` for
   the exact parameters and a comment explaining this).

**Weakest class, named honestly:** `delay_tactic` has 33% recall on the
held-out split — the model most often confuses it with escalation or
policy-defense language. This is a legitimate limitation, not a rounding
error, and is exactly the kind of gap more (ideally real) data would close.

## Say this to the jury, precisely

> "We built a real trained classifier alongside the rule-based engine —
> TF-IDF and logistic regression, five-fold cross-validated at seventy-eight
> point six percent on 215 labeled examples across nine categories. That's
> a genuinely computed, reproducible number — you can run the file yourself.
> It's not production-grade yet — the training data is synthetic, written by
> our team, not mined from real negotiation transcripts, because we don't
> have those yet. We're also upfront that one category, delay tactics, is
> our weakest at about a third recall — that's exactly the kind of gap real
> transcript data would close, and it's on our pilot roadmap."

**Do not say 95% or imply the number could reach it.** A jury member with
ML background will read a suspiciously high accuracy on ~200 self-written
examples as overfitting/memorization, not strength — see the closing
section of `GRAND_FINALE_PREP.md` on calibration being the actual thing
"Team Capability" scores.

## Why this is a hybrid, not a replacement

The system runs **`detect_tactic_hybrid()`**: the ML model's prediction is
used only when its confidence is high; below a threshold (55%), it silently
falls back to the deterministic rule-based engine (`tactics.py`) that powers
the actual live demo. This means:

- The demo you show judges stays on the **auditable, zero-risk rule-based
  path** — nothing about the live prototype changes or gets riskier.
- The ML layer is a **genuine, separately verifiable research contribution**
  you can point to and run live if a technical judge wants to see it.
- Confidence-gated fallback is itself a responsible-AI design choice worth
  naming: the system knows when to distrust its own prediction.

## What would make this production-grade (say this if asked "what's next")

1. **Real data** — replace/augment the synthetic dataset with real,
   anonymized negotiation transcripts collected during the pilot (with
   user consent), per the 12-month roadmap in `GRAND_FINALE_PREP.md`.
2. **More examples per class** — 215 examples across 9 classes (roughly
   20-37 per class) is enough to prove the pipeline works and produce a
   stable, honest number, not enough for a production accuracy claim.
   Real-world deployments typically want hundreds to thousands of labeled
   examples per class.
3. **A held-out real-world test set** — cross-validation on synthetic data
   tells you the model learned *something*; it doesn't tell you how it
   performs on a company chatbot's actual phrasing, which is the real
   validation that matters.

Naming these gaps unprompted, before a judge finds them, is itself a
stronger answer than pretending the number is higher than it is.
