from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V17_BATCH3_REMAINDER_FULLTEXT.csv"


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise AssertionError(f"unversioned screening decision file: {path.name}")
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    versions = [_version(path) for path in files]
    assert versions == list(range(1, 18))
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


def _v(version: int) -> list[dict[str, str]]:
    path = next(path for path in _decision_files() if _version(path) == version)
    return _read(path)


def _positive_geo(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    upper = value.upper()
    return bool(value) and value != "NOT_REPORTED" and not upper.startswith("NO_")


def test_stage_overlays_v12_to_v17_remain_distinct_and_complete() -> None:
    expected = {
        12: (70, "ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"),
        13: (35, "SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"),
        14: (33, "SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"),
        15: (28, "SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"),
        16: (66, "ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"),
        17: (44, "SOURCE_VERIFIED_BATCH3_REMAINDER_FULLTEXT_V17_2026-08-31"),
    }
    for version, (count, source) in expected.items():
        rows = _v(version)
        assert len(rows) == count
        assert {row["decision_source"] for row in rows} == {source}


def test_batch2_and_batch3_title_abstract_are_closed_without_double_screening() -> None:
    files = _decision_files()
    before_v12 = {row["record_id"] for row in _merge(files[:11])}
    v12_ids = {row["record_id"] for row in _v(12)}
    batch2 = {f"SCHPRISMA-{i:06d}" for i in range(101, 201)}
    assert len(v12_ids) == 70
    assert "SCHPRISMA-000172" in before_v12 and "SCHPRISMA-000172" not in v12_ids
    assert v12_ids == batch2 - before_v12

    v14 = _v(14)
    v16 = _v(16)
    assert len(v14) == 33
    assert Counter(row["screen_title_abstract"] for row in v14) == {"RETAIN_FULLTEXT": 28, "EXCLUDE": 5}
    assert len(v16) == 66
    assert Counter(row["screen_title_abstract"] for row in v16) == {"RETAIN_FULLTEXT": 44, "EXCLUDE": 22}
    assert "SCHPRISMA-000219" not in {row["record_id"] for row in v14 + v16}

    rows = _rows()
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert len(rows) == 307
    assert ta["RETAIN_FULLTEXT"] == 202
    assert ta["EXCLUDE"] == 105
    assert DENOMINATOR - len(rows) == 561
    assert all(
        next(row for row in rows if row["record_id"] == f"SCHPRISMA-{i:06d}")["screen_title_abstract"] in {"RETAIN_FULLTEXT", "EXCLUDE"}
        for i in range(201, 301)
    )


def test_v13_v15_and_v17_close_their_retained_fulltext_queues() -> None:
    assert Counter(row["screen_fulltext"] for row in _v(13)) == {"EXCLUDE": 26, "INCLUDE": 9}
    assert Counter(row["screen_fulltext"] for row in _v(15)) == {"INCLUDE": 20, "EXCLUDE": 8}
    assert Counter(row["screen_fulltext"] for row in _v(17)) == {"INCLUDE": 16, "EXCLUDE": 28}

    rows = _rows()
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 89
    assert ft["EXCLUDE"] == 113
    assert ft["UNSCREENED"] == 0
    unavailable = [row for row in rows if row["fulltext_status"] == "UNAVAILABLE"]
    assert [row["record_id"] for row in unavailable] == ["SCHPRISMA-000194"]
    assert unavailable[0]["screen_fulltext_reason"] == "FT_FULLTEXT_UNAVAILABLE"


def test_current_evidence_lanes_keep_strict_at_two_while_lower_layers_expand() -> None:
    included = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(included) == 89
    lanes: Counter[str] = Counter()
    for row in included:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 77
    assert lanes["EVOLUTIONARY_OUTCOME"] == 29
    assert lanes["HISTORICAL_TRANSITION"] == 4
    strict = [row["record_id"] for row in included if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert strict == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_historical_transitions_remain_below_shared_to_private_l4() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    role = rows["SCHPRISMA-000282"]
    assert role["evidence_lanes"] == "EVOLUTIONARY_OUTCOME;HISTORICAL_TRANSITION"
    assert role["selection_form"] == "ROLE_TRANSITION_FROM_FLORIVORY_TO_POLLINATION"
    assert "NOT_SHARED_TO_PRIVATE_CUE" in role["historical_or_phylogenetic_context"]

    abronia = rows["SCHPRISMA-000230"]
    assert "HISTORICAL_TRANSITION" in abronia["evidence_lanes"]
    assert "NOT_SHARED_TO_PRIVATE_CUE" in abronia["historical_or_phylogenetic_context"]

    historical = [row for row in rows.values() if "HISTORICAL_TRANSITION" in row["evidence_lanes"]]
    assert len(historical) == 4
    assert all("DIRECT_L4" not in row["evidence_lanes"] for row in historical)


def test_geography_counts_are_record_level_and_not_independence_counts() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]
    assert len(geo) == 20
    assert len(receiver) == 19
    assert len(joint) == 17
    assert "SCHPRISMA-000217" in joint
    assert "SCHPRISMA-000233" in joint
    assert "SCHPRISMA-000167" in joint and "SCHPRISMA-000523" in joint


def test_same_code_near_passes_still_do_not_inflate_strict_count() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    junker = rows["SCHPRISMA-000197"]
    assert junker["A_manipulated"] == "YES_SYNTHETIC_SCENT_BIOASSAY"
    assert junker["pollinator_response_measured"] == "YES_BUMBLEBEE_ATTRACTION"
    assert junker["antagonist_response_measured"] == "YES_ANT_REPELLENCE_AS_FACULTATIVE_FLOWER_VISITOR"
    assert junker["common_reproductive_outcome"] == "NO_COMMON_PLANT_REPRODUCTIVE_OUTCOME"

    datura = rows["SCHPRISMA-000046"]
    assert datura["A_manipulated"] == "YES_SYNTHETIC_SCENT_AND_ENANTIOMER_MANIPULATION"
    assert datura["pollinator_response_measured"] == "YES_MANDUCA_FEEDING_RESPONSE"
    assert datura["antagonist_response_measured"] == "YES_MANDUCA_OVIPOSITION_RESPONSE"
    assert datura["common_reproductive_outcome"] == "NO_PLANT_REPRODUCTIVE_OUTCOME"


def test_latest_overlay_provenance_is_not_mistaken_for_cumulative_history() -> None:
    merged_sources = Counter(row["decision_source"] for row in _rows())
    assert merged_sources["SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"] == 5
    assert merged_sources["SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"] == 28
    assert merged_sources["ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"] == 22
    assert merged_sources["SOURCE_VERIFIED_BATCH3_REMAINDER_FULLTEXT_V17_2026-08-31"] == 44
