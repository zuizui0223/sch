from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
NOT_APPLICABLE = "NOT_APPLICABLE"
CALIBRATION_STATUS = "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"
REPEATABILITY_STATUS = "CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION"
OBSERVED_FIELDS = ("n", "mean", "q05", "median", "q95")


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CAL-A target template has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _resolve_path(payload: dict, dotted_path: str) -> object:
    current: object = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"payload lacks source path {dotted_path!r}")
        current = current[part]
    return current


def build(
    calibration_summary: dict,
    repeatability_summary: dict,
    target_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict]:
    if calibration_summary.get("status") != CALIBRATION_STATUS:
        raise ValueError("CAL-A materialization requires threshold-free calibration summary")
    if calibration_summary.get("thresholds_selected") is not False:
        raise ValueError("calibration summary must not have selected thresholds")
    if calibration_summary.get("confirmatory_receipt_generated") is not False:
        raise ValueError("calibration summary must not be confirmatory evidence")

    if repeatability_summary.get("status") != REPEATABILITY_STATUS:
        raise ValueError("CAL-A materialization requires repeatability-only summary")
    if repeatability_summary.get("thresholds_selected") is not False:
        raise ValueError("repeatability summary must not have selected thresholds")
    if repeatability_summary.get("confirmatory_receipt_generated") is not False:
        raise ValueError("repeatability summary must not be confirmatory evidence")

    cal_context = (
        calibration_summary.get("population_id"),
        calibration_summary.get("season_id"),
    )
    rep_context = (
        repeatability_summary.get("population_id"),
        repeatability_summary.get("season_id"),
    )
    if cal_context != rep_context:
        raise ValueError("calibration and repeatability summaries must share population and season")
    population_id, season_id = cal_context
    if not isinstance(population_id, str) or not population_id:
        raise ValueError("CAL-A population_id is missing")
    if not isinstance(season_id, str) or not season_id:
        raise ValueError("CAL-A season_id is missing")

    out: list[dict[str, str]] = []
    n_noise = 0
    n_no_noise = 0

    for source_row in target_rows:
        row = dict(source_row)
        decision_id = row.get("decision_id", "")
        if not decision_id:
            raise ValueError("decision_id is required")

        for field in (
            "target_value",
            "target_basis_note",
            "frozen_before_confirmatory_data",
            "frozen_at_utc",
            "status",
        ):
            if row.get(field) != PLACEHOLDER:
                raise ValueError(
                    f"{decision_id}.{field} must remain unresolved during materialization"
                )

        observed = _resolve_path(
            calibration_summary,
            row["calibration_source_path"],
        )
        if not isinstance(observed, dict):
            raise ValueError(f"{decision_id} observed source is not a summary object")
        for field in OBSERVED_FIELDS:
            if field not in observed or observed[field] is None:
                raise ValueError(f"{decision_id} observed source lacks {field}")

        row["population_id"] = population_id
        row["season_id"] = season_id
        row["observed_n"] = str(observed["n"])
        row["observed_mean"] = repr(float(observed["mean"]))
        row["observed_q05"] = repr(float(observed["q05"]))
        row["observed_median"] = repr(float(observed["median"]))
        row["observed_q95"] = repr(float(observed["q95"]))

        rep_path = row.get("repeatability_source_path", "")
        if rep_path == NOT_APPLICABLE:
            if row.get("measurement_noise_q95") != NOT_APPLICABLE:
                raise ValueError(
                    f"{decision_id} measurement_noise_q95 must be {NOT_APPLICABLE}"
                )
            n_no_noise += 1
        else:
            if not rep_path or rep_path == PLACEHOLDER:
                raise ValueError(f"{decision_id} repeatability source is unresolved")
            value = _resolve_path(repeatability_summary, rep_path)
            try:
                numeric = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{decision_id} repeatability q95 is not numeric"
                ) from exc
            if numeric < 0:
                raise ValueError(f"{decision_id} repeatability q95 must be >= 0")
            row["measurement_noise_q95"] = repr(numeric)
            n_noise += 1

        out.append(row)

    receipt = {
        "analysis": "pedicularis_cal_a_observed_materialization_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_target_decisions": len(out),
        "n_with_measurement_noise_q95": n_noise,
        "n_without_direct_repeatability_metric": n_no_noise,
        "targets_selected": 0,
        "status": "CAL_A_OBSERVED_AND_REPEATABILITY_MATERIALIZED_TARGETS_UNFROZEN",
        "claim_ceiling": [
            "observed_and_measurement_noise_context_only",
            "does_not_choose_minimum_separation",
            "does_not_choose_equivalence_margin",
            "does_not_generate_confirmatory_receipt",
        ],
    }
    return out, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty CAL-A target table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Copy Pedicularis CAL-A pilot descriptors and repeatability q95 "
            "into the margin/separation decision table without selecting targets"
        )
    )
    parser.add_argument("calibration_summary_json", type=Path)
    parser.add_argument("repeatability_summary_json", type=Path)
    parser.add_argument("target_template_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    rows, receipt = build(
        _load_json(args.calibration_summary_json),
        _load_json(args.repeatability_summary_json),
        _read_csv(args.target_template_csv),
    )
    _write_csv(args.out_csv, rows)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
