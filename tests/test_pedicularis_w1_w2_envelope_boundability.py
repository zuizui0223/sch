from __future__ import annotations

from scripts.audit_pedicularis_w1_w2_envelope_boundability import (
    build,
)
from scripts.audit_pedicularis_w1_w2_power_basis import DEFAULT_LEDGER, _read


def test_current_evidence_has_zero_direct_numeric_causal_geometry_bounds() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_blocking_geometry_variance_rows"] == 18
    assert result["n_direct_same_estimand_numeric"] == 0
    assert result["any_direct_numeric_causal_geometry_bound"] is False
    assert result[
        "current_evidence_alone_supports_quantitative_robust_envelope"
    ] is False
    assert result["current_evidence_route_B_state"] == (
        "NOT_NUMERICALLY_BOUNDABLE_FROM_CURRENT_EVIDENCE_ALONE"
    )


def test_boundability_partition_is_direction_three_scale_four_unbounded_eleven() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["bound_class_counts"] == {
        "DIRECTION_ONLY_NO_MAGNITUDE": 3,
        "FOCAL_SCALE_OR_RANGE_ONLY": 4,
        "NO_NUMERIC_BOUND": 11,
    }
    assert result["n_direction_only_no_magnitude"] == 3
    assert result["n_focal_scale_or_range_only"] == 4
    assert result["n_no_numeric_bound"] == 11


def test_direction_only_evidence_does_not_bound_surface_or_slope_magnitude() -> None:
    result = build(_read(DEFAULT_LEDGER))
    direction = set(result["direction_only_paths"])

    assert direction == {
        "generating_model.state_fitness_surfaces.P1G1",
        "generating_model.pollen_state_models.P1G0",
        "generating_model.pollen_state_models.P1G1",
    }


def test_focal_scale_evidence_is_not_variance_decomposition_or_state_slope() -> None:
    result = build(_read(DEFAULT_LEDGER))
    scale = set(result["scale_or_range_only_paths"])

    assert scale == {
        "generating_model.pollen_between_plant_sd",
        "generating_model.pollen_residual_sd",
        "generating_model.initial_seed_between_plant_sd_fraction",
        "generating_model.initial_seed_residual_sd_fraction",
    }
    assert (
        "pooled_SD_is_not_promoted_to_plant_residual_variance_decomposition"
        in result["claim_ceiling"]
    )
    assert (
        "population_range_is_not_promoted_to_randomized_state_slope"
        in result["claim_ceiling"]
    )


def test_eleven_paths_have_no_numeric_bound_in_current_basis_ledger() -> None:
    result = build(_read(DEFAULT_LEDGER))
    unbounded = set(result["no_numeric_bound_paths"])

    assert len(unbounded) == 11
    assert {
        "generating_model.state_fitness_surfaces.P0G0",
        "generating_model.state_fitness_surfaces.P1G0",
        "generating_model.state_fitness_surfaces.P0G1",
        "generating_model.pollen_state_models.P0G0",
        "generating_model.pollen_state_models.P0G1",
        "generating_model.initial_seed_state_models.P0G0",
        "generating_model.initial_seed_state_models.P1G0",
        "generating_model.initial_seed_state_models.P0G1",
        "generating_model.initial_seed_state_models.P1G1",
        "generating_model.fitness_between_plant_sd",
        "generating_model.fitness_residual_sd",
    } == unbounded


def test_geometry_pilot_targets_exactly_the_eighteen_unresolved_estimand_rows() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["geometry_pilot_information_target"][
        "n_paths_directly_resolvable"
    ] == 18
    assert set(result["geometry_pilot_information_target"]["target_groups"]) == {
        "FITNESS_VARIANCE",
        "FITNESS_GEOMETRY",
        "POLLEN_VARIANCE",
        "POLLEN_GEOMETRY",
        "INITIAL_SEED_VARIANCE",
        "INITIAL_SEED_GEOMETRY",
    }
