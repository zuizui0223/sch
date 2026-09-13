import math

from scripts.analyze_chapter1_criticality import (
    criticality_report,
    projected_critical_optimum_distance,
)


def _report(scale: float, theta2: float) -> dict:
    return criticality_report(
        {
            "theta1": 0.0,
            "theta2": theta2,
            "weight1": scale,
            "weight2": scale,
            "coupling": scale,
            "architecture_cost": 0.1 * scale,
        }
    )


def test_subcritical_and_supercritical_statuses_ignore_fitness_units():
    for scale in (1e-13, 1e-8, 1.0, 1e8, 1e13):
        below = _report(scale, 0.5)
        above = _report(scale, 1.0)

        assert (
            below["projected_architecture_status"]
            == "SHARED_WORLD_RETAINS_ARCHITECTURE_ADVANTAGE"
        )
        assert (
            above["projected_architecture_status"]
            == "DIFFERENTIATED_WORLD_FAVOURED_IF_AVAILABLE"
        )
        assert below["projected_architecture_margin"] < 0.0
        assert above["projected_architecture_margin"] > 0.0


def test_critical_surface_and_distance_ignore_fitness_units():
    reference_distance = projected_critical_optimum_distance(0.1, 1.0, 1.0, 1.0)

    for scale in (1e-13, 1e-8, 1.0, 1e8, 1e13):
        critical_distance = projected_critical_optimum_distance(
            0.1 * scale,
            scale,
            scale,
            scale,
        )
        assert math.isclose(
            critical_distance, reference_distance, rel_tol=2e-15, abs_tol=0.0
        )
        result = _report(scale, critical_distance)
        assert (
            result["projected_architecture_status"]
            == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"
        )
        assert math.isclose(
            result["projected_architecture_margin_scale"],
            0.1 * scale,
            rel_tol=2e-14,
            abs_tol=0.0,
        )


def test_margin_and_reference_scale_transform_together():
    baseline = _report(1.0, 1.0)
    for scale in (1e-13, 1e13):
        result = _report(scale, 1.0)
        assert math.isclose(
            result["projected_architecture_margin"],
            scale * baseline["projected_architecture_margin"],
            rel_tol=2e-14,
            abs_tol=0.0,
        )
        assert math.isclose(
            result["projected_architecture_margin_scale"],
            scale * baseline["projected_architecture_margin_scale"],
            rel_tol=2e-14,
            abs_tol=0.0,
        )
