"""Export a SCH conflict-budget receipt into the shared three-world interface.

The existing SCH_COMPONENT_CONFLICT_BUDGET_V1 receipt remains unchanged.  This
adapter adds the biological context identity required by BALANCE and BITA so
cross-chapter comparisons cannot silently combine different population/season
contexts.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SOURCE_SCHEMA = "SCH_COMPONENT_CONFLICT_BUDGET_V1"
HANDOFF_SCHEMA = "THREE_WORLD_CONFLICT_HANDOFF_V1"


def _text(value: object, name: str) -> str:
    out = str(value).strip()
    if not out or out == "REQUIRED_BEFORE_USE":
        raise ValueError(f"{name} must be frozen before export")
    return out


def _nonnegative(value: object, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def export_handoff(receipt: dict, context: dict) -> dict:
    if receipt.get("receipt_schema_version") != SOURCE_SCHEMA:
        raise ValueError(f"source receipt must use {SOURCE_SCHEMA}")
    if receipt.get("status") != "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED":
        raise ValueError("source receipt does not identify a shared conflict budget")

    scale = _text(receipt.get("fitness_scale_id"), "source fitness_scale_id")
    context_scale = _text(context.get("fitness_scale_id"), "context fitness_scale_id")
    if scale != context_scale:
        raise ValueError("context fitness_scale_id must exactly match SCH receipt")

    context_id = _text(context.get("context_id"), "context_id")
    system = _text(context.get("system"), "system")
    population = _text(context.get("population_id"), "population_id")
    season = _text(context.get("season_id"), "season_id")

    try:
        point = _nonnegative(receipt["criticality_export"]["L_S_component"], "L point")
        raw_ci = receipt["criticality_export"]["L_S_component_95_ci"]
    except (KeyError, TypeError) as exc:
        raise ValueError("source receipt lacks criticality_export") from exc
    if not isinstance(raw_ci, list) or len(raw_ci) != 2:
        raise ValueError("L_S_component_95_ci must be a two-element list")
    lo = _nonnegative(raw_ci[0], "L lower")
    hi = _nonnegative(raw_ci[1], "L upper")
    if not lo <= point <= hi:
        raise ValueError("L point must lie within its interval")

    return {
        "receipt_schema_version": HANDOFF_SCHEMA,
        "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
        "context_id": context_id,
        "system": system,
        "population_id": population,
        "season_id": season,
        "fitness_scale_id": scale,
        "conflict_load": {
            "point": point,
            "lower_95": lo,
            "upper_95": hi,
            "source_field": "criticality_export.L_S_component",
        },
        "source": {
            "repository": "sch",
            "receipt_schema_version": SOURCE_SCHEMA,
            "source_sch_receipt_schema": receipt.get("source_sch_receipt_schema"),
        },
        "claim_ceiling": (
            "identified fitness-scale shared-coordinate conflict in one frozen biological context; "
            "does not establish BALANCE occupancy, differentiation, architecture cost, or history"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sch_conflict_budget_json", type=Path)
    parser.add_argument("context_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = json.loads(args.sch_conflict_budget_json.read_text(encoding="utf-8"))
    context = json.loads(args.context_json.read_text(encoding="utf-8"))
    result = export_handoff(receipt, context)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
