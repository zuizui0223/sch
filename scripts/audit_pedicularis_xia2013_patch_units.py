from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "data" / "PEDICULARIS_XIA2013_PATCH_UNIT_AUDIT_V1.csv"

EXPECTED_INTERACTION_F = {
    "fruit_set": (3.060, 54),
    "initial_seed_set": (44.556, 2047),
    "final_seed_set": (0.023, 2345),
    "fruit_predation": (10.605, 54),
    "seed_predation": (106.270, 2345),
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Xia2013 patch-unit ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("Xia2013 patch-unit ledger is empty")
    return rows


def seed_output_decomposition(
    initial_seed_fractions: list[float],
    predation_fractions: list[float],
) -> dict[str, float]:
    """Algebraic diagnostic; requires the two fractions from the SAME capsules.

    Initial seed fraction I = (intact + damaged) / ovules.
    Predation fraction q = damaged / (intact + damaged), when defined.
    Final intact seed fraction F = I * (1-q).
    """
    if len(initial_seed_fractions) != len(predation_fractions):
        raise ValueError("initial and predation fractions must have matched capsules")
    if not initial_seed_fractions:
        raise ValueError("at least one matched capsule is required")
    if any(
        not math.isfinite(value) or not 0 <= value <= 1
        for value in initial_seed_fractions + predation_fractions
    ):
        raise ValueError("fractions must be finite and lie in [0,1]")

    mean_initial = mean(initial_seed_fractions)
    mean_predation = mean(predation_fractions)
    mean_product = mean(
        initial * predation
        for initial, predation in zip(
            initial_seed_fractions, predation_fractions, strict=True
        )
    )
    covariance = mean_product - mean_initial * mean_predation
    final = mean(
        initial * (1 - predation)
        for initial, predation in zip(
            initial_seed_fractions, predation_fractions, strict=True
        )
    )
    reconstructed = (
        mean_initial * (1 - mean_predation) - covariance
    )
    if not math.isclose(final, reconstructed, abs_tol=1e-12):
        raise ValueError("same-capsule decomposition identity failed")

    return {
        "mean_initial_seed_fraction": mean_initial,
        "mean_seed_predation_fraction": mean_predation,
        "initial_predation_covariance": covariance,
        "mean_final_seed_fraction": final,
        "mean_only_prediction_without_covariance": (
            mean_initial * (1 - mean_predation)
        ),
        "decomposition_reconstructs_final_seed_fraction": True,
    }


def build(rows: list[dict[str, str]]) -> dict:
    by_endpoint = {row["endpoint"]: row for row in rows}
    if len(by_endpoint) != len(rows) or set(by_endpoint) != set(
        EXPECTED_INTERACTION_F
    ):
        raise ValueError("Xia2013 Table 2 must have exactly five unique endpoints")

    records = []
    for endpoint, (expected_f, expected_denominator_df) in (
        EXPECTED_INTERACTION_F.items()
    ):
        row = by_endpoint[endpoint]
        if row["source_doi"] != "10.1098/rsbl.2013.0387":
            raise ValueError("Xia2013 source DOI drifted")
        if row["study_year"] != "2011" or row["predictor_unit"] != "patch":
            raise ValueError("Xia2013 patch-level design context drifted")
        if int(row["df_numerator"]) != 1:
            raise ValueError("Xia2013 interaction numerator df drifted")
        reported_f = float(row["reported_F_density_by_size"])
        denominator_df = int(row["df_denominator"])
        if (
            not math.isclose(reported_f, expected_f, abs_tol=1e-6)
            or denominator_df != expected_denominator_df
        ):
            raise ValueError(f"Xia2013 published Table 2 values drifted for {endpoint}")
        n_patches = int(row["independent_patches_2011"])
        sparse = int(row["sparse_patches_2011"])
        dense = int(row["dense_patches_2011"])
        spikes = int(row["sampled_spikes_2011"])
        if (n_patches, sparse, dense, spikes) != (11, 5, 6, 58):
            raise ValueError("Xia2013 published patch/plant sampling frame drifted")

        records.append({
            "endpoint": endpoint,
            "reported_F_density_by_size": reported_f,
            "reported_test_df": [1, denominator_df],
            "reported_significance": row["published_significance"],
            "response_unit": row["response_unit"],
            "independent_patch_units": n_patches,
            "reported_denominator_df_exceeds_independent_patches": (
                denominator_df > n_patches
            ),
            "patch_cluster_robust_interval_recovered": False,
        })

    reported = {record["endpoint"]: record for record in records}
    if not (
        reported["initial_seed_set"]["reported_significance"] == "P_LE_0_001"
        and reported["seed_predation"]["reported_significance"] == "P_LE_0_001"
        and reported["final_seed_set"]["reported_significance"]
        == "NOT_SIGNIFICANT"
    ):
        raise ValueError("Xia2013 initial/predation/final contrast drifted")

    return {
        "analysis": "pedicularis_xia2013_patch_unit_inference_audit_v1",
        "source_doi": "10.1098/rsbl.2013.0387",
        "year": 2011,
        "independent_spatial_units": {
            "patches": 11,
            "sparse_patches": 5,
            "dense_patches": 6,
            "sampled_spikes": 58,
        },
        "reported_interaction_tests": records,
        "cross_endpoint_pattern": {
            "initial_seed_set_interaction_reported": True,
            "seed_predation_interaction_reported": True,
            "final_seed_set_interaction_not_detected": True,
            "cross_endpoint_equivalence_or_cancellation_identified": False,
            "seed_predation_patch_level_effect_size_estimated": False,
        },
        "published_predation_patch_size_direction": {
            "sparse_patches": "SMALL_PATCHES_GREATER_PREDATION",
            "dense_patches": "LARGE_PATCHES_GREATER_PREDATION",
            "direction_reversal_reported": True,
            "patch_cluster_robust_uncertainty_recovered": False,
        },
        "inference_gate": {
            "patch_level_predictor_with_nested_plant_or_capsule_responses": True,
            "published_test_denominator_df_not_patch_replication_count": True,
            "hierarchical_or_patch_level_refit_needed": True,
            "robust_density_by_size_interaction_identified": False,
            "functional_optimum_displacement_identified": False,
            "predation_rate_as_randomized_G_identified": False,
        },
        "biological_discriminators_for_raw_data": [
            "does_patch_size_predation_slope_really_reverse_within_density_after_patch_level_inference",
            "does_initial_seed_set_predation_covariance_change_across_density_size_contexts",
            "is_final_seed_set_cross_context_contrast_consistent_with_initial_predation_covariance_decomposition",
            "does_any_context_effect_remain_after_patch_and_plant_hierarchies_are_respected",
        ],
        "raw_data_prerequisites": [
            "legitimate_Xia2013_Dryad_raw_data_xlsx_file_46101",
            "same_capsule_initial_seed_and_damaged_seed_counts_and_ovule_denominator",
            "unique_patch_identifier_and_plant_identifier",
            "density_and_patch_size_at_patch_level",
        ],
        "status": "SUGGESTIVE_CONTEXT_REVERSAL_PATCH_LEVEL_INFERENCE_UNRESOLVED",
        "claim_ceiling": [
            "reported_observational_patch_size_direction_reversal_only",
            "do_not_call_reported_F_patch_robust",
            "do_not_treat_2345_denominator_df_as_independent_patches",
            "nonsignificant_final_seed_interaction_is_not_equivalence",
            "do_not_claim_fecundity_predation_compensation_without_matched_raw_data",
            "do_not_promote_2013_context_to_exsertion_specific_optimum_shift",
            "no_registered_F0_gate_values_recovered",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit Xia2013 patch-level replication and qualify the ecological "
            "density x patch-size reversal without treating nested seeds as patches"
        )
    )
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read(args.evidence))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
