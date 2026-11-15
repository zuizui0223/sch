"""Original published experimental beta sign-matching, strict study units."""
from copy import deepcopy
from pathlib import Path
import pytest

from scripts.analyze_sch_2020_trait_direction_persistence import (
    SOURCE,read_source,run,source_audit,
    block_distribution,select_matched_trait_blocks,
)
ROOT=Path(__file__).resolve().parents[1]


def result():
    return run(read_source(SOURCE))


def test_137_published_pairs_remain_26_source_papers_and_43_eligible():
    r=result()
    assert r["n_original_unduplicated_matched_pairs_unchanged"]==137
    assert r["n_original_independent_papers_unchanged"]==26
    assert r["n_original_all_same_sign_pairs"]==96
    assert r["n_original_all_point_sign_crossings"]==41
    g=r["source_homogeneous_distinct_trait_selection"]
    assert g["selected_blocks"]==11
    assert g["selected_original_papers"]==10
    assert g["selected_original_pairs"]==43
    assert (g["repeated_trait_blocks_excluded_as_cohort_ambiguous_pairs"]+
            g["one_trait_blocks_excluded_as_nonpermutable_pairs"]+43)==137


def test_exact_matching_sign_concordance_exceeds_fixed_margins_trait_null():
    r=result()
    p=r["primary_pair_sign_matching"]
    assert p["observed_same_sign"]==35
    assert p["n_pairs"]==43
    assert p["permutation_expected_same_sign"]==pytest.approx(24.22222222222222)
    assert p["exact_upper_tail_p_conditional_label_exchangeability"]==pytest.approx(
        .00024112654320987653,abs=1e-14)
    assert p["exact_two_sided_p_conditional_label_exchangeability"]==pytest.approx(
        .00024112654320987653,abs=1e-14)
    assert r["eligible_two_arm_approx_nominal_supported_same_sign_count"]==13
    assert r["eligible_two_arm_approx_nominal_supported_opposite_sign_count"]==0


def test_equal_paper_weights_and_class_constrained_null():
    r=result()
    p=r["paper_equal_weight"]
    assert p["n_papers"]==10
    assert len(p["paper_source_receipts"])==10
    assert p["paper_equal_weight_observed_same_sign_fraction"]==pytest.approx(
        .8152777777777778,abs=1e-12)
    assert p["paper_equal_weight_expected_same_sign_fraction"]==pytest.approx(
        .5999228395061729,abs=1e-12)
    assert p["exact_paper_equal_upper_tail_p"]==pytest.approx(
        .00014467592592592592,abs=1e-14)
    restricted=r["same_cohort_trait_class_constrained_repairing"]
    assert restricted["n_pairs"]==43
    assert restricted["observed_same_sign"]==35
    assert restricted["permutation_expected_same_sign"]==pytest.approx(28.73809523809524)
    assert restricted["exact_upper_tail_p_conditional_label_exchangeability"]==pytest.approx(
        .011904761904761904,abs=1e-14)


def test_eight_original_species_are_not_ten_independent_taxa():
    r=result()
    s=r["species_equal_weight"]
    assert s["n_distinct_original_species"]==8
    assert s["source_paper_count_across_species"]==10
    assert s["species_equal_weight_observed_fraction"]==pytest.approx(
        .8425480769230769,abs=1e-12)
    assert s["species_equal_weight_expected_fraction"]==pytest.approx(
        .6038900335775337,abs=1e-12)
    assert s["species_equal_exact_upper_tail_p"]==pytest.approx(
        .00014467592592592592,abs=1e-14)
    species_rows={x["source_species"]:x for x in s["original_species_source_rows"]}
    assert species_rows["Avena barbata"]["distinct_source_papers"]==2
    assert species_rows["Arabidopsis thaliana"]["distinct_source_papers"]==2
    loo=r["leave_one_original_species_out"]
    assert len(loo)==8
    assert loo["Avena barbata"]["n_pairs"]==30
    assert loo["Arabidopsis thaliana"]["n_pairs"]==36
    assert max(x["exact_upper_tail_p_conditional_label_exchangeability"] for x in loo.values())<.00171


def test_one_original_paper_left_out_means_all_its_contexts():
    r=result()
    loo=r["leave_one_entire_paper_out"]
    assert len(loo)==10
    assert loo["13"]["n_pairs"]==35
    assert max(v["exact_upper_tail_p_conditional_label_exchangeability"]
               for v in loo.values())<.00171
    assert not r["randomized_trait_assignment_performed"]
    assert not r["cross_study_effect_size_meta_pooling_performed"]
    assert not r["new_field_plants_or_source_gradients_measured"]


def test_exact_hypergeometric_distribution_sums_to_one():
    b,_=select_matched_trait_blocks(read_source(SOURCE))
    assert len(b)==11
    for group in b:
        item=block_distribution(group)
        assert sum(item["pmf"].values())==1
        assert item["expected"]>=0


@pytest.mark.parametrize("mutation",["source_count","source_flip","beta","missing_group","duplicate_key"])
def test_fail_closed_against_source_grain_and_numeric_drift(mutation):
    q=deepcopy(read_source(SOURCE))
    if mutation=="source_count":
        q.pop()
    elif mutation=="source_flip":
        q[0]["point_sign_flip"]="true" if q[0]["point_sign_flip"]=="false" else "false"
    elif mutation=="beta":
        q[0]["beta1"]="0"
    elif mutation=="missing_group":
        q[0]["fitness_measure"]=""
    elif mutation=="duplicate_key":
        q[1]["paper_id"]=q[0]["paper_id"]
        q[1]["source_row_id_1"]=q[0]["source_row_id_1"]
        q[1]["source_row_id_2"]=q[0]["source_row_id_2"]
    with pytest.raises(ValueError):
        run(q)


def test_document_keeps_43_of_137_selection_boundary():
    t=(ROOT/"docs/SCH_2020_TRAIT_SIGN_PERSISTENCE_META_V1.md").read_text(
        encoding="utf-8")
    for x in ("137", "43", "10 separate original papers", "8 distinct original species", "0.00024113",
              "0.01190476", "0.00014468", "13 pairs",
              "trait-label re-pairing reference", "does not", "L"):
        assert x.lower() in t.lower()
