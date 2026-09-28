from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.freeze_pedicularis_p1_design import (
    SCHEMA,
    STATUS,
    validate,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_P1_DESIGN_TEMPLATE_V1.json"
)


def _payload(design_unit: str) -> dict:
    paired = design_unit == "WITHIN_PLANT_PAIRED_FLOWERS"
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
            "paired flowers retain individual blocking; resource reallocation "
            "risk is acknowledged and checked against whole-plant precedent"
            if paired
            else "whole-plant supplementation treats the whole flowering plant "
            "to reduce within-plant resource-reallocation bias"
        ),
        "donor_protocol": (
            "donor-mixed outcross pollen from non-focal plants; donor reuse limited "
            "prospectively"
        ),
        "randomization_or_matching_protocol": (
            "paired within-plant assignment of natural and supplemented flowers"
            if paired
            else "randomized between-plant assignment to natural or supplemented arms"
        ),
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-28T00:00:00Z",
        "basis_document": "UNIT_TEST_P1_DESIGN_BASIS",
    }


def test_design_template_is_intentionally_unfrozen() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert payload["receipt_schema_version"] == SCHEMA
    assert payload["status"] == "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="status is not positive"):
        validate(payload)


@pytest.mark.parametrize(
    "design_unit,estimand",
    [
        (
            "WITHIN_PLANT_PAIRED_FLOWERS",
            "PAIRED_PLANT_LEVEL_TREATMENT_CONTRAST",
        ),
        (
            "WHOLE_PLANT_RANDOMIZED",
            "INDEPENDENT_ARM_PLANT_LEVEL_TREATMENT_CONTRAST",
        ),
    ],
)
def test_both_registered_p1_design_units_validate(
    design_unit: str,
    estimand: str,
) -> None:
    result = validate(_payload(design_unit))
    assert result["status"] == STATUS
    assert result["design_unit"] == design_unit
    assert result["estimand_family"] == estimand
    assert result["population_id"] == "P_REX_TEST"
    assert result["season_id"] == "S1"


def test_paired_design_requires_paired_assignment() -> None:
    payload = _payload("WITHIN_PLANT_PAIRED_FLOWERS")
    payload["treatment_assignment"] = "RANDOMIZED_BETWEEN_PLANTS"
    with pytest.raises(ValueError, match="requires treatment_assignment"):
        validate(payload)


def test_whole_plant_design_requires_randomized_assignment() -> None:
    payload = _payload("WHOLE_PLANT_RANDOMIZED")
    payload["randomization_or_matching_protocol"] = (
        "plants allocated by convenience"
    )
    with pytest.raises(ValueError, match="randomized between-plant"):
        validate(payload)


def test_whole_plant_design_requires_resource_reallocation_rationale() -> None:
    payload = _payload("WHOLE_PLANT_RANDOMIZED")
    payload["resource_reallocation_strategy"] = "standard handling"
    with pytest.raises(ValueError, match="whole-plant handling"):
        validate(payload)


def test_design_must_be_frozen_before_confirmatory_data() -> None:
    payload = _payload("WITHIN_PLANT_PAIRED_FLOWERS")
    payload["frozen_before_confirmatory_data"] = False
    with pytest.raises(ValueError, match="before confirmatory data"):
        validate(payload)


def test_design_timestamp_must_be_timezone_aware() -> None:
    payload = _payload("WHOLE_PLANT_RANDOMIZED")
    payload["frozen_at_utc"] = "2026-09-28T00:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        validate(payload)
