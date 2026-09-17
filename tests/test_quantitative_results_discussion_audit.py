from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1.md"
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"


def test_quantitative_results_discussion_audit_has_three_column_contract() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |" in text


def test_audit_preserves_sch_evidence_structure() -> None:
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for token in (
        "16 clusters",
        "Five clusters",
        "Seven additional clusters",
        "Two clusters are aligned/no-conflict controls",
        "four strong same-coordinate designs",
        "fewer than three independent clusters",
    ):
        assert token in ledger
        assert token in audit


def test_audit_keeps_cross_system_quantities_fail_closed() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED" in text
    assert "NATURAL_PREVALENCE = NOT_ESTIMATED" in text
    assert "META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED" in text
    assert "not a universal mean trade-off" in text
