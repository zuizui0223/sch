from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scripts.evaluate_pedicularis_predator_weight import evaluate as evaluate_predator_weight
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_g_confirmatory_assignment import (
    FROZEN_FIELDS as G_ALLOCATION_FROZEN_FIELDS,
    RECEIPT_SCHEMA as G_ALLOCATION_SCHEMA,
)
from scripts.pedicularis_config_freeze import (
    validate_freeze_context,
    validate_prospective_freeze,
)


REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "predator_treatment",
    "exclusion_method",
    "sham_device_applied",
    "anthesis_time_hours",
    "barrier_application_time_hours",
    "pollination_window_complete_before_barrier",
    "ovary_swollen_at_barrier",
    "barrier_covers_pollinator_entry",
    "pre_barrier_attack_present",
    "barrier_integrity_failure_present",
    "realized_exsertion",
    "water_depth",
    "pollen_grains",
    "pollinator_visits",
    "early_predator_attack_present",
    "ovule_count",
    "undamaged_seed_count",
    "damaged_seed_count",
    "mechanical_damage",
)

TREATMENTS = ("EXPOSED", "EXCLUDED")
RECEIPT_SCHEMA = "SCH_PEDICULARIS_PREDATOR_METHOD_V4"


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _binary(row: dict[str, str], field: str) -> int:
    raw = row[field].strip()
    if raw not in {"0", "1"}:
        raise ValueError(f"{field} must be coded 0/1, got {raw!r}")
    return int(raw)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        if row["flower_id"] in seen:
            raise ValueError(f"duplicate flower_id {row['flower_id']!r}")
        seen.add(row["flower_id"])
        if row["predator_treatment"] not in TREATMENTS:
            raise ValueError("predator_treatment must be EXPOSED or EXCLUDED")
        for field in (
            "anthesis_time_hours",
            "barrier_application_time_hours",
            "realized_exsertion",
            "water_depth",
            "pollen_grains",
            "pollinator_visits",
            "ovule_count",
            "undamaged_seed_count",
            "damaged_seed_count",
        ):
            _num(row, field)
        for field in (
            "sham_device_applied",
            "pollination_window_complete_before_barrier",
            "ovary_swollen_at_barrier",
            "barrier_covers_pollinator_entry",
            "pre_barrier_attack_present",
            "barrier_integrity_failure_present",
            "early_predator_attack_present",
            "mechanical_damage",
        ):
            _binary(row, field)
        if _num(row, "barrier_application_time_hours") < _num(row, "anthesis_time_hours"):
            raise ValueError("barrier_application_time_hours cannot precede anthesis_time_hours")
    return rows


def _context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one predator-method package must contain one population and season")
    return next(iter(populations)), next(iter(seasons))


def _timing_delay(row: dict[str, str]) -> float:
    return _num(row, "barrier_application_time_hours") - _num(row, "anthesis_time_hours")


def _method_gates(rows: list[dict[str, str]], config: dict) -> tuple[dict[str, bool], dict]:
    cfg = config["method_gate"]
    excluded = [row for row in rows if row["predator_treatment"] == "EXCLUDED"]
    exposed = [row for row in rows if row["predator_treatment"] == "EXPOSED"]
    if not excluded or not exposed:
        raise ValueError("both EXPOSED and EXCLUDED rows are required")

    methods = {row["exclusion_method"] for row in excluded}
    delays = [_timing_delay(row) for row in excluded]

    min_delay = float(cfg["min_hours_after_anthesis_before_barrier"])
    max_delay = float(cfg["max_hours_after_anthesis_before_barrier"])
    if min_delay < 0 or max_delay <= min_delay:
        raise ValueError("invalid prospective barrier timing window")

    paired_plants: dict[str, set[str]] = {}
    for row in rows:
        paired_plants.setdefault(row["plant_id"], set()).add(row["predator_treatment"])
    n_paired = sum(treatments == set(TREATMENTS) for treatments in paired_plants.values())
    counts = {t: sum(row["predator_treatment"] == t for row in rows) for t in TREATMENTS}

    gates = {
        "single_exclusion_method": len(methods) == 1,
        "minimum_paired_plants": n_paired >= int(cfg["min_paired_plants"]),
        "minimum_flowers_per_treatment": all(
            counts[t] >= int(cfg["min_flowers_per_treatment"]) for t in TREATMENTS
        ),
        "barrier_after_minimum_pollination_window": min(delays) >= min_delay,
        "barrier_before_maximum_registered_delay": max(delays) <= max_delay,
        "pollination_window_complete": (
            not bool(cfg.get("require_pollination_window_complete", True))
            or all(_binary(row, "pollination_window_complete_before_barrier") == 1 for row in excluded)
        ),
        "ovary_not_swollen_at_barrier": (
            not bool(cfg.get("require_ovary_not_swollen", True))
            or all(_binary(row, "ovary_swollen_at_barrier") == 0 for row in excluded)
        ),
        "pollinator_entry_not_covered": (
            not bool(cfg.get("require_barrier_not_cover_pollinator_entry", True))
            or all(_binary(row, "barrier_covers_pollinator_entry") == 0 for row in excluded)
        ),
        "no_attack_before_barrier": all(
            _binary(row, "pre_barrier_attack_present") == 0
            for row in excluded
        ),
        "barrier_integrity_preserved": all(
            _binary(row, "barrier_integrity_failure_present") == 0
            for row in excluded
        ),
        "exposed_has_sham_handling": (
            not bool(cfg.get("require_sham_on_exposed", True))
            or all(_binary(row, "sham_device_applied") == 1 for row in exposed)
        ),
    }
    summary = {
        "exclusion_method": next(iter(methods)) if len(methods) == 1 else sorted(methods),
        "barrier_delay_hours_min": min(delays),
        "barrier_delay_hours_max": max(delays),
        "n_paired_plants": n_paired,
        "n_by_treatment": counts,
        "n_excluded_with_pre_barrier_attack": sum(
            _binary(row, "pre_barrier_attack_present")
            for row in excluded
        ),
        "n_excluded_with_barrier_integrity_failure": sum(
            _binary(row, "barrier_integrity_failure_present")
            for row in excluded
        ),
    }
    return gates, summary


