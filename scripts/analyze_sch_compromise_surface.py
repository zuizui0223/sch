from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean


REQUIRED_FIELDS = (
    "plant_id",
    "blossom_id",
    "z_level",
    "z_measured",
    "pollinator_state",
    "antagonist_state",
    "fitness_value",
)

STATE_KEYS = ((0, 0), (1, 0), (0, 1), (1, 1))


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
        if row["blossom_id"] in seen:
            raise ValueError(f"duplicate blossom_id {row['blossom_id']!r}")
        seen.add(row["blossom_id"])
        _number(row, "z_measured")
        _number(row, "fitness_value")
        _binary(row, "pollinator_state")
        _binary(row, "antagonist_state")
    return rows


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take quantile of empty values")
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    w = pos - lo
    return values[lo] * (1 - w) + values[hi] * w


def _solve3(matrix: list[list[float]], rhs: list[float]) -> tuple[float, float, float]:
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("quadratic fit is singular")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(3):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [a - factor * b for a, b in zip(aug[row], aug[col])]
    return aug[0][3], aug[1][3], aug[2][3]


def _fit_quadratic(points: list[tuple[float, float]]) -> dict:
    if len(points) < 3:
        raise ValueError("quadratic fit requires at least three z levels")
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    if len({round(x, 12) for x in xs}) < 3:
        raise ValueError("quadratic fit requires at least three distinct measured z values")

    n = float(len(points))
    s1 = sum(xs)
    s2 = sum(x * x for x in xs)
    s3 = sum(x**3 for x in xs)
    s4 = sum(x**4 for x in xs)
    t0 = sum(ys)
    t1 = sum(x * y for x, y in points)
    t2 = sum((x * x) * y for x, y in points)
    a, b, c = _solve3(
        [[n, s1, s2], [s1, s2, s3], [s2, s3, s4]],
        [t0, t1, t2],
    )

    discrete_index = max(range(len(points)), key=lambda i: points[i][1])
    discrete_optimum = points[discrete_index][0]
    z_min, z_max = min(xs), max(xs)
    vertex = None
    if c < 0:
        candidate = -b / (2 * c)
        if z_min <= candidate <= z_max:
            vertex = candidate
    optimum = vertex if vertex is not None else discrete_optimum
    return {
        "a": a,
        "b": b,
        "c": c,
        "z_min": z_min,
        "z_max": z_max,
        "discrete_optimum": discrete_optimum,
        "quadratic_vertex": vertex,
        "primary_optimum": optimum,
        "optimum_class": "INTERIOR_CONCAVE" if vertex is not None else "BOUNDARY_OR_NONCONCAVE",
        "points": [{"z": x, "mean_fitness": y} for x, y in points],
    }


