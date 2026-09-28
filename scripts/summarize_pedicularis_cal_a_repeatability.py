from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

from scripts.scale_free_relative import relative_change


REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "measurement_replicate",
    "observer_id",
    "realized_exsertion",
    "corolla_opening_width",
    "lower_lip_angle_deg",
    "tube_diameter",
    "bract_height",
    "water_depth",
    "flower_orientation_deg",
)

METRICS = (
    "realized_exsertion",
    "corolla_opening_width",
    "lower_lip_angle_deg",
    "tube_diameter",
    "bract_height",
    "water_depth",
    "flower_orientation_deg",
)

RELATIVE_METRICS = {
    "realized_exsertion",
    "corolla_opening_width",
    "tube_diameter",
    "bract_height",
}


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(
            f"invalid numeric value for {field!r}: {row.get(field)!r}"
        ) from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _replicate(row: dict[str, str]) -> int:
    raw = row["measurement_replicate"].strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(
            f"measurement_replicate must be an integer, got {raw!r}"
        ) from exc
    if value < 1:
        raise ValueError("measurement_replicate must be >= 1")
    return value


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CAL-A repeatability CSV has no header")
        missing = [
            field for field in REQUIRED_FIELDS
            if field not in reader.fieldnames
        ]
        if missing:
            raise ValueError(
                "missing required columns: " + ", ".join(missing)
            )
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]

    if not rows:
        raise ValueError("CAL-A repeatability CSV has no data rows")

    seen: set[tuple[str, int]] = set()
    by_flower: Counter[str] = Counter()

    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "") == "":
                raise ValueError(
                    f"blank required field {field!r} on CSV line {i}"
                )
        rep = _replicate(row)
        key = (row["flower_id"], rep)
        if key in seen:
            raise ValueError(
                "flower_id + measurement_replicate must be unique"
            )
        seen.add(key)
        by_flower[row["flower_id"]] += 1
        for field in METRICS:
            _num(row, field)

    insufficient = sorted(
        flower_id
        for flower_id, n in by_flower.items()
        if n < 2
    )
    if insufficient:
        raise ValueError(
            "every calibration flower requires >=2 measurement replicates: "
            + ", ".join(insufficient)
        )

    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(
            "one CAL-A repeatability package must contain exactly one "
            "population and season"
        )

    return rows


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot summarize empty values")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    w = pos - lo
    return ordered[lo] * (1 - w) + ordered[hi] * w


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        raise ValueError("cannot summarize empty values")
    return {
        "n": len(values),
        "mean": mean(values),
        "sd": stdev(values) if len(values) >= 2 else None,
        "median": _quantile(values, 0.5),
        "q95": _quantile(values, 0.95),
        "max": max(values),
    }


def _metric_summary(
    rows: list[dict[str, str]],
    metric: str,
) -> dict:
    by_flower: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        by_flower[row["flower_id"]].append(_num(row, metric))

    flower_means = {
        flower_id: mean(values)
        for flower_id, values in by_flower.items()
    }

    max_abs_deviation: list[float] = []
    max_relative_deviation: list[float] = []
    within_sq = 0.0
    within_df = 0

    for flower_id, values in by_flower.items():
        center = flower_means[flower_id]
        deviations = [abs(value - center) for value in values]
        max_abs_deviation.append(max(deviations))
        within_sq += sum((value - center) ** 2 for value in values)
        within_df += len(values) - 1

        if metric in RELATIVE_METRICS:
            relative = [
                relative_change(value, center)
                for value in values
            ]
            max_relative_deviation.append(max(relative))

    result = {
        "n_flowers": len(by_flower),
        "n_measurements": sum(len(values) for values in by_flower.values()),
        "replicates_per_flower": _summary(
            [float(len(values)) for values in by_flower.values()]
        ),
        "flower_mean_distribution": _summary(
            list(flower_means.values())
        ),
        "between_flower_sd_of_means": (
            stdev(flower_means.values())
            if len(flower_means) >= 2
            else None
        ),
        "pooled_within_flower_sd": (
            math.sqrt(within_sq / within_df)
            if within_df > 0
            else None
        ),
        "max_absolute_deviation_from_flower_mean": _summary(
            max_abs_deviation
        ),
    }

    if metric in RELATIVE_METRICS:
        result["max_relative_deviation_from_flower_mean"] = _summary(
            max_relative_deviation
        )

    return result


def build(rows: list[dict[str, str]]) -> dict:
    population_id = rows[0]["population_id"]
    season_id = rows[0]["season_id"]

    return {
        "analysis": "pedicularis_cal_a_repeatability_summary_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "n_flowers": len({row["flower_id"] for row in rows}),
        "observer_counts": dict(
            sorted(Counter(row["observer_id"] for row in rows).items())
        ),
        "metric_repeatability": {
            metric: _metric_summary(rows, metric)
            for metric in METRICS
        },
        "status": "CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
        "claim_ceiling": [
            "measurement_repeatability_basis_only",
            "does_not_define_minimum_z_separation",
            "does_not_define_equivalence_margin",
            "does_not_validate_P0_P1_or_G",
            "repeatability_rows_are_not_confirmatory_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize Pedicularis CAL-A repeated measurements without "
            "choosing field thresholds"
        )
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(read_rows(args.csv_path))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
