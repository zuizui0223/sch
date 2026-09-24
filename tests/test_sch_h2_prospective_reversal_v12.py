import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "freeze_sch_h2_prospective_reversal_v12.py"


def _mod():
    spec = importlib.util.spec_from_file_location("h2v12", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_v12_freezes_the_preexisting_463_record_outcome_blind_holdout():
    result = _mod().build(ROOT)
    assert result["formal_prisma_denominator"] == 868
    assert result["n_holdout_records"] == 463
    assert result["holdout_tier_counts"] == {
        "TA0_EXPLICIT_SELECTION": 32,
        "TA1_FINAL_PERFORMANCE": 25,
        "TA2_REPEATED_CONTEXT": 20,
        "TA3_REMAINDER": 386,
    }
    assert result["design_classification_timing"] == (
        "BEFORE_SELECTION_SIGN_OR_SIGNIFICANCE_EXTRACTION"
    )


def test_v12_excludes_every_v11_pilot_programme_from_confirmation():
    result = _mod().build(ROOT)
    assert result["pilot_status"] == "V11_HYPOTHESIS_GENERATING_ONLY"
    assert result["n_pilot_programmes_excluded"] == 8
    assert len(set(result["pilot_programmes_excluded"])) == 8
    assert "Gymnadenia_conopsea_agent_selection" in result["pilot_programmes_excluded"]
    assert "Helianthus_annuus_texanus_Mitchell_selection_program" in result["pilot_programmes_excluded"]


def test_v12_classification_is_design_first_and_spatial_is_external():
    classify = _mod().classify_context_design

    assert classify(
        experimental=True,
        observational_spatial=False,
        n_manipulated_biotic_dimensions=2,
        consumer_identity_or_composition_changes=False,
    ) == "MULTIWEIGHT_OR_CONSUMER_TURNOVER"

    assert classify(
        experimental=True,
        observational_spatial=False,
        n_manipulated_biotic_dimensions=1,
        consumer_identity_or_composition_changes=False,
    ) == "SINGLE_FACTOR_INTENSITY"

    assert classify(
        experimental=True,
        observational_spatial=False,
        n_manipulated_biotic_dimensions=1,
        consumer_identity_or_composition_changes=True,
    ) == "MULTIWEIGHT_OR_CONSUMER_TURNOVER"

    assert classify(
        experimental=False,
        observational_spatial=True,
        n_manipulated_biotic_dimensions=0,
        consumer_identity_or_composition_changes=False,
    ) == "EXTERNAL_SPATIAL_REPLICATION"

    assert classify(
        experimental=False,
        observational_spatial=False,
        n_manipulated_biotic_dimensions=0,
        consumer_identity_or_composition_changes=False,
    ) == "UNCLASSIFIABLE_FAIL_CLOSED"


def test_v12_primary_inference_gate_depends_only_on_design_breadth():
    gate = _mod().confirmatory_gate

    assert gate(
        n_multiweight_programmes=5,
        n_single_factor_programmes=4,
    )["primary_inference_licensed"] is False

    assert gate(
        n_multiweight_programmes=4,
        n_single_factor_programmes=5,
    )["primary_inference_licensed"] is False

    assert gate(
        n_multiweight_programmes=5,
        n_single_factor_programmes=5,
    )["primary_inference_licensed"] is True


def test_v12_uses_programmes_not_axes_as_inferential_replicates():
    result = _mod().build(ROOT)
    assert result["primary_unit"] == "INDEPENDENT_BIOLOGICAL_PROGRAMME"
    assert "mean(q_j" in result["primary_estimand"]
    assert "trait_axes_are_not_independent_replicates" in result["claim_ceiling"]
    assert "zero observed reversal is retained as a valid result" in result["primary_inference"]


def test_v12_frozen_receipt_matches_builder():
    result = _mod().build(ROOT)
    frozen = json.loads(
        (ROOT / "data" / "SCH_H2_PROSPECTIVE_REVERSAL_HYPOTHESIS_V12.json").read_text(
            encoding="utf-8"
        )
    )
    assert result == frozen
