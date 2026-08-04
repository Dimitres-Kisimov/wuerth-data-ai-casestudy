"""Machine-checked consistency / anti-drift guard for the case study.

This module VALIDATES what is already in the case-study docs -- it never invents
numbers or claims. It parses the human-authored documents (README, docs/*.md, the
offline web page, CREDITS) and asserts a handful of internal-consistency
properties so the case study cannot silently go stale:

    1.  Registry integrity          -- validation/portfolio_repos.txt is well-formed.
    2.  Repo references resolve      -- every repo name cited in a doc is registered.
    3.  Registry coverage            -- every registered repo is actually referenced.
    4.  README completeness          -- the README mentions every registered repo.
    5.  CREDITS completeness         -- the provenance credits name every repo.
    6.  Disclaimer present           -- the "independent / not affiliated" disclaimer
                                        is present in every substance doc (EN + DE).
    7.  Metric provenance nearby     -- every currency figure sits in a section that
                                        states its data provenance (synthetic / real /
                                        public-approximate / modelled / assumed / ...).
    8.  Real-data labelling          -- the two real-data repos are labelled "real data"
                                        in every doc that names them.
    9.  License honesty              -- proprietary "all rights reserved" everywhere;
                                        no stale "MIT" self-license claim anywhere.

It is deterministic (sorted output, no wall-clock, no RNG), offline, and depends
only on the Python standard library. Run it to (re)generate a short report that
the README references:

    python -m validation.consistency_check      # writes CONSISTENCY_REPORT.md, prints summary

Exit code is 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "validation" / "portfolio_repos.txt"
REPORT_PATH = ROOT / "validation" / "CONSISTENCY_REPORT.md"

# Human-authored markdown docs whose metric provenance is checked section-by-section.
MARKDOWN_DOCS = (
    "README.md",
    "docs/OPPORTUNITY_MAP.md",
    "docs/JOB_SKILL_MAP.md",
    "docs/ZUSAMMENFASSUNG_DE.md",
    "docs/AREAS_FOR_IMPROVEMENT.md",
    "docs/BUSINESS_CASE.md",
)
# Additional docs scanned for repo references, disclaimers, real-data labels and MIT.
EXTRA_DOCS = ("CREDITS.md", "web/index.html")
SCANNED_DOCS = MARKDOWN_DOCS + EXTRA_DOCS

README_DOC = "README.md"
CREDITS_DOC = "CREDITS.md"
LICENSE_DOC = "LICENSE"

# The only repositories whose numbers are measured on real (public UCI) data.
REAL_DATA_REPOS = ("decision-chain", "retail-analytics-real")

# Backtick tokens that share the repo-name shape but are NOT repositories
# (provenance-tag values and identifiers, kept out of the registry check).
NON_REPO_TOKENS = frozenset({"synthetic-assigned"})

REPO_SHAPE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$")
BACKTICK_TOKEN = re.compile(r"`([^`]+)`")
CODE_TAG_TOKEN = re.compile(r"<code>([^<]+)</code>")
CURRENCY = re.compile(r"(?:€|£|\$|EUR|GBP)\s?\d[\d.,]*|\d[\d.,]*\s?(?:€|£|\$|EUR|GBP)")

# A doc counts as carrying the disclaimer if it matches one of these (EN or DE).
DISCLAIMER_SIGNATURES = ("not affiliated with", "nicht mit würth")

# Provenance qualifiers that legitimately accompany a figure (EN + DE). Wuerth-scale
# public figures are labelled "public / approximate"; portfolio metrics are labelled
# "synthetic" or "real data"; modelled euro figures say "modelled / assumed / ...".
PROVENANCE_TERMS = (
    "synthetic",
    "synthetisch",
    "real data",
    "real-data",
    "real uci",
    "real public",
    "real, messy",
    "echte daten",
    "echten daten",
    "reale daten",
    "modelled",
    "modeled",
    "modelliert",
    "measured",
    "gemessen",
    "assumed",
    "angenommen",
    "invented",
    "labelled",
    "labeled",
    "gekennzeichnet",
    "public",
    "approximate",
    "öffentlich",
    "ungefähr",
)

# A doc names a real-data repo honestly if it also carries one of these.
REAL_DATA_TERMS = (
    "real data",
    "real-data",
    "real uci",
    "real public",
    "real, messy",
    "measured on real",
    "echte daten",
    "echten daten",
    "reale daten",
)


@dataclass
class Check:
    """Result of a single consistency check."""

    name: str
    passed: bool
    detail: str = ""
    failures: list[str] = field(default_factory=list)


def read(rel_path: str) -> str:
    """Read a repo-relative text file as UTF-8."""
    return (ROOT / rel_path).read_text(encoding="utf-8")


def load_registry() -> list[str]:
    """Load the authoritative portfolio-repo registry (sorted, de-duplicated check upstream)."""
    names: list[str] = []
    for raw in REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            names.append(line)
    return names


def extract_repo_tokens(text: str) -> set[str]:
    """Return backtick / <code> tokens that have the shape of a repo name."""
    tokens: set[str] = set()
    for match in BACKTICK_TOKEN.findall(text) + CODE_TAG_TOKEN.findall(text):
        token = match.strip()
        if REPO_SHAPE.match(token) and token not in NON_REPO_TOKENS:
            tokens.add(token)
    return tokens


def split_sections(text: str) -> list[str]:
    """Split markdown into header-delimited sections (preamble + one per heading)."""
    sections: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            sections.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    sections.append("\n".join(current))
    return sections


# --------------------------------------------------------------------------- checks


def check_registry_integrity(registry: list[str]) -> Check:
    failures: list[str] = []
    if len(registry) < 10:
        failures.append(f"registry has only {len(registry)} entries (expected the full portfolio)")
    seen: set[str] = set()
    for name in registry:
        if name in seen:
            failures.append(f"duplicate registry entry: {name}")
        seen.add(name)
        if not REPO_SHAPE.match(name):
            failures.append(f"malformed registry entry: {name!r}")
    return Check(
        "registry integrity",
        not failures,
        f"{len(registry)} repositories registered",
        failures,
    )


def check_repo_references_resolve(registry: list[str]) -> Check:
    known = set(registry)
    failures: list[str] = []
    for doc in SCANNED_DOCS:
        for token in sorted(extract_repo_tokens(read(doc))):
            if token not in known:
                failures.append(f"{doc}: references unregistered repo `{token}`")
    return Check(
        "repo references resolve to the registry",
        not failures,
        "every repo-shaped token in the docs is a registered repository",
        failures,
    )


def check_registry_coverage(registry: list[str]) -> Check:
    referenced: set[str] = set()
    for doc in SCANNED_DOCS:
        referenced |= extract_repo_tokens(read(doc))
    failures = [f"registered repo never referenced in any doc: {r}" for r in registry
                if r not in referenced]
    return Check(
        "registry coverage (no dead entries)",
        not failures,
        f"{len(referenced & set(registry))}/{len(registry)} registered repos referenced",
        failures,
    )


def check_readme_completeness(registry: list[str]) -> Check:
    referenced = extract_repo_tokens(read(README_DOC))
    failures = [f"README does not mention registered repo: {r}" for r in registry
                if r not in referenced]
    return Check(
        "README mentions every registered repo",
        not failures,
        f"{len(referenced & set(registry))}/{len(registry)} registered repos in README",
        failures,
    )


def check_credits_completeness(registry: list[str]) -> Check:
    referenced = extract_repo_tokens(read(CREDITS_DOC))
    failures = [f"CREDITS.md does not credit registered repo: {r}" for r in registry
                if r not in referenced]
    return Check(
        "CREDITS.md credits every registered repo",
        not failures,
        f"{len(referenced & set(registry))}/{len(registry)} registered repos credited",
        failures,
    )


def check_disclaimers() -> Check:
    failures: list[str] = []
    for doc in SCANNED_DOCS:
        low = read(doc).lower()
        if not any(sig in low for sig in DISCLAIMER_SIGNATURES):
            failures.append(f"{doc}: missing 'independent / not affiliated with Wuerth' disclaimer")
    return Check(
        "disclaimer present in every substance doc",
        not failures,
        f"{len(SCANNED_DOCS)} docs carry the not-affiliated disclaimer",
        failures,
    )


def check_metric_provenance() -> Check:
    """Every currency figure must sit in a section that states its data provenance."""
    failures: list[str] = []
    checked = 0
    for doc in MARKDOWN_DOCS:
        for i, section in enumerate(split_sections(read(doc))):
            if not CURRENCY.search(section):
                continue
            checked += 1
            low = section.lower()
            if not any(term in low for term in PROVENANCE_TERMS):
                heading = section.strip().splitlines()[0] if section.strip() else "(preamble)"
                failures.append(f"{doc} section {i} ({heading[:60]!r}): currency figure "
                                "without a synthetic/real/public provenance label nearby")
    return Check(
        "every currency figure has a provenance label nearby",
        not failures,
        f"{checked} money-bearing sections checked, all labelled",
        failures,
    )


def check_real_data_labels() -> Check:
    """The two real-data repos must be labelled 'real data' in every doc that names them."""
    failures: list[str] = []
    for doc in SCANNED_DOCS:
        text = read(doc)
        low = text.lower()
        tokens = extract_repo_tokens(text)
        for repo in REAL_DATA_REPOS:
            if repo in tokens and not any(term in low for term in REAL_DATA_TERMS):
                failures.append(f"{doc}: names real-data repo `{repo}` without a 'real data' label")
    return Check(
        "real-data repos are labelled 'real data' wherever named",
        not failures,
        f"real-data repos {', '.join(REAL_DATA_REPOS)} labelled everywhere they appear",
        failures,
    )


def check_license_honesty() -> Check:
    """Proprietary all-rights-reserved is intact; no stale MIT self-license claim survives.

    Design note / limitation: this repo cites no MIT-licensed third-party components,
    so a strict word-boundary ban on the ``MIT`` token across the docs is both simple
    and correct here -- historically a stale MIT footer did slip in (fixed in git). If a
    legitimate MIT-licensed dependency is ever credited, narrow this to a self-license
    pattern instead of a bare token ban.
    """
    failures: list[str] = []
    mit = re.compile(r"\bMIT\b")
    for doc in (*SCANNED_DOCS, LICENSE_DOC):
        if mit.search(read(doc)):
            failures.append(f"{doc}: contains a stale 'MIT' token (self-license must stay proprietary)")
    license_text = read(LICENSE_DOC).lower()
    if "all rights reserved" not in license_text:
        failures.append("LICENSE: missing 'all rights reserved' (proprietary license expected)")
    for doc in (CREDITS_DOC, "web/index.html"):
        if "all rights reserved" not in read(doc).lower():
            failures.append(f"{doc}: missing the 'all rights reserved' self-license string")
    return Check(
        "license stays proprietary; no stale MIT self-license",
        not failures,
        "LICENSE + docs state 'all rights reserved'; zero 'MIT' tokens present",
        failures,
    )


def run_all_checks() -> list[Check]:
    """Run every consistency check and return the results in report order."""
    registry = load_registry()
    return [
        check_registry_integrity(registry),
        check_repo_references_resolve(registry),
        check_registry_coverage(registry),
        check_readme_completeness(registry),
        check_credits_completeness(registry),
        check_disclaimers(),
        check_metric_provenance(),
        check_real_data_labels(),
        check_license_honesty(),
    ]


# --------------------------------------------------------------------------- report


def render_report(checks: list[Check], registry: list[str]) -> str:
    """Render a deterministic markdown report (no timestamps, sorted throughout)."""
    passed = sum(1 for c in checks if c.passed)
    status = "ALL CHECKS PASS" if passed == len(checks) else "CONSISTENCY DRIFT DETECTED"

    lines: list[str] = [
        "# Consistency / anti-drift report",
        "",
        "> Auto-generated by `validation/consistency_check.py`. Do not edit by hand;",
        "> regenerate with `python -m validation.consistency_check`. Deterministic",
        "> (no timestamps / RNG) so re-runs are byte-identical. This report only",
        "> **validates** what the docs already say -- it invents no numbers or claims.",
        "",
        f"**Status: {status}** ({passed}/{len(checks)} checks passing).",
        "",
        "## Checks",
        "",
        "| # | Check | Result | Detail |",
        "|---|-------|--------|--------|",
    ]
    for idx, c in enumerate(checks, start=1):
        mark = "PASS" if c.passed else "FAIL"
        lines.append(f"| {idx} | {c.name} | {mark} | {c.detail} |")
    lines.append("")

    failing = [c for c in checks if not c.passed]
    if failing:
        lines.append("## Failures")
        lines.append("")
        for c in failing:
            lines.append(f"### {c.name}")
            for f in c.failures:
                lines.append(f"- {f}")
            lines.append("")

    lines.append(f"## Registered portfolio repositories ({len(registry)})")
    lines.append("")
    real = set(REAL_DATA_REPOS)
    for name in sorted(registry):
        kind = "real data (UCI Online Retail II, CC BY 4.0)" if name in real else "synthetic data"
        lines.append(f"- `{name}` — {kind}")
    lines.append("")
    lines.append("_Metrics are on synthetic / self-generated data unless the repo is "
                 "marked real data. Wuerth-scale figures are public and approximate. "
                 "Independent analysis; not affiliated with, endorsed by, or reviewed "
                 "by the Wuerth Group._")
    lines.append("")
    return "\n".join(lines)


def write_report(text: str) -> None:
    """Write the report with LF newlines for cross-platform byte-stability."""
    REPORT_PATH.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    registry = load_registry()
    checks = run_all_checks()
    write_report(render_report(checks, registry))

    print("Consistency / anti-drift guard")
    for c in checks:
        print(f"  [{'PASS' if c.passed else 'FAIL'}] {c.name} -- {c.detail}")
        for f in c.failures:
            print(f"         - {f}")
    passed = sum(1 for c in checks if c.passed)
    print(f"{passed}/{len(checks)} checks passing; {len(registry)} repos registered.")
    print(f"Report written to {REPORT_PATH.relative_to(ROOT).as_posix()}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
