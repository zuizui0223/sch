from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Callable


REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "pollination_treatment",
    "realized_exsertion",
    "water_depth",
    "bract_height",
    "corolla_opening_width",
    "mechanical_damage",
    "pollen_grains_post_treatment",
    "early_predator_attack_present",
    "ovule_count",
    "undamaged_seed_count",
    "damaged_seed_count",
)
TREATMENTS = ("NATURAL", "SUPPLEMENTED")
RECEIPT_SCHEMA_VERSION = "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1"


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


def _validate_seed_counts(row: dict[str, str]) -> None:
    ovules = _num(row, "ovule_count")
    undamaged = _num(row, "undamaged_seed_count")
    damaged = _num(row, "damaged_seed_count")
    if ovules <= 0:
        raise ValueError("ovule_count must be > 0")
    if undamaged < 0 or damaged < 0:
        raise ValueError("seed counts must be >= 0")
    if undamaged + damaged > ovules:
        raise ValueError("undamaged_seed_count + damaged_seed_count cannot exceed ovule_count")


def _read_csv(path: Path) -> list[dict[str, str]]:
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
        if row["pollination_treatment"] not in TREATMENTS:
            raise ValueError("pollination_treatment must be NATURAL or SUPPLEMENTED")
        for field in (
            "realized_exsertion",
            "water_depth",
            "bract_height",
            "corolla_opening_width",
            "pollen_grains_post_treatment",
            "ovule_count",
            "undamaged_seed_count",
            "damaged_seed_count",
        ):
            _num(row, field)
        _binary(row, "mechanical_damage")
        _binary(row, "early_predator_attack_present")
        _validate_seed_counts(row)
    return rows


def _initial_seed_set(row: dict[str, str]) -> float:
    return (_num(row, "undamaged_seed_count") + _num(row, "damaged_seed_count")) / _num(row, "ovule_count")


def _final_seed_set(row: dict[str, str]) -> float:
    return _num(row, "undamaged_seed_count") / _num(row, "ovule_count")


def _predation_fraction(row: dict[str, str]) -> float:
    initiated = _num(row, "undamaged_seed_count") + _num(row, "damaged_seed_count")
    return 0.0 if initiated <= 0 else _num(row, "damaged_seed_count") / initiated


