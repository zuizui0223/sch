"""Build an abstract-free machine-assistance packet for SCH PRISMA screening.

The packet is *not* a screening decision. For each identified candidate it
refetches the OpenAlex work, reconstructs the abstract only in memory, records
where the three registered concepts were matched, and assigns a review
priority. Abstract text is never written. Formal title/abstract decision and
reason fields remain blank for human adjudication.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re
import time

try:  # direct CLI execution from scripts/
    import harvest_sch_prisma_candidates as v1
    import harvest_sch_prisma_candidates_v2 as v2
except ModuleNotFoundError:  # imported as scripts.*
    from scripts import harvest_sch_prisma_candidates as v1
    from scripts import harvest_sch_prisma_candidates_v2 as v2


KNOWN_ANCHOR_DOIS = {
    "10.1093/aob/mcad064",
    "10.1890/11-0825.1",
    "10.1371/journal.pone.0098755",
    "10.1093/aob/mcq045",
    "10.1038/s41467-018-03792-x",
    "10.7554/elife.07641",
    "10.1111/j.1600-0706.2013.20780.x",
    "10.3732/ajb.1400171",
}

OUTPUT_FIELDS = (
    "record_id",
    "doi",
    "title",
    "year",
    "openalex_id",
    "query_ids",
    "openalex_work_type",
    "known_anchor",
    "title_floral",
    "title_pollinator",
    "title_antagonist",
    "abstract_floral",
    "abstract_pollinator",
    "abstract_antagonist",
    "title_floral_matches",
    "title_pollinator_matches",
    "title_antagonist_matches",
    "abstract_floral_matches",
    "abstract_pollinator_matches",
    "abstract_antagonist_matches",
    "machine_priority",
    "machine_note",
    "formal_title_abstract_decision",
    "formal_title_abstract_reason",
)


def _match_terms(pattern: re.Pattern[str], text: str) -> str:
    values = {" ".join(match.group(0).lower().split()) for match in pattern.finditer(text)}
    return ";".join(sorted(values))


def _flags(text: str) -> dict[str, bool]:
    return {
        "floral": bool(v2.FLORAL_RE.search(text)),
        "pollinator": bool(v2.POLLINATOR_RE.search(text)),
        "antagonist": bool(v2.ANTAGONIST_RE.search(text)),
    }


def _priority(*, doi: str, title_flags: dict[str, bool]) -> tuple[str, str]:
    if doi in KNOWN_ANCHOR_DOIS:
        return "KNOWN_ANCHOR", "Frozen source-adjudicated anchor; use as a screening sensitivity control."
    n = sum(title_flags.values())
    if n == 3:
        return "HIGH_TITLE_TRIPLE", "All three registered concepts occur in the title."
    if n == 2:
        return "HIGH_TITLE_PAIR", "Two registered concepts occur in the title; inspect abstract/context."
    if n == 1:
        return "MEDIUM_TITLE_ONE", "One registered concept occurs in the title; other concepts are abstract-supported."
    return "ABSTRACT_ONLY", "All registered concepts are recovered only after abstract information is considered."


def _openalex_api_url(openalex_id: str) -> str:
    work_id = openalex_id.rstrip("/").rsplit("/", 1)[-1]
    if not work_id.startswith("W"):
        raise ValueError(f"invalid OpenAlex work id: {openalex_id!r}")
    return f"https://api.openalex.org/works/{work_id}"


def build_packet(batch_csv: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    with batch_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("screening batch is empty")

    output: list[dict[str, str]] = []
    priority_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    anchor_ids: list[str] = []

    for source in rows:
        openalex_id = (source.get("openalex_id") or "").strip()
        if not openalex_id:
            raise ValueError(f"{source.get('record_id')}: missing openalex_id")
        item = v1._request_json(_openalex_api_url(openalex_id))
        title = str(item.get("title") or source.get("title") or "").strip()
        abstract = v2.reconstruct_abstract(item.get("abstract_inverted_index"))
        title_flags = _flags(title)
        abstract_flags = _flags(abstract)
        combined = {key: title_flags[key] or abstract_flags[key] for key in title_flags}
        if not all(combined.values()):
            raise ValueError(f"{source['record_id']}: V2 concept-filter drift detected")

        doi = v1.normalize_doi(source.get("doi"))
        priority, note = _priority(doi=doi, title_flags=title_flags)
        work_type = str(item.get("type") or "UNKNOWN")
        known_anchor = doi in KNOWN_ANCHOR_DOIS
        if known_anchor:
            anchor_ids.append(source["record_id"])
        priority_counts[priority] += 1
        type_counts[work_type] += 1

        output.append(
            {
                "record_id": source["record_id"],
                "doi": doi,
                "title": source.get("title", ""),
                "year": source.get("year", ""),
                "openalex_id": openalex_id,
                "query_ids": source.get("query_ids", ""),
                "openalex_work_type": work_type,
                "known_anchor": "YES" if known_anchor else "NO",
                "title_floral": "YES" if title_flags["floral"] else "NO",
                "title_pollinator": "YES" if title_flags["pollinator"] else "NO",
                "title_antagonist": "YES" if title_flags["antagonist"] else "NO",
                "abstract_floral": "YES" if abstract_flags["floral"] else "NO",
                "abstract_pollinator": "YES" if abstract_flags["pollinator"] else "NO",
                "abstract_antagonist": "YES" if abstract_flags["antagonist"] else "NO",
                "title_floral_matches": _match_terms(v2.FLORAL_RE, title),
                "title_pollinator_matches": _match_terms(v2.POLLINATOR_RE, title),
                "title_antagonist_matches": _match_terms(v2.ANTAGONIST_RE, title),
                "abstract_floral_matches": _match_terms(v2.FLORAL_RE, abstract),
                "abstract_pollinator_matches": _match_terms(v2.POLLINATOR_RE, abstract),
                "abstract_antagonist_matches": _match_terms(v2.ANTAGONIST_RE, abstract),
                "machine_priority": priority,
                "machine_note": note,
                "formal_title_abstract_decision": "",
                "formal_title_abstract_reason": "",
            }
        )
        time.sleep(0.03)

    receipt: dict[str, object] = {
        "analysis_id": "sch_prisma_v2_abstract_free_triage_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "batch_file": batch_csv.name,
        "candidate_count": len(output),
        "priority_counts": dict(sorted(priority_counts.items())),
        "openalex_work_type_counts": dict(sorted(type_counts.items())),
        "known_anchor_count": len(anchor_ids),
        "known_anchor_record_ids": sorted(anchor_ids),
        "stored_abstracts": False,
        "formal_decisions_written": False,
        "claim_boundary": (
            "Machine priority and concept-location fields are screening assistance only. "
            "They are not PRISMA inclusion/exclusion decisions and never populate the formal screening fields."
        ),
    }
    return output, receipt


def write_packet(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    args = parser.parse_args(argv)
    rows, receipt = build_packet(args.batch_csv)
    write_packet(args.out_csv, rows)
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "anchors": receipt["known_anchor_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
