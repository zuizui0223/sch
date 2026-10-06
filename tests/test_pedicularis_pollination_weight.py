from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_pollination_weight import (
    REQUIRED_FIELDS,
    _allocation_identity,
    _semantic_sha256,
    evaluate,
    evaluate_locked,
)
from scripts.pedicularis_config_freeze import required_gate_paths


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "SCH_PEDICULARIS_POLLINATION_WEIGHT_AND_4_STATE_MAPPING_V1.md"


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
        "prospective_freeze": _freeze("P1"),
        "bootstrap_reps": 300,
        "random_seed": 31,
        "pollination_weight": {
            "experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
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


def _allocation_receipt(
    rows: list[dict[str, str]],
    config: dict,
) -> dict:
    return {
        "receipt_schema": "PEDICULARIS_P1_RANDOMIZED_ALLOCATION_V1",
        "status": "P1_FLOWERS_RANDOMIZED_NOT_YET_MEASURED",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
        "n_allocated_flowers": len(rows),
        "p1_field_config_sha256": _semantic_sha256(config),
        "allocation_identity_sha256": "a" * 64,
        "assignment_method": "SHA256_WITHIN_PLANT_BALANCED_P1_V1",
        "expected_assignments": _allocation_identity(rows),
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
                    "pollination_handling_role": (
                        "DONOR_MIXED_CROSS_POLLEN"
                        if treatment == "SUPPLEMENTED"
                        else "SHAM_STIGMA_CONTACT"
                    ),
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
    assert config["pollination_weight"]["experimental_unit"] == "WITHIN_PLANT_PAIRED_FLOWERS"
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


def test_current_evaluator_rejects_whole_plant_experimental_unit() -> None:
    config = _config()
    config["pollination_weight"]["experimental_unit"] = (
        "WHOLE_PLANT_SUPPLEMENTATION"
    )

    try:
        evaluate(_rows(), config)
    except ValueError as exc:
        assert "supports only WITHIN_PLANT_PAIRED_FLOWERS" in str(exc)
    else:
        raise AssertionError("whole-plant route should fail current V1 evaluator")


def test_handling_role_must_match_treatment() -> None:
    rows = _rows()
    rows[0]["pollination_handling_role"] = "DONOR_MIXED_CROSS_POLLEN"

    try:
        evaluate(rows, _config())
    except ValueError as exc:
        assert "pollination_handling_role" in str(exc)
    else:
        raise AssertionError("mismatched P1 handling role should fail")


def test_locked_evaluator_accepts_exact_randomized_assignment() -> None:
    rows = _rows()
    config = _config()
    result = evaluate_locked(
        rows,
        config,
        _allocation_receipt(rows, config),
    )

    assert result["status"] == "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"
    assert result["field_allocation_verification"][
        "identity_treatment_handling_match"
    ] is True
    assert result["field_allocation_verification"]["experimental_unit"] == (
        "WITHIN_PLANT_PAIRED_FLOWERS"
    )


def test_locked_evaluator_rejects_treatment_drift() -> None:
    rows = _rows()
    config = _config()
    receipt = _allocation_receipt(rows, config)
    changed = [dict(row) for row in rows]
    changed[0]["pollination_treatment"] = "SUPPLEMENTED"
    changed[0]["pollination_handling_role"] = "DONOR_MIXED_CROSS_POLLEN"

    try:
        evaluate_locked(changed, config, receipt)
    except ValueError as exc:
        assert "drifted from randomized allocation" in str(exc)
    else:
        raise AssertionError("P1 treatment drift should fail locked evaluator")


def test_locked_evaluator_rejects_field_config_drift() -> None:
    rows = _rows()
    config = _config()
    receipt = _allocation_receipt(rows, config)
    changed_config = json.loads(json.dumps(config))
    changed_config["pollination_weight"]["min_pollen_grain_delta"] = 6.0

    try:
        evaluate_locked(rows, changed_config, receipt)
    except ValueError as exc:
        assert "exact analyzed field config" in str(exc)
    else:
        raise AssertionError("P1 config drift should fail locked evaluator")
