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
    "assigned_z_level",
    "assigned_z_rank",
    "sham_control",
    "realized_exsertion",
    "corolla_opening_width",
    "lower_lip_angle_deg",
    "tube_diameter",
    "bract_height",
    "water_depth",
    "flower_orientation_deg",
    "mechanical_damage",
    "pollinator_visits",
    "pollen_grains",
)

RELATIVE_OFFTARGET_FIELDS = (
    "corolla_opening_width",
    "tube_diameter",
    "bract_height",
)

ABSOLUTE_OFFTARGET_FIELDS = (
    "lower_lip_angle_deg",
    "water_depth",
    "flower_orientation_deg",
)

RECEIPT_SCHEMA_VERSION = "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1"


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
        flower_id = row["flower_id"]
        if flower_id in seen:
            raise ValueError(f"duplicate flower_id {flower_id!r}")
        seen.add(flower_id)
        _rank(row)
        _binary(row, "sham_control")
        _binary(row, "mechanical_damage")
        for field in (
            "realized_exsertion",
            "corolla_opening_width",
            "lower_lip_angle_deg",
            "tube_diameter",
            "bract_height",
            "water_depth",
            "flower_orientation_deg",
            "pollinator_visits",
            "pollen_grains",
        ):
            _number(row, field)
    return rows


def _number(row: dict[str, str], field: str) -> float:
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


def _rank(row: dict[str, str]) -> int:
    raw = row["assigned_z_rank"].strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"assigned_z_rank must be an integer, got {raw!r}") from exc
    return value


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of empty values")
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    weight = pos - lo
    return values[lo] * (1 - weight) + values[hi] * weight


def _check_single_context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one Stage-P0 package must contain exactly one population_id and one season_id")
    return next(iter(populations)), next(iter(seasons))


def _group_by_rank(rows: list[dict[str, str]]) -> dict[int, list[dict[str, str]]]:
    groups: dict[int, list[dict[str, str]]] = defaultdict(list)
    labels: dict[int, set[str]] = defaultdict(set)
    for row in rows:
        rank = _rank(row)
        groups[rank].append(row)
        labels[rank].add(row["assigned_z_level"])
    if any(len(values) != 1 for values in labels.values()):
        raise ValueError("each assigned_z_rank must map to exactly one assigned_z_level")
    return dict(sorted(groups.items()))


def _mean_field(rows: list[dict[str, str]], field: str) -> float:
    return mean(_number(row, field) for row in rows)


def _damage_rate(rows: list[dict[str, str]]) -> float:
    return mean(_binary(row, "mechanical_damage") for row in rows)


def _sham_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    sham = [row for row in rows if _binary(row, "sham_control") == 1]
    sham_ranks = {_rank(row) for row in sham}
    if not sham:
        raise ValueError("at least one sham_control=1 row is required")
    if len(sham_ranks) != 1:
        raise ValueError("sham_control must occupy exactly one assigned_z_rank")
    return sham


def _relative_difference(value: float, reference: float) -> float:
    scale = max(abs(reference), 1e-12)
    return abs(value - reference) / scale


def _rank_metrics(rows: list[dict[str, str]]) -> dict:
    groups = _group_by_rank(rows)
    ranks = list(groups)
    means = {rank: _mean_field(group, "realized_exsertion") for rank, group in groups.items()}
    gaps = [means[right] - means[left] for left, right in zip(ranks, ranks[1:])]
    return {
        "ranks": ranks,
        "means": means,
        "adjacent_gaps": gaps,
        "minimum_adjacent_gap": min(gaps) if gaps else 0.0,
        "strictly_ordered": all(gap > 0 for gap in gaps),
    }


def _offtarget_metrics(rows: list[dict[str, str]]) -> dict:
    groups = _group_by_rank(rows)
    sham = _sham_rows(rows)
    sham_means = {field: _mean_field(sham, field) for field in RELATIVE_OFFTARGET_FIELDS + ABSOLUTE_OFFTARGET_FIELDS}

    relative = {}
    for field in RELATIVE_OFFTARGET_FIELDS:
        diffs = {
            str(rank): _relative_difference(_mean_field(group, field), sham_means[field])
            for rank, group in groups.items()
        }
        relative[field] = {
            "by_rank": diffs,
            "maximum": max(diffs.values()),
        }

    absolute = {}
    for field in ABSOLUTE_OFFTARGET_FIELDS:
        diffs = {
            str(rank): abs(_mean_field(group, field) - sham_means[field])
            for rank, group in groups.items()
        }
        absolute[field] = {
            "by_rank": diffs,
            "maximum": max(diffs.values()),
        }

    damage = {str(rank): _damage_rate(group) for rank, group in groups.items()}
    return {
        "relative": relative,
        "absolute": absolute,
        "damage_rate_by_rank": damage,
        "maximum_damage_rate": max(damage.values()),
        "sham_rank": _rank(sham[0]),
    }


