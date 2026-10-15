from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_2015_cross_endpoint import (
    SOURCE, build, read_source, chi_square_survival_odd_df,
)


def test_source_printed_three_endpoints_x_three_terms_are_preserved():
    r=build(read_source(SOURCE))
    assert r["n_independent_primary_experiments"]==1
    assert r["n_original_populations"]==6
    assert r["n_endpoints"]==3
    assert r["n_source_table_tests"]==9
    assert not r["source_plant_capsule_raw_data_recovered"]
    x=r["published_site_and_treatment_tests"]
    assert set(x)=={"initial_seed_set","final_seed_set","seed_predation"}
    assert x["seed_predation"]["SITE_X_TREATMENT"]["chi_square"]==36.782
    assert x["final_seed_set"]["SITE_X_TREATMENT"]["chi_square"]==4.913
    assert x["initial_seed_set"]["SITE_X_TREATMENT"]["chi_square"]==1.032
    assert x["final_seed_set"]["TREATMENT"]["chi_square"]==16.710


def test_reproduced_source_p_values_match_original_table_rounding():
    r=build(read_source(SOURCE))
    tests=r["published_site_and_treatment_tests"]
    for e in tests.values():
        for item in e.values():
            p=item["p_from_rounded_chi_square"]
            if item["printed_p"].startswith("<"):
                assert p<float(item["printed_p"][1:])
            else:
                assert p==pytest.approx(float(item["printed_p"]),abs=5.1e-4)
    assert chi_square_survival_odd_df(1.032,5)==pytest.approx(.95994367782)
    assert chi_square_survival_odd_df(4.913,5)==pytest.approx(.42658988937)
    assert chi_square_survival_odd_df(36.782,5)==pytest.approx(.000000662339)


def test_biological_signature_is_narrow_not_fitness_equality():
    r=build(read_source(SOURCE))
    evidence=r["original_results_at_nominal_alpha_0_05"]
    assert evidence["treatment_effect_supported_endpoints"]==[
        "final_seed_set","seed_predation"]
    assert evidence["site_by_treatment_supported_endpoints"]==["seed_predation"]
    assert len(evidence["site_main_effect_supported_endpoints"])==3
    assert "absence_of_significant_final_seed_interaction_is_not_equivalence" in r[
        "causal_interpretation_limits"]
    assert "different_p_values_are_not_a_formal_between_endpoint_interaction_test" in r[
        "causal_interpretation_limits"]
    assert "does_not_estimate_phenotype_dependent_predator_selection" in r[
        "causal_interpretation_limits"]


@pytest.mark.parametrize("key,new_value",[
    ("reported_chi2","0.2"),
    ("reported_p","0.001"),
    ("reported_se","0.05"),
    ("reported_beta","-0.2"),
    ("reported_df","3"),
    ("biological_intervention","WATER_ONLY"),
    ("source_doi","10.0000/fabricated"),
    ("source_table","Table_1"),
])
def test_original_source_identity_and_numeric_values_are_immutable(key,new_value):
    rows=deepcopy(read_source(SOURCE))
    rows[0][key]=new_value
    with pytest.raises(ValueError,match="drift|invalid|contradicts"):
        build(rows)


def test_duplicate_endpoint_and_missing_endpoint_rejected():
    rows=read_source(SOURCE)
    with pytest.raises(ValueError,match="nine"):
        build(rows[:-1])
    duplicates=deepcopy(rows)
    duplicates[1]=deepcopy(duplicates[0])
    with pytest.raises(ValueError,match="duplicated"):
        build(duplicates)


def test_chi_square_tail_fail_closed_on_unsupported_degrees_of_freedom():
    with pytest.raises(ValueError,match="odd positive"):
        chi_square_survival_odd_df(4.913,4)
    with pytest.raises(ValueError,match="invalid chi-square"):
        chi_square_survival_odd_df(-1,5)


def test_source_audit_is_not_novel_randomized_z_G_field_evidence():
    r=build(read_source(SOURCE))
    assert r["status"]=="REAL_PUBLISHED_ENDPOINT_PATTERN_RECOVERED_NO_RAW_CAUSAL_COMPONENTS"
    ceiling=r["causal_interpretation_limits"]
    assert "does_not_estimate_water_fixed_selective_predator_G" in ceiling
    assert "does_not_identify_P_rex_optimum_shift_or_SCH_L" in ceiling
    assert "same_six_sites_are_not_six_independent_experiments" in ceiling


def test_manuscript_and_figure_cite_actual_cross_endpoint_source_without_equivalence():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    paper=(root/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    figure=(root/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md").read_text(encoding="utf-8")
    doc=(root/"docs/SCH_PEDICULARIS_2015_REAL_CROSS_ENDPOINT_DEFENCE_MOSAIC_V1.md").read_text(encoding="utf-8")
    for token in (
        "chi-square = 36.782",
        "chi-square = 4.913",
        "P = 0.4265",
        "P = 0.960",
        "SCH_PEDICULARIS_2015_REAL_CROSS_ENDPOINT_DEFENCE_MOSAIC_V1.md",
    ):
        assert token in paper
    assert "not evidence that final-seed effects are uniform among sites" in paper
    assert "NOT EQUIVALENCE" in figure
    assert "different significance outcomes" not in doc
    assert "not a formal test of the difference" in doc
    assert "No plant data were retrieved" in doc
