from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.pedicularis_config_freeze import FREEZE_SCHEMA, FREEZE_STATUS
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


EXPECTED = {
    "z": {"schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1", "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED"},
    "p": {"schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1", "status": "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"},
    "g": {"schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4", "status": "PEDICULARIS_PREDATOR_METHOD_VALIDATED"},
}
READINESS_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"receipt {path} is not a JSON object")
    return payload


def assemble(z_receipt: dict, p_receipt: dict, g_receipt: dict) -> dict:
    receipts = {"z": z_receipt, "p": p_receipt, "g": g_receipt}
    checks: dict[str, bool] = {}
    contexts = []
    for lane, receipt in receipts.items():
        expected = EXPECTED[lane]
        checks[f"{lane}_schema"] = receipt.get("receipt_schema_version") == expected["schema"]
        checks[f"{lane}_status"] = receipt.get("status") == expected["status"]
        population = receipt.get("population_id")
        season = receipt.get("season_id")
        checks[f"{lane}_context_present"] = (
            isinstance(population, str) and bool(population) and isinstance(season, str) and bool(season)
        )
        freeze = receipt.get("config_freeze")
        checks[f"{lane}_threshold_freeze"] = (
            isinstance(freeze, dict)
            and freeze.get("schema") == FREEZE_SCHEMA
            and freeze.get("status") == FREEZE_STATUS
            and freeze.get("lane") == {"z": "P0", "p": "P1", "g": "G"}[lane]
            and freeze.get("population_id") == population
            and freeze.get("season_id") == season
        )
        contexts.append((population, season))

    same_context = len(set(contexts)) == 1
    checks["same_population_and_season"] = same_context

    z_allocation = z_receipt.get("field_allocation_verification")
    checks["z_randomized_allocation_verified"] = (
        isinstance(z_allocation, dict)
        and z_allocation.get("receipt_schema")
        == "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1"
        and z_allocation.get("identity_z_assignment_match") is True
        and z_allocation.get("physical_manipulation_setting_match") is True
    )
    z_level_plan_sha = (
        z_allocation.get("level_plan_sha256")
        if isinstance(z_allocation, dict)
        else None
    )
    z_field_config_sha = (
        z_allocation.get("p0_field_config_sha256")
        if isinstance(z_allocation, dict)
        else None
    )
    checks["z_plan_provenance_bound"] = (
        isinstance(z_level_plan_sha, str)
        and len(z_level_plan_sha) == 64
        and isinstance(z_field_config_sha, str)
        and len(z_field_config_sha) == 64
    )

    z_levels = z_receipt.get("z_levels")
    checks["z_levels_validated"] = (
        isinstance(z_levels, list)
        and len(z_levels) >= 5
        and len(z_levels) == len(set(z_levels))
        and all(isinstance(value, str) and bool(value) for value in z_levels)
    )
    sham_rank = z_receipt.get("sham_rank")
    validated_sham_z_level = (
        z_levels[sham_rank]
        if (
            checks["z_levels_validated"]
            and type(sham_rank) is int
            and 0 <= sham_rank < len(z_levels)
        )
        else None
    )
    z_manipulation_settings = z_receipt.get("z_manipulation_settings")
    setting_ids = (
        [
            row.get("manipulation_setting_id")
            for row in z_manipulation_settings
            if isinstance(row, dict)
        ]
        if isinstance(z_manipulation_settings, list)
        else []
    )
    setting_labels = (
        [
            row.get("assigned_z_level")
            for row in z_manipulation_settings
            if isinstance(row, dict)
        ]
        if isinstance(z_manipulation_settings, list)
        else []
    )
    checks["z_manipulation_settings_validated"] = (
        checks["z_levels_validated"]
        and isinstance(z_manipulation_settings, list)
        and len(z_manipulation_settings) == len(z_levels)
        and len(setting_ids) == len(z_levels)
        and all(isinstance(value, str) and bool(value) for value in setting_ids)
        and len(setting_ids) == len(set(setting_ids))
        and setting_labels == list(z_levels)
    )

    p_allocation = p_receipt.get("field_allocation_verification")
    p_field_config_sha = (
        p_allocation.get("p1_field_config_sha256")
        if isinstance(p_allocation, dict)
        else None
    )
    checks["p_plan_provenance_bound"] = (
        isinstance(p_field_config_sha, str)
        and len(p_field_config_sha) == 64
    )
    checks["p_randomized_allocation_verified"] = (
        isinstance(p_allocation, dict)
        and p_allocation.get("receipt_schema")
        == "PEDICULARIS_P1_RANDOMIZED_ALLOCATION_V1"
        and p_allocation.get("identity_treatment_handling_match") is True
        and p_allocation.get("experimental_unit")
        == "WITHIN_PLANT_PAIRED_FLOWERS"
    )

    g_allocation = g_receipt.get("field_allocation_verification")
    g_method_summary = g_receipt.get("method_summary")
    g_field_config_sha = (
        g_allocation.get("g_field_config_sha256")
        if isinstance(g_allocation, dict)
        else None
    )
    g_selection_sha = (
        g_allocation.get("selection_receipt_sha256")
        if isinstance(g_allocation, dict)
        else None
    )
    checks["g_plan_provenance_bound"] = (
        isinstance(g_field_config_sha, str)
        and len(g_field_config_sha) == 64
        and isinstance(g_selection_sha, str)
        and len(g_selection_sha) == 64
    )
    validated_g_method = (
        g_method_summary.get("exclusion_method")
        if isinstance(g_method_summary, dict)
        else None
    )
    validated_g_exposed_sham_method = (
        g_allocation.get("exposed_sham_method_code")
        if isinstance(g_allocation, dict)
        else None
    )
    checks["g_randomized_allocation_verified"] = (
        isinstance(g_allocation, dict)
        and g_allocation.get("receipt_schema")
        == "PEDICULARIS_G_CONFIRMATORY_RANDOMIZED_ALLOCATION_V1"
        and g_allocation.get("identity_treatment_method_sham_match") is True
        and isinstance(validated_g_method, str)
        and bool(validated_g_method)
        and g_allocation.get("selected_exclusion_method") == validated_g_method
        and isinstance(validated_g_exposed_sham_method, str)
        and bool(validated_g_exposed_sham_method)
        and validated_g_exposed_sham_method != validated_g_method
    )

    if checks["g_schema"]:
        checks["g_method_timing_validated"] = bool(g_receipt.get("gates")) and all(
            bool(value) for value in g_receipt.get("gates", {}).values()
        )
    else:
        checks["g_method_timing_validated"] = False

    ready = all(checks.values())
    population, season = contexts[0] if same_context else (None, None)

    return {
        "receipt_schema_version": READINESS_SCHEMA,
        "analysis": "pedicularis_pre_surface_readiness_timed_independent_predator_G",
        "population_id": population,
        "season_id": season,
        "checks": checks,
        "source_receipts": {
            lane: {
                "schema": receipt.get("receipt_schema_version"),
                "status": receipt.get("status"),
                "threshold_freeze_status": (
                    receipt.get("config_freeze", {}).get("status")
                    if isinstance(receipt.get("config_freeze"), dict)
                    else None
                ),
                "receipt_sha256": _semantic_sha256(receipt),
            }
            for lane, receipt in receipts.items()
        },
        "validated_execution": {
            "z_levels": list(z_levels) if checks["z_levels_validated"] else None,
            "p0_sham_z_level": validated_sham_z_level,
            "z_manipulation_settings": (
                z_manipulation_settings
                if checks["z_manipulation_settings_validated"]
                else None
            ),
            "p_experimental_unit": (
                p_allocation.get("experimental_unit")
                if checks["p_randomized_allocation_verified"]
                else None
            ),
            "g_exclusion_method": (
                validated_g_method
                if checks["g_randomized_allocation_verified"]
                else None
            ),
            "g_exposed_sham_method": (
                validated_g_exposed_sham_method
                if checks["g_randomized_allocation_verified"]
                else None
            ),
            "z_allocation_identity_sha256": (
                z_allocation.get("allocation_identity_sha256")
                if checks["z_randomized_allocation_verified"]
                else None
            ),
            "p_allocation_identity_sha256": (
                p_allocation.get("allocation_identity_sha256")
                if checks["p_randomized_allocation_verified"]
                else None
            ),
            "g_allocation_identity_sha256": (
                g_allocation.get("allocation_identity_sha256")
                if checks["g_randomized_allocation_verified"]
                else None
            ),
            "p0_level_plan_sha256": (
                z_level_plan_sha
                if checks["z_plan_provenance_bound"]
                else None
            ),
            "p0_field_config_sha256": (
                z_field_config_sha
                if checks["z_plan_provenance_bound"]
                else None
            ),
            "p1_field_config_sha256": (
                p_field_config_sha
                if checks["p_plan_provenance_bound"]
                else None
            ),
            "g_field_config_sha256": (
                g_field_config_sha
                if checks["g_plan_provenance_bound"]
                else None
            ),
            "g_method_selection_sha256": (
                g_selection_sha
                if checks["g_plan_provenance_bound"]
                else None
            ),
        },
        "status": "PEDICULARIS_FULL_SURFACE_READY" if ready else "PEDICULARIS_FULL_SURFACE_NOT_READY",
        "unlocked_next_step": (
            ">=5 realized z levels x pollination-weight P0/P1 x timed independent predator G0/G1 with water-y held fixed"
            if ready else None
        ),
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
        "claim_ceiling": "execution_readiness_only_not_causal_compromise_not_dimensional_release",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble fail-closed Pedicularis z/P/timed-independent-predator-G readiness receipt")
    parser.add_argument("z_receipt", type=Path)
    parser.add_argument("p_receipt", type=Path)
    parser.add_argument("g_receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = assemble(_load(args.z_receipt), _load(args.p_receipt), _load(args.g_receipt))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
