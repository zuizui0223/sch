from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_FILES = (
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V1.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V2_FULLTEXT_ADDITIONS.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V3_REMAINING_FULLTEXT.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V4_BATCH1_MEDIUM.csv",
)
DENOMINATOR = 868


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _rows() -> list[dict[str, str]]:
    """Merge cumulative sparse overlays without losing absent schema fields."""
    loaded = [_read(path) for path in DECISION_FILES]
    all_fields = {
        key
        for rows in loaded
        for update in rows
        for key in update
    }
    merged: dict[str, dict[str, str]] = {}
    for rows in loaded:
        for update in rows:
            record_id = update["record_id"]
            row = merged.setdefault(record_id, {key: "" for key in all_fields})
            for key, value in update.items():
                if value:
                    row[key] = value
    return [merged[key] for key in sorted(merged)]


def _positive_geo(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_")


def test_current_title_abstract_state_is_78_screened() -> None:
    rows = _rows()
    assert len(rows) == 78
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 56
    assert ta["EXCLUDE"] == 22
    assert DENOMINATOR - len(rows) == 790


def test_medium_batch_creates_next_fulltext_queue_without_reopening_old_decisions() -> None:
    rows = _rows()
    ft = Counter(row["screen_fulltext"] or "UNSCREENED" for row in rows if row["screen_title_abstract"] == "RETAIN_FULLTEXT")
    assert ft["INCLUDE"] == 22
    assert ft["EXCLUDE"] == 9
    assert ft["UNSCREENED"] == 25
    reasons = Counter(row["screen_fulltext_reason"] for row in rows if row["screen_fulltext"] == "EXCLUDE")
    assert reasons["FT_REVIEW_ONLY_NO_PRIMARY_ROLE"] == 5
    assert reasons["FT_DUPLICATE_DATASET_OR_REPORT"] == 2
    assert reasons["FT_NO_DECLARED_FLORAL_COORDINATE"] == 2


def test_current_evidence_lanes_keep_one_strict_anchor() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 1
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 20
    assert lanes["EVOLUTIONARY_OUTCOME"] == 6
    strict = [row for row in rows if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert [row["record_id"] for row in strict] == ["SCHPRISMA-000031"]


def test_current_jbi_positive_geography_stays_at_six_until_medium_fulltexts_are_coded() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 22
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    expected = [
        "SCHPRISMA-000008",
        "SCHPRISMA-000032",
        "SCHPRISMA-000066",
        "SCHPRISMA-000172",
        "SCHPRISMA-000523",
        "SCHPRISMA-000710",
    ]
    assert geo == expected
    assert receiver == expected


def test_same_code_near_pass_does_not_inflate_strict_count() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    datura = rows["SCHPRISMA-000046"]
    assert datura["A_manipulated"] == "YES_SYNTHETIC_SCENT_AND_ENANTIOMER_MANIPULATION"
    assert datura["pollinator_response_measured"] == "YES_MANDUCA_FEEDING_RESPONSE"
    assert datura["antagonist_response_measured"] == "YES_MANDUCA_OVIPOSITION_RESPONSE"
    assert datura["common_reproductive_outcome"] == "NO_PLANT_REPRODUCTIVE_OUTCOME"
    assert datura["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_decision_provenance_remains_explicit_after_medium_screen() -> None:
    rows = _rows()
    sources = Counter(row["decision_source"] for row in rows)
    assert sources["PRIOR_SOURCE_ADJUDICATION_FULLTEXT_2026-08-30"] == 8
    assert sources["ASSISTED_SOURCE_VERIFIED_PRIMARY_SCREEN_2026-08-30"] == 12
    assert sources["SOURCE_VERIFIED_FULLTEXT_2026-08-30"] == 20
    assert sources["PRIOR_EVOLUTIONARY_SOURCE_ADJUDICATION_2026-08-30"] == 3
    assert sources["ASSISTED_SOURCE_VERIFIED_MEDIUM_SCREEN_2026-08-30"] == 35
