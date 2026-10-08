from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_xia2013_patch_units import (
    DEFAULT_EVIDENCE,
    _read,
    build,
    seed_output_decomposition,
)


def test_xia2013_reports_eleven_patches_not_thousands_of_patch_replicates() -> None:
    result = build(_read(DEFAULT_EVIDENCE))

    assert result["independent_spatial_units"] == {
        "patches": 11,
        "sparse_patches": 5,
        "dense_patches": 6,
        "sampled_spikes": 58,
    }
    by_endpoint = {
        row["endpoint"]: row
        for row in result["reported_interaction_tests"]
    }
    assert by_endpoint["initial_seed_set"]["reported_test_df"] == [1, 2047]
    assert by_endpoint["final_seed_set"]["reported_test_df"] == [1, 2345]
    assert by_endpoint["seed_predation"]["reported_test_df"] == [1, 2345]
    assert by_endpoint["fruit_predation"]["reported_test_df"] == [1, 54]
    assert all(
        row["reported_denominator_df_exceeds_independent_patches"]
        for row in by_endpoint.values()
    )
    assert all(
        row["patch_cluster_robust_interval_recovered"] is False
        for row in by_endpoint.values()
    )


def test_context_reversal_is_recorded_as_observational_not_robust_causal() -> None:
    result = build(_read(DEFAULT_EVIDENCE))

    direction = result["published_predation_patch_size_direction"]
    assert direction["sparse_patches"] == "SMALL_PATCHES_GREATER_PREDATION"
    assert direction["dense_patches"] == "LARGE_PATCHES_GREATER_PREDATION"
    assert direction["direction_reversal_reported"] is True
    assert direction["patch_cluster_robust_uncertainty_recovered"] is False
    assert result["inference_gate"]["robust_density_by_size_interaction_identified"] is False
    assert result["inference_gate"]["functional_optimum_displacement_identified"] is False
    assert result["status"] == (
        "SUGGESTIVE_CONTEXT_REVERSAL_PATCH_LEVEL_INFERENCE_UNRESOLVED"
    )


def test_final_seed_set_non_significance_is_not_compensation_or_equivalence() -> None:
    result = build(_read(DEFAULT_EVIDENCE))
    pattern = result["cross_endpoint_pattern"]

    assert pattern["initial_seed_set_interaction_reported"] is True
    assert pattern["seed_predation_interaction_reported"] is True
    assert pattern["final_seed_set_interaction_not_detected"] is True
    assert pattern["cross_endpoint_equivalence_or_cancellation_identified"] is False
    assert "nonsignificant_final_seed_interaction_is_not_equivalence" in (
        result["claim_ceiling"]
    )
    assert "do_not_claim_fecundity_predation_compensation_without_matched_raw_data" in (
        result["claim_ceiling"]
    )


def test_published_table_two_statistics_cannot_silently_drift() -> None:
    rows = _read(DEFAULT_EVIDENCE)
    changed = deepcopy(rows)
    for row in changed:
        if row["endpoint"] == "seed_predation":
            row["reported_F_density_by_size"] = "1.0"

    with pytest.raises(ValueError, match="published Table 2 values drifted"):
        build(changed)


def test_covariance_can_change_final_seed_output_with_identical_marginals() -> None:
    initial = [0.2, 0.8]
    coupling = seed_output_decomposition(initial, [0.0, 0.5])
    anticoupling = seed_output_decomposition(initial, [0.5, 0.0])

    assert coupling["mean_initial_seed_fraction"] == pytest.approx(0.5)
    assert anticoupling["mean_initial_seed_fraction"] == pytest.approx(0.5)
    assert coupling["mean_seed_predation_fraction"] == pytest.approx(0.25)
    assert anticoupling["mean_seed_predation_fraction"] == pytest.approx(0.25)
    assert coupling["initial_predation_covariance"] == pytest.approx(0.075)
    assert anticoupling["initial_predation_covariance"] == pytest.approx(-0.075)
    assert coupling["mean_final_seed_fraction"] == pytest.approx(0.30)
    assert anticoupling["mean_final_seed_fraction"] == pytest.approx(0.45)
    assert coupling["decomposition_reconstructs_final_seed_fraction"]
    assert anticoupling["decomposition_reconstructs_final_seed_fraction"]


def test_covariance_diagnostic_rejects_unmatched_or_impossible_capsule_data() -> None:
    with pytest.raises(ValueError, match="matched capsules"):
        seed_output_decomposition([0.2, 0.8], [0.5])
    with pytest.raises(ValueError, match="\[0,1\]"):
        seed_output_decomposition([0.2], [1.1])
    with pytest.raises(ValueError, match="at least one matched"):
        seed_output_decomposition([], [])
