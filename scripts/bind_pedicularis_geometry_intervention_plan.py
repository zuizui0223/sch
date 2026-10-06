from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.assemble_pedicularis_f0_configs import (
    ASSEMBLY_SCHEMA,
    ASSEMBLY_STATUS,
)
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p0_randomized_assignment import _read_level_plan
from scripts.build_pedicularis_p1_randomized_assignment import (
    EXPERIMENTAL_UNIT,
    P1_FIELD_CONFIG_STATUS,
)
from scripts.freeze_pedicularis_g_confirmatory_method import (
    OUTPUT_SCHEMA as G_SELECTION_SCHEMA,
    OUTPUT_STATUS as G_SELECTION_STATUS,
)
from scripts.pedicularis_config_freeze import (
    FREEZE_STATUS,
    validate_prospective_freeze,
)


SCHEMA = "PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_BINDING_V1"
STATUS = "PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_FROZEN_BEFORE_CONFIRMATORY_OUTCOMES"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _context(payload: dict, label: str) -> tuple[str, str]:
    population = payload.get("population_id")
    season = payload.get("season_id")
    if not isinstance(population, str) or not population:
        raise ValueError(f"{label} population_id is missing")
    if not isinstance(season, str) or not season:
        raise ValueError(f"{label} season_id is missing")
    return population, season


def _validate_f0_config(config: dict, lane: str, expected_status: str) -> dict:
    if config.get("status") != expected_status:
        raise ValueError(f"{lane} F0 field config status is not frozen")
    freeze = validate_prospective_freeze(config, lane)
    if freeze.get("status") != FREEZE_STATUS:
        raise ValueError(f"{lane} prospective threshold freeze is not positive")
    return freeze


