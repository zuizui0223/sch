"""Bundle the Pedicularis SCH state-optimum receipt and conflict handoff.

The bundle prevents Experiment B from using state optima from one SCH context and
a conflict budget from another.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FULL_SCHEMA = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"
FULL_WRAPPER = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
HANDOFF_SCHEMA = "THREE_WORLD_CONFLICT_HANDOFF_V1"
BUNDLE_SCHEMA = "PEDICULARIS_THREE_WORLD_SCH_BUNDLE_V1"


def _text(value: object, name: str) -> str:
    out = str(value).strip()
    if not out:
        raise ValueError(f"{name} is required")
    return out


def bundle(full_surface: dict, conflict_handoff: dict) -> dict:
    if full_surface.get("receipt_schema_version") != FULL_SCHEMA:
        raise ValueError(f"full surface must use {FULL_SCHEMA}")
    if full_surface.get("system_wrapper_schema_version") != FULL_WRAPPER:
        raise ValueError(f"full surface must use {FULL_WRAPPER}")
    if full_surface.get("status") != "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE":
        raise ValueError("full surface must be a positive causal-compromise candidate")
    if full_surface.get("system") != "Pedicularis rex":
        raise ValueError("full surface must be Pedicularis rex")

    if conflict_handoff.get("receipt_schema_version") != HANDOFF_SCHEMA:
        raise ValueError(f"conflict handoff must use {HANDOFF_SCHEMA}")
    if conflict_handoff.get("status") != "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED":
        raise ValueError("conflict handoff is not positive")
    if conflict_handoff.get("system") != "Pedicularis rex":
        raise ValueError("conflict handoff must be Pedicularis rex")

    population = _text(full_surface.get("population_id"), "full_surface.population_id")
    season = _text(full_surface.get("season_id"), "full_surface.season_id")
    if conflict_handoff.get("population_id") != population or conflict_handoff.get("season_id") != season:
        raise ValueError("full surface and conflict handoff must match population and season")

    mapping = full_surface.get("pedicularis_state_mapping")
    if not isinstance(mapping, dict):
        raise ValueError("full surface lacks Pedicularis state mapping")
    if mapping.get("G0") != "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED" or mapping.get("G1") != "SEED_PREDATOR_EXPOSED":
        raise ValueError("full surface does not use independent seed-predator G states")
    if mapping.get("water_y") != "HELD_FIXED_ACROSS_ALL_SCH_CELLS":
        raise ValueError("water-y was not fixed during Experiment A")

    est = full_surface.get("observed_estimands")
    semantics = full_surface.get("optimum_semantics")
    if not isinstance(est, dict) or not isinstance(semantics, dict):
        raise ValueError("full surface lacks state-optimum estimands/semantics")
    for field in ("z_pollinator_context", "z_antagonist_context", "z_combined"):
        if field not in est:
            raise ValueError(f"full surface lacks {field}")

    conflict = conflict_handoff.get("conflict_load")
    if not isinstance(conflict, dict):
        raise ValueError("conflict handoff lacks conflict_load")

    return {
        "receipt_schema_version": BUNDLE_SCHEMA,
        "status": "PEDICULARIS_SCH_EXPERIMENT_A_BUNDLED",
        "context_id": _text(conflict_handoff.get("context_id"), "context_id"),
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "fitness_scale_id": _text(conflict_handoff.get("fitness_scale_id"), "fitness_scale_id"),
        "state_optima": {
            "z_P_star": est["z_pollinator_context"],
            "z_G_star": est["z_antagonist_context"],
            "z_C_star": est["z_combined"],
            "z_P_semantics": semantics.get("z_pollinator_context"),
            "z_G_semantics": semantics.get("z_antagonist_context"),
            "z_C_semantics": semantics.get("z_combined"),
        },
        "conflict_load": conflict,
        "experiment_A_guards": {
            "independent_seed_predator_G": True,
            "water_y_held_fixed": True,
            "pollinator_access_preserved_by_registered_G_method": (
                "POLLINATOR_ACCESS_PRESERVED" in str(full_surface.get("readiness_reference", {}).get("predator_method_requirement", ""))
            ),
        },
        "source": {
            "full_surface_schema": FULL_SCHEMA,
            "system_wrapper_schema": FULL_WRAPPER,
            "conflict_handoff_schema": HANDOFF_SCHEMA,
        },
        "claim_ceiling": (
            "same-context SCH Experiment-A bundle: state-specific reference geometry plus fitness-scale conflict budget; "
            "does not identify BALANCE worldline order or BITA dimensional release"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("full_surface_json", type=Path)
    parser.add_argument("conflict_handoff_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    full_surface = json.loads(args.full_surface_json.read_text(encoding="utf-8"))
    conflict_handoff = json.loads(args.conflict_handoff_json.read_text(encoding="utf-8"))
    out = bundle(full_surface, conflict_handoff)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
