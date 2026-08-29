from __future__ import annotations

import csv

import scripts.build_sch_prisma_human_review_queue as queue_mod
import scripts.build_sch_prisma_screening_triage as triage


def _row(record_id: str, priority: str, anchor: str = "NO") -> dict[str, str]:
    row = {field: "" for field in triage.OUTPUT_FIELDS}
    row.update(
        {
            "record_id": record_id,
            "doi": f"10.9999/{record_id[-2:]}",
            "title": f"Candidate {record_id}",
            "year": "2020",
            "openalex_id": f"https://openalex.org/W{record_id[-2:]}",
            "query_ids": "Q01",
            "openalex_work_type": "article",
            "known_anchor": anchor,
            "machine_priority": priority,
        }
    )
    return row


def _write(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=triage.OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_queue_selects_nonanchor_title_triple_and_pair_only(tmp_path) -> None:
    src = tmp_path / "triage.csv"
    _write(
        src,
        [
            _row("SCHPRISMA-000001", "KNOWN_ANCHOR", "YES"),
            _row("SCHPRISMA-000002", "HIGH_TITLE_TRIPLE"),
            _row("SCHPRISMA-000003", "HIGH_TITLE_PAIR"),
            _row("SCHPRISMA-000004", "MEDIUM_TITLE_ONE"),
            _row("SCHPRISMA-000005", "ABSTRACT_ONLY"),
        ],
    )
    queue, receipt = queue_mod.build_queue(src)
    assert [row["record_id"] for row in queue] == ["SCHPRISMA-000002", "SCHPRISMA-000003"]
    assert receipt["selected_record_count"] == 2
    assert receipt["known_anchors_excluded_from_queue"] is True


def test_queue_never_contains_abstract_text_or_prefilled_decision(tmp_path) -> None:
    src = tmp_path / "triage.csv"
    row = _row("SCHPRISMA-000002", "HIGH_TITLE_TRIPLE")
    row["abstract_floral_matches"] = "flowers"
    row["abstract_pollinator_matches"] = "pollinators"
    row["abstract_antagonist_matches"] = "florivores"
    _write(src, [row])
    queue, receipt = queue_mod.build_queue(src)
    assert len(queue) == 1
    assert "abstract" not in {field.lower() for field in queue[0]}
    assert queue[0]["human_title_abstract_decision"] == ""
    assert queue[0]["human_title_abstract_reason"] == ""
    assert receipt["stored_abstracts"] is False
    assert receipt["formal_prisma_decisions_written"] is False


def test_title_triples_sort_before_pairs(tmp_path) -> None:
    src = tmp_path / "triage.csv"
    _write(
        src,
        [
            _row("SCHPRISMA-000010", "HIGH_TITLE_PAIR"),
            _row("SCHPRISMA-000011", "HIGH_TITLE_TRIPLE"),
        ],
    )
    queue, _ = queue_mod.build_queue(src)
    assert queue[0]["machine_priority"] == "HIGH_TITLE_TRIPLE"
    assert queue[0]["review_order"] == "1"
    assert queue[1]["machine_priority"] == "HIGH_TITLE_PAIR"
