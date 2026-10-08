from __future__ import annotations

from fractions import Fraction
from itertools import permutations

import pytest

from scripts.sch_exact_assignment import exact_assignment, MAX_ASSIGNMENT_SIZE


def _brute(costs: list[list]) -> tuple:
    values = []
    for assignment in permutations(range(len(costs))):
        if all(costs[i][j] is not None for i, j in enumerate(assignment)):
            values.append(sum((costs[i][j] for i, j in enumerate(assignment)), 0))
    return (min(values), max(values)) if values else (None, None)


@pytest.mark.parametrize(
    "costs",
    [
        [[1]],
        [[1, 2], [3, 0]],
        [[None, 1], [0, None]],
        [[2, None, -3], [-1, 0, 5], [4, 2, None]],
        [
            [Fraction(1, 3), Fraction(1, 2), None],
            [Fraction(1, 5), None, Fraction(2, 7)],
            [None, Fraction(3, 8), Fraction(1, 9)],
        ],
        [[0,0,0],[0,0,0],[0,0,0]],
        [[1,None,None],[0,5,None],[0,0,9]],
    ],
)
def test_exact_hungarian_matches_independent_permutation_extrema(costs):
    lo, hi = _brute(costs)
    assert lo is not None
    for maximize, expected in ((False,lo),(True,hi)):
        r=exact_assignment(costs,maximize=maximize)
        assert r["objective"] == expected
        assert sorted(r["assignment"]) == list(range(len(costs)))
        assert all(
            costs[i][j] is not None
            for i,j in enumerate(r["assignment"])
        )
        assert r["source_pairs_identified"] is False


def test_sparse_perfect_matching_requires_reassignment_not_row_greedy():
    # Naive row0->column0 leaves row1 with no valid column.
    costs=[[0, 1], [0, None]]
    r=exact_assignment(costs)
    assert r["assignment"] == (1,0)
    assert r["objective"] == 1
    assert exact_assignment(costs,maximize=True)["assignment"] == (1,0)


def test_impossible_matching_cannot_be_rescued_by_large_penalty():
    costs=[[0, None], [0, None]]
    for maximizing in (False, True):
        with pytest.raises(ValueError,match="NO_INTEGER_FEASIBLE_PERFECT_MATCHING"):
            exact_assignment(costs,maximize=maximizing)


@pytest.mark.parametrize("matrix",[
    [],
    [[1,2]],
    [[0], [1]],
    [[1.5]],
    [[True]],
    [[float("inf")]],
    [[None,None], [None,None]],
])
def test_bad_assignment_matrices_are_rejected(matrix):
    with pytest.raises(ValueError):
        exact_assignment(matrix)


def test_120_fruits_equal_costs_remain_exact_and_one_to_one():
    n=120
    q=[Fraction(0)]*60 + [Fraction(1,2)]*60
    counts=[2*(1+i%12) for i in range(n)]
    # Every count is even, so all q pairings are feasible.
    costs=[[count*(1-fraction) for fraction in q] for count in counts]
    lo=exact_assignment(costs)
    hi=exact_assignment(costs,maximize=True)
    s=sorted(counts)
    assert lo["objective"] == sum(counts)-sum(s[-60:])/2
    assert hi["objective"] == sum(counts)-sum(s[:60])/2
    assert sorted(lo["assignment"])==list(range(n))
    assert lo["solver"] == "HUNGARIAN_EXACT_PRIMAL_DUAL_CUBIC"


def test_assignment_limit_is_explicit_and_nonexponential():
    assert MAX_ASSIGNMENT_SIZE >= 120
    with pytest.raises(ValueError,match="1..256"):
        exact_assignment([[0]]*(MAX_ASSIGNMENT_SIZE+1))
