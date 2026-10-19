"""Secondary, explicitly exploratory cross-programme pollination selection response.

Source: frozen V27 outcomes from three independent published programmes,
Dactylorhiza (2010), Primula (2017), Trillium (2022; 2020/2021 years).
This is NOT the frozen H2M1 heldout class-comparison test. Every source
eligible, same-year open-versus-supplemented axis is tested (14 edges),
whether its outcome was positive, negative or null. No contexts may be
selected for this family using observed coefficient signs.

Only within-axis, within-year total-selection coefficients are
subtracted. In the absence of published covariance, SE(bo-bh) <= so+sh
by Cauchy-Schwarz; conditional on comparability and normal-Wald
validity, use 14-edge Bonferroni. Different programmes' effect units
must NEVER be averaged or inverse-variance pooled.

Printed-value intervals and rounding-robust sign certificates are
reported separately. Primula's OP group includes both style morphs,
while only long-styled plants received supplementary pollination.
Trillium Poisson-model coefficient units differ from linear-gradient
units. Thus these are treatment-associated selection changes, not
causal manipulation of the floral phenotype and not SCH L.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv"
READOUT = ROOT / "data/SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json"
ALPHA = .05

PROGRAMMES = {
    "Dactylorhiza_lapponica_000649_selection_program": {
        "doi":"10.1111/j.1469-8137.2010.03296.x",
        "open":"OPEN_POLLINATED_CONTROL",
        "supp":"SUPPLEMENTAL_HAND_POLLINATION",
        "n_edges":5,
    },
    "Primula_alpicola_000651_selection_program": {
        "doi":"10.1038/s41598-017-13340-0",
        "open":"OPEN_POLLINATED",
        "supp":"SUPPLEMENTAL_HAND_POLLINATION",
        "n_edges":4,
    },
    "Trillium_discolor_000661_selection_program": {
        "doi":"10.1002/ajb2.16101",
        "open":"OPEN_POLLINATED",
        "supp":"POLLEN_SUPPLEMENTED",
        "n_edges":5,
    },
}
# The frozen digit string abbreviates D. lapponica 0.30 as "0.3";
# original New Phytologist Table 3 prints 0.30 (verified at source).
DIGIT_PRECISION_OVERRIDES = {
    ("Dactylorhiza_lapponica_000649_selection_program",
     "Dactylorhiza_000649_spur_length","OPEN_POLLINATED_CONTROL","beta"):.01,
}
TRILLIUM_DISPLAY_2020_NOTE = (
    "2020_source_Table_1_display_height_printed_Delta_-2.83_"
    "does_not_equal_open_minus_supplemented_2.96_minus_minus_0.13_=_3.09;"
    "do_not_represent_reconstructed_delta_as_source_reported"
)


def read_csv(path:Path=SOURCE)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream))


def _rounding_step(row:dict[str,str],field:str)->float:
    override=DIGIT_PRECISION_OVERRIDES.get(
        (row["programme_id"],row["canonical_axis"],row["context"],field)
    )
    if override is not None:
        return override
    token=row[field]
    if not token or "e" in token.lower():
        raise ValueError("source number must be a fixed decimal with reported precision")
    digits=len(token.partition(".")[2]) if "." in token else 0
    return 10.**(-digits)


def _number(row:dict[str,str],key:str)->float:
    if not row[key]:
        raise ValueError("numeric source row missing "+key)
    value=float(row[key])
    if not math.isfinite(value):
        raise ValueError("nonfinite source "+key)
    return value


def build(rows:list[dict[str,str]],holdout:dict,alpha:float=ALPHA)->dict:
    if not type(alpha) in (int,float) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be strictly inside (0,1)")
    if len(rows)!=31:
        raise ValueError("expected frozen 31-row original V27 source")
    valid=[r for r in rows if r.get("axis_eligible")=="YES"]
    excluded=[r for r in rows if r.get("axis_eligible")=="NO"]
    if len(valid)!=28 or len(excluded)!=3:
        raise ValueError("unexpected V27 eligible/excluded denominator")
    if not all(r.get("programme_id") in PROGRAMMES for r in rows):
        raise ValueError("unregistered primary programme")
    if not all(r["doi"]==PROGRAMMES[r["programme_id"]]["doi"] for r in rows):
        raise ValueError("source DOI drift")
    if not (holdout.get("n_programmes_adjudicated")==3
            and holdout.get("n_eligible_axes")==12
            and holdout.get("n_supported_reversal_axes")==2):
        raise ValueError("primary holdout readout would be changed")
    if not all(
        r.get("axis_ineligibility_reason") in (
            "NONFLORAL_PLANT_CONDITION_COVARIATE",
            "CATEGORICAL_TRAIT_NO_LINEAR_BETA_SE_PAIR"
        )
        for r in excluded
    ):
        raise ValueError("newly excluded source axes need review")
    if any(r.get("metric_family") not in (
        "LINEAR_TOTAL_SELECTION","POISSON_LINEAR_TOTAL_SELECTION"
    ) for r in valid):
        raise ValueError("noncommensurate or unqualified estimand")

    groups={}
    for r in valid:
        k=(r["programme_id"],r["year"],r["canonical_axis"])
        per=groups.setdefault(k,{})
        context=r["context"]
        if context in per:
            raise ValueError("duplicate same-year context and trait")
        if context not in (
            PROGRAMMES[k[0]]["open"],PROGRAMMES[k[0]]["supp"]
        ):
            raise ValueError("unexpected pollination treatment")
        per[context]=r

    family_size=sum(p["n_edges"] for p in PROGRAMMES.values())
    if family_size!=14 or len(groups)!=family_size:
        raise ValueError("missing or extra 14 same-year source edges")
    by_programme={k:0 for k in PROGRAMMES}
    for k,per in groups.items():
        p=PROGRAMMES[k[0]]
        if set(per)!={p["open"],p["supp"]}:
            raise ValueError("incomplete registered open/hand matched pair")
        if per[p["open"]]["metric_family"] != per[p["supp"]]["metric_family"]:
            raise ValueError("within-pair source estimand family differs")
        by_programme[k[0]]+=1
    if any(by_programme[p]!=PROGRAMMES[p]["n_edges"] for p in PROGRAMMES):
        raise ValueError("programme source-axis counts drifted")

    z=NormalDist().inv_cdf(1-alpha/(2*family_size))
    out=[]
    for (programme,year,axis),per in sorted(groups.items()):
        p=PROGRAMMES[programme]
        op,hp=per[p["open"]],per[p["supp"]]
        bo,bh=_number(op,"beta"),_number(hp,"beta")
        so,sh=_number(op,"se"),_number(hp,"se")
        if min(so,sh)<=0:
            raise ValueError("invalid uncertainty source")
        delta=bo-bh
        se_max=so+sh
        p_upper=math.erfc(abs(delta)/se_max/math.sqrt(2))
        lo,hi=delta-z*se_max,delta+z*se_max
        passed=lo>0 or hi<0
        # Allow every printed source value to move inside its last printed
        # rounding bin; source DOI/table must determine any overrides.
        delta_round_half=(
            _rounding_step(op,"beta")+_rounding_step(hp,"beta")
        )/2
        se_round_upper=se_max+(
            _rounding_step(op,"se")+_rounding_step(hp,"se")
        )/2
        abs_delta_min=max(0.,abs(delta)-delta_round_half)
        robust=abs_delta_min>z*se_round_upper
        out.append({
            "programme":programme,
            "year":year,
            "canonical_axis":axis,
            "trait":op["trait_label"],
            "metric_family":op["metric_family"],
            "source_doi":p["doi"],
            "open_context":p["open"],
            "supplemented_context":p["supp"],
            "beta_open":bo,"se_open":so,
            "beta_supplemented":bh,"se_supplemented":sh,
            "delta_open_minus_supplemented":round(delta,9),
            "covariance_worst_case_se_upper":round(se_max,9),
            "conditional_unadjusted_p_upper":round(p_upper,12),
            "bonferroni_14_adjusted_p_upper":round(min(1.,family_size*p_upper),12),
            "familywise_95pct_normal_wald_outer_interval":[round(lo,7),round(hi,7)],
            "certified_change_at_alpha_05_using_printed_values":passed,
            "certified_with_source_decimal_rounding_sensitivity":robust,
            "rounding_min_absolute_delta":round(abs_delta_min,7),
            "rounding_max_se_upper":round(se_round_upper,7),
            "within_programme_same_year_pair":True,
            "not_functional_optimum_or_causal_do_z":True,
        })
    support=[x for x in out if x[
        "certified_change_at_alpha_05_using_printed_values"]]
    robust=[x for x in out if x[
        "certified_with_source_decimal_rounding_sensitivity"]]
    return {
        "analysis":"sch_h2_three_programme_bonferroni_pollination_gradient_edges_v1",
        "source_data":"data/SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv",
        "n_source_rows":len(rows),
        "n_original_independent_programmes":len(PROGRAMMES),
        "n_registered_same_year_matched_trait_edges":family_size,
        "n_printed_value_familywise_supported_changes":len(support),
        "n_rounding_robust_familywise_supported_changes":len(robust),
        "n_programmes_with_printed_value_supported_change":len({
            x["programme"] for x in support
        }),
        "n_programmes_with_rounding_robust_change":len({
            x["programme"] for x in robust
        }),
        "supported_axis_years":[
            (x["programme"],x["canonical_axis"],x["year"]) for x in support
        ],
        "rounding_robust_axis_years":[
            (x["programme"],x["canonical_axis"],x["year"]) for x in robust
        ],
        "alpha":alpha,
        "confidence_family":f"ALL_{family_size}_FROZEN_V27_WITHIN_YEAR_POLLINATION_EDGES",
        "normal_bonferroni_critical_value":z,
        "original_holdout_H2M1_predictor_classes_and_q_unchanged":True,
        "one_year_pair_is_not_an_independent_biological_programme":True,
        "all_pairs":out,
        "trillium_2020_display_height_printed_source_delta_warning":(
            TRILLIUM_DISPLAY_2020_NOTE
        ),
        "claim_ceiling":[
            "secondary_exploratory_analysis_not_original_H2M1_primary_test",
            "normal_asymptotic_comparability_and_printed_SE_validity_required",
            "unknown_cross_cell_covariance_bounded_not_assumed_zero",
            "14_edge_family_determined_by_all_eligible_same_year_source_pairs",
            "trillium_2020_petal_SE_1_2_rounded_at_one_decimal_does_not_pass_rounding_worst_case",
            "primula_original_open_treatment_includes_two_style_morphs_hand_only_long_style",
            "trillium_poisson_link_coefficients_not_pooled_with_linear_gradient_coefficients",
            "source_primula_2019_erratum_changed_figure1_and_table3_label_not_table2",
            "no_phenotype_randomization_and_no_pure_function_optima",
            "gradient_magnitude_difference_is_not_supported_sign_reversal",
            "no_nonrandom_study_prevalence_estimate_and_no_SCH_L_or_SLK_payoff"
        ],
        "status":"SECONDARY_CROSS_PROGRAMME_SELECTION_MAGNITUDE_NOT_PREVALENCE"
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--primary-holdout",type=Path,default=READOUT)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=build(read_csv(args.source),
                 json.loads(args.primary_holdout.read_text(encoding="utf-8")))
    serialized=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized,encoding="utf-8")
    else:
        print(serialized,end="")


if __name__=="__main__":
    main()
