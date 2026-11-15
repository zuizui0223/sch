"""Audit original-author interaction tests against the frozen 137-pair SCH meta.

Stinchcombe (2002) Table 2 p-values test phenotype-versus-genotype
selection bias within insect regimes, not insect-by-trait interactions.
This is a primary-source reanalysis, not newly collected plant data.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
BEANS = ROOT / "data/SCH_2020_BEANS_ROACH_AUTHOR_INTERACTIONS_V2.csv"
STINCH = ROOT / "data/SCH_2020_STINCHCOMBE_TABLE2_ESTIMAND_V1.csv"

# Original Beans & Roach (2015) AJB Table 2, DOI 10.3732/ajb.1400355.
EXPECTED_BEANS = {
    ("GREENHOUSE", "Early growth rate"): (204, 208, 4.38, "0.04"),
    ("GREENHOUSE", "Hypocotyl length"): (205, 209, 0.76, "0.39"),
    ("GREENHOUSE", "Internode 1 length"): (206, 210, 8.35, "0.005"),
    ("GREENHOUSE", "Number of internodes"): (207, 211, 82.74, "<0.0001"),
    ("FIELD", "Early growth rate"): (212, 216, 3.93, "0.049"),
    ("FIELD", "Hypocotyl length"): (213, 217, 0.09, "0.76"),
    ("FIELD", "Internode 1 length"): (214, 218, 0.17, "0.68"),
    ("FIELD", "Number of internodes"): (215, 219, 0.88, "0.35"),
}
# Stinchcombe et al. (2002) Am Nat Table 2: author tests bias WITHIN regimes.
EXPECTED_STINCH = {
    "INSECTS_ABSENT": (495, .790, .030, .018, .060, 7e-6, 9e-6, .052),
    "INSECTS_PRESENT": (496, .044, .050, .020, .050, 4e-7, 1.2e-6, .76),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def same_float(actual: str, expected: float) -> bool:
    return abs(float(actual) - float(expected)) < 1e-10


def p_upper(source_p: str) -> float:
    """A displayed '<0.0001' stays an inequality, never an invented exact p."""
    return float(source_p[1:] if source_p.startswith("<") else source_p)


def run(pairs: list[dict[str, str]], beans: list[dict[str, str]],
        stinch: list[dict[str, str]]) -> dict:
    if len(pairs) != 137 or len(beans) != 8 or len(stinch) != 2:
        raise ValueError("source cohort count drift: expected 137, eight, and two")
    indexed = {}
    for row in pairs:
        key = (row["paper_id"], row["source_row_id_1"], row["source_row_id_2"])
        if key in indexed:
            raise ValueError("duplicate compiled paper/source pair")
        indexed[key] = row

    checked, found = [], set()
    for source in beans:
        key = (source["study"], source["trait"])
        if key not in EXPECTED_BEANS or key in found:
            raise ValueError("unexpected or duplicate Beans & Roach primary trait")
        found.add(key)
        id1, id2, fitted_F, fitted_p = EXPECTED_BEANS[key]
        context = ("INDOOR_CONTROLLED" if key[0] == "GREENHOUSE"
                   else "IN_SITU_NATURAL_POPULATION")
        if (source["paper_id"] != "13" or
            source["doi"] != "10.3732/ajb.1400355" or
            source["original_source"] != "Table2" or
            source["source_context"] != context or
            source["original_p"] != fitted_p or
            not same_float(source["original_F"], fitted_F) or
            source["original_df"] != ("1,122" if key[0] == "GREENHOUSE" else "1,222") or
            int(source["source_row_id_1"]) != id1 or
            int(source["source_row_id_2"]) != id2):
            raise ValueError("source author-fitted interaction/source row drift")
        pair = indexed.get(("13", str(id1), str(id2)))
        if pair is None or pair["trait"] != key[1] or pair["source_context"] != context:
            raise ValueError("missing or mismatched compiled 137-pair identity")
        for source_col, paired_col in (
            ("beta_absent", "beta1"), ("se_absent", "se1"),
            ("beta_present", "beta2"), ("se_present", "se2")):
            if not same_float(source[source_col], float(pair[paired_col])):
                raise ValueError("original source gradient does not match frozen pair")
        p = p_upper(fitted_p)
        beta1, beta2 = float(pair["beta1"]), float(pair["beta2"])
        checked.append({
            "study": key[0], "trait": key[1], "source_row_ids": [id1, id2],
            "beta_absent": beta1, "beta_present": beta2,
            "delta_beta_present_minus_absent": round(beta2-beta1, 8),
            "original_author_fitted_F": fitted_F, "original_author_p": fitted_p,
            "nominal_p_lt_0_05": p < .05,
            "source_eight_tests_bonferroni_0_05": p < .05/8,
            "exploratory_137_comparison_threshold": p < .05/137,
            "point_sign_flip": beta1 * beta2 < 0,
            "both_arm_opposite_nonzero_supported":
                pair["source_both_arm_opposite_signs_nominal95"].lower() == "true",
        })
    if found != set(EXPECTED_BEANS):
        raise ValueError("missing author test or treatment context")

    source_pair = indexed.get(("37", "495", "496"))
    if source_pair is None or source_pair["trait"] != "Total leaf area":
        raise ValueError("2002 compiled leaf-area source pair missing")
    stin_seen = set()
    for row in stinch:
        regime = row["regime"]
        if regime not in EXPECTED_STINCH or regime in stin_seen:
            raise ValueError("unexpected or duplicate Stinchcombe regime")
        stin_seen.add(regime)
        expected = EXPECTED_STINCH[regime]
        if (row["paper_id"] != "37" or row["doi"] != "10.1086/342069" or
            row["trait"] != "Total leaf area" or row["source"] != "Table2" or
            row["author_test_estimand"] != "PHENOTYPIC_VS_GENOTYPIC_BIAS_WITHIN_REGIME" or
            row["source_row_id"] != str(expected[0])):
            raise ValueError("2002 primary-author tested estimand mismatch")
        for col, number in zip(("beta_phenotypic_standardized",
                                "se_phenotypic_standardized",
                                "beta_genotypic_standardized",
                                "se_genotypic_standardized",
                                "beta_phenotypic_unstandardized",
                                "beta_genotypic_unstandardized",
                                "author_within_regime_bias_p"), expected[1:]):
            if not same_float(row[col], number):
                raise ValueError("2002 original Table 2 numeric drift")
        paired_beta = (source_pair["beta1"] if regime == "INSECTS_ABSENT"
                       else source_pair["beta2"])
        if not same_float(row["beta_phenotypic_standardized"], float(paired_beta)):
            raise ValueError("2002 source beta alignment changed")
    if stin_seen != set(EXPECTED_STINCH):
        raise ValueError("2002 Table 2 treatment arm missing")

    greenhouse = {x["trait"]: x for x in checked if x["study"] == "GREENHOUSE"}
    node_count, first_node = greenhouse["Number of internodes"], greenhouse["Internode 1 length"]
    if not (node_count["delta_beta_present_minus_absent"] > 0 >
            first_node["delta_beta_present_minus_absent"] and
            node_count["source_eight_tests_bonferroni_0_05"] and
            first_node["source_eight_tests_bonferroni_0_05"]):
        raise ValueError("registered opposing strength responses not supported")
    field_growth = next(x for x in checked if x["study"] == "FIELD" and
                        x["trait"] == "Early growth rate")
    if not (field_growth["nominal_p_lt_0_05"] and
            field_growth["point_sign_flip"] and
            not field_growth["both_arm_opposite_nonzero_supported"]):
        raise ValueError("source field-growth test/point-flip distinction changed")

    return {
        "analysis": "sch_2020_original_author_fitted_context_audit_v2",
        "source_meta_doi": "10.5061/dryad.sn02v6x0q",
        "primary_2015_doi": "10.3732/ajb.1400355",
        "primary_2002_doi": "10.1086/342069",
        "compiled_matched_pair_denominator_unchanged": 137,
        "independent_2015_biological_papers_in_this_audit": 1,
        "author_fitted_2015_interaction_tests": len(checked),
        "n_nominal_direct_p_below_0_05": sum(x["nominal_p_lt_0_05"] for x in checked),
        "n_direct_p_below_0_05_over_eight": sum(x["source_eight_tests_bonferroni_0_05"] for x in checked),
        "n_direct_p_below_0_05_over_137": sum(x["exploratory_137_comparison_threshold"] for x in checked),
        "direct_source_tests": sorted(checked, key=lambda x: (x["study"], x["trait"])),
        "greenhouse_trait_specific_strength_divergence":
            ["Number of internodes", "Internode 1 length"],
        "field_early_growth_direct_interaction_nominal_not_two_arm_sign_certified": True,
        "stinchcombe_table2_p_values_test_bias_within_regimes_not_trait_by_insect": True,
        "stinchcombe_source_table2_direct_trait_by_insect_p_recovered": False,
        "original_meta_regression_not_reestimated": True,
        "claim_limits": [
            "2015_eight_tests_are_one_publication_not_eight_independent_species",
            "observational_trait_selection_slopes_do_not_randomize_trait_values",
            "first_internode_and_number_of_internodes_are_distinct_coordinates",
            "2015_field_early_growth_point_sign_flip_is_not_two_arm_supported_reversal",
            "2002_bias_tests_must_not_be_relabelled_treatment_interactions",
            "source_phenotypic_slopes_not_pure_function_optima_or_SCH_L",
            "unrecovered_2002_direct_interaction_not_proof_of_no_interaction",
        ],
        "status": "ONE_PAPER_WITH_TWO_EIGHT_TEST_SUPPORTED_OPPOSITE_MAGNITUDE_CHANGES__NO_META_GENERALITY",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=Path, default=PAIRS)
    parser.add_argument("--beans", type=Path, default=BEANS)
    parser.add_argument("--stinch", type=Path, default=STINCH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(read_csv(args.pairs), read_csv(args.beans), read_csv(args.stinch))
    output = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
