# Job → Skill → Evidence map

> **DISCLAIMER.** Independent, **public-info-only** analysis, **not affiliated with Würth**, **no internal Würth data/systems used**. All measured numbers are on **synthetic data** *(labelled)* and demonstrate method, not Würth outcomes.

Below, each requirement bullet from the two postings is mapped to a concrete piece of evidence: the **repo**, the **file/artifact**, and the **measured number** that backs it up. Where a posting bullet is a general competency (e.g. "team collaboration"), I map it to the artifact that best shows it in practice.

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
| **Prototyping** quickly, iterating | `agent-flow-studio`, `agentic-automation-lab` | runnable prototypes / demos | Multiple runnable prototypes across the automation repos |
| Show **ROI / business value** of automation | `automation-roi-explorer` | automation ROI dashboard | Models **€383k/yr net**; ROI made explicit and inspectable |
| **Python** engineering for automation | across automation repos | Python source in each repo | Python throughout the agent loops and connectors |
| Communicate results to **non-technical stakeholders** | `automation-roi-explorer` | ROI dashboard views | Business-readable ROI presentation, not just code |

## Job #2 — Praktikum Data & AI Analytics

| Posting requirement | Repo | File / artifact | Proof / measured result *(synthetic)* |
|---------------------|------|-----------------|----------------------------------------|
| **BI / Power BI** dashboards | `revops-optimizer` | `powerbi/DAX_measures.md` + 3-page report pack | DAX measure library + executive report pack |
| **KPI dashboards / metrics** | `sales-kpi-analytics` | KPI metric layer + exec review PDF | Defined KPI set with an executive review deliverable |
| **Predictive analytics / forecasting** | `sales-kpi-analytics` | rolling-origin CV forecasting module | **MASE < 1 vs seasonal-naive** (rolling-origin cross-validation) |
| **Forecasting rigour / validation** | `distributor-intelligence-platform` | forecasting engine | **MASE 0.376** on synthetic series (beats naive baseline) |
| **Python** for analytics | `sales-kpi-analytics`, `revops-optimizer` | analysis + modelling scripts | Python analytics pipelines end-to-end |
| **SQL** querying / data modelling | `sales-kpi-analytics` | SQL query set + spend analysis | Hand-written SQL for KPI and spend analysis |
| **Excel**-level tabular analysis | `sales-kpi-analytics` | spend analysis outputs | Tabular spend breakdowns (Excel-equivalent) |
| **Data modelling** | `revops-optimizer` | optimization data model (assortment/inventory/pricing) | Structured entities feeding MILP / newsvendor / elasticity |
| **Optimization / prescriptive analytics** | `revops-optimizer` | assortment MILP, newsvendor, Lerner pricing | MILP > greedy; models **~€160k/yr** uplift |
| **Elasticity / statistical modelling** | `revops-optimizer` | price-elasticity + decline-detection layer | Elasticity estimates; decline classifier **ROC-AUC 0.99** |
| **Turning data into business decisions** | `sales-kpi-analytics` | discount-leakage analysis + exec PDF | Surfaces a **€2.6M discount-leakage lever** with a recommendation |
| **Logistics / operations analytics** | `route-optimizer` | OR-Tools CP-SAT routing vs. heuristics | **4.6% / 31%** cost savings vs. baselines |
| Present findings to **decision-makers** | `revops-optimizer` | executive deck | Exec-level narrative deck built from the analysis |

---

### How to read this

- **Repo** = one of my existing portfolio repositories.
- **File / artifact** = the specific thing to open to verify the claim.
- **Proof** = the measured number, always on **synthetic data**, always labelled.

I'd rather under-claim and be reproducible than over-claim. On real Würth data these numbers would change — establishing the real baseline is the first thing I'd do in the internship (see [`AREAS_FOR_IMPROVEMENT.md`](AREAS_FOR_IMPROVEMENT.md)).
