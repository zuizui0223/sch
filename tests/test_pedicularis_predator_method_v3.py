from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_predator_method_v3 import REQUIRED_FIELDS, evaluate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V3.csv"
CONFIG = ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V3.json"


def _config() -> dict:
    return {
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


def _rows(*, early_barrier: bool = False, cover_pollinator_entry: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(16):
        for treatment in ("EXPOSED", "EXCLUDED"):
            exposed = treatment == "EXPOSED"
            delay = 2.0 if (early_barrier and not exposed) else 12.0
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "flower_id": f"P{plant:02d}_{treatment}",
                    "predator_treatment": treatment,
                    "exclusion_method": "POST_POLLINATION_LOWER_FLOWER_SLEEVE" if not exposed else "SHAM_SLEEVE",
                    "sham_device_applied": "1" if exposed else "0",
                    "anthesis_time_hours": "0",
                    "barrier_application_time_hours": str(delay),
                    "pollination_window_complete_before_barrier": "1",
                    "ovary_swollen_at_barrier": "0",
                    "barrier_covers_pollinator_entry": "1" if (cover_pollinator_entry and not exposed) else "0",
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


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert cfg["method_gate"]["min_hours_after_anthesis_before_barrier"] == "REQUIRED_BEFORE_USE"
    assert cfg["predator_weight"]["min_predation_fraction_reduction"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in cfg["status"]


def test_timed_post_pollination_method_passes_when_selective() -> None:
    result = evaluate(_rows(), _config())
    assert result["receipt_schema_version"] == "SCH_PEDICULARIS_PREDATOR_METHOD_V3"
    assert result["status"] == "PEDICULARIS_PREDATOR_METHOD_VALIDATED"
    assert all(result["gates"].values())
    assert result["method_summary"]["exclusion_method"] == "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
    assert result["predator_weight_receipt"]["status"] == "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED"


def test_barrier_applied_before_registered_pollination_window_fails() -> None:
    result = evaluate(_rows(early_barrier=True), _config())
    assert result["gates"]["method_barrier_after_minimum_pollination_window"] is False
    assert result["status"] == "PEDICULARIS_PREDATOR_METHOD_NOT_VALIDATED"


def test_barrier_covering_pollinator_entry_fails() -> None:
    result = evaluate(_rows(cover_pollinator_entry=True), _config())
    assert result["gates"]["method_pollinator_entry_not_covered"] is False
    assert result["status"] == "PEDICULARIS_PREDATOR_METHOD_NOT_VALIDATED"
