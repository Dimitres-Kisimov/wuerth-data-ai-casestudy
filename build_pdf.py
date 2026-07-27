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
        "measured in my own portfolio (now 21+ repositories, including the "
        "decision-chain integration capstone -- one real dataset through the "
        "whole distributor chain with 13 machine-checked reconciliation "
        "identities -- an MCP agentic-integration server, two "
        "warehouse-logistics flagships, a supply-network optimizer, an energy "
        "forecasting + peak-shaving study, a visual quality-inspection study, "
        "and a live installable quantum-explainer PWA). The euro and accuracy "
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
        ["Procurement / assortment / cross-sell", "MILP vs greedy; Apriori/FP-growth",
         "revops-optimizer, market-basket-analysis",
         "MILP > greedy; 254 rules, top lift 2.41"],
        ["Pricing & margin", "Elasticity + leakage; endogeneity fix",
         "sales-kpi-analytics, ml-models-lab",
         "EUR2.6M leakage lever; bias +1.52 -> +0.03"],
        ["Inventory / replenishment", "Newsvendor + forecast",
         "distributor-intel-platform, ml-models-lab",
         "MASE 0.38; MASE 0.987 / RMSSE 0.948 (beats naive + Holt-Winters)"],
        ["Sales KPIs & analytics", "KPIs + rolling-origin CV",
         "sales-kpi-analytics", "MASE < 1; exec PDF"],
        ["Logistics / routing", "OR-Tools CP-SAT VRP", "route-optimizer",
         "4.6% / 31% savings"],
        ["E-procurement automation", "Agentic + n8n low-code",
         "agentic-automation-lab", "~EUR625k/yr modelled"],
        ["Document processing", "Agentic RFQ/invoice extract", "doc-extract-agent",
         "~EUR145k/yr modelled"],
        ["Customer retention", "Decline + churn classifiers",
         "revops-optimizer, ml-models-lab",
         "ROC-AUC 0.99; churn ECE 0.197 -> 0.021"],
        ["Warehouse / intralogistics (new)", "Digital twin + slotting + DES + packing",
         "logistics-flow-studio, logistics-digital-twin",
         "-48.6% pick travel; slotting -44.2%; fill 2.0% -> 30.2%"],
        ["Supply-network design (new)", "Facility MILP + flows + safety stock",
         "supply-network-opt",
         "-21.2% cost vs greedy; stock -65.7% / -80.1%"],
        ["Energy management / facilities (new)", "Load forecast (rolling CV) + peak-shaving LP",
         "energy-demand-forecast",
         "MASE 0.497, 14/14 folds (Holt-Winters loses to naive, reported); "
         "peak -20.9%; ~EUR11,100/yr at ASSUMED tariff; battery does not pay back "
         "on these assumptions"],
        ["Quality inspection (new)", "Clean-only anomaly detection; pre-registered rule",
         "quality-anomaly-vision",
         "AE 0.779 vs PCA 0.772 ROC-AUC -- inside 0.02 margin, PCA recommended; "
         "TPR 0.407 vs 0.393 @ 5% FPR"],
        ["Real data (completed)", "Cleaning + RFM + leakage-safe CV",
         "retail-analytics-real",
         "real data: seasonal-naive wins CV, MASE 1.094; Champions 25% -> 69.0%"],
        ["Chain integration & reconciliation (new)",
         "Provenance-tagged pipeline + identity ledger; MCP agentic layer",
         "decision-chain, chain-mcp",
         "real data + labelled layers: 13/13 identities PASS; cross-repo revenue "
         "GBP 19,643,861.62 to the penny; naive wins lumpy (MASE 1.782); "
         "slotting optimum -1.6% vs ABC; CVRP -0.2% vs Clarke-Wright"],
    ]
    _draw_table(ax, rows, top=0.815, bottom=0.06,
                col_x=[0.06, 0.31, 0.55, 0.78], col_w=[0.25, 0.24, 0.23, 0.18],
                header_bg="#222222")
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
    ["Build AI-agent workflows", "agentic-automation-lab", "agentic tool-use loops"],
    ["Agentic integration via an open standard (MCP)",
     "chain-mcp (official mcp Python SDK; Claude Desktop / Code configs)",
     "6 real engines as AI-callable tools; typed schemas; never-crash errors; "
     "per-tool honesty label; 20 tests incl. live JSON-RPC handshake"],
    ["Low-code (n8n / Power Automate)", "agentic-automation-lab: n8n/rfq_intake_agent.json",
     "RFQ-intake agent; ~EUR625k/yr"],
    ["Visual / flow-based building", "agent-flow-studio", "flow builder; ~EUR47k/yr"],
    ["Connecting systems / APIs", "agentic-automation-lab connector layer",
     "agents call external APIs"],
    ["Process automation (back-office)", "doc-extract-agent", "RFQ/invoice -> structured"],
    ["Document intake / understanding", "doc-extract-agent", "extract + validate; ~EUR145k/yr"],
    ["Rapid prototyping", "agent-flow-studio, agentic-automation-lab, logistics-flow-studio",
     "runnable prototypes incl. an installable offline PWA"],
    ["Prototyping + education (hype-free)",
     "quantum-explainer -- LIVE: dimitres-kisimov.github.io/quantum-explainer",
     "hand-written simulator ~300 lines, zero deps; 42 physics assertions + "
     "57 structural checks pass"],
    ["Show automation ROI", "automation-roi-explorer", "EUR383k/yr net modelled"],
    ["Python engineering", "all automation repos", "Python throughout"],
    ["Stakeholder communication", "automation-roi-explorer", "business-readable ROI views"],
]

