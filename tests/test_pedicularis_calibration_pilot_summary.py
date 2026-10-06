from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.summarize_pedicularis_calibration_pilots import build


def _write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _p0_rows(season: str = "S1") -> list[dict[str, str]]:
    rows = []
    for plant in range(4):
        for rank in range(5):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P0_{plant:02d}_{rank}",
                    "assigned_z_level": f"Z{rank}",
                    "assigned_z_rank": str(rank),
                    "sham_control": "1" if rank == 4 else "0",
                    "realized_exsertion": str(0.20 + 0.15 * rank + plant * 0.001),
                    "corolla_opening_width": str(8.0 + plant * 0.01),
                    "lower_lip_angle_deg": str(25.0 + plant * 0.02),
                    "tube_diameter": str(4.0 + plant * 0.005),
                    "bract_height": str(20.0 + plant * 0.01),
                    "water_depth": str(5.0 + plant * 0.01),
                    "flower_orientation_deg": str(15.0 + plant * 0.02),
                    "mechanical_damage": "0",
                    "pollinator_visits": str(2 + rank),
                    "pollen_grains": str(10 + 2 * rank),
                }
            )
    return rows


def _p1_rows(season: str = "S1") -> list[dict[str, str]]:
    rows = []
    for plant in range(4):
        for treatment in ("NATURAL", "SUPPLEMENTED"):
            sup = treatment == "SUPPLEMENTED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": f"Q{plant:02d}",
                    "flower_id": f"P1_{plant:02d}_{treatment}",
                    "pollination_treatment": treatment,
                    "pollination_handling_role": (
                        "DONOR_MIXED_CROSS_POLLEN"
                        if treatment == "SUPPLEMENTED"
                        else "SHAM_STIGMA_CONTACT"
                    ),
                    "realized_exsertion": "0.55",
                    "water_depth": "5.0",
                    "bract_height": "20.0",
                    "corolla_opening_width": "8.0",
                    "mechanical_damage": "0",
                    "pollen_grains_post_treatment": "24" if sup else "10",
                    "early_predator_attack_present": "0",
                    "ovule_count": "20",
                    "undamaged_seed_count": "10" if sup else "6",
                    "damaged_seed_count": "2",
                }
            )
    return rows


def _g_rows(season: str = "S1") -> list[dict[str, str]]:
    rows = []
    for plant in range(4):
        for treatment in ("EXPOSED", "EXCLUDED"):
            exposed = treatment == "EXPOSED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": f"G{plant:02d}",
                    "flower_id": f"G_{plant:02d}_{treatment}",
                    "predator_treatment": treatment,
                    "exclusion_method": (
                        "SHAM_SLEEVE"
                        if exposed
                        else "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
                    ),
                    "sham_device_applied": "1" if exposed else "0",
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


P0_FIELDS = list(_p0_rows()[0])
P1_FIELDS = list(_p1_rows()[0])
G_FIELDS = list(_g_rows()[0])


def _g_timing_config(season: str = "S1") -> dict:
    return {
        "schema": "SCH_PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_V1",
        "status": "PEDICULARIS_G_EVENT_TIME_PILOT_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": season,
        "pollination_completion_definition": "unit-test pollen criterion",
        "pollination_completion_measurement": "destructive stigma pollen count",
        "attack_event_definition": "visible egg or puncture",
        "ovary_swelling_definition": "unit-test visible swelling",
        "pollination_sampling_elapsed_hours": [4, 8, 12],
        "attack_swelling_sampling_elapsed_hours": [4, 8, 12],
        "max_sampling_deviation_hours": 0.5,
        "sampling_schedule_basis_note": "fixed unit-test schedule",
        "frozen_before_event_time_data": True,
        "frozen_at_utc": "2026-10-05T00:00:00Z",
    }


