# Opportunity Map — Würth business areas × my portfolio

> **DISCLAIMER.** Independent analysis based on **public information only**. **Not affiliated with or endorsed by Würth.** No internal/confidential Würth data or systems were used. Würth-scale figures are **public and approximate**. Every performance number below is measured on **synthetic / self-generated data** in my own repositories and is labelled *(synthetic)* — none is a claim about Würth's real business. The one exception, `retail-analytics-real`, is **completed and published**: its numbers are measured on real public data (UCI Online Retail II, CC BY 4.0) and labelled *(real data)* wherever they appear — still not a claim about Würth.

This map answers: *for each part of a distribution business like Würth's, what is the public-info problem category, what Data/AI approach fits, and which repo of mine (with a concrete measured result) already demonstrates that capability?*

I deliberately lead with **categories of opportunity** rather than invented Würth numbers. The euro figures are from my synthetic demos and exist to show the *method works and is measurable*, not to forecast Würth outcomes.

*Updated July 2026:* areas 9 and 10 are new — warehouse/intralogistics and supply-network design — backed by three finished projects (`logistics-flow-studio`, `logistics-digital-twin`, `supply-network-opt`), area 1 gains cross-sell evidence from `market-basket-analysis`, and area 4 gains **completed real-data evidence** from `retail-analytics-real`. *Second update:* areas 11 and 12 are new — energy management (`energy-demand-forecast`) and quality inspection (`quality-anomaly-vision`) — both carrying the same honest-losses framing as area 4: the energy repo reports that Holt-Winters loses to the naive baseline and that the battery does not pay for itself at the assumed tariff, and the vision repo's pre-registered rule recommends PCA over the deep model.

---

## 1. Procurement / assortment / cross-sell

- **Public-info problem category.** A catalogue in the millions of articles (public, approximate) means constant decisions about *what to stock and where*, especially in the long tail — capital tied up vs. lost sales. The same transaction data also encodes *what sells together*, which drives cross-sell and assortment bundling.
- **Data/AI approach.** Mixed-integer optimization (MILP) for assortment selection under budget/shelf constraints, benchmarked against a greedy baseline; association-rule mining (Apriori / FP-growth) for basket structure and cross-sell recommendations.
- **Demonstrated by.** `revops-optimizer` (assortment MILP), `distributor-intelligence-platform` (MILP vs. greedy), and `market-basket-analysis` (Apriori + FP-growth implemented from scratch, cross-checked for exact equality).
- **Measured result *(synthetic)*.** Assortment MILP beats greedy on modelled objective; contributes to `revops-optimizer`'s **~€160k/yr** modelled uplift and the platform's **€136,972/yr** modelled uplift. `market-basket-analysis`: **224 frequent itemsets, 254 rules, top lift 2.41, 3 customer segments**, cross-sell recommendations with labelled estimates; 18 tests.

## 2. Pricing & margin

- **Public-info problem category.** With very high order volume, even small pricing/discount inefficiency compounds into large money; margin discipline matters as much as headline price.
- **Data/AI approach.** Price-elasticity estimation and Lerner-index optimal markups; discount-leakage detection from transaction data; explicit correction for endogeneity in elasticity estimates.
- **Demonstrated by.** `revops-optimizer` (elasticity + Lerner pricing), `sales-kpi-analytics` (discount-leakage analysis), and `ml-models-lab` (elasticity endogeneity study).
- **Measured result *(synthetic)*.** `sales-kpi-analytics` surfaces a **€2.6M discount-leakage lever**; `ml-models-lab` corrects elasticity endogeneity bias from **+1.52 to +0.03**, with **profit regret 0.89%** *(synthetic)*.

## 3. Inventory / replenishment

