"""Estimate the shared-axis conflict budget on the SCH reproductive component scale.

For a positive SCH z x P x G experiment with context-stable component optima,
define averaged causal component curves

F1_bar = 0.5 * [(W10-W00) + (W11-W01)]
F2_bar = 0.5 * [(W01-W00) + (W11-W10)].

Their sum is exactly W11-W00 coefficient-wise. The conflict budget is

max_z F1_bar + max_z F2_bar - max_z (F1_bar+F2_bar),

which is the amount of focal biotic reproductive contribution lost because the
two components are forced to share one z coordinate. It is a fitness-scale
analogue of L_S* for the identified component system, not a total architecture
cost and not a historical claim.
"""

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


RECEIPT_SCHEMA_VERSION = "SCH_COMPONENT_CONFLICT_BUDGET_V1"


def _coeffs(surface: dict) -> tuple[float, float, float]:
    return (float(surface["a"]), float(surface["b"]), float(surface["c"]))


def _sub(left: dict, right: dict) -> tuple[float, float, float]:
    a1, b1, c1 = _coeffs(left)
    a0, b0, c0 = _coeffs(right)
    return (a1 - a0, b1 - b0, c1 - c0)


def _avg(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple((a + b) / 2.0 for a, b in zip(left, right))  # type: ignore[return-value]


def _add(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def _value(coeffs: tuple[float, float, float], z: float) -> float:
    a, b, c = coeffs
    return a + b * z + c * z * z


def _curve_max(coeffs: tuple[float, float, float], z_min: float, z_max: float) -> dict:
    a, b, c = coeffs
    if not all(math.isfinite(value) for value in (a, b, c, z_min, z_max)):
        raise ValueError("non-finite curve input")
    if z_min >= z_max:
        raise ValueError("invalid common support")
    if c >= 0:
        raise ValueError("component curve is not concave")
    z_star = -b / (2.0 * c)
    if not (z_min <= z_star <= z_max):
        raise ValueError("component optimum is outside common support")
    return {"z_optimum": z_star, "maximum": _value(coeffs, z_star)}


def _metrics(fits: dict[str, dict]) -> dict:
    supports = [(float(surface["z_min"]), float(surface["z_max"])) for surface in fits.values()]
    z_min = max(item[0] for item in supports)
    z_max = min(item[1] for item in supports)
    if z_min >= z_max:
        raise ValueError("state surfaces have no common z support")

    f1_g0 = _sub(fits["P1G0"], fits["P0G0"])
    f1_g1 = _sub(fits["P1G1"], fits["P0G1"])
    f2_p0 = _sub(fits["P0G1"], fits["P0G0"])
    f2_p1 = _sub(fits["P1G1"], fits["P1G0"])

    f1_bar = _avg(f1_g0, f1_g1)
    f2_bar = _avg(f2_p0, f2_p1)
    shared = _add(f1_bar, f2_bar)
    observed_combined_minus_baseline = _sub(fits["P1G1"], fits["P0G0"])

    identity_error = max(
        abs(a - b) for a, b in zip(shared, observed_combined_minus_baseline)
    )
    if identity_error > 1e-9:
        raise ValueError("averaged component identity W11-W00 failed")

    f1_max = _curve_max(f1_bar, z_min, z_max)
    f2_max = _curve_max(f2_bar, z_min, z_max)
    shared_max = _curve_max(shared, z_min, z_max)
    conflict = f1_max["maximum"] + f2_max["maximum"] - shared_max["maximum"]
    if conflict < -1e-8:
        raise ValueError("negative conflict budget violates max-sum inequality")
    conflict = max(0.0, conflict)

    return {
        "common_support": [z_min, z_max],
        "F1_bar_coefficients": list(f1_bar),
        "F2_bar_coefficients": list(f2_bar),
        "shared_component_coefficients": list(shared),
        "component_identity_max_abs_error": identity_error,
        "F1_separate_optimum": f1_max,
        "F2_separate_optimum": f2_max,
        "shared_component_optimum": shared_max,
        "component_conflict_load": conflict,
        "separate_component_ceiling": f1_max["maximum"] + f2_max["maximum"],
        "shared_component_maximum": shared_max["maximum"],
    }


def estimate(rows: list[dict[str, str]], upgraded_receipt: dict, config: dict) -> dict:
    upgrade = upgraded_receipt.get("pure_function_upgrade", {})
    if upgrade.get("status") != "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED":
        raise ValueError("conflict-budget estimation requires context-stable component optima")
    if "identified_pure_function_optima" not in upgraded_receipt:
        raise ValueError("upgraded receipt lacks identified_pure_function_optima")

    fitness_scale_id = str(config.get("fitness_scale_id", "")).strip()
    if not fitness_scale_id or fitness_scale_id == "REQUIRED_BEFORE_USE":
        raise ValueError("fitness_scale_id must be frozen before use")
    min_levels = int(config.get("min_z_levels", 5))
    if min_levels < 3:
        raise ValueError("min_z_levels must be >= 3")
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    min_valid = float(config.get("min_valid_bootstrap_fraction", 0.8))
    if not 0 < min_valid <= 1:
        raise ValueError("min_valid_bootstrap_fraction must be in (0,1]")

    observed = _metrics(_fit_states(rows, min_levels))
    rng = random.Random(int(config.get("random_seed", 20260905)))
    boot: list[float] = []
    for _ in range(reps):
        sample = _cluster_bootstrap_rows(rows, rng)
        try:
            metric = _metrics(_fit_states(sample, min_levels))
        except ValueError:
            continue
        boot.append(float(metric["component_conflict_load"]))

    if len(boot) < max(50, int(reps * min_valid)):
        raise ValueError("too few valid bootstrap replicates for conflict budget")

    ci = [_quantile(boot, 0.025), _quantile(boot, 0.975)]
    return {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED",
        "fitness_scale_id": fitness_scale_id,
        "source_sch_receipt_schema": upgraded_receipt.get("receipt_schema_version"),
        "source_pure_function_upgrade_schema": upgrade.get("schema_version"),
        "observed_estimands": observed,
        "bootstrap": {
            "requested_reps": reps,
            "valid_reps": len(boot),
            "component_conflict_load_95_ci": ci,
        },
        "criticality_export": {
            "L_S_component": observed["component_conflict_load"],
            "L_S_component_95_ci": ci,
            "semantics": (
                "fitness-scale focal-component conflict budget: separate maxima minus best shared-z maximum; "
                "direct/background W00 excluded"
            ),
        },
        "architecture_boundary_status": (
            "READY_FOR_BITA_PROJECTION_ONLY_AFTER_s_AND_K_ARE_ESTIMATED_ON_COMPATIBLE_SCALE"
        ),
        "claim_ceiling": (
            "identified contemporary focal-component conflict budget; not total fitness architecture cost, "
            "not proof of differentiation, not historical modularization"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate SCH fitness-scale shared conflict budget")
    parser.add_argument("surface_csv", type=Path)
    parser.add_argument("upgraded_receipt_json", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.surface_csv)
    receipt = json.loads(args.upgraded_receipt_json.read_text(encoding="utf-8"))
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = estimate(rows, receipt, config)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
