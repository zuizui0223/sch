import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_ADJUDICATION_BATCH2_V1.csv"
def test_batch2_keeps_cluster_gate_closed():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    assert len(rows)==3
    assert {r["cluster_action"] for r in rows}=={"NO_PROMOTION"}
    assert all(r["qualification_status"].startswith(("BLOCKED","DEPENDENT")) for r in rows)
