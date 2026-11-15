"""Independent published-number Pearson test, not original plant-data refit."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts.audit_sch_trunschke2017_pearson_grain import (
    SOURCE,parse_source,run,pearson_two_sided_p,
)

ROOT=Path(__file__).resolve().parents[1]


def current():
    return run(parse_source(SOURCE))


def test_independent_population_n12_pearson_recalculation():
    r=current()
    x={item["trait"]:item for item in r["published_r_and_P_recalculated_by_independent_population_n12"]}
    assert r["n_independent_populations"]==12
    assert r["n12_nominal_P_under_0_05_count"]==2
    assert r["n12_original_reported_P_labels_recovered_count"]==0
    assert x["Flower size"]["n12_two_sided_pearson_p"]==pytest.approx(.16513256,abs=1e-8)
    assert x["Flowering start"]["n12_two_sided_pearson_p"]==pytest.approx(.00389296,abs=1e-8)
    assert x["Plant height"]["n12_two_sided_pearson_p"]==pytest.approx(.00254344,abs=1e-8)
    assert all(not item["published_P_compatible_with_independent_n12"] for item in x.values())
    assert all(item["printed_P_numerically_near_n24_convention"] for item in x.values())


def test_source_figure_2_opportunity_control_matches_n12():
    r=current()
    assert r["figure2_open_PL_vs_opportunity_published_R2"]==.63
    assert r["figure2_open_recomputed_n12_P"]==pytest.approx(.00205603,abs=1e-8)


def test_reward_group_pl_gap_is_source_coded_and_posthoc_only():
    r=current()
    counts=r["reward_strategy_PL_bimodal_observed_counts"]
    assert sum(v for k,v in counts.items() if k!="species_between_0_4_and_0_8")==12
    assert counts["species_between_0_4_and_0_8"]==0
    assert r["post_hoc_conditional_Fisher_two_sided_P"]==pytest.approx(.01515152,abs=1e-8)
    assert "post_hoc_PL_group_cutoffs_do_not_provide_prospective_population_generalization" in r["critical_limits"]


@pytest.mark.parametrize("mutate",["r","p","n","doi","duplicate"])
def test_original_r_p_n_and_study_identity_cannot_drift(mutate):
    rows=deepcopy(parse_source(SOURCE))
    if mutate=="r":rows[2]["pearson_r"]="-0.500"
    if mutate=="p":rows[3]["original_printed_p"]="0.001"
    if mutate=="n":rows[0]["independent_population_count"]="24"
    if mutate=="doi":rows[1]["paper_doi"]="10.9999/other"
    if mutate=="duplicate":rows[4]["trait"]="Flower size"
    with pytest.raises(ValueError):
        run(rows)


def test_pdf_and_dryad_blockers_do_not_turn_into_raw_reanalysis():
    doc=(ROOT/"docs/SCH_TRUNSCHKE2017_PEARSON_SOURCE_GRAIN_AUDIT_20261115.md").read_text()
    for s in ("0.165133","12 species","n=24","2017","0.01515",
              "not a newly collected","not recalculated","Table S5/S6"):
        assert s.lower() in doc.lower()
    assert "Original individual orchid rows successfully refitted" not in doc
