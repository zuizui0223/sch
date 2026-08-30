from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSITIONING = ROOT / "docs" / "CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_SHARED_CUE_FRAMEWORK.md"
README = ROOT / "README.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_sch_keeps_the_one_trait_conflict_as_its_own_estimand() -> None:
    manuscript = _text(MANUSCRIPT)
    readme = _text(README)
    assert "M_A =" in manuscript
    assert "G_A =" in manuscript
    assert "S_A = M_A - G_A" in manuscript
    assert "This is not the BITA two-trait estimand" in readme
    assert "requires neither a second trait `D` nor `Delta_AD W`" in manuscript
    assert "Delta_AD W =" not in manuscript.split("## 9. Separation from BITA", 1)[0]


def test_positioning_separates_informational_from_functional_escape() -> None:
    text = _text(POSITIONING)
    assert "Informational / architectural escape" in text
    assert "Functional escape" in text
    assert "Antagonists may still detect `A`" in text
    assert "does not establish" in text
    assert "cue privacy" in text


def test_total_escape_sign_does_not_require_full_channel_identification() -> None:
    text = _text(POSITIONING)
    assert "uncertainty lies wholly above zero is sufficient" in text
    assert "Full channel point identification is therefore not required" in text
    assert "further explanatory gate rather than a prerequisite" in text
    stale = (
        "all three terms must be identified before escape can be decided",
        "the complete escape inequality remains unevaluable because",
    )
    for phrase in stale:
        assert phrase not in text


def test_current_evidence_ceiling_preserves_kessler_uncertainty_and_scope() -> None:
    text = _text(POSITIONING)
    assert "positive total interaction sign" in text
    assert "exact source/design-based interaction interval has not been recovered" in text
    assert "nicotine suppression is systemic" in text
    assert "Formal positive functional escape is therefore not yet uncertainty-identified" in text
