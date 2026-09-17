from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "SCH_NPH_VIEWPOINT_V1.md"

CLASSES = (
    "EMPIRICAL",
    "LITERATURE-AUDIT",
    "THEORETICAL-WITNESS",
    "MODEL-PREDICTION",
    "NOT-ESTIMATED",
)


def test_quantitative_claim_ledger_declares_all_claim_classes() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for claim_class in CLASSES:
        assert f"`{claim_class}`" in text


def test_ledger_preserves_sch_evidence_counts() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    tokens = (
        "16 clusters",
        "Five clusters",
        "Seven additional clusters",
        "Two clusters are aligned/no-conflict controls",
        "strict numerical inventory contains four strong same-coordinate designs",
    )
    for token in tokens:
        assert token.lower() in manuscript.lower()
        assert token.lower() in ledger.lower()


def test_ledger_keeps_pooling_fail_closed() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    assert "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED" in text
    assert "NATURAL_PREVALENCE = NOT_ESTIMATED" in text
    assert "fewer than three independent clusters" in text