def validate_randomized_allocation(
    rows: list[dict[str, str]],
    allocation_receipt: dict,
    config: dict,
) -> None:
    if allocation_receipt.get("receipt_schema") != G_ALLOCATION_SCHEMA:
        raise ValueError("confirmatory G allocation receipt schema mismatch")
    if allocation_receipt.get("status") != (
        "G_CONFIRMATORY_FLOWERS_RANDOMIZED_NOT_YET_MEASURED"
    ):
        raise ValueError("confirmatory G allocation receipt is not valid")

    population, season = _context(rows)
    if allocation_receipt.get("population_id") != population:
        raise ValueError("confirmatory G allocation population does not match data")
    if allocation_receipt.get("season_id") != season:
        raise ValueError("confirmatory G allocation season does not match data")
    if int(allocation_receipt.get("n_allocated_flowers", -1)) != len(rows):
        raise ValueError("confirmatory G allocation row count does not match data")
    if allocation_receipt.get("g_field_config_sha256") != _semantic_sha256(config):
        raise ValueError(
            "confirmatory G allocation receipt is not bound to the exact G field config"
        )

    frozen_rows = sorted(
        [
            {
                field: row[field].strip()
                for field in G_ALLOCATION_FROZEN_FIELDS
            }
            for row in rows
        ],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )
    expected = allocation_receipt.get("expected_frozen_rows")
    if not isinstance(expected, list):
        raise ValueError(
            "confirmatory G allocation receipt lacks expected frozen rows"
        )
    if frozen_rows != expected:
        raise ValueError(
            "confirmatory G flower/treatment/method/sham assignment drifted "
            "from randomized allocation"
        )
    if _semantic_sha256(frozen_rows) != allocation_receipt.get(
        "allocation_identity_sha256"
    ):
        raise ValueError("confirmatory G allocation identity digest mismatch")


def evaluate_locked(
    rows: list[dict[str, str]],
    config: dict,
    allocation_receipt: dict,
) -> dict:
    validate_randomized_allocation(rows, allocation_receipt, config)
    result = evaluate(rows, config)
    result["field_allocation_verification"] = {
        "receipt_schema": allocation_receipt["receipt_schema"],
        "allocation_identity_sha256": allocation_receipt[
            "allocation_identity_sha256"
        ],
        "selection_receipt_sha256": allocation_receipt.get(
            "selection_receipt_sha256"
        ),
        "selected_candidate_id": allocation_receipt.get(
            "selected_candidate_id"
        ),
        "selected_exclusion_method": allocation_receipt.get(
            "selected_exclusion_method"
        ),
        "identity_treatment_method_sham_match": True,
    }
    return result


def evaluate(rows: list[dict[str, str]], config: dict) -> dict:
    freeze = validate_prospective_freeze(config, "G")
    population, season = _context(rows)
    validate_freeze_context(freeze, population, season)
    method_gates, method_summary = _method_gates(rows, config)
    predator_result = evaluate_predator_weight(rows, config)

    predator_positive = predator_result.get("status") == "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED"
    gates = {
        **{f"method_{key}": value for key, value in method_gates.items()},
        "predator_weight_selectivity": predator_positive,
    }
    status = "PEDICULARIS_PREDATOR_METHOD_VALIDATED" if all(gates.values()) else "PEDICULARIS_PREDATOR_METHOD_NOT_VALIDATED"

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "pedicularis_independent_seed_predator_method_qualification",
        "population_id": population,
        "season_id": season,
        "config_freeze": freeze,
        "method_summary": method_summary,
        "gates": gates,
        "predator_weight_receipt": predator_result,
        "status": status,
        "claim_ceiling": (
            "independent_antagonist_method_and_selectivity_only; "
            "not_causal_compromise; not_water_y_release; not_structural_trait_differentiation"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Qualify a timed Pedicularis seed-predator exclusion method")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument(
        "--allocation-receipt",
        type=Path,
        required=True,
        help=(
            "PEDICULARIS_G_CONFIRMATORY_RANDOMIZED_ALLOCATION_V1 receipt "
            "for the exact confirmatory flower IDs and EXPOSED/EXCLUDED arms"
        ),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    allocation_receipt = json.loads(
        args.allocation_receipt.read_text(encoding="utf-8")
    )
    result = evaluate_locked(rows, config, allocation_receipt)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
