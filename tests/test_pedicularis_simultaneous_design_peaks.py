from __future__ import annotations

from copy import deepcopy
import math

import pytest

from scripts.infer_pedicularis_simultaneous_design_peaks import (
    SCHEMA, SYNTHETIC_SCHEMA, radius, simultaneous_from_fate_cell_means,
    synthetic_oracle, build,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    build as allocate, ALLOC_FIELDS,
)
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)


CURVES={
    "EXCLUDED":[4,6,8,10,14],
    "EXPOSED":[5,9,11,9,6],
}
K=25
ALPHA=.05


def _synthetic_interval_means(curves=CURVES):
    return {
        g:{z:(float(y),float(y)) for z,y in enumerate(curves[g])}
        for g in ("EXCLUDED","EXPOSED")
    }


def _oracle():
    return {
        "schema":SYNTHETIC_SCHEMA,
        "data_kind":"SYNTHETIC_ASSUMPTIONS_NOT_FIELD_DATA",
        "familywise_alpha":ALPHA,
        "global_potential_seed_cap":K,
        "assumed_complete_maturity_seed_means":deepcopy(CURVES),
        "candidate_batch_counts":[1,8,32,468,469,1872,1873,7490],
        "max_batches_to_examine":12000,
    }


def _source_packet(*, batches=2, missing=False):
    alloc,receipt=allocate(
        _manifest(batches),_settings(),
        allocation_seed="FROZEN_SIMULTANEOUS_HOEFFDING_DESIGN_20261014",
        g_exclusion_candidate_method="NONQUALIFIED_G_EXCLUSION",
        g_exposed_sham_candidate_method="NONQUALIFIED_G_EXPOSED_SHAM",
    )
    rows=[]
    for v in alloc:
        rank=int(v["assigned_z_rank"])
        count=CURVES[v["predator_treatment"]][rank]
        rows.append({
            **{key:v[key] for key in ALLOC_FIELDS},
            "fate_status":"MATURE_COUNTED",
            "intact_seeds":str(count),
            "damaged_seeds":"0",
            "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
            "viable_lower":"",
            "viable_upper":"",
            "seed_potential_upper":str(K),
            "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
            "zero_fate_proof":"",
            "partial_interval_proof":"",
        })
    if missing:
        target=next(v for v in rows if v["assigned_z_rank"]=="4"
                    and v["predator_treatment"]=="EXPOSED")
        target.update(
            fate_status="FATE_UNOBSERVED",
            intact_seeds="",damaged_seeds="",seed_stage_proof="",
        )
    return rows,receipt


def test_simultaneous_union_bound_uses_independent_batches_not_flowers():
    for B in (1,2,32,100,469,1873):
        eps=radius(n_independent_batches=B,
                   global_potential_seed_cap=K,alpha=ALPHA)
        assert eps==pytest.approx(K*math.sqrt(math.log(400)/(2*B)))
        assert 20*math.exp(-2*B*eps*eps/(K*K))==pytest.approx(ALPHA)
    result=simultaneous_from_fate_cell_means(
        _synthetic_interval_means(),
        n_independent_batches=32,
        global_potential_seed_cap=K,alpha=ALPHA,
    )
    assert result["n_eligible_plants_in_design"]==320
    assert result["n_fruit_observations_per_G_z_cell"]==64
    assert result["per_cell_Hoeffding_halfwidth_before_clipping"]==pytest.approx(
        7.6492,abs=.0002
    )
    assert result["n_independent_patch_stage_assignment_batches"]==32
    assert result["n_familywise_two_sided_bounds"]==20
    assert result["positive_shift_certified"] is False
    assert result["state_peak_confidence_sets"]["EXCLUDED"][
        "possible_peak_ranks"
    ]==[0,1,2,3,4]
    assert result["state_peak_confidence_sets"]["EXPOSED"][
        "possible_peak_ranks"
    ]==[0,1,2,3,4]


def test_oracle_optimistic_peak_certification_requires_hundreds_of_batches():
    r=synthetic_oracle(_oracle())
    assert r["status"]==(
        "SYNTHETIC_HOEFFDING_SAMPLE_REQUIREMENT_NOT_P_REX_RECOMMENDATION"
    )
    a=r["idealized_certification_thresholds"]
    assert a["positive_shift_certified"][
        "oracle_source_means_equal_to_observed_cell_means"
    ]["first_batch_count"]==469
    assert a["positive_shift_certified"][
        "sufficient_for_probability_at_least_1_minus_alpha"
    ]["first_batch_count"]==1873
    assert a["both_state_peaks_unique"][
        "oracle_source_means_equal_to_observed_cell_means"
    ]["first_batch_count"]==1873
    assert a["both_state_peaks_unique"][
        "sufficient_for_probability_at_least_1_minus_alpha"
    ]["first_batch_count"]==7490
    assert r["per_candidate_batch"]["468"]["positive_shift_certified"] is False
    assert r["per_candidate_batch"]["469"]["positive_shift_certified"] is True
    assert r["per_candidate_batch"]["1872"]["both_state_peaks_unique"] is False
    assert r["per_candidate_batch"]["1873"]["both_state_peaks_unique"] is True
    assert r["no_real_P_rex_recruitment_requirement_estimated"] is True


