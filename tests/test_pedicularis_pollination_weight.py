from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.evaluate_pedicularis_pollination_weight import (
    PAIRED,
    REQUIRED_FIELDS,
    WHOLE,
    evaluate,
)
from scripts.freeze_pedicularis_p1_design import SCHEMA, STATUS
from scripts.pedicularis_config_freeze import required_gate_paths


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_POLLINATION_WEIGHT_TEMPLATE_V1.csv"
)
CONFIG_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json"
)
CONTRACT = (
    ROOT
    / "docs"
    / "SCH_PEDICULARIS_POLLINATION_WEIGHT_AND_4_STATE_MAPPING_V1.md"
)


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


def _design(design_unit: str) -> dict:
    paired = design_unit == PAIRED
    return {
        "receipt_schema_version": SCHEMA,
        "status": STATUS,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "design_unit": design_unit,
        "treatment_assignment": (
            "PAIRED_WITHIN_PLANT"
            if paired
            else "RANDOMIZED_BETWEEN_PLANTS"
        ),
        "resource_reallocation_strategy": (
            "paired flowers retain individual blocking while acknowledging "
            "within-plant resource reallocation"
            if paired
            else "whole-plant supplementation treats the whole flowering plant "
            "to reduce within-plant resource-reallocation bias"
        ),
        "donor_protocol": (
            "donor-mixed outcross pollen from non-focal plants"
        ),
        "randomization_or_matching_protocol": (
            "paired within-plant assignment of natural and supplemented flowers"
            if paired
            else "randomized between-plant assignment to natural or supplemented arms"
        ),
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-27T00:00:00Z",
        "basis_document": "UNIT_TEST_P1_DESIGN_BASIS",
    }


def _config(
    design_unit: str = PAIRED,
) -> dict:
    return {
        "prospective_freeze": _freeze("P1"),
        "pollination_design": _design(design_unit),
        "bootstrap_reps": 300,
        "random_seed": 31,
        "pollination_weight": {
            "min_plant_units_per_treatment": 15,
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


def _paired_rows() -> list[dict[str, str]]:
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
                    "pollen_grains_post_treatment": (
                        "22" if supplemented else "10"
                    ),
                    "early_predator_attack_present": attack,
                    "ovule_count": "20",
                    "undamaged_seed_count": (
                        "10" if supplemented else "6"
                    ),
                    "damaged_seed_count": "2",
                }
            )
    return rows


def _whole_rows() -> list[dict[str, str]]:
    rows = []
    for treatment, prefix in (
        ("NATURAL", "N"),
        ("SUPPLEMENTED", "S"),
    ):
        supplemented = treatment == "SUPPLEMENTED"
        for plant in range(20):
            shift = (plant % 4) * 0.001
            attack = "1" if plant % 5 == 0 else "0"
            plant_id = f"{prefix}{plant:02d}"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": plant_id,
                    "flower_id": f"{plant_id}_F1",
                    "pollination_treatment": treatment,
                    "realized_exsertion": f"{0.55 + shift:.4f}",
                    "water_depth": f"{5.0 + shift:.4f}",
                    "bract_height": f"{20.0 + shift:.4f}",
                    "corolla_opening_width": f"{8.0 + shift:.4f}",
                    "mechanical_damage": "0",
                    "pollen_grains_post_treatment": (
                        "22" if supplemented else "10"
                    ),
                    "early_predator_attack_present": attack,
                    "ovule_count": "20",
                    "undamaged_seed_count": (
                        "10" if supplemented else "6"
                    ),
                    "damaged_seed_count": "2",
                }
            )
    return rows


