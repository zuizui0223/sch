import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_SOURCE_OBJECT_RECOVERY_QUEUE_V1.csv"
def test_recovery_queue_is_ranked_by_object_value_not_candidate_volume():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    assert [int(r["priority"]) for r in rows]==[1,2,3]
    assert [r["source_id"] for r in rows]==["SCHPRISMA-000812","SCHPRISMA-000525","SCHPRISMA-000648"]
    assert all("MATERIALIZED" in r["current_status"] or "INCOMPLETE" in r["current_status"] for r in rows)
