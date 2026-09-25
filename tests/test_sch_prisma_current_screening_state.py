from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V34_TA2_FULLTEXT_BATCH_A.csv"


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    assert match, path.name
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    assert [_version(path) for path in files] == list(range(1, 35))
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
            row = merged.setdefault(update["record_id"], {key: "" for key in all_fields})
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


def test_stage_overlays_v12_to_v20_remain_distinct_and_complete() -> None:
    expected = {
        12: (70, "ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"),
        13: (35, "SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"),
        14: (33, "SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"),
        15: (28, "SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"),
        16: (66, "ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"),
        17: (44, "SOURCE_VERIFIED_BATCH3_REMAINDER_FULLTEXT_V17_2026-08-31"),
        18: (57, "SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_TA_V18_2026-09-01"),
        19: (46, "SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_FULLTEXT_V19_2026-09-02"),
        20: (41, "ASSISTED_BATCH4_REMAINDER_TA_SCREEN_V20_2026-09-02"),
    }
    for version, (count, source) in expected.items():
        rows = _v(version)
        assert len(rows) == count
        assert {row["decision_source"] for row in rows} == {source}


def test_batch2_batch3_and_batch4_title_abstract_are_closed_without_double_screening() -> None:
    rows = _rows()
    indexed = {row["record_id"]: row for row in rows}
    for i in range(101, 401):
        assert indexed[f"SCHPRISMA-{i:06d}"]["screen_title_abstract"] in {"RETAIN_FULLTEXT", "EXCLUDE"}

    v18 = _v(18)
    v20 = _v(20)
    assert Counter(row["screen_title_abstract"] for row in v18) == {"RETAIN_FULLTEXT": 46, "EXCLUDE": 11}
    assert Counter(row["screen_title_abstract"] for row in v20) == {"RETAIN_FULLTEXT": 29, "EXCLUDE": 12}
    v18_ids = {row["record_id"] for row in v18}
    v20_ids = {row["record_id"] for row in v20}
    assert v18_ids.isdisjoint(v20_ids)
    assert {"SCHPRISMA-000329", "SCHPRISMA-000339"}.isdisjoint(v18_ids | v20_ids)
    assert len(v18_ids | v20_ids | {"SCHPRISMA-000329", "SCHPRISMA-000339"}) == 100

    ta = Counter(row["screen_title_abstract"] for row in rows)
    assert len(rows) == 483
    assert ta["RETAIN_FULLTEXT"] == 339
    assert ta["EXCLUDE"] == 144
    assert DENOMINATOR - len(rows) == 385


