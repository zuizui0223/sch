from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.freeze_pedicularis_g_confirmatory_method import build as freeze_method
from scripts.build_pedicularis_g_confirmatory_assignment import build as allocate
from scripts.evaluate_pedicularis_predator_method import evaluate_locked
from scripts.pedicularis_config_freeze import required_gate_paths


def _freeze() -> dict:
    return {
        "schema": "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "lane": "G",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-10-06T00:00:00Z",
        "basis_document": "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY",
        "threshold_basis": {
            path: "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY"
            for path in required_gate_paths("G")
        },
    }


def _g_config() -> dict:
    return {
        "prospective_freeze": _freeze(),
        "bootstrap_reps": 300,
        "random_seed": 67,
        "method_gate": {
            "min_paired_plants": 12,
            "min_flowers_per_treatment": 12,
            "min_hours_after_anthesis_before_barrier": 6.0,
            "max_hours_after_anthesis_before_barrier": 30.0,
            "require_pollination_window_complete": True,
            "require_ovary_not_swollen": True,
            "require_barrier_not_cover_pollinator_entry": True,
            "require_sham_on_exposed": True,
        },
        "predator_weight": {
            "min_paired_plants": 12,
            "min_flowers_per_treatment": 12,
            "min_early_attack_reduction": 0.5,
            "min_predation_fraction_reduction": 0.15,
            "min_final_seed_set_gain": 0.1,
            "max_initial_seed_set_difference": 0.03,
            "max_pollen_grain_relative_change": 0.05,
            "max_pollinator_visit_relative_change": 0.05,
            "max_z_relative_change": 0.05,
            "max_water_depth_change": 0.5,
            "max_damage_rate_difference": 0.05,
        },
    }


def _screen() -> dict:
    method = "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
    candidate = "G_TEST"
    return {
        "analysis": "pedicularis_g_candidate_linked_screen_v1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "hard_validity_pass_candidate_ids": [candidate],
        "retired_candidate_ids": [],
        "candidate_screens": {
            candidate: {
                "candidate_id": candidate,
                "field_exclusion_method": method,
                "hard_validity_all_pass": True,
            }
        },
        "candidate_selected": False,
        "status": "G_CANDIDATE_LINKED_EXPLORATORY_SCREEN_ONLY",
    }


def _method_freeze() -> dict:
    return {
        "schema": "PEDICULARIS_G_CONFIRMATORY_METHOD_FREEZE_V1",
        "status": "PEDICULARIS_G_CONFIRMATORY_METHOD_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "selected_candidate_id": "G_TEST",
        "selected_exclusion_method": "POST_POLLINATION_LOWER_FLOWER_SLEEVE",
        "exposed_sham_method_code": "SHAM_SLEEVE",
        "planned_n_plants": 16,
        "flowers_per_treatment_per_plant": 1,
        "selection_basis_note": "pre-outcome practical choice among hard-validity-pass methods",
        "frozen_before_confirmatory_G_data": True,
    }


def _manifest() -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower}",
        }
        for plant in range(16)
        for flower in range(2)
    ]


def _completed(
    allocations: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []
    for alloc in allocations:
        exposed = alloc["predator_treatment"] == "EXPOSED"
        rows.append(
            {
                "population_id": alloc["population_id"],
                "season_id": alloc["season_id"],
                "plant_id": alloc["plant_id"],
                "flower_id": alloc["flower_id"],
                "predator_treatment": alloc["predator_treatment"],
                "exclusion_method": alloc["exclusion_method"],
                "sham_device_applied": alloc["sham_device_applied"],
                "anthesis_time_hours": "0",
                "barrier_application_time_hours": "12",
                "pollination_window_complete_before_barrier": "1",
                "ovary_swollen_at_barrier": "0",
                "barrier_covers_pollinator_entry": "0",
                "pre_barrier_attack_present": "0",
                "barrier_integrity_failure_present": "0",
                "realized_exsertion": "0.50",
                "water_depth": "10.0",
                "pollen_grains": "100",
                "pollinator_visits": "10",
                "early_predator_attack_present": "1" if exposed else "0",
                "ovule_count": "100",
                "undamaged_seed_count": "50" if exposed else "68",
                "damaged_seed_count": "20" if exposed else "2",
                "mechanical_damage": "0",
            }
        )
    return rows


def _packet() -> tuple[dict, list[dict[str, str]], dict]:
    selection = freeze_method(_method_freeze(), _screen(), _g_config())
    allocations, receipt = allocate(
        _manifest(),
        selection,
        "CONFIRMATORY-G-SEED",
    )
    return selection, _completed(allocations), receipt


def test_confirmatory_g_freeze_and_randomized_allocation_validate() -> None:
    selection, rows, receipt = _packet()
    result = evaluate_locked(rows, _g_config(), receipt)

    assert selection["status"] == (
        "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTED_BEFORE_OUTCOMES"
    )
    assert receipt["assignment_randomized_within_plant"] is True
    assert receipt["n_plants"] == 16
    assert receipt["n_flowers_per_treatment"] == 16
    assert result["status"] == "PEDICULARIS_PREDATOR_METHOD_VALIDATED"
    assert result["field_allocation_verification"][
        "identity_treatment_method_sham_match"
    ] is True
    assert result["field_allocation_verification"]["selected_candidate_id"] == "G_TEST"
    assert result["field_allocation_verification"]["exposed_sham_method_code"] == (
        "SHAM_SLEEVE"
    )


def test_candidate_must_have_passed_exploratory_hard_validity() -> None:
    screen = _screen()
    screen["hard_validity_pass_candidate_ids"] = []

    with pytest.raises(ValueError, match="hard-validity pass candidate"):
        freeze_method(_method_freeze(), screen, _g_config())


def test_selected_method_must_match_candidate_matrix_linkage() -> None:
    freeze = _method_freeze()
    freeze["selected_exclusion_method"] = "AD_HOC_METHOD"

    with pytest.raises(ValueError, match="does not match"):
        freeze_method(freeze, _screen(), _g_config())


def test_selection_must_meet_frozen_g_sample_size_minima() -> None:
    freeze = _method_freeze()
    freeze["planned_n_plants"] = 10

    with pytest.raises(ValueError, match="below the frozen G minimum paired plants"):
        freeze_method(freeze, _screen(), _g_config())


def test_confirmatory_g_treatment_drift_fails_locked_evaluator() -> None:
    _, rows, receipt = _packet()
    rows[0]["predator_treatment"] = (
        "EXCLUDED" if rows[0]["predator_treatment"] == "EXPOSED" else "EXPOSED"
    )

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        evaluate_locked(rows, _g_config(), receipt)


def test_confirmatory_g_method_drift_fails_locked_evaluator() -> None:
    _, rows, receipt = _packet()
    rows[0]["exclusion_method"] = "AD_HOC_METHOD"

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        evaluate_locked(rows, _g_config(), receipt)


def test_confirmatory_g_flower_substitution_fails_locked_evaluator() -> None:
    _, rows, receipt = _packet()
    rows[0]["flower_id"] = "SUBSTITUTED_FLOWER"

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        evaluate_locked(rows, _g_config(), receipt)


def test_allocation_is_bound_to_exact_g_field_config() -> None:
    _, rows, receipt = _packet()
    changed = deepcopy(_g_config())
    changed["method_gate"]["max_hours_after_anthesis_before_barrier"] = 29.0

    with pytest.raises(ValueError, match="exact G field config"):
        evaluate_locked(rows, changed, receipt)
