from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts.analyze_sch_compromise_surface import analyze as analyze_sch_surface


RAW_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "assigned_z_level",
    "realized_exsertion",
    "pollination_treatment",
    "water_treatment",
    "ovule_count",
    "undamaged_seed_count",
    "damaged_seed_count",
    "pollen_grains",
    "early_predator_attack_present",
    "water_depth",
    "mechanical_damage",
)

POLLINATION_MAP = {"SUPPLEMENTED": 0, "NATURAL": 1}
ANTAGONIST_MAP = {"PROTECTED": 0, "DRAINED": 1}
READINESS_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V1"
READINESS_STATUS = "PEDICULARIS_FULL_SURFACE_READY"
SYSTEM_WRAPPER_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V1"


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
        missing = [field for field in RAW_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in RAW_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        if row["flower_id"] in seen:
            raise ValueError(f"duplicate flower_id {row['flower_id']!r}")
        seen.add(row["flower_id"])
        if row["pollination_treatment"] not in POLLINATION_MAP:
            raise ValueError("pollination_treatment must be NATURAL or SUPPLEMENTED")
        if row["water_treatment"] not in ANTAGONIST_MAP:
            raise ValueError("water_treatment must be PROTECTED or DRAINED")
        for field in (
            "realized_exsertion",
            "ovule_count",
            "undamaged_seed_count",
            "damaged_seed_count",
            "pollen_grains",
            "water_depth",
        ):
            _num(row, field)
        _binary(row, "early_predator_attack_present")
        _binary(row, "mechanical_damage")
        ovules = _num(row, "ovule_count")
        undamaged = _num(row, "undamaged_seed_count")
        damaged = _num(row, "damaged_seed_count")
        if ovules <= 0:
            raise ValueError("ovule_count must be > 0")
        if undamaged < 0 or damaged < 0:
            raise ValueError("seed counts must be >= 0")
        if undamaged + damaged > ovules:
            raise ValueError("undamaged_seed_count + damaged_seed_count cannot exceed ovule_count")
    return rows


def _context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one Pedicularis full-surface package must contain exactly one population and season")
    return next(iter(populations)), next(iter(seasons))


def _validate_readiness(readiness: dict, population: str, season: str) -> None:
    if readiness.get("receipt_schema_version") != READINESS_SCHEMA:
        raise ValueError("Pedicularis full-surface analysis requires the registered readiness receipt schema")
    if readiness.get("status") != READINESS_STATUS:
        raise ValueError("Pedicularis full-surface readiness status is not positive")
    if readiness.get("population_id") != population or readiness.get("season_id") != season:
        raise ValueError("raw full-surface data must match the population and season in the readiness receipt")


def to_sch_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    converted: list[dict[str, str]] = []
    for row in rows:
        converted.append(
            {
                "plant_id": row["plant_id"],
                "blossom_id": row["flower_id"],
                "z_level": row["assigned_z_level"],
                "z_measured": row["realized_exsertion"],
                "pollinator_state": str(POLLINATION_MAP[row["pollination_treatment"]]),
                "antagonist_state": str(ANTAGONIST_MAP[row["water_treatment"]]),
                "fitness_value": row["undamaged_seed_count"],
            }
        )
    return converted


def _initial_seed_set(row: dict[str, str]) -> float:
    return (_num(row, "undamaged_seed_count") + _num(row, "damaged_seed_count")) / _num(row, "ovule_count")


def _final_seed_set(row: dict[str, str]) -> float:
    return _num(row, "undamaged_seed_count") / _num(row, "ovule_count")


def _predation_fraction(row: dict[str, str]) -> float:
    initiated = _num(row, "undamaged_seed_count") + _num(row, "damaged_seed_count")
    return 0.0 if initiated <= 0 else _num(row, "damaged_seed_count") / initiated


def _secondary_summary(rows: list[dict[str, str]]) -> dict:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        p = POLLINATION_MAP[row["pollination_treatment"]]
        g = ANTAGONIST_MAP[row["water_treatment"]]
        groups[f"P{p}G{g}"].append(row)

    out = {}
    for state, group in sorted(groups.items()):
        out[state] = {
            "n": len(group),
            "mean_initial_seed_set": mean(_initial_seed_set(row) for row in group),
            "mean_final_seed_set": mean(_final_seed_set(row) for row in group),
            "mean_predation_fraction": mean(_predation_fraction(row) for row in group),
            "mean_pollen_grains": mean(_num(row, "pollen_grains") for row in group),
            "early_predator_attack_rate": mean(_binary(row, "early_predator_attack_present") for row in group),
            "mean_water_depth": mean(_num(row, "water_depth") for row in group),
            "mechanical_damage_rate": mean(_binary(row, "mechanical_damage") for row in group),
        }
    return out


def analyze(rows: list[dict[str, str]], readiness: dict, config: dict) -> dict:
    population, season = _context(rows)
    _validate_readiness(readiness, population, season)
    sch_config = config.get("sch_surface")
    if not isinstance(sch_config, dict):
        raise ValueError("config must contain a sch_surface object with frozen SCH thresholds")

    result = analyze_sch_surface(to_sch_rows(rows), sch_config)
    result["system_wrapper_schema_version"] = SYSTEM_WRAPPER_SCHEMA
    result["system"] = "Pedicularis rex"
    result["population_id"] = population
    result["season_id"] = season
    result["pedicularis_state_mapping"] = {
        "P0": "SUPPLEMENTED_OPEN_POLLINATION_DEPENDENCE_NEUTRALIZED",
        "P1": "NATURAL_OPEN_POLLINATION_DEPENDENCE_ACTIVE",
        "G0": "PROTECTED_WATER_RETAINED_ANTAGONIST_PRESSURE_SUPPRESSED",
        "G1": "DRAINED_ANTAGONIST_PRESSURE_ACTIVE",
        "fitness_value": "UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER",
        "interpretation": "P0 is functional-weight neutralization by saturating pollen, not pollinator absence; all flowers remain open to the antagonist pathway",
    }
    result["readiness_reference"] = {
        "schema": readiness["receipt_schema_version"],
        "status": readiness["status"],
        "population_id": readiness["population_id"],
        "season_id": readiness["season_id"],
    }
    result["pedicularis_secondary_outcomes"] = _secondary_summary(rows)
    result["pedicularis_claim_ceiling"] = (
        "contemporary_state_specific_causal_compromise_only; "
        "pure_function_optima_require_the_registered_component-stability_upgrade; "
        "historical_modularization_not_identified"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Pedicularis full z x P x G surface through the registered SCH analyzer")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("readiness_receipt", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    readiness = json.loads(args.readiness_receipt.read_text(encoding="utf-8"))
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze(rows, readiness, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