def test_v19_closes_v18_fulltexts_and_v20_opens_only_new_batch4_fulltexts() -> None:
    assert Counter(row["screen_fulltext"] for row in _v(19)) == {"INCLUDE": 28, "EXCLUDE": 18}
    v18_retained = {row["record_id"] for row in _v(18) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"}
    assert {row["record_id"] for row in _v(19)} == v18_retained

    rows = _rows()
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert ft["INCLUDE"] == 145
    assert ft["EXCLUDE"] == 135
    assert ft["UNSCREENED"] == 59
    pending = {row["record_id"] for row in rows if row["screen_title_abstract"] == "RETAIN_FULLTEXT" and not row["screen_fulltext"]}
    assert pending == ({row["record_id"] for row in _v(20) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"} | {row["record_id"] for row in _v(21) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"} | {row["record_id"] for row in _v(23) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"} | {row["record_id"] for row in _v(25) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"} | {row["record_id"] for row in _v(27) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"} | {row["record_id"] for row in _v(33) if row["screen_title_abstract"] == "RETAIN_FULLTEXT"}) - {row["record_id"] for row in _v(22)} - {row["record_id"] for row in _v(24)} - {row["record_id"] for row in _v(26)} - {row["record_id"] for row in _v(28)} - {row["record_id"] for row in _v(29)} - {row["record_id"] for row in _v(30)} - {row["record_id"] for row in _v(31)} - {row["record_id"] for row in _v(32)} - {row["record_id"] for row in _v(34)}
    unavailable = [row for row in rows if row["fulltext_status"] == "UNAVAILABLE"]
    assert [row["record_id"] for row in unavailable] == ["SCHPRISMA-000194"]


def test_v26_adds_four_directional_holdout_studies_without_inflating_strict_lane() -> None:
    included = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(included) == 145
    lanes: Counter[str] = Counter()
    for row in included:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 131
    assert lanes["EVOLUTIONARY_OUTCOME"] == 40
    assert lanes["HISTORICAL_TRANSITION"] == 4
    strict = [row["record_id"] for row in included if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert strict == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_v19_same_code_candidates_do_not_inflate_strict_count() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    thistle = rows["SCHPRISMA-000365"]
    assert thistle["A_manipulated"] == "YES_SYNTHETIC_SCENT_BAITS"
    assert thistle["pollinator_response_measured"] == "YES_MULTIPLE_POLLINATOR_SPECIES_ATTRACTED"
    assert thistle["antagonist_response_measured"] == "YES_MULTIPLE_FLORAL_HERBIVORE_SPECIES_ATTRACTED"
    assert thistle["common_reproductive_outcome"] == "NO_PLANT_REPRODUCTIVE_OUTCOME"
    guide = rows["SCHPRISMA-000319"]
    assert guide["A_manipulated"] == "YES_ARTIFICIAL_FLOWER_GUIDE_MANIPULATION"
    assert guide["common_reproductive_outcome"] == "NO_PLANT_REPRODUCTIVE_OUTCOME"


def test_historical_transitions_remain_below_shared_to_private_l4() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    historical = [row for row in rows.values() if "HISTORICAL_TRANSITION" in row["evidence_lanes"]]
    assert len(historical) == 4
    assert all("DIRECT_L4" not in row["evidence_lanes"] for row in historical)
    assert "NOT_SHARED_TO_PRIVATE_CUE" in rows["SCHPRISMA-000282"]["historical_or_phylogenetic_context"]


def test_geography_counts_are_record_level_and_not_independence_counts() -> None:
    included = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    geo = [row["record_id"] for row in included if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in included if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]
    assert len(geo) == 31
    assert len(receiver) == 27
    assert len(joint) == 25
    for record_id in ["SCHPRISMA-000323", "SCHPRISMA-000334", "SCHPRISMA-000376", "SCHPRISMA-000379", "SCHPRISMA-000380"]:
        assert record_id in joint


def test_stage_provenance_uses_raw_overlays_not_latest_state_as_history() -> None:
    assert len(_v(18)) == 57
    assert len(_v(19)) == 46
    assert len(_v(20)) == 41
    merged_sources = Counter(row["decision_source"] for row in _rows())
    assert merged_sources["SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_TA_V18_2026-09-01"] == 11
    assert merged_sources["SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_FULLTEXT_V19_2026-09-02"] == 46
    assert merged_sources["ASSISTED_BATCH4_REMAINDER_TA_SCREEN_V20_2026-09-02"] == 41


def test_v25_screens_only_still_unscreened_ta0_holdout_records() -> None:
    rows = _v(25)
    assert len(rows) == 28
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 20,
        "EXCLUDE": 8,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA0_HOLDOUT_SCREEN_V25_2026-09-25"
    }
    ids = {row["record_id"] for row in rows}
    assert {
        "SCHPRISMA-000648",
        "SCHPRISMA-000659",
        "SCHPRISMA-000775",
        "SCHPRISMA-000812",
    }.isdisjoint(ids)
    assert {
        "SCHPRISMA-000428",
        "SCHPRISMA-000503",
        "SCHPRISMA-000860",
    }.issubset(ids)


def test_v26_formally_includes_first_four_holdout_programmes_before_outcome_adjudication() -> None:
    rows = _v(26)
    assert len(rows) == 4
    assert {row["record_id"] for row in rows} == {
        "SCHPRISMA-000649",
        "SCHPRISMA-000651",
        "SCHPRISMA-000661",
        "SCHPRISMA-000723",
    }
    assert {row["fulltext_status"] for row in rows} == {"AVAILABLE"}
    assert {row["screen_fulltext"] for row in rows} == {"INCLUDE"}
    assert {row["evidence_lanes"] for row in rows} == {"DIRECTIONAL_OR_NEAR_PASS"}
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_H2_HOLDOUT_FULLTEXT_V26_2026-09-25"
    }


def test_v27_closes_the_frozen_ta1_performance_tier_in_review_order() -> None:
    rows = _v(27)
    assert len(rows) == 23
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 21,
        "EXCLUDE": 2,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA1_HOLDOUT_SCREEN_V27_2026-09-25"
    }
    excluded = {
        row["record_id"]: row["screen_title_abstract_reason"]
        for row in rows
        if row["screen_title_abstract"] == "EXCLUDE"
    }
    assert excluded == {
        "SCHPRISMA-000800": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000801": "TA_NO_POLLINATOR_COMPONENT",
    }


def test_v28_closes_first_four_ta1_fulltexts_without_strict_promotion() -> None:
    rows = _v(28)
    assert len(rows) == 4
    assert {row["record_id"] for row in rows} == {
        "SCHPRISMA-000420",
        "SCHPRISMA-000429",
        "SCHPRISMA-000449",
        "SCHPRISMA-000479",
    }
    assert {row["screen_fulltext"] for row in rows} == {"INCLUDE"}
    assert {row["evidence_lanes"] for row in rows} == {"DIRECTIONAL_OR_NEAR_PASS"}
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA1_FULLTEXT_BATCH_A_V28_2026-09-25"
    }


