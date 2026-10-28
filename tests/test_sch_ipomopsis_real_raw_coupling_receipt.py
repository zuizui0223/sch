"""Protect the REAL original-row, source-hashed Ipomopsis reanalysis receipt.

These tests do not recompute original data in offline CI: the original public
CSV is downloaded + MD5-verified + analyzed separately by the dedicated
network-enabled GitHub Actions workflow, with its run ID frozen here.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/SCH_IPOMOPSIS_REAL_RAW_STAGE_COUPLING_RESULT_V1.json"
DOI="10.7280/D1KM49"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_genuine_archived_raw_data_not_derived_published_table():
    r=_result()
    assert r["original_data_doi"]==DOI
    assert r["source_original_n_rows"]==437
    assert r["n_independent_study_programmes"]==1
    assert r["n_cohorts_eligible"]==15
    assert r["n_cohorts_secondary"]==15
    assert r["n_matched_rows_primary"]==297
    assert r["n_matched_rows_secondary"]==277
    assert r["n_eligible_original_year_blocks"]==8
    assert r["provenance"]["original_csv_md5"]=="12ed3dbe6d269c5f808f9c6b230d468c"
    assert r["provenance"]["original_dictionary_md5"]=="e681a5a0885271c4797730b5a30574d8"
    assert r["provenance"]["github_run_id"]==40615189536
    assert r["provenance"]["github_job_id"]==122575907876


def test_original_null_does_not_get_promoted_to_significant_coupling():
    r=_result()
    assert -.0150<r["primary_normalized_mean_coupling"]<-.0148
    assert r["primary_within_cohort_shuffle_p_two_sided"]==0.102
    assert r["primary_familywise_two_test_adjusted_p"]==0.204
    assert -.0193<r["secondary_width_coupling_delta"]<-.0190
    assert r["secondary_shuffle_p_two_sided"]==0.2566
    assert r["secondary_familywise_two_test_adjusted_p"]==0.5132
    a,b=r["original_year_block_resampling_ci_95pct_primary"]
    assert a<0<b
    a,b=r["original_year_block_resampling_ci_95pct_secondary"]
    assert a<0<b
    assert r["n_permutations"]==4999
    assert r["fixed_random_seed"]==20261028
    assert r["n_width_cohorts_where_stage_proxy_sign_differs_from_marginal_prediction"]==0
    assert r["n_width_cohorts_with_observed_final_seed_direction_check"]==15
    assert r["n_width_cohorts_proxy_and_measured_final_seed_sign_agree"]==15


def test_remaining_uncertainty_and_original_plant_grain_are_material():
    r=_result()
    limits=r["interpretive_limits"]
    assert "fruit_escape_is_proportion_of_fruits_not_seed_survival" in limits
    assert "initiated_times_escape_is_a_labelled_proxy_not_real_final_seeds" in limits
    assert "original_seed_count_can_exceed_reported_initiated_estimate" in limits
    assert "year_bootstrap_only_eight_eligible_year_blocks_in_one_original_study" in limits
    assert "no_empirically_estimated_SCH_L_or_pure_function_optima" in limits
    assert set(r["per_source_site_summary"])=={"agg","hyb","ten"}
    assert len(r["cohort_effects"])==15
    assert sum(x["n_matched_stage_rows"] for x in r["cohort_effects"])==297
    assert r["excluded_rows"]=={
        "in_small_group":78,"incomplete_stage_pair":62
    }


def test_genuine_observational_result_is_explicitly_separate_from_main_review():
    note=(ROOT/"docs/SCH_IPOMOPSIS_ORIGINAL_ROW_COUPLING_EMPIRICAL_RESULT_V1.md").read_text(
        encoding="utf-8")
    assert "437" in note
    assert "375/437" in note
    assert "40/375" in note
    assert "297 matched source rows" in note
    assert "0.1020" in note
    assert "0.2566" in note
    assert "NOT rejected" in note
    assert "not a new field experiment" in note.lower() or "not a new field experiment" in (
        "This is not a new field experiment").lower()
    assert "no empirical SCH loss" not in note.lower() or "not estimated" in note.lower()
