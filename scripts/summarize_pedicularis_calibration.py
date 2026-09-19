"""Summarize independent Pedicularis calibration data without choosing thresholds.

The output is deliberately descriptive. It provides measurement/sham change
scales, plant-level baseline variation, and natural-history timing distributions
that may later justify a prospectively frozen threshold manifest. It never emits
Qz/Qp/Qg pass/fail labels or recommended cutoffs.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev


SCHEMA = "SCH_PEDICULARIS_CALIBRATION_SUMMARY_V1"
ARMS = {"BASELINE_REPEAT", "Z_SHAM_TAPE", "P_SHAM_HANDLING", "G_SHAM_DEVICE"}
EVENTS = {
    "ANTHESIS_START",
    "POLLINATION_WINDOW_COMPLETE",
    "FIRST_PREDATOR_ATTACK",
    "OVARY_SWELLING_START",
    "COROLLA_SENESCENCE",
}

C1_REQUIRED = (
    "population_id", "season_id", "calibration_dataset_id", "plant_id", "flower_id",
    "calibration_arm", "measurement_round", "observer_id", "hours_since_baseline",
    "flower_length_mm", "realized_exsertion", "corolla_opening_width_mm", "tube_diameter_mm",
    "bract_height_mm", "lower_lip_angle_deg", "flower_orientation_deg", "mechanical_damage",
)
C2_REQUIRED = (
    "population_id", "season_id", "calibration_dataset_id", "plant_id", "flower_id",
    "calibration_arm", "timepoint_id", "hours_since_baseline", "water_depth_mm", "bract_height_mm",
    "rainfall_since_last_mm", "external_water_added", "mechanical_damage",
)
C3_REQUIRED = (
    "population_id", "season_id", "calibration_dataset_id", "plant_id", "flower_id",
    "observation_block", "pollinator_observation_minutes", "pollinator_visits", "pollen_grains",
    "ovule_count", "initial_seed_count", "undamaged_seed_count", "damaged_seed_count",
    "early_predator_attack_present", "mechanical_damage",
)
C4_REQUIRED = (
    "population_id", "season_id", "calibration_dataset_id", "plant_id", "flower_id",
    "event_type", "event_time_iso", "anthesis_time_iso", "hours_from_anthesis", "observer_id",
)

C1_RELATIVE = (
    "flower_length_mm", "realized_exsertion", "corolla_opening_width_mm", "tube_diameter_mm", "bract_height_mm",
)
C1_ABSOLUTE = ("lower_lip_angle_deg", "flower_orientation_deg")


def _read(path: Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: missing header")
        missing = [field for field in required if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path}: missing columns {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path}: no calibration rows")
    for line, row in enumerate(rows, start=2):
        for field in required:
            if row.get(field, "").strip() == "":
                raise ValueError(f"{path}: blank {field} on line {line}")
    return rows


def _num(row: dict[str, str], field: str) -> float:
    try:
        out = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid {field}: {row.get(field)!r}") from exc
    if not math.isfinite(out):
        raise ValueError(f"non-finite {field}")
    return out


def _binary(row: dict[str, str], field: str) -> int:
    raw = row[field].strip()
    if raw not in {"0", "1"}:
        raise ValueError(f"{field} must be 0/1")
    return int(raw)


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("empty quantile input")
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    w = pos - lo
    return values[lo] * (1 - w) + values[hi] * w


def _distribution(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "mean": mean(values),
        "sd_population": pstdev(values) if len(values) > 1 else 0.0,
        "q05": _quantile(values, 0.05),
        "q50": _quantile(values, 0.50),
        "q95": _quantile(values, 0.95),
        "min": min(values),
        "max": max(values),
    }


def _identity(rows: list[dict[str, str]]) -> tuple[str, str, str]:
    populations = {r["population_id"] for r in rows}
    seasons = {r["season_id"] for r in rows}
    datasets = {r["calibration_dataset_id"] for r in rows}
    if len(populations) != 1 or len(seasons) != 1 or len(datasets) != 1:
        raise ValueError("each calibration file must contain one population, season and calibration_dataset_id")
    return next(iter(populations)), next(iter(seasons)), next(iter(datasets))


def _check_shared_identity(blocks: list[list[dict[str, str]]]) -> tuple[str, str, str]:
    identities = [_identity(rows) for rows in blocks]
    if len(set(identities)) != 1:
        raise ValueError(f"C1-C4 identity mismatch: {identities}")
    return identities[0]


def _arm(row: dict[str, str]) -> str:
    value = row["calibration_arm"].strip()
    if value not in ARMS:
        raise ValueError(f"unregistered calibration_arm {value!r}")
    return value


def _baseline_pairs(rows: list[dict[str, str]], order_field: str) -> dict[tuple[str, str], tuple[dict, list[dict]]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["flower_id"], _arm(row))].append(row)
    out = {}
    for key, group in grouped.items():
        ordered = sorted(group, key=lambda r: _num(r, order_field))
        if len(ordered) < 2:
            continue
        out[key] = (ordered[0], ordered[1:])
    return out


def summarize_c1(rows: list[dict[str, str]]) -> dict:
    for row in rows:
        _arm(row)
        _num(row, "measurement_round")
        _num(row, "hours_since_baseline")
        for field in C1_RELATIVE + C1_ABSOLUTE:
            _num(row, field)
        _binary(row, "mechanical_damage")

    pairs = _baseline_pairs(rows, "measurement_round")
    arms: dict[str, dict] = {}
    for arm in sorted(ARMS):
        rel: dict[str, list[float]] = {field: [] for field in C1_RELATIVE}
        absolute: dict[str, list[float]] = {field: [] for field in C1_ABSOLUTE}
        damage: list[float] = []
        elapsed: list[float] = []
        n_flowers = 0
        for (flower_id, pair_arm), (base, followups) in pairs.items():
            if pair_arm != arm:
                continue
            n_flowers += 1
            for follow in followups:
                elapsed.append(_num(follow, "hours_since_baseline"))
                for field in C1_RELATIVE:
                    b = _num(base, field)
                    f = _num(follow, field)
                    rel[field].append(abs(f - b) / max(abs(b), 1e-12))
                for field in C1_ABSOLUTE:
                    absolute[field].append(abs(_num(follow, field) - _num(base, field)))
                damage.append(float(_binary(follow, "mechanical_damage")))
        arms[arm] = {
            "n_flowers_with_repeat": n_flowers,
            "hours_since_baseline": _distribution(elapsed),
            "relative_abs_change": {field: _distribution(vals) for field, vals in rel.items()},
            "absolute_change": {field: _distribution(vals) for field, vals in absolute.items()},
            "damage_rate_observations": _distribution(damage),
        }
    return {"n_rows": len(rows), "arms": arms}


def summarize_c2(rows: list[dict[str, str]]) -> dict:
    for row in rows:
        _arm(row)
        for field in ("hours_since_baseline", "water_depth_mm", "bract_height_mm", "rainfall_since_last_mm"):
            _num(row, field)
        _binary(row, "external_water_added")
        _binary(row, "mechanical_damage")

    pairs = _baseline_pairs(rows, "hours_since_baseline")
    arms: dict[str, dict] = {}
    for arm in sorted(ARMS):
        water_abs: list[float] = []
        water_relative: list[float] = []
        elapsed: list[float] = []
        rainfall: list[float] = []
        n_flowers = 0
        for (_, pair_arm), (base, followups) in pairs.items():
            if pair_arm != arm:
                continue
            n_flowers += 1
            b = _num(base, "water_depth_mm")
            for follow in followups:
                f = _num(follow, "water_depth_mm")
                water_abs.append(abs(f - b))
                water_relative.append(abs(f - b) / max(abs(b), 1e-12))
                elapsed.append(_num(follow, "hours_since_baseline"))
                rainfall.append(_num(follow, "rainfall_since_last_mm"))
        arms[arm] = {
            "n_flowers_with_repeat": n_flowers,
            "water_depth_abs_change_mm": _distribution(water_abs),
            "water_depth_relative_abs_change": _distribution(water_relative),
            "hours_since_baseline": _distribution(elapsed),
            "rainfall_since_last_mm": _distribution(rainfall),
        }
    return {"n_rows": len(rows), "arms": arms}


def summarize_c3(rows: list[dict[str, str]]) -> dict:
    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen_flowers: set[str] = set()
    for row in rows:
        if row["flower_id"] in seen_flowers:
            raise ValueError(f"C3 duplicate flower_id {row['flower_id']!r}")
        seen_flowers.add(row["flower_id"])
        for field in (
            "pollinator_observation_minutes", "pollinator_visits", "pollen_grains", "ovule_count",
            "initial_seed_count", "undamaged_seed_count", "damaged_seed_count",
        ):
            _num(row, field)
        _binary(row, "early_predator_attack_present")
        _binary(row, "mechanical_damage")
        if _num(row, "ovule_count") <= 0:
            raise ValueError("C3 ovule_count must be >0")
        by_plant[row["plant_id"]].append(row)

    metrics: dict[str, list[float]] = defaultdict(list)
    flowers_per_plant = []
    for plant, group in by_plant.items():
        flowers_per_plant.append(float(len(group)))
        per_flower: dict[str, list[float]] = defaultdict(list)
        for row in group:
            ovules = _num(row, "ovule_count")
            undamaged = _num(row, "undamaged_seed_count")
            damaged = _num(row, "damaged_seed_count")
            initiated = _num(row, "initial_seed_count")
            if min(undamaged, damaged, initiated) < 0:
                raise ValueError("C3 seed counts must be non-negative")
            if undamaged + damaged > ovules or initiated > ovules:
                raise ValueError("C3 seed counts cannot exceed ovules")
            mature_initiated = undamaged + damaged
            per_flower["pollinator_visits_per_30min"].append(
                _num(row, "pollinator_visits") / _num(row, "pollinator_observation_minutes") * 30.0
            )
            per_flower["pollen_grains"].append(_num(row, "pollen_grains"))
            per_flower["initial_seed_set_early"].append(initiated / ovules)
            per_flower["initial_seed_set_mature_reconstruction"].append(mature_initiated / ovules)
            per_flower["final_intact_seed_set"].append(undamaged / ovules)
            per_flower["predation_fraction"].append(0.0 if mature_initiated <= 0 else damaged / mature_initiated)
            per_flower["early_attack"].append(float(_binary(row, "early_predator_attack_present")))
            per_flower["mechanical_damage"].append(float(_binary(row, "mechanical_damage")))
        for metric, values in per_flower.items():
            metrics[metric].append(mean(values))

    return {
        "n_rows": len(rows),
        "n_plants": len(by_plant),
        "flowers_per_plant": _distribution(flowers_per_plant),
        "plant_level_distributions": {metric: _distribution(values) for metric, values in sorted(metrics.items())},
        "note": "plant-level summaries are calibration variance inputs only; they are not Qp/Qg effect estimates",
    }


def summarize_c4(rows: list[dict[str, str]]) -> dict:
    event_delays: dict[str, list[float]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        event = row["event_type"].strip()
        if event not in EVENTS:
            raise ValueError(f"unregistered C4 event_type {event!r}")
        key = (row["flower_id"], event)
        if key in seen:
            raise ValueError(f"duplicate C4 flower/event {key}")
        seen.add(key)
        delay = _num(row, "hours_from_anthesis")
        if event == "ANTHESIS_START" and abs(delay) > 1e-9:
            raise ValueError("ANTHESIS_START hours_from_anthesis must be 0")
        if event != "ANTHESIS_START" and delay < 0:
            raise ValueError("post-anthesis event cannot have negative delay")
        event_delays[event].append(delay)
    return {
        "n_rows": len(rows),
        "event_delay_hours": {event: _distribution(event_delays.get(event, [])) for event in sorted(EVENTS)},
        "note": "timing distributions do not automatically define the Qg barrier window",
    }


def summarize(c1: list[dict[str, str]], c2: list[dict[str, str]], c3: list[dict[str, str]], c4: list[dict[str, str]], qualification_ids: list[str]) -> dict:
    population, season, calibration_id = _check_shared_identity([c1, c2, c3, c4])
    if calibration_id in {q.strip() for q in qualification_ids if q.strip()}:
        raise ValueError("calibration_dataset_id overlaps a declared qualification dataset id")
    return {
        "receipt_schema_version": SCHEMA,
        "status": "INDEPENDENT_CALIBRATION_SUMMARY_READY",
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "calibration_dataset_id": calibration_id,
        "declared_qualification_dataset_ids": sorted({q for q in qualification_ids if q}),
        "C1_morphology_repeatability": summarize_c1(c1),
        "C2_water_repeatability": summarize_c2(c2),
        "C3_reproductive_consumer_variance": summarize_c3(c3),
        "C4_natural_history_timing": summarize_c4(c4),
        "claim_ceiling": (
            "independent calibration summary only; no thresholds are selected automatically and no "
            "Qz/Qp/Qg/G1/G2 biological gate is identified"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize independent Pedicularis calibration data")
    parser.add_argument("c1", type=Path)
    parser.add_argument("c2", type=Path)
    parser.add_argument("c3", type=Path)
    parser.add_argument("c4", type=Path)
    parser.add_argument("--qualification-id", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    c1 = _read(args.c1, C1_REQUIRED)
    c2 = _read(args.c2, C2_REQUIRED)
    c3 = _read(args.c3, C3_REQUIRED)
    c4 = _read(args.c4, C4_REQUIRED)
    result = summarize(c1, c2, c3, c4, args.qualification_id)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
