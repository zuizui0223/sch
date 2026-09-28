from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


SCHEMA = "SCH_PEDICULARIS_P1_DESIGN_FREEZE_V1"
STATUS = "PEDICULARIS_P1_DESIGN_PROSPECTIVELY_FROZEN"

DESIGNS = {
    "WITHIN_PLANT_PAIRED_FLOWERS": {
        "treatment_assignment": "PAIRED_WITHIN_PLANT",
        "estimand_family": "PAIRED_PLANT_LEVEL_TREATMENT_CONTRAST",
    },
    "WHOLE_PLANT_RANDOMIZED": {
        "treatment_assignment": "RANDOMIZED_BETWEEN_PLANTS",
        "estimand_family": "INDEPENDENT_ARM_PLANT_LEVEL_TREATMENT_CONTRAST",
    },
}


def _text(payload: dict, field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip() or value == "REQUIRED_BEFORE_USE":
        raise ValueError(f"{field} is not prospectively specified")
    return value.strip()


def _timestamp(payload: dict, field: str) -> str:
    value = _text(payload, field)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value


def validate(payload: dict) -> dict:
    if payload.get("receipt_schema_version") != SCHEMA:
        raise ValueError("P1 design receipt schema mismatch")
    if payload.get("status") != STATUS:
        raise ValueError("P1 design status is not positive")

    population_id = _text(payload, "population_id")
    season_id = _text(payload, "season_id")
    design_unit = _text(payload, "design_unit")
    if design_unit not in DESIGNS:
        raise ValueError(
            "design_unit must be WITHIN_PLANT_PAIRED_FLOWERS or WHOLE_PLANT_RANDOMIZED"
        )

    expected_assignment = DESIGNS[design_unit]["treatment_assignment"]
    assignment = _text(payload, "treatment_assignment")
    if assignment != expected_assignment:
        raise ValueError(
            f"{design_unit} requires treatment_assignment={expected_assignment}"
        )

    resource_reallocation_strategy = _text(
        payload,
        "resource_reallocation_strategy",
    )
    donor_protocol = _text(payload, "donor_protocol")
    randomization_or_matching_protocol = _text(
        payload,
        "randomization_or_matching_protocol",
    )
    basis_document = _text(payload, "basis_document")

    if payload.get("frozen_before_confirmatory_data") is not True:
        raise ValueError(
            "P1 design must be frozen before confirmatory data are inspected"
        )
    frozen_at_utc = _timestamp(payload, "frozen_at_utc")

    if design_unit == "WITHIN_PLANT_PAIRED_FLOWERS":
        if "paired" not in randomization_or_matching_protocol.lower():
            raise ValueError(
                "paired-flower design must document within-plant pairing in "
                "randomization_or_matching_protocol"
            )
    else:
        lower = randomization_or_matching_protocol.lower()
        if "random" not in lower:
            raise ValueError(
                "whole-plant design must document randomized between-plant assignment"
            )
        if "whole" not in resource_reallocation_strategy.lower():
            raise ValueError(
                "whole-plant design must explicitly explain whole-plant handling "
                "of resource-reallocation bias"
            )

    return {
        "receipt_schema_version": SCHEMA,
        "analysis": "pedicularis_p1_design_freeze",
        "population_id": population_id,
        "season_id": season_id,
        "design_unit": design_unit,
        "treatment_assignment": assignment,
        "estimand_family": DESIGNS[design_unit]["estimand_family"],
        "resource_reallocation_strategy": resource_reallocation_strategy,
        "donor_protocol": donor_protocol,
        "randomization_or_matching_protocol": randomization_or_matching_protocol,
        "basis_document": basis_document,
        "frozen_at_utc": frozen_at_utc,
        "status": STATUS,
        "claim_ceiling": [
            "design_unit_definition_only",
            "paired_and_whole_plant_estimands_are_not_interchangeable",
            "does_not_select_numeric_thresholds",
            "does_not_validate_pollination_weight",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the prospective Pedicularis P1 experimental-unit choice"
    )
    parser.add_argument("design_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.design_json.read_text(encoding="utf-8"))
    result = validate(payload)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
