"""Source-locked 2015 *P. rex* experimental endpoint-pattern audit.

Input is Table 2 GLM coefficient/SE/chi-square/df/p transcription from
Sun & Huang 2015 (doi:10.1093/aobpla/plv019). It is one six-site field
experiment. The intervention simultaneously punctured bracts and drained
water. No plant-level data, raw site-level fitness estimates, covariances,
trait-randomization, or independently manipulated seed-predator access are
available here.

The supported ECOLOGICAL PATTERN is a significant site-by-treatment test
for seed predation but not for initial or final seed set, alongside a
significant pooled effect on final seed set. Crucially, differing
significance across endpoints is NOT a statistical test of differences
between endpoint-specific interactions, and a nonsignificant final-seed
interaction is not a demonstration of geographical equality.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/PEDICULARIS_2015_CROSS_ENDPOINT_TABLE2_V1.csv"
DOI = "10.1093/aobpla/plv019"
INTERVENTION = "BRACT_PUNCTURE_PLUS_WATER_DRAINAGE"
EXPECTED = {
    ("initial_seed_set", "SITE"): (-.066,.069,5,56.522,"<0.0001"),
    ("initial_seed_set", "TREATMENT"): (.001,.006,1,.014,"0.906"),
    ("initial_seed_set", "SITE_X_TREATMENT"): (-.010,.069,5,1.032,"0.960"),
    ("final_seed_set", "SITE"): (-.015,.068,5,18.157,"0.0028"),
    ("final_seed_set", "TREATMENT"): (.025,.006,1,16.710,"<0.0001"),
    ("final_seed_set", "SITE_X_TREATMENT"): (.013,.068,5,4.913,"0.4265"),
    ("seed_predation", "SITE"): (-.081,.076,5,46.755,"<0.0001"),
    ("seed_predation", "TREATMENT"): (-.072,.007,1,92.808,"<0.0001"),
    ("seed_predation", "SITE_X_TREATMENT"): (-.053,.076,5,36.782,"<0.0001"),
}
ENDPOINTS = ("initial_seed_set", "final_seed_set", "seed_predation")
TERMS = ("SITE", "TREATMENT", "SITE_X_TREATMENT")


def read_source(path: Path = SOURCE) -> list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as handle:
        return list(csv.DictReader(handle))


def chi_square_survival_odd_df(chi2: float, df: int) -> float:
    """Exact upper gamma tail for positive odd df, stdlib only.

    Q(1/2,z)=erfc(sqrt(z));
    Q(a+1,z)=Q(a,z)+z**a * exp(-z) / Gamma(a+1).
    Independent arithmetic check of published rounded chi-square and p,
    not a refit to missing plant/capsule data.
    """
    if type(df) is not int or df < 1 or df % 2 != 1:
        raise ValueError("expected odd positive chi-square source df")
    if not math.isfinite(chi2) or chi2 < 0:
        raise ValueError("invalid chi-square")
    if chi2 == 0:
        return 1.
    z = chi2/2
    result = math.erfc(math.sqrt(z))
    a = .5
    for _ in range((df-1)//2):
        result += math.exp(a*math.log(z)-z-math.lgamma(a+1))
        a += 1
    return max(0.,min(1.,result))


def build(rows: list[dict[str,str]]) -> dict:
    if len(rows) != len(EXPECTED):
        raise ValueError("2015 Table 2 must have exactly nine nonduplicate tests")
    observed={}
    for row in rows:
        if (row.get("source_doi") != DOI
            or row.get("source_table") != "Table_2"
            or row.get("study_cluster") != "Sun_Huang_2015_one_experiment"
            or row.get("biological_intervention") != INTERVENTION):
            raise ValueError("2015 Table 2 source/intervention identity drift")
        key=(row["endpoint"],row["term"])
        if key not in EXPECTED or key in observed:
            raise ValueError("missing or duplicated source endpoint/term")
        beta,se,df,chi,p = EXPECTED[key]
        try:
            actual=(
                float(row["reported_beta"]),float(row["reported_se"]),
                int(row["reported_df"]),float(row["reported_chi2"]),
                row["reported_p"],
            )
        except (TypeError,ValueError) as exc:
            raise ValueError("published numerical source field is invalid") from exc
        if (not all(math.isfinite(x) for x in (actual[0],actual[1],actual[3]))
            or actual[1]<=0 or actual[2]!=df or actual[4]!=p
            or not math.isclose(actual[0],beta,rel_tol=0,abs_tol=1e-10)
            or not math.isclose(actual[1],se,rel_tol=0,abs_tol=1e-10)
            or not math.isclose(actual[3],chi,rel_tol=0,abs_tol=1e-10)):
            raise ValueError("published Table 2 coefficient/df/chi-square/P drifted")
        recalculated=chi_square_survival_odd_df(chi,df)
        if p.startswith("<"):
            if not recalculated < float(p[1:]):
                raise ValueError("source printed p bound contradicts chi-square and df")
        elif abs(recalculated-float(p))>5.1e-4:
            raise ValueError("printed rounded p inconsistent with reported test")
        observed[key]={
            "printed_p":p,
            "chi_square":chi,
            "df":df,
            "p_from_rounded_chi_square":round(recalculated,8),
            "reported_beta":beta,
            "reported_se":se,
            "published_table_effect_has_p_below_0_05":recalculated<.05,
        }
    if set(observed)!=set(EXPECTED):
        raise ValueError("2015 Table 2 required nine tests are incomplete")
    by_endpoint={}
    for endpoint in ENDPOINTS:
        by_endpoint[endpoint]={term:observed[(endpoint,term)] for term in TERMS}
    return {
        "analysis":"pedicularis_2015_real_experimental_cross_endpoint_signature_v1",
        "source_doi":DOI,
        "primary_source":"Sun_Huang_2015_AoB_PLANTS_Table_2",
        "source_article_url":"https://academic.oup.com/aobpla/article/doi/10.1093/aobpla/plv019/200213",
        "source_data_kind":"NINE_PUBLISHED_AGGREGATE_GLM_TESTS",
        "n_independent_primary_experiments":1,
        "n_original_populations":6,
        "n_endpoints":3,
        "n_source_table_tests":9,
        "physical_intervention":INTERVENTION,
        "source_plant_capsule_raw_data_recovered":False,
        "published_site_and_treatment_tests":by_endpoint,
        "original_results_at_nominal_alpha_0_05":{
            "treatment_effect_supported_endpoints":[
                e for e in ENDPOINTS if observed[(e,"TREATMENT")][
                    "published_table_effect_has_p_below_0_05"]],
            "site_by_treatment_supported_endpoints":[
                e for e in ENDPOINTS if observed[(e,"SITE_X_TREATMENT")][
                    "published_table_effect_has_p_below_0_05"]],
            "site_main_effect_supported_endpoints":[
                e for e in ENDPOINTS if observed[(e,"SITE")][
                    "published_table_effect_has_p_below_0_05"]],
        },
        "ecological_claim":(
            "defence_package_effect_on_seed_predation_varied_among_sites_"
            "while_final_seed_set_showed_a_pooled_treatment_effect_"
            "but_no_detected_site_by_treatment_interaction"
        ),
        "causal_interpretation_limits":[
            "reported_effect_is_puncture_plus_drainage_not_water_only",
            "different_p_values_are_not_a_formal_between_endpoint_interaction_test",
            "absence_of_significant_final_seed_interaction_is_not_equivalence",
            "final_seed_response_may_have_different_power_error_and_link_scale",
            "same_six_sites_are_not_six_independent_experiments",
            "plant_and_capsule_raw_data_unavailable_no_refitted_cluster_robust_CI",
            "does_not_estimate_phenotype_dependent_predator_selection",
            "does_not_estimate_water_fixed_selective_predator_G",
            "does_not_identify_P_rex_optimum_shift_or_SCH_L",
        ],
        "status":"REAL_PUBLISHED_ENDPOINT_PATTERN_RECOVERED_NO_RAW_CAUSAL_COMPONENTS",
    }


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=build(read_source(args.source))
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()
