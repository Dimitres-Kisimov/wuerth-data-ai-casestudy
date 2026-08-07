"""Machine-checked SKILL-COVERAGE MATRIX for the case study.

Where the anti-drift guard (``validation/consistency_check.py``) checks that every
repo-shaped token *anywhere* in the docs resolves to the registry, this guard
checks the one thing that is the whole point of the case study: that the
**Job -> Skill -> Evidence map** (``docs/JOB_SKILL_MAP.md``) actually *covers*
every posting requirement. It parses the two job tables and proves, row by row,
that each posting requirement is backed by concrete, registered evidence --

    * at least one **registered** portfolio repo (or an explicit cross-cutting
      "across ... repos" row), so no requirement can silently lose its backing;
    * a non-empty **File / artifact** cell -- the exact thing to open; and
    * a non-empty **Proof / measured result** cell -- the number that backs it.

A blank repo cell, a proof cell that quietly emptied out, or a repo name that no
longer resolves to the registry would all pass the nine anti-drift checks yet
break the case study's core promise -- "every requirement maps to something I
built and measured". This guard fails on exactly those gaps.

It is **validation only**: it invents no numbers and asserts nothing the map does
not already state. It is deterministic (source order preserved, sorted indexes,
no wall-clock, no RNG), offline, and depends only on the Python standard library
plus the registry/token helpers already in ``consistency_check``.

    python -m validation.skill_coverage   # writes SKILL_COVERAGE_MATRIX.md, prints summary

Exit code is 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

from validation.consistency_check import (
    ROOT,
    Check,
    extract_repo_tokens,
    load_registry,
    read,
)

JOB_SKILL_DOC = "docs/JOB_SKILL_MAP.md"
REPORT_PATH = ROOT / "validation" / "SKILL_COVERAGE_MATRIX.md"

# A markdown ``## Job #N -- ...`` heading opens a job section.
JOB_HEADING = re.compile(r"^##\s+Job\s+#(\d+)\b")
# The header row of an evidence table carries all of these column names.
HEADER_TOKENS = ("posting requirement", "repo", "proof")
# A requirement legitimately backed by "the whole family" rather than one repo.
CROSS_CUTTING = re.compile(r"\b(?:across|all)\b.*\brepos?\b")

# Minimum requirement rows expected per job (headroom below the real counts of
# 12 / 19 so ordinary edits do not trip the guard, but a table that collapsed
# would). Both postings must be present.
MIN_ROWS = {"Job #1": 8, "Job #2": 12}
# Minimum number of *distinct* registered repos backing each job -- proves the
# evidence is spread across the portfolio, not concentrated in a single repo.
MIN_DISTINCT_REPOS = {"Job #1": 5, "Job #2": 8}

# The four "crown-jewel" flagships the README/JOB_SKILL_MAP lead with. This guard
# proves each one actually appears as backing evidence for a posting requirement
# (a cross-doc claim check -- the flagships are named, so they must earn a row).
FLAGSHIP_REPOS = (
    "logistics-flow-studio",
    "logistics-digital-twin",
    "decision-chain",
    "distributor-intelligence-platform",
)


@dataclass
class Requirement:
    """One posting-requirement row of the Job -> Skill -> Evidence map."""

    job: str
    requirement: str
    repo_cell: str
    artifact_cell: str
    proof_cell: str
    repos: tuple[str, ...] = ()  # registered repos named in the Repo column
    unregistered: tuple[str, ...] = ()  # repo-shaped tokens that do NOT resolve

    @property
    def is_cross_cutting(self) -> bool:
        """True for an explicit 'across ... repos' row with no single repo named."""
        return not self.repos and bool(CROSS_CUTTING.search(self.repo_cell.lower()))

    @property
    def is_backed(self) -> bool:
        return bool(self.repos) or self.is_cross_cutting


@dataclass
class SkillMap:
    """Parsed job tables plus any structural parse errors."""

    requirements: list[Requirement] = field(default_factory=list)
    headings: dict[str, str] = field(default_factory=dict)
    parse_errors: list[str] = field(default_factory=list)

    def by_job(self, job: str) -> list[Requirement]:
        return [r for r in self.requirements if r.job == job]

    @property
    def jobs(self) -> list[str]:
        seen: list[str] = []
        for r in self.requirements:
            if r.job not in seen:
                seen.append(r.job)
        return seen


def _split_row(line: str) -> list[str]:
    """Split a ``| a | b | c | d |`` markdown row into stripped cells."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_skill_map(registry: list[str]) -> SkillMap:
    """Parse ``docs/JOB_SKILL_MAP.md`` into per-job requirement rows."""
    known = set(registry)
    lines = read(JOB_SKILL_DOC).splitlines()
    result = SkillMap()
    current_job: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = JOB_HEADING.match(line)
        if heading:
            current_job = f"Job #{heading.group(1)}"
            result.headings[current_job] = line.lstrip("# ").strip()
            i += 1
            continue
        low = line.lower()
        is_header = line.lstrip().startswith("|") and all(tok in low for tok in HEADER_TOKENS)
        if is_header:
            i += 2  # skip the header row and the |---| separator row
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = _split_row(lines[i])
                if len(cells) != 4:
                    result.parse_errors.append(
                        f"{current_job or '(no job)'} line {i + 1}: expected 4 columns, "
                        f"got {len(cells)}"
                    )
                else:
                    tokens = extract_repo_tokens(cells[1])
                    repos = tuple(sorted(t for t in tokens if t in known))
                    unregistered = tuple(sorted(t for t in tokens if t not in known))
                    result.requirements.append(
                        Requirement(
                            job=current_job or "(no job)",
                            requirement=cells[0].replace("**", "").strip(),
                            repo_cell=cells[1],
                            artifact_cell=cells[2],
                            proof_cell=cells[3],
                            repos=repos,
                            unregistered=unregistered,
                        )
                    )
                i += 1
            continue
        i += 1
    return result