def _quantile(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        raise ValueError("cannot take quantile of empty values")
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return values[lo]
    w = pos - lo
    return values[lo] * (1 - w) + values[hi] * w


def _check_context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one pollination-weight package must contain exactly one population and season")
    return next(iter(populations)), next(iter(seasons))


def _groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[row["pollination_treatment"]].append(row)
    if set(out) != set(TREATMENTS):
        raise ValueError("both NATURAL and SUPPLEMENTED treatments are required")
    return out


def _paired_plants(rows: list[dict[str, str]]) -> list[str]:
    by_plant: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_plant[row["plant_id"]].add(row["pollination_treatment"])
    return sorted(plant for plant, treatments in by_plant.items() if treatments == set(TREATMENTS))


def _plant_mean(rows: list[dict[str, str]], plant: str, treatment: str, metric: Callable[[dict[str, str]], float]) -> float:
    selected = [r for r in rows if r["plant_id"] == plant and r["pollination_treatment"] == treatment]
    if not selected:
        raise ValueError("paired plant lost a treatment")
    return mean(metric(row) for row in selected)


def _paired_difference(rows: list[dict[str, str]], metric: Callable[[dict[str, str]], float], absolute: bool = False) -> float:
    plants = _paired_plants(rows)
    if len(plants) < 2:
        raise ValueError("at least two paired plants are required")
    diffs = []
    for plant in plants:
        diff = _plant_mean(rows, plant, "SUPPLEMENTED", metric) - _plant_mean(rows, plant, "NATURAL", metric)
        diffs.append(abs(diff) if absolute else diff)
    return mean(diffs)


def _paired_relative_difference(rows: list[dict[str, str]], field: str) -> float:
    plants = _paired_plants(rows)
    if len(plants) < 2:
        raise ValueError("at least two paired plants are required")
    diffs = []
    for plant in plants:
        natural = _plant_mean(rows, plant, "NATURAL", lambda r, f=field: _num(r, f))
        supplemented = _plant_mean(rows, plant, "SUPPLEMENTED", lambda r, f=field: _num(r, f))
        diffs.append(abs(supplemented - natural) / max(abs(natural), 1e-12))
    return mean(diffs)


def _maximum_damage_rate(rows: list[dict[str, str]]) -> float:
    groups = _groups(rows)
    return max(mean(_binary(row, "mechanical_damage") for row in groups[t]) for t in TREATMENTS)


def _bootstrap_paired(rows: list[dict[str, str]], statistic: Callable[[list[dict[str, str]]], float], reps: int, rng: random.Random) -> list[float]:
    plants = _paired_plants(rows)
    if len(plants) < 2:
        raise ValueError("at least two paired plants are required")
    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["plant_id"] in plants:
            by_plant[row["plant_id"]].append(row)
    out: list[float] = []
    for _ in range(reps):
        sampled: list[dict[str, str]] = []
        for draw, source_plant in enumerate(rng.choices(plants, k=len(plants))):
            # Relabel each bootstrap draw so duplicate source plants remain
            # distinct resampled clusters instead of collapsing back to one ID.
            for source_row in by_plant[source_plant]:
                row = dict(source_row)
                row["plant_id"] = f"BOOT_{draw:04d}"
                row["flower_id"] = f"BOOT_{draw:04d}_{source_row['flower_id']}"
                sampled.append(row)
        try:
            out.append(statistic(sampled))
        except ValueError:
            continue
    if len(out) < max(50, reps // 5):
        raise ValueError("too few valid paired bootstrap replicates")
    return out


def evaluate(rows: list[dict[str, str]], config: dict) -> dict:
    population_id, season_id = _check_context(rows)
    groups = _groups(rows)
    plants = _paired_plants(rows)
    cfg = config["pollination_weight"]
    reps = int(config["bootstrap_reps"])
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    rng = random.Random(int(config.get("random_seed", 20260904)))

    metrics: dict[str, Callable[[list[dict[str, str]]], float]] = {
        "initial_seed_set_delta": lambda x: _paired_difference(x, _initial_seed_set),
        "pollen_grains_delta": lambda x: _paired_difference(x, lambda r: _num(r, "pollen_grains_post_treatment")),
        "early_predator_attack_abs_difference": lambda x: _paired_difference(x, lambda r: float(_binary(r, "early_predator_attack_present")), absolute=True),
        "z_relative_difference": lambda x: _paired_relative_difference(x, "realized_exsertion"),
        "bract_height_relative_difference": lambda x: _paired_relative_difference(x, "bract_height"),
        "opening_width_relative_difference": lambda x: _paired_relative_difference(x, "corolla_opening_width"),
        "water_depth_abs_difference": lambda x: _paired_difference(x, lambda r: _num(r, "water_depth"), absolute=True),
        "maximum_mechanical_damage_rate": _maximum_damage_rate,
    }
    observed = {name: stat(rows) for name, stat in metrics.items()}
    cis: dict[str, list[float]] = {}
    for name, stat in metrics.items():
        values = _bootstrap_paired(rows, stat, reps, rng)
        cis[name] = [_quantile(values, 0.025), _quantile(values, 0.975)]

    min_group_n = int(cfg["min_flowers_per_treatment"])
    gates = {
        "minimum_paired_plants": len(plants) >= int(cfg["min_paired_plants"]),
        "minimum_flowers_per_treatment": all(len(groups[t]) >= min_group_n for t in TREATMENTS),
        "supplementation_increases_pollen": cis["pollen_grains_delta"][0] >= float(cfg["min_pollen_grain_delta"]),
        "supplementation_changes_pollination_weight": cis["initial_seed_set_delta"][0] >= float(cfg["min_initial_seed_set_delta"]),
        "early_predator_attack_stable": cis["early_predator_attack_abs_difference"][1] <= float(cfg["max_early_predator_attack_difference"]),
        "realized_z_stable": cis["z_relative_difference"][1] <= float(cfg["max_z_relative_change"]),
        "bract_height_stable": cis["bract_height_relative_difference"][1] <= float(cfg["max_bract_height_relative_change"]),
        "corolla_opening_stable": cis["opening_width_relative_difference"][1] <= float(cfg["max_opening_width_relative_change"]),
        "water_depth_stable": cis["water_depth_abs_difference"][1] <= float(cfg["max_water_depth_change"]),
        "mechanical_damage_low": cis["maximum_mechanical_damage_rate"][1] <= float(cfg["max_mechanical_damage_rate"]),
    }
    status = "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED" if all(gates.values()) else "PEDICULARIS_POLLINATION_WEIGHT_NOT_VALIDATED"

    return {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "analysis": "pedicularis_pollination_weight_supplementation_pilot",
        "population_id": population_id,
        "season_id": season_id,
        "n_rows": len(rows),
        "n_paired_plants": len(plants),
        "n_by_treatment": {t: len(groups[t]) for t in TREATMENTS},
        "observed_estimands": observed,
        "bootstrap_95_ci": cis,
        "descriptive_downstream_outcomes": {
            "initial_seed_set_by_treatment": {t: mean(_initial_seed_set(r) for r in groups[t]) for t in TREATMENTS},
            "final_seed_set_by_treatment": {t: mean(_final_seed_set(r) for r in groups[t]) for t in TREATMENTS},
            "predation_fraction_by_treatment": {t: mean(_predation_fraction(r) for r in groups[t]) for t in TREATMENTS},
            "warning": "later predation fraction is descriptive here and is not the primary selectivity gate because pollen supplementation can change initiated seed number",
        },
        "gates": gates,
        "status": status,
        "claim_ceiling": "pollination_weight_manipulation_only_not_causal_compromise_not_pure_function_optimum_not_dimensional_release",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-closed Pedicularis pollination-weight evaluator")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = _read_csv(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = evaluate(rows, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
