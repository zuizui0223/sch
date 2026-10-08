from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.bound_pedicularis_fruit_fate_selection import (
    REQUIRED_FIELDS, _interpret, build, read,
)
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS, RECEIPT_SCHEMA, RECEIPT_STATUS,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256


def _fixture():
    rows = []
    for plant in ("PLANT_A", "PLANT_B"):
        for z in range(5):
            for g in ("EXCLUDED", "EXPOSED"):
                row = {
                    "population_id": "SYNTHETIC_P_REX",
                    "season_id": "SYNTHETIC_YEAR",
                    "plant_id": plant,
                    "flower_id": f"{plant}_Z{z}_{g}",
                    "assigned_z_level": f"Z{z}",
                    "assigned_z_rank": str(z),
                    "manipulation_setting_id": f"SETTING_{z}",
                    "sham_control": "0",
                    "pollination_treatment": "NATURAL",
                    "predator_treatment": g,
                    "exclusion_method": ("EXCLUSION" if g=="EXCLUDED" else "SHAM"),
                    "fate_status": "MATURE_COUNTED",
                    "intact_seeds": "3",
                    "damaged_seeds": "0",
                    "seed_stage_proof": "COMPLETE_COUNTED_SEED_FATES",
                    "viable_lower": "",
                    "viable_upper": "",
                    "seed_potential_upper": "10",
                    "seed_potential_upper_basis": "PROSPECTIVELY_FROZEN_UPPER_BOUND",
                    "zero_fate_proof": "",
                    "partial_interval_proof": "",
                }
                if z==0 and plant=="PLANT_A":
                    row["intact_seeds"]="2" if g=="EXCLUDED" else "3"
                if z==0 and plant=="PLANT_B":
                    row.update(
                        fate_status="ZERO_VIABLE_VERIFIED",
                        intact_seeds="0",damaged_seeds="",seed_stage_proof="",
                        zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL",
                    )
                if z==4 and plant=="PLANT_A":
                    row["intact_seeds"]="7" if g=="EXCLUDED" else "1"
                if z==4 and plant=="PLANT_B":
                    row.update(
                        fate_status="FATE_UNOBSERVED",
                        intact_seeds="",damaged_seeds="",seed_stage_proof="",
                        seed_potential_upper=("4" if g=="EXCLUDED" else "3")
                    )
                rows.append(row)
    frozen = sorted(
        [{field: row[field] for field in FROZEN_FIELDS} for row in rows],
        key=lambda x:(x["plant_id"],x["flower_id"])
    )
    allocation = {
        "receipt_schema": RECEIPT_SCHEMA,
        "status": RECEIPT_STATUS,
        "cohort_role": "TWO_COHORT_FRUIT",
        "pollination_treatment": "NATURAL",
        "population_id": "SYNTHETIC_P_REX",
        "season_id": "SYNTHETIC_YEAR",
        "n_z_levels": 5,
        "n_allocated_flowers": len(rows),
        "expected_frozen_rows": frozen,
        "allocation_identity_sha256": _semantic_sha256(frozen),
    }
    return rows,allocation


def _cell(receipt,g,z):
    return receipt["mean_fitness_by_predator_treatment_and_z"][g][str(z)]


