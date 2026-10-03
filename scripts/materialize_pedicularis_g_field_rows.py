from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts.evaluate_pedicularis_predator_method import REQUIRED_FIELDS, TREATMENTS


FOCAL_REQUIRED_FIELDS = tuple(
    field for field in REQUIRED_FIELDS if field != "pollen_grains"
)

PROXY_REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "predator_treatment",
    "proxy_flower_id",
    "proxy_anthesis_time_hours",
    "proxy_collection_time_hours",
    "pollination_window_complete_before_collection",
    "pollen_grains",
    "notes",
)


def _read(
    path: Path,
    required_fields: tuple[str, ...],
    *,
    label: str,
) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{label} CSV has no header")
        missing = [
            field
            for field in required_fields
            if field not in reader.fieldnames
        ]
        if missing:
            raise ValueError(
                f"{label} missing required columns: "
                + ", ".join(missing)
            )
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]

    if not rows:
        raise ValueError(f"{label} CSV has no data rows")

    for i, row in enumerate(rows, start=2):
        for field in required_fields:
            if row.get(field, "") == "":
                raise ValueError(
                    f"{label} blank required field {field!r} "
                    f"on CSV line {i}"
                )

    return rows


def _num(row: dict[str, str], field: str, *, label: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(
            f"{label} invalid numeric value for {field!r}: "
            f"{row.get(field)!r}"
        ) from exc
    if not math.isfinite(value):
        raise ValueError(
            f"{label} non-finite numeric value for {field!r}"
        )
    return value


def _binary(
    row: dict[str, str],
    field: str,
    *,
    label: str,
) -> int:
    raw = row[field]
    if raw not in {"0", "1"}:
        raise ValueError(
            f"{label} {field} must be coded 0/1, got {raw!r}"
        )
    return int(raw)


def _context(
    rows: list[dict[str, str]],
    *,
    label: str,
) -> tuple[str, str]:
    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(
            f"{label} must contain exactly one population and season"
        )
    return next(iter(contexts))


def _validate_focal_rows(
    rows: list[dict[str, str]],
) -> tuple[str, str]:
    seen: set[str] = set()

    for i, row in enumerate(rows, start=2):
        label = f"focal line {i}"

        flower_id = row["flower_id"]
        if flower_id in seen:
            raise ValueError(
                f"duplicate focal flower_id {flower_id!r}"
            )
        seen.add(flower_id)

        if row["predator_treatment"] not in TREATMENTS:
            raise ValueError(
                "focal predator_treatment must be EXPOSED or EXCLUDED"
            )

        for field in (
            "anthesis_time_hours",
            "barrier_application_time_hours",
            "realized_exsertion",
            "water_depth",
            "pollinator_visits",
            "ovule_count",
            "undamaged_seed_count",
            "damaged_seed_count",
        ):
            _num(row, field, label=label)

        for field in (
            "sham_device_applied",
            "pollination_window_complete_before_barrier",
            "ovary_swollen_at_barrier",
            "barrier_covers_pollinator_entry",
            "pre_barrier_attack_present",
            "barrier_integrity_failure_present",
            "early_predator_attack_present",
            "mechanical_damage",
        ):
            _binary(row, field, label=label)

        anthesis = _num(
            row,
            "anthesis_time_hours",
            label=label,
        )
        barrier = _num(
            row,
            "barrier_application_time_hours",
            label=label,
        )
        if barrier < anthesis:
            raise ValueError(
                "barrier_application_time_hours cannot precede "
                "anthesis_time_hours"
            )

        ovules = _num(row, "ovule_count", label=label)
        undamaged = _num(
            row,
            "undamaged_seed_count",
            label=label,
        )
        damaged = _num(
            row,
            "damaged_seed_count",
            label=label,
        )
        if (
            ovules <= 0
            or undamaged < 0
            or damaged < 0
            or undamaged + damaged > ovules
        ):
            raise ValueError(
                "invalid focal ovule/seed counts"
            )

    return _context(rows, label="focal field table")


def _validate_proxy_rows(
    rows: list[dict[str, str]],
    *,
    focal_ids: set[str],
) -> tuple[str, str]:
    seen: set[str] = set()

    for i, row in enumerate(rows, start=2):
        label = f"pollen proxy line {i}"

        proxy_id = row["proxy_flower_id"]
        if proxy_id in seen:
            raise ValueError(
                f"duplicate proxy_flower_id {proxy_id!r}"
            )
        seen.add(proxy_id)

        if proxy_id in focal_ids:
            raise ValueError(
                "pollen proxy flower IDs must be disjoint from "
                "focal endpoint flower IDs"
            )

        if row["predator_treatment"] not in TREATMENTS:
            raise ValueError(
                "proxy predator_treatment must be EXPOSED or EXCLUDED"
            )

        anthesis = _num(
            row,
            "proxy_anthesis_time_hours",
            label=label,
        )
        collection = _num(
            row,
            "proxy_collection_time_hours",
            label=label,
        )
        if collection < anthesis:
            raise ValueError(
                "proxy_collection_time_hours cannot precede "
                "proxy_anthesis_time_hours"
            )

        if (
            _binary(
                row,
                "pollination_window_complete_before_collection",
                label=label,
            )
            != 1
        ):
            raise ValueError(
                "every pollen proxy must be collected only after the "
                "registered natural-pollination window is complete"
            )

        pollen = _num(row, "pollen_grains", label=label)
        if pollen < 0:
            raise ValueError(
                "proxy pollen_grains must be >= 0"
            )

    return _context(rows, label="pollen proxy table")


def build(
    focal_path: Path,
    proxy_path: Path,
) -> tuple[list[dict[str, str]], dict]:
    focal_rows = _read(
        focal_path,
        FOCAL_REQUIRED_FIELDS,
        label="focal",
    )
    proxy_rows = _read(
        proxy_path,
        PROXY_REQUIRED_FIELDS,
        label="pollen proxy",
    )

    focal_context = _validate_focal_rows(focal_rows)
    focal_ids = {row["flower_id"] for row in focal_rows}
    proxy_context = _validate_proxy_rows(
        proxy_rows,
        focal_ids=focal_ids,
    )

    if focal_context != proxy_context:
        raise ValueError(
            "focal and pollen-proxy tables must share exactly one "
            "population and season"
        )

    focal_pairs = {
        (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["predator_treatment"],
        )
        for row in focal_rows
    }

    proxy_by_pair: dict[
        tuple[str, str, str, str],
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in proxy_rows:
        key = (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["predator_treatment"],
        )
        if key not in focal_pairs:
            raise ValueError(
                "pollen proxy row has no matching focal "
                "plant/treatment pair"
            )
        proxy_by_pair[key].append(row)

    missing_pairs = sorted(
        focal_pairs - set(proxy_by_pair)
    )
    if missing_pairs:
        raise ValueError(
            "missing pollen proxy rows for focal plant/treatment "
            "pairs: "
            + "; ".join(
                f"{plant}/{treatment}"
                for _, _, plant, treatment in missing_pairs
            )
        )

    materialized: list[dict[str, str]] = []
    provenance_rows = []

    for row in focal_rows:
        key = (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["predator_treatment"],
        )
        proxies = proxy_by_pair[key]
        pollen_mean = mean(
            _num(
                proxy,
                "pollen_grains",
                label="pollen proxy",
            )
            for proxy in proxies
        )

        out = dict(row)
        out["pollen_grains"] = repr(pollen_mean)

        # Keep the exact canonical V4 field order expected by
        # evaluate_pedicularis_predator_method.py.
        materialized.append(
            {
                field: out[field]
                for field in REQUIRED_FIELDS
            }
        )

    for key, proxies in sorted(proxy_by_pair.items()):
        population, season, plant, treatment = key
        values = [
            _num(
                proxy,
                "pollen_grains",
                label="pollen proxy",
            )
            for proxy in proxies
        ]
        provenance_rows.append(
            {
                "population_id": population,
                "season_id": season,
                "plant_id": plant,
                "predator_treatment": treatment,
                "n_proxy_flowers": len(proxies),
                "proxy_flower_ids": sorted(
                    proxy["proxy_flower_id"]
                    for proxy in proxies
                ),
                "mean_pollen_grains_materialized": mean(values),
                "min_proxy_collection_delay_hours": min(
                    _num(
                        proxy,
                        "proxy_collection_time_hours",
                        label="pollen proxy",
                    )
                    - _num(
                        proxy,
                        "proxy_anthesis_time_hours",
                        label="pollen proxy",
                    )
                    for proxy in proxies
                ),
                "max_proxy_collection_delay_hours": max(
                    _num(
                        proxy,
                        "proxy_collection_time_hours",
                        label="pollen proxy",
                    )
                    - _num(
                        proxy,
                        "proxy_anthesis_time_hours",
                        label="pollen proxy",
                    )
                    for proxy in proxies
                ),
            }
        )

    population_id, season_id = focal_context

    receipt = {
        "receipt_schema_version": (
            "SCH_PEDICULARIS_G_FIELD_MATERIALIZATION_V1"
        ),
        "analysis": "pedicularis_g_field_materialization",
        "population_id": population_id,
        "season_id": season_id,
        "n_focal_endpoint_rows": len(focal_rows),
        "n_pollen_proxy_rows": len(proxy_rows),
        "n_plant_treatment_pairs": len(focal_pairs),
        "all_focal_pairs_have_pollen_proxy": True,
        "proxy_flowers_disjoint_from_endpoint_flowers": True,
        "pollen_materialization_semantics": (
            "Each endpoint flower receives the mean pollen-grain "
            "count of its plant x predator-treatment matched "
            "sacrificial proxy flowers. The downstream evaluator "
            "first averages flowers within plant/treatment and then "
            "bootstraps plants, so repeated proxy means do not create "
            "additional plant-level replication."
        ),
        "proxy_provenance": provenance_rows,
        "status": (
            "PEDICULARIS_G_FIELD_ROWS_READY_FOR_"
            "THRESHOLD_FREE_CALIBRATION_SUMMARY"
        ),
        "claim_ceiling": [
            "field_data_materialization_only",
            "pollen_proxy_is_not_same_flower_endpoint",
            "proxy_mean_is_repeated_for_compatibility_not_replication",
            "does_not_validate_G",
            "does_not_choose_thresholds",
        ],
    }

    return materialized, receipt


def _write_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    if not rows:
        raise ValueError("cannot write empty G materialized table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(REQUIRED_FIELDS),
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize canonical Pedicularis G V4 calibration rows "
            "from focal endpoint flowers plus matched sacrificial "
            "pollen-proxy flowers"
        )
    )
    parser.add_argument("focal_csv", type=Path)
    parser.add_argument("pollen_proxy_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    rows, receipt = build(
        args.focal_csv,
        args.pollen_proxy_csv,
    )
    _write_csv(args.out_csv, rows)

    payload = (
        json.dumps(receipt, indent=2, sort_keys=True)
        + "\n"
    )
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
