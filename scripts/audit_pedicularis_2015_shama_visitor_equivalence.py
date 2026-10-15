"""Quantify what the source Shama-only pollinator non-detections DO NOT establish.

Read six published GLM Table 1 rows from Sun & Huang (2015),
DOI 10.1093/aobpla/plv019. All source coefficients are from a
binomial/logit model containing YEAR, TREATMENT and YEAR x TREATMENT.

This audit forms descriptive, normal-approximation Wald intervals
around printed SOURCE COEFFICIENTS, without fitting plant or plot data.
For an ordinary 5%-level two-one-sided equivalence test (TOST), the
90% model-based interval for a PARTICULAR source term must lie
strictly inside a predeclared symmetric [-Delta,+Delta] margin.
We report the smallest arithmetic margin which could cover the
printed 90% interval; this is NOT a retrospective equivalence claim.

Treatment main effect and year interaction are separate model terms;
their covariance is not reported. Do not interpret either a main
effect interval or a nonsignificant year interaction as a marginal
treatment effect across years. Pollinator and robber visits were
measured at SHAMA ONLY, unlike the six-population fruit experiment.

No source confidence interval here has been validated for the ten
plot-level clusters, repeated visits, between-year covariance or
prospectively justified biological equivalence margins.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/PEDICULARIS_2015_SHAMA_VISITOR_TABLE1_V1.csv"
DOI = "10.1093/aobpla/plv019"
TREATMENT = "BRACT_PUNCTURE_PLUS_DRAINAGE"
MODEL = "BINOMIAL_LOGIT"
EXPECTED = {
    ("pollinator_visits", "YEAR"): (.434,.451,1,.946,"0.331"),
    ("pollinator_visits", "TREATMENT"): (.012,.224,1,.003,"0.958"),
    ("pollinator_visits", "YEAR_X_TREATMENT"): (-.099,.451,1,.048,"0.823"),
    ("nectar_robber_visits", "YEAR"): (-1.226,.444,1,8.439,"0.004"),
    ("nectar_robber_visits", "TREATMENT"): (-.014,.225,1,.004,"0.951"),
    ("nectar_robber_visits", "YEAR_X_TREATMENT"): (.117,.444,1,.069,"0.792"),
}
VISITORS = ("pollinator_visits","nectar_robber_visits")
TERMS = ("YEAR","TREATMENT","YEAR_X_TREATMENT")


def read_source(path: Path = SOURCE) -> list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def normal_wald_interval(beta: float,se: float,level: float) -> tuple[float,float]:
    if (not math.isfinite(beta) or not math.isfinite(se) or se<=0
        or not 0<level<1):
        raise ValueError("invalid beta/se/interval confidence")
    z=NormalDist().inv_cdf((1+level)/2)
    return beta-z*se,beta+z*se


def minimum_symmetric_tost_margin(beta:float,se:float) -> float:
    """Infimum for 90% interval inside [-Delta, Delta] with alpha=.05.

    A true equivalence test requires a meaningful Delta registered
    independently of this exploratory source coefficient diagnostic,
    adequate sample/cluster model and intended marginal estimand.
    """
    a,b=normal_wald_interval(beta,se,.90)
    return max(abs(a),abs(b))


def build(rows: list[dict[str,str]]) -> dict:
    if len(rows)!=6:
        raise ValueError("six unique 2015 Shama Table 1 rows required")
    observed={}
    for row in rows:
        if (row.get("source_doi")!=DOI
            or row.get("source_table")!="Table_1"
            or row.get("study_cluster")!="Sun_Huang_2015_one_experiment"
            or row.get("site")!="Shama"
            or row.get("intervention")!=TREATMENT
            or row.get("original_model")!=MODEL):
            raise ValueError("source location, treatment or logit model drift")
        key=(row.get("visitor_class"),row.get("term"))
        if key not in EXPECTED or key in observed:
            raise ValueError("unregistered or duplicate 2015 visitor term")
        beta,se,df,chi,p=EXPECTED[key]
        try:
            got=(float(row["reported_beta"]),float(row["reported_se"]),
                 int(row["reported_df"]),float(row["reported_chi2"]),
                 row["reported_p"])
        except (ValueError,TypeError) as exc:
            raise ValueError("visitor Table 1 numeric field invalid") from exc
        if (not math.isclose(got[0],beta,rel_tol=0,abs_tol=1e-12)
            or not math.isclose(got[1],se,rel_tol=0,abs_tol=1e-12)
            or got[2]!=df
            or not math.isclose(got[3],chi,rel_tol=0,abs_tol=1e-12)
            or got[4]!=p):
            raise ValueError("published Shama Table 1 beta/SE/chi2/P drift")
        # Original paper rounds chi-square to three decimal places.
        # This p check is an arithmetic tolerance check, NOT a model refit.
        p_from_chi=math.erfc(math.sqrt(chi/2))
        if abs(p_from_chi-float(p))>.006:
            raise ValueError("original P incompatible with rounded chi2")
        w90=normal_wald_interval(beta,se,.90)
        w95=normal_wald_interval(beta,se,.95)
        observed[key]={
            "published_beta":beta,
            "published_se":se,
            "published_chi_square":chi,
            "source_p":p,
            "normal_approximation_model_based_90pct_interval":[*w90],
            "normal_approximation_model_based_95pct_interval":[*w95],
            "minimal_symmetric_equivalence_margin_infimum_on_model_scale":(
                minimum_symmetric_tost_margin(beta,se)
            ),
            "equivalence_claim_supported":False,
            "is_plot_cluster_robust_reanalysis":False,
        }
    if set(observed)!=set(EXPECTED):
        raise ValueError("2015 Shama Table 1 terms are incomplete")
    per_visitor={
        v:{term:observed[(v,term)] for term in TERMS}
        for v in VISITORS
    }
    return {
        "analysis":"pedicularis_2015_shama_visitor_equivalence_nonidentification_v1",
        "source_doi":DOI,
        "source_table":"Sun_Huang_2015_Table_1",
        "source_article":"https://academic.oup.com/aobpla/article/doi/10.1093/aobpla/plv019/200213",
        "source_model":"BINOMIAL_LOGIT_WITH_YEAR_BY_TREATMENT_INTERACTION",
        "source_study_count":1,
        "source_visitor_sites":["Shama"],
        "source_visitor_outcomes":list(VISITORS),
        "n_source_coefficients":len(observed),
        "normal_wald_intervals_are_diagnostics_only":True,
        "observed_source_table":per_visitor,
        "interpretation":{
            "pollinator_source_treatment_p":"0.958",
            "robber_source_treatment_p":"0.951",
            "main_effect_is_not_all_years_marginal_effect":True,
            "model_year_treatment_covariance_recovered":False,
            "equivalence_margin_was_prospectively_registered":False,
            "symmetric_margin_thresholds_are_not_posthoc_equivalence_tests":True,
            "visitor_selectivity_across_all_six_sites_identified":False,
            "preferential_functional_loading_established":False,
            "zero_or_negligible_pollinator_cost_established":False,
        },
        "claim_ceiling":[
            "treatment_is_bract_puncture_plus_drainage_not_pure_water",
            "site_is_Shama_only_for_visitor_data",
            "reported_model_contains_year_by_treatment_interaction",
            "source_main_term_not_pooled_all_years_response",
            "source_beta_CI_normal_approximation_not_source_fitted_plot_cluster_CI",
            "no_registered_biological_margin_for_equivalence",
            "no_cross_endpoint_visitor_damage_covariance",
            "source_coefficients_for_visit_and_predation_not_automatically_comparable",
            "antagonist_protection_detected_without_proven_pollinator_equivalence",
            "no_SCH_G_or_BITA_y_selectivity_or_L_SLK_architecture_promotion",
        ],
        "status":"SOURCE_VISITOR_NONDETECTION_RECOVERED_EQUIVALENCE_NOT_IDENTIFIED",
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    a=parser.parse_args()
    receipt=build(read_source(a.source))
    message=json.dumps(receipt,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(message,encoding="utf-8")
    else:
        print(message,end="")


if __name__=="__main__":
    main()
