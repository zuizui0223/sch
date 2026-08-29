from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_FILES = (
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V1.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V2_FULLTEXT_ADDITIONS.csv",
    ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V3_REMAINING_FULLTEXT.csv",
)
DENOMINATOR = 868


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _rows() -> list[dict[str, str]]:
    """Return cumulative sparse decisions with later overlays taking precedence."""
    merged: dict[str, dict[str, str]] = {}
    for path in DECISION_FILES:
        for update in _read(path):
            record_id = update["record_id"]
            row = merged.setdefault(record_id, {key: "" for key in update})
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


def test_current_title_abstract_state_is_43_screened() -> None:
    rows = _rows()
    assert len(rows) == 43
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 31
    assert ta["EXCLUDE"] == 12
    assert DENOMINATOR - len(rows) == 825


def test_all_currently_retained_fulltexts_are_adjudicated() -> None:
    rows = _rows()
    ft = Counter(row["screen_fulltext"] or "UNSCREENED" for row in rows if row["screen_title_abstract"] == "RETAIN_FULLTEXT")
    assert ft["INCLUDE"] == 22
    assert ft["EXCLUDE"] == 9
    assert ft["UNSCREENED"] == 0
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


def test_current_jbi_positive_geography_has_six_independent_primary_records() -> None:
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


def test_decision_provenance_remains_explicit_after_fulltext_closure() -> None:
    rows = _rows()
    sources = Counter(row["decision_source"] for row in rows)
    assert sources["PRIOR_SOURCE_ADJUDICATION_FULLTEXT_2026-08-30"] == 8
    assert sources["ASSISTED_SOURCE_VERIFIED_PRIMARY_SCREEN_2026-08-30"] == 12
    assert sources["SOURCE_VERIFIED_FULLTEXT_2026-08-30"] == 20
    assert sources["PRIOR_EVOLUTIONARY_SOURCE_ADJUDICATION_2026-08-30"] == 3
