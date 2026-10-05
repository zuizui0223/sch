from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PRIMARY_METHOD_ADJUDICATION_V1.csv"
)

EXPECTED_ASSETS = {
    "PRIMARY_JING2013_METHODS": "P1",
    "PRIMARY_WANG1998_PDF": "P1",
    "PRIMARY_TANG2011_THESIS": "G",
}

ALLOWED_FLAG_VALUES = {
    "YES",
    "NO",
    "UNRESOLVED",
    "PARTIAL",
    "NOT_APPLICABLE",
}

P1_TREATMENTS = {
    "HAND_UNSPECIFIED",
    "NATURAL_POLLINATION_DEPENDENCE_ONLY",
    "OPEN_SUPPLEMENTAL_OUTCROSS",
    "BAGGED_HAND_CROSS",
    "BAGGED_SELF_CROSS_ASSAY",
    "OTHER_HAND_TREATMENT",
}

G_TREATMENTS = {
    "NATURAL_HISTORY_ONLY",
    "PREDATOR_ACCESS_EXCLUSION",
    "WATER_DEFENCE_MANIPULATION",
    "OTHER_ANTAGONIST_TREATMENT",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("primary-method adjudication ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("primary-method adjudication ledger is empty")
    return rows


def _yes(row: dict[str, str], field: str) -> bool:
    return row.get(field) == "YES"


def _validate_flags(row: dict[str, str]) -> None:
    for field in (
        "primary_binary_retrieved",
        "p_rex_methods_confirmed",
        "open_natural_control",
        "supplemental_cross_pollen",
        "flowers_open_to_natural_visitors",
        "standardized_multi_donor_cross_pollen",
        "sample_size_reported",
        "reproductive_outcome_reported",
        "pre_predation_reproductive_endpoint_reported",
        "predator_exposed_control",
        "predator_exclusion_intervention",
        "water_y_held_fixed",
        "natural_pollination_preserved",
        "timing_or_localization_qualified",
        "pollinator_entry_preserved",
        "seed_predation_outcome_reported",
        "final_seed_outcome_reported",
    ):
        value = row.get(field, "")
        if value not in ALLOWED_FLAG_VALUES and not (
            field == "timing_or_localization_qualified"
            and value == "NATURAL_HISTORY_ONLY"
        ):
            raise ValueError(
                f"{row.get('asset_id', '<row>')}.{field} has invalid value {value!r}"
            )


def _require_primary_locator(row: dict[str, str]) -> bool:
    locator = row.get("methods_locator", "")
    return (
        bool(locator)
        and locator not in {
            "UNRESOLVED_PRIMARY_METHODS",
            "PUBLIC_611KB_PDF_LISTED_BINARY_NOT_RETRIEVED",
            "FULL_ENGLISH_ABSTRACT_RECOVERED_FULL_THESIS_BINARY_NOT_RETRIEVED",
        }
    )


def _adjudicate_p1(row: dict[str, str]) -> dict:
    asset = row["asset_id"]
    if row["primary_binary_retrieved"] != "YES":
        return {
            "asset_id": asset,
            "gap": "P1",
            "status": "PRIMARY_BINARY_NOT_RETRIEVED",
            "direct_focal_supplementation_effect_recovered": False,
            "registered_p1_estimand_recovered": False,
            "registered_protocol_family_compatible": False,
            "reason": "Primary Methods are not available for treatment adjudication.",
        }

    if row["p_rex_methods_confirmed"] != "YES":
        return {
            "asset_id": asset,
            "gap": "P1",
            "status": "P_REX_METHODS_NOT_CONFIRMED",
            "direct_focal_supplementation_effect_recovered": False,
            "registered_p1_estimand_recovered": False,
            "registered_protocol_family_compatible": False,
            "reason": "Retrieved binary does not yet confirm a P. rex methods block.",
        }

    if not _require_primary_locator(row):
        raise ValueError(
            f"{asset} is marked retrieved but lacks a concrete primary Methods/Table locator"
        )

    treatment = row["treatment_identity"]
    if treatment not in P1_TREATMENTS:
        raise ValueError(f"{asset} has invalid P1 treatment_identity {treatment!r}")

    open_supplement = (
        treatment == "OPEN_SUPPLEMENTAL_OUTCROSS"
        and _yes(row, "open_natural_control")
        and _yes(row, "supplemental_cross_pollen")
        and _yes(row, "flowers_open_to_natural_visitors")
        and _yes(row, "sample_size_reported")
        and _yes(row, "reproductive_outcome_reported")
    )

    direct_effect = open_supplement
    registered_estimand = (
        direct_effect
        and _yes(row, "pre_predation_reproductive_endpoint_reported")
    )
    protocol_compatible = (
        registered_estimand
        and _yes(row, "standardized_multi_donor_cross_pollen")
    )

    if protocol_compatible:
        status = "DIRECT_FOCAL_P1_REGISTERED_FAMILY_RECOVERED"
        reason = (
            "Primary Methods show an open natural control plus standardized "
            "multi-donor supplemental outcross pollen with a pre-predation "
            "reproductive endpoint."
        )
    elif registered_estimand:
        status = "DIRECT_FOCAL_P1_EFFECT_RECOVERED_PROTOCOL_NOT_FULLY_EQUIVALENT"
        reason = (
            "A focal open supplementation effect on a pre-predation endpoint "
            "is recovered, but the historical donor protocol is not fully "
            "equivalent to the registered standardized multi-donor P1 method."
        )
    elif direct_effect:
        status = "DIRECT_FOCAL_SUPPLEMENTATION_EFFECT_RECOVERED_ENDPOINT_NOT_REGISTERED"
        reason = (
            "Open supplemental outcross pollen is recovered, but the reported "
            "outcome is not the registered pre-predation P1 estimand."
        )
    else:
        status = "PRIMARY_METHODS_RECOVERED_NONREGISTERED_P1_TREATMENT"
        reason = (
            "Primary Methods are recovered but do not document the open "
            "supplemental-outcross contrast required for direct focal P1."
        )

    return {
        "asset_id": asset,
        "gap": "P1",
        "status": status,
        "direct_focal_supplementation_effect_recovered": direct_effect,
        "registered_p1_estimand_recovered": registered_estimand,
        "registered_protocol_family_compatible": protocol_compatible,
        "reason": reason,
    }


def _adjudicate_g(row: dict[str, str]) -> dict:
    asset = row["asset_id"]
    if row["primary_binary_retrieved"] != "YES":
        return {
            "asset_id": asset,
            "gap": "G",
            "status": "PRIMARY_BINARY_NOT_RETRIEVED",
            "direct_focal_independent_g_recovered": False,
            "registered_g_effect_estimand_recovered": False,
            "registered_g_protocol_family_compatible": False,
            "reason": "Full P. rex-specific primary Methods are not available.",
        }

    if row["p_rex_methods_confirmed"] != "YES":
        return {
            "asset_id": asset,
            "gap": "G",
            "status": "P_REX_METHODS_NOT_CONFIRMED",
            "direct_focal_independent_g_recovered": False,
            "registered_g_effect_estimand_recovered": False,
            "registered_g_protocol_family_compatible": False,
            "reason": "Retrieved thesis text does not yet confirm a P. rex methods block.",
        }

    if not _require_primary_locator(row):
        raise ValueError(
            f"{asset} is marked retrieved but lacks a concrete primary Methods/Table locator"
        )

    treatment = row["treatment_identity"]
    if treatment not in G_TREATMENTS:
        raise ValueError(f"{asset} has invalid G treatment_identity {treatment!r}")

    core_exclusion = (
        treatment == "PREDATOR_ACCESS_EXCLUSION"
        and _yes(row, "predator_exposed_control")
        and _yes(row, "predator_exclusion_intervention")
        and _yes(row, "water_y_held_fixed")
        and _yes(row, "sample_size_reported")
        and _yes(row, "seed_predation_outcome_reported")
    )

    direct_g = core_exclusion
    effect_estimand = (
        direct_g
        and _yes(row, "final_seed_outcome_reported")
    )
    protocol_compatible = (
        effect_estimand
        and _yes(row, "natural_pollination_preserved")
        and _yes(row, "timing_or_localization_qualified")
        and _yes(row, "pollinator_entry_preserved")
    )

    if protocol_compatible:
        status = "DIRECT_FOCAL_REGISTERED_G_FAMILY_RECOVERED"
        reason = (
            "Primary Methods document predator access/exclusion with water-y "
            "fixed, exposed control, natural pollination preserved, qualified "
            "timing/localization, and predator/final-seed outcomes."
        )
    elif effect_estimand:
        status = "DIRECT_FOCAL_INDEPENDENT_G_RECOVERED_SELECTIVITY_NOT_REGISTERED"
        reason = (
            "A focal independent predator exclusion effect is recovered, but "
            "natural-pollination/timing/access selectivity is not fully "
            "equivalent to the registered G method."
        )
    elif direct_g:
        status = "DIRECT_FOCAL_PREDATOR_EXCLUSION_RECOVERED_ENDPOINT_INCOMPLETE"
        reason = (
            "Predator exclusion is recovered, but the final reproductive "
            "endpoint needed for the registered G effect estimand is missing."
        )
    else:
        status = "PRIMARY_METHODS_RECOVERED_NONREGISTERED_G_TREATMENT"
        reason = (
            "Primary Methods are recovered but do not document an independent "
            "predator access/exclusion intervention with water-y fixed."
        )

    return {
        "asset_id": asset,
        "gap": "G",
        "status": status,
        "direct_focal_independent_g_recovered": direct_g,
        "registered_g_effect_estimand_recovered": effect_estimand,
        "registered_g_protocol_family_compatible": protocol_compatible,
        "reason": reason,
    }


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)
    ids = [row["asset_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("asset_id must be unique")
    if set(ids) != set(EXPECTED_ASSETS):
        raise ValueError(
            "primary-method adjudication asset coverage mismatch: "
            f"missing={sorted(set(EXPECTED_ASSETS) - set(ids))}, "
            f"extra={sorted(set(ids) - set(EXPECTED_ASSETS))}"
        )

    results = []
    for row in rows:
        _validate_flags(row)
        expected_gap = EXPECTED_ASSETS[row["asset_id"]]
        if row["gap"] != expected_gap:
            raise ValueError(
                f"{row['asset_id']} gap mismatch: expected {expected_gap}, got {row['gap']}"
            )
        if expected_gap == "P1":
            results.append(_adjudicate_p1(row))
        else:
            results.append(_adjudicate_g(row))

    p1_results = [row for row in results if row["gap"] == "P1"]
    g_results = [row for row in results if row["gap"] == "G"]

    direct_p1 = any(
        row["direct_focal_supplementation_effect_recovered"]
        for row in p1_results
    )
    registered_p1 = any(
        row["registered_p1_estimand_recovered"]
        for row in p1_results
    )
    protocol_p1 = any(
        row["registered_protocol_family_compatible"]
        for row in p1_results
    )
    direct_g = any(
        row["direct_focal_independent_g_recovered"]
        for row in g_results
    )
    registered_g = any(
        row["registered_g_effect_estimand_recovered"]
        for row in g_results
    )
    protocol_g = any(
        row["registered_g_protocol_family_compatible"]
        for row in g_results
    )

    if protocol_p1 or protocol_g:
        status = "PRIMARY_METHOD_BINARY_RECOVERY_CHANGES_DIRECT_GAP_REAUDIT_FIELD_PLAN"
    elif direct_p1 or direct_g:
        status = "PRIMARY_METHOD_BINARY_RECOVERY_ADDS_FOCAL_EFFECT_BUT_FIELD_PROTOCOL_STILL_REQUIRED"
    else:
        status = "PRIMARY_METHOD_ADJUDICATION_READY_DIRECT_P1_G_STILL_UNRECOVERED"

    return {
        "analysis": "pedicularis_primary_method_adjudication_v1",
        "n_primary_assets": len(rows),
        "asset_results": {
            row["asset_id"]: row
            for row in sorted(results, key=lambda item: item["asset_id"])
        },
        "direct_focal_p1_effect_recovered": direct_p1,
        "registered_p1_estimand_recovered": registered_p1,
        "registered_p1_protocol_family_compatible": protocol_p1,
        "direct_focal_independent_g_recovered": direct_g,
        "registered_g_effect_estimand_recovered": registered_g,
        "registered_g_protocol_family_compatible": protocol_g,
        "direct_f0_values_recovered": 0,
        "field_calibration_still_required": True,
        "status": status,
        "claim_ceiling": [
            "primary_method_recovery_can_change_historical_direct_effect_status_but_not_prospective_F0",
            "hand_pollination_is_not_supplementation_without_open_control_and_cross_pollen",
            "bagged_breeding_system_assay_is_not_registered_P1",
            "water_defence_manipulation_is_not_independent_G",
            "predator_exclusion_without_natural_pollination_selectivity_is_not_registered_G",
            "same_context_prospective_calibration_remains_required_even_after_historical_effect_recovery",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Adjudicate retrieved focal Pedicularis primary Methods against "
            "the registered P1 and independent-G intervention definitions"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
