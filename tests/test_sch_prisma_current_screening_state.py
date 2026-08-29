from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V1.csv"
DENOMINATOR = 868


def _rows() -> list[dict[str, str]]:
    with DECISIONS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _positive_geo(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_")


def test_current_title_abstract_state_is_40_screened() -> None:
    rows = _rows()
    assert len(rows) == 40
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 28
    assert ta["EXCLUDE"] == 12
    assert DENOMINATOR - len(rows) == 828


def test_current_fulltext_state_is_six_primary_includes_two_secondary_excludes() -> None:
    rows = _rows()
    ft = Counter(row["screen_fulltext"] or "UNSCREENED" for row in rows if row["screen_title_abstract"] == "RETAIN_FULLTEXT")
    assert ft["INCLUDE"] == 6
    assert ft["EXCLUDE"] == 2
    assert ft["UNSCREENED"] == 20
    excluded = [row for row in rows if row["screen_fulltext"] == "EXCLUDE"]
    assert all(row["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE" for row in excluded)


def test_current_evidence_lanes_keep_one_strict_anchor() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 1
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 5
    assert lanes["EVOLUTIONARY_OUTCOME"] == 2
    strict = [row for row in rows if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert [row["record_id"] for row in strict] == ["SCHPRISMA-000031"]


def test_current_jbi_positive_geography_is_one_of_six_included_primary_studies() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 6
    geo = [row for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    assert [row["record_id"] for row in geo] == ["SCHPRISMA-000172"]
    assert [row["record_id"] for row in receiver] == ["SCHPRISMA-000172"]


def test_decision_provenance_remains_two_explicit_lanes() -> None:
    rows = _rows()
    sources = Counter(row["decision_source"] for row in rows)
    assert sources["PRIOR_SOURCE_ADJUDICATION_FULLTEXT_2026-08-30"] == 8
    assert sources["ASSISTED_SOURCE_VERIFIED_PRIMARY_SCREEN_2026-08-30"] == 32
