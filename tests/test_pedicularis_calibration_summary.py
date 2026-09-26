from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.summarize_pedicularis_calibration import summarize


CTX = {
    "population_id": "P_REX_POP_A",
    "season_id": "2027",
    "calibration_dataset_id": "CAL_A",
}


def _c1():
    rows = []
    for arm in ("BASELINE_REPEAT", "Z_SHAM_TAPE", "P_SHAM_HANDLING", "G_SHAM_DEVICE"):
        for plant in ("p1", "p2"):
            flower = f"c1_{arm}_{plant}"
            for round_id, shift in ((0, 0.0), (1, 0.01)):
                rows.append({
                    **CTX,
                    "plant_id": plant,
                    "flower_id": flower,
                    "calibration_arm": arm,
                    "measurement_round": str(round_id),
                    "observer_id": "obs",
                    "hours_since_baseline": str(round_id * 2),
                    "flower_length_mm": str(50 + shift),
                    "realized_exsertion": str(0.4 + shift / 10),
                    "corolla_opening_width_mm": str(8 + shift),
                    "tube_diameter_mm": str(3 + shift),
                    "bract_height_mm": str(30 + shift),
                    "lower_lip_angle_deg": str(25 + shift),
                    "flower_orientation_deg": str(10 + shift),
                    "mechanical_damage": "0",
                })
    return rows


def _c2():
    rows = []
    for arm in ("BASELINE_REPEAT", "Z_SHAM_TAPE", "P_SHAM_HANDLING", "G_SHAM_DEVICE"):
        for plant in ("p1", "p2"):
            flower = f"c2_{arm}_{plant}"
            for timepoint, hours, depth in (("t0", 0, 5.0), ("t1", 2, 4.8)):
                rows.append({
                    **CTX,
                    "plant_id": plant,
                    "flower_id": flower,
                    "calibration_arm": arm,
                    "timepoint_id": timepoint,
                    "hours_since_baseline": str(hours),
                    "water_depth_mm": str(depth),
                    "bract_height_mm": "30",
                    "rainfall_since_last_mm": "0",
                    "external_water_added": "0",
                    "mechanical_damage": "0",
                })
    return rows


def _c3():
    rows = []
    for plant in ("p1", "p2", "p3"):
        for j in range(2):
            rows.append({
                **CTX,
                "plant_id": plant,
                "flower_id": f"c3_{plant}_{j}",
                "observation_block": "am",
                "pollinator_observation_minutes": "30",
                "pollinator_visits": str(2 + j),
                "pollen_grains": str(10 + j),
                "ovule_count": "25",
                "initial_seed_count": "12",
                "undamaged_seed_count": "10",
                "damaged_seed_count": "2",
                "early_predator_attack_present": str(j % 2),
                "mechanical_damage": "0",
            })
    return rows


def _c4():
    rows = []
    for plant in ("p1", "p2", "p3"):
        flower = f"c4_{plant}"
        for event, hours in (
            ("ANTHESIS_START", 0),
            ("POLLINATION_WINDOW_COMPLETE", 12),
            ("FIRST_PREDATOR_ATTACK", 18),
            ("OVARY_SWELLING_START", 36),
        ):
            rows.append({
                **CTX,
                "plant_id": plant,
                "flower_id": flower,
                "event_type": event,
                "event_time_iso": f"2027-07-01T{int(hours)%24:02d}:00:00+08:00",
                "anthesis_time_iso": "2027-07-01T00:00:00+08:00",
                "hours_from_anthesis": str(hours),
                "observer_id": "obs",
            })
    return rows


def test_summary_is_descriptive_only() -> None:
    result = summarize(_c1(), _c2(), _c3(), _c4(), ["QUAL_A"])
    assert result["status"] == "INDEPENDENT_CALIBRATION_SUMMARY_READY"
    assert result["calibration_dataset_id"] == "CAL_A"
    assert "Qz" not in result
    assert "threshold" not in result
    assert "no thresholds are selected automatically" in result["claim_ceiling"]


def test_calibration_id_cannot_equal_qualification_id() -> None:
    with pytest.raises(ValueError, match="overlaps"):
        summarize(_c1(), _c2(), _c3(), _c4(), ["CAL_A"])


def test_identity_mismatch_fails() -> None:
    c4 = _c4()
    c4[0] = {**c4[0], "season_id": "2028"}
    with pytest.raises(ValueError, match="one population"):
        summarize(_c1(), _c2(), _c3(), c4, ["QUAL_A"])


def test_timing_cannot_precede_anthesis() -> None:
    c4 = _c4()
    for row in c4:
        if row["event_type"] == "FIRST_PREDATOR_ATTACK":
            row["hours_from_anthesis"] = "-1"
            break
    with pytest.raises(ValueError, match="negative delay"):
        summarize(_c1(), _c2(), _c3(), c4, ["QUAL_A"])


def test_c3_seed_counts_cannot_exceed_ovules() -> None:
    c3 = _c3()
    c3[0]["undamaged_seed_count"] = "24"
    c3[0]["damaged_seed_count"] = "5"
    with pytest.raises(ValueError, match="cannot exceed ovules"):
        summarize(_c1(), _c2(), c3, _c4(), ["QUAL_A"])
