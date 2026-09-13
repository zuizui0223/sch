import math

from scripts.analyze_chapter1_functional_weight_threshold import (
    solve_critical_function2_weight,
)


def test_finite_critical_weight_scales_with_fitness_units():
    reference = solve_critical_function2_weight(1.0, 1.0, 1.0, 0.1)
    assert reference["status"] == "FINITE_PROJECTED_FUNCTION2_WEIGHT_CRITICAL_POINT"
    reference_b = reference["critical_function2_weight"]
    assert isinstance(reference_b, float) and math.isfinite(reference_b)

    for scale in (1e-13, 1e-8, 1.0, 1e8, 1e13):
        result = solve_critical_function2_weight(
            scale,
            scale,
            1.0,
            0.1 * scale,
        )
        assert result["status"] == reference["status"]
        assert math.isclose(
            result["critical_function2_weight"],
            scale * reference_b,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert math.isclose(
            result["asymptotic_recoverable_loss"],
            0.5 * scale,
            rel_tol=2e-15,
            abs_tol=0.0,
        )


def test_above_and_at_ceiling_statuses_are_fitness_scale_invariant():
    for scale in (1e-13, 1.0, 1e13):
        above = solve_critical_function2_weight(
            scale, scale, 1.0, 0.6 * scale
        )
        assert above["critical_function2_weight"] is None
        assert above["status"] == "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_BALANCE_ONLY"

        at = solve_critical_function2_weight(
            scale, scale, 1.0, 0.5 * scale
        )
        assert at["critical_function2_weight"] == math.inf
        assert at["status"] == "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING"


def test_positive_tiny_cost_is_not_collapsed_to_zero_cost():
    result = solve_critical_function2_weight(
        1e-13,
        1e-13,
        1.0,
        1e-14,
    )
    assert result["status"] == "FINITE_PROJECTED_FUNCTION2_WEIGHT_CRITICAL_POINT"
    assert result["critical_function2_weight"] > 0.0


def test_exact_zero_cost_and_zero_conflict_boundaries_are_preserved():
    for scale in (1e-13, 1.0, 1e13):
        zero_cost = solve_critical_function2_weight(scale, scale, 1.0, 0.0)
        assert zero_cost["critical_function2_weight"] == 0.0
        assert (
            zero_cost["status"]
            == "ZERO_COST_COLLAPSES_PROJECTED_ARCHITECTURE_THRESHOLD_TO_CONFLICT_ONSET"
        )

        no_conflict_positive_cost = solve_critical_function2_weight(
            scale, scale, 0.0, 0.1 * scale
        )
        assert no_conflict_positive_cost["critical_function2_weight"] is None
        assert (
            no_conflict_positive_cost["status"]
            == "NO_CONFLICT_SHARED_WORLD_ALWAYS_FAVOURED"
        )

        zero_conflict_zero_cost = solve_critical_function2_weight(
            scale, scale, 0.0, 0.0
        )
        assert zero_conflict_zero_cost["critical_function2_weight"] == 0.0
        assert zero_conflict_zero_cost["status"] == "ALL_WEIGHTS_ON_ZERO_CONFLICT_BOUNDARY"
