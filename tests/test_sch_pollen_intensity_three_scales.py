"""Primary-source three-scale intensity interpretation with fail-closed data grains."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts.audit_sch_pollen_intensity_three_scales import (
    EXPERIMENT,OPPORTUNITY,PUBLISHED,csv_read,run)
ROOT=Path(__file__).resolve().parents[1]

def verified():
    return run(csv_read(EXPERIMENT),csv_read(OPPORTUNITY),csv_read(PUBLISHED))

def test_recover_2016_randomized_access_and_2017_opportunity():
    r=verified()
    assert r["n_distinct_original_published_programmes_considered"]==3
    assert r["source_2016_experiment_sites"]==1
    assert r["source_2016_pollination_intensity_treatments"]==5
    assert r["source_2016_PL_range_observed"]==[0,.77]
    assert r["source_2016_opportunity_selection_approx_fold"]==5
    assert r["source_2016_increased_pollinator_mediated_selection_percent"]=={
        "plant_height":91,"corolla_size":34,"spur_length":330}
    assert r["source_2017_species"]==12
    assert r["source_2017_PL_by_pollination_opportunity_interaction_F"]==pytest.approx(15.60)
    assert r["source_2017_PL_selection_F_components"]["POLLINATOR_MEDIATED"]==pytest.approx(18.79)
    assert r["source_2017_PL_selection_F_components"]["NONPOLLINATOR_MEDIATED"]==pytest.approx(.0045)
    assert not r["between_vs_within_effect_difference_tested"]
    assert not r["cross_study_numeric_pooling_performed"]
    assert r["no_causal_trait_optima_or_SCH_L"]

@pytest.mark.parametrize("where",["experiment","source_table1","table4","denominator"])
def test_source_mismatch_fails_closed(where):
    x=deepcopy(csv_read(EXPERIMENT));y=deepcopy(csv_read(OPPORTUNITY));z=deepcopy(csv_read(PUBLISHED))
    if where=="experiment":x[5]["original_value"]="331"
    if where=="source_table1":y[2]["F"]="15.61"
    if where=="table4":z[3]["F"]="18.0"
    if where=="denominator":y[2]["n_source_fit_units"]="60"
    with pytest.raises(ValueError):
        run(x,y,z)

def test_scientific_claim_ceiling_stays_in_prose():
    s=(ROOT/"docs/SCH_POLLEN_INTENSITY_THREE_SCALES_V1.md").read_text(encoding="utf-8")
    for term in ("91%", "34%", "330%", "16.78", "15.60", "14", "12",
                 "not", "2014", "2016", "2017", "trait", "source", "covariance"):
        assert term.lower() in s.lower()
