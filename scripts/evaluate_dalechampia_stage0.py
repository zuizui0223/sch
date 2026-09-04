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


POPULATION_REQUIRED = (
    "population_id",
    "season_id",
    "plant_id",
    "blossom_id",
    "bract_area",
    "pollen_grains",
    "seed_predator_present",
    "predated_seed_count",
    "initiated_seed_count",
)

EXPOSURE_REQUIRED = (
    "population_id",
    "season_id",
    "plant_id",
    "blossom_id",
    "exposure_window",
    "bract_area",
    "pollen_grains",
    "resin_amount",
    "predated_seed_count",
    "initiated_seed_count",
)


def _read_csv(path: Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in required if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")
    for i, row in enumerate(rows, start=2):
        for field in required:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
    return rows


def _number(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _predated_fraction(row: dict[str, str]) -> float:
    initiated = _number(row, "initiated_seed_count")
    predated = _number(row, "predated_seed_count")
    if initiated <= 0:
        raise ValueError("initiated_seed_count must be > 0 for Stage-0 evaluation")
    if predated < 0 or predated > initiated:
        raise ValueError("predated_seed_count must be between 0 and initiated_seed_count")
    return predated / initiated


def _corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 3:
        raise ValueError("correlation requires at least three paired observations")
    mx, my = mean(xs), mean(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    sx = math.sqrt(sum(v * v for v in dx))
    sy = math.sqrt(sum(v * v for v in dy))
    if sx == 0 or sy == 0:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / (sx * sy)


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


def _cluster_bootstrap(
    rows: list[dict[str, str]],
    statistic: Callable[[list[dict[str, str]]], float],
    reps: int,
    rng: random.Random,
) -> list[float]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clusters[row["plant_id"]].append(row)
    ids = list(clusters)
    if len(ids) < 2:
        raise ValueError("at least two plant_id clusters are required")
    out: list[float] = []
    for _ in range(reps):
        sampled: list[dict[str, str]] = []
        for cluster_id in rng.choices(ids, k=len(ids)):
            sampled.extend(clusters[cluster_id])
        try:
            out.append(statistic(sampled))
        except ValueError:
            continue
    if len(out) < max(50, reps // 5):
        raise ValueError("too few valid bootstrap replicates")
    return out


def _check_single_context(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one Stage-0 package must contain exactly one population_id and one season_id")
    return next(iter(populations)), next(iter(seasons))


def evaluate_population(rows: list[dict[str, str]], config: dict, rng: random.Random) -> dict:
    population_id, season_id = _check_single_context(rows)
    cfg = config["population"]
    reps = int(config["bootstrap_reps"])

    def poll_stat(sample: list[dict[str, str]]) -> float:
        return _corr(
            [_number(row, "bract_area") for row in sample],
            [_number(row, "pollen_grains") for row in sample],
        )

    def pred_stat(sample: list[dict[str, str]]) -> float:
        return _corr(
            [_number(row, "bract_area") for row in sample],
            [_predated_fraction(row) for row in sample],
        )

    poll = poll_stat(rows)
    pred = pred_stat(rows)
    poll_boot = _cluster_bootstrap(rows, poll_stat, reps, rng)
    pred_boot = _cluster_bootstrap(rows, pred_stat, reps, rng)
    incidence = mean(_number(row, "seed_predator_present") for row in rows)
    n_plants = len({row["plant_id"] for row in rows})

    poll_ci = [_quantile(poll_boot, 0.025), _quantile(poll_boot, 0.975)]
    pred_ci = [_quantile(pred_boot, 0.025), _quantile(pred_boot, 0.975)]

    gates = {
        "minimum_blossoms": len(rows) >= int(cfg["min_blossoms"]),
        "minimum_plants": n_plants >= int(cfg["min_plants"]),
        "predator_incidence": incidence >= float(cfg["min_predator_incidence"]),
        "positive_pollination_tracking": poll_ci[0] >= float(cfg["min_positive_correlation"]),
        "positive_predation_tracking": pred_ci[0] >= float(cfg["min_positive_correlation"]),
    }
    qualified = all(gates.values())
    return {
        "analysis": "population_screen",
        "population_id": population_id,
        "season_id": season_id,
        "n_blossoms": len(rows),
        "n_plants": n_plants,
        "predator_incidence": incidence,
        "bract_pollen_correlation": poll,
        "bract_pollen_bootstrap_95_ci": poll_ci,
        "bract_predation_correlation": pred,
        "bract_predation_bootstrap_95_ci": pred_ci,
        "gates": gates,
        "status": "QUALIFIED_CONFLICT_ACTIVE_CANDIDATE" if qualified else "NOT_QUALIFIED_CONFLICT_ACTIVE_CANDIDATE",
        "claim_ceiling": "stage0_screen_only_not_causal_compromise_or_optimum_identification",
    }


def _relative_change(a: float, b: float) -> float:
    scale = max(abs(b), 1e-12)
    return abs(a - b) / scale


def _plant_window_summary(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, float]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["plant_id"], row["exposure_window"])].append(row)

    summaries: dict[tuple[str, str], dict[str, float]] = {}
    for key, group in grouped.items():
        summaries[key] = {
            "damage": mean(_predated_fraction(row) for row in group),
            "pollen": mean(_number(row, "pollen_grains") for row in group),
            "z": mean(_number(row, "bract_area") for row in group),
            "resin": mean(_number(row, "resin_amount") for row in group),
        }
    return summaries


def _paired_exposure_metrics(rows: list[dict[str, str]], window: str) -> list[dict[str, float]]:
    summaries = _plant_window_summary(rows)
    plant_ids = sorted({plant_id for plant_id, _ in summaries})
    paired: list[dict[str, float]] = []
    for plant_id in plant_ids:
        control = summaries.get((plant_id, "E0"))
        treatment = summaries.get((plant_id, window))
        if control is None or treatment is None:
            continue
        paired.append(
            {
                "damage_delta": treatment["damage"] - control["damage"],
                "pollen_rel": _relative_change(treatment["pollen"], control["pollen"]),
                "z_rel": _relative_change(treatment["z"], control["z"]),
                "resin_rel": _relative_change(treatment["resin"], control["resin"]),
            }
        )
    return paired


def _paired_bootstrap(
    paired: list[dict[str, float]], metric: str, reps: int, rng: random.Random
) -> list[float]:
    if len(paired) < 2:
        raise ValueError("paired exposure analysis requires at least two complete plants")
    values: list[float] = []
    for _ in range(reps):
        sampled = rng.choices(paired, k=len(paired))
        values.append(mean(item[metric] for item in sampled))
    return values


def evaluate_exposure(rows: list[dict[str, str]], config: dict, rng: random.Random) -> dict:
    population_id, season_id = _check_single_context(rows)
    cfg = config["exposure"]
    reps = int(config["bootstrap_reps"])
    windows = sorted({row["exposure_window"] for row in rows})
    if "E0" not in windows:
        raise ValueError("exposure package requires E0 no-exposure control")

    min_complete_plants = int(cfg.get("min_complete_plants", cfg.get("min_group_n", 0)))
    if min_complete_plants < 2:
        raise ValueError("exposure config requires min_complete_plants >= 2")

    candidates = []
    for window in (window for window in windows if window != "E0"):
        paired = _paired_exposure_metrics(rows, window)
        if len(paired) < 2:
            candidates.append(
                {
                    "window": window,
                    "n_complete_plants": len(paired),
                    "passes": False,
                    "gates": {"minimum_complete_plants": False},
                    "reason": "too_few_complete_E0_window_plant_pairs",
                }
            )
            continue

        observed = {
            metric: mean(item[metric] for item in paired)
            for metric in ("damage_delta", "pollen_rel", "z_rel", "resin_rel")
        }
        boot = {
            metric: _paired_bootstrap(paired, metric, reps, rng)
            for metric in ("damage_delta", "pollen_rel", "z_rel", "resin_rel")
        }

        gates = {
            "minimum_complete_plants": len(paired) >= min_complete_plants,
            "damage_increase": _quantile(boot["damage_delta"], 0.025)
            >= float(cfg["min_damage_fraction_delta"]),
            "pollination_selectivity": _quantile(boot["pollen_rel"], 0.975)
            <= float(cfg["max_pollen_relative_change"]),
            "z_stability": _quantile(boot["z_rel"], 0.975)
            <= float(cfg["max_z_relative_change"]),
            "resin_stability": _quantile(boot["resin_rel"], 0.975)
            <= float(cfg["max_resin_relative_change"]),
        }
        candidates.append(
            {
                "window": window,
                "n_complete_plants": len(paired),
                "damage_fraction_delta": observed["damage_delta"],
                "damage_delta_bootstrap_95_ci": [
                    _quantile(boot["damage_delta"], 0.025),
                    _quantile(boot["damage_delta"], 0.975),
                ],
                "pollen_relative_change": observed["pollen_rel"],
                "pollen_relative_change_97_5pct": _quantile(boot["pollen_rel"], 0.975),
                "z_relative_change": observed["z_rel"],
                "z_relative_change_97_5pct": _quantile(boot["z_rel"], 0.975),
                "resin_relative_change": observed["resin_rel"],
                "resin_relative_change_97_5pct": _quantile(boot["resin_rel"], 0.975),
                "gates": gates,
                "passes": all(gates.values()),
            }
        )

    passing = [candidate for candidate in candidates if candidate["passes"]]
    selected = max(passing, key=lambda item: item["damage_fraction_delta"], default=None)
    return {
        "analysis": "controlled_weevil_exposure",
        "population_id": population_id,
        "season_id": season_id,
        "design": "within_plant_E0_vs_window_paired_contrasts",
        "candidate_windows": candidates,
        "selected_g1_window": selected["window"] if selected else None,
        "status": "SELECTIVE_G_WINDOW_CANDIDATE" if selected else "NO_SELECTIVE_G_WINDOW_RECOVERED",
        "claim_ceiling": "stage0_selectivity_only_not_direct_oviposition_unless_eggs_or_scars_are_independently_observed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail-closed Dalechampia Stage-0 evaluator")
    parser.add_argument("mode", choices=("population", "exposure"))
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    rng = random.Random(int(config.get("random_seed", 20260904)))

    if args.mode == "population":
        rows = _read_csv(args.csv_path, POPULATION_REQUIRED)
        result = evaluate_population(rows, config, rng)
    else:
        rows = _read_csv(args.csv_path, EXPOSURE_REQUIRED)
        result = evaluate_exposure(rows, config, rng)

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
