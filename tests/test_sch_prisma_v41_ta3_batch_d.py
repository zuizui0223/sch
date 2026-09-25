import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V41_TA3_BATCH_D.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v41_is_exactly_the_fourth_25_frozen_ta3_records():
    v41 = _rows(V41)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[75:100]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v41] == expected
    assert [int(row["review_order"]) for row in frozen[75:100]] == list(range(153, 178))


def test_v41_decision_counts_are_frozen():
    rows = _rows(V41)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 7,
        "EXCLUDE": 18,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_D_SCREEN_V41_2026-09-26"
    }


def test_v41_retains_high_information_boundary_systems():
    rows = {row["record_id"]: row for row in _rows(V41)}
    for rid in (
        "SCHPRISMA-000485",
        "SCHPRISMA-000486",
        "SCHPRISMA-000488",
        "SCHPRISMA-000490",
        "SCHPRISMA-000494",
        "SCHPRISMA-000500",
        "SCHPRISMA-000509",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v41_keeps_common_fitness_pollinator_herbivore_experiment():
    rows = {row["record_id"]: row for row in _rows(V41)}
    assert rows["SCHPRISMA-000494"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "two-factor" in rows["SCHPRISMA-000494"]["decision_note"].lower()
    assert "seed production" in rows["SCHPRISMA-000494"]["decision_note"].lower()


def test_v41_excludes_abiotic_or_nonplant_second_functions():
    rows = {row["record_id"]: row for row in _rows(V41)}
    assert rows["SCHPRISMA-000511"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000512"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000497"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
