"""Author-fit orchid selection: source provenance, fixed denominators and scales."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts.audit_sch_orchid_2017_selection_scale import MATCHED,T2,T4,read_csv,run
ROOT=Path(__file__).resolve().parents[1]

def received():
    return run(read_csv(MATCHED),read_csv(T2),read_csv(T4))

def test_2017_source_original_experimental_selection_associations():
    r=received()
    assert r["compiled_137_pair_base_unchanged"]==137
    assert r["n_in_compilation_matched_pairs"]==12
    assert r["n_original_named_species_in_compilation"]==12
    assert r["n_compiled_trait_types_from_this_paper"]==1
    assert r["n_original_author_table2_trait_axes"]==5
    assert r["original_author_table2_direct_interactions"]==10
    assert r["original_author_table4_trait_component_test_rows"]==9
    p=r["original_author_PL_association_by_fitness_selection_component"]
    assert p["POLLINATOR_MEDIATED"]["original_F"]==pytest.approx(18.79)
    assert p["NONPOLLINATOR_MEDIATED"]["original_F"]==pytest.approx(.0045)
    assert p["NET"]["original_F"]==pytest.approx(6.374)
    assert len(r["direct_trait_interaction_10_comparison_sensitivity_passes"])==1
    assert r["direct_trait_interaction_10_comparison_sensitivity_passes"][0]["trait"]=="Plant height"

def test_2014_2017_scale_not_falsely_pooled():
    r=received()
    assert r["population_year_comparison_2014_n_population_years"]==14
    assert r["population_year_comparison_2014_n_species"]==2
    assert r["cross_study_pooled_scale_regression_performed"] is False
    assert r["independent_2017_source_raw_fitness_model_refitted"] is False
    assert any("species_cluster" in q for q in r["critical_limits"])

@pytest.mark.parametrize("mutation",["F","P","wrong_component","duplicated_species","source_comparison"])
def test_source_fails_closed(mutation):
    a=deepcopy(read_csv(MATCHED)); b=deepcopy(read_csv(T2));c=deepcopy(read_csv(T4))
    if mutation=="F":b[6]["F"]="9.99"
    elif mutation=="P":c[3]["p"]="0.5"
    elif mutation=="wrong_component":c[0]["definition"]="ABS_DELTA_BETA_OPEN_MINUS_HAND"
    elif mutation=="duplicated_species":
        row=next(x for x in a if x["paper_id"]=="33")
        row["species"]="Imaginary species"
    else:
        c[2]["df_den"]="60"
    if mutation=="duplicated_species":
        # One species identity can change without breaking a simple unique count:
        # replace with a species already present to verify duplicate rejection.
        row["species"]=next(x for x in a if x["paper_id"]=="33" and x is not row)["species"]
    with pytest.raises(ValueError):
        run(a,b,c)

def test_interpretation_deliberately_keeps_scope():
    s=(ROOT/"docs/SCH_ORCHID_2017_PL_BETWEEN_WITHIN_SCALE_V1.md").read_text(encoding="utf-8")
    for term in ("18.79", "0.947", "2014", "2017", "12", "14", "種間", "種内", "Dryad", "共通"):
        assert term.lower() in s.lower()
