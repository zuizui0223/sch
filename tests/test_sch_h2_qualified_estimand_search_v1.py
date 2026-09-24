import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_SEARCH_BATCH1_V1.csv"
def test_batch1_is_outcome_blind_and_does_not_promote_from_title():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    assert [r["record_id"] for r in rows]==["SCHPRISMA-000525","SCHPRISMA-000529","SCHPRISMA-000648"]
    assert {r["screening_decision"] for r in rows}=={"RETAIN_FULLTEXT"}
    assert {r["status"] for r in rows}=={"PROSPECTIVE_SOURCE_ADJUDICATION_REQUIRED"}
    assert all("PROMOT" not in r["status"] for r in rows)
