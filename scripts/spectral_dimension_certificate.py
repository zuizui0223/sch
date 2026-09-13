from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence


@dataclass(frozen=True)
class SpectralDimensionCertificate:
    registered_dimension: int
    operator_error_bound: float
    certified_min_dimension: int
    next_eigenvalue: float
    registered_dimension_rejected: bool
    frobenius_rank_d_residual: float


def certify_dimension_from_curvature_spectrum(
    eigenvalues_desc: Sequence[float],
    *,
    registered_dimension: int,
    operator_error_bound: float,
) -> SpectralDimensionCertificate:
    """Apply the SCH Weyl/Eckart-Young dimension certificate.

    Parameters
    ----------
    eigenvalues_desc
        Eigenvalues of the symmetric empirical negative weight-curvature
        matrix, ordered from largest to smallest. Small negative numerical
        values are not silently truncated: the caller should project/audit
        PSD status upstream if that is part of the registered analysis.
    registered_dimension
        Dimension ``d`` of the proposed shared phenotype coordinate.
    operator_error_bound
        Prospective bound ``epsilon`` satisfying ``||Mhat-M||_op <= epsilon``.
    """

    vals = tuple(float(v) for v in eigenvalues_desc)
    if not vals:
        raise ValueError("eigenvalues_desc must be non-empty")
    if registered_dimension < 0:
        raise ValueError("registered_dimension must be nonnegative")
    if operator_error_bound < 0:
        raise ValueError("operator_error_bound must be nonnegative")
    if any(vals[i] < vals[i + 1] for i in range(len(vals) - 1)):
        raise ValueError("eigenvalues_desc must be sorted non-increasingly")

    epsilon = float(operator_error_bound)
    certified = sum(v > epsilon for v in vals)

    if registered_dimension < len(vals):
        next_eig = vals[registered_dimension]
    else:
        next_eig = 0.0

    rejected = next_eig > epsilon
    tail = vals[registered_dimension:] if registered_dimension < len(vals) else ()
    frob = sqrt(sum(max(v, 0.0) ** 2 for v in tail))

    return SpectralDimensionCertificate(
        registered_dimension=registered_dimension,
        operator_error_bound=epsilon,
        certified_min_dimension=certified,
        next_eigenvalue=next_eig,
        registered_dimension_rejected=rejected,
        frobenius_rank_d_residual=frob,
    )
