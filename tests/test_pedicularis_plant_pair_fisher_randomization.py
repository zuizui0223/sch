from __future__ import annotations

from copy import deepcopy
from fractions import Fraction

import pytest

from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    _pairs, _p_from_stats, build, fisher_from_pairs, statistic,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    build as allocate, ALLOC_FIELDS,
)
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)


def _packet(n_batches=1, *, kind="SHARP_NULL"):
    manifest=_manifest(n_batches)
    assignment,receipt=allocate(
        manifest,_settings(),
        allocation_seed="FROZEN_PROSPECTIVE_PAIR_TEST_LONG_SEED_20261009",
        g_exclusion_candidate_method="CANDIDATE_G_EXCLUSION_UNQUALIFIED",
        g_exposed_sham_candidate_method="CANDIDATE_G_EXPOSED_SHAM",
    )
    rows=[]
    for row in assignment:
        z=int(row["assigned_z_rank"])
        plant=int(row["plant_id"].split("PLANT")[1])
        if kind=="SHARP_NULL":
            # Each plant's two measured seed counts are functions of plant
            # identity and z but NOT G; under Fisher H0 the outcomes are
            # invariant to all plant-level G swaps.
            y=3+plant%5 + 2*z
        elif kind=="ALL_EQUAL":
            y=6
        elif kind=="POSITIVE_SHIFT":
            y=(
                [2,4,6,10,20][z] if row["predator_treatment"]=="EXCLUDED"
                else [2,6,16,6,1][z]
            )
        else:
            raise ValueError("unrecognized test DGP")
        rows.append({
            **{key:row[key] for key in ALLOC_FIELDS},
            "fate_status":"MATURE_COUNTED",
            "intact_seeds":str(y),
            "damaged_seeds":"0",
            "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
            "viable_lower":"",
            "viable_upper":"",
            "seed_potential_upper":"30",
            "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
            "zero_fate_proof":"",
            "partial_interval_proof":"",
        })
    return rows,receipt


def test_one_stratum_enumerates_exactly_32_matched_plant_G_assignments():
    rows,receipt=_packet(kind="POSITIVE_SHIFT")
    result=build(rows,receipt)
    assert result["status"]=="NON_GATING_SHARP_NULL_CONDITIONAL_RANDOMIZATION_ONLY"
    assert result["n_matched_plant_pairs"]==5
    assert result["n_parent_plants"]==10
    assert result["n_fruit_flowers"]==20
    assert result["p_calculation"]=="EXACT_CONDITIONAL_ENUMERATION"
    assert result["n_randomization_statistics"]==32
    assert result["observed_peak_shift_direction"]=="POSITIVE"
    assert result["observed_predeclared_peak_statistic"][
        "exclusion_minus_exposure_peak_midrank"
    ]==pytest.approx(2)
    # P is an exact lattice probability, not a claim of significance
    # without checking the actual known sharp null and field G validity.
    assert 0<=result["one_sided_Fisher_sharp_null_p"]<=1
    assert (
        result["one_sided_Fisher_sharp_null_p"]*32
    )==pytest.approx(round(result["one_sided_Fisher_sharp_null_p"]*32))
    assert result["valid_weak_null_of_zero_optimum_shift_test"] is False
    assert result["observed_field_data_independently_verified"] is False


def test_every_null_assignment_yields_superuniform_exact_fisher_p_values():
    rows,receipt=_packet(kind="SHARP_NULL")
    pairs=_pairs(rows,receipt)
    assert len(pairs)==5
    stats=[statistic(pairs,mask)["exclusion_minus_exposure_peak_midrank"]
           for mask in range(32)]
    pvalues=[
        _p_from_stats(t,stats,exact=True)["one_sided_Fisher_sharp_null_p"]
        for t in stats
    ]
    # Conditional on the edge pairs and all potential outcomes under
    # the SHARP G-null, all 2^5 assignments are equally likely.
    for alpha in (0.01,0.05,0.10,0.20,0.50,1.0):
        assert sum(p<=alpha+1e-12 for p in pvalues)/32 <= alpha+1e-12
    assert len(pvalues)==32


def test_permutation_swaps_both_flower_outcomes_of_parent_together():
    rows,receipt=_packet(kind="SHARP_NULL")
    pairs=_pairs(rows,receipt)
    first=pairs[0]
    a,b=first["excluded"],first["exposed"]
    flipped_first=deepcopy(pairs)
    flipped_first[0]["excluded"],flipped_first[0]["exposed"]=b,a
    assert statistic(pairs,1)==statistic(flipped_first,0)
    assert set(a["by_z"])==set(b["by_z"])=={
        first["edge"],(first["edge"]+1)%5
    }
    assert a["plant_id"]!=b["plant_id"]


def test_all_equal_seed_counts_cannot_generate_false_positive_shift():
    rows,receipt=_packet(kind="ALL_EQUAL")
    result=build(rows,receipt)
    assert result["observed_peak_shift_direction"]=="ZERO_OR_TIED_MIDRANK"
    assert result["one_sided_Fisher_sharp_null_p"]==1.0


def test_four_batch_monte_carlo_is_reproducible_and_uses_plus_one_correction():
    rows,receipt=_packet(n_batches=4,kind="POSITIVE_SHIFT")
    a=build(rows,receipt,monte_carlo_permutations=999,random_seed=13579)
    b=build(list(reversed(rows)),receipt,
            monte_carlo_permutations=999,random_seed=13579)
    assert a["n_matched_plant_pairs"]==20
    assert a["n_parent_plants"]==40
    assert a["n_fruit_flowers"]==80
    assert a["p_calculation"]=="MONTE_CARLO_PLUS_ONE_INCLUDE_OBSERVED_REFERENCE"
    assert a["n_randomization_statistics"]==999
    assert a["one_sided_Fisher_sharp_null_p"]==b["one_sided_Fisher_sharp_null_p"]
    assert a["one_sided_Fisher_sharp_null_p"]>=1/1000
    assert (
        1000*a["one_sided_Fisher_sharp_null_p"]
    )==pytest.approx(round(1000*a["one_sided_Fisher_sharp_null_p"]))


def test_missing_maturity_output_never_fabricated_for_randomization():
    rows,receipt=_packet()
    missing=deepcopy(rows)
    missing[0].update(
        fate_status="FATE_UNOBSERVED",
        intact_seeds="",damaged_seeds="",seed_stage_proof="",
    )
    with pytest.raises(ValueError,match="exact mature seed output"):
        build(missing,receipt)
    zero=deepcopy(rows)
    zero[0].update(
        fate_status="ZERO_VIABLE_VERIFIED",
        intact_seeds="0",damaged_seeds="",seed_stage_proof="",
        zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL",
    )
    result=build(zero,receipt)
    assert result["n_randomization_statistics"]==32


def test_treatment_tampering_and_plant_split_cannot_pass_frozen_source_check():
    rows,receipt=_packet()
    corrupted=deepcopy(rows)
    corrupted[0]["predator_treatment"]=(
        "EXCLUDED" if corrupted[0]["predator_treatment"]=="EXPOSED"
        else "EXPOSED"
    )
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(corrupted,receipt)
    missing=deepcopy(rows[:-1])
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(missing,receipt)


@pytest.mark.parametrize("bad",[
    {"monte_carlo_permutations":10},
    {"random_seed":-1},
    {"exact_max_pairs":32},
])
def test_randomization_input_controls_fail_closed(bad):
    rows,receipt=_packet()
    pairs=_pairs(rows,receipt)
    with pytest.raises(ValueError):
        fisher_from_pairs(pairs,**bad)
