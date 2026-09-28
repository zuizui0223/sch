from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_METHOD_PRECEDENTS_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("method precedent ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("method precedent ledger is empty")
    return rows


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)

    ids = [row["precedent_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("method precedent_id must be unique")

    direct_f0 = [
        row["precedent_id"]
        for row in rows
        if row["direct_F0_freeze_eligible"] != "NO"
    ]
    if direct_f0:
        raise ValueError(
            "method precedents must not directly freeze F0 values: "
            + ", ".join(sorted(direct_f0))
        )

    p0 = sorted(
        row["precedent_id"]
        for row in rows
        if "P0" in row["target_stage"]
    )
    p1 = sorted(
        row["precedent_id"]
        for row in rows
        if "P1" in row["target_stage"]
    )
    cal_a = sorted(
        row["precedent_id"]
        for row in rows
        if "CAL_A" in row["target_stage"]
    )
    cal_b = sorted(
        row["precedent_id"]
        for row in rows
        if "CAL_B" in row["target_stage"]
    )

    same_species = sorted(
        row["precedent_id"]
        for row in rows
        if row["direct_P_rex_evidence"].startswith("YES")
    )

    doi_counts = Counter(row["doi"] for row in rows if row["doi"])

    return {
        "analysis": "pedicularis_method_precedent_audit_v1",
        "n_method_precedents": len(rows),
        "n_unique_dois": len(doi_counts),
        "p0_method_precedents": p0,
        "p1_method_precedents": p1,
        "cal_a_method_precedents": cal_a,
        "cal_b_method_precedents": cal_b,
        "same_species_precedents": same_species,
        "n_direct_f0_values": 0,
        "registered_method_gaps_after_recovery": [
            "P_rex_multi_level_realized_exsertion_manipulation",
            "P_rex_same_flower_repeatability",
            "P_rex_pollen_supplementation_effect",
            "P_rex_independent_seed_predator_exclusion",
            "P_rex_independent_G_timing_window",
        ],
        "status": "PEDICULARIS_METHOD_PRECEDENTS_RECOVERED_FOCAL_VALIDATION_STILL_REQUIRED",
        "claim_ceiling": [
            "method_feasibility_and_design_precedent_only",
            "congeneric_effects_are_not_P_rex_effects",
            "same_species_water_drainage_is_not_independent_G",
            "no_method_precedent_directly_freezes_F0",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit Pedicularis experimental method precedents while keeping "
            "them separate from focal-species empirical validation"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
