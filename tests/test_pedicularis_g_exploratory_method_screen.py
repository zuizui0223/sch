from __future__ import annotations

from scripts.screen_pedicularis_g_exploratory_methods import build


def _rows(
    *,
    method_b_integrity_failure: bool = True,
    method_a_pre_attack: bool = False,
    both_pass: bool = False,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(6):
        plant_id = f"P{plant:02d}"

        rows.append(
            {
                "population_id": "P_REX_TEST",
                "season_id": "S1",
                "plant_id": plant_id,
                "flower_id": f"{plant_id}_EXPOSED",
                "predator_treatment": "EXPOSED",
                "exclusion_method": "SHAM_SLEEVE",
                "sham_device_applied": "1",
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
                "early_predator_attack_present": "1",
                "ovule_count": "100",
                "undamaged_seed_count": "50",
                "damaged_seed_count": "20",
                "mechanical_damage": "0",
            }
        )

        rows.append(
            {
                "population_id": "P_REX_TEST",
                "season_id": "S1",
                "plant_id": plant_id,
                "flower_id": f"{plant_id}_A",
                "predator_treatment": "EXCLUDED",
                "exclusion_method": "LOWER_FLOWER_MESH_A",
                "sham_device_applied": "0",
                "anthesis_time_hours": "0",
                "barrier_application_time_hours": "12",
                "pollination_window_complete_before_barrier": "1",
                "ovary_swollen_at_barrier": "0",
                "barrier_covers_pollinator_entry": "0",
                "pre_barrier_attack_present": "1" if method_a_pre_attack else "0",
                "barrier_integrity_failure_present": "0",
                "realized_exsertion": "0.50",
                "water_depth": "10.0",
                "pollen_grains": "100",
                "pollinator_visits": "10",
                "early_predator_attack_present": "0",
                "ovule_count": "100",
                "undamaged_seed_count": "68",
                "damaged_seed_count": "2",
                "mechanical_damage": "0",
            }
        )

        rows.append(
            {
                "population_id": "P_REX_TEST",
                "season_id": "S1",
                "plant_id": plant_id,
                "flower_id": f"{plant_id}_B",
                "predator_treatment": "EXCLUDED",
                "exclusion_method": "LOCAL_OVIPOSITOR_BARRIER_B",
                "sham_device_applied": "0",
                "anthesis_time_hours": "0",
                "barrier_application_time_hours": "14",
                "pollination_window_complete_before_barrier": "1",
                "ovary_swollen_at_barrier": "0",
                "barrier_covers_pollinator_entry": "0",
                "pre_barrier_attack_present": "0",
                "barrier_integrity_failure_present": (
                    "0"
                    if (both_pass or not method_b_integrity_failure)
                    else "1"
                ),
                "realized_exsertion": "0.50",
                "water_depth": "10.0",
                "pollen_grains": "99",
                "pollinator_visits": "10",
                "early_predator_attack_present": "0",
                "ovule_count": "100",
                "undamaged_seed_count": "64",
                "damaged_seed_count": "4",
                "mechanical_damage": "0",
            }
        )
    return rows


def test_one_method_can_pass_hard_validity_without_being_selected() -> None:
    result = build(_rows())

    assert result["status"] == "G_EXPLORATORY_FAIL_FAST_SCREEN_ONLY"
    assert result["n_candidate_methods"] == 2
    assert result["hard_validity_pass_methods"] == ["LOWER_FLOWER_MESH_A"]
    assert result["n_hard_validity_pass_methods"] == 1
    assert result["current_frontier"] == (
        "ONE_METHOD_PASSES_HARD_VALIDITY_"
        "EFFECT_AND_SELECTIVITY_TARGETS_STILL_UNFROZEN"
    )
    assert result["method_selected"] is False
    assert result["effect_thresholds_applied"] is False
    assert result["selectivity_thresholds_applied"] is False
    assert result["confirmatory_receipt_generated"] is False


def test_integrity_failure_is_visible_per_method() -> None:
    result = build(_rows())
    method_b = result["method_screens"]["LOCAL_OVIPOSITOR_BARRIER_B"]

    assert method_b["hard_validity_all_pass"] is False
    assert method_b["hard_validity_flags"][
        "barrier_integrity_preserved"
    ] is False
    assert method_b["hard_validity_failure_counts"][
        "barrier_integrity_preserved"
    ] == 6
    assert method_b["screen_state"] == (
        "HARD_VALIDITY_FAIL_METHOD_SHOULD_NOT_ADVANCE_AS_IS"
    )


def test_multiple_hard_validity_passes_do_not_trigger_automatic_selection() -> None:
    result = build(_rows(method_b_integrity_failure=False, both_pass=True))

    assert result["n_hard_validity_pass_methods"] == 2
    assert result["current_frontier"] == (
        "MULTIPLE_METHODS_PASS_HARD_VALIDITY_NO_AUTOMATIC_METHOD_SELECTION"
    )
    assert result["method_selected"] is False


def test_no_method_passes_when_registered_hard_validity_fails() -> None:
    rows = _rows(method_a_pre_attack=True)

    for row in rows:
        if (
            row["predator_treatment"] == "EXCLUDED"
            and row["exclusion_method"] == "LOCAL_OVIPOSITOR_BARRIER_B"
        ):
            row["barrier_integrity_failure_present"] = "1"

    result = build(rows)
    assert result["hard_validity_pass_methods"] == []
    assert result["current_frontier"] == (
        "NO_METHOD_PASSES_REGISTERED_HARD_VALIDITY"
    )


def test_effect_distributions_are_descriptive_not_gate_results() -> None:
    result = build(_rows())
    method_a = result["method_screens"]["LOWER_FLOWER_MESH_A"]

    assert method_a["effect_distributions"]["predation_reduction"]["mean"] > 0
    assert method_a["effect_distributions"]["final_seed_gain"]["mean"] > 0
    assert method_a["contamination_distributions"][
        "pollen_relative_change"
    ]["mean"] == 0
    assert "does_not_validate_registered_G" in result["claim_ceiling"]


def test_each_method_has_timing_and_paired_plant_distributions() -> None:
    result = build(_rows())
    method_a = result["method_screens"]["LOWER_FLOWER_MESH_A"]
    method_b = result["method_screens"]["LOCAL_OVIPOSITOR_BARRIER_B"]

    assert method_a["n_paired_plants"] == 6
    assert method_b["n_paired_plants"] == 6
    assert method_a["barrier_delay_hours"]["median"] == 12.0
    assert method_b["barrier_delay_hours"]["median"] == 14.0
