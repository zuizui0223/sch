from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATTEMPTS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PRIMARY_BINARY_RETRIEVAL_ATTEMPTS_V1.csv"
)

DIRECT_GAP_ASSETS = {
    "PRIMARY_JING2013_METHODS": "P1",
    "PRIMARY_TANG2011_THESIS": "G",
    "PRIMARY_WANG1998_PDF": "P1",
}

EXTERNAL_PRIOR_ONLY_ASSETS = {
    "RAW_XIA2013_DRYAD",
    "SUPP_SUN2016_MCW097",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("primary-binary retrieval-attempt ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("primary-binary retrieval-attempt ledger is empty")
    return rows


def build(path: Path = DEFAULT_ATTEMPTS) -> dict:
    rows = _read(path)

    ids = [row["attempt_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("attempt_id must be unique")

    asset_counts = Counter(row["asset_id"] for row in rows)
    unknown_assets = set(asset_counts) - (
        set(DIRECT_GAP_ASSETS) | EXTERNAL_PRIOR_ONLY_ASSETS
    )
    if unknown_assets:
        raise ValueError(
            "retrieval ledger contains unregistered primary asset(s): "
            + ", ".join(sorted(unknown_assets))
        )

    direct_states = {}
    for asset, gap in DIRECT_GAP_ASSETS.items():
        asset_rows = [row for row in rows if row["asset_id"] == asset]
        if not asset_rows:
            raise ValueError(f"no retrieval attempt recorded for {asset}")
        states = sorted(
            {row["direct_gap_state_after_attempt"] for row in asset_rows}
        )
        if any(
            state in {"P1_RECOVERED", "G_RECOVERED"}
            for state in states
        ):
            raise ValueError(
                f"{asset} may not be promoted by a retrieval-attempt receipt alone"
            )
        direct_states[asset] = {
            "gap": gap,
            "n_attempts": len(asset_rows),
            "states": states,
            "latest_allowed_action": asset_rows[-1]["next_allowed_action"],
        }

    dryad_rows = [
        row for row in rows if row["asset_id"] == "RAW_XIA2013_DRYAD"
    ]
    dryad_results = {row["result"] for row in dryad_rows}
    if "HTTP_403" not in dryad_results:
        raise ValueError("Dryad file-stream 403 receipt is missing")
    if "DOWNLOAD_ENDPOINT_REQUIRES_BEARER_AUTHENTICATION" not in dryad_results:
        raise ValueError("Dryad API-authentication receipt is missing")

    tang_rows = [
        row for row in rows if row["asset_id"] == "PRIMARY_TANG2011_THESIS"
    ]
    if not any(
        "NATURAL_HISTORY" in row["direct_gap_state_after_attempt"]
        for row in tang_rows
    ):
        raise ValueError(
            "Tang thesis citation-role audit must preserve natural-history-only state"
        )

    external_states = {
        asset: sorted(
            {
                row["direct_gap_state_after_attempt"]
                for row in rows
                if row["asset_id"] == asset
            }
        )
        for asset in sorted(EXTERNAL_PRIOR_ONLY_ASSETS)
    }

    return {
        "analysis": "pedicularis_primary_binary_retrieval_attempt_audit_v1",
        "n_attempts": len(rows),
        "n_primary_assets_with_attempts": len(asset_counts),
        "attempt_counts_by_asset": dict(sorted(asset_counts.items())),
        "direct_gap_asset_states": direct_states,
        "external_prior_only_asset_states": external_states,
        "dryad_file_stream_id": 46101,
        "dryad_anonymous_download_state": (
            "PUBLIC_FILE_IDENTITY_VERIFIED_BYTES_REQUIRE_AUTHENTICATED_ROUTE"
        ),
        "direct_registered_p1_recovered_from_binary_attempts": False,
        "direct_registered_g_recovered_from_binary_attempts": False,
        "broad_screening_should_resume": False,
        "status": (
            "PRIMARY_BINARY_RETRIEVAL_ATTEMPTS_RECORDED_"
            "DIRECT_GAPS_STILL_OPEN"
        ),
        "claim_ceiling": [
            "technical_retrieval_failure_is_not_evidence_of_biological_absence",
            "primary_treatment_identity_must_be_read_from_primary_methods_before_promotion",
            "authenticated_public_data_retrieval_is_distinct_from_literature_discovery",
            "external_prior_assets_do_not_change_direct_P1_G_state",
            "do_not_repeat_anonymous_routes_already_recorded_as_blocked",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit concrete retrieval attempts for the frozen Pedicularis "
            "primary-binary frontier"
        )
    )
    parser.add_argument("--attempts", type=Path, default=DEFAULT_ATTEMPTS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.attempts)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
