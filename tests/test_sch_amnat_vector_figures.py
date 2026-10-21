"""Verify the five static vector publication figures against original ecology.

This is an XML/layout-envelope/source-claim check, NOT optical layout QA.
Five SVG files are original edited vector graphics, with a separate
source-backed Figure 4 and four clearly marked theoretical schematics.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

ROOT=Path(__file__).resolve().parents[1]
FIGURES=ROOT/"manuscript/amnat_figures"
ALL={
    1:"figure_01_theory.svg",
    2:"figure_02_identification.svg",
    3:"figure_03_state_optima.svg",
    4:"figure_04_ecological_routes.svg",
    5:"figure_05_handoff.svg",
}
NS="{http://www.w3.org/2000/svg}"


def _read(name:str)->list[dict[str,str]]:
    with (ROOT/"data"/name).open(encoding="utf-8",newline="") as fh:
        return list(csv.DictReader(fh))


def _one(rows:list[dict[str,str]],**q:str)->dict[str,str]:
    matches=[r for r in rows if all(r.get(k)==v for k,v in q.items())]
    assert len(matches)==1, ("source row missing/duplicate",q)
    return matches[0]


def _svg(which:int):
    svg=ET.parse(FIGURES/ALL[which]).getroot()
    assert svg.tag==NS+"svg"
    return svg," ".join(" ".join(svg.itertext()).split())


def test_five_distinct_self_contained_svg_are_present_with_valid_xml_and_figure_order():
    paths=sorted(FIGURES.glob("figure_*.svg"))
    assert {p.name for p in paths}==set(ALL.values())
    for i in ALL:
        svg,txt=_svg(i)
        assert svg.find(NS+"title") is not None
        assert svg.find(NS+"desc") is not None
        assert "FIGURE "+str(i) in txt
        w,h=(int(svg.attrib[k]) for k in ("width","height"))
        assert w in (1600,2000)
        assert h in (1030,1050,1640)
        assert svg.attrib["viewBox"]==f"0 0 {w} {h}"
        assert list(svg.iter(NS+"text")), "empty or all-raster svg is invalid"
        assert not list(svg.iter(NS+"image")), "embedded raster forbidden"
        assert not list(svg.iter(NS+"foreignObject"))
        assert not list(svg.iter(NS+"script"))
        for element in svg.iter():
            assert not any("href" in name.lower() for name in element.attrib), (
                "no remote media/font references are permitted"
            )
            if element.tag in (NS+"text",NS+"rect",NS+"circle",NS+"line"):
                for xcoord in ("x","x1","x2","cx"):
                    if xcoord in element.attrib:
                        assert 0<=float(element.attrib[xcoord])<=w
                for ycoord in ("y","y1","y2","cy"):
                    if ycoord in element.attrib:
                        assert 0<=float(element.attrib[ycoord])<=h
        assert "Arial,Helvetica,sans-serif" in (
            FIGURES/ALL[i]).read_text(encoding="utf-8")


def test_theory_figures_are_not_mislabeled_as_measured_ecological_fitness():
    for i in (1,2,3,5):
        _,txt=_svg(i)
        assert any(marker in txt.upper() for marker in ("SCHEMATIC","HYPOTHETICAL"))
        assert not "measured trait optimum" in txt.lower()
    _,t2=_svg(2)
    assert "EIGHT" in t2.upper()
    assert all(f"W[{a},{state}](z)" in t2
               for a in (0,1) for state in ("00","10","01","11"))
    _,t3=_svg(3)
    for x in ("W00","W10","W01","W11","zP*","zG*","zC*"):
        assert x in t3
    _,t5=_svg(5)
    assert "Φ = s L − K" in t5
    assert "not yet met" in t5
    assert "SCHEMATIC" in t5


def test_empirical_fig4_has_original_gymnadenia_lythrum_brassica_pedicularis_values():
    _,fig=_svg(4)
    gym=_read("SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv")
    open_z=_one(gym,trait="flowering_start",treatment="C+E")
    supplement=_one(gym,trait="flowering_start",treatment="HP+E")
    assert (open_z["beta"],open_z["se"])==("0.094","0.031")
    assert (supplement["beta"],supplement["se"])==("-0.066","0.028")
    assert "+0.094" in fig and "−0.066" in fig
    assert "Open · excluded" in fig and "Pollen+ · excluded" in fig

    l=_read("SCH_LYTHRUM_THOMSEN_2017_TREATMENT_MEANS_TABLE1_V1.csv")
    inf=_one(l,trait="number_of_inflorescences")
    flower=_one(l,trait="flowering_start_julian")
    assert (inf["control_mean"],inf["clipped_mean"])==("5.4","8")
    assert (flower["control_mean"],flower["clipped_mean"])==("191","196")
    lsel=_read("SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv")
    assert _one(lsel,trait="number_of_inflorescences",context_or_contrast="CONTROL")["beta_or_delta"]=="0.47"
    assert _one(lsel,trait="number_of_inflorescences",context_or_contrast="CLIPPED")["beta_or_delta"]=="0.20"
    for val in ("5.4","8.0","+0.47","+0.20","day 191","day 196","−0.03","−0.28"):
        assert val in fig

    beh=_read("SCH_BRASSICA_2017_RECEIVER_BEHAVIOUR_TABLE1_V1.csv")
    for key,expected in (
        ("BUMBLE_BEE_FLOWER_VISITS","0.24"),
        ("CABBAGE_BUTTERFLY_FLOWER_VISITS","0.15"),
        ("CABBAGE_BUTTERFLY_OVIPOSITION","0.45"),
    ):
        assert _one(beh,trait="corolla_size",receiver_response=key)["beta"]==expected
    seed=_read("SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv")
    assert [_one(seed,trait="corolla_size",consumer_regime=r)["beta"] for r in
            ("BUMBLE_BEE","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY","CABBAGE_BUTTERFLY")
           ]==["0.22","0.22","0.26"]
    assert "Bee +.22" in fig and "Mixed +.22" in fig and "Butterfly +.26" in fig
    assert "Egg presence" in fig

    p=_read("PEDICULARIS_2015_CROSS_ENDPOINT_TABLE2_V1.csv")
    assert _one(p,endpoint="seed_predation",term="SITE_X_TREATMENT")["reported_chi2"]=="36.782"
    assert _one(p,endpoint="final_seed_set",term="SITE_X_TREATMENT")["reported_p"]=="0.4265"
    assert _one(p,endpoint="initial_seed_set",term="SITE_X_TREATMENT")["reported_p"]=="0.960"
    for val in ("36.782","0.4265","0.960","Different P-value decisions"):
        assert val in fig
    assert "no randomized trait" in fig.lower()


def test_fig4_distinct_endpoints_have_no_fake_common_numeric_axis():
    _,txt=_svg(4)
    for x in ("source SE","distinct response models","not a common pooled effect size",
              "No water-only manipulation","Regrowth pathway plausible"):
        # The visual labels are intentionally short; detailed caveats are in captions.
        if x not in txt:
            assert x in (FIGURES/"README.md").read_text(encoding="utf-8")
    assert "Sletvold et al. 2015" in txt
    assert "Thomsen & Sargent 2017" in txt
    assert "Knauer & Schiestl 2017" in txt
    assert "Sun & Huang 2015" in txt


def test_captions_preserve_theory_vs_real_data_and_reproduction_limits():
    doc=(FIGURES/"README.md").read_text(encoding="utf-8")
    for x in (
        "Figure 1.","Figure 2.","Figure 3.","Figure 4.","Figure 5.",
        "REAL PUBLISHED SOURCE FIGURE","SCHEMATIC THEORY",
        "not overplotted into Figure 4",
        "Manual rendered visual review","not yet evidence",
    ):
        assert x in doc
    main=(ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    assert "Table 1. Four source-supported ecological signatures" in main
    assert main.count("| Context-sensitive link |")==1
    assert "multiple locations for ecological reweighting" in main
