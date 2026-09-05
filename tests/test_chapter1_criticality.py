import math

from scripts.analyze_chapter1_criticality import (
    classify_projected_boundary,
    criticality_report,
    decoupling_fraction,
    empirical_state_geometry,
    projected_architecture_margin,
    projected_critical_conflict_load,
    projected_critical_optimum_distance,
    shared_conflict_load,
)


def test_shared_world_conflict_onset_is_not_the_architecture_switch() -> None:
    assert shared_conflict_load(0.0, 0.0) == 0.0
    report = criticality_report(
        {
            "theta1": 0.0,
            "theta2": 1.0,
            "weight1": 1.0,
            "weight2": 1.0,
            "coupling": 1.0,
            "architecture_cost": 0.1,
        }
    )
    assert report["intrinsic_conflict_margin"] > 0
    assert report["fixed_one_axis_phase_switch"] == "NONE_IN_CURRENT_UNBOUNDED_CONVEX_QUADRATIC_MODEL"
    assert report["critical_surface_identity"] == "s*L_S* = K"


def test_reference_case_projects_the_same_boundary_from_chapter1() -> None:
    s = decoupling_fraction(1.0, 1.0, 1.0)
    assert math.isclose(s, 1.0 / 3.0)
    assert math.isclose(projected_critical_conflict_load(0.1, s), 0.3)

    dcrit = projected_critical_optimum_distance(0.1, 1.0, 1.0, 1.0)
    assert math.isclose(dcrit, math.sqrt(0.6), rel_tol=1e-12)

    margin = projected_architecture_margin(0.0, dcrit, 0.1, 1.0, 1.0, 1.0)
    assert abs(margin) < 1e-12
    assert classify_projected_boundary(margin) == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"


def test_either_side_of_reference_boundary_has_expected_projection() -> None:
    assert projected_architecture_margin(0.0, 0.5, 0.1, 1.0, 1.0, 1.0) < 0
    assert projected_architecture_margin(0.0, 1.0, 0.1, 1.0, 1.0, 1.0) > 0


def test_empirical_state_optima_do_not_identify_architecture_criticality_by_themselves() -> None:
    result = empirical_state_geometry(z_p=2.0, z_g=-2.0, z_c=0.0)
    assert result["state_optimum_separation"] == 4.0
    assert result["combined_inside_state_interval"] is True
    assert result["intrinsic_state_conflict_boundary"] == "z_P* = z_G*"
    assert result["architecture_critical_point_status"].startswith("NOT_IDENTIFIED")


def test_zero_cost_collapses_projected_architecture_threshold_to_conflict_onset() -> None:
    report = criticality_report(
        {
            "theta1": 0.0,
            "theta2": 0.0,
            "weight1": 1.0,
            "weight2": 1.0,
            "coupling": 4.0,
            "architecture_cost": 0.0,
        }
    )
    assert report["projected_critical_conflict_load"] == 0.0
    assert report["projected_critical_optimum_distance"] == 0.0
    assert report["projected_architecture_status"] == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"