def test_primary_fitness_and_optimum_shift_survive_unknown_fruit_fates():
    rows,allocation = _fixture()
    result = build(rows,allocation)
    assert result["status"] == "NON_GATING_FINITE_ASSIGNED_FRUIT_FATE_BOUNDS"
    assert result["n_all_allocated_flowers"] == 20
    assert result["n_independent_plant_blocks"] == 2
    assert result["fate_status_counts"] == {
        "FATE_UNOBSERVED":2,
        "MATURE_COUNTED":16,
        "PARTIALLY_CENSORED":0,
        "ZERO_VIABLE_VERIFIED":2,
    }
    assert _cell(result,"EXCLUDED", "4")["mean_viable_seeds_per_flower_bounds"] == [
        {"exact":"7/2","value":3.5},
        {"exact":"11/2","value":5.5},
    ]
    zero = _cell(result,"EXCLUDED","0")
    assert zero["n_verified_zero_mature_yield"] == 1
    assert zero["n_stage_predation_q_unknown"] == 1
    assert zero["n_exact_mature_fitness"] == 2
    assert result["extreme_z_fitness_selection_contrasts"]["EXCLUDED"][
        "direction"
    ] == "POSITIVE_IN_EVERY_FATE_COMPLETION"
    assert result["extreme_z_fitness_selection_contrasts"]["EXPOSED"][
        "direction"
    ] == "SIGN_UNRESOLVED_UNDER_FATE_CENSORING"
    assert result["predator_state_possible_optimum_ranks"]["EXCLUDED"] == {
        "possible_discrete_optimum_ranks":[4],
        "guaranteed_unique_discrete_optimum_rank":4,
        "rank_optimum_claim_only_conditional_on_independently_feasible_cell_bounds":True,
    }
    assert result["predator_state_possible_optimum_ranks"]["EXPOSED"][
        "possible_discrete_optimum_ranks"
    ] == [1,2,3]
    assert result["excluded_minus_exposed_optimum_rank_shift_outer_bound"] == [1,3]
    assert result["optimum_shift_guaranteed_positive_given_bounds"] is True
    assert "separate_two_cohort_exploratory_lane_not_primary_W1_W2" in result["claim_ceiling"]


def test_partial_censored_surviving_seed_bounds_are_not_replaced_with_zero():
    rows,allocation=_fixture()
    row = next(r for r in rows
               if r["flower_id"]=="PLANT_B_Z4_EXCLUDED")
    row.update(fate_status="PARTIALLY_CENSORED",viable_lower="1",viable_upper="2",
               partial_interval_proof="DOCUMENTED_INTACT_LOWER_AND_POTENTIAL_SEED_UPPER")
    result=build(rows,allocation)
    assert result["fate_status_counts"]["PARTIALLY_CENSORED"]==1
    assert result["fate_status_counts"]["FATE_UNOBSERVED"]==1
    assert [v["exact"] for v in _cell(result,"EXCLUDED","4")[
        "mean_viable_seeds_per_flower_bounds"
    ]] == ["4","9/2"]


def test_known_zero_yield_does_not_identify_predation():
    rows,_ = _fixture()
    zero=next(r for r in rows if r["fate_status"]=="ZERO_VIABLE_VERIFIED")
    classification=_interpret(zero)
    assert classification["seed_fitness_lower"] == 0
    assert classification["seed_fitness_upper"] == 0
    assert classification["predation_q_identified_from_stage_counts"] is False
    counted=next(r for r in rows if r["fate_status"]=="MATURE_COUNTED")
    assert _interpret(counted)["predation_q_identified_from_stage_counts"] is True
    counted["intact_seeds"]="0"
    counted["damaged_seeds"]="0"
    assert _interpret(counted)["predation_q_identified_from_stage_counts"] is False


def test_fully_unobserved_fate_can_make_trait_direction_indeterminate():
    rows,allocation = _fixture()
    for row in rows:
        if row["predator_treatment"]=="EXCLUDED" and row["assigned_z_rank"]=="4":
            row.update(fate_status="FATE_UNOBSERVED",intact_seeds="",
                       damaged_seeds="",seed_stage_proof="",
                       seed_potential_upper="10")
    result=build(rows,allocation)
    assert result["extreme_z_fitness_selection_contrasts"]["EXCLUDED"][
        "direction"
    ] == "SIGN_UNRESOLVED_UNDER_FATE_CENSORING"
    assert result["predator_state_possible_optimum_ranks"]["EXCLUDED"][
        "guaranteed_unique_discrete_optimum_rank"
    ] is None
    assert result["optimum_shift_guaranteed_positive_given_bounds"] is False