def build(
    *,
    geometry_config: dict,
    p0_level_plan: list[dict[str, str]],
    p0_field_config: dict,
    p1_field_config: dict,
    g_field_config: dict,
    g_method_selection: dict,
    f0_assembly_receipt: dict,
) -> dict:
    if geometry_config.get("schema") != "PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_V1":
        raise ValueError("geometry pilot config schema mismatch")
    if geometry_config.get("status") != (
        "PEDICULARIS_P2_GEOMETRY_PILOT_PROSPECTIVELY_FROZEN"
    ):
        raise ValueError("geometry pilot config is not prospectively frozen")
    if geometry_config.get("frozen_before_geometry_outcomes") is not True:
        raise ValueError("geometry pilot config must be frozen before outcomes")

    if f0_assembly_receipt.get("receipt_schema_version") != ASSEMBLY_SCHEMA:
        raise ValueError("F0 assembly receipt schema mismatch")
    if f0_assembly_receipt.get("status") != ASSEMBLY_STATUS:
        raise ValueError("F0 assembly receipt is not positive")

    p0_freeze = _validate_f0_config(
        p0_field_config,
        "P0",
        "PEDICULARIS_P0_FIELD_CONFIG_FROZEN",
    )
    p1_freeze = _validate_f0_config(
        p1_field_config,
        "P1",
        P1_FIELD_CONFIG_STATUS,
    )
    g_freeze = _validate_f0_config(
        g_field_config,
        "G",
        "PEDICULARIS_G_FIELD_CONFIG_FROZEN",
    )

    contexts = {
        _context(geometry_config, "geometry config"),
        _context(f0_assembly_receipt, "F0 assembly"),
        (p0_freeze["population_id"], p0_freeze["season_id"]),
        (p1_freeze["population_id"], p1_freeze["season_id"]),
        (g_freeze["population_id"], g_freeze["season_id"]),
    }

    if g_method_selection.get("receipt_schema") != G_SELECTION_SCHEMA:
        raise ValueError("confirmatory G method-selection receipt schema mismatch")
    if g_method_selection.get("status") != G_SELECTION_STATUS:
        raise ValueError("confirmatory G method-selection receipt is not positive")
    contexts.add(_context(g_method_selection, "G method selection"))

    if len(contexts) != 1:
        raise ValueError(
            "geometry, F0 P0/P1/G, and selected G method must share one population/season"
        )
    population_id, season_id = next(iter(contexts))

    p1_block = p1_field_config.get("pollination_weight")
    if not isinstance(p1_block, dict):
        raise ValueError("P1 field config lacks pollination_weight block")
    if p1_block.get("experimental_unit") != EXPERIMENTAL_UNIT:
        raise ValueError(
            "parallel geometry collection requires the current paired-flower P1 intervention"
        )

    normalized_plan = sorted(
        [
            {
                "assigned_z_level": row["assigned_z_level"],
                "assigned_z_rank": str(int(row["assigned_z_rank"])),
                "sham_control": row["sham_control"],
            }
            for row in p0_level_plan
        ],
        key=lambda row: int(row["assigned_z_rank"]),
    )
    geometry_z = sorted(
        [
            {
                "assigned_z_level": str(row["assigned_z_level"]),
                "assigned_z_rank": str(int(row["assigned_z_rank"])),
            }
            for row in geometry_config["z_levels"]
        ],
        key=lambda row: int(row["assigned_z_rank"]),
    )
    planned_z = [
        {
            "assigned_z_level": row["assigned_z_level"],
            "assigned_z_rank": row["assigned_z_rank"],
        }
        for row in normalized_plan
    ]
    if geometry_z != planned_z:
        raise ValueError(
            "geometry-pilot z labels/ranks must match the frozen P0 level plan"
        )

    selected_method = g_method_selection.get("selected_exclusion_method")
    selected_sham = g_method_selection.get("exposed_sham_method_code")
    if geometry_config.get("excluded_method_code") != selected_method:
        raise ValueError(
            "geometry excluded method must match the pre-outcome selected G method"
        )
    if geometry_config.get("exposed_method_code") != selected_sham:
        raise ValueError(
            "geometry exposed sham method must match the selected G sham method"
        )
    if g_method_selection.get("g_field_config_sha256") != _semantic_sha256(
        g_field_config
    ):
        raise ValueError(
            "selected G method receipt is not bound to the exact frozen G field config"
        )

    assembled_status = f0_assembly_receipt.get("assembled_config_status")
    if assembled_status != {
        "P0": p0_field_config["status"],
        "P1": p1_field_config["status"],
        "G": g_field_config["status"],
    }:
        raise ValueError("F0 assembly lane statuses do not match supplied field configs")

    supplied_config_sha = {
        "P0": _semantic_sha256(p0_field_config),
        "P1": _semantic_sha256(p1_field_config),
        "G": _semantic_sha256(g_field_config),
    }
    assembled_config_sha = f0_assembly_receipt.get("assembled_config_sha256")
    if assembled_config_sha != supplied_config_sha:
        raise ValueError(
            "supplied P0/P1/G configs are not the exact configs produced by F0 assembly"
        )

    p0_plan_sha = _semantic_sha256(normalized_plan)
    config_sha = _semantic_sha256(geometry_config)

    return {
        "analysis": "pedicularis_geometry_intervention_plan_binding_v1",
        "receipt_schema": SCHEMA,
        "population_id": population_id,
        "season_id": season_id,
        "geometry_config_sha256": config_sha,
        "p0_level_plan_sha256": p0_plan_sha,
        "p0_field_config_sha256": supplied_config_sha["P0"],
        "p1_field_config_sha256": supplied_config_sha["P1"],
        "g_field_config_sha256": supplied_config_sha["G"],
        "g_method_selection_sha256": _semantic_sha256(g_method_selection),
        "f0_assembly_receipt_sha256": _semantic_sha256(f0_assembly_receipt),
        "z_level_plan": normalized_plan,
        "p1_experimental_unit": EXPERIMENTAL_UNIT,
        "g_selected_candidate_id": g_method_selection.get(
            "selected_candidate_id"
        ),
        "g_exclusion_method": selected_method,
        "g_exposed_sham_method": selected_sham,
        "geometry_collection_may_run_before_lane_validation": True,
        "geometry_analysis_requires_later_positive_readiness_v3": True,
        "status": STATUS,
        "claim_ceiling": [
            "preoutcome_intervention_plan_identity_only",
            "P0_P1_G_configs_must_match_exact_F0_assembly_digests",
            "does_not_validate_P0_P1_or_G",
            "does_not_authorize_geometry_basis_use_before_readiness",
            "parallel_collection_is_wasted_if_any_lane_fails_readiness",
            "does_not_assign_W0_W5",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Bind the frozen P0/P1/G intervention plan to a separate geometry "
            "pilot before confirmatory outcomes, enabling parallel collection "
            "while deferring geometry use until later readiness V3"
        )
    )
    parser.add_argument("geometry_config_json", type=Path)
    parser.add_argument("p0_level_plan_csv", type=Path)
    parser.add_argument("p0_field_config_json", type=Path)
    parser.add_argument("p1_field_config_json", type=Path)
    parser.add_argument("g_field_config_json", type=Path)
    parser.add_argument("g_method_selection_json", type=Path)
    parser.add_argument("f0_assembly_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        geometry_config=_load(args.geometry_config_json),
        p0_level_plan=_read_level_plan(args.p0_level_plan_csv),
        p0_field_config=_load(args.p0_field_config_json),
        p1_field_config=_load(args.p1_field_config_json),
        g_field_config=_load(args.g_field_config_json),
        g_method_selection=_load(args.g_method_selection_json),
        f0_assembly_receipt=_load(args.f0_assembly_receipt_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