def _cluster_bootstrap(rows: list[dict[str, str]], statistic: Callable[[list[dict[str, str]]], float], reps: int, rng: random.Random) -> list[float]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clusters[row["plant_id"]].append(row)
    ids = list(clusters)
    if len(ids) < 2:
        raise ValueError("at least two plant_id clusters are required")
    values: list[float] = []
    for _ in range(reps):
        sampled: list[dict[str, str]] = []
        for plant_id in rng.choices(ids, k=len(ids)):
            sampled.extend(clusters[plant_id])
        try:
            values.append(statistic(sampled))
        except ValueError:
            continue
    if len(values) < max(50, reps // 5):
        raise ValueError("too few valid bootstrap replicates")
    return values


def _minimum_adjacent_gap(rows: list[dict[str, str]]) -> float:
    metrics = _rank_metrics(rows)
    if len(metrics["ranks"]) < 2:
        raise ValueError("at least two z ranks are required")
    return float(metrics["minimum_adjacent_gap"])


def _relative_field_max(rows: list[dict[str, str]], field: str) -> float:
    return float(_offtarget_metrics(rows)["relative"][field]["maximum"])


def _absolute_field_max(rows: list[dict[str, str]], field: str) -> float:
    return float(_offtarget_metrics(rows)["absolute"][field]["maximum"])


def _maximum_damage(rows: list[dict[str, str]]) -> float:
    return float(_offtarget_metrics(rows)["maximum_damage_rate"])


def evaluate(rows: list[dict[str, str]], config: dict) -> dict:
    population_id, season_id = _check_single_context(rows)
    groups = _group_by_rank(rows)
    sham = _sham_rows(rows)
    cfg = config["stage_p0"]
    reps = int(config["bootstrap_reps"])
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    rng = random.Random(int(config.get("random_seed", 20260904)))

    n_plants = len({row["plant_id"] for row in rows})
    rank_metrics = _rank_metrics(rows)
    off = _offtarget_metrics(rows)

    gap_boot = _cluster_bootstrap(rows, _minimum_adjacent_gap, reps, rng)
    gap_ci = [_quantile(gap_boot, 0.025), _quantile(gap_boot, 0.975)]

    relative_ci: dict[str, list[float]] = {}
    for field in RELATIVE_OFFTARGET_FIELDS:
        vals = _cluster_bootstrap(rows, lambda sample, f=field: _relative_field_max(sample, f), reps, rng)
        relative_ci[field] = [_quantile(vals, 0.025), _quantile(vals, 0.975)]

    absolute_ci: dict[str, list[float]] = {}
    for field in ABSOLUTE_OFFTARGET_FIELDS:
        vals = _cluster_bootstrap(rows, lambda sample, f=field: _absolute_field_max(sample, f), reps, rng)
        absolute_ci[field] = [_quantile(vals, 0.025), _quantile(vals, 0.975)]

    damage_boot = _cluster_bootstrap(rows, _maximum_damage, reps, rng)
    damage_ci = [_quantile(damage_boot, 0.025), _quantile(damage_boot, 0.975)]

    min_group_n = int(cfg["min_flowers_per_level"])
    min_plants = int(cfg["min_plants"])
    min_levels = int(cfg["min_z_levels"])
    min_gap = float(cfg["min_adjacent_exsertion_gap"])

    gates = {
        "minimum_z_levels": len(groups) >= min_levels,
        "minimum_flowers_per_level": all(len(group) >= min_group_n for group in groups.values()),
        "minimum_plants": n_plants >= min_plants,
        "realized_z_ordered": bool(rank_metrics["strictly_ordered"]),
        "realized_z_separation": gap_ci[0] >= min_gap,
        "opening_width_stable": relative_ci["corolla_opening_width"][1] <= float(cfg["max_opening_width_relative_change"]),
        "tube_diameter_stable": relative_ci["tube_diameter"][1] <= float(cfg["max_tube_diameter_relative_change"]),
        "bract_height_stable": relative_ci["bract_height"][1] <= float(cfg["max_bract_height_relative_change"]),
        "lower_lip_angle_stable": absolute_ci["lower_lip_angle_deg"][1] <= float(cfg["max_lower_lip_angle_change_deg"]),
        "water_depth_stable": absolute_ci["water_depth"][1] <= float(cfg["max_water_depth_change"]),
        "flower_orientation_stable": absolute_ci["flower_orientation_deg"][1] <= float(cfg["max_flower_orientation_change_deg"]),
        "mechanical_damage_low": damage_ci[1] <= float(cfg["max_mechanical_damage_rate"]),
    }

    status = "PEDICULARIS_Z_MANIPULATION_VALIDATED" if all(gates.values()) else "PEDICULARIS_Z_MANIPULATION_NOT_VALIDATED"

    return {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "analysis": "pedicularis_stage_p0_exsertion_manipulation",
        "population_id": population_id,
        "season_id": season_id,
        "n_rows": len(rows),
        "n_plants": n_plants,
        "z_levels": [groups[rank][0]["assigned_z_level"] for rank in groups],
        "sham_rank": _rank(sham[0]),
        "realized_exsertion": {
            "mean_by_rank": {str(k): v for k, v in rank_metrics["means"].items()},
            "adjacent_gaps": rank_metrics["adjacent_gaps"],
            "minimum_adjacent_gap_bootstrap_95_ci": gap_ci,
        },
        "off_target_observed": off,
        "off_target_bootstrap_95_ci": {
            "relative_maximum_by_field": relative_ci,
            "absolute_maximum_by_field": absolute_ci,
            "maximum_damage_rate": damage_ci,
        },
        "descriptive_functional_checks": {
            "pollinator_visits_mean_by_rank": {str(rank): _mean_field(group, "pollinator_visits") for rank, group in groups.items()},
            "pollen_grains_mean_by_rank": {str(rank): _mean_field(group, "pollen_grains") for rank, group in groups.items()},
            "interpretation": "descriptive only at Stage P0; pollination responses are not required to remain equal because z is intended to alter the pollination-facing function",
        },
        "gates": gates,
        "status": status,
        "claim_ceiling": "manipulation_validity_only_not_functional_conflict_not_causal_compromise_not_dimensional_release",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-closed Pedicularis Stage-P0 exsertion-manipulation evaluator")
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