JOB2_ROWS = [
    ["One dataset through the whole chain (real data + labelled layers)",
     "decision-chain (run artifact + offline dashboard + 110 tests)",
     "13/13 reconciliation identities PASS; cross-repo revenue GBP "
     "19,643,861.62 to the penny; ledger to the cent; naive wins lumpy "
     "(MASE 1.782); slotting optimum -1.6% vs ABC; CVRP -0.2% vs "
     "Clarke-Wright; crew 18% utilized; cost rates labelled INVENTED"],
    ["BI / Power BI", "revops-optimizer: powerbi/DAX_measures.md", "DAX pack + 3-page report"],
    ["KPI dashboards / metrics", "sales-kpi-analytics", "KPI layer + exec PDF"],
    ["Predictive analytics / forecasting",
     "sales-kpi-analytics; ml-models-lab global forecaster",
     "MASE < 1; MASE 0.987 / RMSSE 0.948 beats naive + Holt-Winters"],
    ["Forecasting rigour", "distributor-intel-platform", "MASE 0.38 (9 rolling folds)"],
    ["Energy forecasting + optimization",
     "energy-demand-forecast (forecasters + LP from scratch; 19 tests)",
     "MASE 0.497 / MAPE 4.8%, 14/14 folds (Holt-Winters loses to naive, reported); "
     "peak 368.2 -> 291.1 kW (-20.9%); ~EUR11,100/yr at ASSUMED EUR12/kW-month; "
     "timer baseline EUR0; battery does not pay back on these assumptions"],
    ["Python for analytics", "sales-kpi-analytics, revops-optimizer", "end-to-end pipelines"],
    ["SQL / data modelling", "sales-kpi-analytics SQL set", "spend analysis queries"],
    ["Excel-level tabular analysis", "sales-kpi-analytics", "spend breakdowns"],
    ["Optimization / prescriptive",
     "revops-optimizer; supply-network-opt; logistics-digital-twin",
     "~EUR160k/yr; -21.2% cost vs greedy; fill 2.0% -> 30.2% (CP-SAT proof)"],
    ["Elasticity / statistical modelling", "revops-optimizer; ml-models-lab",
     "ROC-AUC 0.99; elasticity bias +1.52 -> +0.03; churn ECE 0.197 -> 0.021"],
    ["Data into business decisions", "sales-kpi-analytics; market-basket-analysis",
     "EUR2.6M leakage lever; cross-sell recs, top lift 2.41"],
    ["Market-basket / cross-sell", "market-basket-analysis",
     "Apriori + FP-growth from scratch; 224 itemsets, 254 rules; 18 tests"],
    ["Classification / anomaly detection", "ml-models-lab",
     "SKU macro-F1 0.963; AE PR-AUC 0.963 vs PCA 0.951 (PCA default)"],
    ["Visual quality inspection (vision)",
     "quality-anomaly-vision (3 detectors, pre-registered rule; 15 tests)",
     "AE ROC-AUC 0.779 vs PCA 0.772 -- inside 0.02 margin, PCA recommended; "
     "TPR 0.407 vs 0.393 @ 5% FPR; texture-breaks hard for all (best 0.609)"],
    ["Warehouse / intralogistics",
     "logistics-flow-studio (WarehouseTwin); logistics-digital-twin",
     "-48.6% pick travel; ABC ~21% > random; BYO CSV import (in-browser, "
     "row-numbered validation) + floor-plan underlay w/ 2-point calibration; "
     "slotting -44.2%; DES -76.1% / -66.5%"],
    ["Logistics / ops analytics", "route-optimizer; supply-network-opt",
     "4.6% / 31% savings; safety stock -65.7% / -80.1%"],
    ["Real, messy data (completed)",
     "retail-analytics-real (UCI Online Retail II, 1,067,371 real rows, CC BY 4.0)",
     "real data: 94.0% rows kept; GBP 19.6M revenue; Champions 25% -> 69.0%; "
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
