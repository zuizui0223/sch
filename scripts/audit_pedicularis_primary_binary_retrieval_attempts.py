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

    wang_rows = [
        row for row in rows if row["asset_id"] == "PRIMARY_WANG1998_PDF"
    ]
    exact_wang = [
        row for row in wang_rows
        if row["result"] == "EXACT_CITATION_PDF_URL_RECOVERED_DIRECT_GET_HTTP_403"
    ]
    if len(exact_wang) != 1:
        raise ValueError(
            "Wang1998 exact citation_pdf_url retrieval receipt must occur exactly once"
        )
    wang_pdf_url = exact_wang[0]["locator"]
    if (
        wang_pdf_url
        != "https://www.jipb.net/EN/article/downloadArticleFile.do?attachType=PDF&id=25287"
    ):
        raise ValueError("Wang1998 exact citation_pdf_url drifted")
    if not any(
        row["result"] == "ALL_FOUR_KNOWN_PDF_ENDPOINTS_HTTP_403"
        for row in wang_rows
    ):
        raise ValueError(
            "Wang1998 known mirror-endpoint closure receipt is missing"
        )

    jing_rows = [
        row for row in rows if row["asset_id"] == "PRIMARY_JING2013_METHODS"
    ]
    if not any(
        row["result"]
        == "PRIMARY_PUBLISHER_PAGE_FETCHED_SUBSCRIPTION_PREVIEW_ONLY_METHODS_NOT_EXPOSED"
        for row in jing_rows
    ):
        raise ValueError("Jing2013 live primary-publisher preview receipt is missing")

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
        "wang1998_exact_pdf_url": wang_pdf_url,
        "wang1998_direct_pdf_state": (
            "EXACT_URL_KNOWN_ALL_KNOWN_PUBLIC_ENDPOINT_VARIANTS_HTTP_403"
        ),
        "jing2013_primary_page_state": (
            "LIVE_PUBLISHER_PREVIEW_METHODS_NOT_PUBLICLY_EXPOSED"
        ),
        "tang2011_live_host_state": (
            "GLOBETHESIS_REDIRECTS_TO_SUSPENDED_PAGE_NO_BINARY_LINKS"
        ),
        "primary_route_search_stop": {
            "PRIMARY_JING2013_METHODS": (
                "STOP_ABSTRACT_AND_INDEX_SEARCH_RETRY_ONLY_LEGITIMATE_PRIMARY_BINARY"
            ),
            "PRIMARY_WANG1998_PDF": (
                "STOP_URL_DISCOVERY_EXACT_PDF_URL_KNOWN_RETRY_ONLY_LEGITIMATE_BINARY_ROUTE"
            ),
            "PRIMARY_TANG2011_THESIS": (
                "STOP_GLOBETHESIS_RETRIES_USE_ONLY_WUHAN_CNKI_LIBRARY_BINARY"
            ),
        },
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
            "exact_pdf_url_discovery_is_complete_for_Wang1998_but_binary_access_is_not",
            "publisher_preview_does_not_substitute_for_primary_methods",
            "suspended_host_state_is_a_technical_blocker_not_biological_evidence",
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