@pytest.mark.parametrize(("mutate","error"), [
    (lambda r:r.update(fate_status="UNKNOWN"),"unrecognized fruit fate"),
    (lambda r:r.update(seed_potential_upper=""),"missing required"),
    (lambda r:r.update(seed_potential_upper="10.0"),"nonnegative integer"),
    (lambda r:r.update(intact_seeds="12"),"integer intact"),
    (lambda r:r.update(damaged_seeds="10"),"damaged\\+intact"),
    (lambda r:r.update(seed_stage_proof="UNKNOWN"),"unknown stage fate"),
    (lambda r:r.update(seed_potential_upper_basis="UNVERIFIED"),"positive prospective provenance"),
])
def test_counted_fate_rejects_false_data(mutate,error):
    rows,allocation=_fixture()
    target=next(r for r in rows if r["fate_status"]=="MATURE_COUNTED")
    mutate(target)
    with pytest.raises(ValueError,match=error):
        build(rows,allocation)


@pytest.mark.parametrize(("mutate","error"), [
    (lambda r:r.update(zero_fate_proof=""),"pre-dispersal outcome proof"),
    (lambda r:r.update(zero_fate_proof="SEEDS_DISPERSED"),"pre-dispersal outcome proof"),
    (lambda r:r.update(damaged_seeds="3"),"no inferred initiation"),
    (lambda r:r.update(intact_seeds="1"),"no inferred initiation"),
])
def test_confirmed_zero_requires_independently_coded_pre_disperal_evidence(mutate,error):
    rows,allocation=_fixture()
    target=next(r for r in rows if r["fate_status"]=="ZERO_VIABLE_VERIFIED")
    mutate(target)
    with pytest.raises(ValueError,match=error):
        build(rows,allocation)


@pytest.mark.parametrize(("mutate","error"),[
    (lambda r:r.update(intact_seeds="0"),"cannot be recoded as zero"),
    (lambda r:r.update(viable_upper="0"),"cannot be recoded as zero"),
    (lambda r:r.update(zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL"),"cannot be recoded as zero"),
])
def test_missing_fate_is_not_automatically_zero(mutate,error):
    rows,allocation=_fixture()
    target=next(r for r in rows if r["fate_status"]=="FATE_UNOBSERVED")
    mutate(target)
    with pytest.raises(ValueError,match=error):
        build(rows,allocation)


def test_undeclared_partial_bounds_fail_closed():
    rows,allocation=_fixture()
    target=next(r for r in rows if r["fate_status"]=="FATE_UNOBSERVED")
    target.update(fate_status="PARTIALLY_CENSORED",viable_lower="1",viable_upper="2")
    with pytest.raises(ValueError,match="independently documented"):
        build(rows,allocation)
    target["partial_interval_proof"]="DOCUMENTED_INTACT_LOWER_AND_POTENTIAL_SEED_UPPER"
    target["viable_upper"]="9"
    with pytest.raises(ValueError,match="independently documented"):
        build(rows,allocation)


def test_omitted_or_swapped_randomized_flower_cannot_distort_fitness():
    rows,allocation=_fixture()
    with pytest.raises(ValueError,match="exact allocated"):
        build(rows[:-1],allocation)
    rows2=deepcopy(rows)
    rows2[0]["predator_treatment"]="EXPOSED"
    with pytest.raises(ValueError,match="exact allocated"):
        build(rows2,allocation)
    rows3=deepcopy(rows)
    rows3[0]["flower_id"]=rows3[1]["flower_id"]
    with pytest.raises(ValueError,match="duplicate"):
        build(rows3,allocation)


def test_provenance_is_not_claimed_causal_qualification():
    rows,allocation=_fixture()
    allocation["status"]="DESCRIPTIVE_ONLY"
    with pytest.raises(ValueError,match="frozen nonconfirmatory"):
        build(rows,allocation)


def test_csv_reader_preserves_incomplete_rows_and_cli_required_fields(tmp_path:Path):
    rows,allocation=_fixture()
    p=tmp_path/"fruit_fate.csv"
    with p.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    out=build(read(p),allocation)
    assert out["n_all_allocated_flowers"]==len(rows)
    with p.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["flower_id"])
        writer.writeheader()
        writer.writerows([{"flower_id":"f1"}])
    with pytest.raises(ValueError,match="missing source or fate"):
        read(p)
