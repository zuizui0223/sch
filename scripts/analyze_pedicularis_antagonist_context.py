from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts import analyze_pedicularis_full_surface as surface


CONFIG_SCHEMA = "PEDICULARIS_P2_ANTAGONIST_CONTEXT_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_P2_ANTAGONIST_CONTEXT_PROSPECTIVELY_FROZEN"
SURFACE_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

REGISTRY_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "patch_id",
    "context_measurement_date",
    "patch_area_m2",
    "patch_size_flowering_plants",
    "notes",
)


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _read_context(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("antagonist-context registry has no header")
        missing = [field for field in REGISTRY_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(
                "antagonist-context registry lacks columns: " + ", ".join(missing)
            )
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("antagonist-context registry is empty")
    return rows


def _semantic_sha256(payload: object) -> str:
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _number(value: object, label: str) -> float:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be resolved")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _number(value, label)
    if out < 1 or not out.is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(out)


def _validate_config(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"context config schema must be {CONFIG_SCHEMA}")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("antagonist-context config is not prospectively frozen")
    if config.get("frozen_before_p2_outcomes") is not True:
        raise ValueError("antagonist-context config must be frozen before P2 outcomes")

    population_id = config.get("population_id")
    season_id = config.get("season_id")
    if not isinstance(population_id, str) or not population_id or population_id == PLACEHOLDER:
        raise ValueError("context config population_id is unresolved")
    if not isinstance(season_id, str) or not season_id or season_id == PLACEHOLDER:
        raise ValueError("context config season_id is unresolved")

    historical = config.get("historical_comparison")
    if not isinstance(historical, dict):
        raise ValueError("historical_comparison block is required")

    sparse_max = _number(
        historical.get("sparse_density_max_exclusive_plants_m2"),
        "sparse_density_max_exclusive_plants_m2",
    )
    dense_min = _number(
        historical.get("dense_density_min_exclusive_plants_m2"),
        "dense_density_min_exclusive_plants_m2",
    )
    small_max = _positive_int(
        historical.get("small_patch_max_exclusive_flowering_plants"),
        "small_patch_max_exclusive_flowering_plants",
    )
    large_min = _positive_int(
        historical.get("large_patch_min_exclusive_flowering_plants"),
        "large_patch_min_exclusive_flowering_plants",
    )
    if sparse_max >= dense_min:
        raise ValueError("sparse density threshold must be below dense threshold")
    if small_max != large_min:
        raise ValueError(
            "historical small/large patch boundary must use one shared excluded value"
        )
    if historical.get("exact_boundary_is_unclassified") is not True:
        raise ValueError("historical patch boundary must remain unclassified")

    gate = config.get("analysis_gate")
    if not isinstance(gate, dict):
        raise ValueError("analysis_gate is required")
    min_plants = _positive_int(
        gate.get("min_plants_per_historical_context_cell"),
        "min_plants_per_historical_context_cell",
    )

    return {
        "population_id": population_id,
        "season_id": season_id,
        "sparse_density_max_exclusive": sparse_max,
        "dense_density_min_exclusive": dense_min,
        "patch_boundary_exclusive": small_max,
        "min_plants_per_cell": min_plants,
        "source": historical.get("source"),
    }


def _validate_surface_receipt(rows: list[dict[str, str]], receipt: dict) -> None:
    if receipt.get("system_wrapper_schema_version") != SURFACE_SCHEMA:
        raise ValueError("context analysis requires a canonical Pedicularis surface receipt")
    if receipt.get("system") != "Pedicularis rex":
        raise ValueError("surface receipt is not Pedicularis rex")

    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("P2 rows must contain one population and season")
    population_id = next(iter(populations))
    season_id = next(iter(seasons))

    if receipt.get("population_id") != population_id:
        raise ValueError("surface receipt population does not match P2 rows")
    if receipt.get("season_id") != season_id:
        raise ValueError("surface receipt season does not match P2 rows")
    observed = surface.surface_data_sha256(rows)
    if receipt.get("surface_data_sha256") != observed:
        raise ValueError(
            "context analysis rows are not the exact data used for the P2 surface receipt"
        )


def _validate_context(
    context_rows: list[dict[str, str]],
    p2_rows: list[dict[str, str]],
    config: dict,
) -> dict[str, dict]:
    p2_plants = {row["plant_id"] for row in p2_rows}
    by_plant: dict[str, dict] = {}
    patch_sizes: dict[str, set[int]] = defaultdict(set)
    patch_areas: dict[str, set[float]] = defaultdict(set)

    for row in context_rows:
        if row["population_id"] != config["population_id"]:
            raise ValueError("context registry population does not match frozen config")
        if row["season_id"] != config["season_id"]:
            raise ValueError("context registry season does not match frozen config")
        plant = row["plant_id"]
        patch = row["patch_id"]
        date = row["context_measurement_date"]
        if not plant or not patch or not date:
            raise ValueError("plant_id, patch_id and context_measurement_date are required")
        if plant in by_plant:
            raise ValueError("each P2 plant must have exactly one context row")

        patch_area = _number(row["patch_area_m2"], "patch_area_m2")
        patch_size = _positive_int(
            row["patch_size_flowering_plants"],
            "patch_size_flowering_plants",
        )
        if patch_area <= 0:
            raise ValueError("patch_area_m2 must be >0")

        patch_density = patch_size / patch_area
        by_plant[plant] = {
            **row,
            "patch_area_m2": patch_area,
            "patch_flowering_density_plants_m2": patch_density,
            "patch_size_flowering_plants": patch_size,
        }
        patch_sizes[patch].add(patch_size)
        patch_areas[patch].add(patch_area)

    if set(by_plant) != p2_plants:
        missing = sorted(p2_plants - set(by_plant))
        extra = sorted(set(by_plant) - p2_plants)
        raise ValueError(
            "context registry must cover exactly the P2 plants: "
            f"missing={missing}, extra={extra}"
        )

    inconsistent_sizes = sorted(
        patch for patch, values in patch_sizes.items() if len(values) != 1
    )
    if inconsistent_sizes:
        raise ValueError(
            "patch_size_flowering_plants must be constant within patch_id: "
            + ", ".join(inconsistent_sizes)
        )
    inconsistent_areas = sorted(
        patch for patch, values in patch_areas.items() if len(values) != 1
    )
    if inconsistent_areas:
        raise ValueError(
            "patch_area_m2 must be constant within patch_id: "
            + ", ".join(inconsistent_areas)
        )
    return by_plant


def _density_class(density: float, config: dict) -> str:
    if density < config["sparse_density_max_exclusive"]:
        return "SPARSE"
    if density > config["dense_density_min_exclusive"]:
        return "DENSE"
    return "INTERMEDIATE"


def _patch_class(size: int, config: dict) -> str:
    boundary = config["patch_boundary_exclusive"]
    if size < boundary:
        return "SMALL"
    if size > boundary:
        return "LARGE"
    return "BOUNDARY_UNCLASSIFIED"


def _plant_natural_exposed(rows: list[dict[str, str]]) -> dict[str, dict]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if (
            row["pollination_treatment"] == "NATURAL"
            and row["predator_treatment"] == "EXPOSED"
        ):
            grouped[row["plant_id"]].append(row)

    result = {}
    for plant, plant_rows in grouped.items():
        damaged = sum(float(row["damaged_seed_count"]) for row in plant_rows)
        undamaged = sum(float(row["undamaged_seed_count"]) for row in plant_rows)
        developed = damaged + undamaged
        ovules = sum(float(row["ovule_count"]) for row in plant_rows)
        if developed <= 0 or ovules <= 0:
            continue
        result[plant] = {
            "n_natural_exposed_flowers": len(plant_rows),
            "seed_predation_fraction": damaged / developed,
            "early_attack_rate": mean(
                int(row["early_predator_attack_present"]) for row in plant_rows
            ),
            "final_undamaged_seed_fraction": undamaged / ovules,
        }
    return result


def _cell_summary(values: list[dict]) -> dict:
    return {
        "n_plants": len(values),
        "mean_seed_predation_fraction": mean(
            value["seed_predation_fraction"] for value in values
        ),
        "mean_early_attack_rate": mean(value["early_attack_rate"] for value in values),
        "mean_final_undamaged_seed_fraction": mean(
            value["final_undamaged_seed_fraction"] for value in values
        ),
    }


def build(
    rows: list[dict[str, str]],
    surface_receipt: dict,
    context_rows: list[dict[str, str]],
    config_payload: dict,
) -> dict:
    config = _validate_config(config_payload)
    _validate_surface_receipt(rows, surface_receipt)

    population = {row["population_id"] for row in rows}
    season = {row["season_id"] for row in rows}
    if population != {config["population_id"]} or season != {config["season_id"]}:
        raise ValueError("P2 rows do not match frozen context population/season")

    context = _validate_context(context_rows, rows, config)
    natural_exposed = _plant_natural_exposed(rows)

    cells: dict[str, list[dict]] = defaultdict(list)
    classified_plants = []
    for plant, outcome in natural_exposed.items():
        info = context[plant]
        density_class = _density_class(
            info["patch_flowering_density_plants_m2"],
            config,
        )
        patch_class = _patch_class(
            info["patch_size_flowering_plants"],
            config,
        )
        cell = f"{density_class}_{patch_class}"
        record = {
            "plant_id": plant,
            "patch_id": info["patch_id"],
            "patch_flowering_density_plants_m2": info[
                "patch_flowering_density_plants_m2"
            ],
            "patch_size_flowering_plants": info["patch_size_flowering_plants"],
            "density_class": density_class,
            "patch_size_class": patch_class,
            **outcome,
        }
        classified_plants.append(record)
        if density_class in {"SPARSE", "DENSE"} and patch_class in {
            "SMALL",
            "LARGE",
        }:
            cells[cell].append(record)

    expected_cells = {
        "SPARSE_SMALL",
        "SPARSE_LARGE",
        "DENSE_SMALL",
        "DENSE_LARGE",
    }
    cell_summaries = {
        cell: _cell_summary(cells[cell])
        for cell in sorted(expected_cells & set(cells))
    }
    n_by_cell = {cell: len(cells.get(cell, [])) for cell in sorted(expected_cells)}
    modelable = all(
        n_by_cell[cell] >= config["min_plants_per_cell"]
        for cell in expected_cells
    )

    if modelable:
        ss = cell_summaries["SPARSE_SMALL"]["mean_seed_predation_fraction"]
        sl = cell_summaries["SPARSE_LARGE"]["mean_seed_predation_fraction"]
        ds = cell_summaries["DENSE_SMALL"]["mean_seed_predation_fraction"]
        dl = cell_summaries["DENSE_LARGE"]["mean_seed_predation_fraction"]

        sparse_all = cells["SPARSE_SMALL"] + cells["SPARSE_LARGE"]
        dense_all = cells["DENSE_SMALL"] + cells["DENSE_LARGE"]
        sparse_mean = mean(x["seed_predation_fraction"] for x in sparse_all)
        dense_mean = mean(x["seed_predation_fraction"] for x in dense_all)

        contrasts = {
            "dense_minus_sparse_seed_predation": dense_mean - sparse_mean,
            "sparse_large_minus_small_patch_effect": sl - ss,
            "dense_large_minus_small_patch_effect": dl - ds,
            "patch_by_density_difference_in_differences": (dl - ds) - (sl - ss),
        }
        sign_checks = {
            "seed_predation_lower_in_dense_than_sparse": (
                contrasts["dense_minus_sparse_seed_predation"] < 0
            ),
            "small_patch_more_predated_within_sparse": (
                contrasts["sparse_large_minus_small_patch_effect"] < 0
            ),
            "large_patch_more_predated_within_dense": (
                contrasts["dense_large_minus_small_patch_effect"] > 0
            ),
            "patch_size_effect_reverses_with_density": (
                contrasts["patch_by_density_difference_in_differences"] > 0
            ),
        }
        status = (
            "P2_ANTAGONIST_CONTEXT_PATTERN_CONSISTENT_WITH_XIA2013"
            if all(sign_checks.values())
            else "P2_ANTAGONIST_CONTEXT_PATTERN_NOT_RECOVERED"
        )
    else:
        contrasts = None
        sign_checks = None
        status = "P2_ANTAGONIST_CONTEXT_HISTORICAL_COMPARISON_NOT_MODELABLE"

    return {
        "analysis": "pedicularis_p2_antagonist_context_v1",
        "receipt_schema": "PEDICULARIS_P2_ANTAGONIST_CONTEXT_V1",
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "surface_data_sha256": surface_receipt["surface_data_sha256"],
        "surface_status": surface_receipt.get("status"),
        "context_config_sha256": _semantic_sha256(config_payload),
        "context_registry_sha256": _semantic_sha256(
            sorted(context_rows, key=lambda row: row["plant_id"])
        ),
        "historical_source": config["source"],
        "historical_thresholds": {
            "sparse_density_lt_plants_m2": config[
                "sparse_density_max_exclusive"
            ],
            "dense_density_gt_plants_m2": config[
                "dense_density_min_exclusive"
            ],
            "small_patch_lt_flowering_plants": config["patch_boundary_exclusive"],
            "large_patch_gt_flowering_plants": config["patch_boundary_exclusive"],
        },
        "analysis_state": "NATURAL_POLLINATION_PLUS_PREDATOR_EXPOSED",
        "n_p2_plants": len(context),
        "n_plants_with_natural_exposed_rows": len(natural_exposed),
        "historical_context_cell_n": n_by_cell,
        "historical_context_cell_summary": cell_summaries,
        "historical_comparison_modelable": modelable,
        "historical_pattern_contrasts": contrasts,
        "historical_pattern_sign_checks": sign_checks,
        "plant_level_secondary_data": sorted(
            classified_plants,
            key=lambda row: row["plant_id"],
        ),
        "status": status,
        "claim_ceiling": [
            "secondary_ecological_context_only",
            "patch_density_and_patch_size_are_observational_not_randomized",
            "does_not_change_or_rescue_primary_W0_W5",
            "does_not_claim_context_causes_optimum_displacement",
            "does_not_test_context_moderation_of_state_optima_without_separate_power",
            "historical_pattern_comparison_uses_Xia2013_thresholds_not_posthoc_cutpoints",
            "natural_EXPOSED_state_only_for_historical_comparability",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Test whether natural predator pressure in the P. rex P2 cohort "
            "recovers the predeclared Xia et al. 2013 density-by-patch-size pattern "
            "without altering the primary W0-W5 analysis"
        )
    )
    parser.add_argument("completed_p2_csv", type=Path)
    parser.add_argument("p2_surface_receipt_json", type=Path)
    parser.add_argument("context_registry_csv", type=Path)
    parser.add_argument("context_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        surface.read_rows(args.completed_p2_csv),
        _load_json(args.p2_surface_receipt_json),
        _read_context(args.context_registry_csv),
        _load_json(args.context_config_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
