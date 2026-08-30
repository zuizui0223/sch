from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSITIONING = ROOT / "docs" / "CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md"
NICOTIANA = ROOT / "docs" / "NICOTIANA_PROGRAM_COMPOSITE_BRIDGE_V1.md"
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


def test_positioning_separates_information_from_three_functional_levels() -> None:
    text = _text(POSITIONING)
    assert "Informational / architectural escape" in text
    assert "Functional interaction relief" in text
    assert "Functional constraint release" in text
    assert "Strict functional reversal" in text
    assert "Antagonists may still detect `A`" in text
    assert "cue privacy" in text
    assert "A positive `Delta_AD W` can occur while `A0` and `A1` are both negative" in text


def test_positive_total_interaction_is_only_level_one_without_A0_A1() -> None:
    text = _text(POSITIONING)
    assert "This equivalence decides the Level-1 total-interaction inequality" in text
    assert "Levels 2 and 3 require the conditional attraction contrasts `A0` and `A1`" in text
    assert "Full channel point identification is not required for a valid outcome-level decision" in text
    assert "Did `D` improve the attraction effect?" in text
    assert "Did that improvement release a non-beneficial state?" in text
    assert "Did it strictly reverse a negative state?" in text
    stale = (
        "all three terms must be identified before escape can be decided",
        "the complete escape inequality remains unevaluable because",
        "A positive total interaction is functional escape",
    )
    for phrase in stale:
        assert phrase not in text


def test_current_evidence_ceiling_preserves_kessler_hierarchy_uncertainty_and_scope() -> None:
    text = _text(POSITIONING)
    assert "Level 1: strong positive aggregate-sign anchor" in text
    assert "Level 2: unresolved" in text
    assert "Level 3: unresolved" in text
    assert "exact source/design-based intervals have not been recovered" in text
    assert "nicotine suppression is systemic" in text
    assert "does not automatically equal release of a previously negative attraction effect" in text


def test_nicotiana_is_a_program_composite_not_a_merged_experiment() -> None:
    positioning = _text(POSITIONING)
    bridge = _text(NICOTIANA)
    for text in (positioning, bridge):
        assert "PROGRAM_COMPOSITE_NEAR_COMPLETE" in text
        assert "DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED" in text
    for doi in (
        "10.7554/eLife.07641",
        "10.1126/science.1160072",
        "10.1073/pnas.1703463114",
        "10.1111/jipb.12607",
    ):
        assert doi in bridge
    assert "cannot be combined as though they were one experimental table" in bridge
    assert "infer constraint release from `Delta_AD W > 0` alone" in bridge
    assert "same hawkmoth can contribute both pollination and oviposition" in bridge
    assert "forcing a separable BITA decomposition" in bridge
