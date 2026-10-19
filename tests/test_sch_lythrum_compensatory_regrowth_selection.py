"""2017 original-source tolerance, phenotype and floral selection fidelity."""
from __future__ import annotations

from copy import deepcopy
import csv
import json
from pathlib import Path

import pytest

from scripts.audit_sch_lythrum_compensatory_regrowth_selection import (
    PHENOTYPES, SELECTION, build, _rows,
)

ROOT=Path(__file__).resolve().parents[1]


def _case():
    return build(_rows(PHENOTYPES),_rows(SELECTION))


def test_full_original_table_1_and_table_2_source_grain():
    r=_case()
    assert r["source_doi"]=="10.1093/aob/mcx026"
    assert r["original_study_count"]==1
    assert len(r["original_table_1_reported_phenotypes"])==7
    assert len(r["original_table_2_selection_responses"])==3
    assert r["source_design_counts"]=={
        "clipped_final":87,"control_final":86,"final_total":173,
        "original_selected_stems":178,"original_control_reassigned":8,
        "pollen_pair_count":429,
    }
    assert r["clipping_reassignment_violates_pure_initial_ITT_interpretation"]
    assert r["paired_within_plant_pollen_supplementation_not_independent_plant_randomization"]


def test_regrowth_means_and_selection_have_opposing_context_direction():
    r=_case()
    p=r["original_table_1_reported_phenotypes"]
    t=r["original_table_2_selection_responses"]
    assert p["number_of_inflorescences"]["clipped_mean"]==8
    assert p["number_of_inflorescences"]["control_mean"]==5.4
    assert p["number_of_inflorescences"]["relative_change_percent_vs_control"]==pytest.approx(48.14815,abs=1e-5)
    assert p["number_of_flowers"]["relative_change_percent_vs_control"]==pytest.approx(27.03030,abs=1e-5)
    assert p["number_of_fruit"]["relative_change_percent_vs_control"]==pytest.approx(31.23596,abs=1e-5)
    assert p["flowering_start_julian"]["clipped_minus_control"]==5
    assert p["flowering_end_julian"]["clipped_minus_control"]==0
    assert r["mean_calendar_window_proxy"]=={
        "control_end_minus_start":45.0,
        "clipped_end_minus_start":40.0,
        "differential_mean_calendar_span_days":-5.0,
        "not_plant_level_flowering_duration_distribution":True,
    }
    assert t["number_of_inflorescences"]["clipped_beta"]==pytest.approx(.20)
    assert t["number_of_inflorescences"]["control_beta"]==pytest.approx(.47)
    assert t["number_of_inflorescences"]["damage_control_minus_clipped_delta"]==pytest.approx(.27)
    assert t["flowering_start_time"]["clipped_beta"]==pytest.approx(-.28)
    assert t["flowering_start_time"]["control_beta"]==pytest.approx(-.03)
    assert t["flowering_start_time"]["damage_control_minus_clipped_delta"]==pytest.approx(.25)


def test_damage_selection_source_significance_not_pollen_equivalence():
    r=_case()
    assert r["mean_seed_set_hand_pollen_gain_percent"]==17.4
    assert r["pollen_limitation_between_damage_groups_original_p"]==pytest.approx(.2718)
    assert r["pollen_limitation_no_difference_detected_is_not_equivalence"]
    gradients=r["original_table_2_selection_responses"]
    assert {x["damage_original_source_flag"] for x in gradients.values()}=={
        "P_LT_0.01", "P_LT_0.05", "NS"
    }
    assert all(x["pollination_treatment_x_trait_source_flag"]=="NS" for x in gradients.values())
    assert all(x["pollination_x_damage_x_trait_source_flag"]=="NS" for x in gradients.values())
    assert r["n_damage_interactions_with_original_p_below_0_05"]==2
    assert r["n_3_damage_test_bonferroni_normal_supported"]==2
    assert r["n_3_damage_test_bonferroni_rounding_robust"]==1
    assert r["n_all_9_contrast_bonferroni_supported"]==0
    assert gradients["number_of_inflorescences"][
        "bonferroni_three_damage_tests_rounding_robust"]
    assert not gradients["flowering_start_time"][
        "bonferroni_three_damage_tests_rounding_robust"]


@pytest.mark.parametrize(("column","tamper"),[
    ("source_doi","10.0000/fake"),
    ("source_table","Table_2"),
    ("model_transform","UNTRANSFORMED"),
    ("clipped_mean","0"),
    ("clipped_se","0.001"),
    ("control_mean","30"),
    ("source_p","0.90"),
])
def test_table1_source_tampering_rejected(column,tamper):
    p=deepcopy(_rows(PHENOTYPES))
    p[0][column]=tamper
    with pytest.raises(ValueError,match="drift|invalid|source"):
        build(p,_rows(SELECTION))


@pytest.mark.parametrize(("column","tamper"),[
    ("source_id","FABRICATED"),
    ("estimand_role","POLLINATOR_CAUSAL_OPTIMUM"),
    ("trait_standardization","RAW_MM"),
    ("beta_or_delta","9"),
    ("se","0.001"),
    ("significance","P_LT_0.001"),
])
def test_table2_source_tampering_rejected(column,tamper):
    s=deepcopy(_rows(SELECTION))
    s[0][column]=tamper
    with pytest.raises(ValueError,match="source|drift"):
        build(_rows(PHENOTYPES),s)


def test_no_silent_missing_rows_or_duplicate_components():
    phenotypes=_rows(PHENOTYPES)
    selection=_rows(SELECTION)
    with pytest.raises(ValueError,match="seven"):
        build(phenotypes[:-1],selection)
    with pytest.raises(ValueError,match="3 traits x 5"):
        build(phenotypes,selection[:-1])
    dup=deepcopy(selection)
    dup[0]=deepcopy(dup[1])
    with pytest.raises(ValueError,match="duplicate"):
        build(phenotypes,dup)


def test_fifth_study_uses_existing_cluster_no_pollination_holdout_corruption():
    r=_case()
    original=json.loads((ROOT/"data/SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json").read_text(encoding="utf-8"))
    assert original["n_programmes_adjudicated"]==3
    assert original["n_supported_reversal_axes"]==2
    ledger=_rows(ROOT/"data/SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv")
    assert len(ledger)==15
    assert len({row["programme_id"] for row in ledger})==1
    assert "one_published_study_not_an_additional_V27_pollination_programme" in r["claim_ceiling"]
    assert "flower_pair_pollination_treatment_is_within_plant_not_crossed_whole_plant_P" in r["claim_ceiling"]


def test_manuscript_and_figure_do_not_promote_trait_optimum():
    text=(ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    figure=(ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md").read_text(encoding="utf-8")
    note=(ROOT/"docs/SCH_LYTHRUM_COMPENSATORY_REGROWTH_SELECTION_V1.md").read_text(encoding="utf-8")
    for required in ("### 7.10","17.4%","5 days","0.27","0.25","Lythrum"):
        assert required in text
    assert "eight" in note.lower() and "reassign" in note.lower()
    assert "not an equivalence" in note.lower()
    assert "Lythrum" in figure
    assert "source phenotype not randomly assigned" in figure