def _state_points(rows: list[dict[str, str]], p: int, g: int, min_levels: int) -> list[tuple[float, float]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if _binary(row, "pollinator_state") == p and _binary(row, "antagonist_state") == g:
            grouped[row["z_level"]].append(row)
    if len(grouped) < min_levels:
        raise ValueError(f"state P{p}G{g} has {len(grouped)} z levels; requires >= {min_levels}")
    points = []
    for level in sorted(grouped):
        group = grouped[level]
        points.append(
            (
                mean(_number(row, "z_measured") for row in group),
                mean(_number(row, "fitness_value") for row in group),
            )
        )
    return sorted(points)


def _fit_states(rows: list[dict[str, str]], min_levels: int) -> dict[str, dict]:
    fits: dict[str, dict] = {}
    for p, g in STATE_KEYS:
        fits[f"P{p}G{g}"] = _fit_quadratic(_state_points(rows, p, g, min_levels))
    return fits


def _subtract_coeffs(left: dict, right: dict) -> tuple[float, float, float]:
    return (
        left["a"] - right["a"],
        left["b"] - right["b"],
        left["c"] - right["c"],
    )


def _add_coeffs(*terms: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(sum(term[i] for term in terms) for i in range(3))  # type: ignore[return-value]


def _gradient(coeffs: tuple[float, float, float], z: float) -> float:
    _, b, c = coeffs
    return b + 2 * c * z


def _surface_metrics(fits: dict[str, dict]) -> dict:
    baseline = (fits["P0G0"]["a"], fits["P0G0"]["b"], fits["P0G0"]["c"])
    pollinator = _subtract_coeffs(fits["P1G0"], fits["P0G0"])
    antagonist_at_p1 = _subtract_coeffs(fits["P1G1"], fits["P1G0"])
    antagonist_at_p0 = _subtract_coeffs(fits["P0G1"], fits["P0G0"])
    interaction = _add_coeffs(
        (fits["P1G1"]["a"], fits["P1G1"]["b"], fits["P1G1"]["c"]),
        (-fits["P1G0"]["a"], -fits["P1G0"]["b"], -fits["P1G0"]["c"]),
        (-fits["P0G1"]["a"], -fits["P0G1"]["b"], -fits["P0G1"]["c"]),
        (fits["P0G0"]["a"], fits["P0G0"]["b"], fits["P0G0"]["c"]),
    )

    z_combined = fits["P1G1"]["primary_optimum"]
    z_pollinator_context = fits["P1G0"]["primary_optimum"]
    z_antagonist_context = fits["P0G1"]["primary_optimum"]

    return {
        "z_combined": z_combined,
        "z_pollinator_context": z_pollinator_context,
        "z_antagonist_context": z_antagonist_context,
        "state_optimum_separation": z_pollinator_context - z_antagonist_context,
        "shift_remove_antagonist": z_pollinator_context - z_combined,
        "shift_remove_pollinator": z_antagonist_context - z_combined,
        "combined_interior": fits["P1G1"]["optimum_class"] == "INTERIOR_CONCAVE",
        "gradients_at_combined_optimum": {
            "baseline_P0G0": _gradient(baseline, z_combined),
            "pollinator_component_G0": _gradient(pollinator, z_combined),
            "antagonist_component_P1": _gradient(antagonist_at_p1, z_combined),
            "antagonist_component_P0": _gradient(antagonist_at_p0, z_combined),
            "PxG_interaction": _gradient(interaction, z_combined),
            "combined_P1G1": fits["P1G1"]["b"] + 2 * fits["P1G1"]["c"] * z_combined,
        },
        "component_coefficients": {
            "baseline_P0G0": baseline,
            "pollinator_component_G0": pollinator,
            "antagonist_component_P1": antagonist_at_p1,
            "antagonist_component_P0": antagonist_at_p0,
            "PxG_interaction": interaction,
        },
    }


def _cluster_bootstrap_rows(rows: list[dict[str, str]], rng: random.Random) -> list[dict[str, str]]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        clusters[row["plant_id"]].append(row)
    ids = list(clusters)
    if len(ids) < 2:
        raise ValueError("at least two plant_id clusters are required")
    sampled: list[dict[str, str]] = []
    for cluster_id in rng.choices(ids, k=len(ids)):
        sampled.extend(clusters[cluster_id])
    return sampled


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    min_levels = int(config.get("min_z_levels", 5))
    if min_levels < 3:
        raise ValueError("min_z_levels must be >= 3")
    reps = int(config.get("bootstrap_reps", 0))
    if reps < 200:
        raise ValueError("bootstrap_reps must be >= 200")
    rng = random.Random(int(config.get("random_seed", 20260904)))

    observed_fits = _fit_states(rows, min_levels)
    observed = _surface_metrics(observed_fits)

    boot_metrics: list[dict] = []
    interior_count = 0
    for _ in range(reps):
        sample = _cluster_bootstrap_rows(rows, rng)
        try:
            fits = _fit_states(sample, min_levels)
            metrics = _surface_metrics(fits)
        except ValueError:
            continue
        boot_metrics.append(metrics)
        interior_count += int(metrics["combined_interior"])

    min_valid_fraction = float(config.get("min_valid_bootstrap_fraction", 0.5))
    if len(boot_metrics) < max(50, int(reps * min_valid_fraction)):
        raise ValueError("too few valid plant-cluster bootstrap replicates")

    def ci(key: str) -> list[float]:
        values = [float(item[key]) for item in boot_metrics]
        return [_quantile(values, 0.025), _quantile(values, 0.975)]

    gradient_names = tuple(observed["gradients_at_combined_optimum"])
    gradient_cis = {}
    for name in gradient_names:
        values = [float(item["gradients_at_combined_optimum"][name]) for item in boot_metrics]
        gradient_cis[name] = [_quantile(values, 0.025), _quantile(values, 0.975)]

    sep_ci = ci("state_optimum_separation")
    shift_g_ci = ci("shift_remove_antagonist")
    shift_p_ci = ci("shift_remove_pollinator")

    min_sep = float(config.get("min_optimum_separation", 0.0))
    min_shift = float(config.get("min_optimum_shift", 0.0))
    min_grad = float(config.get("min_abs_component_gradient", 0.0))
    min_interior_fraction = float(config.get("min_interior_bootstrap_fraction", 0.5))

    separated = sep_ci[0] >= min_sep or sep_ci[1] <= -min_sep
    shifts_opposed = (
        shift_g_ci[0] >= min_shift and shift_p_ci[1] <= -min_shift
    ) or (
        shift_p_ci[0] >= min_shift and shift_g_ci[1] <= -min_shift
    )
    poll_ci = gradient_cis["pollinator_component_G0"]
    ant_ci = gradient_cis["antagonist_component_P1"]
    gradients_opposed = (
        poll_ci[0] >= min_grad and ant_ci[1] <= -min_grad
    ) or (
        ant_ci[0] >= min_grad and poll_ci[1] <= -min_grad
    )
    interior_fraction = interior_count / len(boot_metrics)
    interior_supported = observed["combined_interior"] and interior_fraction >= min_interior_fraction

    decisions = {
        "distinct_state_optima": separated,
        "combined_interior_optimum": interior_supported,
        "opposing_optimum_shifts": shifts_opposed,
        "opposed_functional_gradients": gradients_opposed,
    }

    return {
        "analysis": "sch_multilevel_causal_compromise_surface",
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "z_levels": sorted({row["z_level"] for row in rows}),
        "state_fits": observed_fits,
        "observed_estimands": observed,
        "bootstrap": {
            "requested_reps": reps,
            "valid_reps": len(boot_metrics),
            "combined_interior_fraction": interior_fraction,
            "state_optimum_separation_95_ci": sep_ci,
            "shift_remove_antagonist_95_ci": shift_g_ci,
            "shift_remove_pollinator_95_ci": shift_p_ci,
            "gradient_95_ci": gradient_cis,
        },
        "predeclared_thresholds": {
            "min_optimum_separation": min_sep,
            "min_optimum_shift": min_shift,
            "min_abs_component_gradient": min_grad,
            "min_interior_bootstrap_fraction": min_interior_fraction,
        },
        "decisions": decisions,
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
        if all(decisions.values())
        else "COMPROMISE_CRITERIA_NOT_ALL_RECOVERED",
        "claim_ceiling": (
            "randomized_multilevel_local_quadratic_compromise_model_only_"
            "not_historical_modularization_and_not_direct_cost_allocation"
        ),
        "interpretation_note": (
            "The zero slope of an interior fitted P1G1 quadratic at its own vertex is a model property, "
            "not an independent gradient-cancellation test. Evidence for balance comes from interior curvature, "
            "opposed component-gradient intervals, and causal optimum shifts under selective P/G interventions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze SCH multi-level z x P x G compromise experiment")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze(rows, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
