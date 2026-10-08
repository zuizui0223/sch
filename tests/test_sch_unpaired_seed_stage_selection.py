from __future__ import annotations

import csv
from itertools import permutations
from pathlib import Path

import pytest

from scripts.bound_sch_unpaired_seed_stage_selection import (
    stage_bounds,
    compare_settings,
    build_from_csv,
)


LOW_I = [0.05, 0.75]       # e.g. 2 and 30 initiated / 40 ovules
HIGH_I = [0.20, 1.00]      # e.g. 8 and 40 initiated / 40 ovules
COMMON_Q = [0.0, 0.5]      # both trait ranks: identical full marginal distribution


def test_identical_predation_distributions_allow_opposite_fitness_directions() -> None:
    r = compare_settings(LOW_I, COMMON_Q, HIGH_I, COMMON_Q)
    assert r["low_z_setting"]["mean_initiation"] == pytest.approx(.4)
    assert r["high_z_setting"]["mean_initiation"] == pytest.approx(.6)
    assert r["low_z_setting"]["mean_predation"] == pytest.approx(.25)
    assert r["high_z_setting"]["mean_predation"] == pytest.approx(.25)
    assert r["low_z_setting"]["minimum_possible_mean_viable_seed_fraction"] == pytest.approx(.2125)
    assert r["low_z_setting"]["maximum_possible_mean_viable_seed_fraction"] == pytest.approx(.3875)
    assert r["high_z_setting"]["minimum_possible_mean_viable_seed_fraction"] == pytest.approx(.35)
    assert r["high_z_setting"]["maximum_possible_mean_viable_seed_fraction"] == pytest.approx(.55)
    assert r["sharp_high_minus_low_fitness_interval"] == pytest.approx([-.0375, .3375])
    assert r["selection_sign_given_only_stage_marginals"] == (
        "TRAIT_FITNESS_SIGN_NOT_IDENTIFIED_BY_MARGINALS"
    )
    assert r["sign_is_a_causal_selection_response_without_randomized_z"] is False


def test_two_complete_worlds_have_identical_stage_marginals_but_opposite_selection() -> None:
    # World A: high initiation is preferentially attacked at HIGH rank,
    # while attack targets the low-initiation fruit at LOW rank.
    low_a = [(0.05, 0.5), (0.75, 0.0)]
    high_a = [(0.20, 0.0), (1.0, 0.5)]
    # World B swaps the coupling without changing either unordered stage
    # marginal within either z rank.
    low_b = [(0.05, 0.0), (0.75, 0.5)]
    high_b = [(0.20, 0.5), (1.0, 0.0)]
    worlds = [(low_a, high_a, -.0375), (low_b, high_b, .3375)]
    for low, high, expected in worlds:
        for group, expected_i in ((low, LOW_I), (high, HIGH_I)):
            assert sorted(i for i, q in group) == sorted(expected_i)
            assert sorted(q for i, q in group) == sorted(COMMON_Q)
            # Every pairing can be a valid 40-ovule capsule with integer
            # distinguishably initiated and damaged seeds.
            for i, q in group:
                assert int(i * 40) == i * 40
                assert int(i * 40 * q) == i * 40 * q
        f_low = sum(i * (1-q) for i, q in low) / 2
        f_high = sum(i * (1-q) for i, q in high) / 2
        assert f_high - f_low == pytest.approx(expected)
    result = compare_settings(LOW_I, COMMON_Q, HIGH_I, COMMON_Q)
    assert result["sharp_high_minus_low_fitness_interval"] == pytest.approx(
        [worlds[0][2], worlds[1][2]]
    )


def test_rearrangement_bounds_are_attained_over_every_three_fruit_matching() -> None:
    initial = [0.2, 0.5, 0.8]
    predation = [0.1, 0.3, 0.9]
    all_fitness = [
        sum(i * (1 - q) for i, q in zip(initial, p, strict=True)) / 3
        for p in permutations(predation)
    ]
    result = stage_bounds(initial, predation)
    assert result["minimum_possible_mean_viable_seed_fraction"] == pytest.approx(
        min(all_fitness)
    )
    assert result["maximum_possible_mean_viable_seed_fraction"] == pytest.approx(
        max(all_fitness)
    )


def test_conservative_positive_sign_identified_without_matching() -> None:
    r = compare_settings([.15, .25], [.1,.3], [.7,.9], [.1,.3])
    low, high = r["sharp_high_minus_low_fitness_interval"]
    assert low > 0 and high > low
    assert r["selection_sign_given_only_stage_marginals"] == (
        "POSITIVE_HIGH_MINUS_LOW_SIGN_FIXED_ACROSS_ALL_COUPLINGS"
    )


def test_conservative_negative_sign_identified_without_matching() -> None:
    r = compare_settings([.7, .9], [.1,.3], [.15,.25], [.1,.3])
    low, high = r["sharp_high_minus_low_fitness_interval"]
    assert low < high and high < 0
    assert r["selection_sign_given_only_stage_marginals"] == (
        "NEGATIVE_HIGH_MINUS_LOW_SIGN_FIXED_ACROSS_ALL_COUPLINGS"
    )


@pytest.mark.parametrize(("initial","predator","msg"),[
    ([], [], "nonempty"),
    ([.5], [.1,.2], "equal-length"),
    ([0.0], [.5], "not defined"),
    ([float("nan")], [.5], "finite"),
    ([.5], [1.5], "finite"),
])
def test_marginal_bounds_reject_inconsistent_or_unqualified_fruit_fates(
    initial, predator, msg
) -> None:
    with pytest.raises(ValueError, match=msg):
        stage_bounds(initial, predator)


def test_cli_long_form_marginal_file_does_not_reconstruct_false_fruit_matches(
    tmp_path: Path,
) -> None:
    rows = []
    for setting, initial in (("LOW", LOW_I), ("HIGH", HIGH_I)):
        for channel, vals in (
            ("INITIATION_FRACTION", initial),
            ("PREDATION_FRACTION", COMMON_Q),
        ):
            for v in vals:
                rows.append({"setting":setting, "channel":channel, "value":v})
    file = tmp_path / "marginal.csv"
    with file.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=["setting", "channel", "value"])
        w.writeheader()
        w.writerows(rows)
    a = build_from_csv(file)
    assert a["sharp_high_minus_low_fitness_interval"] == pytest.approx(
        [-.0375,.3375]
    )
    assert "matching_not_reconstructed_by_arbitrary_pairing" in a["claim_ceiling"]
    with file.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=["setting", "channel", "value"])
        w.writeheader()
        w.writerows(rows[:-1])
    with pytest.raises(ValueError, match="equal-length"):
        build_from_csv(file)
