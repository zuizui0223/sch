"""Source-check the canonical SCH manuscript's 2015 orchid experiment.

No synthetic field samples, new biological cluster, randomization of
flowering start, or full covariance estimate are asserted.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import NormalDist

ROOT=Path(__file__).resolve().parents[1]
TABLE=ROOT/"data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
PATTERNS=ROOT/"data/SCH_PATTERN_LEDGER_V1.csv"
MANUSCRIPT=ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"
FIGURE=ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md"


def _rows(path:Path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def _by_treatment(trait):
    return {r["treatment"]:r for r in _rows(TABLE) if r["trait"]==trait}


def test_original_same_herbivory_factorial_edge_is_source_locked():
    t=_by_treatment("flowering_start")
    assert set(t)=={"C+H","C+E","HP+H","HP+E"}
    assert len(_rows(TABLE))==20
    assert (t["C+E"]["pollination_state"],t["HP+E"]["pollination_state"])==(
        "OPEN_POLLINATED","HAND_POLLINATED"
    )
    assert all(t[k]["herbivory_state"]=="HERBIVORES_EXCLUDED" for k in ("C+E","HP+E"))
    assert (t["C+E"]["beta"],t["C+E"]["se"])==("0.094","0.031")
    assert (t["HP+E"]["beta"],t["HP+E"]["se"])==("-0.066","0.028")
    assert t["C+E"]["significance"]=="P_LT_0.01"
    assert t["HP+E"]["significance"]=="P_LT_0.05"


def test_worst_covariance_interval_is_conditional_not_full_family():
    t=_by_treatment("flowering_start")
    diff=float(t["HP+E"]["beta"])-float(t["C+E"]["beta"])
    upper_se=float(t["HP+E"]["se"])+float(t["C+E"]["se"])
    assert math.isclose(diff,-.160,abs_tol=1e-12)
    assert math.isclose(upper_se,.059,abs_tol=1e-12)
    z=NormalDist().inv_cdf(.975)
    lower,upper=diff-z*upper_se,diff+z*upper_se
    assert -.277<lower<-.275 and -.045<upper<-.043
    upper_p=2*(1-NormalDist().cdf(abs(diff)/upper_se))
    assert .006<upper_p<.0075
    assert 20*upper_p>.05
    assert math.isclose(float(t["C+H"]["beta"]),-.0042,abs_tol=1e-12)
    residual=(float(t["C+H"]["beta"])-float(t["C+E"]["beta"])
              -float(t["HP+H"]["beta"])+float(t["HP+E"]["beta"]))
    assert math.isclose(residual,-.0042,abs_tol=1e-12)


def test_spur_and_phenology_have_different_sign_geometry():
    spur=_by_treatment("spur_length")
    assert spur["C+E"]["beta"]=="0.077"
    assert spur["HP+E"]["beta"]=="-0.042"
    assert spur["HP+E"]["significance"]=="NS"
    assert spur["C+H"]["beta"]=="0.18"
    assert spur["HP+H"]["beta"]=="0.083"


def test_manuscript_promotes_real_ecology_but_not_theory_or_prevalence():
    patterns=[r for r in _rows(PATTERNS) if r["plant_taxon"]=="Gymnadenia conopsea"]
    assert len(patterns)==1
    assert patterns[0]["pattern_class"]=="CONTEXT_WEIGHT_SHIFT"
    assert len(_rows(PATTERNS))==16
    text=MANUSCRIPT.read_text(encoding="utf-8")
    figure=FIGURE.read_text(encoding="utf-8")
    sec=text.split("### 7.7 Experimentally changing one ecological input",1)[1].split(
        "## 8. Final causal identification layer",1
    )[0]
    for token in (
        "−0.160","0.059","−0.276","−0.044","0.134",
        "not extra independent systems","not causal do(z)",
        "not a new held-out programme","trait coordinates",
    ):
        assert token in sec
    assert "source-point contrast −0.160" in figure
    assert "not a manipulated flowering-time optimum" in text
