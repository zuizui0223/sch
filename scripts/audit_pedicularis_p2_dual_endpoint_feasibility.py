from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CONFIG_SCHEMA = "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_P2_DUAL_ENDPOINT_ASSAY_PROSPECTIVELY_FROZEN"
PILOT_SCHEMA = "PEDICULARIS_P2_DUAL_ENDPOINT_PILOT_VALIDATION_V1"
PILOT_STATUS = "PEDICULARIS_P2_DUAL_ENDPOINT_COMPATIBILITY_VALIDATED"
RECEIPT_SCHEMA = "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1"
READY_STATUS = "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBLE_FOR_SINGLE_FLOWER_PIPELINE"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

SUPPORTED_CURRENT_ROUTES = {
    "SAME_FLOWER_NONDESTRUCTIVE_POLLEN_QUANTIFICATION",
    "SAME_FLOWER_POST_POLLINATION_STIGMA_SAMPLING_COMPATIBILITY_VALIDATED",
}

REQUIRED_PILOT_GATES = (
    "prospective_acceptance_margins_frozen",
    "pilot_cohort_independent_of_confirmatory_P2",
    "same_flower_pollen_count_and_mature_seed_linkage_verified",
    "pollen_count_accuracy_against_independent_reference_pass",
    "mature_seed_noninterference_equivalence_pass",
    "pollination_and_predator_treatment_compatibility_pass",
    "positive_nonzero_pollen_and_mature_seed_records_recovered",
)


def _semantic_sha256(payload: object) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{name} must be resolved before confirmatory P2")
    return value.strip()


def _hex_digest(value: object, name: str) -> str:
    value = _text(value, name)
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value.lower()):
        raise ValueError(f"{name} must be a 64-character SHA-256 hex digest")
    return value


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def build(config: dict, pilot: dict) -> dict:
    """Validate the current ONE-FLOWER pollen-plus-mature-seed assumption.

    Does not adjudicate split-sentinel designs or produce pilot outcomes.
    """
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError("dual-endpoint feasibility config schema mismatch")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("P2 dual-endpoint assay is not prospectively frozen")
    if config.get("frozen_before_compatibility_pilot_outcomes") is not True:
        raise ValueError(
            "P2 dual-endpoint assay/margins must be frozen before validation outcomes"
        )

    population = _text(config.get("population_id"), "population_id")
    season = _text(config.get("season_id"), "season_id")
    route = _text(config.get("collection_route"), "collection_route")
    method = _text(config.get("pollen_assay_method_id"), "pollen_assay_method_id")
    for field in (
        "assay_protocol_reference",
        "seed_endpoint_protocol_reference",
        "compatibility_margin_basis",
    ):
        _text(config.get(field), field)

    if route not in SUPPORTED_CURRENT_ROUTES:
        if route == "SPLIT_FLOWER_POLLEN_SENTINEL":
            raise ValueError(
                "split-flower pollen sentinels require a new two-cohort estimator, "
                "field allocation and W1/W2 power model; the current single-flower "
                "P2 analyzer does not support this route"
            )
        raise ValueError(
            "current P2 raw rows require a validated same-flower pollen-plus-mature-seed "
            "route; unvalidated destructive stigma crushing cannot authorize P2"
        )

    if pilot.get("receipt_schema") != PILOT_SCHEMA:
        raise ValueError("dual-endpoint independent pilot receipt schema mismatch")
    if pilot.get("status") != PILOT_STATUS:
        raise ValueError("joint pollen/seed endpoint compatibility is not validated")
    if pilot.get("population_id") != population or pilot.get("season_id") != season:
        raise ValueError(
            "dual-endpoint pilot and P2 assay plan must share population and season"
        )
    if pilot.get("collection_route") != route:
        raise ValueError("dual-endpoint pilot used a different collection route")
    if pilot.get("pollen_assay_method_id") != method:
        raise ValueError("dual-endpoint pilot used a different pollen assay")

    failed = [
        name for name in REQUIRED_PILOT_GATES
        if pilot.get(name) is not True
    ]
    if failed:
        raise ValueError(
            "same-flower pollen-plus-seed compatibility gates did not all pass: "
            + ", ".join(failed)
        )

    pilot_digest = _hex_digest(
        pilot.get("pilot_data_sha256"),
        "pilot_data_sha256",
    )
    pilot_protocol = _text(
        pilot.get("pilot_protocol_basis"),
        "pilot_protocol_basis",
    )
    if (
        config.get("compatibility_margin_basis")
        != pilot_protocol
    ):
        raise ValueError(
            "pilot prospective noninterference margin basis does not match assay freeze"
        )

    return {
        "analysis": "pedicularis_p2_dual_endpoint_feasibility_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "population_id": population,
        "season_id": season,
        "collection_route": route,
        "pollen_assay_method_id": method,
        "flower_endpoint_unit": "SAME_FLOWER",
        "same_flower_pollen_and_mature_seeds_validated": True,
        "accuracy_validation_passed": True,
        "mature_seed_noninterference_equivalence_passed": True,
        "predator_and_pollination_lane_compatibility_passed": True,
        "frozen_config_sha256": _semantic_sha256(config),
        "independent_pilot_receipt_sha256": _semantic_sha256(pilot),
        "independent_pilot_data_sha256": pilot_digest,
        "pilot_cohort_independent_of_confirmatory_P2": True,
        "status": READY_STATUS,
        "claim_ceiling": [
            "measurement_feasibility_only",
            "historical_crushed_stigmas_do_not_validate_joint_endpoint_collection",
            "no_split_flower_sentinel_design_accepted_by_current_analyzer",
            "no_P0_P1_G_validation_inferred",
            "no_W0_W5_or_seed_predator_effect_inferred",
            "power_must_use_variance_of_actual_qualified_pollen_assay",
        ],
    }


