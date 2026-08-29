from scripts.plan_ficus_same_code_assay import build_plan


def test_equivalence_requires_far_more_than_legacy_choice_counts() -> None:
    plan = build_plan()
    rows = {row["target_power"]: row for row in plan["equivalence_rows"]}
    assert rows[0.80]["decisive_choices"] == 206
    assert rows[0.90]["decisive_choices"] == 260
    assert rows[0.80]["planned_introductions"] == 412
    assert rows[0.90]["planned_introductions"] == 520


def test_strong_attraction_is_cheaper_than_equivalence_supported_nonresponse() -> None:
    plan = build_plan()
    rows = {
        (row["true_choice_probability"], row["target_power"]): row
        for row in plan["attraction_rows"]
    }
    assert rows[(0.65, 0.80)]["decisive_choices"] == 82
    assert rows[(0.65, 0.90)]["decisive_choices"] == 111
    assert rows[(0.70, 0.80)]["decisive_choices"] == 43
    assert rows[(0.70, 0.90)]["decisive_choices"] == 62
    assert rows[(0.65, 0.80)]["decisive_choices"] < 206


def test_planner_never_equates_nonsignificance_with_privacy() -> None:
    plan = build_plan()
    boundary = plan["claim_boundary"]
    assert "nonsignificant attraction test is not equivalence" in boundary
    assert "validated NPFW positive control" in boundary
