"""Tests for the machine-checked consistency / anti-drift guard.

These assert that the case study stays internally consistent: every portfolio
repo it references is registered, the disclaimer and synthetic/real-data labels
are present, no stale MIT self-license claim survives, and the committed
consistency report is up to date (byte-stable, ignoring line endings).
"""

from validation.consistency_check import (
    REAL_DATA_REPOS,
    REPORT_PATH,
    Check,
    load_registry,
    render_report,
    run_all_checks,
)


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n")


def test_all_consistency_checks_pass():
    checks = run_all_checks()
    failed = [c for c in checks if not c.passed]
    assert not failed, "consistency drift detected:\n" + "\n".join(
        f"- {c.name}:\n    " + "\n    ".join(c.failures) for c in failed
    )


def test_each_check_is_reported_individually():
    checks = run_all_checks()
    # The guard must exercise a meaningful battery, and each result is a Check.
    assert len(checks) >= 8
    assert all(isinstance(c, Check) for c in checks)
    names = [c.name for c in checks]
    assert len(names) == len(set(names)), "duplicate check names"


def test_registry_is_wellformed_and_covers_real_data_repos():
    registry = load_registry()
    assert len(registry) == len(set(registry)), "duplicate registry entries"
    assert len(registry) >= 15
    for repo in REAL_DATA_REPOS:
        assert repo in registry, f"real-data repo {repo} missing from the registry"


def test_committed_report_is_fresh():
    registry = load_registry()
    regenerated = render_report(run_all_checks(), registry)
    committed = REPORT_PATH.read_text(encoding="utf-8")
    assert _normalize(committed) == _normalize(regenerated), (
        "validation/CONSISTENCY_REPORT.md is stale -- regenerate with "
        "`python -m validation.consistency_check`"
    )


def test_report_declares_all_pass():
    committed = REPORT_PATH.read_text(encoding="utf-8")
    assert "ALL CHECKS PASS" in committed
