"""Cross-check source-RECONSTRUCTED treatment gradient changes with primary tests.

Only three estimated changes clear the CONDITIONAL 137-pair normal-Wald bound
when treatment-gradient uncertainty is approximated from source arm SEs.
The source authors' ACTUAL fitted interaction test may have a different
error structure. One 2015 original paper explicitly demonstrates this:
its early-growth treatment-by-trait p=.04, vs p<=.0105 after 137-test
adjustment from the *separate* marginal beta SEs (arithmetically stronger).

The discrepancy is a failed compatibility assumption for promotion. Do not
call the reconstructed p a universal conservative p-value. Distinguish
those numeric screens from the directly published source interactions.

Source primary papers:
Beans & Roach 2015 doi:10.3732/ajb.1400355
Stinchcombe et al. 2002 doi:10.1086/342069 (explicit environmental bias)
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
META=ROOT/"data/SCH_2020_FUNCTIONAL_META_EXPERIMENTAL_READOUT_V1.json"
QA=ROOT/"data/SCH_2020_FUNCTIONAL_META_PRIMARY_SOURCE_INTERACTION_QA_V1.csv"
ALPHA=0.05


def read(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def run(meta:dict,source_primary:list[dict[str,str]])->dict:
    rows=meta["source_reconstructed_familywise_contrast_certificate_details"]
    if len(rows)!=3 or len(source_primary)!=3:
        raise ValueError("exactly three compiled estimate contrasts requiring source QA")
    tests=meta["eligible_matched_pair_total"]
    if tests!=137:
        raise ValueError("published original source family denominator unexpectedly changed")
    expected={
      ("13","Early growth rate"):(
        "10.3732/ajb.1400355","0.04",
        "SOURCE_DIRECT_TEST_NOMINAL_ONLY"),
      ("13","Number of internodes"):(
        "10.3732/ajb.1400355","<0.0001",
        "AUTHOR_DIRECT_TEST_SURVIVES_137_BONFERRONI"),
      ("37","Total leaf area"):(
        "10.1086/342069","NOT_VERIFIED",
        "UNRESOLVED_DIRECT_TEST_AND_PHENOTYPIC_BIAS_RISK"),
    }
    keys=[(str(row["paper_id"]),row["trait"]) for row in rows]
    if set(keys)!=set(expected) or len(set(keys))!=3:
        raise ValueError("reconstructed source study/trait identification changed")
    checks=[]
    for original in source_primary:
        key=(original["original_paper_id"],original["trait"])
        if key not in expected:
            raise ValueError("unexpected source primary interaction/trait")
        doi,p,assessment=expected[key]
        if ((original["primary_article_doi"],original["author_fitted_treatment_trait_p"],
             original["independent_primary_source_assessment"])!=(doi,p,assessment)):
            raise ValueError("author direct primary test p-value metadata drift")
        rebuilt=next(x for x in rows if (str(x["paper_id"]),x["trait"])==key)
        source_nominal=None
        source_bonf=None
        if p=="NOT_VERIFIED":
            direct_p_max=None
        elif p.startswith("<"):
            direct_p_max=float(p[1:])
            source_nominal=True
            source_bonf=direct_p_max*tests<=ALPHA
        else:
            direct_p_max=float(p)
            source_nominal=direct_p_max<ALPHA
            source_bonf=direct_p_max*tests<=ALPHA
        if source_bonf and not rebuilt["stored_source_decimal_rounding_robust"]:
            raise ValueError("source original direct familywise test differs from stored rounding expectation")
        mismatched_primary_p=(
            direct_p_max is not None and p[0]!="<"
            and rebuilt["adjusted_137_family_normal_p_upper"]
                <direct_p_max * tests * 0.5
        )
        checks.append({
            "paper_id":key[0],
            "original_paper_doi":doi,
            "original_authors":original["compiled_authors"],
            "original_trait":key[1],
            "original_fitted_interaction_p":p,
            "original_source_nominal_interaction_detected":source_nominal,
            "original_source_p_survives_137_Bonferroni":source_bonf,
            "reconstructed_137_normal_Wald_adjusted_p_upper":
                rebuilt["adjusted_137_family_normal_p_upper"],
            "reconstructed_stored_decimal_precision_robust":
                rebuilt["stored_source_decimal_rounding_robust"],
            "source_reconstructed_vs_original_direct_test_inconsistent":
                mismatched_primary_p,
            "source_fitted_interaction_primary_test_required_for_promotion":True,
            "assessment":assessment,
        })
    n_direct=sum(x["original_source_p_survives_137_Bonferroni"] is True for x in checks)
    if n_direct!=1:
        raise ValueError("original direct author-fitted source test certificates changed")
    return {
        "analysis":"sch_functional_trait_source_interaction_contrast_adjudication_v1",
        "source_meta_doi":"10.5061/dryad.sn02v6x0q",
        "n_source_compiled_selected_source_p_values":3,
        "n_conditional_reconstructed_137_fwer_candidates":3,
        "n_robust_to_stored_workbook_decimal_format":2,
        "n_direct_original_fitted_interactions_with_verified_test":2,
        "n_direct_original_fitted_interactions_p_137_fwer_supported":n_direct,
        "n_source_direct_original_interaction_unverified":1,
        "n_primary_p_conflicts_with_reconstructed_se_inference":sum(
            x["source_reconstructed_vs_original_direct_test_inconsistent"]
            for x in checks),
        "original_primary_test_checks":sorted(checks,key=lambda x:(x["paper_id"],x["original_trait"])),
        "registered_137_comparison_alpha":ALPHA,
        "individual_source_direct_Bonferroni_threshold":ALPHA/tests,
        "interpretive_ceiling":[
            "reconstructed_beta_se_difference_is_not_author_original_fitted_interaction_test",
            "two_cell_normal_wald_se_bound_only_when_marginal_SEs_are_comparable_estimands",
            "source_2015_early_growth_original_p_0_04_contradicts_reconstructed_p_strength",
            "source_2002_study_demonstrates_possible_environmental_bias_not_specific_leaf_area_bias",
            "source_external_paper_bias_not_demonstrated_for_any_specific_leaf_pair",
            "one_verified_direct_interaction_not_species_wide_generalization",
            "no_137_source_primary_interaction_p_values_recovered_for_all_studies",
            "no_verified_experimental_pure_function_optima_or_SCH_L",
        ],
        "status":"ONE_PRIMARY_FITTED_DIRECT_INTERACTION_BONFERRONI_SUPPORTED_OTHERS_PENDING",
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--meta",type=Path,default=META)
    p.add_argument("--source-tests",type=Path,default=QA)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    receipt=run(json.loads(a.meta.read_text(encoding="utf-8")),
                read(a.source_tests))
    data=json.dumps(receipt,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data,encoding="utf-8")
    print("BEGIN_SCH_2020_FUNCTIONAL_META_SOURCE_INTERACTION_QA")
    print(data)
    print("END_SCH_2020_FUNCTIONAL_META_SOURCE_INTERACTION_QA")


if __name__=="__main__":
    main()
