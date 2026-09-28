from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CAL_B_RECEIPT_SCHEMA = "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1"
CAL_B_STATUS = "PEDICULARIS_CAL_B_TARGETS_FROZEN"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

EFFECT_GATE_PATHS = {
    "pollination_weight.min_pollen_grain_delta",
    "pollination_weight.min_initial_seed_set_delta",
    "predator_weight.min_early_attack_reduction",
    "predator_weight.min_predation_fraction_reduction",
    "predator_weight.min_final_seed_set_gain",
}


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CAL-C criteria table has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def build(
    cal_b_receipt: dict,
    criteria_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict]:
    if cal_b_receipt.get("receipt_schema_version") != CAL_B_RECEIPT_SCHEMA:
        raise ValueError("CAL-B receipt schema is not recognized")
    if cal_b_receipt.get("status") != CAL_B_STATUS:
        raise ValueError("CAL-B target receipt is not positive")

    population_id = cal_b_receipt.get("population_id")
    season_id = cal_b_receipt.get("season_id")
    targets = cal_b_receipt.get("targets")
    decisions = cal_b_receipt.get("decision_rows")
    if not isinstance(targets, dict) or not isinstance(decisions, list):
        raise ValueError("CAL-B receipt lacks target decision payload")

    decision_by_gate = {
        row["gate_path"]: row
        for row in decisions
        if isinstance(row, dict) and "gate_path" in row
    }

    missing_targets = EFFECT_GATE_PATHS - set(targets)
    if missing_targets:
        raise ValueError(
            "CAL-B receipt lacks effect targets: "
            + ", ".join(sorted(missing_targets))
        )

    out: list[dict[str, str]] = []
    filled: list[str] = []

    for source_row in criteria_rows:
        row = dict(source_row)
        if row.get("population_id") != population_id:
            raise ValueError(
                f"{row.get('criterion_id')} population does not match CAL-B receipt"
            )
        if row.get("season_id") != season_id:
            raise ValueError(
                f"{row.get('criterion_id')} season does not match CAL-B receipt"
            )

        gate_path = row.get("gate_path")
        if gate_path in EFFECT_GATE_PATHS:
            if row.get("boundary") != PLACEHOLDER:
                raise ValueError(
                    f"{gate_path} CAL-C boundary is already populated"
                )
            if row.get("basis_note") != PLACEHOLDER:
                raise ValueError(
                    f"{gate_path} CAL-C basis_note is already populated"
                )
            decision = decision_by_gate.get(gate_path)
            if decision is None:
                raise ValueError(
                    f"CAL-B decision row is missing for {gate_path}"
                )
            row["boundary"] = repr(float(targets[gate_path]))
            row["basis_note"] = (
                "CAL_B_TARGET_FREEZE: "
                + str(decision.get("target_basis_note", "")).strip()
            )
            filled.append(gate_path)

        if row.get("assumed_true_value") != PLACEHOLDER:
            raise ValueError(
                f"{row.get('criterion_id')} assumed_true_value must remain unresolved"
            )
        out.append(row)

    if set(filled) != EFFECT_GATE_PATHS:
        raise ValueError(
            "CAL-C criteria table does not contain all five CAL-B effect gates"
        )

    receipt = {
        "analysis": "pedicularis_cal_b_to_cal_c_boundary_transfer_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_boundaries_transferred": len(filled),
        "transferred_gate_paths": sorted(filled),
        "assumed_true_values_selected": 0,
        "status": "CAL_B_EFFECT_BOUNDARIES_TRANSFERRED_TO_CAL_C",
        "claim_ceiling": [
            "transcription_bridge_only",
            "does_not_choose_CAL_B_target",
            "does_not_choose_CAL_C_assumed_true_value",
            "does_not_generate_sample_size",
        ],
    }
    return out, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty CAL-C criteria table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Transfer the five frozen CAL-B minimum-effect targets into the "
            "matching CAL-C power boundaries without selecting assumed true values"
        )
    )
    parser.add_argument("cal_b_receipt_json", type=Path)
    parser.add_argument("cal_c_criteria_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    rows, receipt = build(
        _load_json(args.cal_b_receipt_json),
        _read_csv(args.cal_c_criteria_csv),
    )
    _write_csv(args.out_csv, rows)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
