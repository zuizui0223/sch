from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts import analyze_pedicularis_full_surface as surface


EXPECTED_WRAPPER = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
EXPECTED_CORE = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot summarize empty bootstrap distribution")
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    w = pos - lo
    return ordered[lo] * (1 - w) + ordered[hi] * w


def _slope(points: list[tuple[float, float]]) -> float:
    if len(points) < 3:
        raise ValueError("slope requires >=3 observations")
    xbar = mean(x for x, _ in points)
    ybar = mean(y for _, y in points)
    denom = sum((x - xbar) ** 2 for x, _ in points)
    if denom <= 0:
        raise ValueError("slope requires variation in realized z")
    return sum((x - xbar) * (y - ybar) for x, y in points) / denom


def _initial_seed_set(row: dict[str, str]) -> float:
    ovules = float(row["ovule_count"])
    return (
        float(row["undamaged_seed_count"])
        + float(row["damaged_seed_count"])
    ) / ovules


def _state_rows(
    rows: list[dict[str, str]],
    *,
    predator_treatment: str,
) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row["pollination_treatment"] == "NATURAL"
        and row["predator_treatment"] == predator_treatment
    ]


def _metric_slope(
    rows: list[dict[str, str]],
    metric: str,
) -> float:
    points: list[tuple[float, float]] = []
    for row in rows:
        z = float(row["realized_exsertion"])
        if metric == "pollen_grains":
            y = float(row["pollen_grains"])
        elif metric == "initial_seed_set":
            y = _initial_seed_set(row)
        else:
            raise ValueError(f"unknown metric {metric!r}")
        points.append((z, y))
    return _slope(points)


def _cluster_bootstrap_slopes(
    rows: list[dict[str, str]],
    *,
    metric: str,
    reps: int,
    seed: int,
) -> list[float]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clusters[row["plant_id"]].append(row)
    ids = sorted(clusters)
    if len(ids) < 3:
        raise ValueError("diagnostic requires >=3 plant blocks")

    rng = random.Random(seed)
    slopes: list[float] = []
    for _ in range(reps):
        sampled: list[dict[str, str]] = []
        for draw_index, plant_id in enumerate(rng.choices(ids, k=len(ids))):
            # Plant IDs do not enter the slope itself, so duplicated bootstrap
            # clusters can simply contribute their rows again.
            sampled.extend(clusters[plant_id])
        try:
            slopes.append(_metric_slope(sampled, metric))
        except ValueError:
            continue
    return slopes


def _slope_receipt(
    rows: list[dict[str, str]],
    *,
    metric: str,
    reps: int,
    seed: int,
) -> dict:
    observed = _metric_slope(rows, metric)
    boot = _cluster_bootstrap_slopes(
        rows,
        metric=metric,
        reps=reps,
        seed=seed,
    )
    if len(boot) < max(50, int(reps * 0.5)):
        raise ValueError("too few valid plant-cluster bootstrap slopes")
    ci = [_quantile(boot, 0.025), _quantile(boot, 0.975)]
    return {
        "observed_slope": observed,
        "slope_95_ci": ci,
        "positive_with_95_ci": ci[0] > 0,
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
    }


