"""Guard authentic JPE source identity, original cohort and separated NB2 claims."""
from pathlib import Path
from scripts.analyze_sch_milkweed_2024_nb2_two_part import (
    DOI,SOURCE_SHA256,N,N_LABELS,N_TRAITS,SEED,BOOT,ALPHA_GRID
)

def test_source_identity_and_registered_alpha_sensitivity():
    assert DOI=="10.26786/1920-7603(2024)758"
    assert SOURCE_SHA256=="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
    assert (N,N_LABELS,N_TRAITS)==(103,102,10)
    assert SEED==20261117
    assert BOOT==499
    assert ALPHA_GRID==(.25,.5,1.0,2.0)

def test_joint_source_plant_labels_and_noncausal_hurdle_limitation():
    s=Path("scripts/analyze_sch_milkweed_2024_nb2_two_part.py").read_text(encoding="utf-8")
    for item in (
        "block[pid][:p]+=scoreF[i]",
        "block[pid][p:]+=scoreI[i]",
        "L@cov@L.T",
        "np.log(total)",
        "math.log(10)",
        "family=sm.families.NegativeBinomial(alpha=alpha)",
        '"positive_only_NB_regression_is_working_conditional_mean_not_truncated_NB_hurdle_likelihood"',
        '"no_causal_reproductive_component_difference_or_sch_L":True',
    ):
        assert item in s
