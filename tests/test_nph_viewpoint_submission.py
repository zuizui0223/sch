from pathlib import Path
import re

from scripts import build_sch_viewpoint_figures_svg as figures

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "SCH_NPH_VIEWPOINT_V1.md"
PRESUB = ROOT / "manuscript" / "NPH_PRESUBMISSION_ENQUIRY_V1.md"


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-’'][A-Za-z0-9]+)*", text)


def _section(text: str, heading: str, next_heading_prefix: str = "## ") -> str:
    marker = f"## {heading}\n"
    assert marker in text
    tail = text.split(marker, 1)[1]
    m = re.search(r"\n## ", tail)
    return tail[: m.start()] if m else tail


def test_viewpoint_title_summary_and_keywords() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ")
    assert len(title) <= 130

    summary = _section(text, "Summary")
    assert len(_words(summary)) <= 200

    keyword_line = next(line for line in text.splitlines() if line.startswith("**Key words:**"))
    keywords = [k.strip(" .") for k in keyword_line.split(":", 1)[1].split(";")]
    assert 5 <= len(keywords) <= 8
    assert keywords == sorted(keywords, key=str.lower)


def test_viewpoint_preserves_frozen_evidence_counts_and_ceiling() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for token in (
        "16 independent plant systems",
        "Five clusters",
        "Seven additional clusters",
        "Two clusters are aligned/no-conflict controls",
        "fail-closed",
        "they are not estimates of natural prevalence",
    ):
        assert token.lower() in text.lower()

    assert "does not establish that those functions favor different trait states" in text
    assert "not automatically the pure optima" in text
    assert "does not, by itself, identify" in text


def test_viewpoint_keeps_sch_upstream_of_slk_and_bita() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "first establish whether conflict exists on the shared coordinate" in text
    assert "downstream architecture" in text
    assert "orthogonal identification problem" in text
    # SCH must not claim the SLK quadratic architecture bridge as its own result.
    assert "Phi=sL-K" not in text
    assert "Φ=sL-K" not in text


def test_presubmission_answers_within_fifty_words() -> None:
    text = PRESUB.read_text(encoding="utf-8")
    for i in (1, 2, 3):
        marker = f"### {i}."
        start = text.index(marker)
        body_start = text.index("\n\n", start) + 2
        next_marker = text.find("\n### ", body_start)
        if next_marker == -1:
            next_marker = text.find("\n\nThe full manuscript", body_start)
        body = text[body_start:next_marker].strip()
        assert len(_words(body)) <= 50, (i, len(_words(body)), body)


def test_builds_four_viewpoint_figures(tmp_path: Path) -> None:
    paths = figures.build(tmp_path)
    assert [p.name for p in paths] == figures.FIGURE_NAMES
    assert len(paths) == 4
    for path in paths:
        svg = path.read_text(encoding="utf-8")
        assert svg.startswith("<svg")
        assert svg.endswith("</svg>")
        assert "Multifunctionality" in svg or "Figure" in svg


def test_figure3_matches_frozen_pattern_ledger_counts() -> None:
    svg = figures.fig3()
    assert "16 independent biological clusters" in svg
    assert "Direct conflict signatures" in svg and ">5<" in svg
    assert "Context-weight shifts" in svg and ">7<" in svg
    assert "Aligned / no-conflict controls" in svg and ">2<" in svg
    assert "random-effects stratum" in svg


def test_figure4_preserves_programme_ownership() -> None:
    svg = figures.fig4()
    assert "SCH — identify conflict" in svg
    assert "SLK — transport value" in svg
    assert "BITA" in svg
    assert "orthogonal" in svg
