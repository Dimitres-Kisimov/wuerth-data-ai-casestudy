# Opportunity Map — Würth business areas × my portfolio

> **DISCLAIMER.** Independent analysis based on **public information only**. **Not affiliated with or endorsed by Würth.** No internal/confidential Würth data or systems were used. Würth-scale figures are **public and approximate**. Every performance number below is measured on **synthetic / self-generated data** in my own repositories and is labelled *(synthetic)* — none is a claim about Würth's real business.

This map answers: *for each part of a distribution business like Würth's, what is the public-info problem category, what Data/AI approach fits, and which repo of mine (with a concrete measured result) already demonstrates that capability?*

I deliberately lead with **categories of opportunity** rather than invented Würth numbers. The euro figures are from my synthetic demos and exist to show the *method works and is measurable*, not to forecast Würth outcomes.

---

## 1. Procurement / assortment

- **Public-info problem category.** A catalogue in the millions of articles (public, approximate) means constant decisions about *what to stock and where*, especially in the long tail — capital tied up vs. lost sales.
- **Data/AI approach.** Mixed-integer optimization (MILP) for assortment selection under budget/shelf constraints, benchmarked against a greedy baseline so the value of optimization is explicit.
- **Demonstrated by.** `revops-optimizer` (assortment MILP) and `distributor-intelligence-platform` (MILP vs. greedy).
- **Measured result *(synthetic)*.** Assortment MILP beats greedy on modelled objective; contributes to `revops-optimizer`'s **~€160k/yr** modelled uplift and the platform's **€136,972/yr** modelled uplift.

## 2. Pricing & margin

- **Public-info problem category.** With very high order volume, even small pricing/discount inefficiency compounds into large money; margin discipline matters as much as headline price.
- **Data/AI approach.** Price-elasticity estimation and Lerner-index optimal markups; discount-leakage detection from transaction data.
- **Demonstrated by.** `revops-optimizer` (elasticity + Lerner pricing) and `sales-kpi-analytics` (discount-leakage analysis).
- **Measured result *(synthetic)*.** Elasticity-based pricing layer in `revops-optimizer`; `sales-kpi-analytics` surfaces a **€2.6M discount-leakage lever** *(synthetic)*.

## 3. Inventory / replenishment

- **Public-info problem category.** ORSY-style shelf/bin systems and multi-channel fulfilment need the right stock at the right place — a service-level-vs-holding-cost trade-off at scale.
- **Data/AI approach.** Newsvendor inventory optimization + demand forecasting to drive replenishment points.
- **Demonstrated by.** `revops-optimizer` (newsvendor) and the forecasting engines in `sales-kpi-analytics` / `distributor-intelligence-platform`.
- **Measured result *(synthetic)*.** Forecasting at **MASE 0.376** in `distributor-intelligence-platform` and **MASE ~0.75** in `revops-optimizer` — both beat a seasonal-naive baseline (MASE < 1) *(synthetic)*.

## 4. Sales KPIs & analytics

- **Public-info problem category.** Field sales, branches, and e-commerce generate transaction data that must become decisions branch/field managers can act on.
- **Data/AI approach.** KPI metric layer + forecasting with **rolling-origin cross-validation** and MASE; BI dashboards (Power BI/DAX); exec reporting.
- **Demonstrated by.** `sales-kpi-analytics` (KPIs, forecasting, SQL, exec PDF) and `revops-optimizer` (Power BI / DAX pack + exec deck).
- **Measured result *(synthetic)*.** Rolling-origin CV with **MASE < 1 vs seasonal-naive**; a 3-page Power BI report pack + DAX measures; exec review PDF *(synthetic)*.

## 5. Logistics / routing

- **Public-info problem category.** Deliveries across branches and customers make route efficiency a direct cost lever (km, time, fuel).
- **Data/AI approach.** Capacitated vehicle routing via constraint programming (OR-Tools CP-SAT) vs. heuristic baselines.
- **Demonstrated by.** `route-optimizer` and the routing engine in `distributor-intelligence-platform`.
- **Measured result *(synthetic)*.** **4.6% / 31%** savings vs. heuristics in `route-optimizer`; **25% km saved** in the platform routing demo *(synthetic)*.

## 6. E-procurement / order automation

- **Public-info problem category.** E-procurement/EDI and email-based **RFQ → quote → order** flows carry high volume and manual toil; connecting systems and APIs is core.
- **Data/AI approach.** Agentic tool-use loops + **low-code (n8n) workflows** that intake RFQs, call systems/APIs, and orchestrate steps; ROI made explicit.
- **Demonstrated by.** `agentic-automation-lab` (agent loops + n8n RFQ-intake workflow), `agent-flow-studio` (visual flow builder), `automation-roi-explorer`.
- **Measured result *(synthetic)*.** `agentic-automation-lab` models **~€625k/yr**; `agent-flow-studio` **~€47k/yr**; `automation-roi-explorer` **€383k/yr net** *(synthetic)*.

## 7. Document processing

- **Public-info problem category.** RFQs, invoices, and order documents arrive as semi-structured text/PDF/email and must become structured records.
- **Data/AI approach.** Agentic document extraction (RFQ/invoice → structured fields) with validation.
- **Demonstrated by.** `doc-extract-agent`.
- **Measured result *(synthetic)*.** Structured extraction pipeline modelling **~€145k/yr** *(synthetic)*.

## 8. Customer retention / decline detection

- **Public-info problem category.** In a large recurring-order customer base, spotting accounts whose ordering is declining lets sales intervene early.
- **Data/AI approach.** A classification "predict layer" (decline detection) alongside forecasting and elasticity.
- **Demonstrated by.** `revops-optimizer` predict layer.
- **Measured result *(synthetic)*.** Decline-detection classifier at **ROC-AUC 0.99** on the synthetic set — strong on synthetic data; real-world validation required *(synthetic)*.

---

## Summary table

| # | Würth area (public-info) | Data/AI approach | Repo(s) | Measured result *(synthetic)* |
|---|--------------------------|------------------|---------|-------------------------------|
| 1 | Procurement / assortment | MILP vs. greedy | revops-optimizer, distributor-intelligence-platform | MILP > greedy; part of €136,972/yr platform uplift |
| 2 | Pricing & margin | Elasticity + Lerner; leakage detection | revops-optimizer, sales-kpi-analytics | €2.6M discount-leakage lever |
| 3 | Inventory / replenishment | Newsvendor + forecasting | revops-optimizer, distributor-intelligence-platform | MASE 0.376 / ~0.75 (< 1 baseline) |
| 4 | Sales KPIs & analytics | KPIs + rolling-origin CV + Power BI | sales-kpi-analytics, revops-optimizer | MASE < 1; DAX pack + exec PDF |
| 5 | Logistics / routing | OR-Tools CP-SAT VRP | route-optimizer, distributor-intelligence-platform | 4.6% / 31% savings; 25% km saved |
| 6 | E-procurement automation | Agentic + n8n low-code | agentic-automation-lab, agent-flow-studio, automation-roi-explorer | ~€625k / ~€47k / €383k net /yr |
| 7 | Document processing | Agentic RFQ/invoice extraction | doc-extract-agent | ~€145k/yr |
| 8 | Customer retention | Decline-detection classifier | revops-optimizer | ROC-AUC 0.99 |

All euro and accuracy figures are **modelled on synthetic data** and demonstrate method; they are **not** predictions about Würth.
