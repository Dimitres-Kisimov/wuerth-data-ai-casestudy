# Data & AI Case Study — mapped to two Würth internship roles

> **DISCLAIMER — read this first.** This is an **independent** case study I put together on my own. It is based **only on publicly available information** about the Würth Group (company website, public press, general industry knowledge). It is **not affiliated with, endorsed by, or reviewed by Würth**, and it uses **no internal, confidential, or proprietary Würth data or systems** of any kind. Every figure attributed to Würth's scale (number of companies, employees, revenue, ORSY installations, article counts) is **public and approximate** and is labelled as such — I have not invented internal Würth numbers. Every performance number in my own portfolio is measured on **synthetic / self-generated data** unless explicitly labelled otherwise, and I say so each time it appears (the one real-data exception, `retail-analytics-real`, is measured on the public UCI Online Retail II dataset — CC BY 4.0 — and is labelled **real data** everywhere its numbers appear). The point of this repo is to show *how I think and what I can build*, not to claim results on Würth's real business.

Hi — I'm Dimitres. I built this repository to answer one question honestly: *if I did a Data & AI internship at Würth, what could I actually contribute, and where's the evidence?*

I applied to two postings and this case study speaks to both:

- **Job #1 — Praktikum Data & AI: (Agentic) Automation mit Low-code Plattformen.** Building AI-agent workflows, low-code automation (n8n, Power Automate), connecting systems and APIs, rapid prototyping.
- **Job #2 — Praktikum Data & AI Analytics.** BI and Power BI, KPI dashboards, forecasting / predictive analytics, Python and SQL, data modelling, turning data into business decisions.

Rather than assert skills, I mapped each requirement to something I've already **built and measured** in my existing portfolio. The three documents in [`docs/`](docs/) are the substance; this README is the orientation.

---

## Who Würth is (public profile)

The Würth Group is a large, family-owned German-headquartered group in **assembly and fastening materials** and industrial **MRO** (maintenance, repair, operations) distribution. From public sources, at a high level and approximately:

- **~400+ operating companies** across **80+ countries** (public, approximate).
- On the order of **~87,000 employees** and **~€20B+ annual group revenue** (public, approximate — figures vary by year and reporting).
- A catalogue in the **millions of articles** — screws, fasteners, tools, chemicals, consumables (public, approximate).
- A deliberately **multi-channel** go-to-market: a large **field sales** force, physical **branches / trade outlets**, **e-commerce** shops, and **e-procurement / EDI** integrations into customer systems.
- The **ORSY** family of inventory and shelf-management systems (bins, racks, scanners, vending/automated replenishment) installed across many customer sites (public; exact counts approximate).

None of that is my data — it's the public picture of a distribution business that runs on **assortment, pricing, availability, logistics, and a very high volume of transactional documents and orders**. That combination is almost a textbook case for applied Data & AI.

## Why Data & AI matters in a business like this

A distributor at this scale lives or dies on a handful of quantitative levers, each of which is a place where analytics and automation pay for themselves:

- **Assortment** — which of millions of articles to stock, where. Wrong long-tail decisions tie up cash or lose sales.
- **Pricing & margin** — elasticity-aware pricing and discount discipline; small leakage on a huge order count is large money.
- **Inventory / replenishment** — service level vs. holding cost, ORSY-style auto-replenishment, demand forecasting.
- **Sales KPIs** — turning transaction data into decisions field and branch managers can act on.
- **Logistics** — routing and delivery efficiency across branches and customers.
- **Process automation** — the sheer volume of **RFQs, quotes, orders, invoices** flowing through email/EDI is where **agentic + low-code automation** removes manual toil.

## How this repo demonstrates fit for **both** postings

