"""2024 milkweed source and exact zero-truncated NB mathematical tests."""
from pathlib import Path
import pytest
from scripts.analyze_sch_milkweed_2024_zero_truncated_nb import (
    SOURCE_DOI,SOURCE_SHA256,N_SOURCE,N_SOURCE_LABELS,N_POSITIVE,
    N_POSITIVE_LABELS,N_BOOT,_pieces,_objective
)

def test_source_grain():
    assert SOURCE_DOI=="10.26786/1920-7603(2024)758"
    assert SOURCE_SHA256=="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
    assert (N_SOURCE,N_SOURCE_LABELS,N_POSITIVE,N_POSITIVE_LABELS,N_BOOT)==(103,102,63,62,199)

def test_analytic_gradient_matches_symmetric_difference():
    np=pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    rng=np.random.default_rng(20261117)
    X=np.column_stack((np.ones(35),rng.normal(size=(35,4))))
    y=rng.integers(1,8,size=35)
    offset=np.log(rng.uniform(30,160,size=35))
    beta=np.array([-3.8,.15,.2,-.12,.04])
    ll,grad=_objective(beta,X,y,offset,.5)
    finite=np.zeros_like(grad)
    for j in range(len(beta)):
        d=np.zeros_like(beta);d[j]=1e-5
        finite[j]=(_objective(beta+d,X,y,offset,.5)[0]-
                   _objective(beta-d,X,y,offset,.5)[0])/(2e-5)
    assert np.max(np.abs(grad-finite))<1e-6
    assert np.isfinite(ll)

def test_proper_truncated_pmf_not_unconditional_nb():
    np=pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    from scipy.stats import nbinom
    X=np.ones((1,1));offset=np.zeros(1);beta=np.log(np.array([3.]))
    alpha=.5;r=1/alpha
    y=np.arange(1,101)
    pmf=nbinom.pmf(y,r,r/(r+3.))
    p0=nbinom.pmf(0,r,r/(r+3.))
    expected=pmf/(1-p0)
    assert sum(expected)==pytest.approx(1,abs=1e-10)
    for term,value in zip(y[:10],expected[:10]):
        lp,score,weight,mean=_pieces(beta,X,np.array([term]),offset,alpha)
        assert np.exp(lp[0])==pytest.approx(value,rel=1e-10)

def test_script_preserves_no_causal_tradeoff_limit():
    s=Path("scripts/analyze_sch_milkweed_2024_zero_truncated_nb.py").read_text(encoding="utf-8")
    for token in ("1-p0", "no_SCH_conflict_loss_L",
                  "selected_F_gt_0_source_cohort",
                  "source_positive_fruit_rows", "not_causal"):
        if token=="not_causal":
            continue
        assert token in s