def test_v29_closes_next_four_ta1_fulltexts_with_one_antagonist_exclusion() -> None:
    rows = _v(29)
    assert len(rows) == 4
    assert {row["record_id"] for row in rows} == {
        "SCHPRISMA-000510",
        "SCHPRISMA-000538",
        "SCHPRISMA-000540",
        "SCHPRISMA-000542",
    }
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000510"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000510"]["screen_fulltext_reason"] == "FT_NO_ANTAGONIST_EVIDENCE"
    assert {by_id[x]["screen_fulltext"] for x in ("SCHPRISMA-000538","SCHPRISMA-000540","SCHPRISMA-000542")} == {"INCLUDE"}
    assert {by_id[x]["evidence_lanes"] for x in ("SCHPRISMA-000538","SCHPRISMA-000540","SCHPRISMA-000542")} == {"DIRECTIONAL_OR_NEAR_PASS"}


def test_v30_closes_next_four_ta1_fulltexts_as_near_pass_only() -> None:
    rows = _v(30)
    assert len(rows) == 4
    assert {row["record_id"] for row in rows} == {
        "SCHPRISMA-000543",
        "SCHPRISMA-000546",
        "SCHPRISMA-000548",
        "SCHPRISMA-000549",
    }
    assert {row["screen_fulltext"] for row in rows} == {"INCLUDE"}
    assert {row["evidence_lanes"] for row in rows} == {"DIRECTIONAL_OR_NEAR_PASS"}
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA1_FULLTEXT_BATCH_C_V30_2026-09-25"
    }


def test_v31_closes_next_four_ta1_fulltexts_with_duplicate_exclusion() -> None:
    rows = _v(31)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000564",
        "SCHPRISMA-000565",
        "SCHPRISMA-000599",
        "SCHPRISMA-000610",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000565"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000565"]["screen_fulltext_reason"] == "FT_DUPLICATE_DATASET_OR_REPORT"
    for rid in ("SCHPRISMA-000564","SCHPRISMA-000599","SCHPRISMA-000610"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v32_closes_next_four_ta1_fulltexts_with_meta_analysis_exclusion() -> None:
    rows = _v(32)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000663",
        "SCHPRISMA-000729",
        "SCHPRISMA-000736",
        "SCHPRISMA-000780",
        "SCHPRISMA-000839",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000780"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000780"]["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE"
    for rid in ("SCHPRISMA-000663","SCHPRISMA-000729","SCHPRISMA-000736","SCHPRISMA-000839"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v33_closes_the_frozen_ta2_repeated_context_tier() -> None:
    rows = _v(33)
    assert len(rows) == 20
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 14,
        "EXCLUDE": 6,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA2_HOLDOUT_SCREEN_V33_2026-09-25"
    }
    excluded = {
        row["record_id"]: row["screen_title_abstract_reason"]
        for row in rows
        if row["screen_title_abstract"] == "EXCLUDE"
    }
    assert excluded == {
        "SCHPRISMA-000455": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000461": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000524": "TA_NO_POLLINATOR_COMPONENT",
        "SCHPRISMA-000681": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000718": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000822": "TA_NO_ANTAGONIST_COMPONENT",
    }


def test_v34_closes_first_ta2_fulltext_batch_with_duplicate_control() -> None:
    rows = _v(34)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000569",
        "SCHPRISMA-000594",
        "SCHPRISMA-000621",
        "SCHPRISMA-000622",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000621"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000621"]["screen_fulltext_reason"] == "FT_DUPLICATE_DATASET_OR_REPORT"
    assert by_id["SCHPRISMA-000594"]["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    for rid in ("SCHPRISMA-000569", "SCHPRISMA-000622"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"
