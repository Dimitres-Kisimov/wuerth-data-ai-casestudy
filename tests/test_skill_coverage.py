"""Tests for the machine-checked skill-coverage matrix.

These assert two things. First, that the real Job -> Skill -> Evidence map covers
every posting requirement (a registered repo + artifact + proof for each) and that
the committed matrix report is fresh. Second -- and this is what makes the guard
worth having -- that it actually *fails on a gap*: for each check we build a
skill map with a deliberately introduced hole (a blanked proof, a dangling repo,
an unbacked requirement, a missing flagship, a collapsed table) and assert the
corresponding check turns red. A guard that cannot fail proves nothing.
"""

from validation.consistency_check import load_registry
from validation.skill_coverage import (
    FLAGSHIP_REPOS,
    REPORT_PATH,
    Check,
    Requirement,
    SkillMap,
    check_artifacts_present,
    check_backing_completeness,
    check_evidence_repos_registered,
    check_flagship_coverage,
    check_job_breadth,
    check_proofs_present,
    check_tables_parsed,
    parse_skill_map,
    render_report,
    run_all_checks,
)


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n")


def _req(job="Job #1", requirement="Do a thing", repo_cell="`revops-optimizer`",
         artifact="some/file.py", proof="MASE 0.38 (synthetic)",
         repos=("revops-optimizer",), unregistered=()):
    return Requirement(job, requirement, repo_cell, artifact, proof, repos, unregistered)


# --------------------------------------------------------------- real-map coverage


def test_all_coverage_checks_pass():
    checks = run_all_checks()
    failed = [c for c in checks if not c.passed]
    assert not failed, "skill-coverage gap detected:\n" + "\n".join(
        f"- {c.name}:\n    " + "\n    ".join(c.failures) for c in failed
    )


def test_each_check_is_reported_individually():
    checks = run_all_checks()
    assert len(checks) >= 6
    assert all(isinstance(c, Check) for c in checks)
    names = [c.name for c in checks]
    assert len(names) == len(set(names)), "duplicate check names"


def test_real_map_has_both_jobs_and_enough_rows():
    sm = parse_skill_map(load_registry())
    assert sm.jobs == ["Job #1", "Job #2"], sm.jobs
    assert not sm.parse_errors, sm.parse_errors
    assert len(sm.by_job("Job #1")) >= 8
    assert len(sm.by_job("Job #2")) >= 12
    # Every parsed requirement resolves to at least one registered repo or is
    # an explicit cross-cutting row -- nothing dangles.
    assert all(r.is_backed for r in sm.requirements)


def test_flagships_each_back_a_requirement():
    sm = parse_skill_map(load_registry())
    backing = {repo for r in sm.requirements for repo in r.repos}
    for flagship in FLAGSHIP_REPOS:
        assert flagship in backing, f"{flagship} backs no requirement"


def test_committed_report_is_fresh():
    sm = parse_skill_map(load_registry())
    regenerated = render_report(run_all_checks(sm), sm)
    committed = REPORT_PATH.read_text(encoding="utf-8")
    assert _normalize(committed) == _normalize(regenerated), (
        "validation/SKILL_COVERAGE_MATRIX.md is stale -- regenerate with "
        "`python -m validation.skill_coverage`"
    )


def test_report_declares_full_coverage():
    committed = REPORT_PATH.read_text(encoding="utf-8")
    assert "FULL COVERAGE" in committed


# --------------------------------------------------------------- fails-on-a-gap

# A minimal healthy map: both jobs, enough rows, enough distinct repos, all
# flagships present. Each gap test perturbs one facet of this and expects red.
def _healthy_map() -> SkillMap:
    job1_repos = [
        "agentic-automation-lab", "chain-mcp", "agent-flow-studio",
        "doc-extract-agent", "automation-roi-explorer", "quantum-explainer",
        "logistics-flow-studio", "agentic-automation-lab",
    ]
    job2_repos = [
        "decision-chain", "revops-optimizer", "sales-kpi-analytics",
        "ml-models-lab", "distributor-intelligence-platform", "energy-demand-forecast",
        "supply-network-opt", "logistics-digital-twin", "market-basket-analysis",
        "quality-anomaly-vision", "route-optimizer", "retail-analytics-real",
    ]
    reqs = [_req("Job #1", f"req1-{i}", f"`{r}`", "f.py", "n", (r,)) for i, r in enumerate(job1_repos)]
    reqs += [_req("Job #2", f"req2-{i}", f"`{r}`", "f.py", "n", (r,)) for i, r in enumerate(job2_repos)]
    return SkillMap(requirements=reqs)


def test_healthy_map_passes_every_check():
    sm = _healthy_map()
    assert all(c.passed for c in run_all_checks(sm)), [c.name for c in run_all_checks(sm) if not c.passed]


def test_blank_proof_fails_proof_check():
    sm = _healthy_map()
    sm.requirements[0].proof_cell = "   "
    assert not check_proofs_present(sm).passed
    # A bare dash is not a proof either.
    sm.requirements[0].proof_cell = "-"
    assert not check_proofs_present(sm).passed


def test_blank_artifact_fails_artifact_check():
    sm = _healthy_map()
    sm.requirements[0].artifact_cell = ""
    assert not check_artifacts_present(sm).passed


def test_unregistered_repo_fails_resolution_check():
    sm = _healthy_map()
    sm.requirements[0].unregistered = ("totally-made-up-repo",)
    assert not check_evidence_repos_registered(sm).passed


def test_unbacked_requirement_fails_backing_check():
    sm = _healthy_map()
    # No registered repo, and the repo cell is not a cross-cutting phrase.
    sm.requirements[0].repos = ()
    sm.requirements[0].repo_cell = "TODO: pick a repo"
    assert not check_backing_completeness(sm).passed


def test_cross_cutting_row_is_accepted_as_backed():
    sm = _healthy_map()
    sm.requirements[0].repos = ()
    sm.requirements[0].repo_cell = "across automation repos"
    assert check_backing_completeness(sm).passed
    assert sm.requirements[0].is_cross_cutting


def test_missing_flagship_fails_flagship_check():
    sm = _healthy_map()
    dropped = FLAGSHIP_REPOS[0]
    for r in sm.requirements:
        if dropped in r.repos:
            r.repos = tuple(x for x in r.repos if x != dropped)
    assert not check_flagship_coverage(sm).passed


def test_collapsed_table_fails_structure_check():
    # Job #2 present but with too few rows -> structure check must fail.
    sm = SkillMap(requirements=[_req("Job #1", "only-one", "`revops-optimizer`")])
    assert not check_tables_parsed(sm).passed


def test_narrow_evidence_fails_breadth_check():
    # Enough rows, but every Job #2 row leans on the same single repo.
    reqs = [_req("Job #2", f"r{i}", "`revops-optimizer`", "f.py", "n", ("revops-optimizer",))
            for i in range(14)]
    sm = SkillMap(requirements=reqs)
    assert not check_job_breadth(sm).passed
