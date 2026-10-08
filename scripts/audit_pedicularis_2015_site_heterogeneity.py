"""Source-backed, descriptive heterogeneity of the 2015 P. rex water experiment.

The six rows are site-specific estimates from ONE focal experiment, not six
independent papers. Coefficients are kept on their reported GLM scale.
Do not interpret this as a generalizable species-level meta-analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical/architecture/PEDICULARIS_PUBLISHED_EMPIRICAL_PRIORS_V1.csv"
EXPECTED_SITES = {
    "Baishuitai": ("PRX2015_PRED_BAISHUITAI", -0.104, 0.014),
    "Sanba": ("PRX2015_PRED_SANBA", -0.144, 0.015),
    "Zhongdian": ("PRX2015_PRED_ZHONGDIAN", -0.093, 0.348),
    "Deqin": ("PRX2015_PRED_DEQIN", -0.035, 0.017),
    "Daxueshan": ("PRX2015_PRED_DAXUESHAN", -0.084, 0.017),
    "Shama": ("PRX2015_PRED_SHAMA", -0.049, 0.017),
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("published site-effect ledger is empty")
    return rows


def _summary(effects: list[tuple[str, float, float]]) -> dict:
    if len(effects) < 3:
        raise ValueError("site heterogeneity requires at least three site estimates")
    fixed_w = [1.0 / (se * se) for _, _, se in effects]
    sw = sum(fixed_w)
    fixed_mean = sum(w * beta for w, (_, beta, _) in zip(fixed_w, effects, strict=True)) / sw
    q = sum(
        w * (beta - fixed_mean) ** 2
        for w, (_, beta, _) in zip(fixed_w, effects, strict=True)
    )
    df = len(effects) - 1
    denom = sw - sum(w * w for w in fixed_w) / sw
    if denom <= 0:
        raise ValueError("fixed-weight heterogeneity denominator is invalid")
    tau2 = max(0.0, (q - df) / denom)  # DerSimonian–Laird: sensitivity descriptor only.
    rw = [1.0 / (se * se + tau2) for _, _, se in effects]
    sw_re = sum(rw)
    re_mean = sum(w * beta for w, (_, beta, _) in zip(rw, effects, strict=True)) / sw_re
    return {
        "n_population_estimates": len(effects),
        "fixed_inverse_variance_model_scale_mean": fixed_mean,
        "fixed_inverse_variance_standard_error": math.sqrt(1.0 / sw),
        "Cochran_Q_source_estimates": q,
        "Cochran_Q_df": df,
        "I2_descriptive": max(0.0, (q - df) / q) if q > 0 else 0.0,
        "DerSimonian_Laird_tau2": tau2,
        "DerSimonian_Laird_tau": math.sqrt(tau2),
        "approx_random_effect_mean_model_scale": re_mean,
        "approx_random_effect_normal_se": math.sqrt(1.0 / sw_re),
    }


def build(rows: list[dict[str, str]]) -> dict:
    matched: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("measurement_id", "").startswith("PRX2015_PRED_"):
            if row["measurement_id"] in matched:
                raise ValueError("duplicate 2015 site estimate")
            matched[row["measurement_id"]] = row
    if set(matched) != {spec[0] for spec in EXPECTED_SITES.values()}:
        raise ValueError("original six 2015 site treatment coefficients are incomplete")

    effects = []
    original = []
    for site, (record_id, expected_beta, expected_se) in EXPECTED_SITES.items():
        record = matched[record_id]
        if (
            record["population_scope"] != site
            or record["source_id"] != "PRX2015_WATER"
            or record["evidence_level"] != "SITE_MODEL_COEFFICIENT"
            or record["uncertainty_type"] != "SE"
            or record["direct_freeze_eligible"] != "NO"
        ):
            raise ValueError(f"{site}: expected source/site/SE identity changed")
        try:
            beta = float(record["estimate"])
            se = float(record["uncertainty_value"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{site}: beta and SE must be numeric") from exc
        if (
            not math.isfinite(beta)
            or not math.isfinite(se)
            or se <= 0
            or abs(beta - expected_beta) > 1e-12
            or abs(se - expected_se) > 1e-12
        ):
            raise ValueError(f"{site}: published Table 2 beta or SE drifted")
        effects.append((site, beta, se))
        original.append({
            "site": site,
            "source_model_beta": beta,
            "source_model_SE": se,
            "source_model_beta_approx_wald_interval": [
                beta - 1.96 * se, beta + 1.96 * se
            ],
            "source_table": "Sun_Huang_2015_Table_2",
            "original_source_p_note": record["notes"],
        })

    result = _summary(effects)
    leavers = {}
    for site, _, _ in effects:
        sub = _summary([item for item in effects if item[0] != site])
        leavers[site] = {
            "approx_random_effect_mean_model_scale": sub[
                "approx_random_effect_mean_model_scale"
            ],
            "DerSimonian_Laird_tau": sub["DerSimonian_Laird_tau"],
            "I2_descriptive": sub["I2_descriptive"],
        }
    other_se = [se for site, _, se in effects if site != "Zhongdian"]
    site_values = [beta for _, beta, _ in effects]

    return {
        "analysis": "pedicularis_2015_six_site_water_damage_contrast_heterogeneity_v1",
        "source_doi": "10.1093/aobpla/plv019",
        "source_data_kind": "SIX_REPORTED_POPULATION_SPECIFIC_GLM_COEFFICIENTS_AND_SE",
        "original_source_units": "GLM_COEFFICIENT_SCALE_NOT_A_PROPORTION_OR_RISK_RATIO",
        "water_treatment_definition": "BRACT_PUNCTURE_PLUS_DRAINAGE_VS_INTACT",
        "water_only_effect_identified": False,
        "original_reported_site_by_treatment_chi2": 36.782,
        "original_reported_site_by_treatment_df": 5,
        "n_site_beta_negative": sum(b < 0 for b in site_values),
        "site_effects": original,
        "site_beta_span": max(site_values) - min(site_values),
        "source_Zhongdian_se_over_other_five_median": (
            next(se for site, _, se in effects if site == "Zhongdian")
            / median(other_se)
        ),
        "heterogeneity": result,
        "leave_one_site_out_descriptive": leavers,
        "claim_ceiling": [
            "one_2015_experiment_with_six_population_estimates_not_six_independent_studies",
            "inverse_variance_meta_formulas_are_diagnostics_not_source_model_refit",
            "high_I2_with_only_six_sites_is_imprecise_and_model_dependent",
            "normal_random_effect_SE_is_not_a_calibrated_small_k_confidence_interval",
            "original_global_site_interaction_is_primary_source_evidence",
            "GLM_beta_is_not_an_absolute_predation_probability_difference",
            "Zhongdian_nonsignificance_is_not_an_effect_absence",
            "cannot_infer_water_only_causes_reduced_predation_from_puncture_plus_drainage",
            "cannot_infer_plant_trait_specific_selection_or_SCH_qualified_independent_G",
            "raw_population_sample_sizes_covariance_and_reproductive_optima_not_recovered",
        ],
        "status": "PUBLISHED_CAUSAL_TREATMENT_GEOGRAPHIC_HETEROGENEITY_QUANTIFIED",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = build(_read(args.source))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