- **Public-info problem category.** ORSY-style shelf/bin systems and multi-channel fulfilment need the right stock at the right place — a service-level-vs-holding-cost trade-off at scale.
- **Data/AI approach.** Newsvendor inventory optimization + demand forecasting to drive replenishment points; multi-echelon safety stock with risk pooling for where to hold buffer.
- **Demonstrated by.** `revops-optimizer` (newsvendor), the forecasting engines in `sales-kpi-analytics` / `distributor-intelligence-platform` / `ml-models-lab`, and `supply-network-opt` (safety stock).
- **Measured result *(synthetic)*.** Forecasting at **MASE 0.38** (9 rolling folds) in `distributor-intelligence-platform`; `ml-models-lab`'s global forecaster at **MASE 0.987 / RMSSE 0.948**, beating seasonal-naive (1.080 / 1.062) and Holt-Winters (1.101 / 1.019); safety stock with risk pooling **−65.7%** (network) / **−80.1%** (centralized) in `supply-network-opt` *(synthetic)*.

## 4. Sales KPIs & analytics

- **Public-info problem category.** Field sales, branches, and e-commerce generate transaction data that must become decisions branch/field managers can act on.
- **Data/AI approach.** KPI metric layer + forecasting with **rolling-origin cross-validation** and MASE; BI dashboards (Power BI/DAX); exec reporting.
- **Demonstrated by.** `sales-kpi-analytics` (KPIs, forecasting, SQL, exec PDF) and `revops-optimizer` (Power BI / DAX pack + exec deck). `retail-analytics-real` is the **completed real-data counterpart** (UCI Online Retail II, 1,067,371 genuinely messy real rows, 2009–2011, CC BY 4.0): documented cleaning pipeline, RFM, leakage-safe rolling-origin forecasting — published with measured results, 20/20 tests on a committed real-data fixture, 6 QA'd figures, exec PDF + Excel deliverables.
- **Measured result *(synthetic)*.** Rolling-origin CV with **MASE < 1 vs seasonal-naive**; a 3-page Power BI report pack + DAX measures; exec review PDF *(synthetic)*.
- **Measured result *(real data — `retail-analytics-real`)*.** Cleaning logs every step: **94.0% of rows retained**, **22.77% missing CustomerID** flagged (kept for revenue, excluded from customer analytics), cancellations separated as a returns frame (**3.65%** of gross value), **£19,643,862** revenue analyzed. RFM: **5,852 identified customers, 10 segments** — Champions are **25% of customers carrying 69.0% of identified revenue**. Forecasting (5-fold rolling-origin CV, leakage-safe): the honest headline is that **seasonal-naive wins** — MASE **1.094** vs Holt-Winters **1.187** and lag-features **1.590** — with only one seasonal cycle of training data. Reported plainly, not hidden.

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
- **Data/AI approach.** A classification "predict layer" (decline detection) alongside forecasting and elasticity; churn modelling with honest probability calibration.
- **Demonstrated by.** `revops-optimizer` predict layer and `ml-models-lab` (churn study).
- **Measured result *(synthetic)*.** Decline-detection classifier at **ROC-AUC 0.99** on the synthetic set — strong on synthetic data; real-world validation required. `ml-models-lab` churn model at **PR-AUC 0.653** with Platt calibration bringing **ECE from 0.197 to 0.021** — a deliberately realistic, unglamorous number reported as-is *(synthetic)*.

## 9. Warehouse operations / intralogistics *(new)*

