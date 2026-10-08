from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_p2_dual_endpoint_feasibility import (
    READY_STATUS,
    build,
    validate_receipt,
)


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_CONFIG_V1",
        "status": "PEDICULARIS_P2_DUAL_ENDPOINT_ASSAY_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "collection_route": "SAME_FLOWER_NONDESTRUCTIVE_POLLEN_QUANTIFICATION",
        "pollen_assay_method_id": "SYNTHETIC_ASSAY_TEST_ONLY",
        "assay_protocol_reference": "SYNTHETIC_ASSAY_SPEC_ONLY",
        "seed_endpoint_protocol_reference": "SYNTHETIC_SEED_ENDPOINT_SPEC_ONLY",
        "compatibility_margin_basis": "SYNTHETIC_MARGIN_PREOUTCOME",
        "frozen_before_compatibility_pilot_outcomes": True,
    }


def _pilot() -> dict:
    return {
        "receipt_schema": "PEDICULARIS_P2_DUAL_ENDPOINT_PILOT_VALIDATION_V1",
        "status": "PEDICULARIS_P2_DUAL_ENDPOINT_COMPATIBILITY_VALIDATED",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "pollen_assay_method_id": "SYNTHETIC_ASSAY_TEST_ONLY",
        "collection_route": "SAME_FLOWER_NONDESTRUCTIVE_POLLEN_QUANTIFICATION",
        "prospective_acceptance_margins_frozen": True,
        "pilot_cohort_independent_of_confirmatory_P2": True,
        "same_flower_pollen_count_and_mature_seed_linkage_verified": True,
        "pollen_count_accuracy_against_independent_reference_pass": True,
        "mature_seed_noninterference_equivalence_pass": True,
        "pollination_and_predator_treatment_compatibility_pass": True,
        "positive_nonzero_pollen_and_mature_seed_records_recovered": True,
        "pilot_data_sha256": "a" * 64,
        "pilot_protocol_basis": "SYNTHETIC_MARGIN_PREOUTCOME",
    }


def test_independent_same_flower_compatibility_receipt_qualifies_current_layout() -> None:
    receipt = build(_config(), _pilot())
    assert receipt["status"] == READY_STATUS
    assert receipt["flower_endpoint_unit"] == "SAME_FLOWER"
    assert receipt["same_flower_pollen_and_mature_seeds_validated"] is True
    assert len(receipt["independent_pilot_receipt_sha256"]) == 64
    assert len(receipt["frozen_config_sha256"]) == 64
    assert validate_receipt(receipt, "P_REX_TEST", "S1")["status"] == READY_STATUS


def test_unfrozen_templates_cannot_authorize_joint_endpoints() -> None:
    config = _config()
    config["status"] = "REQUIRED_BEFORE_USE"

    with pytest.raises(ValueError, match="not prospectively frozen"):
        build(config, _pilot())


def test_historical_destructive_stigma_slide_protocol_does_not_authorize_p2() -> None:
    config = _config()
    config["collection_route"] = "DESTRUCTIVE_STIGMA_CRUSHING"
    pilot = _pilot()
    pilot["collection_route"] = "DESTRUCTIVE_STIGMA_CRUSHING"

    with pytest.raises(ValueError, match="unvalidated destructive stigma crushing"):
        build(config, pilot)


def test_split_pollen_sentinels_require_new_cohort_and_power_design() -> None:
    config = _config()
    config["collection_route"] = "SPLIT_FLOWER_POLLEN_SENTINEL"
    pilot = _pilot()
    pilot["collection_route"] = "SPLIT_FLOWER_POLLEN_SENTINEL"

    with pytest.raises(ValueError, match="two-cohort estimator"):
        build(config, pilot)


@pytest.mark.parametrize(
    "failed_field",
    [
        "pilot_cohort_independent_of_confirmatory_P2",
        "same_flower_pollen_count_and_mature_seed_linkage_verified",
        "pollen_count_accuracy_against_independent_reference_pass",
        "mature_seed_noninterference_equivalence_pass",
        "pollination_and_predator_treatment_compatibility_pass",
        "positive_nonzero_pollen_and_mature_seed_records_recovered",
        "prospective_acceptance_margins_frozen",
    ],
)
def test_any_missing_independent_pilot_gate_blocks_p2(failed_field: str) -> None:
    pilot = _pilot()
    pilot[failed_field] = False
    with pytest.raises(ValueError, match="compatibility gates did not all pass"):
        build(_config(), pilot)


def test_posthoc_margin_edit_does_not_match_independent_pilot() -> None:
    config = _config()
    config["compatibility_margin_basis"] = "AFTER_SEED_OUTCOMES"
    with pytest.raises(ValueError, match="margin basis does not match"):
        build(config, _pilot())


def test_validation_must_match_assay_method_and_population_season() -> None:
    pilot = _pilot()
    pilot["pollen_assay_method_id"] = "DIFFERENT_ASSAY"
    with pytest.raises(ValueError, match="different pollen assay"):
        build(_config(), pilot)

    receipt = build(_config(), _pilot())
    with pytest.raises(ValueError, match="population/season does not match"):
        validate_receipt(receipt, "P_REX_TEST", "S2")


def test_unsupported_split_route_cannot_be_relabelled_as_positive() -> None:
    receipt = deepcopy(build(_config(), _pilot()))
    receipt["collection_route"] = "SPLIT_FLOWER_POLLEN_SENTINEL"
    with pytest.raises(ValueError, match="split-flower sentinels"):
        validate_receipt(receipt, "P_REX_TEST", "S1")


def test_missing_pilot_data_fingerprint_is_not_evidence() -> None:
    pilot = _pilot()
    pilot["pilot_data_sha256"] = "UNKNOWN"
    with pytest.raises(ValueError, match="64-character SHA-256"):
        build(_config(), pilot)
