from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V13_BATCH2_FULLTEXT_CLOSURE.csv"


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise AssertionError(f"unversioned screening decision file: {path.name}")
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    assert [_version(path) for path in files] == list(range(1, 14))
    assert files[-1].name == LATEST
    return files


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _merge(files: list[Path]) -> list[dict[str, str]]:
    loaded = [_read(path) for path in files]
    all_fields = {key for rows in loaded for update in rows for key in update}
    merged: dict[str, dict[str, str]] = {}
    for updates in loaded:
        for update in updates:
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


def test_batch2_title_abstract_remains_closed_without_double_screening_prior_anchor() -> None:
    files = _decision_files()
    v12 = _read(files[-2])
    v12_ids = {row["record_id"] for row in v12}
    before_v12_ids = {row["record_id"] for row in _merge(files[:-2])}
    batch2 = {f"SCHPRISMA-{i:06d}" for i in range(101, 201)}

    assert len(v12) == 70
    assert "SCHPRISMA-000172" in before_v12_ids
    assert "SCHPRISMA-000172" not in v12_ids
    assert v12_ids == batch2 - before_v12_ids

    rows = _rows()
    decided_ids = {row["record_id"] for row in rows}
    assert {f"SCHPRISMA-{i:06d}" for i in range(1, 201)} <= decided_ids
    assert len(rows) == 208

    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 130
    assert ta["EXCLUDE"] == 78
    assert DENOMINATOR - len(rows) == 660


def test_v13_closes_all_currently_retained_batch2_fulltexts() -> None:
    files = _decision_files()
    v13 = _read(files[-1])
    assert len(v13) == 35
    assert Counter(row["screen_fulltext"] for row in v13) == {"EXCLUDE": 26, "INCLUDE": 9}

    rows = _rows()
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 53
    assert ft["EXCLUDE"] == 77
    assert ft["UNSCREENED"] == 0

    unavailable = [row for row in rows if row["fulltext_status"] == "UNAVAILABLE"]
    assert [row["record_id"] for row in unavailable] == ["SCHPRISMA-000194"]
    assert unavailable[0]["screen_fulltext_reason"] == "FT_FULLTEXT_UNAVAILABLE"


def test_current_evidence_lanes_keep_two_strict_measurement_architectures() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 46
    assert lanes["EVOLUTIONARY_OUTCOME"] == 15
    strict = [row for row in rows if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert [row["record_id"] for row in strict] == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_v13_adds_same_code_opposite_receiver_near_pass_without_strict_inflation() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    junker = rows["SCHPRISMA-000197"]
    assert junker["A_manipulated"] == "YES_SYNTHETIC_SCENT_BIOASSAY"
    assert junker["pollinator_response_measured"] == "YES_BUMBLEBEE_ATTRACTION"
    assert junker["antagonist_response_measured"] == "YES_ANT_REPELLENCE_AS_FACULTATIVE_FLOWER_VISITOR"
    assert junker["common_reproductive_outcome"] == "NO_COMMON_PLANT_REPRODUCTIVE_OUTCOME"
    assert junker["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"

    stickiness = rows["SCHPRISMA-000195"]
    assert stickiness["A_manipulated"] == "YES_METHANOL_REMOVAL_OF_STICKINESS"
    assert stickiness["antagonist_response_measured"] == "YES_FLORIVORY_RESPONSE_TO_STICKINESS"
    assert stickiness["common_reproductive_outcome"] == "YES_FRUIT_SET"
    assert "NOT_DIRECT_RESPONSE_TO_DO_A" in stickiness["pollinator_response_measured"]
    assert stickiness["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_jbi_geography_and_receiver_counts_preserve_independence_boundary() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 53
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]

    assert len(geo) == 11
    assert len(receiver) == 11
    assert len(joint) == 10
    assert "SCHPRISMA-000151" in joint
    assert "SCHPRISMA-000167" in joint
    assert "SCHPRISMA-000195" in geo
    assert "SCHPRISMA-000195" not in receiver

    # 167 and 523 belong to the same Primula farinosa research programme.
    # Record counts therefore must not be reported as independent-system counts.
    assert "SCHPRISMA-000167" in joint and "SCHPRISMA-000523" in joint


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


def test_v12_and_v13_provenance_remain_stage_specific_in_raw_overlays() -> None:
    files = _decision_files()
    v12 = _read(files[-2])
    v13 = _read(files[-1])

    assert len(v12) == 70
    assert {row["decision_source"] for row in v12} == {
        "ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"
    }
    assert len(v13) == 35
    assert {row["decision_source"] for row in v13} == {
        "SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"
    }

    # decision_source is overlay-level provenance, not a cumulative-history field.
    # In the merged latest-state view, V13 legitimately replaces the latest source
    # for the 35 records that received a full-text adjudication while the 35 V12
    # title/abstract exclusions retain their V12 source.
    merged_sources = Counter(row["decision_source"] for row in _rows())
    assert merged_sources["ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"] == 35
    assert merged_sources["SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"] == 35
