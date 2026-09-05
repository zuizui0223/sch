from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from scripts.analyze_sch_compromise_surface import (
    _cluster_bootstrap_rows,
    _fit_states,
    _quantile,
    read_rows,
)


UPGRADE_SCHEMA_VERSION = "SCH_CONTEXT_STABLE_COMPONENT_OPTIMA_V1"


def _component_optimum(left: dict, right: dict) -> dict:
    a = float(left["a"]) - float(right["a"])
    b = float(left["b"]) - float(right["b"])
    c = float(left["c"]) - float(right["c"])
    z_min = max(float(left["z_min"]), float(right["z_min"]))
    z_max = min(float(left["z_max"]), float(right["z_max"]))
    if z_min >= z_max:
        raise ValueError("component surfaces have no common z support")
    vertex = None
    if c < 0:
        candidate = -b / (2.0 * c)
        if z_min <= candidate <= z_max and math.isfinite(candidate):
            vertex = candidate
    return {
        "a": a,
        "b": b,
        "c": c,
        "z_min": z_min,
        "z_max": z_max,
        "primary_optimum": vertex,
        "optimum_class": "INTERIOR_CONCAVE" if vertex is not None else "NOT_IDENTIFIED_INTERIOR",
    }


def _component_metrics(fits: dict[str, dict]) -> dict:
    poll_g0 = _component_optimum(fits["P1G0"], fits["P0G0"])
    poll_g1 = _component_optimum(fits["P1G1"], fits["P0G1"])
    ant_p0 = _component_optimum(fits["P0G1"], fits["P0G0"])
    ant_p1 = _component_optimum(fits["P1G1"], fits["P1G0"])

    def pair(left: dict, right: dict) -> dict:
        l = left["primary_optimum"]
        r = right["primary_optimum"]
        if l is None or r is None:
            return {
                "both_interior": False,
                "context_difference": None,
                "pooled_optimum": None,
            }
        return {
            "both_interior": True,
            "context_difference": float(l) - float(r),
            "pooled_optimum": (float(l) + float(r)) / 2.0,
        }

    return {
        "pollinator_component_G0": poll_g0,
        "pollinator_component_G1": poll_g1,
        "antagonist_component_P0": ant_p0,
        "antagonist_component_P1": ant_p1,
        "F1_pair": pair(poll_g0, poll_g1),
        "F2_pair": pair(ant_p0, ant_p1),
    }


def identify(rows: list[dict[str, str]], base_receipt: dict, config: dict) -> dict:
    if base_receipt.get("receipt_schema_version") != "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1":
        raise ValueError("base receipt must use SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1")
    if base_receipt.get("status") != "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE":
        raise ValueError("pure-function promotion requires a positive SCH causal-compromise receipt")

    min_levels = int(config.get("min_z_levels", 5))
    if min_levels < 3:
        raise ValueError("min_z_levels must be >= 3")
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    min_valid_fraction = float(config.get("min_valid_bootstrap_fraction", 0.8))
    min_interior_fraction = float(config.get("min_component_interior_bootstrap_fraction", 0.9))
    max_context_difference = float(config["max_context_optimum_difference"])
    if max_context_difference < 0:
        raise ValueError("max_context_optimum_difference must be >= 0")

    observed = _component_metrics(_fit_states(rows, min_levels))
    rng = random.Random(int(config.get("random_seed", 20260904)))
    boot: list[dict] = []
    for _ in range(reps):
        sample = _cluster_bootstrap_rows(rows, rng)
        try:
            metrics = _component_metrics(_fit_states(sample, min_levels))
        except ValueError:
            continue
        boot.append(metrics)

    if len(boot) < max(50, int(reps * min_valid_fraction)):
        raise ValueError("too few valid bootstrap replicates for component-optimum identification")

    def summarize(pair_name: str) -> dict:
        valid = [item[pair_name] for item in boot if item[pair_name]["both_interior"]]
        interior_fraction = len(valid) / len(boot)
        if valid:
            abs_diffs = [abs(float(item["context_difference"])) for item in valid]
            pooled = [float(item["pooled_optimum"]) for item in valid]
            abs_diff_97_5 = _quantile(abs_diffs, 0.975)
            pooled_ci = [_quantile(pooled, 0.025), _quantile(pooled, 0.975)]
        else:
            abs_diff_97_5 = None
            pooled_ci = None
        observed_pair = observed[pair_name]
        passes = (
            observed_pair["both_interior"]
            and interior_fraction >= min_interior_fraction
            and abs_diff_97_5 is not None
            and abs_diff_97_5 <= max_context_difference
        )
        return {
            "observed": observed_pair,
            "interior_bootstrap_fraction": interior_fraction,
            "absolute_context_difference_97_5pct": abs_diff_97_5,
            "pooled_optimum_95_ci": pooled_ci,
            "passes_context_stability": passes,
        }

    f1 = summarize("F1_pair")
    f2 = summarize("F2_pair")
    identified = f1["passes_context_stability"] and f2["passes_context_stability"]

    result = dict(base_receipt)
    result["pure_function_upgrade"] = {
        "schema_version": UPGRADE_SCHEMA_VERSION,
        "component_semantics": {
            "F1_G0": "W10_MINUS_W00_POLLINATOR_MEDIATED_REPRODUCTIVE_CONTRIBUTION",
            "F1_G1": "W11_MINUS_W01_POLLINATOR_MEDIATED_REPRODUCTIVE_CONTRIBUTION",
            "F2_P0": "W01_MINUS_W00_ANTAGONIST_PRESENT_REPRODUCTIVE_CONTRIBUTION_HIGHER_IS_BETTER",
            "F2_P1": "W11_MINUS_W10_ANTAGONIST_PRESENT_REPRODUCTIVE_CONTRIBUTION_HIGHER_IS_BETTER",
        },
        "observed_component_surfaces": {
            key: value for key, value in observed.items() if key not in {"F1_pair", "F2_pair"}
        },
        "F1_context_stability": f1,
        "F2_context_stability": f2,
        "thresholds": {
            "max_context_optimum_difference": max_context_difference,
            "min_component_interior_bootstrap_fraction": min_interior_fraction,
        },
        "status": "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED" if identified else "PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED",
        "claim_ceiling": "pure_function_mapping_requires_selective_interventions_and_context_stable_component_optima",
    }
    if identified:
        result["identified_pure_function_optima"] = {
            "z_F1": float(f1["observed"]["pooled_optimum"]),
            "z_F2": float(f2["observed"]["pooled_optimum"]),
            "semantics": "CONTEXT_STABLE_CAUSAL_COMPONENT_OPTIMA_ON_COMMON_REPRODUCTIVE_SCALE",
            "F1_95_ci": f1["pooled_optimum_95_ci"],
            "F2_95_ci": f2["pooled_optimum_95_ci"],
        }
    else:
        result.pop("identified_pure_function_optima", None)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Identify context-stable SCH component optima")
    parser.add_argument("surface_csv", type=Path)
    parser.add_argument("base_receipt_json", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = read_rows(args.surface_csv)
    base_receipt = json.loads(args.base_receipt_json.read_text(encoding="utf-8"))
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = identify(rows, base_receipt, config)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
