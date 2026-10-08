from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASETS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PUBLISHED_DATASETS_V1.csv"
)
DEFAULT_PRIORS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PUBLISHED_EMPIRICAL_PRIORS_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _water_2015_site_evidence(priors: list[dict[str, str]]) -> dict:
    """Audit source-scale *published coefficients*, not a new water experiment.

    This diagnostic intentionally keeps treatment coding, model-based SE,
    individual/inflorescence treatment unit, and the Shama-only visitor
    experiment distinct. It does NOT pool published coefficients.
    """
    ids = {
        "Baishuitai": "PRX2015_PRED_BAISHUITAI",
        "Sanba": "PRX2015_PRED_SANBA",
        "Zhongdian": "PRX2015_PRED_ZHONGDIAN",
        "Deqin": "PRX2015_PRED_DEQIN",
        "Daxueshan": "PRX2015_PRED_DAXUESHAN",
        "Shama": "PRX2015_PRED_SHAMA",
    }
    lookup = {row["measurement_id"]: row for row in priors}
    site_rows = [
        row for row in priors
        if row["source_id"] == "PRX2015_WATER"
        and row["evidence_level"] == "SITE_MODEL_COEFFICIENT"
    ]
    if {row["measurement_id"] for row in site_rows} != set(ids.values()):
        raise ValueError("2015 water site-model coefficient set is incomplete or expanded")

    site_effects: dict[str, dict] = {}
    for site, measurement_id in ids.items():
        row = lookup[measurement_id]
        if (row["population_scope"] != site
            or row["uncertainty_type"] != "SE"
            or row["direct_freeze_eligible"] != "NO"):
            raise ValueError("2015 water site effect lost site, SE or external-prior identity")
        try:
            beta = float(row["estimate"])
            se = float(row["uncertainty_value"])
        except (ValueError, TypeError) as exc:
            raise ValueError("2015 site coefficients and SE must be numeric") from exc
        if not math.isfinite(beta) or not math.isfinite(se) or se <= 0:
            raise ValueError("2015 site coefficients must be finite with positive SE")
        site_effects[site] = {
            "published_model_beta": beta,
            "published_model_se": se,
            # Wald intervals are a diagnostic from reported SE, NOT source CIs.
            "approx_wald95_model_scale": [beta - 1.96 * se, beta + 1.96 * se],
            "source_p_note": row["notes"],
        }

    zhong = site_effects["Zhongdian"]
    informative_se = [v["published_model_se"] for site, v in site_effects.items()
                      if site != "Zhongdian"]
    visitor = lookup["PRX2015_POLLINATOR_TREAT_BETA"]
    if visitor["population_scope"] != "Shama" or visitor["source_id"] != "PRX2015_WATER":
        raise ValueError("2015 visitor-rate comparison was Shama only")

    return {
        "source_doi": "10.1093/aobpla/plv019",
        "n_source_populations": len(site_effects),
        "n_negative_signed_site_coefficients": sum(
            effect["published_model_beta"] < 0 for effect in site_effects.values()
        ),
        "site_coefficients": site_effects,
        "Zhongdian_se_relative_to_other_five_median": (
            zhong["published_model_se"] / median(informative_se)
        ),
        "Zhongdian_approx_interval_contains_zero": (
            zhong["approx_wald95_model_scale"][0] <= 0
            <= zhong["approx_wald95_model_scale"][1]
        ),
        "site_effect_source_scale": "PUBLISHED_GLM_COEFFICIENT_NOT_RISK_DIFFERENCE",
        "water_intervention": "BRACT_PUNCTURE_PLUS_DRAINAGE_AS_ONE_TREATMENT",
        "water_only_vs_wounding_effect_identified": False,
        "water_by_randomized_exsertion_interaction_identified": False,
        "published_visitation_comparison_scope": "SHAMA_ONLY",
        "published_visitation_comparison_source_p_note": visitor["notes"],
        "water_state_is_main_SCH_independent_G": False,
        "status": "SOURCE_LEVEL_WATER_EFFECT_AND_PRECISION_AUDITED_NO_MECHANISM_SPLIT",
        "claim_ceiling": [
            "negative_beta_direction_uses_original_paper_treatment_coding",
            "all_six_coefficients_share_sign_but_one_non_significant_site_is_imprecise",
            "Wald_interval_from_reported_SE_is_not_a_reanalysis_of_raw_capsules",
            "no_plant_or_patch_robust_reanalysis_from_article_coefficients",
            "water_effect_not_separated_from_bract_puncture",
            "visitation_nonsignificance_at_Shama_is_not_global_equivalence",
            "no_z_by_water_causal_interaction_or_optimum_identified",
        ],
    }


