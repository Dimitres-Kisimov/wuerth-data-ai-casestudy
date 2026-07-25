# Job → Skill → Evidence map

> **DISCLAIMER.** Independent, **public-info-only** analysis, **not affiliated with Würth**, **no internal Würth data/systems used**. All measured numbers are on **synthetic data** *(labelled)* unless explicitly marked otherwise, and demonstrate method, not Würth outcomes.

Below, each requirement bullet from the two postings is mapped to a concrete piece of evidence: the **repo**, the **file/artifact**, and the **measured number** that backs it up. Where a posting bullet is a general competency (e.g. "team collaboration"), I map it to the artifact that best shows it in practice.

*Updated July 2026.* Since the first version of this document I've finished several logistics and analytics projects — `logistics-flow-studio`, `logistics-digital-twin`, `supply-network-opt`, `market-basket-analysis`, and final measured results in `ml-models-lab` — so the logistics and analytics rows below carry stronger evidence than before. One project, `retail-analytics-real`, is the **real-data** counterpart and is **in progress**: it's listed as evidence of direction, not results, and I cite no numbers from it until they're measured.

---

## Job #1 — Praktikum Data & AI: (Agentic) Automation mit Low-code Plattformen

| Posting requirement | Repo | File / artifact | Proof / measured result *(synthetic)* |
|---------------------|------|-----------------|----------------------------------------|
| Build **AI-agent workflows** (agentic automation) | `agentic-automation-lab` | agentic tool-use loop modules | Working agentic loops orchestrating multi-step tool calls |
| **Low-code platforms** (n8n, Power Automate style) | `agentic-automation-lab` | `n8n/rfq_intake_agent.json` | Importable n8n RFQ-intake AI-agent workflow; models **~€625k/yr** |
| **Visual / flow-based** agent building | `agent-flow-studio` | visual agent/flow builder app | Drag-style flow composition; models **~€47k/yr** |
| **Connecting systems / APIs** in automations | `agentic-automation-lab` | tool/connector layer in the agent loop | Agents call external tools/APIs as steps in the workflow |
| **Process automation** of high-volume back-office flows | `doc-extract-agent` | RFQ/invoice → structured extraction pipeline | Structured document automation; models **~€145k/yr** |
| **Document intake / understanding** (RFQ, invoice) | `doc-extract-agent` | extraction + validation modules | Semi-structured docs → structured fields with validation |
| **Prototyping** quickly, iterating | `agent-flow-studio`, `agentic-automation-lab`, `logistics-flow-studio` | runnable prototypes / demos | Multiple runnable prototypes; `logistics-flow-studio` is a full installable **offline PWA** (canvas layout editor + deterministic warehouse sim + offline heuristic AI advisor with explained suggestions) |
| Show **ROI / business value** of automation | `automation-roi-explorer` | automation ROI dashboard | Models **€383k/yr net**; ROI made explicit and inspectable |
| **Python** engineering for automation | across automation repos | Python source in each repo | Python throughout the agent loops and connectors |
| Communicate results to **non-technical stakeholders** | `automation-roi-explorer` | ROI dashboard views | Business-readable ROI presentation, not just code |

## Job #2 — Praktikum Data & AI Analytics

