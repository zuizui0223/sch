"""Assess temporal and internal univariate-selection compatibility for Marchantia 2002.

On the selected phenotypic cohort the original analysis regresses
day-120 asexual-cup count on date of first sexual expression; original
Table1 reports mean sexual onset day132.9 for the wider n40 females,
whereas paired selection gradients use n31 complete females. Those
cohorts cannot be conflated.

Reported original Table6 univariate 's' for sexual onset vs sex
structures is +.243, whereas Table7 Pearson r between these variables
is -.56. Conditional on both using identical observations and a
positively oriented date/fitness outcome, a univariate linear
selection differential s and r MUST have the same sign. Thus this is
an *unresolved source-level provenance/estimand discrepancy*, not proof
that published numbers are wrong without the 31 original plant records.

All original values from Fuselier & McLetchie 2002 AJB, DOI:
10.3732/ajb.89.4.592. Dissertation (Fuselier 2004), UKnowledge,
reproduces Tables 6.6 and 6.7 and source r/s signs.

This is a readout of source numbers, NOT a refit of original plants.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/SCH_MARCHANTIA2002_SEXUAL_ASEXUAL_TEMPORAL_SOURCE_V1.csv"
DOI="10.3732/ajb.89.4.592"
EXPECTED={
 "asexual_cup_count_observation_day":("Methods_Clonal_fitness","day",120.0,102,"all_females_55_shade"),
 "sexual_structure_count_observation_day":("Methods_Sexual_fitness","day",150.0,40,"sex_expressing_females_55_shade"),
 "mean_first_sex_expression_day":("Table1","day_mean",132.9,40,"sex_expressing_females_55_shade"),
 "sexual_selection_regression_n":("Table6","individual_count",31.0,31,"sexual_selection_model_females_55_shade"),
 "sexual_onset_multivariate_beta_sexual_structures":("Table6","standardized_beta",-.915,31,"sexual_selection_model_females_55_shade"),
 "sexual_onset_multivariate_beta_asexual_cups":("Results_Sexual_fitness","standardized_beta",+.496,31,"asexual_selection_model_females_55_shade"),
 "sexual_onset_total_selection_s":("Table6","selection_differential",+.243,31,"sexual_selection_model_females_55_shade"),
 "sexual_onset_versus_sex_structures_Pearson_r":("Table7","pearson_r",-.56,31,"sexual_selection_model_females_55_shade"),
}


def read_rows(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run(rows):
    if len(rows)!=len(EXPECTED):
        raise ValueError("source Marchantia item count changed")
    values={}
    for row in rows:
        key=row["metric"]
        if key in values or key not in EXPECTED:
            raise ValueError("duplicate/unknown original study measure")
        table,typ,value,n,cohort=EXPECTED[key]
        if ((row["source_doi"],row["source_location"],row["metric_type"],
             row["cohort"],row["sex"],row["shade_percent"])
            !=(DOI,table,typ,cohort,"FEMALE","55")
            or abs(float(row["published_value"])-value)>1e-10
            or row["original_sample_n"]!=str(n)):
            raise ValueError("original Marchantia source timing, sample or statistic drift")
        values[key]=float(row["published_value"])
    if set(values)!=set(EXPECTED):
        raise ValueError("missing original primary source temporal record")

    cup_day=values["asexual_cup_count_observation_day"]
    sex_output_day=values["sexual_structure_count_observation_day"]
    sex_onset_mean=values["mean_first_sex_expression_day"]
    sample_n=int(values["sexual_selection_regression_n"])
    component_sign_opposed=(values["sexual_onset_multivariate_beta_sexual_structures"]<0<
                            values["sexual_onset_multivariate_beta_asexual_cups"])
    r=values["sexual_onset_versus_sex_structures_Pearson_r"]
    s=values["sexual_onset_total_selection_s"]
    # Standardized positive-affine x and relative fitness y leave the sign of
    # their ordinary least-squares slope identical to the sign of Pearson r
    # ONLY if the source data/coding and observations actually match.
    sign_consistent=(r*s>0)
    if not (cup_day==120 and sex_output_day==150
            and sex_onset_mean>cup_day and sample_n==31
            and component_sign_opposed and not sign_consistent):
        raise ValueError("original published temporal/sign readout no longer matches")
    return {
      "analysis":"sch_marchantia_2002_temporal_component_identification_v1",
      "source_article_doi":DOI,
      "source_dissertation_archive":"https://uknowledge.uky.edu/gradschool_diss/267/",
      "sex":"FEMALE",
      "shade_percent":55,
      "asexual_output_cups_observed_day":int(cup_day),
      "sexual_output_structures_observed_day":int(sex_output_day),
      "female_sex_onset_mean_day_original_table1":sex_onset_mean,
      "female_table1_sex_onset_sample_n":40,
      "female_selection_complete_case_n":sample_n,
      "onset_mean_minus_asexual_outcome_day":round(sex_onset_mean-cup_day,1),
      "individual_31_sample_onset_after_day120_fraction":"UNAVAILABLE",
      "source_at_least_one_of_40_table1_onset_after_day120":True,
      "sample_overlap_between_original_table1_40_and_regression_31":"NOT_FULLY_REPORTABLE",
      "same_trait_two_phenotypic_component_slopes_opposed":component_sign_opposed,
      "sexual_structures_component_direct_phenotypic_beta":-.915,
      "asexual_cups_component_direct_phenotypic_beta":+.496,
      "published_sex_onset_total_selection_s_Table6":s,
      "published_sex_onset_vs_sex_structures_Pearson_r_Table7":r,
      "reported_r_s_sign_compatible_if_identical_n31_and_positive_axes":sign_consistent,
      "univariate_covariance_identity_source_discrepancy":"UNRESOLVED_CHECK_SOURCE_ORIGINAL_PLANT_ROWS",
      "component_gradient_difference_published_direct_test":False,
      "causal_sexual_onset_to_day120_cup_output_estimated":False,
      "selection_on_heritable_trait_identified":False,
      "pure_function_optima_or_conflict_loss_L_identified":False,
      "source_r_s_check_not_proof_of_paper_error":True,
      "critical_limits":[
          "Table1_sex_onset_mean_from_40_is_not_31_complete_case_onset_distribution",
          "some_of_original_40_express_sex_after_day120_but_number_in_selected31_unknown",
          "day120_cup_outcome_cannot_be_causally_affected_by_later_sex_onset_for_any_post_day120_individual",
          "observational_date_of_future_sexual_expression_can_index_prior_vigor_or_allocation",
          "conditional_31_sex_expressing_selection_may_add_cohort_selection_bias",
          "univariate_r_and_s_cannot_have_opposite_sign_under_exact_same_sample_and_positive_affine_scales",
          "unexplained_source_reported_r_s_sign_discrepancy_cannot_be_fixed_by_guessing_minus_sign",
          "original_genotypic_sexual_onset_effect_not_detected",
          "two_phenotypic_component_betas_are_not_two_causal_pure_function_surfaces",
      ],
      "status":"SAME_TRAIT_OPPOSITION_PHENOTYPIC_ONLY_TIMING_AND_SOURCE_SIGN_PROVENANCE_NOT_RESOLVED",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    res=run(read_rows(a.source))
    data=json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data,encoding="utf-8")
    print(data)


if __name__=="__main__":
    main()