def test_source_locked_actual_candidate_assigned_fruits_are_not_population_inference():
    rows,receipt=_source_packet(batches=2)
    out=build(rows,receipt,alpha=.05,global_potential_seed_cap=K)
    assert out["receipt_schema"]==SCHEMA
    assert out["status"]==(
        "CONDITIONAL_NONASYMPTOTIC_JOINT_PEAK_SET_NOT_FIELD_QUALIFIED"
    )
    assert out["population_id"]=="SYNTHETIC_P_REX"
    assert out["design_randomization_simultaneous_inference"][
        "n_independent_patch_stage_assignment_batches"
    ]==2
    assert out["design_randomization_simultaneous_inference"][
        "positive_shift_certified"
    ] is False
    assert out["descriptive_finite_allocation_peak_sets"][
        "EXCLUDED"
    ]["possible_discrete_optimum_ranks"]==[4]
    assert out["descriptive_finite_allocation_peak_sets"][
        "EXPOSED"
    ]["possible_discrete_optimum_ranks"]==[2]
    assert out["field_independence_of_batch_randomization_authenticated"] is False
    assert out["all_potential_seed_outcomes_proven_bounded_by_input_K"] is False
    assert "confidence_covers_design_expectations_of_fixed_eligible_cohort_not_landscape_population" in (
        out["claim_ceiling"]
    )


def test_missing_maturity_fate_is_never_imputed_and_only_widens_confidence():
    complete,receipt=_source_packet(batches=2)
    loss,_=_source_packet(batches=2,missing=True)
    good=build(complete,receipt,global_potential_seed_cap=K)
    missing=build(loss,receipt,global_potential_seed_cap=K)
    a=good["design_randomization_simultaneous_inference"][
        "simultaneous_interval_endpoints_by_G_z"
    ]["EXPOSED"]["4"]
    b=missing["design_randomization_simultaneous_inference"][
        "simultaneous_interval_endpoints_by_G_z"
    ]["EXPOSED"]["4"]
    assert missing["n_source_fate_missing"]==1
    assert b[0] <= a[0]
    assert b[1] >= a[1]
    assert missing["source_outcomes_sha256"]!=good["source_outcomes_sha256"]


def test_fake_upper_cap_or_missing_allocated_flower_fails_before_inference():
    rows,receipt=_source_packet()
    with pytest.raises(ValueError,match="global seed bound"):
        build(rows,receipt,global_potential_seed_cap=20)
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(rows[:-1],receipt,global_potential_seed_cap=K)
    tampered=deepcopy(rows)
    tampered[0]["predator_treatment"]=(
        "EXPOSED" if tampered[0]["predator_treatment"]=="EXCLUDED" else "EXCLUDED"
    )
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(tampered,receipt,global_potential_seed_cap=K)


def test_no_real_shift_cannot_be_certified_by_shrinking_intervals():
    same={"EXCLUDED":[5,9,11,9,6],"EXPOSED":[5,9,11,9,6]}
    means=_synthetic_interval_means(same)
    for B in (1,32,1000,100000):
        r=simultaneous_from_fate_cell_means(
            means,n_independent_batches=B,
            global_potential_seed_cap=K,alpha=.05,
        )
        assert not r["positive_shift_certified"]
        assert not r["negative_shift_certified"]
        assert r["possible_zero_shift"]


@pytest.mark.parametrize("bad",[
    {"familywise_alpha":0},
    {"global_potential_seed_cap":0},
    {"data_kind":"REAL_FIELD_DATA"},
    {"assumed_complete_maturity_seed_means":{
        "EXCLUDED":[1,2],"EXPOSED":[1,2]
    }},
    {"candidate_batch_counts":[1,1]},
    {"max_batches_to_examine":-1},
])
def test_oracle_rejects_fabricated_field_or_broken_parameter_declarations(bad):
    config=_oracle()
    config.update(bad)
    with pytest.raises(ValueError):
        synthetic_oracle(config)


def test_missing_or_invalid_per_cell_values_fail_closed():
    curves=_synthetic_interval_means()
    curves["EXCLUDED"].pop(3)
    with pytest.raises(ValueError,match="five distinct"):
        simultaneous_from_fate_cell_means(
            curves,n_independent_batches=4,
            global_potential_seed_cap=K
        )
    curves=_synthetic_interval_means()
    curves["EXCLUDED"][3]=(14,8)
    with pytest.raises(ValueError,match="outside seed potential cap"):
        simultaneous_from_fate_cell_means(
            curves,n_independent_batches=4,
            global_potential_seed_cap=K
        )
    with pytest.raises(ValueError,match="independent batches"):
        radius(n_independent_batches=0,global_potential_seed_cap=K,alpha=.05)
    with pytest.raises(ValueError,match="alpha"):
        radius(n_independent_batches=10,global_potential_seed_cap=K,alpha=1.)
