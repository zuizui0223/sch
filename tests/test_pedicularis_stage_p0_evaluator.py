from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_stage_p0 import (
    REQUIRED_FIELDS,
    evaluate,
    evaluate_locked,
)
from scripts.build_pedicularis_p0_randomized_assignment import build as allocate_p0
from scripts.pedicularis_config_freeze import required_gate_paths


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_EXSERTION_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "SCH_PEDICULARIS_STAGE_P0_DATA_CONTRACT_V1.md"


def _freeze(lane: str) -> dict:
    return {
        "schema": "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "lane": lane,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-27T00:00:00Z",
        "basis_document": "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY",
        "threshold_basis": {
            path: "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY"
            for path in required_gate_paths(lane)
        },
    }


def _config() -> dict:
    return {
        "prospective_freeze": _freeze("P0"),
        "bootstrap_reps": 300,
        "random_seed": 23,
        "stage_p0": {
            "min_z_levels": 5,
            "min_flowers_per_level": 15,
            "min_plants": 15,
            "min_adjacent_exsertion_gap": 0.10,
            "max_opening_width_relative_change": 0.03,
            "max_tube_diameter_relative_change": 0.03,
            "max_bract_height_relative_change": 0.03,
            "max_lower_lip_angle_change_deg": 2.0,
            "max_water_depth_change": 0.15,
            "max_flower_orientation_change_deg": 2.0,
            "max_mechanical_damage_rate": 0.05,
        },
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(20):
        plant_shift = (plant % 4) * 0.001
        for rank in range(5):
            exsertion = 0.20 + 0.15 * rank + plant_shift
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P{plant:02d}_Z{rank}",
                    "assigned_z_level": f"Z{rank}",
                    "assigned_z_rank": str(rank),
                    "sham_control": "1" if rank == 4 else "0",
                    "realized_exsertion": f"{exsertion:.4f}",
                    "corolla_opening_width": f"{8.0 + plant_shift:.4f}",
                    "lower_lip_angle_deg": f"{25.0 + plant_shift:.4f}",
                    "tube_diameter": f"{4.0 + plant_shift:.4f}",
                    "bract_height": f"{20.0 + plant_shift:.4f}",
                    "water_depth": f"{5.0 + plant_shift:.4f}",
                    "flower_orientation_deg": f"{15.0 + plant_shift:.4f}",
                    "mechanical_damage": "0",
                    "pollinator_visits": f"{2.0 + rank * 0.5:.4f}",
                    "pollen_grains": f"{8.0 + rank * 2.0:.4f}",
                }
            )
    return rows


def _locked_rows_and_receipt() -> tuple[list[dict[str, str]], dict]:
    manifest = [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(20)
        for flower in range(5)
    ]
    levels = [
        {
            "assigned_z_level": f"Z{rank}",
            "assigned_z_rank": str(rank),
            "sham_control": "1" if rank == 4 else "0",
        }
        for rank in range(5)
    ]
    allocations, receipt = allocate_p0(
        manifest,
        levels,
        allocation_seed="P0-LOCKED-TEST-SEED",
    )

    rows = []
    for alloc in allocations:
        rank = int(alloc["assigned_z_rank"])
        plant = int(alloc["plant_id"][1:])
        plant_shift = (plant % 4) * 0.001
        exsertion = 0.20 + 0.15 * rank + plant_shift
        rows.append(
            {
                "population_id": alloc["population_id"],
                "season_id": alloc["season_id"],
                "plant_id": alloc["plant_id"],
                "flower_id": alloc["flower_id"],
                "assigned_z_level": alloc["assigned_z_level"],
                "assigned_z_rank": alloc["assigned_z_rank"],
                "sham_control": alloc["sham_control"],
                "realized_exsertion": f"{exsertion:.4f}",
                "corolla_opening_width": f"{8.0 + plant_shift:.4f}",
                "lower_lip_angle_deg": f"{25.0 + plant_shift:.4f}",
                "tube_diameter": f"{4.0 + plant_shift:.4f}",
                "bract_height": f"{20.0 + plant_shift:.4f}",
                "water_depth": f"{5.0 + plant_shift:.4f}",
                "flower_orientation_deg": f"{15.0 + plant_shift:.4f}",
                "mechanical_damage": "0",
                "pollinator_visits": f"{2.0 + rank * 0.5:.4f}",
                "pollen_grains": f"{8.0 + rank * 2.0:.4f}",
            }
        )
    return rows, receipt


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["stage_p0"]["min_adjacent_exsertion_gap"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_valid_ordered_exsertion_manipulation_passes_without_requiring_equal_pollination() -> None:
    result = evaluate(_rows(), _config())
    assert result["status"] == "PEDICULARIS_Z_MANIPULATION_VALIDATED"
    assert all(result["gates"].values())
    assert result["realized_exsertion"]["minimum_adjacent_gap_bootstrap_95_ci"][0] > 0.10
    visits = result["descriptive_functional_checks"]["pollinator_visits_mean_by_rank"]
    assert float(visits["4"]) > float(visits["0"])
    assert result["claim_ceiling"].startswith("manipulation_validity_only")


def test_water_defence_contamination_fails_p0() -> None:
    rows = _rows()
    for row in rows:
        if row["assigned_z_rank"] == "0":
            row["water_depth"] = "3.5"
    result = evaluate(rows, _config())
    assert result["status"] == "PEDICULARIS_Z_MANIPULATION_NOT_VALIDATED"
    assert result["gates"]["water_depth_stable"] is False


def test_contract_separates_manipulation_validity_from_functional_inference() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "PEDICULARIS_Z_MANIPULATION_VALIDATED" in text
    assert "are recorded and summarized by z rank but are **not required to remain equal across z levels**" in text
    assert "does not establish" in text
    assert "causal compromise" in text


def test_locked_p0_evaluator_accepts_exact_randomized_assignment() -> None:
    rows, receipt = _locked_rows_and_receipt()
    result = evaluate_locked(rows, _config(), receipt)

    assert result["status"] == "PEDICULARIS_Z_MANIPULATION_VALIDATED"
    assert result["field_allocation_verification"]["identity_z_assignment_match"] is True
    assert result["field_allocation_verification"]["receipt_schema"] == (
        "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1"
    )


def test_locked_p0_evaluator_rejects_z_assignment_drift() -> None:
    rows, receipt = _locked_rows_and_receipt()
    rows[0]["assigned_z_level"] = rows[1]["assigned_z_level"]
    rows[0]["assigned_z_rank"] = rows[1]["assigned_z_rank"]
    rows[0]["sham_control"] = rows[1]["sham_control"]

    import pytest

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        evaluate_locked(rows, _config(), receipt)


def test_locked_p0_evaluator_rejects_flower_substitution() -> None:
    rows, receipt = _locked_rows_and_receipt()
    rows[0]["flower_id"] = "SUBSTITUTED_FLOWER"

    import pytest

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        evaluate_locked(rows, _config(), receipt)