def test_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS

    config = json.loads(
        CONFIG_TEMPLATE.read_text(encoding="utf-8")
    )
    assert (
        config["pollination_weight"][
            "min_plant_units_per_treatment"
        ]
        == "REQUIRED_BEFORE_USE"
    )
    assert config["pollination_design"]["status"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_effective_selective_paired_supplementation_validates() -> None:
    result = evaluate(_paired_rows(), _config(PAIRED))

    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"
    assert result["design_unit"] == PAIRED
    assert result["estimand_family"] == (
        "PAIRED_PLANT_LEVEL_TREATMENT_CONTRAST"
    )
    assert result["n_paired_plants"] == 20
    assert result["plant_units_by_treatment"] == {
        "NATURAL": 20,
        "SUPPLEMENTED": 20,
    }
    assert all(result["gates"].values())
    assert (
        result["bootstrap_95_ci"][
            "initial_seed_set_delta"
        ][0]
        > 0.10
    )
    assert (
        result["bootstrap_95_ci"][
            "pollen_grains_delta"
        ][0]
        > 5.0
    )
    assert (
        result["observed_estimands"][
            "early_predator_attack_abs_difference"
        ]
        == 0.0
    )


def test_effective_selective_whole_plant_supplementation_validates() -> None:
    result = evaluate(_whole_rows(), _config(WHOLE))

    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"
    assert result["design_unit"] == WHOLE
    assert result["estimand_family"] == (
        "INDEPENDENT_ARM_PLANT_LEVEL_TREATMENT_CONTRAST"
    )
    assert result["n_paired_plants"] is None
    assert result["plant_units_by_treatment"] == {
        "NATURAL": 20,
        "SUPPLEMENTED": 20,
    }
    assert all(result["gates"].values())
    assert (
        result["bootstrap_95_ci"][
            "initial_seed_set_delta"
        ][0]
        > 0.10
    )
    assert (
        result["bootstrap_95_ci"][
            "pollen_grains_delta"
        ][0]
        > 5.0
    )


def test_supplementation_that_changes_early_predator_attack_is_rejected() -> None:
    rows = _paired_rows()
    for row in rows:
        row["early_predator_attack_present"] = (
            "0"
            if row["pollination_treatment"] == "NATURAL"
            else "1"
        )
    result = evaluate(rows, _config(PAIRED))
    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"
    assert result["gates"]["early_predator_attack_stable"] is False


def test_no_pollen_limitation_means_P_weight_is_uninformative() -> None:
    rows = _paired_rows()
    for row in rows:
        if row["pollination_treatment"] == "SUPPLEMENTED":
            row["undamaged_seed_count"] = "6"
    result = evaluate(rows, _config(PAIRED))
    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"
    assert (
        result["gates"][
            "supplementation_changes_pollination_weight"
        ]
        is False
    )


def test_paired_design_rejects_one_arm_plants() -> None:
    rows = [
        row
        for row in _paired_rows()
        if not (
            row["plant_id"] == "P00"
            and row["pollination_treatment"] == "SUPPLEMENTED"
        )
    ]
    with pytest.raises(
        ValueError,
        match="requires every plant to contain both",
    ):
        evaluate(rows, _config(PAIRED))


def test_whole_plant_design_rejects_plants_with_both_treatments() -> None:
    rows = _paired_rows()
    with pytest.raises(
        ValueError,
        match="exactly one pollination treatment",
    ):
        evaluate(rows, _config(WHOLE))


def test_design_context_must_match_confirmatory_data() -> None:
    config = _config(PAIRED)
    config["pollination_design"]["season_id"] = "S2"
    with pytest.raises(
        ValueError,
        match="population/season must match",
    ):
        evaluate(_paired_rows(), config)


def test_contract_maps_open_supplementation_without_pollinator_exclusion() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "P1 = open natural pollination" in text
    assert (
        "P0 = open + standardized saturating supplemental cross-pollen"
        in text
    )
    assert (
        "seed-predator natural-history window overlaps open flowering"
        in text
    )
    assert (
        "later predation fraction is not the only selectivity check"
        in text
    )
    assert "WITHIN_PLANT_PAIRED_FLOWERS" in text
    assert "WHOLE_PLANT_SUPPLEMENTATION" in text
