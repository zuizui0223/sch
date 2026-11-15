"""Original author source-reverified context moderation vs signed-component conflict."""
from copy import deepcopy
from pathlib import Path
import pytest

from scripts.audit_sch_primary_reversal_mechanisms_v1 import (
    PAIRS,CANDIDATES,MODERATION,COMPONENTS,INDIRECT,csv_read,run,
)

ROOT=Path(__file__).resolve().parents[1]


def data():
    return [csv_read(p) for p in (PAIRS,CANDIDATES,MODERATION,COMPONENTS,INDIRECT)]


def verified():
    return run(*data())


def test_original_137_point_crossings_strength_and_five_highest_candidates():
    r=verified()
    assert r["n_original_matched_beta_pairs"]==137
    assert r["n_original_source_papers"]==26
    assert r["n_source_point_sign_crossings"]==41
    assert r["n_crossings_with_min_arm_z_below_one"]==36
    assert r["n_crossings_with_min_arm_z_between_one_and_1_96"]==5
    assert r["n_crossings_with_both_arm_z_at_least_1_96"]==0
    assert r["n_high_information_point_crossing_candidates_with_source_primary_qa"]==5
    assert r["n_high_information_crossings_with_author_certified_own_trait_reversal"]==0
    by={tuple(x["source_key"]):x for x in r["source_crossing_audit"]}
    assert set(by)=={
        ("21","295","301"),("33","429","430"),("41","530","542"),
        ("41","533","545"),("41","535","547")}
    assert by[("21","295","301")]["author_direct_stat"]=="F=1.79"
    assert by[("33","429","430")]["author_test_scope"]=="POOLED_12_SPECIES_FLOWERING_X_POLLINATION"
    assert all(not x["species_level_original_author_fitted_reversal_certified"]
               for x in by.values())


def test_original_direct_treatment_moderation_preserves_selection_signs():
    r=verified()
    a={x["paper_id"]:x for x in r["source_verified_same_sign_treatment_modulation"]}
    assert set(a)=={"21","41"}
    c=a["21"]
    assert c["source_pair_ids"]==["294","300"]
    assert c["source_beta1"]==pytest.approx(-.820)
    assert c["source_beta2"]==pytest.approx(-.215)
    assert tuple(c["author_original_direct_interaction"])==("PHENOTYPIC_CUP_X_SHADE","F=13.57","<0.001")
    assert tuple(c["author_original_secondary_interaction"])==("GENOTYPIC_CUP_X_SHADE","F=4.14","<0.05")
    leaf=a["41"]
    assert leaf["source_pair_ids"]==["537","549"]
    assert leaf["source_beta1"]==pytest.approx(.120)
    assert leaf["source_beta2"]==pytest.approx(.240)
    assert tuple(leaf["author_original_direct_interaction"])==("HERBIVORY_X_SLA_IN_SHADE","chi2=16.10","0.008")
    assert all(not x["treatment_sign_crossing"] for x in a.values())


def test_same_female_trait_two_reproductive_components_opposed_in_one_study():
    r=verified()
    q=r["same_female_individuals_sexual_vs_asexual_fitness_components"]
    assert q["n_individuals"]==31
    assert q["trait"]=="age_at_first_sexual_expression"
    assert q["both_source_gradients_nominally_individually_reported_nonzero_opposite"]
    by={x["fitness_component"]:x for x in q["component_gradients"]}
    assert by["SEXUAL"]["beta_pheno"]==pytest.approx(-.915)
    assert by["ASEXUAL"]["beta_pheno"]==pytest.approx(+.496)
    assert by["SEXUAL"]["published_nominal_significance"]=="<0.02"
    assert by["ASEXUAL"]["published_nominal_significance"]=="<0.05"
    assert q["arithmetic_beta_asexual_minus_beta_sexual"]==pytest.approx(1.411)
    assert q["direct_fitness_component_difference_p_reported"] is False
    assert q["genotype_level_dual_component_confirmation_reported"] is False
    assert q["original_trait_z_randomized"] is False
    assert q["measured_SCH_conflict_loss_L"] is False


def test_male_area_total_selection_shift_not_verified_direct_gradient_shift():
    r=verified()
    x=r["same_study_male_direct_vs_total_selection"]
    assert x["source_pair_ids"]==["296","302"]
    assert x["male_area_direct_beta_73pct"]==pytest.approx(.640)
    assert x["male_area_direct_beta_55pct"]==pytest.approx(-.199)
    assert x["author_direct_area_x_shade_F"]==pytest.approx(3.31)
    assert x["original_direct_interaction_significant"] is False
    assert x["author_total_area_x_shade_F"]==pytest.approx(3.90)
    assert x["original_total_selection_interaction_reported_p"]=="<0.05"
    assert x["two_individually_supported_opposite_total_slopes"] is False


@pytest.mark.parametrize("mutation",[
    "n_original","original_beta","primary_source","pooled_species_test",
    "shade_sla_p","genotype_f","sexual_fit_sign","component_cohort",
    "total_female_model","male_total_model",
])
def test_primary_source_tampering_fails_closed(mutation):
    q=[deepcopy(x) for x in data()]
    pairs,candidates,moderation,components,indirect=q
    if mutation=="n_original":pairs.pop()
    elif mutation=="original_beta":pairs[0]["beta1"]="0"
    elif mutation=="primary_source":candidates[0]["primary_doi"]="10.9999/invalid"
    elif mutation=="pooled_species_test":candidates[1]["author_test_scope"]="SPECIES_SPECIFIC_NEOTTIA"
    elif mutation=="shade_sla_p":moderation[1]["author_direct_p"]="0.000001"
    elif mutation=="genotype_f":moderation[0]["secondary_stat"]="F=14.14"
    elif mutation=="sexual_fit_sign":components[0]["original_standardized_beta"]="0.915"
    elif mutation=="component_cohort":components[1]["n_sex_expressing_individuals"]="32"
    elif mutation=="total_female_model":indirect[0]["author_total_area_x_shade_F"]="30.90"
    elif mutation=="male_total_model":indirect[0]["author_direct_area_x_shade_p"]="<0.05"
    with pytest.raises(ValueError):
        run(*q)


def test_research_interpretation_retains_exact_scope_and_conflict_ceiling():
    source=(ROOT/"docs/SCH_2020_REVERSAL_MECHANISMS_SOURCE_CONFLICT_V1.md").read_text(encoding="utf-8")
    for marker in (
        "36/41","5/41","0/41","13.57","4.14",
        "0.008","0.496","0.915","same 31","3.90","3.31",
        "Table 7","L is NOT identified","not a demonstrated three-way",
    ):
        assert marker.lower() in source.lower()
