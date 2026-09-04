"""Actions wrapper for the registered SCH PRISMA harvester.

The scientific harvester remains fail-closed. This wrapper separates live API
availability from CI health: it uses an OpenAlex API key when configured and,
when a registered external source is unavailable, writes a machine-readable
BLOCKED receipt instead of falsely claiming a complete identification pass.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
from typing import Any
from urllib.parse import urlencode

import scripts.harvest_sch_prisma_candidates as base


CI_RECEIPT_VERSION = "SCH_PRISMA_CI_WRAPPER_V1"


class SourceUnavailable(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def fetch_openalex_with_key(query: str, *, cap: int, api_key: str) -> tuple[list[base.Candidate], int]:
    if not api_key:
        raise SourceUnavailable("OPENALEX_API_KEY_NOT_CONFIGURED")

    records: list[base.Candidate] = []
    cursor = "*"
    reported_total = 0
    while len(records) < cap and cursor:
        per_page = min(base.PAGE_SIZE, cap - len(records))
        params = urlencode(
            {
                "search": query,
                "per-page": per_page,
                "cursor": cursor,
                "api_key": api_key,
            }
        )
        try:
            payload = base._request_json(f"https://api.openalex.org/works?{params}")
        except base.RetrievalError as exc:
            # Do not propagate the exception text because the URL contains the API key.
            raise SourceUnavailable("OPENALEX_RETRIEVAL_FAILED") from exc

        meta = payload.get("meta") or {}
        if not reported_total:
            reported_total = int(meta.get("count") or 0)
        items = payload.get("results") or []
        if not items:
            break
        for item in items:
            title = str(item.get("title") or "").strip()
            if not title:
                continue
            records.append(
                base.Candidate(
                    doi=base.normalize_doi(item.get("doi")),
                    title=title,
                    year=str(item.get("publication_year") or ""),
                    venue=base._openalex_venue(item),
                    openalex_id=str(item.get("id") or ""),
                )
            )
            if len(records) >= cap:
                break
        cursor = str(meta.get("next_cursor") or "")
        # Keep the Actions job well below burst-rate behaviour even with a key.
        time.sleep(0.25)
    return records, reported_total


def _merge_records(
    merged: dict[str, base.Candidate],
    records: list[base.Candidate],
    *,
    database: str,
    query_id: str,
) -> None:
    for candidate in records:
        candidate.source_databases.add(database)
        candidate.query_ids.add(query_id)
        key = base.dedup_key(candidate)
        if key in merged:
            base.merge_candidate(merged[key], candidate)
        else:
            merged[key] = candidate


def harvest_ci(*, cap: int = base.DEFAULT_CAP, openalex_api_key: str | None = None) -> tuple[list[base.Candidate], dict[str, Any]]:
    if cap < 1:
        raise ValueError("cap must be >= 1")

    key = (openalex_api_key if openalex_api_key is not None else os.getenv("OPENALEX_API_KEY", "")).strip()
    merged: dict[str, base.Candidate] = {}
    query_receipts: list[dict[str, Any]] = []
    raw_hits = 0
    failures: list[dict[str, str]] = []

    for query_id, query in base.QUERY_REGISTRY:
        for database in ("OPENALEX", "CROSSREF"):
            try:
                if database == "OPENALEX":
                    records, reported_total = fetch_openalex_with_key(query, cap=cap, api_key=key)
                else:
                    records, reported_total = base.fetch_crossref(query, cap=cap)
                retrieval_status = "OK"
                error_code = ""
            except SourceUnavailable as exc:
                records, reported_total = [], 0
                retrieval_status = "BLOCKED"
                error_code = exc.code
                failures.append({"database": database, "query_id": query_id, "error_code": error_code})
            except base.RetrievalError:
                records, reported_total = [], 0
                retrieval_status = "BLOCKED"
                error_code = f"{database}_RETRIEVAL_FAILED"
                failures.append({"database": database, "query_id": query_id, "error_code": error_code})

            raw_hits += len(records)
            truncated = retrieval_status == "OK" and reported_total > len(records) and len(records) >= cap
            query_receipts.append(
                {
                    "database": database,
                    "query_id": query_id,
                    "query_text": query,
                    "retrieval_status": retrieval_status,
                    "error_code": error_code,
                    "retrieved_hits": len(records),
                    "reported_total_results": reported_total,
                    "registered_cap": cap,
                    "truncated_at_registered_cap": truncated,
                }
            )
            if retrieval_status == "OK":
                _merge_records(merged, records, database=database, query_id=query_id)

    candidates = sorted(
        merged.values(),
        key=lambda row: (base.normalize_title(row.title), row.year, row.doi),
    )
    any_truncated = any(row["truncated_at_registered_cap"] for row in query_receipts)
    if failures:
        completion = "PRISMA_IDENTIFICATION_BLOCKED_EXTERNAL_SOURCE"
    elif any_truncated:
        completion = "PRISMA_IDENTIFICATION_TRUNCATED"
    else:
        completion = "PRISMA_IDENTIFICATION_ONLY"

    receipt = {
        "protocol_version": base.PROTOCOL_VERSION,
        "ci_wrapper_version": CI_RECEIPT_VERSION,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "registered_cap_per_query_database": cap,
        "query_count": len(base.QUERY_REGISTRY),
        "database_count": 2,
        "raw_hits_across_query_database_pairs": raw_hits,
        "deduplicated_records": len(candidates),
        "duplicates_removed_from_query_hit_stream": raw_hits - len(candidates),
        "any_truncated_query": any_truncated,
        "external_source_failures": failures,
        "registered_source_retrieval_complete": not failures and not any_truncated,
        "systematic_completion_status": completion,
        "query_results": query_receipts,
        "claim_boundary": (
            "This is an Actions orchestration receipt for bibliographic identification only. "
            "Any BLOCKED external source or truncated query prevents a registered-source completeness claim. "
            "A green workflow means the harvester and receipt machinery executed; it does not mean PRISMA identification is complete."
        ),
    }
    return candidates, receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    parser.add_argument("--cap", type=int, default=base.DEFAULT_CAP)
    args = parser.parse_args(argv)

    candidates, receipt = harvest_ci(cap=args.cap)
    base.write_candidates(args.out_csv, candidates)
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": receipt["systematic_completion_status"],
                "raw_hits": receipt["raw_hits_across_query_database_pairs"],
                "deduplicated_records": receipt["deduplicated_records"],
                "external_source_failures": len(receipt["external_source_failures"]),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
