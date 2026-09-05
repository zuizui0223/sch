from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSITIONING = ROOT / "docs" / "CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md"
NICOTIANA = ROOT / "docs" / "NICOTIANA_PROGRAM_COMPOSITE_BRIDGE_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"
README = ROOT / "README.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_sch_keeps_local_conflict_and_compromise_as_chapter_one_estimands() -> None:
    manuscript = _text(MANUSCRIPT)
    readme = _text(README)
    assert "M_A(g)" in manuscript
    assert "G_A(p)" in manuscript
    assert "does not by itself locate the full compromise optimum" in manuscript
    assert "z_1^*" in manuscript or "z1*" in manuscript
    assert "Chapter 2 / BITA" in readme
    assert "functional differentiation / modularization" in readme


def test_positioning_separates_shared_compromise_from_functional_differentiation() -> None:
    text = _text(POSITIONING)
    assert "D1  shared conflict exists" in text
    assert "D2  preferential functional loading" in text
    assert "D3  dimensional release" in text
    assert "D4  mechanism allocation" in text
    assert "D5  historical modularization" in text
    assert "Contemporary experiments can establish D1-D4 without proving D5." in text


def test_positive_total_interaction_remains_only_level_one_without_A0_A1() -> None:
    text = _text(POSITIONING)
    assert "Delta_AD W = A1 - A0." in text
    assert "Level 1  positive interaction relief" in text
    assert "Delta_AD W > 0" in text
    assert "Level 2  constraint release" in text
    assert "A0 <= 0 < A1" in text
    assert "Level 3  strict reversal" in text
    assert "A0 < 0 < A1" in text


def test_current_kessler_evidence_ceiling_is_preserved_in_program_bridge() -> None:
    text = _text(NICOTIANA)
    assert "POSITIVE_AGGREGATE_INTERACTION_SIGN_ANCHOR" in text
    assert "exact source/design-based interaction uncertainty is not recovered" in text
    assert "systemic nicotine suppression" in text
    assert "infer constraint release from `Delta_AD W > 0` alone" in text
    assert "does not yet allocate the mechanism" in text


def test_nicotiana_is_a_program_composite_not_a_merged_experiment() -> None:
    bridge = _text(NICOTIANA)
    positioning = _text(POSITIONING)
    assert "PROGRAM_COMPOSITE_NEAR_COMPLETE" in bridge
    assert "DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED" in bridge
    for doi in (
        "10.7554/eLife.07641",
        "10.1126/science.1160072",
        "10.1073/pnas.1703463114",
        "10.1111/jipb.12607",
    ):
        assert doi in bridge
    assert "cannot be combined as though they were one experimental table" in bridge
    assert "a hawkmoth can contribute both pollination and oviposition" in bridge
    assert "forcing a separable BITA decomposition" in bridge
    assert "pollinator-antagonist floral system is the main empirical realization" in positioning
