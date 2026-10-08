from __future__ import annotations

from copy import deepcopy
from fractions import Fraction

import pytest

from scripts.prioritize_pedicularis_optimum_shift_remeasurement import (
    _original_means, _shift, build, outcome_ranges,
)
from scripts.bound_pedicularis_fruit_fate_selection import build as fate_build
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS, RECEIPT_SCHEMA, RECEIPT_STATUS,
)


def _packet(exposed_high_known: int = 3, exposed_missing_cap: int = 8):
    rows = []
    for plant in ("A", "B"):
        for rank in range(5):
            for g in ("EXCLUDED", "EXPOSED"):
                row = {
                    "population_id": "SYNTHETIC_P_REX",
                    "season_id": "SYNTHETIC",
                    "plant_id": plant,
                    "flower_id": f"{plant}_Z{rank}_{g}",
                    "assigned_z_level": f"Z{rank}",
                    "assigned_z_rank": str(rank),
                    "manipulation_setting_id": f"MANIP_{rank}",
                    "sham_control": "0",
                    "pollination_treatment": "NATURAL",
                    "predator_treatment": g,
                    "exclusion_method": "BARRIER" if g=="EXCLUDED" else "SHAM",
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
                if rank == 0 and plant == "A":
                    row["intact_seeds"] = "2" if g=="EXCLUDED" else "3"
                if rank == 0 and plant == "B":
                    row.update(
                        fate_status="ZERO_VIABLE_VERIFIED",
                        intact_seeds="0",damaged_seeds="",seed_stage_proof="",
                        zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL"
                    )
                if rank == 4 and plant == "A":
                    row["intact_seeds"] = (
                        "7" if g=="EXCLUDED" else str(exposed_high_known)
                    )
                if rank == 4 and plant == "B":
                    row.update(
                        fate_status="FATE_UNOBSERVED",
                        intact_seeds="",damaged_seeds="",seed_stage_proof="",
                        seed_potential_upper=(
                            "4" if g=="EXCLUDED" else str(exposed_missing_cap)
                        ),
                    )
                rows.append(row)
    frozen = sorted(
        [{key:row[key] for key in FROZEN_FIELDS} for row in rows],
        key=lambda row: (row["plant_id"],row["flower_id"])
    )
    allocation={
        "receipt_schema": RECEIPT_SCHEMA,
        "status": RECEIPT_STATUS,
        "cohort_role": "TWO_COHORT_FRUIT",
        "pollination_treatment": "NATURAL",
        "population_id": "SYNTHETIC_P_REX",
        "season_id": "SYNTHETIC",
        "n_z_levels": 5,
        "n_allocated_flowers": len(rows),
        "expected_frozen_rows": frozen,
        "allocation_identity_sha256": _semantic_sha256(frozen),
    }
    return rows, allocation


def _measured_packet(rows, flower_id, x):
    full=deepcopy(rows)
    row=next(row for row in full if row["flower_id"]==flower_id)
    row.update(
        fate_status="MATURE_COUNTED",
        intact_seeds=str(x),
        damaged_seeds="",
        seed_stage_proof="",
    )
    return full


def _find_segment(segments, x):
    found=[
        segment for segment in segments
        if segment["minimum_viable_seeds_if_observed"]
        <= x <= segment["maximum_viable_seeds_if_observed"]
    ]
    assert len(found)==1
    return found[0]


def _expected_from_fate_receipt(receipt):
    ex=receipt["predator_state_possible_optimum_ranks"]["EXCLUDED"][
        "possible_discrete_optimum_ranks"
    ]
    ep=receipt["predator_state_possible_optimum_ranks"]["EXPOSED"][
        "possible_discrete_optimum_ranks"
    ]
    return {
        "excluded": ex, "exposed": ep,
        "outer": [min(ex)-max(ep),max(ex)-min(ep)],
    }


def test_one_missing_fruit_has_three_distinct_exact_optimum_shift_regimes():
    rows, allocation=_packet()
    out=build(rows,allocation)
    assert out["status"]=="NON_GATING_FINITE_SAMPLE_OPTIMUM_SHIFT_TIPPING_V1"
    assert out["n_original_allocated_flowers"]==20
    assert out["n_currently_uncertain_fruits"]==2
    assert out["baseline"]["classification"]=="NONNEGATIVE_SHIFT_ZERO_STILL_POSSIBLE"
    assert out["baseline"]["excluded_minus_exposed_rank_shift_outer_interval"]==[0,3]
    top=out["prioritized_missing_fruit_optimum_shift_assessments"][0]
    assert top["flower_id"]=="B_Z4_EXPOSED"
    assert top["unobserved_viable_seed_count_interval"]==[0,8]
    assert top["some_single_fruit_outcome_newly_identifies_shift"] is True
    segments=top["integer_outcome_ranges_after_exact_one_fruit_ascertainment"]
    assert [
        (s["minimum_viable_seeds_if_observed"],
         s["maximum_viable_seeds_if_observed"],
         s["classification"]) for s in segments
    ]==[
        (0,2,"GUARANTEED_POSITIVE_EXCLUSION_SHIFT"),
        (3,3,"NONNEGATIVE_SHIFT_ZERO_STILL_POSSIBLE"),
        (4,8,"GUARANTEED_ZERO_EXCLUSION_SHIFT"),
    ]
    assert top["n_integer_outcomes_that_newly_certify_shift_or_zero"]==8
    # These are eight possible integers, NOT an estimated 8/9 probability.
    assert top["total_integer_outcome_values_not_a_probability"]==9
    assert out["one_fruit_integer_outcome_ranges_are_not_probabilities"] is True
    other=out["prioritized_missing_fruit_optimum_shift_assessments"][1]
    assert other["flower_id"]=="B_Z4_EXCLUDED"
    assert other["some_single_fruit_outcome_newly_identifies_shift"] is False


def test_segment_boundaries_match_independent_full_fate_refit_at_every_x():
    rows, allocation=_packet()
    out=build(rows,allocation)
    for item in out["prioritized_missing_fruit_optimum_shift_assessments"]:
        a,b=item["unobserved_viable_seed_count_interval"]
        for x in range(a,b+1):
            segment=_find_segment(
                item["integer_outcome_ranges_after_exact_one_fruit_ascertainment"],x
            )
            completed=fate_build(_measured_packet(rows,item["flower_id"],x),allocation)
            truth=_expected_from_fate_receipt(completed)
            assert segment["excluded"]["possible_optimum_ranks"]==truth["excluded"]
            assert segment["exposed"]["possible_optimum_ranks"]==truth["exposed"]
            assert segment["excluded_minus_exposed_rank_shift_outer_interval"]==truth["outer"]


def test_preexisting_positive_shift_is_not_misclassified_as_new_information():
    rows,allocation=_packet(exposed_high_known=1,exposed_missing_cap=3)
    result=build(rows,allocation)
    assert result["baseline"]["classification"]=="GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    assert result["baseline"]["excluded_minus_exposed_rank_shift_outer_interval"]==[1,3]
    assert all(
        not item["some_single_fruit_outcome_newly_identifies_shift"]
        for item in result["prioritized_missing_fruit_optimum_shift_assessments"]
    )


def test_exact_breakpoints_do_not_enumerate_million_integer_fates():
    vals={
        "EXCLUDED":{i:(Fraction(3),Fraction(3)) for i in range(5)},
        "EXPOSED":{i:(Fraction(3),Fraction(3)) for i in range(5)},
    }
    vals["EXCLUDED"][4]=(Fraction(10),Fraction(10))
    vals["EXPOSED"][4]=(Fraction(0),Fraction(1000000))
    ranges=outcome_ranges(
        source_means=vals,target_g="EXPOSED",target_rank=4,
        n_fruits_in_cell=1,viable_lower=0,viable_upper=1000000
    )
    assert sum(x["n_integer_outcome_values"] for x in ranges)==1000001
    assert len(ranges)<=4
    assert _find_segment(ranges,2)["classification"]=="GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    assert _find_segment(ranges,3)["classification"]=="NONNEGATIVE_SHIFT_ZERO_STILL_POSSIBLE"
    assert _find_segment(ranges,11)["classification"]=="GUARANTEED_ZERO_EXCLUSION_SHIFT"


def test_fail_closed_for_bad_fate_or_corrupted_frozen_allocation():
    rows,allocation=_packet()
    with pytest.raises(ValueError,match="exact allocated"):
        build(rows[:-1],allocation)
    bad=deepcopy(rows)
    bad[0]["assigned_z_rank"]="4"
    with pytest.raises(ValueError,match="exact allocated"):
        build(bad,allocation)
    bad=deepcopy(rows)
    broken=next(x for x in bad if x["flower_id"]=="B_Z4_EXPOSED")
    broken["intact_seeds"]="0"
    with pytest.raises(ValueError,match="cannot be recoded as zero"):
        build(bad,allocation)
    means=_original_means(fate_build(rows,allocation))
    with pytest.raises(ValueError,match="invalid single-fruit"):
        outcome_ranges(
            source_means=means,target_g="EXPOSED",target_rank=4,
            n_fruits_in_cell=0,viable_lower=0,viable_upper=8
        )
