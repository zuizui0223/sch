from __future__ import annotations

from scripts.screen_pedicularis_g_devices import build


def _row(
    plant: int,
    treatment: str,
    method: str,
    *,
    integrity_failure: bool = False,
    cover_entry: bool = False,
    pre_attack: bool = False,
    incomplete_pollination: bool = False,
    swollen: bool = False,
    effect_positive: bool = True,
) -> dict[str, str]:
    exposed = treatment == "EXPOSED"
    excluded = not exposed

    if exposed:
        early_attack = 1
        undamaged = 50
        damaged = 20
    elif effect_positive:
        early_attack = 0
        undamaged = 68
        damaged = 2
    else:
        early_attack = 1
        undamaged = 45
        damaged = 25

    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": f"P{plant:02d}",
        "flower_id": f"P{plant:02d}_{treatment}_{method}",
        "predator_treatment": treatment,
        "exclusion_method": method,
        "sham_device_applied": "1" if exposed else "0",
        "anthesis_time_hours": "0",
        "barrier_application_time_hours": "12",
        "pollination_window_complete_before_barrier": (
            "0" if (excluded and incomplete_pollination) else "1"
        ),
        "ovary_swollen_at_barrier": "1" if (excluded and swollen) else "0",
        "barrier_covers_pollinator_entry": (
            "1" if (excluded and cover_entry) else "0"
        ),
        "pre_barrier_attack_present": (
            "1" if (excluded and pre_attack) else "0"
        ),
        "barrier_integrity_failure_present": (
            "1" if (excluded and integrity_failure) else "0"
        ),
        "realized_exsertion": "0.50",
        "water_depth": "10.0",
        "pollen_grains": "100",
        "pollinator_visits": "10",
        "early_predator_attack_present": str(early_attack),
        "ovule_count": "100",
        "undamaged_seed_count": str(undamaged),
        "damaged_seed_count": str(damaged),
        "mechanical_damage": "0",
    }


def _two_method_rows(
    *,
    method_b_failure: str | None = "integrity",
    method_a_effect_positive: bool = True,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(8):
        rows.append(_row(plant, "EXPOSED", "SHAM_SLEEVE"))
        rows.append(
            _row(
                plant,
                "EXCLUDED",
                "LOWER_FLOWER_SLEEVE_A",
                effect_positive=method_a_effect_positive,
            )
        )
        kwargs = {
            "integrity_failure": method_b_failure == "integrity",
            "cover_entry": method_b_failure == "entry",
            "pre_attack": method_b_failure == "pre_attack",
            "incomplete_pollination": method_b_failure == "pollination",
            "swollen": method_b_failure == "swollen",
        }
        rows.append(
            _row(
                plant,
                "EXCLUDED",
                "LOWER_FLOWER_SLEEVE_B",
                **kwargs,
            )
        )
    return rows


def test_screen_separates_admissible_and_hard_invalid_methods() -> None:
    result = build(_two_method_rows(method_b_failure="integrity"))

    assert result["receipt_schema_version"] == "SCH_PEDICULARIS_G_DEVICE_SCREEN_V1"
    assert result["status"] == "G_DEVICE_SCREEN_HAS_ADMISSIBLE_METHOD"
    assert result["candidate_methods"] == [
        "LOWER_FLOWER_SLEEVE_A",
        "LOWER_FLOWER_SLEEVE_B",
    ]
    assert result["admissible_methods"] == ["LOWER_FLOWER_SLEEVE_A"]
    assert result["rejected_methods"] == ["LOWER_FLOWER_SLEEVE_B"]

    a = result["method_results"]["LOWER_FLOWER_SLEEVE_A"]
    b = result["method_results"]["LOWER_FLOWER_SLEEVE_B"]
    assert a["hard_validity_pass"] is True
    assert b["hard_validity_pass"] is False
    assert b["hard_failure_counts"]["barrier_integrity_failure"] == 8


def test_hard_screen_does_not_turn_exploratory_effect_size_into_pass_fail() -> None:
    result = build(
        _two_method_rows(
            method_b_failure="entry",
            method_a_effect_positive=False,
        )
    )

    a = result["method_results"]["LOWER_FLOWER_SLEEVE_A"]
    assert a["hard_validity_pass"] is True
    assert a["status"] == "G_DEVICE_HARD_VALIDITY_ADMISSIBLE"
    assert (
        a["plant_level_distributions"]["predation_reduction"]["mean"]
        < 0
    )

    assert result["thresholds_applied"] is False
    assert result["effectiveness_pass_fail_applied"] is False
    assert result["confirmatory_receipt_generated"] is False


def test_each_hard_validity_failure_can_reject_a_method() -> None:
    expectations = {
        "integrity": "barrier_integrity_failure",
        "entry": "pollinator_entry_covered",
        "pre_attack": "pre_barrier_attack_present",
        "pollination": "pollination_window_incomplete",
        "swollen": "ovary_swollen_at_barrier",
    }
    for failure, key in expectations.items():
        result = build(_two_method_rows(method_b_failure=failure))
        b = result["method_results"]["LOWER_FLOWER_SLEEVE_B"]
        assert b["hard_validity_pass"] is False
        assert b["hard_failure_counts"][key] == 8


def test_multiple_hard_valid_methods_are_not_automatically_ranked_or_selected() -> None:
    result = build(_two_method_rows(method_b_failure=None))

    assert result["n_admissible_methods"] == 2
    assert result["admissible_methods"] == [
        "LOWER_FLOWER_SLEEVE_A",
        "LOWER_FLOWER_SLEEVE_B",
    ]
    assert "selected_method" not in result
    assert "ranking" not in result


def test_screen_preserves_timing_and_pairing_descriptively() -> None:
    result = build(_two_method_rows(method_b_failure=None))
    a = result["method_results"]["LOWER_FLOWER_SLEEVE_A"]

    assert a["n_paired_plants"] == 8
    assert a["barrier_delay_hours"]["mean"] == 12
    assert a["plant_level_distributions"]["attack_reduction"]["mean"] == 1
    assert a["plant_level_distributions"]["final_seed_gain"]["mean"] > 0