def validate_receipt(
    receipt: dict,
    population: str,
    season: str,
) -> dict:
    if receipt.get("receipt_schema") != RECEIPT_SCHEMA:
        raise ValueError("P2 allocation requires a dual-endpoint feasibility receipt")
    if receipt.get("status") != READY_STATUS:
        raise ValueError("P2 dual-endpoint feasibility is not positive")
    if receipt.get("population_id") != population or receipt.get("season_id") != season:
        raise ValueError(
            "P2 dual-endpoint feasibility population/season does not match field plan"
        )
    if receipt.get("collection_route") not in SUPPORTED_CURRENT_ROUTES:
        raise ValueError(
            "split-flower sentinels cannot be analyzed by the current P2 pipeline"
        )
    if receipt.get("flower_endpoint_unit") != "SAME_FLOWER":
        raise ValueError("current P2 pipeline requires the same actual flower for both endpoints")
    for field in (
        "same_flower_pollen_and_mature_seeds_validated",
        "accuracy_validation_passed",
        "mature_seed_noninterference_equivalence_passed",
        "predator_and_pollination_lane_compatibility_passed",
        "pilot_cohort_independent_of_confirmatory_P2",
    ):
        if receipt.get(field) is not True:
            raise ValueError(
                f"P2 dual-endpoint feasibility lacks positive {field}"
            )
    for field in (
        "frozen_config_sha256",
        "independent_pilot_receipt_sha256",
        "independent_pilot_data_sha256",
    ):
        _hex_digest(receipt.get(field), field)
    return {
        "receipt_schema": RECEIPT_SCHEMA,
        "status": READY_STATUS,
        "collection_route": receipt["collection_route"],
        "pollen_assay_method_id": _text(
            receipt.get("pollen_assay_method_id"), "pollen_assay_method_id"
        ),
        "feasibility_receipt_sha256": _semantic_sha256(receipt),
        "independent_pilot_data_sha256": receipt["independent_pilot_data_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Block P. rex single-flower P2 collection until the same flower can "
            "yield an accurate pollen count AND unbiased mature seed endpoint"
        )
    )
    parser.add_argument("frozen_endpoint_assay_config_json", type=Path)
    parser.add_argument("independent_compatibility_pilot_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load(args.frozen_endpoint_assay_config_json),
        _load(args.independent_compatibility_pilot_receipt_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
