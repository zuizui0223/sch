import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_SEARCH_BATCH2_V1.csv"
def test_batch2_targets_three_source_audits_without_promotion():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    assert [r["record_id"] for r in rows]==["SCHPRISMA-000806","SCHPRISMA-000812","SCHPRISMA-000434"]
    assert {r["decision"] for r in rows}=={"RETAIN_FULLTEXT"}
    assert {r["status"] for r in rows}=={"PROSPECTIVE_SOURCE_ADJUDICATION_REQUIRED"}