def _g_timing_rows(season: str = "S1") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(4):
        for hours, pollen, complete in (
            (4, 10 + plant, 0),
            (8, 30 + plant, 1 if plant < 2 else 0),
            (12, 50 + plant, 1),
        ):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": f"T{plant:02d}",
                    "flower_id": f"T{plant:02d}_P{hours}",
                    "flower_role": "POLLINATION_SENTINEL",
                    "anthesis_time_hours": "0",
                    "scheduled_elapsed_hours": str(hours),
                    "observation_time_hours": str(hours),
                    "pollen_grains": str(pollen),
                    "pollination_complete": str(complete),
                    "attack_present": "",
                    "ovary_swollen": "",
                }
            )
        for hours, attack, swollen in (
            (4, 0, 0),
            (8, 0, 0),
            (12, 1 if plant < 2 else 0, 1 if plant >= 2 else 0),
        ):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": f"T{plant:02d}",
                    "flower_id": f"T{plant:02d}_N",
                    "flower_role": "ATTACK_SWELL_SENTINEL",
                    "anthesis_time_hours": "0",
                    "scheduled_elapsed_hours": str(hours),
                    "observation_time_hours": str(hours),
                    "pollen_grains": "",
                    "pollination_complete": "",
                    "attack_present": str(attack),
                    "ovary_swollen": str(swollen),
                }
            )
    return rows


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_all_three_calibration_lanes_are_summarized_without_threshold_decisions(tmp_path: Path) -> None:
    p0 = _write(tmp_path / "p0.csv", P0_FIELDS, _p0_rows())
    p1 = _write(tmp_path / "p1.csv", P1_FIELDS, _p1_rows())
    g = _write(tmp_path / "g.csv", G_FIELDS, _g_rows())

    result = build(p0_path=p0, p1_path=p1, g_path=g)

    assert result["status"] == "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"
    assert result["thresholds_selected"] is False
    assert result["confirmatory_receipt_generated"] is False
    assert result["available_pilot_lanes"] == ["G", "P0", "P1"]

    p0s = result["pilot_summaries"]["P0"]
    assert p0s["n_assigned_z_levels"] == 5
    assert p0s["observed_minimum_adjacent_gap"] == pytest.approx(0.15)
    assert p0s["n_complete_profile_plants"] == 4
    p0_gate = p0s["plant_level_gate_metric_distributions"]
    assert p0_gate["minimum_adjacent_exsertion_gap"]["mean"] == pytest.approx(0.15)
    assert p0_gate["minimum_adjacent_exsertion_gap"]["sd"] is not None
    assert p0_gate["opening_width_relative_change"]["mean"] >= 0
    assert p0_gate["maximum_mechanical_damage_rate"]["max"] == 0

    p1s = result["pilot_summaries"]["P1"]["plant_level_distributions"]
    assert p1s["pollen_grains_delta"]["mean"] == pytest.approx(14.0)
    assert p1s["initial_seed_set_delta"]["mean"] > 0

    gs = result["pilot_summaries"]["G"]
    assert gs["barrier_delay_hours"]["median"] == pytest.approx(12.0)
    assert gs["excluded_pre_barrier_attack_free_rate"] == pytest.approx(1.0)
    assert gs["excluded_barrier_integrity_success_rate"] == pytest.approx(1.0)
    assert gs["plant_level_distributions"]["attack_reduction"]["mean"] == pytest.approx(1.0)
    assert gs["plant_level_distributions"]["predation_reduction"]["mean"] > 0
    assert gs["plant_level_distributions"]["final_seed_gain"]["mean"] > 0


def test_partial_calibration_package_is_allowed(tmp_path: Path) -> None:
    p0 = _write(tmp_path / "p0.csv", P0_FIELDS, _p0_rows())
    result = build(p0_path=p0)
    assert result["available_pilot_lanes"] == ["P0"]
    assert result["calibration_modules_supported"]["CAL_B"] == []


def test_calibration_inputs_must_share_population_and_season(tmp_path: Path) -> None:
    p0 = _write(tmp_path / "p0.csv", P0_FIELDS, _p0_rows("S1"))
    p1 = _write(tmp_path / "p1.csv", P1_FIELDS, _p1_rows("S2"))
    with pytest.raises(ValueError, match="same population and season"):
        build(p0_path=p0, p1_path=p1)


def test_calibration_summary_does_not_expose_gate_decisions(tmp_path: Path) -> None:
    p1 = _write(tmp_path / "p1.csv", P1_FIELDS, _p1_rows())
    g = _write(tmp_path / "g.csv", G_FIELDS, _g_rows())
    result = build(p1_path=p1, g_path=g)
    payload = str(result)
    assert "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED" not in payload
    assert "PEDICULARIS_PREDATOR_METHOD_VALIDATED" not in payload
    assert "'gates':" not in payload


def test_g_event_time_summary_integrates_as_separate_cal_b_lane(tmp_path: Path) -> None:
    p1 = _write(tmp_path / "p1.csv", P1_FIELDS, _p1_rows())
    g = _write(tmp_path / "g.csv", G_FIELDS, _g_rows())
    timing_rows = _g_timing_rows()
    timing = _write(
        tmp_path / "g_timing.csv",
        list(timing_rows[0]),
        timing_rows,
    )
    config = _write_json(
        tmp_path / "g_timing_config.json",
        _g_timing_config(),
    )

    result = build(
        p1_path=p1,
        g_path=g,
        g_timing_config_path=config,
        g_timing_path=timing,
    )

    assert result["available_pilot_lanes"] == ["G", "G_TIMING", "P1"]
    assert result["calibration_modules_supported"]["CAL_B"] == [
        "G",
        "G_TIMING",
        "P1",
    ]
    gt = result["pilot_summaries"]["G_TIMING"]
    assert gt["status"] == "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED"
    assert gt["timing_window_selected"] is False
    assert gt["pollination_complete_observation_hours"] is not None
    assert gt["first_constraint_positive_observation_hours"] is not None


def test_g_event_time_config_and_data_are_jointly_required(tmp_path: Path) -> None:
    timing_rows = _g_timing_rows()
    timing = _write(
        tmp_path / "g_timing.csv",
        list(timing_rows[0]),
        timing_rows,
    )
    with pytest.raises(ValueError, match="both config and data"):
        build(g_timing_path=timing)


def test_g_event_time_must_share_calibration_context(tmp_path: Path) -> None:
    p1 = _write(tmp_path / "p1.csv", P1_FIELDS, _p1_rows("S1"))
    timing_rows = _g_timing_rows("S2")
    timing = _write(
        tmp_path / "g_timing.csv",
        list(timing_rows[0]),
        timing_rows,
    )
    config = _write_json(
        tmp_path / "g_timing_config.json",
        _g_timing_config("S2"),
    )
    with pytest.raises(ValueError, match="same population and season"):
        build(
            p1_path=p1,
            g_timing_config_path=config,
            g_timing_path=timing,
        )