def build(
    dataset_path: Path = DEFAULT_DATASETS,
    prior_path: Path = DEFAULT_PRIORS,
) -> dict:
    datasets = _read(dataset_path)
    priors = _read(prior_path)

    source_ids = [row["source_id"] for row in datasets]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("published dataset source_id must be unique")
    source_set = set(source_ids)

    measurement_ids = [row["measurement_id"] for row in priors]
    if len(measurement_ids) != len(set(measurement_ids)):
        raise ValueError("published empirical measurement_id must be unique")

    unknown = sorted(
        {row["source_id"] for row in priors} - source_set
    )
    if unknown:
        raise ValueError(
            "published empirical prior references unknown source_id: "
            + ", ".join(unknown)
        )

    direct_freeze_rows = [
        row
        for row in priors
        if row["direct_freeze_eligible"] != "NO"
    ]
    if direct_freeze_rows:
        raise ValueError(
            "published prior ledger must not silently promote historical "
            "measurements into direct F0 freeze values"
        )

    source_direct_freeze = [
        row
        for row in datasets
        if row["direct_F0_freeze_eligible"] != "NO"
    ]
    if source_direct_freeze:
        raise ValueError(
            "published dataset ledger must remain external-prior only"
        )

    source_counts = Counter(row["source_id"] for row in priors)
    evidence_counts = Counter(row["evidence_level"] for row in priors)
    access_counts = Counter(row["public_data_status"] for row in datasets)

    raw_sources = sorted(
        row["source_id"]
        for row in datasets
        if "RAW_DATA" in row["public_data_status"]
    )
    supplement_sources = sorted(
        row["source_id"]
        for row in datasets
        if "SUPPLEMENT" in row["public_data_status"]
    )

    sd_rows = [
        row["measurement_id"]
        for row in priors
        if row["uncertainty_type"] == "SD"
    ]
    se_rows = [
        row["measurement_id"]
        for row in priors
        if row["uncertainty_type"] == "SE"
    ]
    sem_rows = [
        row["measurement_id"]
        for row in priors
        if row["uncertainty_type"] == "SEM"
    ]

    external_support = {
        "CAL_A": sorted(
            row["measurement_id"]
            for row in priors
            if "CAL_A" in row["candidate_gate_family"]
        ),
        "CAL_B": sorted(
            row["measurement_id"]
            for row in priors
            if "CAL_B" in row["candidate_gate_family"]
        ),
        "CAL_C": sorted(
            row["measurement_id"]
            for row in priors
            if "CAL_C" in row["candidate_gate_family"]
        ),
    }

    missing_direct_systems = [
        "same_flower_repeatability_for_registered_P0_metrics",
        "multi_level_P_rex_z_manipulation_with_off_target_checks",
        "P_rex_pollination_supplementation_effect_on_pollen_and_initial_seed_set",
        "independent_seed_predator_exclusion_effect_with_water_y_fixed",
        "independent_G_timing_window_qualified_in_P_rex",
    ]

    return {
        "analysis": "pedicularis_published_empirical_prior_audit_v1",
        "n_published_sources": len(datasets),
        "n_published_measurement_rows": len(priors),
        "measurement_rows_by_source": dict(sorted(source_counts.items())),
        "evidence_level_counts": dict(sorted(evidence_counts.items())),
        "public_data_status_counts": dict(sorted(access_counts.items())),
        "public_raw_data_sources": raw_sources,
        "public_supplement_sources": supplement_sources,
        "n_rows_with_reported_sd": len(sd_rows),
        "rows_with_reported_sd": sorted(sd_rows),
        "n_rows_with_reported_se": len(se_rows),
        "rows_with_reported_se": sorted(se_rows),
        "n_rows_with_reported_sem": len(sem_rows),
        "rows_with_reported_sem": sorted(sem_rows),
        "water_2015_site_evidence": _water_2015_site_evidence(priors),
        "external_support_by_calibration_module": external_support,
        "n_direct_F0_freeze_values_recovered": 0,
        "published_data_can_replace_same_context_calibration_package": False,
        "highest_priority_raw_recovery": {
            "source_id": "PRX2013_ALLEE",
            "dataset_doi": "10.5061/dryad.6cv06",
            "file": "raw data.xlsx",
            "reason": (
                "public raw data are explicitly deposited and can recover "
                "seed-set/predation distributions beyond article-level summaries"
            ),
        },
        "second_priority_recovery": {
            "source_id": "PRX2016_SELECTION",
            "article_doi": "10.1093/aob/mcw097",
            "files": [
                "supp_mcw097_aob-16074-s01.doc",
                "supp_mcw097_aob-16074-s02.xls",
            ],
            "reason": (
                "supplements contain population means/SE for 12 traits and "
                "pollination plus initial/final seed set and predation"
            ),
        },
        "remaining_direct_empirical_gaps": missing_direct_systems,
        "status": "PUBLISHED_EMPIRICAL_PRIORS_RECOVERED_CALIBRATION_STILL_REQUIRED",
        "claim_ceiling": [
            "historical_external_priors_only",
            "do_not_relabel_water_drainage_as_independent_G",
            "do_not_use_article_model_coefficients_as_same_context_gate_values",
            "raw_or_aggregate_historical_data_can_inform_variance_effect_scale_and_feasibility",
            "same_context_prospective_CAL_A_B_C_and_F0_are_not_replaced",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit recovered published Pedicularis rex measurements and their "
            "bounded use as external CAL-A/B/C priors"
        )
    )
    parser.add_argument("--datasets", type=Path, default=DEFAULT_DATASETS)
    parser.add_argument("--priors", type=Path, default=DEFAULT_PRIORS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.datasets, args.priors)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
