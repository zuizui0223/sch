"""Guard authentic JPE source identity, original cohort and separated NB2 claims."""
from pathlib import Path
import pytest
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


def test_source_actual_ten_trait_NB2_results_are_frozen_with_correct_cluster_unit():
    import csv
    from pathlib import Path
    with Path("data/SCH_MILKWEED_2024_NB2_TWO_PART_RESULTS_V1.csv").open(
            encoding="utf-8",newline="") as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==10
    assert len({r["trait"] for r in rows})==10
    assert all(r["source_doi"]==DOI for r in rows)
    assert all(r["original_xlsx_sha256"]==SOURCE_SHA256 for r in rows)
    assert all(r["n_source_rows"]=="103" and r["n_plant_ID_labels"]=="102"
               for r in rows)
    r=next(x for x in rows if x["trait"]=="Inflorescence number")
    assert float(r["working_nb2_alpha_fruit"])==pytest.approx(.439880208744,abs=1e-9)
    assert float(r["working_nb2_alpha_insertion"])==pytest.approx(.378091895863,abs=1e-9)
    assert float(r["fruit_minus_insertion_log_rate_delta"])==pytest.approx(.089064600259,abs=1e-9)
    assert float(r["two_sided_nominal_P"])==pytest.approx(.612810090462,abs=1e-9)
    assert float(r["normal95_lower"])<0<float(r["normal95_upper"])


def test_ecological_claim_ceiling_and_observation_units_stay_explicit():
    from pathlib import Path
    s=Path("docs/SCH_MILKWEED_2024_NB2_TWO_PART_RATE_V1.md").read_text(
        encoding="utf-8").lower().replace("*","")
    for term in ("103", "102", "40 stems", "63 stems", "0.61281",
                 "0.42390", "0.000269", "0.67228", "0.85279",
                 "not a properly normalized", "not establish an allocation trade-off",
                 "same individual flower", "not equivalence"):
        assert term.lower() in s
