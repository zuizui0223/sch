from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RANKING = ROOT / "docs" / "SCH_GENERALIZED_EXECUTION_CANDIDATE_RANKING_V1.md"
EXPERIMENT = ROOT / "docs" / "SCH_DALECHAMPIA_CAUSAL_COMPROMISE_EXPERIMENT_V1.md"
RECOVERY = ROOT / "docs" / "SCH_DALECHAMPIA_GEOGRAPHIC_CONFLICT_AND_G0_RECOVERY_V1.md"
FIELD = ROOT / "docs" / "SCH_DALECHAMPIA_STAGE0_FIELD_EXECUTION_PROTOCOL_V1.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_dalechampia_is_conditional_not_species_wide_positive() -> None:
    readme = _text(README)
    ranking = _text(RANKING)
    recovery = _text(RECOVERY)
    assert "conditional first-choice" in readme
    assert "CONDITIONAL_FIRST_CHOICE_CAUSAL_COMPROMISE_SYSTEM" in ranking
    assert "Dalechampia species-wide conflict" in recovery
    assert "NOT SUPPORTED" in recovery
    assert "Costa Rica" in ranking
    assert "Mexican" in ranking or "Mexico" in ranking


def test_oviposition_is_not_overclaimed() -> None:
    experiment = _text(EXPERIMENT)
    recovery = _text(RECOVERY)
    field = _text(FIELD)
    assert "DIRECT_OVIPOSITION_WINDOW" in experiment
    assert "NOT RECOVERED" in experiment
    assert "Do not call this direct oviposition" in experiment
    assert "conditional on the assumption" in recovery
    assert "differential larval success" in recovery
    assert "controlled adult exposure is a new Stage-0 method" in field
    assert "not a recovered published Nanobaris protocol" in field


def test_antagonist_gate_uses_controlled_sequential_exposure() -> None:
    experiment = _text(EXPERIMENT)
    recovery = _text(RECOVERY)
    for text in (experiment, recovery):
        assert "controlled sequential" in text.lower()
        assert "female-phase exposure" in text
        assert "early bisexual" in text
        assert "post-receptive" in text
    assert "G1 controlled exposure materially increases later seed loss" in experiment
    assert "G0 no-exposure / validated exclusion keeps later seed loss low" in experiment


def test_failed_population_screen_is_biologically_interpretable() -> None:
    recovery = _text(RECOVERY)
    experiment = _text(EXPERIMENT)
    assert "Failure to find a conflict-active population is a biological result" in recovery
    assert "weak antagonist weight can erase the compromise" in experiment


def test_field_protocol_controls_enclosure_sex_and_fallback() -> None:
    text = _text(FIELD)
    assert "same enclosure + no adults" in text
    assert "mixed-adult exposure = feasibility evidence only" in text
    assert "DIRECT_OVIPOSITION_MARKER_OBSERVED" in text
    assert "switch causal compromise closure to Castilleja" in text
    assert ">= 5 z levels x 2 P states x 2 G states" in text
