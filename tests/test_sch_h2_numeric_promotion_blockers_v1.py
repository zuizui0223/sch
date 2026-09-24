import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"data"/"SCH_H2_NUMERIC_PROMOTION_BLOCKERS_V1.csv"

def _rows():
    with LEDGER.open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def test_numeric_promotion_blockers_are_fail_closed_and_distinct():
    rows={r["source_id"]:r for r in _rows()}
    assert {"SCHPRISMA-000208","SCHPRISMA-000312","SCHPRISMA-000376"} <= set(rows)
    assert rows["SCHPRISMA-000208"]["promotion_status"]=="BLOCKED_EXACT_NUMERIC_COEFFICIENTS_NOT_MATERIALIZED"
    assert rows["SCHPRISMA-000312"]["promotion_status"]=="BLOCKED_EXACT_NUMERIC_COEFFICIENTS_NOT_MATERIALIZED"
    assert rows["SCHPRISMA-000376"]["promotion_status"]=="BLOCKED_SUPPLEMENT_BINARY_NOT_MATERIALIZED"
    assert all(r["counts_as_total_selection_cluster"]=="NO" for r in rows.values())

def test_collaea_duplicate_programme_is_not_double_counted():
    rows={r["source_id"]:r for r in _rows()}
    assert rows["SCHPRISMA-000312"]["cluster_id"]=="Collaea_cipoensis_attractiveness_program"
    assert rows["SCHPRISMA-000312"]["dependent_source_ids"]=="SCHPRISMA-000353"
