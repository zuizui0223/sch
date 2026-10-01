from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FRONTIER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PRIMARY_BINARY_RETRIEVAL_FRONTIER_V1.csv"
)

EXPECTED_PRIORITY = [
    "PRIMARY_JING2013_METHODS",
    "PRIMARY_TANG2011_THESIS",
    "PRIMARY_WANG1998_PDF",
    "RAW_XIA2013_DRYAD",
    "SUPP_SUN2016_MCW097",
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("primary-binary retrieval frontier has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("primary-binary retrieval frontier is empty")
    return rows


def _is_retrieved(state: str) -> bool:
    return any(
        token in state
        for token in (
            "BINARY_RETRIEVED",
            "FULL_TEXT_INGESTED",
            "WORKBOOK_INGESTED",
            "SUPPLEMENT_INGESTED",
        )
    )


def build(path: Path = DEFAULT_FRONTIER) -> dict:
    rows = _read(path)

    ids = [row["asset_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("asset_id must be unique")
    if ids != EXPECTED_PRIORITY:
        raise ValueError(
            "retrieval frontier priority/order drift: "
            f"expected={EXPECTED_PRIORITY}, actual={ids}"
        )

    direct_candidates = [
        row["asset_id"]
        for row in rows
        if row["could_change_direct_gap"] != "NO"
    ]
    non_direct_assets = [
        row["asset_id"]
        for row in rows
        if row["could_change_direct_gap"] == "NO"
    ]
    retrieved = [
        row["asset_id"]
        for row in rows
        if _is_retrieved(row["current_access_state"])
    ]
    retrieved_direct_candidates = [
        row["asset_id"]
        for row in rows
        if (
            row["could_change_direct_gap"] != "NO"
            and _is_retrieved(row["current_access_state"])
        )
    ]

    if retrieved_direct_candidates:
        status = "PRIMARY_DIRECT_GAP_BINARY_AVAILABLE_REAUDIT_REQUIRED"
        next_action = (
            "Audit only the newly retrieved primary binary against its explicit "
            "promotion condition before changing P1/G status."
        )
    elif retrieved:
        status = "PRIMARY_NON_DIRECT_BINARY_AVAILABLE_PRIOR_REANALYSIS_REQUIRED"
        next_action = (
            "Audit retrieved raw/supplement files as external priors while "
            "keeping direct focal gaps open; field calibration remains primary."
        )
    else:
        status = (
            "LITERATURE_EXPANSION_STOPPED_PENDING_PRIMARY_BINARY_OR_FIELD_DATA"
        )
        next_action = (
            "Do not expand congeneric/general literature screening. Proceed with "
            "the focal calibration field package; retry only the five named "
            "primary assets through legitimate binary/library routes."
        )

    return {
        "analysis": "pedicularis_primary_binary_retrieval_frontier_v1",
        "n_primary_assets": len(rows),
        "priority_order": ids,
        "n_assets_that_could_change_direct_gap": len(direct_candidates),
        "direct_gap_candidate_assets": direct_candidates,
        "n_external_prior_only_assets": len(non_direct_assets),
        "external_prior_only_assets": non_direct_assets,
        "n_retrieved_assets": len(retrieved),
        "retrieved_assets": retrieved,
        "n_retrieved_direct_gap_candidates": len(retrieved_direct_candidates),
        "retrieved_direct_gap_candidates": retrieved_direct_candidates,
        "general_literature_expansion_permitted": False,
        "congeneric_prior_expansion_permitted": False,
        "field_calibration_is_primary_path": not bool(
            retrieved_direct_candidates
        ),
        "status": status,
        "next_action": next_action,
        "claim_ceiling": [
            "retrieval_failure_is_not_proof_that_the_primary_file_does_not_exist",
            "only_primary_method_text_can_resolve_Jing2013_treatment_identity",
            "observational_raw_data_cannot_create_randomized_G",
            "aggregate_supplements_cannot_create_missing_interventions",
            "no_further_congeneric_screening_without_new_direct_gap_rationale",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the small set of primary Pedicularis binaries that remain "
            "worth retrieving before further literature expansion"
        )
    )
    parser.add_argument("--frontier", type=Path, default=DEFAULT_FRONTIER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.frontier)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
