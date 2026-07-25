"""Smoke tests for the case-study deliverables.

Checks that the PDF builds and is non-trivial, that the web page stays fully
self-contained (no external asset references), and that the disclaimer-first
framing is present in both the README and the web page.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DISCLAIMER_PHRASE = "not affiliated with, endorsed by, or reviewed by W"


def test_build_pdf_produces_pdf_over_10kb():
    result = subprocess.run(
        [sys.executable, str(ROOT / "build_pdf.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, f"build_pdf.py failed: {result.stdout}\n{result.stderr}"
    pdf = ROOT / "deliverables" / "wuerth_data_ai_casestudy.pdf"
    assert pdf.exists(), "PDF was not written"
    size = pdf.stat().st_size
    assert size > 10 * 1024, f"PDF too small: {size} bytes"
    assert pdf.read_bytes()[:5] == b"%PDF-", "output is not a PDF"


def test_web_page_has_no_external_asset_refs():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert "@import" not in html, "external stylesheet import found"
    assert re.search(r"url\(\s*['\"]?https?://", html) is None, "external url() reference found"
    for match in re.finditer(r"""(src|href)\s*=\s*["'](https?://[^"']+)["']""", html):
        attr, url = match.groups()
        # Plain github.com anchors are allowed; loaded assets are not.
        assert attr == "href" and url.startswith("https://github.com/"), (
            f"external asset reference found: {match.group(0)}"
        )


def test_disclaimer_present_in_readme_and_web():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert DISCLAIMER_PHRASE in readme, "disclaimer missing from README.md"
    assert DISCLAIMER_PHRASE in html, "disclaimer missing from web/index.html"
