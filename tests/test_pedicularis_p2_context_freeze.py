from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_p2_context_priors import (
    DEFAULT_PRIORS,
    _read,
    build as audit_priors,
)
from scripts.freeze_pedicularis_p2_context import build


def _readiness() -> dict:
    checks = {
        "z_schema": True,
        "z_status": True,
        "z_context_present": True,
        "z_threshold_freeze": True,
        "p_schema": True,
        "p_status": True,
        "p_context_present": True,
        "p_threshold_freeze": True,
        "g_schema": True,
        "g_status": True,
        "g_context_present": True,
        "g_threshold_freeze": True,
        "same_population_and_season": True,
        "g_method_timing_validated": True,
    }
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "population_id": "P_REX_FIELD",
        "season_id": "S2027",
        "checks": checks,
        "source_receipts": {
            "z": {
                "schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
                "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED",
                "threshold_freeze_status": (
                    "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN"
                ),
            },
            "p": {
                "schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
                "status": "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED",
                "threshold_freeze_status": (
                    "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN"
                ),
            },
            "g": {
                "schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
                "status": "PEDICULARIS_PREDATOR_METHOD_VALIDATED",
                "threshold_freeze_status": (
                    "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN"
                ),
            },
        },
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": (
            "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_"
            "POLLINATOR_ACCESS_PRESERVED"
        ),
    }


def _current_config() -> dict:
    return {
        "schema": "PEDICULARIS_P2_CONTEXT_FREEZE_CONFIG_V1",
        "status": "PEDICULARIS_P2_CONTEXT_SELECTION_PROSPECTIVELY_DECLARED",
        "population_id": "P_REX_FIELD",
        "season_id": "S2027",
        "historical_population_code": "NONE",
        "selection_mode": "CURRENT_CONTEXT_ONLY",
        "inference_scope": "PRIMARY_TESTED_CONTEXT_ONLY",
        "selection_basis_note": (
            "Current population/season proceeds only after same-context "
            "P1 and G validation; no historical population identity is claimed."
        ),
        "declared_before_full_surface_outcomes": True,
        "historical_mapping_status": "NONE",
        "historical_mapping_source": "NONE",
    }


def _historical_config() -> dict:
    config = _current_config()
    config.update(
        {
            "historical_population_code": "POP5",
            "selection_mode": "HISTORICAL_CONTEXT_PRIOR",
            "inference_scope": "PRIMARY_HIGH_ANTAGONISM_ENRICHED_CONTEXT",
            "selection_basis_note": (
                "Source-verified revisit of the historical POP5 locality, "
                "subject to current-season P1/G validation."
            ),
            "historical_mapping_status": "SOURCE_VERIFIED",
            "historical_mapping_source": (
                "Sun et al. 2016 Supplementary Table S1, source-verified "
                "POP5 locality mapping"
            ),
        }
    )
    return config


def test_historical_prior_ledger_locks_exact_pressure_and_linkage_facts() -> None:
    result = audit_priors(_read(DEFAULT_PRIORS))

    assert result["n_historical_populations"] == 12
    assert result["linked_historical_populations"] == [
        "POP1",
        "POP10",
        "POP11",
        "POP3",
        "POP5",
        "POP8",
        "POP9",
    ]
    assert result["exact_main_text_pressure_cases"]["POP5"][
        "seed_predation_percent"
    ] == 27.42
    assert result["exact_main_text_pressure_cases"]["POP5"]["rank"] == 1
    assert result["exact_main_text_pressure_cases"]["POP12"][
        "seed_predation_percent"
    ] == 18.50
    assert result["exact_main_text_pressure_cases"]["POP12"]["linked"] is False
    assert result["historical_prior_can_select_p2_context_automatically"] is False


def test_current_context_can_freeze_without_claiming_historical_identity() -> None:
    result = build(
        _current_config(),
        _readiness(),
        _read(DEFAULT_PRIORS),
    )

    assert result["historical_context_prior"] is None
    assert result["same_season_pollination_and_antagonist_lanes_validated"] is True
    assert result["current_season_context"]["pollination_lane_validated"] is True
    assert result["current_season_context"]["antagonist_lane_validated"] is True
    assert result["status"] == (
        "P2_CONTEXT_FROZEN_CURRENT_SEASON_BOTH_FUNCTIONAL_LANES_VALIDATED"
    )


def test_source_verified_pop5_prior_can_be_attached_but_not_promoted_to_current_pressure() -> None:
    result = build(
        _historical_config(),
        _readiness(),
        _read(DEFAULT_PRIORS),
    )

    prior = result["historical_context_prior"]
    assert prior["historical_population_code"] == "POP5"
    assert prior["exact_main_text_seed_predation_percent"] == 27.42
    assert prior["exact_pressure_rank_among_four"] == 1
    assert prior["individual_linkage_retained"] is True
    assert prior["history_class"] == "HIGHEST_EXACT_PRESSURE_LINKED"
    assert prior["historical_value_is_current_season_measurement"] is False
    assert prior["mapping_status"] == "SOURCE_VERIFIED"
    assert "historical_pressure_is_recruitment_prior" in str(
        result["claim_ceiling"]
    )


def test_pop5_code_is_rejected_without_source_verified_locality_mapping() -> None:
    config = _historical_config()
    config["historical_mapping_status"] = "NONE"
    config["historical_mapping_source"] = "NONE"

    with pytest.raises(ValueError, match="SOURCE_VERIFIED locality mapping"):
        build(config, _readiness(), _read(DEFAULT_PRIORS))


def test_current_context_mode_cannot_smuggle_historical_code() -> None:
    config = _current_config()
    config["historical_population_code"] = "POP5"

    with pytest.raises(ValueError, match="historical_population_code=NONE"):
        build(config, _readiness(), _read(DEFAULT_PRIORS))


def test_readiness_context_must_match_selected_context() -> None:
    readiness = _readiness()
    readiness["season_id"] = "S2028"

    with pytest.raises(ValueError, match="season_id does not match"):
        build(_current_config(), readiness, _read(DEFAULT_PRIORS))


def test_negative_current_pollination_lane_blocks_context_freeze() -> None:
    readiness = _readiness()
    readiness["source_receipts"]["p"]["status"] = (
        "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"
    )

    with pytest.raises(ValueError, match="pollination lane is not validated"):
        build(_current_config(), readiness, _read(DEFAULT_PRIORS))


def test_negative_current_antagonist_lane_blocks_context_freeze() -> None:
    readiness = _readiness()
    readiness["source_receipts"]["g"]["status"] = (
        "PEDICULARIS_PREDATOR_METHOD_NOT_VALIDATED"
    )

    with pytest.raises(ValueError, match="antagonist lane is not validated"):
        build(_current_config(), readiness, _read(DEFAULT_PRIORS))


def test_context_selection_must_predate_full_surface_outcomes() -> None:
    config = _current_config()
    config["declared_before_full_surface_outcomes"] = False

    with pytest.raises(ValueError, match="before full-surface outcomes"):
        build(config, _readiness(), _read(DEFAULT_PRIORS))
