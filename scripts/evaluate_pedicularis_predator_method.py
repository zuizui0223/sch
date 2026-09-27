from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scripts.evaluate_pedicularis_predator_weight import evaluate as evaluate_predator_weight


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
RECEIPT_SCHEMA = "SCH_PEDICULARIS_PREDATOR_METHOD_V3"


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
    }
    return gates, summary


def evaluate(rows: list[dict[str, str]], config: dict) -> dict:
    population, season = _context(rows)
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
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = evaluate(read_rows(args.csv_path), json.loads(args.config_path.read_text(encoding="utf-8")))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