def build(
    rows: list[dict[str, str]],
    surface_receipt: dict,
    config: dict,
) -> dict:
    if surface_receipt.get("system_wrapper_schema_version") != EXPECTED_WRAPPER:
        raise ValueError("requires Pedicularis full-surface wrapper V2")
    if surface_receipt.get("receipt_schema_version") != EXPECTED_CORE:
        raise ValueError("requires SCH causal-compromise state-optima receipt")
    if surface_receipt.get("system") != "Pedicularis rex":
        raise ValueError("surface receipt is not Pedicularis rex")
    if surface_receipt.get("status") != "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE":
        raise ValueError(
            "antagonist-constrained pollination diagnostic requires a positive "
            "causal-compromise surface first"
        )

    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("diagnostic rows must contain one population and season")
    population_id = next(iter(populations))
    season_id = next(iter(seasons))
    if (
        surface_receipt.get("population_id") != population_id
        or surface_receipt.get("season_id") != season_id
    ):
        raise ValueError("raw rows and surface receipt context do not match")

    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >=200")
    seed = int(config.get("random_seed", 20261005))

    excluded = _state_rows(rows, predator_treatment="EXCLUDED")
    exposed = _state_rows(rows, predator_treatment="EXPOSED")
    if not excluded or not exposed:
        raise ValueError("both natural-pollination G states are required")

    diagnostics = {}
    for label, subset, offset in (
        ("P1G0_predator_excluded", excluded, 0),
        ("P1G1_predator_exposed", exposed, 1000003),
    ):
        diagnostics[label] = {
            "pollen_grains_vs_z": _slope_receipt(
                subset,
                metric="pollen_grains",
                reps=reps,
                seed=seed + offset,
            ),
            "initial_seed_set_vs_z": _slope_receipt(
                subset,
                metric="initial_seed_set",
                reps=reps,
                seed=seed + offset + 17,
            ),
        }

    bootstrap = surface_receipt.get("bootstrap", {})
    shift_ci = bootstrap.get("shift_remove_antagonist_95_ci")
    if (
        not isinstance(shift_ci, list)
        or len(shift_ci) != 2
        or not all(isinstance(value, (int, float)) for value in shift_ci)
    ):
        raise ValueError("surface receipt lacks shift_remove_antagonist_95_ci")

    observed = surface_receipt.get("observed_estimands", {})
    z_predator_free_state = float(observed["z_pollinator_context"])
    z_combined_state = float(observed["z_combined"])
    observed_shift = float(observed["shift_remove_antagonist"])

    optimum_shift_up = float(shift_ci[0]) > 0
    pollen_positive_both = all(
        diagnostics[state]["pollen_grains_vs_z"]["positive_with_95_ci"]
        for state in diagnostics
    )
    initial_seed_positive_both = all(
        diagnostics[state]["initial_seed_set_vs_z"]["positive_with_95_ci"]
        for state in diagnostics
    )

    pollen_cost_chain = optimum_shift_up and pollen_positive_both
    initial_seed_cost_chain = pollen_cost_chain and initial_seed_positive_both

    if initial_seed_cost_chain:
        status = (
            "CONTEMPORARY_ANTAGONIST_DOWNWARD_STATE_SHIFT_WITH_"
            "POLLEN_AND_INITIAL_SEED_COST_SUPPORTED"
        )
    elif pollen_cost_chain:
        status = (
            "CONTEMPORARY_ANTAGONIST_DOWNWARD_STATE_SHIFT_WITH_"
            "POLLEN_COST_SUPPORTED"
        )
    else:
        status = "CONTEMPORARY_ANTAGONIST_POLLINATION_COST_CHAIN_NOT_RECOVERED"

    return {
        "analysis": "pedicularis_antagonist_constrained_pollination_surface_v1",
        "population_id": population_id,
        "season_id": season_id,
        "surface_status": surface_receipt["status"],
        "z_predator_free_natural_pollination_state_optimum": z_predator_free_state,
        "z_predator_exposed_natural_pollination_state_optimum": z_combined_state,
        "state_optimum_semantics": (
            "reproductive_state_optima_not_pure_function_optima"
        ),
        "pollinator_favored_optimum_identified": False,
        "observed_shift_remove_antagonist": observed_shift,
        "shift_remove_antagonist_95_ci": [
            float(shift_ci[0]),
            float(shift_ci[1]),
        ],
        "predator_removal_shifts_optimum_upward": optimum_shift_up,
        "natural_pollination_secondary_slopes": diagnostics,
        "higher_z_increases_pollen_receipt_in_both_G_states": pollen_positive_both,
        "higher_z_increases_initial_seed_set_in_both_G_states": initial_seed_positive_both,
        "antagonist_shift_away_from_higher_pollen_receipt_supported": pollen_cost_chain,
        "antagonist_shift_away_from_higher_initial_seed_set_supported": (
            initial_seed_cost_chain
        ),
        "antagonist_contribution_to_pollen_limitation_identified": False,
        "adaptive_pollen_limitation_supported": False,
        "evolutionary_maintenance_identified": False,
        "cue_identity_identified": False,
        "status": status,
        "claim_ceiling": [
            "contemporary_state_optimum_shift_plus_randomized_z_pollination_response",
            "predator_free_state_optimum_is_not_a_pure_pollinator_optimum",
            "does_not_show_G_directly_changes_pollen_at_fixed_z",
            "does_not_identify_antagonist_maintenance_of_pollen_limitation",
            "does_not_identify_historical_adaptation",
            "does_not_identify_genetic_response",
            "does_not_identify_predator_cue",
            "does_not_promote_to_adaptive_pollen_limitation",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Diagnose whether predator exposure shifts the P. rex reproductive "
            "state optimum away from trait states with greater pollination performance"
        )
    )
    parser.add_argument("surface_csv", type=Path)
    parser.add_argument("surface_receipt_json", type=Path)
    parser.add_argument("--bootstrap-reps", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=20261005)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = surface.read_rows(args.surface_csv)
    receipt = json.loads(args.surface_receipt_json.read_text(encoding="utf-8"))
    result = build(
        rows,
        receipt,
        {
            "bootstrap_reps": args.bootstrap_reps,
            "random_seed": args.random_seed,
        },
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
