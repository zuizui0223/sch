from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_SUFFIX = "." + "md"
TRIAGE = ROOT / "docs" / f"REVIEWER_QUANTITATIVE_REQUEST_TRIAGE_V1{DOC_SUFFIX}"
AUDIT = ROOT / "docs" / f"QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1{DOC_SUFFIX}"


def test_reviewer_quantitative_triage_declares_decision_contract() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    assert "| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |" in text
    for decision in ("DO_NOW", "DO_IF_REQUESTED", "DECLINE"):
        assert f"`{decision}`" in text


def test_sch_triage_prioritizes_compatibility_over_forced_pooling() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    for token in (
        "compatibility matrix",
        "classification sensitivity",
        "second-adjudicator",
        "pooled conflict effect",
        "convert 16/5/7/2 into prevalence",
    ):
        assert token in text


def test_sch_triage_preserves_fail_closed_ceiling() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    triage = TRIAGE.read_text(encoding="utf-8")
    for token in (
        "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED",
        "NATURAL_PREVALENCE = NOT_ESTIMATED",
        "META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED",
        "not a universal mean trade-off",
    ):
        assert token in audit
        assert token in triage
