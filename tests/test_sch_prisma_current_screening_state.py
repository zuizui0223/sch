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
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V5_BATCH1_MEDIUM_FULLTEXT.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V6_GEOGRAPHY_CORRECTION.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V7_BATCH1_ABSTRACT_ONLY.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V8_BATCH1_ABSTRACT_ONLY_FULLTEXT.csv",
)
DENOMINATOR = 868


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _rows() -> list[dict[str, str]]:
    """Merge cumulative sparse overlays without losing absent schema fields."""
    loaded = [_read(path) for path in DECISION_FILES]
    all_fields = {key for rows in loaded for update in rows for key in update}
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


def test_batch1_is_complete_and_total_title_abstract_state_is_109_screened() -> None:
    rows = _rows()
    assert len(rows) == 109
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 69
    assert ta["EXCLUDE"] == 40
    assert DENOMINATOR - len(rows) == 759
    batch1_ids = {f"SCHPRISMA-{i:06d}" for i in range(1, 101)}
    decided_ids = {row["record_id"] for row in rows}
    assert batch1_ids <= decided_ids


def test_all_currently_retained_fulltexts_are_adjudicated() -> None:
    rows = _rows()
    ft = Counter(row["screen_fulltext"] or "UNSCREENED" for row in rows if row["screen_title_abstract"] == "RETAIN_FULLTEXT")
    assert ft["INCLUDE"] == 35
    assert ft["EXCLUDE"] == 34
    assert ft["UNSCREENED"] == 0


def test_current_evidence_lanes_keep_one_strict_anchor() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 1
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 30
    assert lanes["EVOLUTIONARY_OUTCOME"] == 11
    strict = [row for row in rows if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert [row["record_id"] for row in strict] == ["SCHPRISMA-000031"]


def test_jbi_geography_and_receiver_counts_are_not_conflated() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 35
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]
    expected_joint = [
        "SCHPRISMA-000008",
        "SCHPRISMA-000032",
        "SCHPRISMA-000066",
        "SCHPRISMA-000067",
        "SCHPRISMA-000074",
        "SCHPRISMA-000172",
        "SCHPRISMA-000523",
        "SCHPRISMA-000710",
    ]
    assert geo == expected_joint
    assert joint == expected_joint
    assert len(receiver) == 9
    assert "SCHPRISMA-000075" in receiver
    assert "SCHPRISMA-000075" not in geo
    assert "SCHPRISMA-000050" not in geo
    assert "SCHPRISMA-000061" not in geo


def test_same_code_and_disa_near_passes_do_not_inflate_strict_count() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    datura = rows["SCHPRISMA-000046"]
    assert datura["A_manipulated"] == "YES_SYNTHETIC_SCENT_AND_ENANTIOMER_MANIPULATION"
    assert datura["pollinator_response_measured"] == "YES_MANDUCA_FEEDING_RESPONSE"
    assert datura["antagonist_response_measured"] == "YES_MANDUCA_OVIPOSITION_RESPONSE"
    assert datura["common_reproductive_outcome"] == "NO_PLANT_REPRODUCTIVE_OUTCOME"
    assert datura["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"

    disa = rows["SCHPRISMA-000048"]
    assert disa["A_manipulated"] == "YES_PAINT_AND_EXCISION_COLOR_MANIPULATION"
    assert disa["common_reproductive_outcome"] == "YES_FRUIT_SET_FOR_COLOR_MANIPULATION"
    assert "NOT_RESPONSE_TO_DO_A" in disa["antagonist_response_measured"]
    assert disa["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_decision_provenance_remains_explicit_after_batch1_completion() -> None:
    rows = _rows()
    sources = Counter(row["decision_source"] for row in rows)
    assert sources["PRIOR_SOURCE_ADJUDICATION_FULLTEXT_2026-08-30"] == 8
    assert sources["ASSISTED_SOURCE_VERIFIED_PRIMARY_SCREEN_2026-08-30"] == 12
    assert sources["SOURCE_VERIFIED_FULLTEXT_2026-08-30"] == 20
    assert sources["PRIOR_EVOLUTIONARY_SOURCE_ADJUDICATION_2026-08-30"] == 3
    assert sources["ASSISTED_SOURCE_VERIFIED_MEDIUM_SCREEN_2026-08-30"] == 10
    assert sources["SOURCE_VERIFIED_MEDIUM_FULLTEXT_2026-08-30"] == 25
    assert sources["ASSISTED_METADATA_AND_ABSTRACT_SCREEN_2026-08-30"] == 18
    assert sources["SOURCE_VERIFIED_ABSTRACT_ONLY_FULLTEXT_2026-08-30"] == 13
