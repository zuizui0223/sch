from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_antagonist_weight import REQUIRED_FIELDS, evaluate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_ANTAGONIST_WEIGHT_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_ANTAGONIST_WEIGHT_CONFIG_TEMPLATE_V1.json"


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 37,
        "antagonist_weight": {
            "min_paired_plants": 15,
            "min_flowers_per_treatment": 15,
            "min_water_depth_delta": 3.0,
            "min_early_attack_delta": 0.5,
            "min_predation_fraction_delta": 0.20,
            "min_final_seed_set_delta": 0.10,
            "max_pollinator_visit_difference": 0.20,
            "max_initial_seed_set_difference": 0.05,
            "max_z_relative_change": 0.03,
            "max_bract_height_relative_change": 0.03,
            "max_opening_width_relative_change": 0.03,
            "max_mechanical_damage_rate": 0.05,
        },
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(20):
        shift = (plant % 4) * 0.001
        for treatment in ("INTACT", "DRAINED"):
            drained = treatment == "DRAINED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P{plant:02d}_{treatment}",
                    "defence_treatment": treatment,
                    "realized_exsertion": f"{0.55 + shift:.4f}",
                    "water_depth": "1.0" if drained else "5.0",
                    "bract_height": f"{20.0 + shift:.4f}",
                    "corolla_opening_width": f"{8.0 + shift:.4f}",
                    "mechanical_damage": "0",
                    "pollinator_visits": "3.0",
                    "early_predator_attack_present": "1" if drained else "0",
                    "ovule_count": "20",
                    "undamaged_seed_count": "7" if drained else "11",
                    "damaged_seed_count": "5" if drained else "1",
                }
            )
    return rows


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["antagonist_weight"]["min_predation_fraction_delta"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_selective_water_defence_manipulation_validates_antagonist_weight() -> None:
    result = evaluate(_rows(), _config())
    assert result["status"] == "PEDICULARIS_ANTAGONIST_WEIGHT_VALIDATED"
    assert all(result["gates"].values())
    assert result["bootstrap_95_ci"]["predation_fraction_delta_drained_minus_intact"][0] > 0.20
    assert result["bootstrap_95_ci"]["final_seed_set_delta_intact_minus_drained"][0] > 0.10
    assert result["observed_estimands"]["pollinator_visits_abs_difference"] == 0.0


def test_G_manipulation_that_changes_pollinator_visits_is_rejected() -> None:
    rows = _rows()
    for row in rows:
        if row["defence_treatment"] == "DRAINED":
            row["pollinator_visits"] = "5.0"
    result = evaluate(rows, _config())
    assert result["status"] == "PEDICULARIS_ANTAGONIST_WEIGHT_NOT_VALIDATED"
    assert result["gates"]["pollinator_visitation_stable"] is False


def test_no_predation_relief_means_G_manipulation_is_uninformative() -> None:
    rows = _rows()
    for row in rows:
        if row["defence_treatment"] == "DRAINED":
            row["undamaged_seed_count"] = "11"
            row["damaged_seed_count"] = "1"
            row["early_predator_attack_present"] = "0"
    result = evaluate(rows, _config())
    assert result["status"] == "PEDICULARIS_ANTAGONIST_WEIGHT_NOT_VALIDATED"
    assert result["gates"]["seed_predation_increases_when_drained"] is False
    assert result["gates"]["early_antagonist_attack_increases_when_drained"] is False