| Posting requirement | Repo | File / artifact | Proof / measured result *(synthetic unless noted)* |
|---------------------|------|-----------------|----------------------------------------|
| **BI / Power BI** dashboards | `revops-optimizer` | `powerbi/DAX_measures.md` + 3-page report pack | DAX measure library + executive report pack |
| **KPI dashboards / metrics** | `sales-kpi-analytics` | KPI metric layer + exec review PDF | Defined KPI set with an executive review deliverable |
| **Predictive analytics / forecasting** | `sales-kpi-analytics`, `ml-models-lab` | rolling-origin CV forecasting module; global forecaster | **MASE < 1 vs seasonal-naive** (rolling-origin CV); `ml-models-lab` global forecaster **MASE 0.987 / RMSSE 0.948**, beating both seasonal-naive (1.080 / 1.062) **and** Holt-Winters (1.101 / 1.019) |
| **Forecasting rigour / validation** | `distributor-intelligence-platform` | forecasting engine | **MASE 0.376** on synthetic series (beats naive baseline) |
| **Python** for analytics | `sales-kpi-analytics`, `revops-optimizer` | analysis + modelling scripts | Python analytics pipelines end-to-end |
| **SQL** querying / data modelling | `sales-kpi-analytics` | SQL query set + spend analysis | Hand-written SQL for KPI and spend analysis |
| **Excel**-level tabular analysis | `sales-kpi-analytics` | spend analysis outputs | Tabular spend breakdowns (Excel-equivalent) |
| **Data modelling** | `revops-optimizer` | optimization data model (assortment/inventory/pricing) | Structured entities feeding MILP / newsvendor / elasticity |
| **Optimization / prescriptive analytics** | `revops-optimizer`, `supply-network-opt`, `logistics-digital-twin` | assortment MILP; facility-location MILP; packing FFD + CP-SAT | MILP > greedy, models **~€160k/yr**; facility-location MILP opens **3 of 8 DCs at −21.2% total cost** vs a greedy baseline ($83,550 on the instance); min-cost flow cross-checked **LP == graph solver to $0.00**; container fill **2.0% → 30.2%** (**56 containers saved**, CP-SAT proves the heuristic optimal on the checked instance) |
| **Elasticity / statistical modelling** | `revops-optimizer`, `ml-models-lab` | price-elasticity + decline-detection layer; elasticity & churn studies | Decline classifier **ROC-AUC 0.99**; `ml-models-lab` elasticity endogeneity bias corrected **+1.52 → +0.03** (profit regret 0.89%); churn **PR-AUC 0.653** with Platt calibration **ECE 0.197 → 0.021** |
| **Turning data into business decisions** | `sales-kpi-analytics`, `market-basket-analysis` | discount-leakage analysis + exec PDF; cross-sell recommendations | Surfaces a **€2.6M discount-leakage lever**; cross-sell recommendations from **254 association rules** (top lift **2.41**) across **3 customer segments**, with labelled estimates |
| **Market-basket / cross-sell analytics** | `market-basket-analysis` | Apriori + FP-growth implemented from scratch | **224 frequent itemsets, 254 rules, top lift 2.41**; the two algorithms cross-checked for **exact equality**; 18 tests |
| **Classification / anomaly detection** | `ml-models-lab` | SKU text classifier; autoencoder vs PCA anomaly study | SKU classifier **macro-F1 0.963**; anomaly AE **PR-AUC 0.963 vs PCA 0.951** — a narrow win, honestly reported, with **PCA recommended as the default** |
| **Warehouse / intralogistics modelling** | `logistics-flow-studio` (WarehouseTwin), `logistics-digital-twin` | warehouse digital twin (offline PWA); slotting + discrete-event sim | One-click layout optimizer **−49.8% pick travel** on the demo layout; **ABC 80/20 beats random slotting ~26%** on pick travel (A/B comparison); slotting via linear assignment **−44.2% pick travel** (reshuffle break-even **~0.7 days**); hand-rolled discrete-event sim modern-vs-legacy: **cycle time −76.1%, picker travel −66.5%**; 24 tests |
| **Logistics / operations analytics** | `route-optimizer`, `supply-network-opt` | OR-Tools CP-SAT routing; multi-echelon safety stock | **4.6% / 31%** routing savings vs baselines; safety stock with risk pooling **−65.7%** (network) / **−80.1%** (centralized); 19 tests |
| **Real, messy data** *(in progress — real data, not synthetic)* | `retail-analytics-real` | UCI Online Retail II (~1M rows, CC BY 4.0) cleaning + analytics pipeline | **In progress**: documented cleaning pipeline, RFM, leakage-safe rolling-origin forecasting on genuinely messy real data. No results cited until they're measured. |
| Present findings to **decision-makers** | `revops-optimizer` | executive deck | Exec-level narrative deck built from the analysis |

A note on `logistics-flow-studio`'s standards panel: it references German norms (ASR A1.8, DIN 15185, EN 15512, EPAL/DIN EN 13698, VDI 2510/3564, DGUV) and is explicitly framed as **"aligned to, NOT a certification"** — the same honesty rule as everywhere else in this portfolio. A depth pass (all storage systems, material-flow chains, push/pull dynamics, zone/batch/wave picking, and a clearly disclaimed Würth-style illustrative preset) is in progress.

---

### How to read this

- **Repo** = one of my existing portfolio repositories.
- **File / artifact** = the specific thing to open to verify the claim.
- **Proof** = the measured number, on **synthetic data** unless the row says otherwise, always labelled. The one real-data project (`retail-analytics-real`) is in progress and contributes no numbers yet.

I'd rather under-claim and be reproducible than over-claim. On real Würth data these numbers would change — establishing the real baseline is the first thing I'd do in the internship (see [`AREAS_FOR_IMPROVEMENT.md`](AREAS_FOR_IMPROVEMENT.md)).
