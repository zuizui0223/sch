from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_FOCAL_DIRECT_EVIDENCE_SEARCH_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("focal direct-evidence search ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("focal direct-evidence search ledger is empty")
    return rows


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)

    ids = [row["gap_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("gap_id must be unique")

    p1 = [
        row for row in rows
        if row["registered_target"] == "P_rex_pollination_supplementation_effect"
    ]
    g = [
        row for row in rows
        if row["registered_target"]
        == "independent_seed_predator_exclusion_with_water_y_fixed"
    ]
    repeatability = [
        row for row in rows
        if row["registered_target"]
        == "same_flower_repeatability_for_registered_P0_metrics"
    ]
    p0 = [
        row for row in rows
        if row["registered_target"]
        == "multi_level_P_rex_realized_exsertion_manipulation"
    ]

    direct_p1 = [
        row for row in p1
        if row["qualification_status"] == "DIRECT_REGISTERED_P1_RECOVERED"
    ]
    direct_g = [
        row for row in g
        if row["qualification_status"] == "DIRECT_REGISTERED_G_RECOVERED"
    ]
    direct_repeatability = [
        row for row in repeatability
        if row["qualification_status"] == "DIRECT_SAME_FLOWER_REPEATABILITY_RECOVERED"
    ]
    direct_p0 = [
        row for row in p0
        if row["qualification_status"] == "DIRECT_MULTI_LEVEL_P0_RECOVERED"
    ]

    jing = next(
        row for row in rows
        if row["gap_id"] == "P1_JING2013"
    )
    if "TREATMENT_IDENTITY_UNRESOLVED" not in jing["qualification_status"]:
        raise ValueError(
            "Jing2013 hand-pollination evidence must remain unresolved until "
            "the primary methods classify the treatment"
        )

    water = next(
        row for row in rows
        if row["gap_id"] == "G_SUN2015"
    )
    if "WRONG_G_AXIS" not in water["qualification_status"]:
        raise ValueError(
            "Sun2015 water manipulation must remain a wrong-axis G precedent"
        )

    return {
        "analysis": "pedicularis_focal_direct_evidence_search_audit_v1",
        "n_search_rows": len(rows),
        "n_p1_sources_checked": len(p1),
        "n_independent_g_sources_checked": len(g),
        "n_repeatability_sources_checked": len(repeatability),
        "n_p0_direct_sources_checked": len(p0),
        "direct_registered_p1_recovered": bool(direct_p1),
        "direct_registered_g_recovered": bool(direct_g),
        "direct_same_flower_repeatability_recovered": bool(
            direct_repeatability
        ),
        "direct_multi_level_p0_recovered": bool(direct_p0),
        "p1_hand_pollination_treatment_identity_status": jing[
            "qualification_status"
        ],
        "remaining_focal_direct_gaps": [
            "P_rex_multi_level_realized_exsertion_manipulation",
            "P_rex_same_flower_repeatability",
            "P_rex_registered_pollination_supplementation_effect",
            "P_rex_independent_seed_predator_exclusion",
            "P_rex_independent_G_timing_window",
        ],
        "status": (
            "FOCAL_DIRECT_EVIDENCE_SEARCHED_"
            "REGISTERED_CALIBRATION_STILL_REQUIRED"
        ),
        "claim_ceiling": [
            "absence_of_recovery_is_not_proof_of_absence",
            "hand_pollination_is_not_relabelled_as_supplementation_without_primary_methods",
            "water_drainage_is_not_independent_G",
            "different_flowers_per_plant_are_not_same_flower_repeatability",
            "congeneric_manipulation_is_not_focal_P0_validation",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit focal Pedicularis rex direct-evidence searches and keep "
            "unresolved treatments from being silently promoted"
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
