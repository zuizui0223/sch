from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
DENOMINATOR = 868
LATEST = "SCH_PRISMA_V2_SCREENING_DECISIONS_V19_BATCH4_HIGH_INFORMATION_FULLTEXT.csv"


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise AssertionError(f"unversioned screening decision file: {path.name}")
    return int(match.group(1))


def _decision_files() -> list[Path]:
    files = sorted(PRISMA.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)
    versions = [_version(path) for path in files]
    assert versions == list(range(1, 20))
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


def test_stage_overlays_v12_to_v19_remain_distinct_and_complete() -> None:
    expected = {
        12: (70, "ASSISTED_BATCH2_REMAINDER_TITLE_ABSTRACT_SCREEN_2026-08-31"),
        13: (35, "SOURCE_VERIFIED_BATCH2_FULLTEXT_V13_2026-08-31"),
        14: (33, "SOURCE_VERIFIED_BATCH3_HIGH_INFORMATION_TA_2026-08-31"),
        15: (28, "SOURCE_VERIFIED_BATCH3_FULLTEXT_V15_2026-08-31"),
        16: (66, "ASSISTED_BATCH3_REMAINDER_TA_SCREEN_2026-08-31"),
        17: (44, "SOURCE_VERIFIED_BATCH3_REMAINDER_FULLTEXT_V17_2026-08-31"),
        18: (57, "SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_TA_V18_2026-09-01"),
        19: (46, "SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_FULLTEXT_V19_2026-09-01"),
    }
    for version, (count, source) in expected.items():
        rows = _v(version)
        assert len(rows) == count
        assert {row["decision_source"] for row in rows} == {source}


def test_batch2_and_batch3_remain_closed() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    for i in range(101, 301):
        row = rows[f"SCHPRISMA-{i:06d}"]
        assert row["screen_title_abstract"] in {"RETAIN_FULLTEXT", "EXCLUDE"}
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT":
            assert row["screen_fulltext"] in {"INCLUDE", "EXCLUDE"}


def test_v18_and_v19_close_the_batch4_high_information_lane_without_rescreening_prior_records() -> None:
    v18 = _v(18)
    v19 = _v(19)
    v18_ids = {row["record_id"] for row in v18}
    v19_ids = {row["record_id"] for row in v19}
    assert len(v18) == 57
    assert Counter(row["screen_title_abstract"] for row in v18) == {"RETAIN_FULLTEXT": 46, "EXCLUDE": 11}
    assert {"SCHPRISMA-000329", "SCHPRISMA-000339"}.isdisjoint(v18_ids)
    assert len(v19) == 46
    assert Counter(row["screen_fulltext"] for row in v19) == {"INCLUDE": 30, "EXCLUDE": 16}
    assert v19_ids == {row["record_id"] for row in v18 if row["screen_title_abstract"] == "RETAIN_FULLTEXT"}


def test_v19_machine_audited_current_state() -> None:
    rows = _rows()
    ta = Counter(row["screen_title_abstract"] for row in rows)
    ft = Counter(
        row["screen_fulltext"] or "UNSCREENED"
        for row in rows
        if row["screen_title_abstract"] == "RETAIN_FULLTEXT"
    )
    assert len(rows) == 364
    assert ta["RETAIN_FULLTEXT"] == 248
    assert ta["EXCLUDE"] == 116
    assert DENOMINATOR - len(rows) == 504
    assert ft["INCLUDE"] == 119
    assert ft["EXCLUDE"] == 129
    assert ft["UNSCREENED"] == 0
    unavailable = [row for row in rows if row["fulltext_status"] == "UNAVAILABLE"]
    assert [row["record_id"] for row in unavailable] == ["SCHPRISMA-000194"]


