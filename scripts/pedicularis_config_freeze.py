from __future__ import annotations

from datetime import datetime
import math
from typing import Any


FREEZE_SCHEMA = "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1"
FREEZE_STATUS = "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

LANE_SPECS: dict[str, dict[str, tuple[str, ...]]] = {
    "P0": {
        "stage_p0": (
            "min_z_levels",
            "min_flowers_per_level",
            "min_plants",
            "min_adjacent_exsertion_gap",
            "max_opening_width_relative_change",
            "max_tube_diameter_relative_change",
            "max_bract_height_relative_change",
            "max_lower_lip_angle_change_deg",
            "max_water_depth_change",
            "max_flower_orientation_change_deg",
            "max_mechanical_damage_rate",
        ),
    },
    "P1": {
        "pollination_weight": (
            "min_plant_units_per_treatment",
            "min_flowers_per_treatment",
            "min_pollen_grain_delta",
            "min_initial_seed_set_delta",
            "max_early_predator_attack_difference",
            "max_z_relative_change",
            "max_bract_height_relative_change",
            "max_opening_width_relative_change",
            "max_water_depth_change",
            "max_mechanical_damage_rate",
        ),
    },
    "G": {
        "method_gate": (
            "min_paired_plants",
            "min_flowers_per_treatment",
            "min_hours_after_anthesis_before_barrier",
            "max_hours_after_anthesis_before_barrier",
            "require_pollination_window_complete",
            "require_ovary_not_swollen",
            "require_barrier_not_cover_pollinator_entry",
            "require_sham_on_exposed",
        ),
        "predator_weight": (
            "min_paired_plants",
            "min_flowers_per_treatment",
            "min_early_attack_reduction",
            "min_predation_fraction_reduction",
            "min_final_seed_set_gain",
            "max_initial_seed_set_difference",
            "max_pollen_grain_relative_change",
            "max_pollinator_visit_relative_change",
            "max_z_relative_change",
            "max_water_depth_change",
            "max_damage_rate_difference",
        ),
    },
}


def required_gate_paths(lane: str) -> tuple[str, ...]:
    if lane not in LANE_SPECS:
        raise ValueError(f"unknown Pedicularis execution lane: {lane}")
    return tuple(
        f"{section}.{field}"
        for section, fields in LANE_SPECS[lane].items()
        for field in fields
    )


def _is_concrete_gate_value(value: Any) -> bool:
    if value == PLACEHOLDER or value is None:
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return False


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def inspect_prospective_freeze(config: dict, lane: str) -> dict:
    if lane not in LANE_SPECS:
        raise ValueError(f"unknown Pedicularis execution lane: {lane}")

    freeze = config.get("prospective_freeze")
    issues: list[str] = []
    if not isinstance(freeze, dict):
        freeze = {}
        issues.append("prospective_freeze_missing")

    if freeze.get("schema") != FREEZE_SCHEMA:
        issues.append("freeze_schema_invalid")
    if freeze.get("status") != FREEZE_STATUS:
        issues.append("freeze_status_not_positive")
    if freeze.get("lane") != lane:
        issues.append("freeze_lane_mismatch")

    population_id = freeze.get("population_id")
    season_id = freeze.get("season_id")
    if not isinstance(population_id, str) or not population_id.strip() or population_id == PLACEHOLDER:
        issues.append("population_id_not_frozen")
    if not isinstance(season_id, str) or not season_id.strip() or season_id == PLACEHOLDER:
        issues.append("season_id_not_frozen")
    if freeze.get("frozen_before_confirmatory_data") is not True:
        issues.append("not_declared_frozen_before_confirmatory_data")
    if not _valid_timestamp(freeze.get("frozen_at_utc")):
        issues.append("freeze_timestamp_invalid")

    basis_document = freeze.get("basis_document")
    if (
        not isinstance(basis_document, str)
        or not basis_document.strip()
        or basis_document == PLACEHOLDER
    ):
        issues.append("basis_document_missing")

    basis = freeze.get("threshold_basis")
    if not isinstance(basis, dict):
        basis = {}
        issues.append("threshold_basis_missing")

    for section, fields in LANE_SPECS[lane].items():
        block = config.get(section)
        if not isinstance(block, dict):
            issues.append(f"section_missing:{section}")
            continue
        for field in fields:
            path = f"{section}.{field}"
            if field not in block:
                issues.append(f"gate_missing:{path}")
            elif not _is_concrete_gate_value(block[field]):
                issues.append(f"gate_not_frozen:{path}")
            note = basis.get(path)
            if not isinstance(note, str) or not note.strip() or note == PLACEHOLDER:
                issues.append(f"basis_missing:{path}")

    return {
        "schema": FREEZE_SCHEMA,
        "status": FREEZE_STATUS if not issues else "PEDICULARIS_THRESHOLDS_NOT_FROZEN",
        "lane": lane,
        "population_id": population_id if isinstance(population_id, str) else None,
        "season_id": season_id if isinstance(season_id, str) else None,
        "frozen_at_utc": freeze.get("frozen_at_utc"),
        "basis_document": basis_document if isinstance(basis_document, str) else None,
        "n_required_gate_fields": len(required_gate_paths(lane)),
        "issues": issues,
    }


def validate_prospective_freeze(config: dict, lane: str) -> dict:
    receipt = inspect_prospective_freeze(config, lane)
    if receipt["issues"]:
        raise ValueError(
            "Pedicularis config is not prospectively frozen for "
            f"{lane}: " + "; ".join(receipt["issues"])
        )
    return receipt


def validate_freeze_context(
    freeze_receipt: dict,
    population_id: str,
    season_id: str,
) -> None:
    if (
        freeze_receipt.get("population_id") != population_id
        or freeze_receipt.get("season_id") != season_id
    ):
        raise ValueError(
            "Pedicularis data population/season do not match the prospective "
            "threshold-freeze context"
        )
