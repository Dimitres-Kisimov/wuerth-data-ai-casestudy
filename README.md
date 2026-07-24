# Data & AI Case Study — mapped to two Würth internship roles

> **DISCLAIMER — read this first.** This is an **independent** case study I put together on my own. It is based **only on publicly available information** about the Würth Group (company website, public press, general industry knowledge). It is **not affiliated with, endorsed by, or reviewed by Würth**, and it uses **no internal, confidential, or proprietary Würth data or systems** of any kind. Every figure attributed to Würth's scale (number of companies, employees, revenue, ORSY installations, article counts) is **public and approximate** and is labelled as such — I have not invented internal Würth numbers. Every performance number in my own portfolio is measured on **synthetic / self-generated data**, and I say so each time it appears. The point of this repo is to show *how I think and what I can build*, not to claim results on Würth's real business.

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

I've built two complementary bodies of work, which is exactly why I can speak to both roles:

**Analytics side (Job #2)** — forecasting, KPIs, optimization, BI:
- `revops-optimizer` — assortment (MILP), newsvendor inventory, elasticity pricing, a **Power BI / DAX** pack and an exec deck; ~**€160k/yr** modelled uplift *(synthetic data)*.
- `sales-kpi-analytics` — KPI metrics, **forecasting with rolling-origin CV and MASE**, SQL, a **€2.6M** discount-leakage lever *(synthetic data)*.
- `distributor-intelligence-platform` — the engines composed into one platform; **MASE 0.376** forecasting, **25% km** routing saving, MILP vs. greedy assortment *(synthetic data)*.
- `route-optimizer` — OR-Tools CP-SAT vehicle routing vs. heuristics, **4.6% / 31%** savings *(synthetic data)*.

**Automation side (Job #1)** — agentic workflows, low-code, document processing:
- `agentic-automation-lab` — agentic tool-use loops **plus an n8n low-code RFQ-intake agent workflow** *(synthetic data)*.
- `agent-flow-studio` — a visual agent/flow builder *(synthetic data)*.
- `doc-extract-agent` — agentic extraction of RFQ / invoice documents into structured data *(synthetic data)*.
- `automation-roi-explorer` — an automation ROI dashboard *(synthetic data)*.

Supporting research/method work: `bio-efficient-ai` (a small research PoC with an honestly cited paper) and `ml-models-lab` (method specs for small models).

> All uplift/€ figures above are **modelled on synthetic data** to demonstrate method and are **not** claims about Würth. On real Würth data the numbers would be different — validating that is exactly the internship work.

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
```

## Honesty notes

- Independent analysis, **public info only**, **not affiliated with Würth**.
- No internal Würth data or systems were used or accessed.
- All portfolio metrics are on **synthetic data** and demonstrate method, not guaranteed business outcomes.
- No superlatives — I don't claim to "beat everyone" or "guarantee" anything. This is honest, reproducible work.

— Dimitres Kisimov, 2026
