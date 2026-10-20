from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.audit_sch_brassica_multistage_receiver_geometry import (
    BEHAVIOUR, NET, CORR, NONADD, REGIMES, RESPONSES, build, read,
)

ROOT=Path(__file__).resolve().parents[1]


def _frozen():
    return build(read(BEHAVIOUR),read(NET),read(CORR),read(NONADD))


def test_primary_original_table_denominators_one_cage_experiment():
    s=_frozen()
    assert s["source_doi"]=="10.1007/s10682-016-9878-8"
    assert s["n_independent_original_cage_experiments"]==1
    assert s["n_floral_trait_coordinates"]==9
    assert s["n_original_consumer_regimes"]==3
    assert s["n_original_receiver_response_classes"]==3
    assert s["source_table_rows"]=={
        "receiver_behavior_Table_1":27,
        "net_selection_Table_2":27,
        "correlational_selection_Table_3":18,
        "nonadditive_author_main_text":2,
    }
    assert s["butterfly_ecological_role"]=="FLOWER_VISITOR_AND_LARVAL_HERBIVORE_PARENT"


def test_exactly_two_flower_signals_overlap_visitor_and_oviposition_channels():
    s=_frozen()
    assert s["nominal_triple_positive_receiver_traits"]==[
        "corolla_size","phenylacetaldehyde"
    ]
    assert s["receiver_overlap_count_nominal"]==2
    d=s["two_shared_receiver_traits_response_matrix"]
    assert d["corolla_size"]["BUMBLE_BEE_FLOWER_VISITS"]["beta"]==pytest.approx(.24)
    assert d["corolla_size"]["CABBAGE_BUTTERFLY_FLOWER_VISITS"]["beta"]==pytest.approx(.15)
    assert d["corolla_size"]["CABBAGE_BUTTERFLY_OVIPOSITION"]["beta"]==pytest.approx(.45)
    assert d["phenylacetaldehyde"]["CABBAGE_BUTTERFLY_OVIPOSITION"]["beta"]==pytest.approx(.41)
    assert all(v["nominal_source_positive"] for vals in d.values() for v in vals.values())


def test_net_seed_selection_stays_positive_for_corolla_across_three_regimes():
    s=_frozen()
    assert s["net_seed_selection_positive_in_all_three_regimes"]==["corolla_size"]
    q=s["net_coral_positive_all_3_source_p"]
    assert [q[r]["beta"] for r in REGIMES]==pytest.approx([.22,.22,.26])
    assert all(q[r]["nominal_source_positive"] for r in REGIMES)
    p=s["phenylacetaldehyde_net_selection"]
    assert [p[r]["beta"] for r in REGIMES]==pytest.approx([.15,-.09,.08])
    assert [r for r in REGIMES if p[r]["nominal_source_positive"]]==["BUMBLE_BEE"]
    assert all(not p[r]["nominal_source_negative"] for r in REGIMES)


def test_bee_biased_farnesene_detection_not_proof_of_private_channel():
    s=_frozen()
    assert s["nominal_bee_positive_without_detected_butterfly_visitation_or_oviposition"]==[
        "e_alpha_farnesene"
    ]
    t=s["e_alpha_farnesene_receiver_results"]
    assert [t[r]["beta"] for r in RESPONSES]==pytest.approx([.18,-.05,-.16])
    assert t["BUMBLE_BEE_FLOWER_VISITS"]["nominal_source_positive"]
    assert not t["CABBAGE_BUTTERFLY_FLOWER_VISITS"]["nominal_source_negative"]
    assert not t["CABBAGE_BUTTERFLY_OVIPOSITION"]["nominal_source_negative"]
    assert "bee_only_farnesene_source_nominal_detections_do_not_certify_butterfly_equivalence" in s[
        "claim_ceiling"]


def test_mixed_corolla_scent_correlational_result_is_not_familywise_supported():
    s=_frozen()
    k=s["mixed_regime_corolla_x_phenylacetaldehyde"]
    assert k["beta"]==pytest.approx(-.17)
    assert k["se"]==pytest.approx(.08)
    assert k["source_p"]=="0.029"
    assert k["18_correlational_tests_bonferroni_alpha"]==pytest.approx(.05/18)
    assert k["source_nominal_18_test_significance"] is True
    assert k["source_familywise_18_test_significance"] is False
    assert k["is_independent_test_of_between_regime_correlational_difference"] is False
    assert s["n_table3_source_p_below_0_05"]==1
    assert s["n_table3_bonferroni_18_p_below_0_05"]==0


