from __future__ import annotations

import csv
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

    p1s = result["pilot_summaries"]["P1"]["plant_level_distributions"]
    assert p1s["pollen_grains_delta"]["mean"] == pytest.approx(14.0)
    assert p1s["initial_seed_set_delta"]["mean"] > 0

    gs = result["pilot_summaries"]["G"]
    assert gs["barrier_delay_hours"]["median"] == pytest.approx(12.0)
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
