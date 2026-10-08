"""Exact polynomial-time square assignment with prohibited edges.

Primal-dual Hungarian shortest-augmenting-path algorithm, O(n^3) arithmetic
operations, with Python int/Fraction arithmetic so seed-count fitness
optimization has no rounding-driven integer-feasibility mistakes.

Rows are source fruits with linked ovule/initiation counts; columns are
unlinked exact predation fractions. Missing (None) edges are BIOLOGICALLY
IMPOSSIBLE and are never filled with an artificial large finite penalty.
The procedure returns a mathematically feasible *witness*, NOT recovered
historical fruit identities.
"""
from __future__ import annotations

from fractions import Fraction

MAX_ASSIGNMENT_SIZE = 256


def exact_assignment(
    costs: list[list[int | Fraction | None]],
    *,
    maximize: bool = False,
) -> dict:
    """Minimize/maximize a signed exact cost over perfect feasible matchings.

    Costs are int or Fraction (NOT floats). This is a dense O(n^3)
    primal-dual Hungarian solver that treats forbidden edges as None.
    """
    if not isinstance(costs, list) or not (1 <= len(costs) <= MAX_ASSIGNMENT_SIZE):
        raise ValueError("assignment requires 1..256 fruit observations")
    n = len(costs)
    for row in costs:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError("assignment requires a square fruit-by-predation matrix")
        if any(
            entry is not None and (
                type(entry) not in (int, Fraction)
            ) for entry in row
        ):
            raise ValueError("assignment costs must be exact int/Fraction or None")

    # Flip sign for maximization. No floating-point sentinel penalties.
    matrix = [
        [None if c is None else (-c if maximize else c) for c in row]
        for row in costs
    ]
    u: list[int | Fraction] = [0] * (n+1)
    v: list[int | Fraction] = [0] * (n+1)
    p: list[int] = [0] * (n+1)
    way: list[int] = [0] * (n+1)
    inner_iterations = 0

    for i in range(1, n+1):
        p[0] = i
        j0 = 0
        minv: list[int | Fraction | None] = [None] * (n+1)
        used = [False] * (n+1)
        while True:
            inner_iterations += 1
            used[j0] = True
            i0 = p[j0]
            delta: int | Fraction | None = None
            j1: int | None = None
            for j in range(1, n+1):
                if used[j]:
                    continue
                c = matrix[i0-1][j-1]
                if c is not None:
                    cur = c - u[i0] - v[j]
                    if minv[j] is None or cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                if minv[j] is not None and (
                    delta is None or minv[j] < delta
                ):
                    delta = minv[j]
                    j1 = j

            if j1 is None or delta is None:
                raise ValueError(
                    "NO_INTEGER_FEASIBLE_PERFECT_MATCHING: cannot assign all "
                    "predation fractions to source fruits as integer damage counts"
                )

            for j in range(0, n+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                elif minv[j] is not None:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break

        while True:
            previous_j = way[j0]
            p[j0] = p[previous_j]
            j0 = previous_j
            if j0 == 0:
                break

    assignment = [None] * n
    for j in range(1, n+1):
        if p[j] == 0:
            raise AssertionError("Hungarian assignment left an unmatched column")
        assignment[p[j]-1] = j-1
    if any(j is None or costs[i][j] is None for i,j in enumerate(assignment)):
        raise AssertionError("invalid forbidden-edge assignment")
    objective = sum((costs[i][j] for i,j in enumerate(assignment)), 0)
    return {
        "objective": objective,
        "assignment": tuple(assignment),
        "n_fruits": n,
        "inner_iterations": inner_iterations,
        "solver": "HUNGARIAN_EXACT_PRIMAL_DUAL_CUBIC",
        "source_pairs_identified": False,
    }
