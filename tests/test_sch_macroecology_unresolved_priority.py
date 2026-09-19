import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "SCH_MACROECOLOGY_UNRESOLVED_AXIS_PRIORITY_V1.csv"


def _rows():
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_unresolved_priority_queue_matches_current_14_axis_frontier():
    rows = _rows()
    assert len(rows) == 14
    assert len({row["canonical_trait_axis_id"] for row in rows}) == 14
    assert Counter(row["h1_resolution_priority"] for row in rows) == {
        "HIGH": 4,
        "MEDIUM": 4,
        "LOW": 6,
    }


def test_h2_high_value_queue_is_not_equated_with_h1_resolution():
    rows = _rows()
    e = [row for row in rows if row["cluster_id"] == "Erysimum_mediohispanicum_selection_mosaic"]
    assert len(e) == 6
    assert all(row["h1_resolution_priority"] == "LOW" for row in e)
    assert all(row["h2_context_priority"] == "HIGH" for row in e)


def test_high_h1_priority_targets_agent_specific_source_tables():
    rows = _rows()
    high = [row for row in rows if row["h1_resolution_priority"] == "HIGH"]
    assert {row["cluster_id"] for row in high} == {
        "Gymnadenia_conopsea_agent_selection",
        "Primula_farinosa_scape_program",
    }
