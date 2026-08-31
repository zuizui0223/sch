from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V12_BATCH2_REMAINDER_TITLE_ABSTRACT.csv"


def _version(path: Path) -> int:
    match = re.search(r"_V(\d+)", path.name)
    if not match:
        raise AssertionError(f"unversioned screening decision file: {path.name}")
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    assert [ _version(path) for path in files ] == list(range(1, 13))
    assert files[-1].name == LATEST
    return files


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _merge(files: list[Path]) -> list[dict[str, str]]:
    loaded = [_read(path) for path in files]
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


def _rows() -> list[dict[str, str]]:
    return _merge(_decision_files())


def _positive_geo(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_")


def test_v12_closes_batch2_title_abstract_without_double_screening_prior_anchor() -> None:
    files = _decision_files()
    before_v12 = _merge(files[:-1])
    before_ids = {row["record_id"] for row in before_v12}
    v12 = _read(files[-1])
    v12_ids = {row["record_id"] for row in v12}
    batch2 = {f"SCHPRISMA-{i:06d}" for i in range(101, 201)}

    assert len(v12) == 70
    assert "SCHPRISMA-000172" in before_ids
    assert "SCHPRISMA-000172" not in v12_ids
    assert v12_ids == batch2 - before_ids

    rows = _rows()
    decided_ids = {row["record_id"] for row in rows}
    assert {f"SCHPRISMA-{i:06d}" for i in range(1, 201)} <= decided_ids
    assert len(rows) == 208

    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 130
    assert ta["EXCLUDE"] == 78
    assert DENOMINATOR - len(rows) == 660

    v12_ta = Counter(row["screen_title_abstract"] for row in v12)
    assert v12_ta["RETAIN_FULLTEXT"] == 35
    assert v12_ta["EXCLUDE"] == 35
    reasons = Counter(row["screen_title_abstract_reason"] for row in v12 if row["screen_title_abstract"] == "EXCLUDE")
    assert reasons == {
        "TA_NOT_FLORAL_SIGNAL": 9,
        "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS": 9,
        "TA_NO_ANTAGONIST_COMPONENT": 13,
        "TA_NO_POLLINATOR_COMPONENT": 4,
    }


def test_v12_reopens_only_the_newly_retained_fulltext_queue() -> None:
    rows = _rows()
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 44
    assert ft["EXCLUDE"] == 51
    assert ft["UNSCREENED"] == 35


def test_current_evidence_lanes_keep_two_strict_measurement_architectures() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 38
    assert lanes["EVOLUTIONARY_OUTCOME"] == 12
    strict = [row for row in rows if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert [row["record_id"] for row in strict] == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_jbi_geography_and_receiver_counts_are_not_conflated() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 44
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


def test_v12_decision_provenance_is_explicit() -> None:
    rows = _rows()
    sources = Counter(row["decision_source"] for row in rows)
    assert sources["SOURCE_VERIFIED_BATCH2_FULLTEXT_2026-08-31"] == 16
    assert sources["ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"] == 70
