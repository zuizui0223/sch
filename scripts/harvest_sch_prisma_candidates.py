"""Harvest bibliographic candidates for the SCH JBI systematic-expansion lane.

This script performs *identification only*. It queries the predeclared V1 search
strings against OpenAlex and Crossref, stores bibliographic metadata only,
deduplicates by DOI then normalized title/year, and writes an UNSCREENED
candidate ledger plus a machine-readable identification receipt.

Publisher full text and reconstructed abstracts are intentionally not stored.
Any failed query aborts the run. Any query whose reported result count exceeds
the registered retrieval cap is marked truncated so the receipt cannot be
mistaken for a complete systematic search.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PROTOCOL_VERSION = "SCH_PRISMA_V1"
DEFAULT_CAP = 200
PAGE_SIZE = 100
USER_AGENT = "sch-prisma-identification/1.0 (+https://github.com/zuizui0223/sch)"

QUERY_REGISTRY: tuple[tuple[str, str], ...] = (
    ("Q01", '"floral scent" pollinator herbivore'),
    ("Q02", '"floral scent" pollinator florivore'),
    ("Q03", '"floral scent" pollinator "seed predator"'),
    ("Q04", '"floral scent" pollinator "nectar robber"'),
    ("Q05", '"floral volatile" pollinator herbivore'),
    ("Q06", '"floral color" pollinator herbivore'),
    ("Q07", '"floral colour" pollinator herbivore'),
    ("Q08", '"floral display" pollinator herbivore'),
    ("Q09", '"flower size" pollinator herbivore'),
    ("Q10", '"floral trait" pollinator antagonist'),
    ("Q11", '"floral signal" pollinator antagonist'),
    ("Q12", 'flower pollinator "seed predator" trait'),
    ("Q13", 'flower pollinator "nectar robber" trait'),
    ("Q14", 'fig scent pollinator "non-pollinating wasp"'),
)

OUTPUT_FIELDS = (
    "record_id",
    "doi",
    "title",
    "year",
    "venue",
    "source_databases",
    "query_ids",
    "openalex_id",
    "crossref_url",
    "identification_status",
    "screen_title_abstract",
    "screen_title_abstract_reason",
    "fulltext_status",
    "screen_fulltext",
    "screen_fulltext_reason",
    "evidence_lanes",
    "A_trait",
    "A_manipulated",
    "pollinator_response_measured",
    "antagonist_response_measured",
    "common_reproductive_outcome",
    "selection_form",
    "cue_architecture",
    "evolutionary_level",
    "causal_strength",
    "claim_ceiling",
    "study_region",
    "country_or_ocean_basin",
    "latitude_reported",
    "longitude_reported",
    "spatial_grain",
    "spatial_extent",
    "single_site_vs_multisite",
    "geographic_contrast",
    "receiver_assemblage_contrast",
    "biogeographic_context",
    "historical_or_phylogenetic_context",
    "notes",
)


@dataclass
class Candidate:
    doi: str
    title: str
    year: str
    venue: str = ""
    openalex_id: str = ""
    crossref_url: str = ""
    source_databases: set[str] = field(default_factory=set)
    query_ids: set[str] = field(default_factory=set)


class RetrievalError(RuntimeError):
    pass


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    doi = value.strip().lower()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.strip()


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    text = value.casefold()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def dedup_key(candidate: Candidate) -> str:
    if candidate.doi:
        return f"doi:{candidate.doi}"
    return f"titleyear:{normalize_title(candidate.title)}|{candidate.year}"


def _request_json(url: str, *, retries: int = 3, timeout: int = 45) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            with urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # network/service errors are fail-closed
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    raise RetrievalError(f"failed after {retries} attempts: {url}: {last_error}")


def _openalex_venue(item: dict[str, Any]) -> str:
    primary = item.get("primary_location") or {}
    source = primary.get("source") or {}
    return str(source.get("display_name") or "")


def fetch_openalex(query: str, *, cap: int) -> tuple[list[Candidate], int]:
    records: list[Candidate] = []
    cursor = "*"
    reported_total = 0
    while len(records) < cap and cursor:
        per_page = min(PAGE_SIZE, cap - len(records))
        params = urlencode({"search": query, "per-page": per_page, "cursor": cursor})
        payload = _request_json(f"https://api.openalex.org/works?{params}")
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
            doi = normalize_doi(item.get("doi"))
            year = str(item.get("publication_year") or "")
            records.append(
                Candidate(
                    doi=doi,
                    title=title,
                    year=year,
                    venue=_openalex_venue(item),
                    openalex_id=str(item.get("id") or ""),
                )
            )
            if len(records) >= cap:
                break
        cursor = str(meta.get("next_cursor") or "")
        time.sleep(0.08)
    return records, reported_total


def _crossref_year(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        value = item.get(key) or {}
        parts = value.get("date-parts") or []
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def fetch_crossref(query: str, *, cap: int) -> tuple[list[Candidate], int]:
    records: list[Candidate] = []
    offset = 0
    reported_total = 0
    select = "DOI,title,published-print,published-online,published,issued,created,container-title,URL"
    while len(records) < cap:
        rows = min(PAGE_SIZE, cap - len(records))
        params = urlencode(
            {
                "query.bibliographic": query,
                "rows": rows,
                "offset": offset,
                "select": select,
            }
        )
        payload = _request_json(f"https://api.crossref.org/works?{params}")
        message = payload.get("message") or {}
        if not reported_total:
            reported_total = int(message.get("total-results") or 0)
        items = message.get("items") or []
        if not items:
            break
        for item in items:
            titles = item.get("title") or []
            title = str(titles[0] if titles else "").strip()
            if not title:
                continue
            venues = item.get("container-title") or []
            records.append(
                Candidate(
                    doi=normalize_doi(item.get("DOI")),
                    title=title,
                    year=_crossref_year(item),
                    venue=str(venues[0] if venues else ""),
                    crossref_url=str(item.get("URL") or ""),
                )
            )
            if len(records) >= cap:
                break
        offset += len(items)
        if len(items) < rows:
            break
        time.sleep(0.08)
    return records, reported_total


def merge_candidate(existing: Candidate, incoming: Candidate) -> Candidate:
    if not existing.doi and incoming.doi:
        existing.doi = incoming.doi
    if not existing.venue and incoming.venue:
        existing.venue = incoming.venue
    if not existing.year and incoming.year:
        existing.year = incoming.year
    if not existing.openalex_id and incoming.openalex_id:
        existing.openalex_id = incoming.openalex_id
    if not existing.crossref_url and incoming.crossref_url:
        existing.crossref_url = incoming.crossref_url
    existing.source_databases |= incoming.source_databases
    existing.query_ids |= incoming.query_ids
    return existing


def harvest(*, cap: int = DEFAULT_CAP) -> tuple[list[Candidate], dict[str, Any]]:
    if cap < 1:
        raise ValueError("cap must be >= 1")
    merged: dict[str, Candidate] = {}
    query_receipts: list[dict[str, Any]] = []
    raw_hits = 0

    for query_id, query in QUERY_REGISTRY:
        for database, fetcher in (("OPENALEX", fetch_openalex), ("CROSSREF", fetch_crossref)):
            records, reported_total = fetcher(query, cap=cap)
            raw_hits += len(records)
            query_receipts.append(
                {
                    "database": database,
                    "query_id": query_id,
                    "query_text": query,
                    "retrieved_hits": len(records),
                    "reported_total_results": reported_total,
                    "registered_cap": cap,
                    "truncated_at_registered_cap": reported_total > len(records) and len(records) >= cap,
                }
            )
            for candidate in records:
                candidate.source_databases.add(database)
                candidate.query_ids.add(query_id)
                key = dedup_key(candidate)
                if key in merged:
                    merge_candidate(merged[key], candidate)
                else:
                    merged[key] = candidate

    candidates = sorted(
        merged.values(),
        key=lambda row: (normalize_title(row.title), row.year, row.doi),
    )
    receipt = {
        "protocol_version": PROTOCOL_VERSION,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "registered_cap_per_query_database": cap,
        "query_count": len(QUERY_REGISTRY),
        "database_count": 2,
        "raw_hits_across_query_database_pairs": raw_hits,
        "deduplicated_records": len(candidates),
        "duplicates_removed_from_query_hit_stream": raw_hits - len(candidates),
        "any_truncated_query": any(row["truncated_at_registered_cap"] for row in query_receipts),
        "systematic_completion_status": (
            "PRISMA_IDENTIFICATION_TRUNCATED"
            if any(row["truncated_at_registered_cap"] for row in query_receipts)
            else "PRISMA_IDENTIFICATION_ONLY"
        ),
        "query_results": query_receipts,
        "claim_boundary": (
            "This receipt covers automated bibliographic identification only. It does not constitute title/abstract or full-text screening, prevalence estimation, or scientific inclusion. Any truncated query blocks a completeness claim."
        ),
    }
    return candidates, receipt


def write_candidates(path: Path, candidates: list[Candidate]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for index, candidate in enumerate(candidates, start=1):
            row = {field: "" for field in OUTPUT_FIELDS}
            row.update(
                {
                    "record_id": f"SCHPRISMA-{index:06d}",
                    "doi": candidate.doi,
                    "title": candidate.title,
                    "year": candidate.year,
                    "venue": candidate.venue,
                    "source_databases": ";".join(sorted(candidate.source_databases)),
                    "query_ids": ";".join(sorted(candidate.query_ids)),
                    "openalex_id": candidate.openalex_id,
                    "crossref_url": candidate.crossref_url,
                    "identification_status": "UNSCREENED",
                }
            )
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP)
    args = parser.parse_args(argv)

    candidates, receipt = harvest(cap=args.cap)
    write_candidates(args.out_csv, candidates)
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": receipt["systematic_completion_status"],
        "raw_hits": receipt["raw_hits_across_query_database_pairs"],
        "deduplicated_records": receipt["deduplicated_records"],
        "any_truncated_query": receipt["any_truncated_query"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
