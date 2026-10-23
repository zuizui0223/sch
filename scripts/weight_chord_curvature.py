from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChordGapBounds:
    lower: float
    upper: float
    observed_gap: float | None = None
    violates_lower: bool = False
    violates_upper: bool = False


def concave_chord_gap_bounds(
    *,
    curvature_lower: float,
    curvature_upper: float,
    t: float,
    direction_metric_norm_sq: float = 1.0,
) -> tuple[float, float]:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must lie in [0, 1]")
    if curvature_lower < 0.0 or curvature_upper < curvature_lower:
        raise ValueError("curvature bounds must satisfy 0 <= lower <= upper")
    if direction_metric_norm_sq < 0.0:
        raise ValueError("direction metric norm squared must be nonnegative")
    factor = 0.5 * t * (1.0 - t) * direction_metric_norm_sq
    return curvature_lower * factor, curvature_upper * factor


def audit_concave_chord_gap(
    *,
    endpoint0: float,
    endpoint1: float,
    observed: float,
    curvature_lower: float,
    curvature_upper: float,
    t: float,
    direction_metric_norm_sq: float = 1.0,
    tolerance: float = 0.0,
) -> ChordGapBounds:
    if tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")
    lower, upper = concave_chord_gap_bounds(
        curvature_lower=curvature_lower,
        curvature_upper=curvature_upper,
        t=t,
        direction_metric_norm_sq=direction_metric_norm_sq,
    )
    chord = (1.0 - t) * endpoint0 + t * endpoint1
    gap = observed - chord
    return ChordGapBounds(
        lower=lower,
        upper=upper,
        observed_gap=gap,
        violates_lower=gap < lower - tolerance,
        violates_upper=gap > upper + tolerance,
    )
