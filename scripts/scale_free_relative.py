"""Scale-free relative-change helpers for empirical qualification gates."""

from __future__ import annotations

import math


def relative_change(value: float, reference: float) -> float:
    """Return |value-reference|/|reference| without a physical-unit floor.

    A genuinely zero reference has the mathematically degenerate behavior:
    zero versus zero is no change, while any nonzero departure is infinite
    relative change.  Positive common rescaling of both values therefore never
    changes the result.
    """

    value = float(value)
    reference = float(reference)
    if not math.isfinite(value) or not math.isfinite(reference):
        raise ValueError("relative-change inputs must be finite")
    if reference == 0.0:
        return 0.0 if value == 0.0 else math.inf
    return abs(value - reference) / abs(reference)
