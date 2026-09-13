"""Scale-free relative-change helper for field qualification gates."""

from __future__ import annotations

import math


def relative_change(value: float, reference: float) -> float:
    """Return absolute change relative to ``reference`` without a unit floor.

    A positive rescaling of both inputs leaves the result unchanged.  At an
    exact zero reference, no change is zero and any nonzero change is treated
    as unbounded rather than being made finite by an arbitrary physical-unit
    epsilon.
    """

    value = float(value)
    reference = float(reference)
    if not math.isfinite(value) or not math.isfinite(reference):
        raise ValueError("relative-change inputs must be finite")
    if reference == 0.0:
        return 0.0 if value == 0.0 else math.inf
    return abs(value / reference - 1.0)
