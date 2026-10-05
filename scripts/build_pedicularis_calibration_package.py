from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


from scripts import evaluate_pedicularis_pollination_weight as p1
from scripts import evaluate_pedicularis_predator_method as gmethod
from scripts import evaluate_pedicularis_stage_p0 as p0
from scripts import summarize_pedicularis_cal_a_repeatability as repeatability
from scripts import summarize_pedicularis_calibration_pilots as calibration
from scripts import summarize_pedicularis_g_event_time_pilot as gtiming
from scripts import validate_pedicularis_cohort_registry as cohort


EXPECTED_DATA_ROLE = {
    "repeatability": "CAL_A",
    "P0": "CAL_A",
    "P1": "CAL_B_P1",
    "G": "CAL_B_G",
    "G_TIMING": "CAL_B_G_TIMING",
}


def _context(rows: list[dict[str, str]], label: str) -> tuple[str, str]:
    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(f"{label} must contain exactly one population and season")
    return next(iter(contexts))


def _registry_by_flower(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["flower_id"]: row for row in rows}


def _check_dataset_registration(
    *,
    label: str,
    rows: list[dict[str, str]],
    expected_role: str,
    registry: dict[str, dict[str, str]],
) -> dict:
    flower_ids = {row["flower_id"] for row in rows}
    missing = sorted(flower_ids - set(registry))
    if missing:
        raise ValueError(
            f"{label} contains flower_id values missing from cohort registry: "
            + ", ".join(missing)
        )

    wrong_role = sorted(
        flower_id
        for flower_id in flower_ids
        if registry[flower_id]["cohort_role"] != expected_role
    )
    if wrong_role:
        raise ValueError(
            f"{label} flower_id values have wrong cohort_role; expected "
            f"{expected_role}: " + ", ".join(wrong_role)
        )

    ineligible = sorted(
        flower_id
        for flower_id in flower_ids
        if registry[flower_id]["threshold_basis_eligible"] != "YES"
        or registry[flower_id]["confirmatory_eligible"] != "NO"
    )
    if ineligible:
        raise ValueError(
            f"{label} calibration rows are not threshold-basis-only: "
            + ", ".join(ineligible)
        )

    return {
        "role": expected_role,
        "n_rows": len(rows),
        "n_flowers": len(flower_ids),
        "flower_ids": sorted(flower_ids),
        "plant_ids": sorted({row["plant_id"] for row in rows}),
    }


