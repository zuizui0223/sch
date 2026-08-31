from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V16_BATCH3_REMAINDER_TITLE_ABSTRACT.csv"


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise AssertionError(f"unversioned screening decision file: {path.name}")
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    versions = [_version(path) for path in files]
    assert versions == list(range(1, max(versions) + 1))
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
    v12 = _read(files[-5])
    v12_ids = {row["record_id"] for row in v12}
    before_v12_ids = {row["record_id"] for row in _merge(files[:-5])}
    batch2 = {f"SCHPRISMA-{i:06d}" for i in range(101, 201)}
    assert len(v12) == 70
    assert "SCHPRISMA-000172" in before_v12_ids
    assert "SCHPRISMA-000172" not in v12_ids
    assert v12_ids == batch2 - before_v12_ids


def test_v13_closes_all_currently_retained_batch2_fulltexts() -> None:
    files = _decision_files()
    v13 = _read(files[-4])
    assert len(v13) == 35
    assert Counter(row["screen_fulltext"] for row in v13) == {"EXCLUDE": 26, "INCLUDE": 9}
    unavailable = [row for row in _rows() if row["fulltext_status"] == "UNAVAILABLE"]
    assert [row["record_id"] for row in unavailable] == ["SCHPRISMA-000194"]
    assert unavailable[0]["screen_fulltext_reason"] == "FT_FULLTEXT_UNAVAILABLE"


def test_v14_adjudicates_batch3_high_information_without_rescreening_prior_219() -> None:
    files = _decision_files()
    v14 = _read(files[-3])
    ids = {row["record_id"] for row in v14}
    assert len(v14) == 33
    assert "SCHPRISMA-000219" not in ids
    assert Counter(row["screen_title_abstract"] for row in v14) == {"RETAIN_FULLTEXT": 28, "EXCLUDE": 5}
    rows = _merge(files[:-2])
    assert len(rows) == 241
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 158
    assert ta["EXCLUDE"] == 83
    assert DENOMINATOR - len(rows) == 627


def test_v15_closes_batch3_high_information_fulltexts_without_strict_inflation() -> None:
    files = _decision_files()
    v15 = _read(files[-2])
    assert len(v15) == 28
    assert Counter(row["screen_fulltext"] for row in v15) == {"INCLUDE": 20, "EXCLUDE": 8}
    rows = _merge(files[:-1])
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 73
    assert ft["EXCLUDE"] == 85
    assert ft["UNSCREENED"] == 0


def test_v16_closes_batch3_title_abstract_screening_and_opens_44_fulltexts() -> None:
    files = _decision_files()
    v16 = _read(files[-1])
    assert len(v16) == 66
    assert Counter(row["screen_title_abstract"] for row in v16) == {
        "RETAIN_FULLTEXT": 44,
        "EXCLUDE": 22,
    }
    rows = _rows()
    assert len(rows) == 307
    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert ta["RETAIN_FULLTEXT"] == 202
    assert ta["EXCLUDE"] == 105
    assert DENOMINATOR - len(rows) == 561
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 73
    assert ft["EXCLUDE"] == 85
    assert ft["UNSCREENED"] == 44


def test_v16_preserves_v15_evidence_ceiling_until_fulltexts_are_adjudicated() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(rows) == 73
    lanes: Counter[str] = Counter()
    for row in rows:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 64
    assert lanes["EVOLUTIONARY_OUTCOME"] == 22
    assert lanes["HISTORICAL_TRANSITION"] == 1
    strict = [
        row["record_id"]
        for row in rows
        if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]
    ]
    assert strict == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_v15_role_transition_is_historical_evidence_but_not_shared_to_private_l4() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    role = rows["SCHPRISMA-000282"]
    assert role["evidence_lanes"] == "EVOLUTIONARY_OUTCOME;HISTORICAL_TRANSITION"
    assert role["selection_form"] == "ROLE_TRANSITION_FROM_FLORIVORY_TO_POLLINATION"
    assert role["historical_or_phylogenetic_context"] == "ROLE_TRANSITION_AND_TRAIT_DIVERGENCE_NOT_SHARED_TO_PRIVATE_CUE"
    assert "not a reconstructed shared-cue to private-cue transition" in role["claim_ceiling"]


def test_v16_geography_counts_do_not_become_independence_counts() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]
    assert len(geo) == 13
    assert len(receiver) == 12
    assert len(joint) == 11
    assert "SCHPRISMA-000217" in joint
    assert "SCHPRISMA-000277" in geo
    assert "SCHPRISMA-000277" not in receiver
    assert "SCHPRISMA-000167" in joint and "SCHPRISMA-000523" in joint


def test_v13_same_code_and_other_near_passes_do_not_inflate_strict_count() -> None:
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


def test_v12_to_v16_provenance_remains_stage_specific_in_raw_overlays() -> None:
    files = _decision_files()
    expected = [
        (-5, 70, "ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"),
        (-4, 35, "SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"),
        (-3, 33, "SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"),
        (-2, 28, "SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"),
        (-1, 66, "ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"),
    ]
    for index, count, source in expected:
        rows = _read(files[index])
        assert len(rows) == count
        assert {row["decision_source"] for row in rows} == {source}
    merged_sources = Counter(row["decision_source"] for row in _rows())
    assert merged_sources["SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"] == 5
    assert merged_sources["SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"] == 28
    assert merged_sources["ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"] == 66
