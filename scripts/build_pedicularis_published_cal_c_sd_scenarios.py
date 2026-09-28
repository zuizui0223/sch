from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PUBLISHED_EMPIRICAL_PRIORS_V1.csv"
)

SOURCE_MAP = {
    "P1_POLLEN": {
        "measurement_id": "PRX2016_POLLEN_GLM_POOL",
        "gate_path": "pollination_weight.min_pollen_grain_delta",
        "metric": "paired supplementation-minus-natural pollen-grain difference",
        "source_marginal_metric": "plant-level pollen grains on stigma",
    },
    "G_PREDATION": {
        "measurement_id": "PRX2016_PREDATION_GLM_POOL",
        "gate_path": "predator_weight.min_predation_fraction_reduction",
        "metric": "paired exposed-minus-excluded seed-predation difference",
        "source_marginal_metric": "plant-level seed-predation proportion",
    },
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("published-prior ledger has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _source_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_id = {row["measurement_id"]: row for row in rows}
    out = {}
    for criterion_id, spec in SOURCE_MAP.items():
        measurement_id = spec["measurement_id"]
        if measurement_id not in by_id:
            raise ValueError(
                f"required published SD row is missing: {measurement_id}"
            )
        row = by_id[measurement_id]
        if row["uncertainty_type"] != "SD":
            raise ValueError(
                f"{measurement_id} must carry a directly reported SD"
            )
        if row["direct_freeze_eligible"] != "NO":
            raise ValueError(
                f"{measurement_id} must remain external-prior only"
            )
        try:
            sd = float(row["uncertainty_value"])
        except ValueError as exc:
            raise ValueError(
                f"{measurement_id} SD is not numeric"
            ) from exc
        if not math.isfinite(sd) or sd <= 0:
            raise ValueError(f"{measurement_id} SD must be finite and > 0")
        out[criterion_id] = {**row, "_sd": sd}
    return out


def paired_difference_sd(
    marginal_sd: float,
    within_pair_correlation: float,
) -> float:
    if not math.isfinite(marginal_sd) or marginal_sd <= 0:
        raise ValueError("marginal_sd must be finite and > 0")
    if not -1.0 < within_pair_correlation < 1.0:
        raise ValueError("within_pair_correlation must lie in (-1, 1)")
    return marginal_sd * math.sqrt(
        2.0 * (1.0 - within_pair_correlation)
    )


def build(
    prior_path: Path = DEFAULT_PRIORS,
    correlations: tuple[float, ...] = (0.0, 0.25, 0.50, 0.75),
) -> dict:
    rows = _read(prior_path)
    sources = _source_rows(rows)

    if len(correlations) < 2:
        raise ValueError("at least two correlation scenarios are required")
    if len(correlations) != len(set(correlations)):
        raise ValueError("correlation scenarios must be unique")
    for rho in correlations:
        if not -1.0 < rho < 1.0:
            raise ValueError("correlation scenarios must lie in (-1, 1)")

    scenarios = []
    criterion_summary = {}

    for criterion_id, spec in SOURCE_MAP.items():
        source = sources[criterion_id]
        marginal_sd = float(source["_sd"])
        criterion_rows = []

        for rho in correlations:
            diff_sd = paired_difference_sd(marginal_sd, rho)
            record = {
                "criterion_id": criterion_id,
                "gate_path": spec["gate_path"],
                "target_metric": spec["metric"],
                "published_measurement_id": source["measurement_id"],
                "published_source_id": source["source_id"],
                "published_marginal_metric": spec[
                    "source_marginal_metric"
                ],
                "published_marginal_sd": marginal_sd,
                "within_pair_correlation_assumption": rho,
                "implied_paired_difference_sd": diff_sd,
                "scenario_role": (
                    "EXTERNAL_CAL_C_SENSITIVITY_ONLY_NOT_PILOT_SD"
                ),
            }
            scenarios.append(record)
            criterion_rows.append(record)

        sds = [
            row["implied_paired_difference_sd"]
            for row in criterion_rows
        ]
        criterion_summary[criterion_id] = {
            "gate_path": spec["gate_path"],
            "published_measurement_id": source["measurement_id"],
            "published_marginal_sd": marginal_sd,
            "min_implied_paired_difference_sd": min(sds),
            "max_implied_paired_difference_sd": max(sds),
            "correlation_grid": list(correlations),
        }

    return {
        "analysis": "pedicularis_published_cal_c_sd_scenarios_v1",
        "n_criteria_with_external_sd_scenarios": len(SOURCE_MAP),
        "n_scenarios": len(scenarios),
        "paired_difference_formula": (
            "sd_delta = sd_marginal * sqrt(2 * (1 - rho)) "
            "under equal marginal variances"
        ),
        "criterion_summary": criterion_summary,
        "scenarios": scenarios,
        "status": "PUBLISHED_SD_SENSITIVITY_SCENARIOS_READY",
        "direct_cal_c_pilot_sd_values_materialized": 0,
        "direct_f0_values_materialized": 0,
        "claim_ceiling": [
            "external_historical_variance_sensitivity_only",
            "equal_marginal_variance_assumption_is_explicit",
            "within_pair_correlation_is_unknown_and_varied",
            "do_not_write_scenario_sd_into_CAL_C_as_observed_pilot_sd",
            "replace_with_same_context_calibration_variance_when_available",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build external Pedicularis CAL-C paired-difference SD "
            "sensitivity scenarios from directly reported published SDs"
        )
    )
    parser.add_argument("--priors", type=Path, default=DEFAULT_PRIORS)
    parser.add_argument(
        "--correlations",
        type=float,
        nargs="+",
        default=[0.0, 0.25, 0.50, 0.75],
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        prior_path=args.priors,
        correlations=tuple(args.correlations),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