- **Public-info problem category.** A distribution group at this scale runs many warehouses and branch stores: layout, slotting, picking strategy, and material flow directly drive pick travel, cycle time, and safety compliance.
- **Data/AI approach.** A warehouse **digital twin**: layout editing + deterministic simulation to compare strategies before touching the physical warehouse; slotting as an assignment problem; discrete-event simulation of process variants; explained heuristic suggestions rather than black-box output.
- **Demonstrated by.** `logistics-flow-studio` (WarehouseTwin — a game-like warehouse digital twin as an installable **offline PWA**: canvas layout editor with racks/docks/conveyors/push-pull stations, EUR1–EUR6 pallet catalog, DIN 15185-informed aisle checks, deterministic simulation, offline heuristic AI advisor with explained suggestions) and `logistics-digital-twin` (packing, slotting, discrete-event sim; 24 tests).
- **Measured result *(synthetic)*.** One-click layout optimizer **−48.6% pick travel** on the demo layout (pinned + reproducible in the repo's `docs/MEASUREMENTS.md`); A/B strategy comparison shows **ABC 80/20 beats random slotting ~21%** on pick travel; slotting via linear assignment **−44.2% pick travel** with reshuffle break-even **~0.7 days**; discrete-event sim modern-vs-legacy **cycle time −76.1%**, **picker travel −66.5%**; container packing FFD + CP-SAT lifts fill **2.0% → 30.2%** (**56 containers saved**; CP-SAT proves the heuristic optimal on the checked instance) *(synthetic)*.
- **Honesty note.** The German-standards panel (ASR A1.8, DIN 15185, EN 15512, EPAL/DIN EN 13698, VDI 2510/3564, DGUV) is framed **"aligned to, NOT a certification"**. A depth pass (all storage systems, material-flow chains, push/pull dynamics, zone/batch/wave picking, and a clearly disclaimed Würth-style illustrative preset) is **in progress**.

## 10. Supply-network design *(new)*

- **Public-info problem category.** ~400+ companies in 80+ countries (public, approximate) implies recurring network questions: which DCs to operate, how flows route through the network, and where safety stock should sit.
- **Data/AI approach.** Capacitated facility-location MILP vs. a greedy baseline; min-cost flow with an independent cross-check; multi-echelon safety stock with risk pooling.
- **Demonstrated by.** `supply-network-opt` (19 tests).
- **Measured result *(synthetic)*.** Facility-location MILP opens **3 of 8 DCs** at **−21.2% total cost** vs greedy (**$83,550** on the instance); min-cost flow cross-checked **LP == graph solver to $0.00**; safety stock with risk pooling **−65.7%** (network) / **−80.1%** (centralized) *(synthetic)*.

## 11. Energy management / facility operations *(new)*

- **Public-info problem category.** A group operating warehouses, production companies, and branch sites across 80+ countries (public, approximate) pays industrial electricity tariffs where a monthly **demand charge** is set by the single highest hourly load — a few peak hours per month price the whole month. Forecasting site load and shifting the peak is a direct, recurring cost lever.
- **Data/AI approach.** Day-ahead load forecasting under rolling-origin CV (temperature + calendar regression vs seasonal-naive vs Holt-Winters, MASE-scored), then battery dispatch against the monthly peak formulated as a **linear program** — with the ROI framed on labelled assumptions rather than a sales pitch.
- **Demonstrated by.** `energy-demand-forecast` (forecasters and the LP written from scratch on numpy/scipy; 19 tests).
- **Measured result *(synthetic)*.** Regression at **MASE 0.497 / MAPE 4.8%**, winning **14/14 CV folds** vs seasonal-naive (**1.369 / 17.6%**); the LP cuts the mean monthly peak **368.2 → 291.1 kW (−20.9%)**, worth **~EUR 11,100/yr at an ASSUMED EUR 12/kW-month tariff**, while a fixed evening-timer baseline saves **EUR 0** — on this site, *when* to discharge is the entire product *(synthetic)*.
- **Honesty note.** Two losses reported, not hidden: **Holt-Winters loses to the seasonal-naive baseline** (MASE 3.040 vs 1.369) — a real lesson in method-to-problem fit — and at an assumed EUR 120,000–180,000 battery cost the demand-charge saving alone is a **10+ year simple payback: the battery does not pay for itself on these assumptions**, and the repo's business case says so instead of inflating the tariff until it does.

## 12. Quality inspection *(new)*

- **Public-info problem category.** An assembly/fastening products group lives on product quality — in its own production companies and in incoming-goods QA, surface-defect screening (scratches, pits, texture irregularities) is a classic vision task where the real question is *when a neural network actually earns its keep over simpler methods*.
- **Data/AI approach.** Three anomaly detectors trained on **clean images only** (local statistics, PCA reconstruction, small conv autoencoder), one shared image-level scoring rule fixed before results were seen, and a **pre-registered complexity rule** deciding the recommendation; ROC/PR/IoU metrics implemented from scratch.
- **Demonstrated by.** `quality-anomaly-vision` (15 tests).
- **Measured result *(synthetic)*.** Conv autoencoder ROC-AUC **0.779** vs PCA **0.772** vs local statistics 0.687 — the AE's 0.007 lead is inside the pre-registered 0.02 margin, so **PCA reconstruction is the recommendation**: it also wins the screening operating point (**TPR 0.407 vs 0.393 at 5% FPR**) and localization (**mean IoU 0.207**) *(synthetic)*.
- **Honesty note.** The one defect class that splits the field is stated plainly: texture-breaks are hard for every method (best ROC-AUC **0.609**, autoencoder only — if they dominated a real defect mix, the recommendation could legitimately flip), and training the autoencoder longer made it **worse** (0.779 → 0.738 at 30 epochs). This is the same pre-registered-rule honesty as the `ml-models-lab` anomaly study: the rule picked the simpler method, and that's a feature.

---

## Summary table

| # | Würth area (public-info) | Data/AI approach | Repo(s) | Measured result *(synthetic unless noted)* |
|---|--------------------------|------------------|---------|-------------------------------|
| 1 | Procurement / assortment / cross-sell | MILP vs. greedy; Apriori/FP-growth | revops-optimizer, distributor-intelligence-platform, market-basket-analysis | MILP > greedy; part of €136,972/yr platform uplift; 254 rules, top lift 2.41 |
| 2 | Pricing & margin | Elasticity + Lerner; leakage; endogeneity fix | revops-optimizer, sales-kpi-analytics, ml-models-lab | €2.6M leakage lever; elasticity bias +1.52 → +0.03 |
| 3 | Inventory / replenishment | Newsvendor + forecasting + safety stock | revops-optimizer, distributor-intelligence-platform, ml-models-lab, supply-network-opt | MASE 0.38; MASE 0.987 / RMSSE 0.948 (beats naive + Holt-Winters); safety stock −65.7% / −80.1% |
| 4 | Sales KPIs & analytics | KPIs + rolling-origin CV + Power BI | sales-kpi-analytics, revops-optimizer (+ retail-analytics-real, real data) | MASE < 1; DAX pack + exec PDF; *real data:* seasonal-naive wins CV (MASE 1.094 vs HW 1.187), £19.6M analyzed, Champions 25% → 69.0% of revenue |
| 5 | Logistics / routing | OR-Tools CP-SAT VRP | route-optimizer, distributor-intelligence-platform | 4.6% / 31% savings; 25% km saved |
| 6 | E-procurement automation | Agentic + n8n low-code | agentic-automation-lab, agent-flow-studio, automation-roi-explorer | ~€625k / ~€47k / €383k net /yr |
| 7 | Document processing | Agentic RFQ/invoice extraction | doc-extract-agent | ~€145k/yr |
| 8 | Customer retention | Decline / churn classifiers + calibration | revops-optimizer, ml-models-lab | ROC-AUC 0.99; churn PR-AUC 0.653, ECE 0.197 → 0.021 |
| 9 | Warehouse / intralogistics | Digital twin + slotting + DES + packing | logistics-flow-studio, logistics-digital-twin | −48.6% pick travel (optimizer); ABC ~21% > random; slotting −44.2%; DES −76.1% cycle / −66.5% travel; fill 2.0% → 30.2% |
| 10 | Supply-network design | Facility MILP + min-cost flow + safety stock | supply-network-opt | −21.2% cost vs greedy; LP == graph to $0.00; −65.7% / −80.1% stock |
| 11 | Energy management / facilities | Load forecasting (rolling-origin CV) + peak-shaving LP | energy-demand-forecast | MASE 0.497, 14/14 folds (HW loses to naive, reported); peak −20.9%; ~EUR 11,100/yr at ASSUMED tariff; battery does not pay back on these assumptions |
| 12 | Quality inspection | Clean-only anomaly detection; pre-registered rule | quality-anomaly-vision | AE 0.779 vs PCA 0.772 ROC-AUC — inside the 0.02 margin, PCA recommended; TPR 0.407 vs 0.393 @ 5% FPR |

All euro/dollar and accuracy figures are **modelled on synthetic data** and demonstrate method; they are **not** predictions about Würth. The exception is `retail-analytics-real`: its figures are **measured on real data** (UCI Online Retail II, CC BY 4.0), labelled as such — including the honest one, that the seasonal-naive baseline won its forecast comparison — and they are still not predictions about Würth.