The portfolio behind this case study is now **19+ repositories** (all at [github.com/Dimikissimov](https://github.com/Dimikissimov)). I've built three complementary bodies of work, which is exactly why I can speak to both roles:

**Analytics side (Job #2)** — forecasting, KPIs, optimization, BI:
- `revops-optimizer` — assortment (MILP), newsvendor inventory, elasticity pricing, a **Power BI / DAX** pack and an exec deck; ~**€160k/yr** modelled uplift *(synthetic data)*.
- `sales-kpi-analytics` — KPI metrics, **forecasting with rolling-origin CV and MASE**, SQL, a **€2.6M** discount-leakage lever *(synthetic data)*.
- `distributor-intelligence-platform` — the engines composed into one platform; **MASE 0.38** forecasting (9 rolling folds), **25% km** routing saving, MILP vs. greedy assortment, **€136,972/yr** modelled uplift, 24 tests, Docker, CI *(synthetic data)*.
- `route-optimizer` — OR-Tools CP-SAT vehicle routing vs. heuristics, **4.6% / 31%** savings *(synthetic data)*.
- `market-basket-analysis` — Apriori + FP-growth implemented from scratch and cross-checked for **exact equality**; **224 frequent itemsets, 254 rules, top lift 2.41**, 3 customer segments, cross-sell recommendations with labelled estimates; 18 tests *(synthetic data)*.
- `ml-models-lab` — small models, measured properly: a global forecaster at **MASE 0.987 / RMSSE 0.948** that beats both seasonal-naive (1.080/1.062) *and* Holt-Winters (1.101/1.019); a SKU text classifier at **macro-F1 0.963**; an anomaly autoencoder at **PR-AUC 0.963 vs PCA 0.951** — a narrow win I report honestly, recommending PCA as the default; churn at **PR-AUC 0.653** with Platt calibration taking ECE from 0.197 to **0.021**; elasticity endogeneity bias corrected from **+1.52 to +0.03** (profit regret 0.89%) *(synthetic data)*.
- `energy-demand-forecast` — day-ahead load forecasting + peak-shaving battery dispatch, from scratch on numpy/scipy: a temperature + calendar regression at **MASE 0.497 / MAPE 4.8%** winning **14/14 rolling-origin CV folds** vs seasonal-naive (1.369 / 17.6%) — with **Holt-Winters losing to the naive baseline (3.040 / 37.6%) reported, not hidden**; the peak-shaving **LP** cuts the mean monthly peak **368.2 → 291.1 kW (−20.9%)**, worth **~EUR 11,100/yr at an ASSUMED EUR 12/kW-month tariff** while a fixed-timer baseline saves **EUR 0** — and the business case states plainly that at an assumed EUR 120k–180k battery cost this is a **10+ year simple payback: the battery does not pay for itself on these assumptions**; 19 tests *(synthetic data)*.
- `quality-anomaly-vision` — surface-defect screening with three detectors trained on clean images only (local statistics, PCA reconstruction, small conv autoencoder), one scoring rule fixed in advance, metrics from scratch: the autoencoder's ROC-AUC **0.779** beats PCA's **0.772** by only 0.007 — inside the **pre-registered 0.02 margin, so PCA is recommended over the deep model** (it also wins TPR **0.407 vs 0.393** at 5% FPR and localization); texture-breaks stay hard for everyone (best AUC 0.609) and training the AE longer made it worse (0.779 → 0.738) — both reported; 15 tests *(synthetic data)*.
- `retail-analytics-real` — the **completed real-data counterpart** ([published](https://github.com/Dimitres-Kisimov/retail-analytics-real)), on UCI Online Retail II (**1,067,371** genuinely messy real transaction rows, 2009–2011, CC BY 4.0). A cleaning pipeline that logs every step: **94.0% of rows retained**, **22.77% missing CustomerID** flagged (kept for revenue, excluded from customer analytics), cancellations separated into a returns frame (**3.65%** returns rate of gross value), **£19,643,862** revenue analyzed. RFM segmentation: **5,852 identified customers, 10 segments** — Champions are **25% of customers carrying 69.0% of identified revenue**. Forecasting under leakage-safe **5-fold rolling-origin CV**, and the honest headline is that **seasonal-naive wins** (MASE **1.094**) against Holt-Winters (**1.187**) and a lag-features model (**1.590**) — with only one seasonal cycle of training data, "same week last year" is genuinely hard to beat, and I report that plainly instead of hiding it. 20/20 tests on a committed real-data fixture, 6 QA'd figures, executive PDF + Excel deliverables *(real data)*.

**Logistics & operations side (new, and central to a distribution business)** — warehouse and network optimization:
- `logistics-flow-studio` (WarehouseTwin) — a game-like **warehouse digital twin** as an installable offline PWA: a canvas layout editor (racks, docks, conveyors, push/pull stations), an EUR1–EUR6 pallet catalog, DIN 15185-informed aisle checks, deterministic simulation, and an offline heuristic AI advisor that explains its suggestions. A/B strategy comparison shows **ABC 80/20 beating random slotting by ~21%** on pick travel, and the one-click layout optimizer measured **−48.6% pick travel** on the demo layout (pinned + reproducible in the repo's `docs/MEASUREMENTS.md`) *(synthetic data)*. The German-standards panel (ASR A1.8, DIN 15185, EN 15512, EPAL/DIN EN 13698, VDI 2510/3564, DGUV) is framed "aligned to, **not** a certification"; a depth pass (all storage systems, material-flow chains, push/pull dynamics, zone/batch/wave picking, a clearly disclaimed Würth-style illustrative preset) is in progress.
- `logistics-digital-twin` — container packing with FFD + CP-SAT (fill **2.0% → 30.2%**, **56 containers saved**, CP-SAT proves the heuristic optimal on the checked instance), slotting via linear assignment (**−44.2% pick travel**, reshuffle break-even ~0.7 days), and a hand-rolled discrete-event simulation of modern vs. legacy processes (**cycle time −76.1%**, picker travel **−66.5%**); 24 tests *(synthetic data)*.
- `supply-network-opt` — a capacitated facility-location MILP that opens **3 of 8 DCs** at **−21.2% total cost** vs. a greedy baseline ($83,550 on the instance), min-cost flow cross-checked **LP == graph solver to $0.00**, and multi-echelon safety stock with risk pooling (**−65.7%** network / **−80.1%** centralized); 19 tests *(synthetic data)*.

**Automation side (Job #1)** — agentic workflows, low-code, document processing:
- `agentic-automation-lab` — agentic tool-use loops **plus an n8n low-code RFQ-intake agent workflow** *(synthetic data)*.
- `agent-flow-studio` — a visual agent/flow builder *(synthetic data)*.
- `doc-extract-agent` — agentic extraction of RFQ / invoice documents into structured data *(synthetic data)*.
- `automation-roi-explorer` — an automation ROI dashboard *(synthetic data)*.
- `quantum-explainer` — **live and installable** at [dimitres-kisimov.github.io/quantum-explainer](https://dimitres-kisimov.github.io/quantum-explainer/): an offline-first PWA teaching quantum computing on a hand-written state-vector simulator (~300 lines, zero dependencies) — **42 physics/behaviour assertions** plus **57 structural/offline checks** pass; no frameworks, no build step, no network calls. Not a data project — it's the prototyping/education evidence: build a polished tool fast and explain a hard topic without hype.

Supporting research/method work: `bio-efficient-ai` (a small research PoC with an honestly cited paper). And on how I keep this maintained: `portfolio-ops` holds the audit scorecards, ranked backlog, KPI methodology, and security review that I run across the whole portfolio.

> All uplift/€ figures above are **modelled on synthetic data** to demonstrate method and are **not** claims about Würth — except the `retail-analytics-real` figures, which are **measured on real public retail data** and labelled as such. On real Würth data the numbers would still be different — validating that is exactly the internship work.

## What's in this repo

| File | What it is |
|------|-----------|
| [`docs/OPPORTUNITY_MAP.md`](docs/OPPORTUNITY_MAP.md) | Each Würth business area → the public-info problem category → the Data/AI approach → the exact portfolio repo + measured (synthetic) result that demonstrates it. |
| [`docs/JOB_SKILL_MAP.md`](docs/JOB_SKILL_MAP.md) | Two tables, one per posting: every major requirement bullet → repo + file/artifact + the number that proves it. |
| [`docs/AREAS_FOR_IMPROVEMENT.md`](docs/AREAS_FOR_IMPROVEMENT.md) | Honest, living list of what a *real* Würth deployment would additionally need (real data, GDPR/security, MLOps, scale, human-in-the-loop) and how I'd approach each. |
| [`deliverables/wuerth_data_ai_casestudy.pdf`](deliverables/) | A one-page executive PDF (built by `build_pdf.py`) — disclaimer, opportunity summary, both skill maps. |
| [`web/index.html`](web/index.html) | A self-contained offline web version of the case study. |

## How to reproduce the artifacts

```bash
# PDF one-pager (matplotlib):
python build_pdf.py           # writes deliverables/wuerth_data_ai_casestudy.pdf

# Web version: just open web/index.html in any browser (no internet needed).

# Smoke tests (CI runs these too, plus ruff):
python -m pytest -q           # PDF builds > 10 KB, web page stays self-contained,
                              # disclaimer present in README + web page
```

## Honesty notes

- Independent analysis, **public info only**, **not affiliated with Würth**.
- No internal Würth data or systems were used or accessed.
- All portfolio metrics cited here are on **synthetic data** and demonstrate method, not guaranteed business outcomes — with one exception: `retail-analytics-real` (UCI Online Retail II under CC BY 4.0, 1,067,371 raw rows) is **completed and published**, its numbers are measured on real transactions, and they're labelled **real data** wherever cited. Its forecasting headline — the **seasonal-naive baseline won** (MASE 1.094 vs Holt-Winters 1.187 and lag-features 1.590) — is reported plainly, because that's what one seasonal cycle of training data honestly supports.
- Standards references in `logistics-flow-studio` are framed "aligned to, **not** a certification".
- The newer projects keep the same honest-losses rule: `energy-demand-forecast` reports that **Holt-Winters loses to the seasonal-naive baseline** and that **the battery does not pay for itself at the assumed tariff** (10+ year simple payback on the stated assumptions); `quality-anomaly-vision`'s pre-registered rule **recommends PCA over the conv autoencoder** because the deep model's lead (0.007 ROC-AUC) is inside the pre-declared 0.02 margin.
- No superlatives — I don't claim to "beat everyone" or "guarantee" anything. This is honest, reproducible work.

— Dimitres Kisimov, 2026
