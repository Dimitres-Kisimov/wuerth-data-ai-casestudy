# Data & AI Case Study — mapped to two Würth internship roles

> **DISCLAIMER — read this first.** This is an **independent** case study I put together on my own. It is based **only on publicly available information** about the Würth Group (company website, public press, general industry knowledge). It is **not affiliated with, endorsed by, or reviewed by Würth**, and it uses **no internal, confidential, or proprietary Würth data or systems** of any kind. Every figure attributed to Würth's scale (number of companies, employees, revenue, ORSY installations, article counts) is **public and approximate** and is labelled as such — I have not invented internal Würth numbers. Every performance number in my own portfolio is measured on **synthetic / self-generated data** unless explicitly labelled otherwise, and I say so each time it appears (the real-data exceptions, `retail-analytics-real` and `decision-chain`, are measured on the public UCI Online Retail II dataset — CC BY 4.0 — and are labelled **real data** everywhere their numbers appear; `decision-chain` additionally labels its invented physical layers **synthetic-assigned** on every line). The point of this repo is to show *how I think and what I can build*, not to claim results on Würth's real business.

**In one sentence:** this repo maps two Würth Data & AI internship postings, requirement by requirement, to things I've already built and measured across a 19+-repo portfolio — e.g. forecasting at **MASE 0.38** over 9 rolling folds *(synthetic data)*, **−48.6% pick travel** from a one-click warehouse layout optimizer *(synthetic data)*, and **£19,643,862** of real transactions analyzed in `retail-analytics-real` *(real data, labelled)*.

**Deutsche Zusammenfassung:** eine deutschsprachige Kurzfassung (Disclaimer zuerst, Kernidee, stärkste Belege, das Real-Daten-Projekt) steht in [`docs/ZUSAMMENFASSUNG_DE.md`](docs/ZUSAMMENFASSUNG_DE.md).

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