# --------------------------------------------------------------------------- checks


def check_tables_parsed(sm: SkillMap) -> Check:
    failures = list(sm.parse_errors)
    for job in ("Job #1", "Job #2"):
        rows = sm.by_job(job)
        if not rows:
            failures.append(f"{job}: evidence table not found or empty")
        elif len(rows) < MIN_ROWS[job]:
            failures.append(f"{job}: only {len(rows)} requirement rows (expected >= {MIN_ROWS[job]})")
    total = len(sm.requirements)
    return Check(
        "both job tables parse into 4-column requirement rows",
        not failures,
        f"{total} requirement rows across {len(sm.jobs)} job tables",
        failures,
    )


def check_artifacts_present(sm: SkillMap) -> Check:
    failures = [
        f"{r.job} `{r.requirement[:60]}`: empty File/artifact cell"
        for r in sm.requirements
        if not r.artifact_cell.strip().strip("-").strip()
    ]
    return Check(
        "every requirement names a file / artifact to open",
        not failures,
        f"{len(sm.requirements)} requirements all cite a concrete artifact",
        failures,
    )


def check_proofs_present(sm: SkillMap) -> Check:
    failures = [
        f"{r.job} `{r.requirement[:60]}`: empty Proof / measured-result cell"
        for r in sm.requirements
        if not r.proof_cell.strip().strip("-").strip()
    ]
    return Check(
        "every requirement carries a proof / measured result",
        not failures,
        f"{len(sm.requirements)} requirements all carry a proof cell",
        failures,
    )


def check_evidence_repos_registered(sm: SkillMap) -> Check:
    failures = [
        f"{r.job} `{r.requirement[:60]}`: Repo column names unregistered repo `{name}`"
        for r in sm.requirements
        for name in r.unregistered
    ]
    return Check(
        "every repo cited as evidence resolves to the registry",
        not failures,
        "no dangling / unregistered repo appears in a Repo column",
        failures,
    )


def check_backing_completeness(sm: SkillMap) -> Check:
    failures = [
        f"{r.job} `{r.requirement[:60]}`: no registered repo and not an explicit "
        f"cross-cutting row (Repo cell: {r.repo_cell!r})"
        for r in sm.requirements
        if not r.is_backed
    ]
    backed = sum(1 for r in sm.requirements if r.is_backed)
    return Check(
        "every posting requirement is backed by a registered repo",
        not failures,
        f"{backed}/{len(sm.requirements)} requirements backed (incl. explicit cross-cutting rows)",
        failures,
    )


def check_flagship_coverage(sm: SkillMap) -> Check:
    backing: set[str] = set()
    for r in sm.requirements:
        backing |= set(r.repos)
    failures = [
        f"flagship repo `{repo}` backs no posting requirement in the skill map"
        for repo in FLAGSHIP_REPOS
        if repo not in backing
    ]
    return Check(
        "each crown-jewel flagship backs at least one requirement",
        not failures,
        f"{len(FLAGSHIP_REPOS) - len(failures)}/{len(FLAGSHIP_REPOS)} flagships appear as evidence",
        failures,
    )


