"""Only numerical/selection-software fixtures; no fabricated field outcomes."""
from __future__ import annotations

import pytest

from scripts.analyze_sch_ipomopsis_primary_coupling import (
    covariance, mean, stage_coupling, width_split_group,
    eligible_groups, analyze,
)


def test_exact_reproductive_stage_covariance_identity():
    # The numerical values are test fixtures, NEVER claimed as Ipomopsis.
    x=[1.,3.,5.]
    escape=[0.2,0.6,1.]
    assert mean(x)==3.
    assert mean(escape)==.6
    assert covariance(x,escape)==pytest.approx(.533333333333)
    c=[{"init":a,"escape":b,"width":w,"final":a}
       for a,b,w in zip(x,escape,[2.,3.,4.])]
    assert stage_coupling(c)==pytest.approx(.533333333333/3)
    assert stage_coupling(c,[1.,.6,.2])<0


def test_width_proxy_decomposition_is_algebraically_exact_even_with_coupling():
    rows=[
        {"init":10.,"escape":.2,"width":1.,"final":7.},
        {"init":20.,"escape":.8,"width":2.,"final":8.},
        {"init":30.,"escape":.9,"width":3.,"final":9.},
        {"init":40.,"escape":.1,"width":4.,"final":10.},
        {"init":50.,"escape":.9,"width":5.,"final":10.},
        {"init":60.,"escape":.2,"width":6.,"final":11.},
        {"init":70.,"escape":1.,"width":7.,"final":12.},
        {"init":80.,"escape":.8,"width":8.,"final":13.},
    ]
    split=width_split_group(rows)
    assert split is not None
    assert len(split["low"])==len(split["high"])==4
    assert split["width_median"]==4.5
    assert split["n_width_tied_dropped"]==0
    assert split["proxy_stage_response_high_minus_low"]==pytest.approx(
        split["independent_marginal_stage_prediction_delta"]+
        split["coupling_delta_high_minus_low"]
    )


def test_width_ties_do_not_get_randomized_into_fake_high_vs_low_treatment():
    rows=[{"init":float(i+1),"escape":.1*i,"width":2., "final":float(i)}
          for i in range(8)]
    assert width_split_group(rows) is None
    rows=[{"init":float(i+1),"escape":.1*i,
           "width":1. if i<4 else 3.,"final":float(i)} for i in range(8)]
    result=width_split_group(rows)
    assert result is not None
    assert result["n_width_tied_dropped"]==0


def test_incomplete_stage_data_never_coerced_to_zero_and_small_cohorts_excluded():
    def row(site,year,typ,i,e,width):
        return {"Site":site,"Year":year,"Type":typ,
                "seedsinit":i,"flyescape":e,"width":width,"seeds":"9"}
    rows=[row("agg","2017","A","12","0.8","3") for _ in range(8)]
    rows.extend([
        row("hyb","2014","H","10",".","3"),
        row("hyb","2014","H","10","0.4","3"),
    ])
    groups,excluded=eligible_groups(rows)
    assert len(groups)==1
    assert groups[0]["n"]==8
    assert excluded["incomplete_stage_pair"]==1
    assert excluded["in_small_group"]==1


def test_hypothesis_test_fails_if_not_real_source_437_original_rows():
    with pytest.raises(ValueError,match="original public archive"):
        analyze([],permutations=99,bootstraps=99)


@pytest.mark.parametrize("bad",[-1,0,5])
def test_low_monte_carlo_effort_fails_closed(bad):
    original=[
        {"Site":"agg","Year":str(2010+i//50),"Type":"A",
         "seedsinit":str(i+1),"flyescape":str((i%10)/10),
         "width":str(i%5+1),"seeds":str(i+1)}
        for i in range(437)
    ]
    with pytest.raises(ValueError,match="Monte Carlo"):
        analyze(original,permutations=bad,bootstraps=99)


def test_original_study_interpretation_ceiling_makes_no_direct_trait_fitness_claim():
    from pathlib import Path
    script=Path("scripts/analyze_sch_ipomopsis_primary_coupling.py").read_text(
        encoding="utf-8")
    for term in (
        "fraction of FRUITS",
        "only a proxy",
        "not population",
        "not independent",
        "not a causal",
    ):
        assert term.lower() in script.lower()
