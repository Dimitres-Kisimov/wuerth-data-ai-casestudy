# Areas for improvement — what a real Würth deployment would additionally require

> **DISCLAIMER.** Independent, **public-info-only** analysis, **not affiliated with Würth**, **no internal Würth data/systems used**. My portfolio metrics are on **synthetic data**. This document is deliberately about the *gap* between a synthetic demo and a production deployment.

**This is a living document.** I don't think a portfolio built on synthetic data is "done" — it's the *starting evidence*. Below is an honest list of everything a real deployment at a company like Würth would need beyond what I've shown, and how I'd approach each. I'd expect this list to grow during an internship, not shrink to zero.

---

## 1. Real data integration (the biggest gap)

- **The gap.** Every number in my portfolio is on synthetic data I generated. Real ERP/CRM/e-procurement data has messy joins, missing values, historical policy changes, and distribution shift my synthetic generators don't capture.
- **How I'd approach it.** Start read-only: profile a real (governed, permissioned) sample, re-establish baselines, and *re-measure every metric* before claiming anything. Treat the synthetic numbers purely as method proof, and expect the real ones to differ.

## 2. Security, privacy & GDPR

- **The gap.** My repos have no auth, no data-governance layer, no PII handling — fine for a synthetic demo, unacceptable in production, especially under EU **GDPR**.
- **How I'd approach it.** Data minimisation, role-based access, pseudonymisation of customer identifiers, clear data-retention rules, and keeping models/automation inside approved infrastructure. Follow the company's security review rather than inventing my own.

## 3. MLOps & reproducibility

- **The gap.** Demos run once on my machine. Production needs versioned data, versioned models, monitoring for drift, retraining triggers, rollback.
- **How I'd approach it.** Pipeline the training/scoring, track experiments and data versions, add drift and performance monitoring, and define a retraining cadence with alerting when a metric like forecast MASE degrades.

## 4. Scale

- **The gap.** A catalogue in the millions of articles and very high transaction volume is far past my synthetic set sizes. MILP and CP-SAT can get slow; forecasting per-SKU explodes.
- **How I'd approach it.** Hierarchical/segmented modelling (long-tail vs. core), approximate/decomposed optimization with the exact solver kept for tractable sub-problems, and honest measurement of runtime vs. quality trade-offs.

## 5. Human-in-the-loop for agentic automation

- **The gap.** Autonomous agents acting on RFQs/orders/invoices can make expensive mistakes. My automation demos assume the happy path.
- **How I'd approach it.** Confidence thresholds with human review for low-confidence or high-value cases, full audit logging of every agent action, safe-by-default (propose, not commit), and staged rollout starting with suggestions only.

## 6. Validation on real distributions

- **The gap.** A ROC-AUC of 0.99 or MASE of 0.38 on synthetic data is *not* evidence of real-world performance — synthetic data can be too clean/separable.
- **How I'd approach it.** Proper backtesting on real history, out-of-time validation, calibration checks, and comparison against the *current* process (not just a naive baseline) before any go-live decision.

## 7. Integration with existing systems (ORSY, ERP, EDI)

- **The gap.** Public info tells me Würth runs ORSY inventory systems and e-procurement/EDI, but I have no access to their APIs or schemas, so my connectors are generic.
- **How I'd approach it.** Build against real interface specs once available, respect existing data contracts, and prefer augmenting existing systems over replacing them.

## 8. Business validation & change management

- **The gap.** A modelled €-uplift is not realised value. Real value needs stakeholder buy-in, controlled A/B or phased rollout, and measurement of *actual* outcomes.
- **How I'd approach it.** Co-define success metrics with the business owner up front, run controlled pilots, and report realised (not modelled) impact honestly — including when it underperforms the demo.

## 9. Robustness, testing & edge cases

- **The gap.** Portfolio test coverage is demonstration-grade. Production needs adversarial inputs, malformed documents, and failure-mode handling.
- **How I'd approach it.** Expand test suites toward real edge cases, add input validation and graceful degradation, and treat "what happens when the model/agent is wrong" as a first-class design question.

## 10. Cost, sustainability & maintainability

- **The gap.** I haven't accounted for compute cost, energy, or long-term maintenance ownership.
- **How I'd approach it.** Prefer small/efficient models where they suffice (see `bio-efficient-ai` and `ml-models-lab` for that mindset), measure cost per decision, and document handover so the work outlives my internship.

---

### Summary

The honest one-line version: **my portfolio proves I can build and measure the methods; it does not prove they work on Würth's real data yet.** Closing that gap — data, governance, MLOps, scale, human oversight, real validation — is exactly what I'd want to spend an internship doing, and I'd keep this document updated as I learned.