def build_package(
    *,
    registry_path: Path,
    repeatability_path: Path,
    p0_path: Path,
    p1_path: Path,
    g_path: Path,
    g_timing_config_path: Path,
    g_timing_path: Path,
) -> tuple[dict, dict, dict]:
    registry_rows = cohort._read(registry_path)
    cohort_receipt = cohort.validate(registry_rows)
    registry = _registry_by_flower(registry_rows)

    repeatability_rows = repeatability.read_rows(repeatability_path)
    p0_rows = p0._read_csv(p0_path)
    p1_rows = p1._read_csv(p1_path)
    g_rows = gmethod.read_rows(g_path)
    g_timing_config = gtiming._read_json(g_timing_config_path)
    g_timing_rows = gtiming._read_csv(g_timing_path)
    g_timing_summary = gtiming.build(g_timing_config, g_timing_rows)

    datasets = {
        "repeatability": repeatability_rows,
        "P0": p0_rows,
        "P1": p1_rows,
        "G": g_rows,
        "G_TIMING": g_timing_rows,
    }

    contexts = {
        label: _context(rows, label)
        for label, rows in datasets.items()
    }
    contexts["registry"] = (
        cohort_receipt["population_id"],
        cohort_receipt["season_id"],
    )
    if len(set(contexts.values())) != 1:
        raise ValueError(
            "repeatability, P0, P1, G, G_TIMING and cohort registry contexts must match exactly: "
            + ", ".join(
                f"{label}={context[0]}/{context[1]}"
                for label, context in sorted(contexts.items())
            )
        )
    population_id, season_id = next(iter(set(contexts.values())))

    dataset_receipts = {
        label: _check_dataset_registration(
            label=label,
            rows=rows,
            expected_role=EXPECTED_DATA_ROLE[label],
            registry=registry,
        )
        for label, rows in datasets.items()
    }

    rep_ids = set(dataset_receipts["repeatability"]["flower_ids"])
    p0_ids = set(dataset_receipts["P0"]["flower_ids"])
    p1_ids = set(dataset_receipts["P1"]["flower_ids"])
    g_ids = set(dataset_receipts["G"]["flower_ids"])
    g_timing_ids = set(dataset_receipts["G_TIMING"]["flower_ids"])

    if not rep_ids <= p0_ids:
        raise ValueError(
            "CAL-A repeatability flower_ids must be a subset of the CAL-A P0 "
            "exploratory flowers so repeated measurements are attached to the "
            "same calibration units"
        )

    lane_flower_ids = {
        "P0": p0_ids,
        "P1": p1_ids,
        "G": g_ids,
        "G_TIMING": g_timing_ids,
    }
    forbidden_overlaps = {
        f"{left}_vs_{right}": lane_flower_ids[left] & lane_flower_ids[right]
        for left, right in itertools.combinations(lane_flower_ids, 2)
    }
    nonempty = {
        key: sorted(values)
        for key, values in forbidden_overlaps.items()
        if values
    }
    if nonempty:
        raise ValueError(
            "calibration lane flower reuse detected outside allowed "
            "repeatability-within-CAL_A overlap: "
            + json.dumps(nonempty, sort_keys=True)
        )

    repeatability_summary = repeatability.build(repeatability_rows)
    calibration_summary = calibration.build(
        p0_path=p0_path,
        p1_path=p1_path,
        g_path=g_path,
        g_timing_config_path=g_timing_config_path,
        g_timing_path=g_timing_path,
    )

    if (
        repeatability_summary["population_id"],
        repeatability_summary["season_id"],
    ) != (population_id, season_id):
        raise ValueError("repeatability summary context drifted during build")
    if (
        calibration_summary["population_id"],
        calibration_summary["season_id"],
    ) != (population_id, season_id):
        raise ValueError("calibration summary context drifted during build")
    if (
        g_timing_summary["population_id"],
        g_timing_summary["season_id"],
    ) != (population_id, season_id):
        raise ValueError("G event-time summary context drifted during build")
    if calibration_summary.get("pilot_summaries", {}).get("G_TIMING") != g_timing_summary:
        raise ValueError("G event-time summary drifted during package assembly")

    receipt = {
        "receipt_schema_version": "SCH_PEDICULARIS_CALIBRATION_PACKAGE_V1",
        "analysis": "pedicularis_calibration_package",
        "population_id": population_id,
        "season_id": season_id,
        "cohort_registry_status": cohort_receipt["status"],
        "cohort_independence_status": cohort_receipt["independence_status"],
        "dataset_registration": {
            label: {
                "role": result["role"],
                "n_rows": result["n_rows"],
                "n_flowers": result["n_flowers"],
                "n_plants": len(result["plant_ids"]),
            }
            for label, result in dataset_receipts.items()
        },
        "allowed_repeatability_p0_overlap_n_flowers": len(rep_ids),
        "cross_lane_flower_overlap_detected": False,
        "repeatability_summary_status": repeatability_summary["status"],
        "calibration_summary_status": calibration_summary["status"],
        "g_event_time_summary_status": g_timing_summary["status"],
        "g_effect_and_timing_flower_overlap_detected": False,
        "status": "PEDICULARIS_CALIBRATION_PACKAGE_READY_FOR_TARGET_FREEZE",
        "unlocked_next_steps": [
            "materialize_and_freeze_CAL_A_targets",
            "materialize_and_freeze_CAL_B_targets",
            "materialize_CAL_C_pilot_SD_provenance",
        ],
        "claim_ceiling": [
            "calibration_package_integrity_only",
            "requires_separate_G_effect_and_natural_event_time_cohorts",
            "does_not_select_thresholds",
            "does_not_validate_P0_P1_or_G",
            "does_not_use_confirmatory_rows",
        ],
    }

    return repeatability_summary, calibration_summary, receipt


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and summarize a Pedicularis CAL-A/B calibration package "
            "against the cohort registry"
        )
    )
    parser.add_argument("cohort_registry", type=Path)
    parser.add_argument("repeatability_csv", type=Path)
    parser.add_argument("p0_csv", type=Path)
    parser.add_argument("p1_csv", type=Path)
    parser.add_argument("g_csv", type=Path)
    parser.add_argument("--g-timing-config", type=Path, required=True)
    parser.add_argument("--g-timing", type=Path, required=True)
    parser.add_argument("--repeatability-out", type=Path, required=True)
    parser.add_argument("--calibration-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    rep, cal, receipt = build_package(
        registry_path=args.cohort_registry,
        repeatability_path=args.repeatability_csv,
        p0_path=args.p0_csv,
        p1_path=args.p1_csv,
        g_path=args.g_csv,
        g_timing_config_path=args.g_timing_config,
        g_timing_path=args.g_timing,
    )
    _write_json(args.repeatability_out, rep)
    _write_json(args.calibration_out, cal)
    _write_json(args.receipt_out, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
