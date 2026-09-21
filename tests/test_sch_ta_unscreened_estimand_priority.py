import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
SCRIPT = ROOT / "scripts" / "build_sch_ta_unscreened_estimand_priority.py"


def _mod():
    spec = importlib.util.spec_from_file_location("sch_ta_priority", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_priority_rule_recognizes_selection_performance_and_context_without_outcome_sign():
    mod = _mod()

    selection = mod.classify_title("Conflicting selection on floral traits across pollinator contexts")
    assert selection["priority_tier"] == "TA0_EXPLICIT_SELECTION_FITNESS"

    performance = mod.classify_title("Floral display and reproductive success under nectar robbing")
    assert performance["priority_tier"] == "TA1_FINAL_REPRODUCTIVE_PERFORMANCE"

    context = mod.classify_title("Geographic variation in floral scent and pollinator interactions")
    assert context["priority_tier"] == "TA2_REPEATED_CONTEXT"

    other = mod.classify_title("Chemistry of a tropical flower")
    assert other["priority_tier"] == "TA3_OTHER_UNSCREENED"


def test_priority_queue_covers_exact_current_unscreened_denominator_and_generates_no_decisions():
    rows, receipt = _mod().build(FROZEN, PRISMA)

    assert receipt["n_frozen_candidates"] == 868
    assert receipt["n_formally_ta_screened"] == 405
    assert receipt["n_unscreened_priority_queue"] == 463
    assert len(rows) == 463
    assert receipt["n_formal_decisions_generated"] == 0
    assert all(row["formal_title_abstract_decision"] == "" for row in rows)
    assert all(row["priority_status"] == "OUTCOME_BLIND_REVIEW_ORDER_ONLY" for row in rows)


def test_priority_queue_has_unique_records_and_deterministic_order():
    rows, _ = _mod().build(FROZEN, PRISMA)
    assert len({row["record_id"] for row in rows}) == 463
    assert [int(row["review_order"]) for row in rows] == list(range(1, 464))
    assert [mod_tier := _mod().TIER_RANK[row["priority_tier"]] for row in rows] == sorted(
        _mod().TIER_RANK[row["priority_tier"]] for row in rows
    )


def test_priority_rule_is_explicitly_review_order_only():
    _, receipt = _mod().build(FROZEN, PRISMA)
    assert "priority_changes_review_order_only" in receipt["claim_ceiling"]
    assert "same_axis_common_outcome_and_estimand_rules_are_unchanged" in receipt["claim_ceiling"]
