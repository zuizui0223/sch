"""Build a compact human-review queue from the SCH machine-triage packet.

This selects non-anchor HIGH_TITLE_TRIPLE and HIGH_TITLE_PAIR candidates only.
The queue contains bibliographic identifiers, title, registered concept-hit
summaries and blank human decision fields. It contains no abstract text and no
machine-generated PRISMA decision.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SELECTED_PRIORITIES = {"HIGH_TITLE_TRIPLE", "HIGH_TITLE_PAIR"}
OUTPUT_FIELDS = (
    "review_order",
    "record_id",
    "doi",
    "title",
    "year",
    "openalex_id",
    "query_ids",
    "openalex_work_type",
    "machine_priority",
    "title_floral_matches",
    "title_pollinator_matches",
    "title_antagonist_matches",
    "abstract_floral_matches",
    "abstract_pollinator_matches",
    "abstract_antagonist_matches",
    "human_title_abstract_decision",
    "human_title_abstract_reason",
    "human_note",
)


def build_queue(triage_csv: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    with triage_csv.open(encoding="utf-8", newline="") as handle:
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]
    selected = [
        row
        for row in rows
        if row.get("known_anchor") != "YES" and row.get("machine_priority") in SELECTED_PRIORITIES
    ]
    rank = {"HIGH_TITLE_TRIPLE": 0, "HIGH_TITLE_PAIR": 1}
    selected.sort(key=lambda row: (rank[row["machine_priority"]], row["record_id"]))

    queue: list[dict[str, str]] = []
    for i, row in enumerate(selected, start=1):
        queue.append(
            {
                "review_order": str(i),
                "record_id": row["record_id"],
                "doi": row["doi"],
                "title": row["title"],
                "year": row["year"],
                "openalex_id": row["openalex_id"],
                "query_ids": row["query_ids"],
                "openalex_work_type": row["openalex_work_type"],
                "machine_priority": row["machine_priority"],
                "title_floral_matches": row["title_floral_matches"],
                "title_pollinator_matches": row["title_pollinator_matches"],
                "title_antagonist_matches": row["title_antagonist_matches"],
                "abstract_floral_matches": row["abstract_floral_matches"],
                "abstract_pollinator_matches": row["abstract_pollinator_matches"],
                "abstract_antagonist_matches": row["abstract_antagonist_matches"],
                "human_title_abstract_decision": "",
                "human_title_abstract_reason": "",
                "human_note": "",
            }
        )

    counts = {
        priority: sum(row["machine_priority"] == priority for row in queue)
        for priority in sorted(SELECTED_PRIORITIES)
    }
    receipt: dict[str, object] = {
        "analysis_id": "sch_prisma_v2_batch1_human_review_queue_v1",
        "selected_record_count": len(queue),
        "priority_counts": counts,
        "known_anchors_excluded_from_queue": True,
        "stored_abstracts": False,
        "formal_prisma_decisions_written": False,
        "claim_boundary": (
            "This is a review-order worksheet only. Blank human decision fields must be adjudicated before any record is added to the formal decision overlay."
        ),
    }
    return queue, receipt


def write_queue(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("triage_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    args = parser.parse_args(argv)
    queue, receipt = build_queue(args.triage_csv)
    write_queue(args.out_csv, queue)
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"selected": len(queue), "priority_counts": receipt["priority_counts"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
