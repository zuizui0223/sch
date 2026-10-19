"""Four-programme ecological selection spectrum, including full Gymnadenia factorial.

Secondary exploration from ALREADY-FROZEN primary numerical tables only.
Extend the complete 14 within-year open-versus-supplemented V27 edges by
ALL ten analogous Gymnadenia Table A2 pollination edges (five trait axes
in each of TWO fixed herbivory states). Never cherry-pick favorable traits.

Classify THREE different objects:
(1) point-estimate selection sign switch, NOT inferential proof;
(2) both cell slopes individually nominal-95%-supported and opposite;
(3) change in same-trait slope supported at familywise alpha=.05 by an
    arbitrary-covariance SE upper bound and normal Bonferroni over all
    TWENTY-FOUR edges.

Source rounding is assessed separately, and original 14-edge results
are not overwritten. Phenotypic z itself was not experimentally randomized.
Four independent experiments are NOT 24 independent biological systems.
Cross-paper linear and conditional Poisson coefficients are NEVER pooled.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import NormalDist

from scripts.audit_sch_h2_cross_programme_pollination_edges import (
    SOURCE as V27_SOURCE,
    READOUT as V27_READOUT,
    read_csv as read_v27,
    build as build_v27,
)

ROOT = Path(__file__).resolve().parents[1]
GYM_SOURCE = ROOT / "data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
GYM_PROGRAMME = "Gymnadenia_conopsea_2015_pollination_herbivory_factorial"
GYM_DOI = "10.1890/14-0119.1"
GYM_TRAITS = frozenset((
    "plant_height", "number_of_flowers", "corolla_size",
    "spur_length", "flowering_start",
))
GYM_CELLS = {
    "C+H": ("OPEN_POLLINATED", "NATURAL_HERBIVORY", 146),
    "C+E": ("OPEN_POLLINATED", "HERBIVORES_EXCLUDED", 112),
    "HP+H": ("HAND_POLLINATED", "NATURAL_HERBIVORY", 117),
    "HP+E": ("HAND_POLLINATED", "HERBIVORES_EXCLUDED", 110),
}
GYM_CONTRASTS = (
    ("NATURAL_HERBIVORY", "C+H", "HP+H"),
    ("HERBIVORES_EXCLUDED", "C+E", "HP+E"),
)
N_TOTAL_EDGES = 24
N_UNIQUE_PROGRAMMES = 4


def read_gym(path: Path = GYM_SOURCE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _source_number(s: str, field: str) -> float:
    if not s or "e" in s.lower():
        raise ValueError(f"{field} must be a source-printed fixed decimal")
    value = float(s)
    if not math.isfinite(value) or (field == "se" and value <= 0):
        raise ValueError(f"invalid source {field}")
    return value


def _step(token: str) -> float:
    if not token or "e" in token.lower():
        raise ValueError("invalid source decimal-precision field")
    return 10. ** -len(token.partition(".")[2])


def _gym_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    if len(rows) != len(GYM_TRAITS) * len(GYM_CELLS):
        raise ValueError("complete original 5 x 4 Gymnadenia table required")
    lookup = {}
    for row in rows:
        trait, treatment = row.get("trait"), row.get("treatment")
        if trait not in GYM_TRAITS or treatment not in GYM_CELLS:
            raise ValueError("unregistered Gymnadenia trait/treatment")
        key = (trait, treatment)
        if key in lookup:
            raise ValueError("duplicate original Gymnadenia treatment cell")
        state, herb, n = GYM_CELLS[treatment]
        if (
            row.get("pollination_state") != state
            or row.get("herbivory_state") != herb
            or row.get("treatment_n") != str(n)
            or row.get("source_table") != "Table_A2"
            or row.get("significance") not in (
                "NS", "P_EQ_0.057", "P_LT_0.05", "P_LT_0.01",
                "P_LT_0.001",
            )
        ):
            raise ValueError("original Gymnadenia Table A2 source identity drift")
        _source_number(row["beta"], "beta")
        _source_number(row["se"], "se")
        lookup[key] = row
    if set(lookup) != {
        (t, c) for t in GYM_TRAITS for c in GYM_CELLS
    }:
        raise ValueError("missing Gymnadenia Table A2 treatment cell")
    return lookup


def _annotate(
    *, programme: str, axis: str, context: str,
    metric_family: str, doi: str, open_beta: float, open_se: float,
    supplemented_beta: float, supplemented_se: float,
    rounding_delta_min: float, rounding_se_upper: float,
    confidence_z: float, family_n: int,
    from_original_holdout: bool,
) -> dict:
    delta = open_beta - supplemented_beta
    worst_se = open_se + supplemented_se
    p_upper = math.erfc(abs(delta) / (math.sqrt(2) * worst_se))
    half = confidence_z * worst_se
    robust = rounding_delta_min > confidence_z * rounding_se_upper
    opposite = open_beta * supplemented_beta < 0
    both_cell_supported = (
        opposite and abs(open_beta/open_se) > 1.96
        and abs(supplemented_beta/supplemented_se) > 1.96
    )
    return {
        "programme_id":programme,
        "canonical_axis":axis,
        "fixed_context":context,
        "metric_family":metric_family,
        "source_doi":doi,
        "from_V27_frozen_holdout":from_original_holdout,
        "beta_open":round(open_beta,9),
        "se_open":round(open_se,9),
        "beta_supplemented":round(supplemented_beta,9),
        "se_supplemented":round(supplemented_se,9),
        "delta_open_minus_supplemented":round(delta,9),
        "covariance_worst_se_upper":round(worst_se,9),
        "normal_two_sided_p_upper_conditional":round(p_upper,12),
        "bonferroni_adjusted_p_upper":round(min(1.,family_n*p_upper),12),
        "normal_familywise_95pct_outer_interval":[
            round(delta-half,8), round(delta+half,8),
        ],
        "point_selection_sign_switch":opposite,
        "opposite_individually_supported_source_cell_directions":both_cell_supported,
        "contrast_supported_at_24_edge_nominal_familywise_05":abs(delta)>half,
        "rounding_minimum_abs_delta":round(rounding_delta_min,9),
        "rounding_maximum_worst_case_se":round(rounding_se_upper,9),
        "contrast_supported_after_decimal_rounding":robust,
        "source_trait_not_randomized":True,
    }


def build(
    v27_rows: list[dict[str,str]],
    holdout: dict,
    gym_rows: list[dict[str,str]],
    *,
    alpha: float = .05,
) -> dict:
    if type(alpha) not in (int,float) or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("invalid alpha")
    base = build_v27(v27_rows,holdout,alpha=alpha)
    if (
        base["n_original_independent_programmes"] != 3
        or base["n_registered_same_year_matched_trait_edges"] != 14
        or len(base["all_pairs"]) != 14
    ):
        raise ValueError("unaltered three-programme source family required")
    gym = _gym_index(gym_rows)
    z = NormalDist().inv_cdf(1-alpha/(2*N_TOTAL_EDGES))
    result=[]
    for pair in base["all_pairs"]:
        result.append(_annotate(
            programme=pair["programme"],
            axis=pair["canonical_axis"],
            context=pair["year"],
            metric_family=pair["metric_family"],
            doi=pair["source_doi"],
            open_beta=pair["beta_open"],
            open_se=pair["se_open"],
            supplemented_beta=pair["beta_supplemented"],
            supplemented_se=pair["se_supplemented"],
            rounding_delta_min=pair["rounding_min_absolute_delta"],
            rounding_se_upper=pair["rounding_max_se_upper"],
            confidence_z=z,
            family_n=N_TOTAL_EDGES,
            from_original_holdout=True,
        ))
    for trait in sorted(GYM_TRAITS):
        for background,open_code,supp_code in GYM_CONTRASTS:
            o=gym[(trait,open_code)]
            h=gym[(trait,supp_code)]
            bo,so=(_source_number(o[c],c) for c in ("beta","se"))
            bh,sh=(_source_number(h[c],c) for c in ("beta","se"))
            delta_half=(_step(o["beta"])+_step(h["beta"]))/2
            max_worst_se=so+sh+(_step(o["se"])+_step(h["se"]))/2
            result.append(_annotate(
                programme=GYM_PROGRAMME,
                axis=f"Gymnadenia_000030_{trait}",
                context=background,
                metric_family="STANDARDIZED_LINEAR_TOTAL_SELECTION",
                doi=GYM_DOI,
                open_beta=bo, open_se=so,
                supplemented_beta=bh, supplemented_se=sh,
                rounding_delta_min=max(0.,abs(bo-bh)-delta_half),
                rounding_se_upper=max_worst_se,
                confidence_z=z,
                family_n=N_TOTAL_EDGES,
                from_original_holdout=False,
            ))
    if len(result)!=N_TOTAL_EDGES or len({
        x["programme_id"] for x in result
    })!=N_UNIQUE_PROGRAMMES:
        raise AssertionError("incorrect independent-programme/edge denominator")
    summary={}
    for programme in sorted({x["programme_id"] for x in result}):
        sub=[x for x in result if x["programme_id"]==programme]
        summary[programme]={
            "n_contrasts":len(sub),
            "point_sign_switches":sum(x["point_selection_sign_switch"] for x in sub),
            "nominal_both_cell_signs_supported":sum(
                x["opposite_individually_supported_source_cell_directions"] for x in sub
            ),
            "familywise_printed_changes":sum(
                x["contrast_supported_at_24_edge_nominal_familywise_05"] for x in sub
            ),
            "familywise_rounding_robust_changes":sum(
                x["contrast_supported_after_decimal_rounding"] for x in sub
            ),
        }
    totals={
        "n_source_frozen_v27_pairs":14,
        "n_source_gymnadenia_pollen_by_herbivory_pairs":10,
        "n_independent_programmes":N_UNIQUE_PROGRAMMES,
        "n_within_axis_fixed_context_pollination_edges":N_TOTAL_EDGES,
        "n_point_sign_switches":sum(x["point_selection_sign_switch"] for x in result),
        "n_opposite_individually_supported_directions":sum(
            x["opposite_individually_supported_source_cell_directions"] for x in result
        ),
        "n_familywise_printed_difference_certificates":sum(
            x["contrast_supported_at_24_edge_nominal_familywise_05"] for x in result
        ),
        "n_familywise_rounding_robust_certificates":sum(
            x["contrast_supported_after_decimal_rounding"] for x in result
        ),
    }
    return {
        "analysis":"sch_four_programme_24_pollination_response_spectrum_v1",
        "status":"REAL_PUBLISHED_SELECTION_RESPONSE_BOUNDED_NOT_GENERAL_PREVALENCE",
        "alpha":alpha,
        "normal_two_sided_bonferroni_critical_z":z,
        "family_structure":"ALL_14_FROZEN_V27_PLUS_ALL_10_GYMNADENIA_WITHIN_HERBIVORY_POLLINATION_EDGES",
        "counting_unit":"WITHIN_STUDY_SAME_TRAIT_SAME_YEAR_FIXED_HERBIVORY_POLLINATION_PAIR",
        "independent_biological_unit":"FOUR_PUBLISHED_PROGRAMMES_NOT_24_EDGES",
        "totals":totals,
        "programme_summaries":summary,
        "contrasts":result,
        "original_V27_readout_and_frozen_H2M1_class_comparison_unchanged":True,
        "legacy_14_edge_results_retained_as_separate_family":True,
        "interpretation_ceiling":[
            "point_sign_flip_is_not_individually_supported_two_sided_sign_reversal",
            "both_cells_individually_supported_is_not_24_edge_familywise_proof",
            "two_printed_value_familywise_differences_lost_under_decimal_rounding",
            "normal_Wald_with_reported_SE_and_comparability_assumptions",
            "arbitrary_source_cell_covariance_not_set_to_zero",
            "posthoc_24_family_extension_is_sensitivity_not_prospective_primary_test",
            "fitness_outcome_models_differ_between_original_programmes_no_numeric_pooling",
            "primula_style_morph_composition_not_matched_across_pollen_arms",
            "trillium_2020_petal_size_direct_original_source_test_separate",
            "gymnadenia_same_five_traits_across_two_backgrounds_not_ten_independent_axes",
            "Gymnadenia_flowering_start_original_source_signs_are_herbivores_excluded_only",
            "source_phenotypes_not_directly_randomized_so_no_z_optimum_or_SCH_L",
            "no_estimate_of_natural_ecological_frequency_or_Slk_architecture_advantage",
        ]
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v27-source",type=Path,default=V27_SOURCE)
    parser.add_argument("--v27-holdout",type=Path,default=V27_READOUT)
    parser.add_argument("--gym-source",type=Path,default=GYM_SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    receipt=build(
        read_v27(args.v27_source),
        json.loads(args.v27_holdout.read_text(encoding="utf-8")),
        read_gym(args.gym_source),
    )
    data=json.dumps(receipt,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    else:
        print(data,end="")


if __name__=="__main__":
    main()