def check_job_breadth(sm: SkillMap) -> Check:
    failures: list[str] = []
    for job, minimum in MIN_DISTINCT_REPOS.items():
        distinct = {repo for r in sm.by_job(job) for repo in r.repos}
        if len(distinct) < minimum:
            failures.append(f"{job}: only {len(distinct)} distinct registered repos (expected >= {minimum})")
    return Check(
        "each job's evidence spans several distinct repos",
        not failures,
        "; ".join(
            f"{job}: {len({repo for r in sm.by_job(job) for repo in r.repos})} distinct repos"
            for job in MIN_DISTINCT_REPOS
        ),
        failures,
    )


def run_all_checks(sm: SkillMap | None = None) -> list[Check]:
    """Run every skill-coverage check and return results in report order."""
    if sm is None:
        sm = parse_skill_map(load_registry())
    return [
        check_tables_parsed(sm),
        check_artifacts_present(sm),
        check_proofs_present(sm),
        check_evidence_repos_registered(sm),
        check_backing_completeness(sm),
        check_flagship_coverage(sm),
        check_job_breadth(sm),
    ]


# --------------------------------------------------------------------------- report


def _repo_index(sm: SkillMap) -> list[tuple[str, list[str]]]:
    """Sorted (repo -> list of jobs it backs a requirement in) for the report."""
    index: dict[str, set[str]] = {}
    for r in sm.requirements:
        for repo in r.repos:
            index.setdefault(repo, set()).add(r.job)
    return [(repo, sorted(index[repo])) for repo in sorted(index)]


def render_report(checks: list[Check], sm: SkillMap) -> str:
    """Render a deterministic markdown coverage matrix (no timestamps, source order)."""
    passed = sum(1 for c in checks if c.passed)
    status = "FULL COVERAGE" if passed == len(checks) else "COVERAGE GAP DETECTED"

    lines: list[str] = [
        "# Skill-coverage matrix",
        "",
        "> Auto-generated by `validation/skill_coverage.py`. Do not edit by hand;",
        "> regenerate with `python -m validation.skill_coverage`. Deterministic",
        "> (no timestamps / RNG) so re-runs are byte-identical. This report only",
        "> **validates** that every posting requirement in `docs/JOB_SKILL_MAP.md`",
        "> is backed by a registered repo + artifact + measured proof -- it invents",
        "> no numbers and asserts nothing the map does not already state.",
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

    for job in sm.jobs:
        rows = sm.by_job(job)
        distinct = sorted({repo for r in rows for repo in r.repos})
        heading = sm.headings.get(job, job)
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(f"_{len(rows)} requirements, {len(distinct)} distinct registered repos._")
        lines.append("")
        lines.append("| # | Posting requirement | Registered repos backing it |")
        lines.append("|---|---------------------|------------------------------|")
        for i, r in enumerate(rows, start=1):
            if r.repos:
                backing = ", ".join(f"`{repo}`" for repo in r.repos)
            elif r.is_cross_cutting:
                backing = f"_(cross-cutting: {r.repo_cell})_"
            else:
                backing = "**(none)**"
            lines.append(f"| {i} | {r.requirement} | {backing} |")
        lines.append("")

    lines.append("## Repo -> requirements index")
    lines.append("")
    lines.append("| Repo | Backs requirements in |")
    lines.append("|------|------------------------|")
    for repo, jobs in _repo_index(sm):
        lines.append(f"| `{repo}` | {', '.join(jobs)} |")
    lines.append("")
    lines.append("_Every figure referenced above is measured on synthetic / self-generated "
                 "data unless the repo is marked real data (UCI Online Retail II, CC BY 4.0). "
                 "Independent analysis; not affiliated with, endorsed by, or reviewed by the "
                 "Wuerth Group._")
    lines.append("")
    return "\n".join(lines)


def write_report(text: str) -> None:
    """Write the report with LF newlines for cross-platform byte-stability."""
    REPORT_PATH.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sm = parse_skill_map(load_registry())
    checks = run_all_checks(sm)
    write_report(render_report(checks, sm))

    print("Skill-coverage matrix")
    for c in checks:
        print(f"  [{'PASS' if c.passed else 'FAIL'}] {c.name} -- {c.detail}")
        for f in c.failures:
            print(f"         - {f}")
    passed = sum(1 for c in checks if c.passed)
    print(f"{passed}/{len(checks)} checks passing; {len(sm.requirements)} requirements mapped.")
    print(f"Report written to {REPORT_PATH.relative_to(ROOT).as_posix()}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
