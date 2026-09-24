import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_ADJUDICATION_BATCH1_V1.csv"
def test_batch1_adjudication_promotes_nothing_without_numeric_contract():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    assert len(rows)==3
    assert all(not r["status"].startswith("QUALIFIED") for r in rows)
    assert rows[0]["record_id"]=="SCHPRISMA-000525"
    assert rows[0]["status"]=="BLOCKED_PRIMARY_NUMERIC_SOURCE_NOT_MATERIALIZED"
    assert rows[1]["status"].startswith("DOWNGRADED")
    assert rows[2]["status"]=="BLOCKED_SOURCE_LEVEL_ESTIMAND_NOT_YET_MATERIALIZED"
