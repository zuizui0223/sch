from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
NOT_APPLICABLE = "NOT_APPLICABLE"
SUMMARY_STATUS = "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("criteria template has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _metric_summary(
    summary: dict,
    lane: str,
    metric_source: str,
) -> tuple[dict, str]:
    pilots = summary.get("pilot_summaries")
    if not isinstance(pilots, dict) or lane not in pilots:
        raise ValueError(f"calibration summary lacks {lane} pilot data")

    if lane == "P0":
        path = (
            f"pilot_summaries.P0.plant_level_gate_metric_distributions."
            f"{metric_source}"
        )
        metrics = pilots["P0"].get("plant_level_gate_metric_distributions")
    elif lane == "P1":
        path = (
            f"pilot_summaries.P1.plant_level_distributions."
            f"{metric_source}"
        )
        metrics = pilots["P1"].get("plant_level_distributions")
    elif lane == "G":
        path = (
            f"pilot_summaries.G.plant_level_distributions."
            f"{metric_source}"
        )
        metrics = pilots["G"].get("plant_level_distributions")
    else:
        raise ValueError(f"unregistered calibration lane: {lane}")

    if not isinstance(metrics, dict) or metric_source not in metrics:
        raise ValueError(
            f"calibration summary lacks metric {metric_source!r} for lane {lane}"
        )
    metric = metrics[metric_source]
    if not isinstance(metric, dict):
        raise ValueError(f"metric summary is not an object: {path}")
    return metric, path


def build(
    calibration_summary: dict,
    criteria_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict]:
    if calibration_summary.get("status") != SUMMARY_STATUS:
        raise ValueError(
            "CAL-C SD materialization requires the threshold-free calibration "
            "pilot summary"
        )
    if calibration_summary.get("thresholds_selected") is not False:
        raise ValueError("calibration summary must not have selected thresholds")
    if calibration_summary.get("confirmatory_receipt_generated") is not False:
        raise ValueError(
            "calibration summary must not be a confirmatory receipt"
        )

    population_id = calibration_summary.get("population_id")
    season_id = calibration_summary.get("season_id")
    if not isinstance(population_id, str) or not population_id:
        raise ValueError("calibration summary population_id is missing")
    if not isinstance(season_id, str) or not season_id:
        raise ValueError("calibration summary season_id is missing")

    lanes = set(calibration_summary.get("available_pilot_lanes") or [])
    if lanes != {"P0", "P1", "G"}:
        raise ValueError(
            "full CAL-C materialization requires P0, P1 and G calibration summaries"
        )

    out: list[dict[str, str]] = []
    n_sd = 0
    n_binomial = 0

    for source_row in criteria_rows:
        row = dict(source_row)
        row["population_id"] = population_id
        row["season_id"] = season_id

        criterion_type = row.get("criterion_type")
        if criterion_type == "NORMAL_BOUND":
            metric, source_path = _metric_summary(
                calibration_summary,
                row["lane"],
                row["metric_source"],
            )
            sd_field = (
                "planning_sd"
                if metric.get("planning_sd") is not None
                else "sd"
            )
            sd = metric.get(sd_field)
            if sd is None:
                raise ValueError(
                    f"pilot planning SD is unavailable for {row['criterion_id']}"
                )
            try:
                sd_value = float(sd)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"pilot planning SD is not numeric for {row['criterion_id']}"
                ) from exc
            if sd_value <= 0:
                raise ValueError(
                    f"pilot planning SD must be > 0 for {row['criterion_id']}"
                )
            row["pilot_sd"] = repr(sd_value)
            row["pilot_sd_source"] = (
                source_path + "." + sd_field
            )
            n_sd += 1
        elif criterion_type == "BINOMIAL_UPPER":
            row["pilot_sd"] = NOT_APPLICABLE
            row["pilot_sd_source"] = NOT_APPLICABLE
            n_binomial += 1
        else:
            raise ValueError(
                f"unsupported criterion_type: {criterion_type}"
            )

        for field in ("boundary", "assumed_true_value", "basis_note"):
            if row.get(field) != PLACEHOLDER:
                raise ValueError(
                    f"criteria template field {field} must remain unresolved "
                    "during pilot-SD materialization"
                )

        out.append(row)

    receipt = {
        "analysis": "pedicularis_cal_c_pilot_sd_materialization_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_criteria": len(out),
        "n_continuous_criteria_with_pilot_sd": n_sd,
        "n_binomial_criteria_without_sd": n_binomial,
        "p1_design_unit": (
            calibration_summary.get("pilot_summaries", {})
            .get("P1", {})
            .get("design_unit")
        ),
        "p1_estimand_family": (
            calibration_summary.get("pilot_summaries", {})
            .get("P1", {})
            .get("estimand_family")
        ),
        "boundaries_selected": 0,
        "assumed_true_values_selected": 0,
        "status": "CAL_C_PILOT_SD_MATERIALIZED_TARGETS_STILL_UNFROZEN",
        "claim_ceiling": [
            "pilot_variability_provenance_only",
            "does_not_choose_gate_boundary",
            "does_not_choose_assumed_true_effect",
            "does_not_choose_familywise_power",
            "does_not_generate_sample_size_until_targets_are_frozen",
        ],
    }
    return out, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty criteria table")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Copy pilot SDs and provenance from the threshold-free Pedicularis "
            "calibration summary into the CAL-C criteria table"
        )
    )
    parser.add_argument("calibration_summary_json", type=Path)
    parser.add_argument("criteria_template_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    rows, receipt = build(
        _load_json(args.calibration_summary_json),
        _read_csv(args.criteria_template_csv),
    )
    _write_csv(args.out_csv, rows)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