The portfolio behind this case study is now **21+ repositories** (at [github.com/Dimitres-Kisimov](https://github.com/Dimitres-Kisimov)). I've built three complementary bodies of work — plus an integration capstone that ties them together — which is exactly why I can speak to both roles:

**Integration capstone (new, and the strongest single piece of evidence)**:
- `decision-chain` — **one real dataset through the whole distributor decision chain, with numbers that reconcile.** The UCI Online Retail II transactions (1,067,371 raw rows, *real data*) flow through clean → forecast → replenish → slot → pick → route → cost, and a reconciliation ledger machine-checks **13 cross-stage identities — all PASS**, including the cleaned revenue reproduced across two of my repositories **to the penny (£19,643,861.62)** and the cost ledger's total to the cent. The honest findings are part of the product: on lumpy demand nothing beats the naive walk (MASE 1.782); the exact slotting optimum is worth only **1.6% over classic ABC** (with the math explained); the CVRP metaheuristic beats the 1964 Clarke-Wright baseline by only **0.2%** and loses 19 of 48 days; the synthetic picking crew is **18% utilized** — reported, not hidden; every invented cost rate is labelled INVENTED. Ships an offline dashboard with the 13-identity reconciliation panel, byte-reproducible PDF/Excel deliverables from a committed run artifact, and 110 tests *(real data + labelled synthetic-assigned layers)*.

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
- `logistics-flow-studio` (WarehouseTwin — **v1.0**) — an offline, browser-based **warehouse / WMS digital twin and plant-flow simulator** (installable PWA, zero network calls). Describe a plant in plain keywords and a **transparent, deterministic generator** builds a full valid layout — steerable with plain-language commands (*"include 2 more RGVs in the picking sector"*) through an **offline natural-language parser, not a trained model** — then **simulate the WMS operation** (receiving → put-away → replenishment → picking → packing → shipping) with **ISO 22400-grounded KPIs** and the bottleneck stage named, a **live animated material flow** (stations, queues, conveyor-path routing) and a **live KPI dashboard**. Storage slotting/occupancy/retrieval, automation modelling (AS/RS, shuttle, RGV, AGV, conveyor), an **editable standards knowledge base** (edit the DIN/ASR/EN/VDI/ISO values the checks reason over), a canvas up to 120 × 80 m and a 2.5D view, **22 example scenarios** with per-example JSON/CSV export, plus the real-world pass — **import your own article/order CSVs** (in-browser, row-numbered validation, orders replayed exactly, honest "Data: yours" vs "Data: synthetic demo" badge) and a **floor-plan image underlay** with two-point calibration. The one-click layout optimizer measures **−48.6% pick travel** on the demo layout and **ABC 80/20 beats random slotting by ~21%** (both pinned + reproducible in `docs/MEASUREMENTS.md`); it outputs a consolidated **WMS Report** (print/JSON/CSV) and a scoped **IFC4** export, and **23 headless verification harnesses** back the documented behaviour *(synthetic data unless you import your own)*. The German-standards panel (ISO 22400, ASR A1.8, DIN 15185, EN 15512, EPAL/DIN EN 13698, VDI 2510/3564, DGUV) is framed "aligned to, **not** a certification".
- `logistics-digital-twin` — container packing with FFD + CP-SAT (fill **2.0% → 30.2%**, **56 containers saved**, CP-SAT proves the heuristic optimal on the checked instance), slotting via linear assignment (**−44.2% pick travel**, reshuffle break-even ~0.7 days), and a hand-rolled discrete-event simulation of modern vs. legacy processes (**cycle time −76.1%**, picker travel **−66.5%**); 24 tests *(synthetic data)*.
- `supply-network-opt` — a capacitated facility-location MILP that opens **3 of 8 DCs** at **−21.2% total cost** vs. a greedy baseline ($83,550 on the instance), min-cost flow cross-checked **LP == graph solver to $0.00**, and multi-echelon safety stock with risk pooling (**−65.7%** network / **−80.1%** centralized); 19 tests *(synthetic data)*.

**Automation side (Job #1)** — agentic workflows, low-code, document processing:
- `chain-mcp` — the **agentic-integration layer** over the portfolio: an **MCP server** (official `mcp` Python SDK; the Model Context Protocol is the open standard for connecting AI applications to tools) exposing six real engines — forecasting, slotting, carton packing, CVRP routing, discount-leakage analytics, repo audit — as tools Claude Desktop / Claude Code can call mid-conversation, with typed schemas, structured never-crash error results, a per-tool honesty label (`data_note`), and 20 tests including a live JSON-RPC handshake. Five tools run on deterministic synthetic seeded datasets *(labelled)*; `forecast_demand` runs on the real UCI pipeline *(real data; forecasts derived)*.
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
| [`docs/ZUSAMMENFASSUNG_DE.md`](docs/ZUSAMMENFASSUNG_DE.md) | German executive summary (Deutsche Zusammenfassung) — disclaimer first, core idea, strongest evidence, the real-data project; every number sourced from the English docs. |
| [`docs/OPPORTUNITY_MAP.md`](docs/OPPORTUNITY_MAP.md) | Each Würth business area → the public-info problem category → the Data/AI approach → the exact portfolio repo + measured (synthetic) result that demonstrates it. |
| [`docs/JOB_SKILL_MAP.md`](docs/JOB_SKILL_MAP.md) | Two tables, one per posting: every major requirement bullet → repo + file/artifact + the number that proves it. |
| [`docs/AREAS_FOR_IMPROVEMENT.md`](docs/AREAS_FOR_IMPROVEMENT.md) | Honest, living list of what a *real* Würth deployment would additionally need (real data, GDPR/security, MLOps, scale, human-in-the-loop) and how I'd approach each. |
| [`deliverables/wuerth_data_ai_casestudy.pdf`](deliverables/) | A one-page executive PDF (built by `build_pdf.py`) — disclaimer, opportunity summary, both skill maps. |
| [`web/index.html`](web/index.html) | A self-contained offline web version of the case study. |
| [`validation/CONSISTENCY_REPORT.md`](validation/CONSISTENCY_REPORT.md) | Machine-checked **anti-drift report** — every referenced repo resolves to the registry, every cited figure has a synthetic/real/public provenance label nearby, the disclaimers are present, and the license stays proprietary (no stale permissive self-license string). Auto-generated and deterministic; regenerate with `python -m validation.consistency_check`. |

## How to reproduce the artifacts

```bash
# PDF one-pager (matplotlib):
python build_pdf.py           # writes deliverables/wuerth_data_ai_casestudy.pdf

# Web version: just open web/index.html in any browser (no internet needed).

# Smoke tests (CI runs these too, plus ruff):
python -m pytest -q           # PDF builds > 10 KB, web page stays self-contained,
                              # disclaimer present in README + web page,
                              # and the consistency / anti-drift guard passes

# Consistency / anti-drift guard (offline, deterministic, stdlib only):
python -m validation.consistency_check   # validates repo names, provenance labels,
                                         # disclaimers and license; rewrites the report
```

The consistency guard is honest by design: it only **validates** what the docs
already state (it invents no numbers). It reads the authoritative repo registry in
[`validation/portfolio_repos.txt`](validation/portfolio_repos.txt) and fails if a
doc references an unregistered repo, if a cited figure lacks a nearby
synthetic/real/public provenance label, if a disclaimer goes missing, or if a
stale permissive open-source self-license string ever creeps back in (the
license must stay proprietary — all rights reserved). See
[`validation/CONSISTENCY_REPORT.md`](validation/CONSISTENCY_REPORT.md).

## Honesty notes

- Independent analysis, **public info only**, **not affiliated with Würth**.
- No internal Würth data or systems were used or accessed.
- All portfolio metrics cited here are on **synthetic data** and demonstrate method, not guaranteed business outcomes — with two exceptions measured on real transactions (UCI Online Retail II under CC BY 4.0, 1,067,371 raw rows) and labelled **real data** wherever cited: `retail-analytics-real` is **completed and published**, and its forecasting headline — the **seasonal-naive baseline won** (MASE 1.094 vs Holt-Winters 1.187 and lag-features 1.590) — is reported plainly, because that's what one seasonal cycle of training data honestly supports; and `decision-chain` runs the same real dataset through the whole chain, reproduces that repo's revenue **to the penny (£19,643,861.62)** across two codebases, and keeps its honest losses in the headline (naive wins lumpy demand; the slotting optimum is worth only 1.6% over ABC; CVRP beats Clarke-Wright by only 0.2%). Its invented layers (warehouse geometry, geography, cost rates) are labelled **synthetic-assigned** on every ledger line, and its cost table makes **no profit claims**.
- Standards references in `logistics-flow-studio` are framed "aligned to, **not** a certification".
- The newer projects keep the same honest-losses rule: `energy-demand-forecast` reports that **Holt-Winters loses to the seasonal-naive baseline** and that **the battery does not pay for itself at the assumed tariff** (10+ year simple payback on the stated assumptions); `quality-anomaly-vision`'s pre-registered rule **recommends PCA over the conv autoencoder** because the deep model's lead (0.007 ROC-AUC) is inside the pre-declared 0.02 margin.
- No superlatives — I don't claim to "beat everyone" or "guarantee" anything. This is honest, reproducible work.

— Dimitres Kisimov, 2026
