"""Harvest the SCH PRISMA V2 title/abstract candidate universe.

V2 uses OpenAlex only for discovery, fully retrieves each frozen V1 query up to
a cap above the largest V1 OpenAlex result count, and applies a predeclared
three-block title/abstract concept filter in memory. Reconstructed abstracts
are never written to disk.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import time
from typing import Any
from urllib.parse import urlencode

try:  # direct CLI execution from scripts/
    import harvest_sch_prisma_candidates as v1
except ModuleNotFoundError:  # import as scripts.harvest_sch_prisma_candidates_v2
    from scripts import harvest_sch_prisma_candidates as v1


PROTOCOL_VERSION = "SCH_PRISMA_V2"
DEFAULT_CAP = 2500
PAGE_SIZE = 200

FLORAL_RE = re.compile(r"\b(?:floral|flower|flowers|blossom|fig|figs|syconium|syconia)\b", re.I)
POLLINATOR_RE = re.compile(r"(?:pollinat\w*|flower\s+visitors?|floral\s+visitors?)", re.I)
ANTAGONIST_RE = re.compile(
    r"(?:herbiv\w*|floriv\w*|seed[-\s]?(?:predat\w*|eat\w*)|"
    r"nectar\s+(?:robb\w*|thie\w*)|antagon\w*|non[-\s]?pollinat\w*|"
    r"parasitoid\w*|parasit\w*|exploit\w*|oviposit\w*)",
    re.I,
)


def reconstruct_abstract(inverted: dict[str, list[int]] | None) -> str:
    if not inverted:
        return ""
    max_position = max((max(pos) for pos in inverted.values() if pos), default=-1)
    if max_position < 0:
        return ""
    words = [""] * (max_position + 1)
    for word, positions in inverted.items():
        for position in positions:
            if 0 <= position < len(words):
                words[position] = word
    return " ".join(word for word in words if word)


def concept_flags(title: str, abstract: str) -> dict[str, bool]:
    text = f"{html.unescape(title)} {abstract}"
    return {
        "floral_signal": bool(FLORAL_RE.search(text)),
        "pollinator": bool(POLLINATOR_RE.search(text)),
        "antagonist": bool(ANTAGONIST_RE.search(text)),
    }


def passes_concept_filter(title: str, abstract: str) -> bool:
    return all(concept_flags(title, abstract).values())


def _venue(item: dict[str, Any]) -> str:
    primary = item.get("primary_location") or {}
    source = primary.get("source") or {}
    return str(source.get("display_name") or "")


def fetch_openalex_v2(
    query: str,
    *,
    cap: int,
) -> tuple[list[v1.Candidate], dict[str, int | bool]]:
    if cap < 1:
        raise ValueError("cap must be >= 1")
    candidates: list[v1.Candidate] = []
    cursor = "*"
    reported_total = 0
    retrieved = 0
    concept_pass = 0

    while retrieved < cap and cursor:
        per_page = min(PAGE_SIZE, cap - retrieved)
        params = urlencode(
            {
                "search": query,
                "per-page": per_page,
                "cursor": cursor,
                "select": "id,doi,title,publication_year,primary_location,abstract_inverted_index",
            }
        )
        payload = v1._request_json(f"https://api.openalex.org/works?{params}")
        meta = payload.get("meta") or {}
        if not reported_total:
            reported_total = int(meta.get("count") or 0)
        items = payload.get("results") or []
        if not items:
            break
        for item in items:
            if retrieved >= cap:
                break
            retrieved += 1
            title = html.unescape(str(item.get("title") or "")).strip()
            if not title:
                continue
            abstract = reconstruct_abstract(item.get("abstract_inverted_index"))
            if not passes_concept_filter(title, abstract):
                continue
            concept_pass += 1
            candidates.append(
                v1.Candidate(
                    doi=v1.normalize_doi(item.get("doi")),
                    title=title,
                    year=str(item.get("publication_year") or ""),
                    venue=_venue(item),
                    openalex_id=str(item.get("id") or ""),
                    source_databases={"OPENALEX"},
                )
            )
        cursor = str(meta.get("next_cursor") or "")
        time.sleep(0.05)

    metrics: dict[str, int | bool] = {
        "reported_total_results": reported_total,
        "retrieved_records": retrieved,
        "concept_pass_hits": concept_pass,
        "concept_filter_fail_hits": retrieved - concept_pass,
        "truncated_at_registered_cap": reported_total > retrieved and retrieved >= cap,
    }
    return candidates, metrics


def harvest(*, cap: int = DEFAULT_CAP) -> tuple[list[v1.Candidate], dict[str, Any]]:
    merged: dict[str, v1.Candidate] = {}
    query_receipts: list[dict[str, Any]] = []
    total_retrieved = 0
    total_pass_hits = 0

    for query_id, query in v1.QUERY_REGISTRY:
        candidates, metrics = fetch_openalex_v2(query, cap=cap)
        total_retrieved += int(metrics["retrieved_records"])
        total_pass_hits += int(metrics["concept_pass_hits"])
        query_receipts.append(
            {
                "query_id": query_id,
                "query_text": query,
                "registered_cap": cap,
                **metrics,
            }
        )
        for candidate in candidates:
            candidate.query_ids.add(query_id)
            key = v1.dedup_key(candidate)
            if key in merged:
                v1.merge_candidate(merged[key], candidate)
            else:
                merged[key] = candidate

    candidates = sorted(
        merged.values(),
        key=lambda row: (v1.normalize_title(row.title), row.year, row.doi),
    )
    truncated = any(bool(row["truncated_at_registered_cap"]) for row in query_receipts)
    receipt = {
        "protocol_version": PROTOCOL_VERSION,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "discovery_database": "OPENALEX",
        "registered_cap_per_query": cap,
        "query_count": len(v1.QUERY_REGISTRY),
        "raw_openalex_records_retrieved": total_retrieved,
        "automated_concept_pass_hits_across_queries": total_pass_hits,
        "automated_concept_filter_fail_hits_across_queries": total_retrieved - total_pass_hits,
        "deduplicated_unscreened_candidates": len(candidates),
        "duplicate_concept_pass_query_hits_removed": total_pass_hits - len(candidates),
        "any_truncated_query": truncated,
        "systematic_completion_status": (
            "PRISMA_V2_IDENTIFICATION_TRUNCATED"
            if truncated
            else "PRISMA_V2_IDENTIFICATION_COMPLETE"
        ),
        "query_results": query_receipts,
        "stored_abstracts": False,
        "crossref_discovery": False,
        "claim_boundary": (
            "V2 COMPLETE means the registered OpenAlex identification/search coordinate was fully retrieved and filtered. "
            "It does not mean title/abstract screening, full-text screening, scientific inclusion, prevalence estimation, or JBI geographic-fit coding is complete."
        ),
    }
    return candidates, receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP)
    args = parser.parse_args(argv)

    try:
        candidates, receipt = harvest(cap=args.cap)
    except Exception as exc:
        failure = {
            "protocol_version": PROTOCOL_VERSION,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            "systematic_completion_status": "PRISMA_V2_RETRIEVAL_FAILED",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_receipt_json.write_text(json.dumps(failure, indent=2), encoding="utf-8")
        raise

    v1.write_candidates(args.out_csv, candidates)
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": receipt["systematic_completion_status"],
                "retrieved": receipt["raw_openalex_records_retrieved"],
                "concept_pass_hits": receipt["automated_concept_pass_hits_across_queries"],
                "deduplicated_candidates": receipt["deduplicated_unscreened_candidates"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