def test_original_nonadditivity_is_author_test_not_fake_reestimated_covariance():
    s=_frozen()
    nonadd=s["author_reported_nonadditive_selection"]
    scent=nonadd["phenylacetaldehyde"]
    assert scent["arithmetic_reference_from_printed_table_2"]==pytest.approx(.115)
    assert scent["arithmetic_mixed_minus_additive"]==pytest.approx(-.205)
    assert scent["source_direct_author_fitted_observed_minus_expected"]==pytest.approx(-.20)
    assert scent["reported_source_se"]==pytest.approx(.08)
    assert scent["reported_source_p"]=="0.009"
    itc=nonadd["1_butene_4_isothiocyanate"]
    assert itc["arithmetic_reference_from_printed_table_2"]==pytest.approx(-.12)
    assert itc["arithmetic_mixed_minus_additive"]==pytest.approx(.19)
    assert itc["reported_source_p"]=="0.018"
    assert all(v["arithmetic_is_not_new_covariance_aware_original_test"] for v in nonadd.values())


def test_seed_fitness_bridge_is_distinct_from_binary_oviposition_beta():
    s=_frozen()
    f=s["source_fitness_pathway_results"]
    assert f["bee_visitation_to_seeds_beta"]==pytest.approx(20.5)
    assert f["butterfly_visitation_to_seeds_beta"]==pytest.approx(6.8)
    assert f["caterpillar_infestation_to_seeds_beta"]==pytest.approx(-104.5)
    assert f["bee_visits_x_caterpillar_infestation_beta"]==pytest.approx(-18.9)
    assert f["bee_visits_x_caterpillar_infestation_source_p"]=="0.046"
    assert f["same_model_scale_as_receiver_table_1_beta"] is False


@pytest.mark.parametrize(("file_index","field","bad"),[
    (0,"source_p","0.90"),
    (0,"beta","0.00"),
    (0,"response_scale","COST_IN_SEEDS"),
    (0,"source_warning","NONE"),
    (1,"p_value","0.999"),
    (1,"source_table","Table_3"),
    (2,"correlational_beta","0.999"),
    (2,"trait_pair","not_a_measured_pair"),
    (3,"reported_p","0.999"),
    (3,"expected_additive_rule","SOURCE_FABRICATED"),
])
def test_original_source_signatures_fail_closed_on_tampering(file_index,field,bad):
    sets=[read(BEHAVIOUR),read(NET),read(CORR),read(NONADD)]
    if file_index==0 and field=="source_warning":
        index=next(i for i,r in enumerate(sets[0]) if
                   r["trait"]=="methyl_benzoate"
                   and r["receiver_response"]=="CABBAGE_BUTTERFLY_FLOWER_VISITS")
    elif file_index==1 and field=="p_value":
        index=next(i for i,r in enumerate(sets[1]) if
                   r["trait"]=="corolla_size"
                   and r["consumer_regime"]=="BUMBLE_BEE")
    else:
        index=0
    sets[file_index][index][field]=bad
    with pytest.raises(ValueError,match="drift|source|unexpected|nonadditive|incomplete"):
        build(*sets)


def test_missing_data_and_duplicate_response_cannot_create_new_evidence():
    files=[read(BEHAVIOUR),read(NET),read(CORR),read(NONADD)]
    for i in range(4):
        corrupt=deepcopy(files)
        corrupt[i].pop()
        with pytest.raises(ValueError):
            build(*corrupt)
    corrupt=deepcopy(files)
    corrupt[0][1]=deepcopy(corrupt[0][0])
    with pytest.raises(ValueError,match="duplicate"):
        build(*corrupt)


def test_canonical_manuscript_preserves_original_one_study_and_stage_limits():
    m=(ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    fig=(ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md").read_text(encoding="utf-8")
    doc=(ROOT/"docs/SCH_BRASSICA_2017_MULTISTAGE_RECEIVER_ROLE_CONFLICT_V1.md").read_text(encoding="utf-8")
    sec=m.split("### 7.11 ",1)[1].split("## 8. Final causal identification layer",1)[0]
    for cue in (
        "Brassica rapa","phenylacetaldehyde","0.029","−0.17",
        "three","positive net seed-fitness selection","not a 27-test","no causal",
    ):
        assert cue.lower() in sec.lower()
    assert "Brassica" in fig
    for cue in ("18-test","neither an equivalence test","no significant","one source-backed"):
        assert cue.lower() in doc.lower()