def test_v19_expands_lower_layers_but_strict_remains_two() -> None:
    included = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    assert len(included) == 119
    lanes: Counter[str] = Counter()
    for row in included:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)
    assert lanes["STRICT_LINKED_EXPERIMENT"] == 2
    assert lanes["DIRECTIONAL_OR_NEAR_PASS"] == 102
    assert lanes["EVOLUTIONARY_OUTCOME"] == 42
    assert lanes["HISTORICAL_TRANSITION"] == 4
    strict = [row["record_id"] for row in included if "STRICT_LINKED_EXPERIMENT" in row["evidence_lanes"]]
    assert strict == ["SCHPRISMA-000031", "SCHPRISMA-000166"]


def test_v19_high_value_same_trait_cases_do_not_inflate_strict() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    collaea = rows["SCHPRISMA-000312"]
    assert collaea["A_manipulated"] == "NO_OBSERVATIONAL_TRAIT_VARIATION"
    assert collaea["pollinator_response_measured"] == "YES_POLLINATOR_VISIT_RATE"
    assert collaea["antagonist_response_measured"] == "YES_NECTAR_ROBBER_AND_FLORIVORE_VISIT_RATE"
    assert collaea["common_reproductive_outcome"] == "YES_MULTIPLICATIVE_FEMALE_FITNESS_COMPONENT"

    thistle = rows["SCHPRISMA-000365"]
    assert thistle["A_manipulated"] == "YES_SYNTHETIC_SCENT_BAIT"
    assert thistle["pollinator_response_measured"] == "YES_POLLINATOR_ATTRACTION_TO_COMPOUNDS"
    assert thistle["antagonist_response_measured"] == "YES_FLORAL_HERBIVORE_ATTRACTION_TO_COMPOUNDS"
    assert thistle["common_reproductive_outcome"] == "NO_COMMON_PLANT_REPRODUCTIVE_OUTCOME"

    ursinia = rows["SCHPRISMA-000323"]
    assert "EVOLUTIONARY_OUTCOME" in ursinia["evidence_lanes"]
    assert ursinia["A_manipulated"].startswith("NO_")


def test_v19_geography_counts_are_record_level_not_independence_counts() -> None:
    rows = [row for row in _rows() if row["screen_fulltext"] == "INCLUDE"]
    geo = [row["record_id"] for row in rows if _positive_geo(row["geographic_contrast"])]
    receiver = [row["record_id"] for row in rows if _positive_receiver(row["receiver_assemblage_contrast"])]
    joint = [record_id for record_id in geo if record_id in set(receiver)]
    assert len(geo) == 26
    assert len(receiver) == 25
    assert len(joint) == 23
    for record_id in ["SCHPRISMA-000323", "SCHPRISMA-000334", "SCHPRISMA-000376", "SCHPRISMA-000379", "SCHPRISMA-000380", "SCHPRISMA-000388"]:
        assert record_id in joint


def test_historical_transitions_still_remain_below_shared_to_private_l4() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    historical = [row for row in rows.values() if "HISTORICAL_TRANSITION" in row["evidence_lanes"]]
    assert len(historical) == 4
    assert all("DIRECT_L4" not in row["evidence_lanes"] for row in historical)
    assert "NOT_SHARED_TO_PRIVATE_CUE" in rows["SCHPRISMA-000282"]["historical_or_phylogenetic_context"]
    assert "NOT_SHARED_TO_PRIVATE_CUE" in rows["SCHPRISMA-000230"]["historical_or_phylogenetic_context"]


def test_v19_exclusions_preserve_primary_report_boundary() -> None:
    rows = {row["record_id"]: row for row in _rows()}
    assert rows["SCHPRISMA-000340"]["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE"
    assert rows["SCHPRISMA-000383"]["screen_fulltext_reason"] == "FT_NO_POLLINATOR_EVIDENCE"
    assert rows["SCHPRISMA-000394"]["screen_fulltext_reason"] == "FT_NO_POLLINATOR_EVIDENCE"


def test_latest_overlay_provenance_is_stage_specific() -> None:
    merged_sources = Counter(row["decision_source"] for row in _rows())
    assert merged_sources["SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_TA_V18_2026-09-01"] == 11
    assert merged_sources["SOURCE_VERIFIED_BATCH4_HIGH_INFORMATION_FULLTEXT_V19_2026-09-01"] == 46
