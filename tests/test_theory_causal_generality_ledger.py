import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "THEORY_CAUSAL_GENERALITY_LEDGER_V1.csv"


def _rows():
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_stage_order_and_layers_are_explicit():
    rows = _rows()
    assert [row["stage"] for row in rows] == [
        "T1", "T2", "T3", "C0", "C1", "C2", "C3", "G0", "G1", "G2"
    ]
    assert {row["layer"] for row in rows[:3]} == {"theory"}
    assert {row["layer"] for row in rows[3:7]} == {"causal"}
    assert {row["layer"] for row in rows[7:]} == {"generality"}


def test_software_readiness_does_not_promote_pedicularis_biology():
    by_stage = {row["stage"]: row for row in _rows()}
    assert "NOT_YET_EXECUTED" in by_stage["C2"]["status"]
    assert "NOT_YET_EXECUTED" in by_stage["C3"]["status"]
    assert "NOT_YET_EXECUTED" in by_stage["G0"]["status"]


def test_payoff_game_is_not_a_sch_promotion_gate():
    text = (ROOT / "docs" / "THEORY_CAUSAL_GENERALITY_RECOVERY_V1.md").read_text(encoding="utf-8")
    assert "PAYOFF population frequency" in text
    assert "outside this spine" in text
