from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class WeightNullspaceResult:
    relative_weights: tuple[float, ...]
    nullity: int
    residual_max_abs: float


@dataclass(frozen=True)
class NullspaceStabilityBound:
    stable_one_dimensional_nullspace: bool
    conservative_gap_lower: float
    sin_angle_upper: float | None


def _validate_square(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    rows = [list(map(float, row)) for row in matrix]
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("curvature matrix must be nonempty and square")
    return rows


def curvature_weight_residual(
    curvature: Sequence[Sequence[float]],
    weights: Sequence[float],
) -> tuple[float, ...]:
    matrix = _validate_square(curvature)
    w = tuple(map(float, weights))
    if len(w) != len(matrix):
        raise ValueError("weights must match curvature dimension")
    return tuple(sum(a * b for a, b in zip(row, w)) for row in matrix)


def _nullspace_basis(matrix: list[list[float]], tol: float) -> list[list[float]]:
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0])
    pivot_cols: list[int] = []
    r = 0

    for c in range(n):
        pivot = max(range(r, m), key=lambda i: abs(a[i][c]), default=r)
        if r >= m or abs(a[pivot][c]) <= tol:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(m):
            if i == r:
                continue
            f = a[i][c]
            if abs(f) <= tol:
                continue
            a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivot_cols.append(c)
        r += 1
        if r == m:
            break

    free_cols = [c for c in range(n) if c not in pivot_cols]
    basis: list[list[float]] = []
    for free in free_cols:
        v = [0.0] * n
        v[free] = 1.0
        for row_idx, pivot_col in enumerate(pivot_cols):
            v[pivot_col] = -a[row_idx][free]
        basis.append(v)
    return basis


def infer_relative_weights_from_curvature(
    curvature: Sequence[Sequence[float]],
    *,
    tol: float = 1e-9,
) -> WeightNullspaceResult:
    if tol <= 0:
        raise ValueError("tol must be positive")
    matrix = _validate_square(curvature)
    basis = _nullspace_basis(matrix, tol)
    if len(basis) != 1:
        raise ValueError("relative weights are identifiable only for a one-dimensional nullspace")

    v = basis[0]
    if sum(v) < 0:
        v = [-x for x in v]
    if any(x <= tol for x in v):
        raise ValueError("the unique null direction is not strictly positive")

    total = sum(v)
    w = tuple(x / total for x in v)
    residual = curvature_weight_residual(matrix, w)
    return WeightNullspaceResult(
        relative_weights=w,
        nullity=1,
        residual_max_abs=max(abs(x) for x in residual),
    )


def nullspace_angle_bound_from_true_gap(*, true_gap: float, operator_error: float) -> float:
    if true_gap <= 0.0:
        raise ValueError("true_gap must be positive")
    if operator_error < 0.0:
        raise ValueError("operator_error must be nonnegative")
    if operator_error >= true_gap / 2.0:
        raise ValueError("operator_error must be smaller than half the true gap")
    return operator_error / (true_gap - operator_error)


def nullspace_stability_from_estimated_gap(
    *,
    estimated_second_eigenvalue: float,
    operator_error: float,
) -> NullspaceStabilityBound:
    if estimated_second_eigenvalue < 0.0:
        raise ValueError("estimated_second_eigenvalue must be nonnegative")
    if operator_error < 0.0:
        raise ValueError("operator_error must be nonnegative")

    gap_lower = max(0.0, estimated_second_eigenvalue - operator_error)
    if estimated_second_eigenvalue <= 3.0 * operator_error:
        return NullspaceStabilityBound(
            stable_one_dimensional_nullspace=False,
            conservative_gap_lower=gap_lower,
            sin_angle_upper=None,
        )

    denominator = estimated_second_eigenvalue - 2.0 * operator_error
    return NullspaceStabilityBound(
        stable_one_dimensional_nullspace=True,
        conservative_gap_lower=gap_lower,
        sin_angle_upper=operator_error / denominator,
    )
