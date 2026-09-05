from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_pollination_weight import REQUIRED_FIELDS, evaluate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "SCH_PEDICULARIS_POLLINATION_WEIGHT_AND_4_STATE_MAPPING_V1.md"


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 31,
        "pollination_weight": {
            "min_paired_plants": 15,
            "min_flowers_per_treatment": 15,
            "min_pollen_grain_delta": 5.0,
            "min_initial_seed_set_delta": 0.10,
            "max_early_predator_attack_difference": 0.05,
            "max_z_relative_change": 0.03,
            "max_bract_height_relative_change": 0.03,
            "max_opening_width_relative_change": 0.03,
            "max_water_depth_change": 0.15,
            "max_mechanical_damage_rate": 0.05,
        },
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(20):
        shift = (plant % 4) * 0.001
        attack = "1" if plant % 5 == 0 else "0"
        for treatment in ("NATURAL", "SUPPLEMENTED"):
            supplemented = treatment == "SUPPLEMENTED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P{plant:02d}_{treatment}",
                    "pollination_treatment": treatment,
                    "realized_exsertion": f"{0.55 + shift:.4f}",
                    "water_depth": f"{5.0 + shift:.4f}",
                    "bract_height": f"{20.0 + shift:.4f}",
                    "corolla_opening_width": f"{8.0 + shift:.4f}",
                    "mechanical_damage": "0",
                    "pollen_grains_post_treatment": "22" if supplemented else "10",
                    "early_predator_attack_present": attack,
                    "ovule_count": "20",
                    "undamaged_seed_count": "10" if supplemented else "6",
                    "damaged_seed_count": "2",
                }
            )
    return rows


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["pollination_weight"]["min_initial_seed_set_delta"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_effective_selective_supplementation_validates_pollination_weight() -> None:
    result = evaluate(_rows(), _config())
    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"
    assert all(result["gates"].values())
    assert result["bootstrap_95_ci"]["initial_seed_set_delta"][0] > 0.10
    assert result["bootstrap_95_ci"]["pollen_grains_delta"][0] > 5.0
    assert result["observed_estimands"]["early_predator_attack_abs_difference"] == 0.0


def test_supplementation_that_changes_early_predator_attack_is_rejected() -> None:
    rows = _rows()
    for row in rows:
        if row["pollination_treatment"] == "NATURAL":
            row["early_predator_attack_present"] = "0"
        else:
            row["early_predator_attack_present"] = "1"
    result = evaluate(rows, _config())
    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"
    assert result["gates"]["early_predator_attack_stable"] is False


def test_no_pollen_limitation_means_the_P_weight_manipulation_is_uninformative() -> None:
    rows = _rows()
    for row in rows:
        if row["pollination_treatment"] == "SUPPLEMENTED":
            row["undamaged_seed_count"] = "6"
    result = evaluate(rows, _config())
    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"
    assert result["gates"]["supplementation_changes_pollination_weight"] is False


def test_contract_maps_open_supplementation_without_pollinator_exclusion() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "P1 = open natural pollination" in text
    assert "P0 = open + standardized saturating supplemental cross-pollen" in text
    assert "seed-predator natural-history window overlaps open flowering" in text
    assert "later predation fraction is not the only selectivity check" in text
