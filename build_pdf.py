"""Build the executive one-pager PDF for the Wuerth Data & AI case study.

Independent, public-info-only analysis. Not affiliated with Wuerth. No internal
Wuerth data or systems used. All portfolio metrics are on SYNTHETIC data except
retail-analytics-real, which is measured on real UCI Online Retail II data
(CC BY 4.0) and labelled REAL DATA wherever cited.

Usage:
    python build_pdf.py
Writes deliverables/wuerth_data_ai_casestudy.pdf (multi-panel, executive).
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

# Windows-console-safe stdout (ASCII markers used anyway, but be defensive).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = "deliverables"
OUT_PATH = os.path.join(OUT_DIR, "wuerth_data_ai_casestudy.pdf")

INK = "#1a1a1a"
MUTED = "#555555"
ACCENT = "#c8102e"  # a neutral red, not a logo asset
RULE = "#cccccc"

DISCLAIMER = (
    "DISCLAIMER: Independent analysis based on PUBLIC information only. NOT "
    "affiliated with, endorsed by, or reviewed by the Wuerth Group. No internal, "
    "confidential, or proprietary Wuerth data or systems were used. Wuerth-scale "
    "figures are public and approximate. All portfolio performance numbers are on "
    "SYNTHETIC / self-generated data unless labelled REAL DATA, and demonstrate "
    "method only -- they are not claims about Wuerth's real business. The "
    "real-data projects (retail-analytics-real, decision-chain) are completed: "
    "measured on public UCI Online Retail II data (CC BY 4.0) and labelled REAL "
    "DATA where cited; decision-chain labels its invented layers on every line."
)


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def new_page(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    return fig, ax


def disclaimer_band(ax, y=0.965):
    ax.add_patch(
        plt.Rectangle((0.06, y - 0.085), 0.88, 0.085, transform=ax.transAxes,
                      facecolor="#fdeaec", edgecolor=ACCENT, lw=0.8, zorder=0)
    )
    lines = _wrap(DISCLAIMER, 92)
    ax.text(0.075, y - 0.011, "\n".join(lines), transform=ax.transAxes,
            fontsize=6.6, color="#7a1420", va="top", family="DejaVu Sans")


def cover(pdf):
    fig, ax = new_page(pdf)
    ax.text(0.06, 0.90, "Data & AI Case Study", fontsize=30, fontweight="bold",
            color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.855, "Mapped to two Wuerth internship roles",
            fontsize=14, color=MUTED, transform=ax.transAxes)
    ax.plot([0.06, 0.94], [0.835, 0.835], color=ACCENT, lw=2,
            transform=ax.transAxes)

    disclaimer_band(ax, y=0.80)

    intro = (
        "This is my independent case study. I mapped the requirements of two "
        "Wuerth Data & AI internship postings to work I have already built and "
        "measured in my own portfolio (now 23 repositories, including the "
        "decision-chain integration capstone -- one real dataset through the "
        "whole distributor chain with 13 machine-checked reconciliation "
        "identities plus four additive ones -- an MCP agentic-integration "
        "server with contract-enforced result provenance and idempotent "
        "result caching, two "
        "warehouse-logistics flagships, a supply-network "
        "optimizer, an energy forecasting + dispatch study, a visual "
        "quality-inspection study with SPC monitoring, a fraud-operations "
        "study with gated retrain promotion, a predictive-maintenance policy "
        "study, and a live installable quantum-explainer PWA). The euro and accuracy "
        "figures throughout are on synthetic data (except retail-analytics-real "
        "and decision-chain, measured and labelled on real public data) and "
        "exist to prove the methods work and are measurable -- not to forecast "
        "Wuerth outcomes."
    )
    ax.text(0.06, 0.685, "\n".join(_wrap(intro, 86)), fontsize=10,
            color=INK, va="top", transform=ax.transAxes)

    roles = [
        ("Job #1  --  (Agentic) Automation with Low-code Platforms",
         ("Agentic AI workflows, low-code (n8n / Power Automate), connecting "
          "systems & APIs, document automation, ROI, rapid prototyping.")),
        ("Job #2  --  Data & AI Analytics",
         ("BI / Power BI, KPI dashboards, forecasting & predictive analytics, "
          "Python & SQL, data modelling, turning data into decisions.")),
    ]
    y = 0.57
    for title, body in roles:
        ax.add_patch(plt.Rectangle((0.06, y - 0.085), 0.88, 0.095,
                     transform=ax.transAxes, facecolor="#f5f5f5",
                     edgecolor=RULE, lw=0.8))
        ax.text(0.075, y - 0.005, title, fontsize=11, fontweight="bold",
                color=ACCENT, va="top", transform=ax.transAxes)
        ax.text(0.075, y - 0.035, "\n".join(_wrap(body, 82)), fontsize=8.8,
                color=INK, va="top", transform=ax.transAxes)
        y -= 0.125

    who = (
        "Wuerth (public profile, approximate): a large family-owned German-HQ "
        "group in assembly/fastening and industrial MRO distribution -- ~400+ "
        "companies in 80+ countries, ~87,000 employees, ~EUR 20B+ revenue, a "
        "catalogue in the millions of articles, multi-channel (field sales, "
        "branches, e-commerce, e-procurement/EDI, ORSY inventory systems). A "
        "business that runs on assortment, pricing, availability, logistics, and "
        "high-volume transactional documents -- a natural fit for applied Data & AI."
    )
    ax.text(0.06, 0.30, "Who Wuerth is (public info)", fontsize=12,
            fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.275, "\n".join(_wrap(who, 88)), fontsize=8.8, color=MUTED,
            va="top", transform=ax.transAxes)

    ax.text(0.06, 0.04, "Dimitres Kisimov  |  2026  |  all rights reserved "
            "(portfolio review)  |  metrics on synthetic data unless labelled "
            "real data", fontsize=8, color=MUTED, transform=ax.transAxes)
    pdf.savefig(fig)
    plt.close(fig)


def opportunity_page(pdf):
    fig, ax = new_page(pdf)
    disclaimer_band(ax, y=0.985)
    ax.text(0.06, 0.885, "Opportunity map (summary)", fontsize=18,
            fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.86, "Wuerth business area (public-info) -> Data/AI approach "
            "-> repo + measured result (synthetic unless noted)", fontsize=8.5,
            color=MUTED, transform=ax.transAxes)

    rows = [
        ["Area (public-info)", "Approach", "Repo", "Result (synthetic -- labelled if real)"],
        ["Procurement / assortment / cross-sell",
         "MILP vs greedy; Apriori/FP-growth; rule redundancy pruning",
         "revops-optimizer, market-basket-analysis",
         "MILP > greedy; 254 rules, top lift 2.41; 41% of rules redundant -- "
         "the 149 kept carry all the information"],
        ["Pricing & margin", "Elasticity + leakage; endogeneity fix; per-move robustness gate; ablation",
         "revops-optimizer, sales-kpi-analytics, ml-models-lab",
         "EUR2.6M leakage lever; bias +1.52 -> +0.03; price-move gate 17/29 ACCEPT -- "
         "the biggest move (45% of the pricing uplift) is HELD, stated as a screen; "
         "ablation: endogeneity-control knockout +1.446 RMSE -- the load-bearing piece"],
        ["Inventory / replenishment",
         "Newsvendor + forecast + ROP/EOQ policy + supplier reliability",
         "distributor-intel-platform, ml-models-lab",
         "MASE 0.38; MASE 0.987 / RMSSE 0.948 (beats naive + Holt-Winters); "
         "policy: EUR127,421 working capital (cycle+safety exactly), 5.5x turns, 99.9% fill; "
         "measured lead times cost +14.4% safety stock -- wobble is 3/4 of the bill"],
        ["Sales KPIs & analytics",
         "KPIs + rolling-origin CV + pacing interval + rep decomposition",
         "sales-kpi-analytics",
         "MASE < 1; exec PDF; pacing EUR10.91M = 95.7% of plan, 80% interval -- "
         "closed-year back-check landed above the band, reported; rep decomposition "
         "(indirect standardization): 92% of the league table is territory, 8% execution"],
        ["Logistics / routing", "OR-Tools CP-SAT VRP + robustness + Fleet Size and Mix VRP",
         "route-optimizer",
         "4.6% / 31% savings; 5% headroom: failing scenarios 96% -> 44%, "
         "expected day -4.6%; fleet mix: -17.5% vs the status quo with the "
         "service price shown (longest route +25.2%)"],
        ["E-procurement automation",
         "Agentic + n8n low-code + reliability benchmark + content-verification "
         "layer + dry-run flow cost estimator",
         "agentic-automation-lab, agent-flow-studio",
         "~EUR625k/yr modelled; 1,350 seeded trials: content faults fail "
         "silently, stated (assumed rates); verification layer on the same "
         "fault schedule: 88.7% -> 98.8% delivered-correct, silent-wrong "
         "11,523/yr -> 0 (price stated; 71 tests); flow estimator: "
         "engine-verified branch scenarios, 'not a bill' (declared rates)"],
        ["Document processing", "Agentic extract + 7-rule validation gate + cost model",
         "doc-extract-agent",
         "~EUR145k/yr modelled; combined-gate precision 70.0% -> 87.5%; cost model: "
         "auto-post pays only above 98.4% precision -- the gate alone would lose "
         "money (modeled), the pre-fill carries the value"],
        ["Customer retention", "Decline + churn classifiers + ablation",
         "revops-optimizer, ml-models-lab",
         "ROC-AUC 0.99; churn ECE 0.197 -> 0.021; "
         "bootstrap skill CI +0.457 [+0.381, +0.528]; ablation: freq_slope "
         "knockout -0.247 PR-AUC; null knockouts not counted as wins"],
        ["Warehouse / WMS (new)",
         "WMS twin + factory/plant sim (Story Mode, 894-element plant, definable objects, "
         "multi-way line sim + fluids solver); slotting + DES + packing + pick-path routing "
         "+ order batching",
         "logistics-flow-studio (WarehouseTwin v3.19), logistics-digital-twin (engine)",
         "-48.6% pick travel; ABC ~21% > random; ISO 22400 KPIs; 112/112 self-test + 45 harnesses; "
         "line sim 112.5 parts/hr (~88.1% eff.); fluids solver (modelled); "
         "engine slotting -44.2% (golden-zone 25% -> 100%); fill 2.0% -> 30.2%; "
         "routing: return +3.0% vs exact optimum, optimized layout ~46% shorter; "
         "batching: savings -71.3%, routing flips to largest-gap"],
        ["Supply-network design (new)",
         "Facility MILP + flows + safety stock + service frontier + growth plan",
         "supply-network-opt",
         "-21.2% cost vs greedy; stock -65.7% / -80.1%; "
         "frontier $2,353 -> $14,750 per service point (6.3x); "
         "growth: +8.8% headroom, 4th DC first pays at 1.30x (planning estimates)"],
        ["Energy management / facilities (new)",
         "Load forecast (rolling CV) + peak-shaving LP + causal dispatch backtest "
         "+ degree-day decomposition",
         "energy-demand-forecast",
         "MASE 0.497, 14/14 folds (Holt-Winters loses to naive, reported); "
         "peak -20.9%; ~EUR11,100/yr at ASSUMED tariff; battery does not pay back "
         "on these assumptions; backtest captures 72.7% of the LP bound "
         "(robust variant loses, reported); decomposition recovers designed "
         "balance points exactly -- weather 4.5% of energy, 18% of the July peak "
         "(modelled attribution)"],
        ["Quality inspection (new)",
         "Clean-only anomaly detection; pre-registered rule; SPC p-chart + WE rules; "
         "measured OCAP",
         "quality-anomaly-vision",
         "AE 0.779 vs PCA 0.772 ROC-AUC -- inside 0.02 margin, PCA recommended; "
         "TPR 0.407 vs 0.393 @ 5% FPR; calibration correction 0 -> 0.70% measured; "
         "OCAP: label-free re-centering is a trap (green chart, near-blind screen); "
         "refit on verified-clean frames recovers ~99% of the drift cost"],
        ["Real data (completed)", "Cleaning + RFM + returns + lifecycle + leakage-safe CV",
         "retail-analytics-real",
         "real data: seasonal-naive wins CV, MASE 1.094; returns 3.65% of gross, "
         "95.0% of value matched, median 10-day lag; Champions 25% -> 69.0%; "
         "lifecycle: resurrections outnumber repeats (439 vs 390/month)"],
        ["Chain integration & reconciliation (new)",
         "Provenance-tagged pipeline + identity ledger; MCP agentic layer w/ "
         "machine-readable result provenance + idempotent caching",
         "decision-chain, chain-mcp",
         "real data + labelled layers: 13/13 identities PASS + additive (n), (o), "
         "(p), (q); per-order spread to the cent over 4,151 orders (top decile "
         "59.0%, Gini 0.665); fleet knob: only the transport line moves, vans "
         "unpriced (model property, not fleet advice); cross-repo revenue "
         "GBP 19,643,861.62 to the penny; naive wins lumpy (MASE 1.782); "
         "contract-enforced provenance + cache-status, 193 tests"],
        ["Fraud & transaction-risk ops (new)",
         "Cost-based alerting; gated retrain promotion; selective-labels feedback sim",
         "fraud-detection-ops",
         "PR-AUC 0.270 vs oracle 0.367; swap-set gates -> PROMOTE at $8,632 vs "
         "$8,841 -- retrain finds no new fraud, wins by shedding load (stated); "
         "feedback sim: ranking survives censoring, probabilities + alerts collapse"],
        ["Maintenance & asset reliability (new)",
         "Censored Weibull + age-replacement vs condition-based + CBM re-tuning",
         "predictive-maintenance",
         "beta 4.81; T* = 44.4 d at 7.16/machine-day -- the calendar rule beats "
         "the repo's own detector at the default threshold, reported; re-tuned "
         "economically the ranking flips to CBM (4.02) -- bounded, in-sample"],
    ]
    _draw_table(ax, rows, top=0.815, bottom=0.06,
                col_x=[0.06, 0.31, 0.55, 0.78], col_w=[0.25, 0.24, 0.23, 0.18],
                header_bg="#222222", fs=7.0)
    pdf.savefig(fig)
    plt.close(fig)


def skillmap_page(pdf, job_title, subtitle, rows):
    fig, ax = new_page(pdf)
    disclaimer_band(ax, y=0.985)
    ax.text(0.06, 0.885, job_title, fontsize=15, fontweight="bold",
            color=INK, transform=ax.transAxes)
    ax.text(0.06, 0.862, subtitle, fontsize=8.5, color=MUTED,
            transform=ax.transAxes)
    header = ["Requirement", "Repo / artifact", "Proof (synthetic unless noted)"]
    _draw_table(ax, [header] + rows, top=0.83, bottom=0.05,
                col_x=[0.06, 0.40, 0.68], col_w=[0.33, 0.27, 0.26],
                header_bg=ACCENT, fs=7.4)
    pdf.savefig(fig)
    plt.close(fig)


def _draw_table(ax, rows, top, bottom, col_x, col_w, header_bg, fs=8.0):
    n = len(rows)
    rh = (top - bottom) / n
    for i, row in enumerate(rows):
        y = top - i * rh
        is_head = i == 0
        if is_head:
            ax.add_patch(plt.Rectangle((0.06, y - rh), 0.88, rh,
                         transform=ax.transAxes, facecolor=header_bg,
                         edgecolor="none", zorder=1))
        elif i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.06, y - rh), 0.88, rh,
                         transform=ax.transAxes, facecolor="#f4f4f4",
                         edgecolor="none", zorder=0))
        for cx, cw, cell in zip(col_x, col_w, row, strict=True):
            color = "white" if is_head else INK
            weight = "bold" if is_head else "normal"
            lines = _wrap(str(cell), max(10, int(cw * 150)))
            ax.text(cx, y - rh / 2 + (len(lines) - 1) * 0.006,
                    "\n".join(lines), transform=ax.transAxes, fontsize=fs,
                    color=color, va="center", fontweight=weight)
    ax.plot([0.06, 0.94], [top, top], color=RULE, lw=0.6, transform=ax.transAxes)
    ax.plot([0.06, 0.94], [bottom, bottom], color=RULE, lw=0.6,
            transform=ax.transAxes)


JOB1_ROWS = [
    ["Build AI-agent workflows -- and measure how they fail",
     "agentic-automation-lab (+ eval/reliability.py benchmark + "
     "eval/verification.py content-verification layer)",
     "agentic tool-use loops; reliability benchmark (1,350 seeded trials): "
     "content faults fail silently past the guards and retries can't zero "
     "them (assumed fault rates, stated); content-verification layer replays "
     "the same fault schedule: delivered-correct 88.7% -> 98.8%, silent-wrong "
     "11,523/yr -> 0 on that schedule (escalations 260 -> 1,300/yr stated; "
     "prose blind spot unit-tested); 71 tests"],
    ["Agentic integration via an open standard (MCP)",
     "chain-mcp (official mcp Python SDK; Claude Desktop / Code configs)",
     "6 real engines as AI-callable tools; typed schemas; never-crash errors; "
     "contract-enforced machine-readable result provenance (data label + "
     "engine commit + determinism flag); idempotency + result caching -- the "
     "key binds args + the exact engine checkout, and every success says "
     "computed-or-replayed (provenance.cache, contract-required); 193 tests "
     "incl. live JSON-RPC handshake"],
    ["Low-code (n8n / Power Automate)", "agentic-automation-lab: n8n/rfq_intake_agent.json",
     "RFQ-intake agent; ~EUR625k/yr"],
    ["Visual / flow-based building", "agent-flow-studio (+ estimator.js dry-run estimator)",
     "flow builder; ~EUR47k/yr; dry-run cost/latency estimator: declared rate "
     "card, branch scenarios enumerated and proven against real engine runs "
     "branch-for-branch -- 'emphatically not a bill' (78 node tests)"],
    ["Connecting systems / APIs", "agentic-automation-lab connector layer",
     "agents call external APIs"],
    ["Process automation (back-office)", "doc-extract-agent", "RFQ/invoice -> structured"],
    ["Document intake / understanding",
     "doc-extract-agent + 7-rule validation layer + cost model (eval/run_cost)",
     "extract + validate; ~EUR145k/yr; combined-gate precision 70.0% -> 87.5%; "
     "cost model: auto-post pays only above 98.4% precision -- the gate alone "
     "would lose money (modeled), the pre-fill carries the value"],
    ["Rapid prototyping", "agent-flow-studio, agentic-automation-lab, logistics-flow-studio",
     "runnable prototypes incl. a full installable offline WMS twin + "
     "factory/plant simulator (PWA, v3.19; 45 harnesses + 112/112 self-test)"],
    ["Prototyping + education (hype-free)",
     "quantum-explainer -- LIVE: dimitres-kisimov.github.io/quantum-explainer; "
     "bio-efficient-ai (learned BioHash vs random, public MNIST benchmark)",
     "hand-written simulator ~300 lines, zero deps; lessons incl. superdense "
     "coding (no-FTL demo -- the encoded pair is locally invisible; Holevo's "
     "bound respected, not beaten); 201 physics assertions + 53 self-test + "
     "93 structural checks pass; BioHash: mid-range wins from a 10x smaller "
     "circuit -- negatives kept (both tips lost, no memory-frontier point, "
     "corpus-dependent)"],
    ["Show automation ROI", "automation-roi-explorer", "EUR383k/yr net modelled"],
    ["Python engineering", "all automation repos", "Python throughout"],
    ["Stakeholder communication", "automation-roi-explorer", "business-readable ROI views"],
]

JOB2_ROWS = [
    ["One dataset through the whole chain (real data + labelled layers)",
     "decision-chain (run artifact + offline dashboard; FAIL path per identity)",
     "13/13 reconciliation identities PASS + additive (n), (o), (p), (q); "
     "cross-repo revenue GBP 19,643,861.62 to the penny; ledger to the cent; "
     "forecast-error elasticity == holding share exactly (0.0580); per-order "
     "cost-to-serve to the cent over 4,151 real orders -- top decile 59.0%, "
     "Gini 0.665 (model shape, not profitability); fleet knob swept with every "
     "day's CVRP re-solved: only transport moves, vans unpriced (not fleet "
     "advice); naive wins lumpy (MASE 1.782); slotting optimum -1.6% vs ABC; "
     "CVRP -0.2% vs Clarke-Wright; cost rates labelled INVENTED"],
    ["BI / Power BI", "revops-optimizer: powerbi/DAX_measures.md + kpi_uplift_risk",
     "DAX pack + 3-page report + Monte-Carlo P10/P50/P90 risk table w/ DAX"],
    ["KPI dashboards / metrics + fair performance measurement",
     "sales-kpi-analytics + pacing bullet chart + repperf.py",
     "KPI layer + exec PDF; pacing EUR10.91M = 95.7% of plan, 80% interval; "
     "back-check: realised EUR11.28M landed above the band -- honest miss; "
     "rep decomposition (indirect standardization): 92% of the league-table "
     "dispersion is territory, only 8% execution"],
    ["Uncertainty / risk quantification",
     "revops-optimizer simulate.py + robustness.py; ml-models-lab BENCHMARK_CI.md",
     "P10-P90 EUR145,091..170,723/yr, ~43% chance of clearing the headline; "
     "tornado ranks drivers; price-move gate: 17/29 ACCEPT, the biggest move "
     "HELD (67% carry) -- a screen, not a guarantee; bootstrap skill CIs: "
     "churn +0.457 [+0.381, +0.528]"],
    ["Inventory policy / working capital",
     "distributor-intelligence-platform dip/inventory.py + dip/reliability.py; "
     "supply-network-opt frontier",
     "ROP/EOQ at ABC-XYZ targets: EUR127,421 working capital (cycle+safety "
     "exactly), 5.5x turns, 99.9% fill; supplier reliability: measured lead "
     "times cost +14.4% safety stock -- wobble is 3/4 of the bill; frontier "
     "6.3x convexity"],
    ["Predictive analytics / forecasting",
     "sales-kpi-analytics; ml-models-lab global forecaster",
     "MASE < 1; MASE 0.987 / RMSSE 0.948 beats naive + Holt-Winters"],
    ["Forecasting rigour + reconciliation guard",
     "distributor-intelligence-platform (MRO command center)",
     "MASE 0.38 (9 rolling folds); /reconcile guard renders a green 'no silent drift' verdict over "
     "16/16 cross-engine identities with all 21 headline numbers present"],
    ["Energy forecasting + optimization",
     "energy-demand-forecast (forecasters + LP + dispatch backtest + "
     "degree-day decomposition; 72 tests)",
     "MASE 0.497 / MAPE 4.8%, 14/14 folds (Holt-Winters loses to naive, reported); "
     "peak 368.2 -> 291.1 kW (-20.9%); ~EUR11,100/yr at ASSUMED EUR12/kW-month; "
     "timer baseline EUR0; battery does not pay back on these assumptions; "
     "causal backtest captures 72.7% of the LP bound (robust variant loses); "
     "decomposition recovers designed balance points exactly -- weather 4.5% "
     "of energy, 18% of the July peak (modelled attribution, not a sub-meter)"],
    ["Python for analytics", "sales-kpi-analytics, revops-optimizer", "end-to-end pipelines"],
    ["SQL / data modelling", "sales-kpi-analytics SQL set", "spend analysis queries"],
    ["Excel-level tabular analysis", "sales-kpi-analytics", "spend breakdowns"],
    ["Optimization / prescriptive",
     "revops-optimizer; supply-network-opt; logistics-digital-twin",
     "~EUR160k/yr; -21.2% cost vs greedy; fill 2.0% -> 30.2% (CP-SAT proof)"],
    ["Elasticity / statistical modelling",
     "revops-optimizer; ml-models-lab (+ ablation -> docs/ABLATION.md, drift-gated)",
     "ROC-AUC 0.99; elasticity bias +1.52 -> +0.03; churn ECE 0.197 -> 0.021, "
     "bootstrap skill CI +0.457 [+0.381, +0.528]; ablation: freq_slope knockout "
     "-0.247 PR-AUC, endogeneity-control knockout +1.446 RMSE; the calibration "
     "knockout's bit-identical PR-AUC is the kept honest exception; null "
     "knockouts not counted as wins (numpy only, CI-reproducible)"],
    ["Data into business decisions", "sales-kpi-analytics; market-basket-analysis",
     "EUR2.6M leakage lever; cross-sell recs, top lift 2.41"],
    ["Market-basket / cross-sell", "market-basket-analysis + affinity.py + redundancy.py",
     "Apriori + FP-growth from scratch; 224 itemsets, 254 rules; affinity "
     "network Q=0.58, 3 communities, 4 bridges; 41% of rules redundant -- "
     "149 carry all the information; 68 tests"],
    ["Classification / anomaly detection", "ml-models-lab; fraud-detection-ops",
     "SKU macro-F1 0.963; AE PR-AUC 0.963 vs PCA 0.951 (PCA default); fraud "
     "PR-AUC 0.270 vs oracle ceiling 0.367; 55 tests"],
    ["Model lifecycle / MLOps (gated retrain)",
     "fraud-detection-ops challenger.py + feedback.py",
     "swap-set + five pre-declared gates -> PROMOTE at $8,632 vs $8,841; "
     "retrain finds no new fraud, wins by shedding load ($8/review assumption, "
     "stated); selective-labels feedback sim: ranking survives censoring "
     "(PR-AUC 0.268-0.273) but probabilities die -- alerts starve 651 -> 197 "
     "while the arm's own dashboard reads 100% recall by construction"],
    ["Reliability / maintenance (survival)",
     "predictive-maintenance pdm/policy.py + pdm/cbm_tuning.py",
     "censored Weibull beta 4.81; age-replacement T* 44.4 d at 7.16/machine-day "
     "beats the repo's own detector (8.28) at the default threshold -- reported; "
     "re-tuned economically the ranking flips to CBM (4.02, break-even "
     "inspection cost 553.3) -- bounded, in-sample; 80 tests"],
    ["Visual quality inspection (vision)",
     "quality-anomaly-vision (3 detectors, pre-registered rule; SPC + OCAP; 59 tests)",
     "AE ROC-AUC 0.779 vs PCA 0.772 -- inside 0.02 margin, PCA recommended; "
     "TPR 0.407 vs 0.393 @ 5% FPR; texture-breaks hard for all (best 0.609); "
     "SPC p-chart + WE rules; calibration correction 0 -> 0.70% measured; "
     "measured OCAP: label-free threshold re-centering is a trap (bit-identical "
     "ROC-AUC, 1.1/15 defects at +0.10 drift); refit on 200 verified-clean "
     "frames recovers ~99% of the drift cost"],
    ["Warehouse / intralogistics + factory / process industry",
     "logistics-flow-studio (WarehouseTwin v3.19); logistics-digital-twin (engine)",
     "WMS twin + factory/plant sim: keyword-generated layout, WMS flow w/ ISO 22400 "
     "KPIs, live material flow + KPI dashboard, Story Mode tour, an 894-element "
     "signature plant (29 object types), a user-definable object library, "
     "multi-way line sim (QA-split 112.5 parts/hr, ~88.1% eff.) + fluids "
     "solver (modelled, not measured), BYO CSV "
     "import + floor-plan underlay; -48.6% pick travel; ABC ~21% > random; 112/112 "
     "self-test + 45 harnesses; engine slotting -44.2% (golden-zone 25% -> 100%), "
     "fill 2.0% -> 30.2%; DES -76.1% / -66.5%; pick-path routing: return +3.0% "
     "vs exact optimum, optimized layout ~46% shorter; batching: savings "
     "-71.3%, routing flips to largest-gap (+1.2%)"],
    ["Logistics / ops analytics",
     "route-optimizer (46 tests, fleetmix.py); supply-network-opt (71 tests, growth.py)",
     "4.6% / 31% savings; robustness: 5% headroom cuts failures 96% -> 44%, "
     "expected day -4.6%; fleet mix (FSM): 5 large vans -17.5% vs 10 mediums "
     "with the service price shown (longest route +25.2%); a genuine mix wins "
     "the small instance (-8.5%; illustrative catalogue); safety stock -65.7% / "
     "-80.1%; frontier 6.3x; growth plan: +8.8% headroom, 4th DC first pays at "
     "1.30x (planning estimates)"],
    ["Real, messy data (completed)",
     "retail-analytics-real (UCI Online Retail II, 1,067,371 real rows, CC BY 4.0)",
     "real data: 94.0% rows kept; GBP 19.6M revenue; returns 3.65% of gross, "
     "95.0% of value matched, median 10-day lag; Champions 25% -> 69.0%; "
     "lifecycle: resurrections outnumber repeats (439 vs 390/month); "
     "seasonal-naive wins CV, MASE 1.094"],
    ["Present to decision-makers", "revops-optimizer exec deck", "exec narrative deck"],
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with PdfPages(OUT_PATH) as pdf:
        cover(pdf)
        opportunity_page(pdf)
        skillmap_page(pdf, "Job #1 -- (Agentic) Automation with Low-code",
                      "Every posting requirement -> repo + artifact + measured "
                      "proof (all synthetic data).", JOB1_ROWS)
        skillmap_page(pdf, "Job #2 -- Data & AI Analytics",
                      "Every posting requirement -> repo + artifact + measured "
                      "proof (synthetic data unless labelled real data).", JOB2_ROWS)
        d = pdf.infodict()
        d["Title"] = "Wuerth Data & AI Case Study (independent, public-info)"
        d["Author"] = "Dimitres Kisimov"
        d["Subject"] = "Independent Data & AI opportunity map + skill evidence"

    size = os.path.getsize(OUT_PATH)
    print(f"[OK] wrote {OUT_PATH} ({size} bytes, {size / 1024:.1f} KB)")
    if size < 10 * 1024:
        print("[WARN] PDF smaller than 10 KB")
        sys.exit(1)


if __name__ == "__main__":
    main()
