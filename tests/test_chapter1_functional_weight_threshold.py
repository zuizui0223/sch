import math

from scripts.analyze_chapter1_functional_weight_threshold import (
    asymptotic_recovery,
    recoverable_loss,
    report,
    solve_critical_function2_weight,
)


def test_finite_weight_threshold_hits_imported_architecture_boundary() -> None:
    result = solve_critical_function2_weight(1.0, 1.0, 1.0, 0.1)
    bcrit = result["critical_function2_weight"]
    assert result["status"] == "FINITE_PROJECTED_FUNCTION2_WEIGHT_CRITICAL_POINT"
    assert bcrit is not None
    assert math.isfinite(bcrit)
    assert math.isclose(recoverable_loss(bcrit, 1.0, 1.0, 1.0), 0.1, rel_tol=1e-12, abs_tol=1e-12)


def test_recovery_has_finite_upper_bound_as_function2_weight_increases() -> None:
    ceiling = asymptotic_recovery(1.0, 1.0, 1.0)
    assert math.isclose(ceiling, 0.5)
    values = [recoverable_loss(b, 1.0, 1.0, 1.0) for b in (0.1, 1.0, 10.0, 1000.0)]
    assert all(right > left for left, right in zip(values, values[1:]))
    assert values[-1] < ceiling
    assert math.isclose(values[-1], ceiling, rel_tol=3e-3)


def test_cost_above_ceiling_creates_balance_only_world() -> None:
    result = solve_critical_function2_weight(1.0, 1.0, 1.0, 0.6)
    assert result["critical_function2_weight"] is None
    assert result["status"] == "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_BALANCE_ONLY"


def test_cost_at_ceiling_has_only_asymptotic_boundary() -> None:
    result = solve_critical_function2_weight(1.0, 1.0, 1.0, 0.5)
    assert result["critical_function2_weight"] == math.inf
    assert result["status"] == "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING"


def test_zero_architecture_cost_collapses_projected_threshold_to_conflict_onset() -> None:
    result = solve_critical_function2_weight(1.0, 2.0, 1.0, 0.0)
    assert result["critical_function2_weight"] == 0.0
    assert result["status"] == "ZERO_COST_COLLAPSES_PROJECTED_ARCHITECTURE_THRESHOLD_TO_CONFLICT_ONSET"


def test_report_keeps_sch_intrinsic_and_cross_architecture_boundaries_distinct() -> None:
    result = report(
        {
            "function1_weight": 1.0,
            "coupling": 1.0,
            "optimum_distance": 1.0,
            "architecture_cost": 0.1,
        }
    )
    assert result["chapter"] == "SCH_CHAPTER_1_BALANCE"
    assert result["critical_surface_identity"] == "s(b)*L_S*(b)=K"
    assert result["intrinsic_sch_phase_switch"] == "NONE_IN_CURRENT_CONVEX_ONE_AXIS_MODEL"
    assert math.isclose(result["boundary_recoverable_loss"], 0.1, rel_tol=1e-12)
