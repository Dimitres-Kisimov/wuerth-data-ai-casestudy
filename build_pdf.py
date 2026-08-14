"""Build the executive PDF for the Wuerth Data & AI case study.

Independent, public-info-only analysis. Not affiliated with Wuerth. No internal
Wuerth data or systems used. All portfolio metrics are on SYNTHETIC data except
retail-analytics-real, which is measured on real UCI Online Retail II data
(CC BY 4.0) and labelled REAL DATA wherever cited.

Layout engine ("dossier" pass): every table cell is measured with the actual
font metrics (Agg renderer), wrapped to its column width, and rows take the
height their content needs -- tables flow across pages with a repeated header
row instead of cramming into one fixed grid. Consistent margins, a running
header, hairline (booktabs-style) rules and page numbers throughout. The cover
carries one oversized figure -- the number of mapped requirements -- computed at
build time from the repository's own validation guards, never hard-coded.

Usage:
    python build_pdf.py
Writes deliverables/wuerth_data_ai_casestudy.pdf (multi-page, executive).
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
# Render every string verbatim: '$' is a currency sign in this document, never
# a mathtext delimiter (otherwise "$2,353 -> $14,750" would be typeset as math).
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

# Windows-console-safe stdout (ASCII markers used anyway, but be defensive).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Make the validation package importable when run from anywhere.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT_DIR = "deliverables"
OUT_PATH = os.path.join(OUT_DIR, "wuerth_data_ai_casestudy.pdf")

INK = "#1a1a1a"
MUTED = "#555555"
ACCENT = "#c8102e"  # a neutral red, not a logo asset
RULE = "#cccccc"
NOTICE_BG = "#fdf3f4"
NOTICE_INK = "#7a1420"

SANS = "DejaVu Sans"
MONO = "DejaVu Sans Mono"

# ---------------------------------------------------------------- page geometry
PAGE_W, PAGE_H = 8.27, 11.69  # A4 portrait, inches
MARGIN_L = 0.75
MARGIN_R = 0.75
MARGIN_B = 0.95  # room for the footer furniture
BODY_TOP = 1.05  # content starts below the running header
BODY_W = PAGE_W - MARGIN_L - MARGIN_R

LEAD = 1.42  # line-height multiple used for every measured text block
CELL_PAD_X = 0.07  # inches of horizontal padding inside a table cell
CELL_PAD_Y = 0.065  # inches of vertical padding above/below a table row


def X(x_in):
    """Inches from the left edge -> axes fraction."""
    return x_in / PAGE_W


def Y(y_in):
    """Inches from the TOP edge -> axes fraction."""
    return 1.0 - y_in / PAGE_H


# ------------------------------------------------------------- text measurement

_probe_fig = None
_probe_renderer = None
_width_cache = {}
_space_cache = {}


def _renderer():
    global _probe_fig, _probe_renderer
    if _probe_renderer is None:
        _probe_fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        _probe_renderer = FigureCanvasAgg(_probe_fig).get_renderer()
    return _probe_fig, _probe_renderer


def text_width(s, fs, weight="normal", family=SANS):
    """Measured width of a string, in inches, using the real font metrics."""
    key = (s, fs, weight, family)
    if key not in _width_cache:
        fig, renderer = _renderer()
        t = fig.text(0, 0, s, fontsize=fs, fontweight=weight, family=family)
        bb = t.get_window_extent(renderer=renderer)
        t.remove()
        _width_cache[key] = bb.width / fig.dpi
    return _width_cache[key]


def _space_width(fs, weight, family):
    key = (fs, weight, family)
    if key not in _space_cache:
        _space_cache[key] = text_width("i i", fs, weight, family) - 2 * text_width(
            "i", fs, weight, family
        )
    return _space_cache[key]


def _split_long(word, fs, maxw, weight, family):
    """Visual-only break of a token wider than its column (URLs, repo lists).

    Prefers existing '-' and '/' boundaries (the separator stays with the left
    fragment, standard typography); falls back to character packing. No
    characters are added or removed -- the string content is unchanged.
    """
    frags, cur = [], ""
    for ch in word:
        cur += ch
        if ch in "-/":
            frags.append(cur)
            cur = ""
    if cur:
        frags.append(cur)

    pieces, cur = [], ""
    for frag in frags:
        cand = cur + frag
        if cur and text_width(cand, fs, weight, family) > maxw:
            pieces.append(cur)
            cur = frag
        else:
            cur = cand
    if cur:
        pieces.append(cur)

    out = []
    for piece in pieces:
        if text_width(piece, fs, weight, family) <= maxw:
            out.append(piece)
            continue
        chunk = ""
        for ch in piece:
            if chunk and text_width(chunk + ch, fs, weight, family) > maxw:
                out.append(chunk)
                chunk = ch
            else:
                chunk += ch
        if chunk:
            out.append(chunk)
    return out


def wrap_measured(text, fs, maxw, weight="normal", family=SANS):
    """Greedy word wrap against measured glyph widths (2% safety margin)."""
    limit = maxw * 0.98
    words = []
    for w in str(text).split():
        if text_width(w, fs, weight, family) <= limit:
            words.append(w)
        else:
            words.extend(_split_long(w, fs, limit, weight, family))

    space = _space_width(fs, weight, family)
    lines, cur, cur_w = [], [], 0.0
    for w in words:
        ww = text_width(w, fs, weight, family)
        if cur and cur_w + space + ww > limit:
            lines.append(" ".join(cur))
            cur, cur_w = [w], ww
        else:
            cur.append(w)
            cur_w = cur_w + space + ww if cur else ww
            if len(cur) == 1:
                cur_w = ww
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]


def block_height(n_lines, fs):
    """Height in inches of an n-line text block at the shared leading."""
    return n_lines * fs * LEAD / 72.0


# ------------------------------------------------------------------- document

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

FOOTER_LEFT = "Independent, public-info analysis -- not affiliated with the Wuerth Group"
RUNNING_TITLE = "DATA & AI CASE STUDY"


class Doc:
    """Collects pages, then stamps footers with final page numbers and saves."""

    def __init__(self):
        self.pages = []

    def new_page(self, section=None):
        fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        if section:
            ax.text(X(MARGIN_L), Y(0.58), RUNNING_TITLE, fontsize=6.3,
                    color=MUTED, family=SANS, fontweight="bold", va="bottom")
            ax.text(X(PAGE_W - MARGIN_R), Y(0.58), section.upper(), fontsize=6.3,
                    color=MUTED, family=SANS, va="bottom", ha="right")
            hairline(ax, 0.66, lw=0.6)
        self.pages.append((fig, ax))
        return fig, ax

    def finalize(self, path):
        n = len(self.pages)
        with PdfPages(path) as pdf:
            for i, (fig, ax) in enumerate(self.pages):
                hairline(ax, PAGE_H - 0.68, lw=0.6)
                ax.text(X(MARGIN_L), Y(PAGE_H - 0.60), FOOTER_LEFT,
                        fontsize=6.3, color=MUTED, family=SANS, va="top")
                ax.text(X(PAGE_W - MARGIN_R), Y(PAGE_H - 0.60), f"{i + 1} / {n}",
                        fontsize=6.3, color=MUTED, family=MONO, va="top", ha="right")
                pdf.savefig(fig)
                plt.close(fig)
            d = pdf.infodict()
            d["Title"] = "Wuerth Data & AI Case Study (independent, public-info)"
            d["Author"] = "Dimitres Kisimov"
            d["Subject"] = "Independent Data & AI opportunity map + skill evidence"
        return n


def hairline(ax, y_in, lw=0.5, color=RULE, x0=MARGIN_L, x1=PAGE_W - MARGIN_R):
    ax.plot([X(x0), X(x1)], [Y(y_in), Y(y_in)], color=color, lw=lw,
            solid_capstyle="butt")


def paragraph(ax, y_in, text, fs, color=INK, weight="normal", family=SANS,
              width=BODY_W, x_in=MARGIN_L):
    """Paint a measured, wrapped paragraph; returns the y below it (inches)."""
    lines = wrap_measured(text, fs, width, weight, family)
    ax.text(X(x_in), Y(y_in), "\n".join(lines), fontsize=fs, color=color,
            fontweight=weight, family=family, va="top", linespacing=LEAD)
    return y_in + block_height(len(lines), fs)


def disclaimer_band(ax, y_in):
    """The unchanged disclaimer, set as a designed notice: light tint, red
    left-hand rule, measured height. Returns the y below the band."""
    fs = 6.6
    pad = 0.12
    inner_w = BODY_W - 2 * pad - 0.04
    lines = wrap_measured(DISCLAIMER, fs, inner_w)
    h = block_height(len(lines), fs) + 2 * pad
    ax.add_patch(plt.Rectangle((X(MARGIN_L), Y(y_in + h)), BODY_W / PAGE_W,
                               h / PAGE_H, facecolor=NOTICE_BG, edgecolor="none",
                               zorder=0))
    ax.plot([X(MARGIN_L), X(MARGIN_L)], [Y(y_in), Y(y_in + h)], color=ACCENT,
            lw=2.2, solid_capstyle="butt")
    ax.text(X(MARGIN_L + pad + 0.04), Y(y_in + pad), "\n".join(lines),
            fontsize=fs, color=NOTICE_INK, family=SANS, va="top",
            linespacing=LEAD)
    return y_in + h


# ------------------------------------------------------------------ table engine

def layout_row(cells, widths, fs_list, weights, families):
    """Wrap every cell; return (wrapped_cells, row_height_inches)."""
    wrapped = []
    n_max = 1
    tallest = 0.0
    for cell, w, fs, weight, family in zip(cells, widths, fs_list, weights,
                                           families, strict=True):
        lines = wrap_measured(cell, fs, w - 2 * CELL_PAD_X, weight, family)
        wrapped.append(lines)
        n_max = max(n_max, len(lines))
        tallest = max(tallest, block_height(len(lines), fs))
    return wrapped, tallest + 2 * CELL_PAD_Y


def paint_row(ax, y_in, wrapped, widths, fs_list, weights, families, colors):
    x = MARGIN_L
    for lines, w, fs, weight, family, color in zip(wrapped, widths, fs_list,
                                                   weights, families, colors,
                                                   strict=True):
        ax.text(X(x + CELL_PAD_X), Y(y_in + CELL_PAD_Y), "\n".join(lines),
                fontsize=fs, color=color, fontweight=weight, family=family,
                va="top", linespacing=LEAD)
        x += w


class TableStyle:
    """Booktabs-style evidence table: hairline rules, no fills, measured rows."""

    def __init__(self, widths, fs_list, weights, families):
        self.widths = widths
        self.fs_list = fs_list
        self.weights = weights
        self.families = families
        self.head_fs = [6.8] * len(widths)
        self.head_weights = ["bold"] * len(widths)
        self.head_families = [SANS] * len(widths)

    def header_layout(self, header):
        return layout_row(header, self.widths, self.head_fs,
                          self.head_weights, self.head_families)

    def paint_header(self, ax, y_in, header_wrapped, header_h):
        hairline(ax, y_in, lw=1.1, color=INK)
        paint_row(ax, y_in, header_wrapped, self.widths, self.head_fs,
                  self.head_weights, self.head_families, [MUTED] * len(self.widths))
        hairline(ax, y_in + header_h, lw=0.5, color=INK)
        return y_in + header_h

    def row_layout(self, row):
        return layout_row(row, self.widths, self.fs_list, self.weights,
                          self.families)

    def paint_body_row(self, ax, y_in, wrapped, h, last):
        colors = [INK] * len(self.widths)
        paint_row(ax, y_in, wrapped, self.widths, self.fs_list, self.weights,
                  self.families, colors)
        y_next = y_in + h
        hairline(ax, y_next, lw=1.1 if last else 0.4,
                 color=INK if last else RULE)
        return y_next


def section_title(ax, y_in, index, title, subtitle):
    """Numbered section heading; returns y below the heading block."""
    ax.text(X(MARGIN_L), Y(y_in), f"{index:02d}", fontsize=9.5, color=ACCENT,
            family=MONO, fontweight="bold", va="top")
    y = y_in + 0.20
    ax.text(X(MARGIN_L), Y(y), title, fontsize=16, fontweight="bold",
            color=INK, family=SANS, va="top")
    y += 0.30
    y = paragraph(ax, y, subtitle, 8.2, color=MUTED)
    return y + 0.14


def table_section(doc, index, section_label, title, subtitle, header, rows,
                  style):
    """One numbered section whose table flows across as many pages as it needs."""
    fig, ax = doc.new_page(section_label)
    y = disclaimer_band(ax, BODY_TOP) + 0.26
    y = section_title(ax, y, index, title, subtitle)

    header_wrapped, header_h = style.header_layout(header)
    y = style.paint_header(ax, y, header_wrapped, header_h)

    limit = PAGE_H - MARGIN_B
    for i, row in enumerate(rows):
        wrapped, h = style.row_layout(row)
        if y + h > limit:
            hairline(ax, y, lw=1.1, color=INK)  # close the table on this page
            fig, ax = doc.new_page(section_label)
            y = BODY_TOP
            ax.text(X(MARGIN_L), Y(y), f"{title} (continued)", fontsize=8.0,
                    color=MUTED, family=SANS, style="italic", va="top")
            y += 0.24
            y = style.paint_header(ax, y, header_wrapped, header_h)
        last = i == len(rows) - 1
        y = style.paint_body_row(ax, y, wrapped, h, last)


# ------------------------------------------------------------- build-time stats

def gather_stats():
    """Figures for the cover, computed from the repo's own validation guards.

    Nothing here is hard-coded: the requirement count comes from parsing
    docs/JOB_SKILL_MAP.md exactly the way validation/skill_coverage.py does,
    the repo count from the registry, and the check tallies from actually
    running both guard batteries (read-only; no reports are written).
    """
    from validation.consistency_check import load_registry
    from validation.consistency_check import run_all_checks as consistency_checks
    from validation.skill_coverage import parse_skill_map
    from validation.skill_coverage import run_all_checks as coverage_checks

    registry = load_registry()
    sm = parse_skill_map(registry)
    cc = consistency_checks()
    sc = coverage_checks(sm)
    return {
        "requirements": len(sm.requirements),
        "repos": len(registry),
        "consistency": (sum(1 for c in cc if c.passed), len(cc)),
        "coverage": (sum(1 for c in sc if c.passed), len(sc)),
    }


# --------------------------------------------------------------------- content

ROLES = [
    ("Job #1  --  (Agentic) Automation with Low-code Platforms",
     ("Agentic AI workflows, low-code (n8n / Power Automate), connecting "
      "systems & APIs, document automation, ROI, rapid prototyping.")),
    ("Job #2  --  Data & AI Analytics",
     ("BI / Power BI, KPI dashboards, forecasting & predictive analytics, "
      "Python & SQL, data modelling, turning data into decisions.")),
]

INTRO = (
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

WHO_TITLE = "Who Wuerth is (public info)"
WHO = (
    "Wuerth (public profile, approximate): a large family-owned German-HQ "
    "group in assembly/fastening and industrial MRO distribution -- ~400+ "
    "companies in 80+ countries, ~87,000 employees, ~EUR 20B+ revenue, a "
    "catalogue in the millions of articles, multi-channel (field sales, "
    "branches, e-commerce, e-procurement/EDI, ORSY inventory systems). A "
    "business that runs on assortment, pricing, availability, logistics, and "
    "high-volume transactional documents -- a natural fit for applied Data & AI."
)

BYLINE = ("Dimitres Kisimov  |  2026  |  all rights reserved "
          "(portfolio review)  |  metrics on synthetic data unless labelled "
          "real data")

OPPORTUNITY_HEADER = ["Area (public-info)", "Approach", "Repo",
                      "Result (synthetic -- labelled if real)"]

OPPORTUNITY_ROWS = [
    ["Procurement / assortment / cross-sell",
     "MILP vs greedy; Apriori/FP-growth; rule redundancy pruning",
     "revops-optimizer, market-basket-analysis",
     "MILP > greedy; 254 rules, top lift 2.41; 41% of rules redundant -- "
     "the 149 kept carry all the information"],
    ["Pricing & margin", "Elasticity + leakage; endogeneity fix; per-move robustness gate; ablation",
     "revops-optimizer, sales-kpi-analytics, ml-models-lab",
     "EUR2.6M leakage lever; bias +1.52 -> +0.03; price-move gate 17/29 ACCEPT -- "
     "the biggest move (45% of the pricing uplift) is HELD, stated as a screen; "
     "ablation: endogeneity-control knockout +1.446 RMSE -- the load-bearing piece; "
     "scenario compare: EUR159,966.19 -> EUR139,487.29 attributed to named drivers "
     "with a EUR0.00 residual -- pricing gains EUR7,382.88 while the assortment gap "
     "loses EUR23,895.20, and its two ORDERED drivers are disclosed"],
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
     "(indirect standardization): 92% of the league table is territory, 8% execution; "
     "concentration: HHI 68 company-wide but 2,064 inside one territory (the largest "
     "account is 35.76% of one rep's book) -- removal arithmetic on measured revenue, "
     "no churn modelled anywhere"],
    ["Logistics / routing", "OR-Tools CP-SAT VRP + robustness + Fleet Size and Mix VRP",
     "route-optimizer",
     "4.6% / 31% savings; 5% headroom: failing scenarios 96% -> 44%, "
     "expected day -4.6%; fleet mix: -17.5% vs the status quo with the "
     "service price shown (longest route +25.2%); driver shifts: the statutory "
     "limits are SLACK on this data (worst duty 267 of 600 min, 43 min of "
     "continuous-drive slack, zero breaks needed) -- capping at 210 min costs "
     "+17.5% km and an eleventh van, 180 min is infeasible at any fleet size; "
     "informed by EU 561/2006, not a compliance tool"],
    ["E-procurement automation",
     "Agentic + n8n low-code + reliability benchmark + content-verification "
     "layer + dry-run flow cost estimator",
     "agentic-automation-lab, agent-flow-studio",
     "~EUR625k/yr modelled; 1,350 seeded trials: content faults fail "
     "silently, stated (assumed rates); verification layer on the same "
     "fault schedule: 88.7% -> 98.8% delivered-correct, silent-wrong "
     "11,523/yr -> 0 (price stated; 100 tests); flow estimator: "
     "engine-verified branch scenarios, 'not a bill' (declared rates); "
     "HITL checkpoints priced per placement: risk-gated review takes "
     "silent-wrong 11,523/yr -> 0 for EUR88,948/yr = EUR7.65 per prevented "
     "error, per-step approval costs EUR349,708/yr and buys nothing extra, "
     "and a skipped validation is MISSED at pre-commit -- the reviewer is "
     "modelled generously, so catch rates are upper bounds"],
    ["Document processing", "Agentic extract + 7-rule validation gate + cost model",
     "doc-extract-agent",
     "~EUR145k/yr modelled; combined-gate precision 70.0% -> 87.5%; cost model: "
     "auto-post pays only above 98.4% precision -- the gate alone would lose "
     "money (modeled), the pre-fill carries the value; source spans: every read "
     "value underlined where it was read (25 of 26 located, 1 derived marked "
     "'no span'), verified across all 30 committed documents -- a character "
     "range, never a pixel region"],
    ["Customer retention", "Decline + churn classifiers + ablation",
     "revops-optimizer, ml-models-lab",
     "ROC-AUC 0.99; churn ECE 0.197 -> 0.021; "
     "bootstrap skill CI +0.457 [+0.381, +0.528]; ablation: freq_slope "
     "knockout -0.247 PR-AUC; null knockouts not counted as wins"],
    ["Warehouse / WMS (new)",
     "WMS twin + factory/plant sim (Story Mode, 894-element plant, definable objects, "
     "multi-way line sim + fluids solver); slotting + DES + packing + pick-path routing "
     "+ order batching",
     "logistics-flow-studio (WarehouseTwin v3.24), logistics-digital-twin (engine)",
     "-48.6% pick travel; ABC ~21% > random; ISO 22400 KPIs; 149/149 self-test + 49 harnesses; "
     "line sim 112.5 parts/hr (~88.1% eff.); fluids solver (modelled); "
     "engine slotting -44.2% (golden-zone 25% -> 100%); fill 2.0% -> 30.2%; "
     "routing: return +3.0% vs exact optimum, optimized layout ~46% shorter; "
     "batching: savings -71.3%, routing flips to largest-gap; v3.21-v3.24 plant "
     "floor -- concrete + safety-yellow paint, living workers, pallet -> carton -> "
     "tote -> parcel, hauling forklifts, anti-strobe congestion bands, dock "
     "trailers (RENDERING, not model: no number, no export changes); floor plan: "
     "ABC-classed bays, a real pick tour 69.2 m vs its 64.4 m exact optimum (+7.5%)"],
    ["Supply-network design (new)",
     "Facility MILP + flows + safety stock + service frontier + growth plan",
     "supply-network-opt",
     "-21.2% cost vs greedy; stock -65.7% / -80.1%; "
     "frontier $2,353 -> $14,750 per service point (6.3x); "
     "growth: +8.8% headroom, 4th DC first pays at 1.30x (planning estimates); "
     "phased build: staged $2,750,462 NPV (DC0 yr 2, DC3 yr 6) vs a $2,598,732 "
     "free-redesign LOWER BOUND, building ahead +24.4%, no expansion fails in "
     "year 2 -- growth and discount rates illustrative, fixed cost as recurring "
     "opex not capex, no construction lead time"],
    ["Energy management / facilities (new)",
     "Load forecast (rolling CV) + peak-shaving LP + causal dispatch backtest "
     "+ degree-day decomposition",
     "energy-demand-forecast",
     "MASE 0.497, 14/14 folds (Holt-Winters loses to naive, reported); "
     "peak -20.9%; ~EUR11,100/yr at ASSUMED tariff; battery does not pay back "
     "on these assumptions; backtest captures 72.7% of the LP bound "
     "(robust variant loses, reported); decomposition recovers designed "
     "balance points exactly -- weather 4.5% of energy, 18% of the July peak "
     "(modelled attribution); battery sizing: at an ASSUMED EUR375/kWh the "
     "15-year break-even is EUR25/kWh-yr and only the 100 kWh system clears it "
     "(11.3-yr payback vs 18.6 at 400 kWh) -- and the linear per-kWh price is "
     "flagged as a caveat that cuts against the repo's own headline"],
    ["Quality inspection (new)",
     "Clean-only anomaly detection; pre-registered rule; SPC p-chart + WE rules; "
     "measured OCAP",
     "quality-anomaly-vision",
     "AE 0.779 vs PCA 0.772 ROC-AUC -- inside 0.02 margin, PCA recommended; "
     "TPR 0.407 vs 0.393 @ 5% FPR; calibration correction 0 -> 0.70% measured; "
     "OCAP: label-free re-centering is a trap (green chart, near-blind screen); "
     "refit on verified-clean frames recovers ~99% of the drift cost; severity "
     "grading: the bill rises 368 -> 509 EUR/1,000 parts (+39%) but THE DECISION "
     "DOES NOT MOVE (a critical escape needs 259 EUR, 7.4x, to shift it), and the "
     "expensive grade is the one the screen sees worst (critical AUC 0.706)"],
    ["Real data (completed)", "Cleaning + RFM + returns + lifecycle + leakage-safe CV",
     "retail-analytics-real",
     "real data: seasonal-naive wins CV, MASE 1.094; returns 3.65% of gross, "
     "95.0% of value matched, median 10-day lag; Champions 25% -> 69.0%; "
     "lifecycle: resurrections outnumber repeats (439 vs 390/month); price "
     "ladders: 88.7% of SKUs sold at more than one price, realization 98.6% "
     "('not an opportunity'), slopes -1.71 within-week / -1.67 market-adjusted "
     "with 74.1% beating a permutation null -- and NO elasticity claimed, "
     "nothing causal"],
    ["Chain integration & reconciliation (new)",
     "Provenance-tagged pipeline + identity ledger; MCP agentic layer w/ "
     "machine-readable result provenance + idempotent caching",
     "decision-chain, chain-mcp",
     "real data + labelled layers: 13/13 identities PASS + additive (n), (o), "
     "(p), (q); per-order spread to the cent over 4,151 orders (top decile "
     "59.0%, Gini 0.665); fleet knob: only the transport line moves, vans "
     "unpriced (model property, not fleet advice); cross-repo revenue "
     "GBP 19,643,861.62 to the penny; naive wins lumpy (MASE 1.782); "
     "contract-enforced provenance + cache-status, 193 tests; plan diff "
     "(synthetic): EUR136,972.20 -> EUR115,728.86 with every euro attributed to "
     "a named cause over 11 change identities and a -EUR0.02 rounding line "
     "against a EUR4.03 bound -- real, never fitted to close the gap"],
    ["Fraud & transaction-risk ops (new)",
     "Cost-based alerting; gated retrain promotion; selective-labels feedback sim",
     "fraud-detection-ops",
     "PR-AUC 0.270 vs oracle 0.367; swap-set gates -> PROMOTE at $8,632 vs "
     "$8,841 -- retrain finds no new fraud, wins by shedding load (stated); "
     "feedback sim: ranking survives censoring, probabilities + alerts collapse; "
     "reason codes: EXACT Shapley on the linear champion, checked against "
     "brute-force enumeration over all 2^m coalitions -- and the most common "
     "reason is not the most predictive one (merchant_category principal on "
     "40.5% but 11.4% fraud vs transaction_amount 19.1% / 20.7%); logits "
     "against a stated reference, not causal, not legal advice"],
    ["Maintenance & asset reliability (new)",
     "Censored Weibull + age-replacement vs condition-based + CBM re-tuning",
     "predictive-maintenance",
     "beta 4.81; T* = 44.4 d at 7.16/machine-day -- the calendar rule beats "
     "the repo's own detector at the default threshold, reported; re-tuned "
     "economically the ranking flips to CBM (4.02) -- bounded, in-sample; "
     "spares from the same fit: run-to-failure/CBM 0.0148 parts/machine-day "
     "(base stock 126) vs age replacement 0.0229 (188) -- the calendar rule "
     "draws +54% MORE PARTS while cutting the cost rate 51.7%; a modelled "
     "provisioning exercise, not an order"],
]

SKILL_HEADER = ["Requirement", "Repo / artifact", "Proof (synthetic unless noted)"]

JOB1_ROWS = [
    ["Build AI-agent workflows -- and measure how they fail",
     "agentic-automation-lab (+ eval/reliability.py benchmark + "
     "eval/verification.py content-verification layer)",
     "agentic tool-use loops; reliability benchmark (1,350 seeded trials): "
     "content faults fail silently past the guards and retries can't zero "
     "them (assumed fault rates, stated); content-verification layer replays "
     "the same fault schedule: delivered-correct 88.7% -> 98.8%, silent-wrong "
     "11,523/yr -> 0 on that schedule (escalations 260 -> 1,300/yr stated; "
     "prose blind spot unit-tested); and the review itself is now priced where "
     "it sits -- risk-gated approval takes silent-wrong to 0 for EUR88,948/yr "
     "(EUR7.65 per prevented error) while per-step approval costs EUR349,708/yr "
     "and buys nothing extra; 100 tests"],
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
     "would lose money (modeled), the pre-fill carries the value; source spans: "
     "every read value underlined where it was read (25 of 26 located, 1 derived "
     "marked 'no span'; a non-matching span is reported as NOT LOCATED), "
     "verified across all 30 committed documents"],
    ["Rapid prototyping", "agent-flow-studio, agentic-automation-lab, logistics-flow-studio",
     "runnable prototypes incl. a full installable offline WMS twin + "
     "factory/plant simulator (PWA, v3.24; 49 harnesses + 149/149 self-test), "
     "whose floor now reads like a working shift -- rendering, not model"],
    ["Prototyping + education (hype-free)",
     "quantum-explainer -- LIVE: dimitres-kisimov.github.io/quantum-explainer; "
     "bio-efficient-ai (learned BioHash vs random, public MNIST benchmark)",
     "hand-written simulator ~300 lines, zero deps; lessons incl. superdense "
     "coding (no-FTL demo -- the encoded pair is locally invisible; Holevo's "
     "bound respected, not beaten); 201 physics assertions + 53 self-test + "
     "93 structural checks pass; BioHash: mid-range wins from a 10x smaller "
     "circuit -- negatives kept (both tips lost, no memory-frontier point, "
     "corpus-dependent)"],
    ["Human-in-the-loop control of agentic actions (new row)",
     "agentic-automation-lab: src/agentic_lab/checkpoints.py + eval/checkpoints.py",
     "where the human sits, priced. A gate hands out a resumable, digest-stamped "
     "envelope, so an approved gate costs 0 extra tokens (restarting would cost "
     "7.90x more) and an edited envelope is refused. Five placements on the same "
     "fault schedule: none -> 11,523 silent-wrong/yr; risk-gated -> 0 for "
     "EUR88,948/yr = EUR7.65 per prevented error; pre-delivery EUR188,438/yr; "
     "every step EUR349,708/yr and buys nothing extra. Placement changes COVERAGE "
     "too -- a skipped validation is missed at pre-commit and every-step. The "
     "reviewer is modelled generously, so catch rates are upper bounds and the "
     "zero false-alarm rate says nothing about people; EUR labour and USD tokens "
     "reported side by side, never summed; 100 tests"],
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
     "dispersion is territory, only 8% execution; concentration: Gini 0.5476, "
     "HHI 68 company-wide (~148 effective accounts of 383) but 2,064 inside one "
     "territory, where the largest account is 35.76% of that rep's book -- "
     "removal arithmetic on measured revenue, no churn probability modelled"],
    ["Uncertainty / risk quantification",
     "revops-optimizer simulate.py + robustness.py; ml-models-lab BENCHMARK_CI.md",
     "P10-P90 EUR145,091..170,723/yr, ~43% chance of clearing the headline; "
     "tornado ranks drivers; price-move gate: 17/29 ACCEPT, the biggest move "
     "HELD (67% carry) -- a screen, not a guarantee; bootstrap skill CIs: "
     "churn +0.457 [+0.381, +0.528]; scenario compare: EUR159,966.19 -> "
     "EUR139,487.29 with every euro attributed to a named driver and a EUR0.00 "
     "residual (pricing gains EUR7,382.88 while the assortment gap loses "
     "EUR23,895.20) -- two ORDERED drivers disclosed, the gap shipped whole; "
     "91 tests"],
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
     "16/16 cross-engine identities with all 21 headline numbers present; new "
     "plan-diff station: EUR136,972.20 -> EUR115,728.86 with every euro attributed "
     "to a named cause over 11 change identities -- price moves -EUR29,931.98, "
     "drops -EUR150,919.35 against greedy re-picks +EUR150,224.01, routing "
     "+EUR9,384.00 and a -EUR0.02 rounding line against a EUR4.03 bound, real and "
     "never fitted to close the gap"],
    ["Energy forecasting + optimization",
     "energy-demand-forecast (forecasters + LP + dispatch backtest + "
     "degree-day decomposition; 72 tests)",
     "MASE 0.497 / MAPE 4.8%, 14/14 folds (Holt-Winters loses to naive, reported); "
     "peak 368.2 -> 291.1 kW (-20.9%); ~EUR11,100/yr at ASSUMED EUR12/kW-month; "
     "timer baseline EUR0; battery does not pay back on these assumptions; "
     "causal backtest captures 72.7% of the LP bound (robust variant loses); "
     "decomposition recovers designed balance points exactly -- weather 4.5% "
     "of energy, 18% of the July peak (modelled attribution, not a sub-meter); "
     "battery sizing on the same causal controller: break-even EUR25/kWh-yr at "
     "an ASSUMED EUR375/kWh, and only the 100 kWh system clears it (EUR33.3/"
     "kWh-yr, 11.3-yr payback) while 400 kWh buys 2.4x the saving for 4x the "
     "battery -- the linear per-kWh price is flagged as cutting against the "
     "repo's own headline"],
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
     "while the arm's own dashboard reads 100% recall by construction; 78 tests"],
    ["Reliability / maintenance (survival)",
     "predictive-maintenance pdm/policy.py + pdm/cbm_tuning.py",
     "censored Weibull beta 4.81; age-replacement T* 44.4 d at 7.16/machine-day "
     "beats the repo's own detector (8.28) at the default threshold -- reported; "
     "re-tuned economically the ranking flips to CBM (4.02, break-even "
     "inspection cost 553.3) -- bounded, in-sample; spares from the same fit: "
     "run-to-failure/CBM 0.0148 parts/machine-day (base stock 126) vs age "
     "replacement 0.0229 (188) -- the calendar rule draws +54% MORE PARTS while "
     "cutting the cost rate 51.7%; Poisson checked, not assumed (cycle CV 0.24 / "
     "0.07); a modelled provisioning exercise, NOT an order -- no lead time, no "
     "batching, counts units not money; 80 tests"],
    ["Visual quality inspection (vision)",
     "quality-anomaly-vision (3 detectors, pre-registered rule; SPC + OCAP; 59 tests)",
     "AE ROC-AUC 0.779 vs PCA 0.772 -- inside 0.02 margin, PCA recommended; "
     "TPR 0.407 vs 0.393 @ 5% FPR; texture-breaks hard for all (best 0.609); "
     "SPC p-chart + WE rules; calibration correction 0 -> 0.70% measured; "
     "measured OCAP: label-free threshold re-centering is a trap (bit-identical "
     "ROC-AUC, 1.1/15 defects at +0.10 drift); refit on 200 verified-clean "
     "frames recovers ~99% of the drift cost; severity grading: the bill rises "
     "368 -> 509 EUR/1,000 parts (+39%, 63% of it from 2.3 critical escapes) but "
     "the operating point does not move -- a critical escape needs 259 EUR (7.4x) "
     "before it does -- and critical AUC 0.706 vs 0.819 major: the expensive "
     "grade is the one the screen sees worst"],
    ["Explainability / decision transparency (new row)",
     "fraud-detection-ops: fdo/reasons.py (python -m fdo --reasons)",
     "reason codes in the shape regulated lending uses -- computed from the model "
     "already trained: no surrogate, no sampling, no randomness. The champion is "
     "linear in its standardized features, so against a stated reference profile "
     "(z(r) = -0.509) the per-feature terms ARE the Shapley values, asserted "
     "against brute-force enumeration over all 2^m coalitions rather than cited; "
     "the explained set is the same 608 alerts the shipped threshold fires. The "
     "finding is negative: the most common reason is not the most predictive one "
     "-- merchant_category is principal on 40.5% of alerts but confirms fraud "
     "only 11.4% of the time, while transaction_amount is principal on 19.1% and "
     "confirms 20.7%. Contributions are logits against a stated reference: not "
     "probabilities, not dollars, not causal -- and the four-reason format is "
     "borrowed from adverse-action practice as a discipline, not legal advice; "
     "78 tests"],
    ["Warehouse / intralogistics + factory / process industry",
     "logistics-flow-studio (WarehouseTwin v3.24); logistics-digital-twin (engine)",
     "WMS twin + factory/plant sim: keyword-generated layout, WMS flow w/ ISO 22400 "
     "KPIs, live material flow + KPI dashboard, Story Mode tour, an 894-element "
     "signature plant (29 object types), a user-definable object library, "
     "multi-way line sim (QA-split 112.5 parts/hr, ~88.1% eff.) + fluids "
     "solver (modelled, not measured), BYO CSV "
     "import + floor-plan underlay; -48.6% pick travel; ABC ~21% > random; 149/149 "
     "self-test + 49 harnesses; engine slotting -44.2% (golden-zone 25% -> 100%), "
     "fill 2.0% -> 30.2%; DES -76.1% / -66.5%; pick-path routing: return +3.0% "
     "vs exact optimum, optimized layout ~46% shorter; batching: savings "
     "-71.3%, routing flips to largest-gap (+1.2%); v3.21-v3.24 plant floor -- "
     "industrial materials, living workers with per-station task poses, physical "
     "goods (pallet-load -> carton -> tote -> parcel) on belts and forks, hauling "
     "forklifts, frame-rate-invariant anti-strobe congestion bands, dock trailers "
     "and an andon lamp: RENDERING, not model -- no number, no export changes; "
     "and the engine's result drawn on the floor it happens on (a renderer, not a "
     "new model): ABC-classed bays, a real pick tour 69.2 m against its 64.4 m "
     "exact optimum (+7.5%), batching plate 254.0 -> 66.8 m (-73.7%)"],
    ["Logistics / ops analytics",
     "route-optimizer (74 tests, fleetmix.py + shifts.py); supply-network-opt "
     "(71 tests, growth.py + phasing.py)",
     "4.6% / 31% savings; robustness: 5% headroom cuts failures 96% -> 44%, "
     "expected day -4.6%; fleet mix (FSM): 5 large vans -17.5% vs 10 mediums "
     "with the service price shown (longest route +25.2%); a genuine mix wins "
     "the small instance (-8.5%; illustrative catalogue); safety stock -65.7% / "
     "-80.1%; frontier 6.3x; growth plan: +8.8% headroom, 4th DC first pays at "
     "1.30x (planning estimates); driver shifts: the statutory limits are SLACK on "
     "this data (worst duty 267 of 600 min, 43 min of continuous-drive slack, "
     "zero breaks needed) -- capping at 240 min costs +5.3% km, 210 min +17.5% "
     "and an eleventh van, 180 min is infeasible at any fleet size (a proof, not "
     "a search that gave up); informed by EU 561/2006, not a compliance tool. "
     "Phased build: staged $2,750,462 NPV (DC0 yr 2, DC3 yr 6) vs a $2,598,732 "
     "free-redesign lower bound, building ahead +24.4%, never closing +5.8%, no "
     "expansion failing in year 2 -- illustrative growth and discount rates, "
     "recurring opex not capex, no construction lead time"],
    ["Real, messy data (completed)",
     "retail-analytics-real (UCI Online Retail II, 1,067,371 real rows, CC BY 4.0)",
     "real data: 94.0% rows kept; GBP 19.6M revenue; returns 3.65% of gross, "
     "95.0% of value matched, median 10-day lag; Champions 25% -> 69.0%; "
     "lifecycle: resurrections outnumber repeats (439 vs 390/month); "
     "seasonal-naive wins CV, MASE 1.094; price ladders: 88.7% of SKUs sold at "
     "more than one price, realization 98.6% ('not an opportunity'), slopes "
     "-1.71 within-week / -1.67 market-adjusted with 74.1% beating a permutation "
     "null -- and NO elasticity claimed, nothing causal: an assortment-level "
     "statement, not a per-SKU price recommendation"],
    ["Present to decision-makers", "revops-optimizer exec deck", "exec narrative deck"],
]


# ----------------------------------------------------------------------- pages

def cover(doc, stats):
    fig, ax = doc.new_page(section=None)

    y = 0.82
    ax.text(X(MARGIN_L), Y(y), "INDEPENDENT CASE STUDY -- PUBLIC INFORMATION ONLY",
            fontsize=6.8, color=ACCENT, family=SANS, fontweight="bold", va="top")
    y += 0.18
    ax.text(X(MARGIN_L), Y(y), "Data & AI Case Study", fontsize=27,
            fontweight="bold", color=INK, family=SANS, va="top")
    y += 0.48
    ax.text(X(MARGIN_L), Y(y), "Mapped to two Wuerth internship roles",
            fontsize=12.5, color=MUTED, family=SANS, va="top")
    y += 0.30
    hairline(ax, y, lw=1.8, color=ACCENT)
    y += 0.16

    y = disclaimer_band(ax, y) + 0.24
    y = paragraph(ax, y, INTRO, 9.0) + 0.26

    # The one oversized figure: requirement count, computed from the guards.
    hairline(ax, y, lw=1.1, color=INK)
    y_fig = y + 0.14
    big = str(stats["requirements"])
    ax.text(X(MARGIN_L), Y(y_fig), big, fontsize=56, fontweight="bold",
            color=INK, family=SANS, va="top")
    big_w = text_width(big, 56, "bold") + 0.28
    label_x = MARGIN_L + big_w
    label_w = BODY_W - big_w
    ax.text(X(label_x), Y(y_fig + 0.10),
            "requirements mapped -> repo + artifact + measured proof",
            fontsize=11, fontweight="bold", color=ACCENT, family=SANS, va="top")
    cc, cc_n = stats["consistency"]
    sc, sc_n = stats["coverage"]
    sub = (f"computed at build time from this repository's own guards: "
           f"skill coverage {sc}/{sc_n} checks and consistency {cc}/{cc_n} "
           f"checks passing; {stats['repos']} portfolio repositories "
           f"registered")
    y_sub = paragraph(ax, y_fig + 0.34, sub, 7.4, color=MUTED, width=label_w,
                      x_in=label_x)
    y = max(y_fig + 0.90, y_sub) + 0.12
    hairline(ax, y, lw=1.1, color=INK)
    y += 0.28

    for title, body in ROLES:
        ax.text(X(MARGIN_L), Y(y), title, fontsize=10.5, fontweight="bold",
                color=INK, family=SANS, va="top")
        y += 0.20
        y = paragraph(ax, y, body, 8.6, color=MUTED) + 0.10
        hairline(ax, y, lw=0.4)
        y += 0.18

    y += 0.06
    ax.text(X(MARGIN_L), Y(y), WHO_TITLE, fontsize=11.5, fontweight="bold",
            color=INK, family=SANS, va="top")
    y += 0.24
    y = paragraph(ax, y, WHO, 8.6, color=MUTED)

    ax.text(X(MARGIN_L), Y(PAGE_H - 1.02), BYLINE, fontsize=7.6, color=MUTED,
            family=SANS, va="bottom")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    stats = gather_stats()
    doc = Doc()

    cover(doc, stats)

    opportunity_style = TableStyle(
        widths=[1.22, 1.50, 1.28, 2.77],
        fs_list=[7.0, 7.0, 6.4, 7.0],
        weights=["bold", "normal", "normal", "normal"],
        families=[SANS, SANS, MONO, SANS],
    )
    table_section(
        doc, 2, "Opportunity map", "Opportunity map (summary)",
        "Wuerth business area (public-info) -> Data/AI approach "
        "-> repo + measured result (synthetic unless noted)",
        OPPORTUNITY_HEADER, OPPORTUNITY_ROWS, opportunity_style,
    )

    skill_style = TableStyle(
        widths=[1.50, 1.90, 3.37],
        fs_list=[7.2, 6.6, 7.2],
        weights=["bold", "normal", "normal"],
        families=[SANS, MONO, SANS],
    )
    table_section(
        doc, 3, "Job #1 -- Automation with Low-code",
        "Job #1 -- (Agentic) Automation with Low-code",
        "Every posting requirement -> repo + artifact + measured "
        "proof (all synthetic data).",
        SKILL_HEADER, JOB1_ROWS, skill_style,
    )
    table_section(
        doc, 4, "Job #2 -- Data & AI Analytics",
        "Job #2 -- Data & AI Analytics",
        "Every posting requirement -> repo + artifact + measured "
        "proof (synthetic data unless labelled real data).",
        SKILL_HEADER, JOB2_ROWS, skill_style,
    )

    pages = doc.finalize(OUT_PATH)

    size = os.path.getsize(OUT_PATH)
    print(f"[OK] wrote {OUT_PATH} ({size} bytes, {size / 1024:.1f} KB, {pages} pages)")
    if size < 10 * 1024:
        print("[WARN] PDF smaller than 10 KB")
        sys.exit(1)


if __name__ == "__main__":
    main()
