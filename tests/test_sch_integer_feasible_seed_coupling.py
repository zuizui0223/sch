from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from itertools import permutations

import pytest

from scripts.bound_sch_integer_feasible_seed_stage_selection import (
    build, compare_settings_integer, integer_stage_bounds,
    integer_stage_bounds_variable_ovules, compare_settings_variable_ovules,
)


def _demo() -> dict:
    return {
        "schema": "SCH_INTEGER_SEED_STAGE_MARGINS_V1",
        "data_kind": "SYNTHETIC_DEMONSTRATION",
        "ovules_per_fruit": 12,
        "setting_margins": {
            "LOW": {
                "initiated_seed_counts": [1, 2],
                "predation_fractions": ["1/2", "1"],
            },
            "HIGH": {
                "initiated_seed_counts": [1, 4],
                "predation_fractions": ["1/2", "1"],
            },
        },
    }


def test_integer_biology_identifies_positive_sign_that_continuous_margins_cannot():
    r = build(_demo())
    assert r["source_data_kind"] == "SYNTHETIC_DEMONSTRATION"
    assert r["observed_field_data_independently_verified"] is False
    assert r["field_selection_effect_identified"] is False
    assert r["low"]["sharp_integer_feasible_mean_viable_fraction"] == pytest.approx(
        [1/24, 1/24]
    )
    assert r["high"]["sharp_integer_feasible_mean_viable_fraction"] == pytest.approx(
        [2/24, 2/24]
    )
    assert r["fractionally_relaxed_high_minus_low_interval"] == pytest.approx(
        [-1/48, 1/16]
    )
    assert r["integer_feasible_high_minus_low_interval"] == pytest.approx(
        [1/24, 1/24]
    )
    assert r["integer_constraint_changes_sign_identifiability"] is True
    assert r["SCH_primary_fitness_endpoint"] == "UNDAMAGED_MATURE_SEED_COUNT_PER_FLOWER"
    assert r["fractionally_relaxed_high_minus_low_seed_count_per_flower_interval"] == pytest.approx(
        [-.25,.75]
    )
    assert r["integer_constraint_changes_SCH_primary_seed_count_sign_identifiability"] is True
    assert r["integer_feasible_high_minus_low_seed_count_per_flower_interval"] == pytest.approx(
        [.5,.5]
    )
    assert r["integer_constraint_changes_SCH_primary_seed_count_sign_identifiability"] is True
    assert r["SCH_primary_seed_count_selection_direction"] == (
        "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    )
    assert r["high_minus_low_direction_given_margins"] == (
        "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    )
    assert {w["initiated_count"] for w in r["low"]["minimum_fitness_attaining_matching"]} == {1,2}
    assert {w["initiated_count"] for w in r["high"]["maximum_fitness_attaining_matching"]} == {1,4}
    assert all(
        w["damaged_count"] + w["viable_count"] == w["initiated_count"]
        for state in ("low","high")
        for w in r[state]["minimum_fitness_attaining_matching"]
    )


def test_existing_40_ovule_two_world_witness_survives_integer_constraints():
    r = compare_settings_integer(
        [2,30],["0","1/2"],
        [8,40],["0","1/2"],
        40
    )
    assert r["integer_feasible_high_minus_low_interval"] == pytest.approx(
        [-.0375,.3375]
    )
    assert r["fractionally_relaxed_high_minus_low_interval"] == pytest.approx(
        [-.0375,.3375]
    )
    assert r["high_minus_low_direction_given_margins"] == (
        "SIGN_NOT_IDENTIFIED_ACROSS_INTEGER_FEASIBLE_COUPLINGS"
    )
    assert r["integer_constraint_changes_sign_identifiability"] is False


def test_exhaustively_enumerated_permutations_match_integer_dp_extrema():
    n_ovules = 12
    counts = [3,4,6,12]
    fractions = ["0", "1/2", "1/3", "1"]
    viable = []
    for ordering in permutations(fractions):
        sub = []
        for count, text in zip(counts, ordering, strict=True):
            damaged = count * Fraction(text)
            if damaged.denominator != 1:
                break
            sub.append(count-int(damaged))
        else:
            viable.append(sum(sub))
    assert viable
    result = integer_stage_bounds(counts, fractions, n_ovules)
    assert result["integer_viable_total_seeds_extrema"] == [
        min(viable),max(viable)
    ]
    for key, target in (
        ("minimum_fitness_attaining_matching",min(viable)),
        ("maximum_fitness_attaining_matching",max(viable)),
    ):
        witness = result[key]
        assert sum(row["viable_count"] for row in witness) == target
        assert all(
            row["initiated_count"] * Fraction(row["q_fraction"])
            == row["damaged_count"]
            for row in witness
        )


def test_no_integer_matching_fails_rather_than_inventing_damaged_counts():
    with pytest.raises(ValueError, match="NO_INTEGER_FEASIBLE_PERFECT_MATCHING"):
        integer_stage_bounds([1,3],["1/2","1/4"],12)


def test_fraction_strings_are_exact_never_round_to_one_third():
    valid = integer_stage_bounds([3],["1/3"],12)
    assert valid["integer_viable_total_seeds_extrema"] == [2,2]
    with pytest.raises(ValueError,match="NO_INTEGER_FEASIBLE_PERFECT_MATCHING"):
        integer_stage_bounds([3],["0.3333333333333333"],12)


@pytest.mark.parametrize(
    ("counts","fractions","n","error"),
    [
        ([0],["0"],12,"exact integer"),
        ([13],["0"],12,"exact integer"),
        ([1],["1.2"],12,"within"),
        ([1],["no"],12,"exact rational"),
        ([1],["1/0"],12,"exact rational"),
        ([1],[.5],12,"string or exact integer"),
        ([1,2],["0"],12,"equal-length"),
        ([],[],12,"equal-length"),
        ([True],["0"],12,"exact integer"),
        ([1],["0"],0,"exact integer"),
        ([1]*257,["0"]*257,12,"equal-length"),
    ],
)
def test_invalid_biological_fates_and_intractable_designs_are_rejected(
    counts, fractions, n, error
):
    with pytest.raises(ValueError,match=error):
        integer_stage_bounds(counts,fractions,n)


def test_observed_route_requires_fate_validation_and_site_provenance():
    payload = _demo()
    payload["data_kind"] = "OBSERVED_UNPAIRED_MARGINS"
    with pytest.raises(ValueError,match="fate adjudication"):
        build(payload)
    payload["complete_fruit_fate_adjudication"] = True
    with pytest.raises(ValueError,match="population/season provenance"):
        build(payload)
    payload["source_population"] = "EXAMPLE_ONLY"
    payload["source_season"] = "SYNTHETIC_SEASON"
    r = build(payload)
    assert r["user_claims_observed_margins"] is True
    assert r["observed_field_data_independently_verified"] is False
    assert r["field_selection_effect_identified"] is False
    # This test checks input validation only, not actual data provenance.


def test_schema_and_setting_loss_fail_closed():
    p=_demo()
    p["schema"]="OTHER"
    with pytest.raises(ValueError,match="expected integer"):
        build(p)
    p=_demo()
    del p["setting_margins"]["HIGH"]
    with pytest.raises(ValueError,match="both LOW/HIGH"):
        build(p)
    p=_demo()
    p["setting_margins"]["LOW"]["q"]="1/2"
    with pytest.raises(ValueError,match="count and ratio"):
        build(p)


def test_variable_ovule_counts_recover_positive_sign_and_preserve_per_fruit_weights():
    # Ovules vary across individual fruits. The ovule/initiation pair is
    # measured on one fruit; only the q origin is unlinked.
    low=[{"ovules":12,"initiated":1},{"ovules":8,"initiated":2}]
    high=[{"ovules":15,"initiated":1},{"ovules":10,"initiated":4}]
    r=compare_settings_variable_ovules(low,["1/2","1"],high,["1/2","1"])
    assert r["low"]["ovule_count_heterogeneous"] is True
    assert r["high"]["ovule_count_heterogeneous"] is True
    assert r["low"]["ovules_per_fruit"] is None
    assert r["high"]["ovules_per_fruit"] is None
    assert r["low"]["sharp_integer_feasible_mean_viable_fraction"] == pytest.approx(
        [1/16,1/16]
    )
    assert r["high"]["sharp_integer_feasible_mean_viable_fraction"] == pytest.approx(
        [1/10,1/10]
    )
    assert r["integer_feasible_high_minus_low_interval"] == pytest.approx(
        [3/80,3/80]
    )
    assert r["integer_feasible_high_minus_low_seed_count_per_flower_interval"] == pytest.approx(
        [.5,.5]
    )
    relaxed=r["fractionally_relaxed_high_minus_low_interval"]
    assert relaxed[0] < 0 < relaxed[1]
    assert r["integer_constraint_changes_sign_identifiability"] is True
    assert r["high_minus_low_direction_given_margins"] == (
        "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    )
    # The mean of fractions is the target, NOT the pooled viable seed
    # count divided by the pooled number of ovules.
    witnesses=r["high"]["maximum_fitness_attaining_matching"]
    assert sum(x["viable_count"]/x["ovule_count"] for x in witnesses)/2 == pytest.approx(
        .1
    )


def test_variable_ovule_cli_schema_and_ambiguous_ovule_pairs_are_rejected():
    p=_demo()
    p["ovule_count_mode"]="VARIABLE_OVULES_PER_FRUIT"
    p.pop("ovules_per_fruit")
    p["setting_margins"]={
        "LOW":{"ovule_and_initiated_counts":[
            {"ovules":12,"initiated":1},{"ovules":8,"initiated":2}],
            "predation_fractions":["1/2","1"]},
        "HIGH":{"ovule_and_initiated_counts":[
            {"ovules":15,"initiated":1},{"ovules":10,"initiated":4}],
            "predation_fractions":["1/2","1"]},
    }
    r=build(p)
    assert r["integer_constraint_changes_sign_identifiability"] is True
    assert r["observed_field_data_independently_verified"] is False
    broken=deepcopy(p)
    del broken["setting_margins"]["LOW"]["ovule_and_initiated_counts"][0]["ovules"]
    with pytest.raises(ValueError,match="must pair ovules"):
        build(broken)
    broken=deepcopy(p)
    broken["setting_margins"]["HIGH"]["ovule_and_initiated_counts"][0]["initiated"]=0
    with pytest.raises(ValueError,match="exact integer"):
        build(broken)
    broken=deepcopy(p)
    broken["ovule_count_mode"]="UNKNOWN"
    with pytest.raises(ValueError,match="unregistered ovule_count_mode"):
        build(broken)


def test_variable_fruit_count_exact_permutation_optimization():
    fruits=[{"ovules":6,"initiated":2},
            {"ovules":10,"initiated":5},
            {"ovules":12,"initiated":6}]
    fractions=["0","1/2","1"]
    values=[]
    for ordering in permutations(fractions):
        part=[]
        for f,q in zip(fruits,ordering,strict=True):
            damaged=f["initiated"]*Fraction(q)
            if damaged.denominator!=1:
                break
            part.append(Fraction(f["initiated"]-int(damaged),f["ovules"]))
        else:
            values.append(sum(part)/len(part))
    assert values
    fitted=integer_stage_bounds_variable_ovules(fruits,fractions)
    assert fitted["sharp_integer_feasible_mean_viable_fraction"] == pytest.approx(
        [float(min(values)),float(max(values))]
    )
    assert fitted["exact_fractional_mean_viability_extrema"] == [
        str(min(values)),str(max(values))
    ]


def test_variable_ovule_counts_can_reverse_primary_count_vs_fraction_fitness_sign():
    # Both are fully observed integer seed counts with q=0.
    # LOW: 50 surviving seeds out of 100 ovules.
    # HIGH: 8 surviving seeds out of 10 ovules.
    # Higher z improves the *fraction* surviving but reduces total
    # viable seed output per flower, which is SCH's registered fitness.
    r=compare_settings_variable_ovules(
        [{"ovules":100,"initiated":50}],["0"],
        [{"ovules":10,"initiated":8}],["0"]
    )
    assert r["integer_feasible_high_minus_low_interval"] == pytest.approx(
        [.3,.3]
    )
    assert r["integer_feasible_high_minus_low_seed_count_per_flower_interval"] == pytest.approx(
        [-42,-42]
    )
    assert r["per_flower_viable_fraction_selection_direction"] == (
        "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    )
    assert r["SCH_primary_seed_count_selection_direction"] == (
        "NEGATIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    )
    assert r["count_and_fraction_direction_agree"] is False


def test_variable_ovule_optimization_count_and_fraction_may_use_different_pairings():
    fruits=[
        {"ovules":8,"initiated":4},
        {"ovules":100,"initiated":20},
    ]
    ratios=["0","1/2"]
    fit=integer_stage_bounds_variable_ovules(fruits,ratios)
    min_fraction=fit["minimum_fitness_attaining_matching"]
    min_count=fit["minimum_seed_count_attaining_matching"]
    assert [(r["initiated_count"],r["q_fraction"]) for r in min_fraction] != [
        (r["initiated_count"],r["q_fraction"]) for r in min_count
    ]
    assert fit["sharp_integer_feasible_mean_viable_seeds_per_flower"][0] == pytest.approx(7)
    assert fit["sharp_integer_feasible_mean_viable_fraction"][0] == pytest.approx(.225)


def test_large_source_like_120_fruit_stage_margins_use_exact_assignment():
    # This is synthetic, not an actual P. rex published population sample.
    counts=[2*(i%12+1) for i in range(120)]
    fractions=["0"]*60+["1/2"]*60
    r=integer_stage_bounds(counts,fractions,40)
    assert r["n_equal_weight_fruits"]==120
    assert r["method"]=="EXACT_HUNGARIAN_PERFECT_MATCHING_INTEGER_SEED_FATES"
    assert r["n_exact_assignment_solutions"]==4
    sorted_counts=sorted(counts)
    total=sum(counts)
    min_total=total-sum(sorted_counts[-60:])//2
    max_total=total-sum(sorted_counts[:60])//2
    assert r["integer_viable_total_seeds_extrema"]==[min_total,max_total]
    assert r["sharp_integer_feasible_mean_viable_seeds_per_flower"]==pytest.approx(
        [min_total/120,max_total/120]
    )
    for key,expected in (
        ("minimum_seed_count_attaining_matching",min_total),
        ("maximum_seed_count_attaining_matching",max_total),
    ):
        matched=r[key]
        assert len(matched)==120
        assert sum(x["viable_count"] for x in matched)==expected
        assert all(
            Fraction(x["initiated_count"])*Fraction(x["q_fraction"])
            ==x["damaged_count"] and x["viable_count"]>=0
            for x in matched
        )


def test_120_fruit_variable_ovules_independent_exact_fitness_objectives():
    n=120
    fruits=[
        {"ovules":20+(i%13), "initiated":2*(1+i%8)}
        for i in range(n)
    ]
    ratios=["0"]*60+["1/2"]*60
    result=integer_stage_bounds_variable_ovules(fruits,ratios)
    assert result["ovule_count_heterogeneous"] is True
    assert result["n_equal_weight_fruits"]==120
    for key,interval in (
        ("seed_count","sharp_integer_feasible_mean_viable_seeds_per_flower"),
        ("fraction","sharp_integer_feasible_mean_viable_fraction"),
    ):
        low,high=result[interval]
        assert low<=high
        assert all(
            len(result[s])==n for s in (
                ("minimum_seed_count_attaining_matching",
                 "maximum_seed_count_attaining_matching")
                if key=="seed_count"
                else ("minimum_fitness_attaining_matching",
                      "maximum_fitness_attaining_matching")
            )
        )
    count_low=result["minimum_seed_count_attaining_matching"]
    count_high=result["maximum_seed_count_attaining_matching"]
    assert sum(x["viable_count"] for x in count_low)/n==pytest.approx(
        result["sharp_integer_feasible_mean_viable_seeds_per_flower"][0]
    )
    assert sum(x["viable_count"] for x in count_high)/n==pytest.approx(
        result["sharp_integer_feasible_mean_viable_seeds_per_flower"][1]
    )


def test_infeasible_large_sparse_graph_must_fail_closed():
    # There are 119 fruits with odd initiated counts, but 120 q=1/2;
    # no integer-damage perfect matching exists.
    with pytest.raises(ValueError,match="NO_INTEGER_FEASIBLE_PERFECT_MATCHING"):
        integer_stage_bounds([1]*119+[2],["1/2"]*120,40)
