"""Guard the manuscript's focal ecological interpretation against over-promotion.

These are source-to-claim checks, not additional P. rex field measurements.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATTERN = ROOT / "data/SCH_PATTERN_LEDGER_V1.csv"
SOURCE_WATER = ROOT / "empirical/architecture/PEDICULARIS_PUBLISHED_EMPIRICAL_PRIORS_V1.csv"
SOURCE_YEAR2016 = ROOT / "data/PEDICULARIS_2016_SELECTION_MODEL_AICC_V1.csv"
SOURCE_PATCH = ROOT / "data/PEDICULARIS_XIA2013_PATCH_UNIT_AUDIT_V1.csv"
MANUSCRIPT = ROOT / "manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"
FIGURE = ROOT / "manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_focal_reality_anchor_does_not_add_new_cluster_or_promote_L():
    entries = read_csv(SOURCE_PATTERN)
    assert len(entries) == 16
    focal = [r for r in entries if r["taxon"] == "Pedicularis rex"]
    assert len(focal) == 1
    assert focal[0]["pattern_class"] == "OPPOSING_DIRECTION"
    m = MANUSCRIPT.read_text(encoding="utf-8")
    assert "already contributes to the five conflict-signature clusters" in m
    section = m.split("### 7.6 A focal biological anchor:", 1)[1].split(
        "## 8. Final causal identification layer", 1
    )[0]
    assert "do **not** constitute one crossed" in section
    assert "none can be promoted to a measured L" in section
    assert "context-specific" not in focal[0]["pattern_class"]


def test_water_result_is_only_compound_manipulation_and_shama_visitation():
    site_rows = [
        r for r in read_csv(SOURCE_WATER)
        if r["measurement_id"].startswith("PRX2015_PRED_")
    ]
    assert len(site_rows) == 6
    assert all(r["source_id"] == "PRX2015_WATER" for r in site_rows)
    assert all(float(r["estimate"]) < 0 for r in site_rows)
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    for token in (
        "doi:10.1093/aobpla/plv019",
        "puncture-plus-water drainage",
        "five populations",
        "Shama",
        "P = 0.958",
        "neither global neutrality nor an equivalence test",
    ):
        assert token in manuscript
    assert "not selectively excluding seed predators" not in manuscript  # use precise qualified G wording
    assert "selectively excluding seed predators while bract water is held constant" in manuscript


def test_fitness_translation_and_patch_unit_are_not_trait_optima():
    models = read_csv(SOURCE_YEAR2016)
    patch = read_csv(SOURCE_PATCH)
    assert {r["endpoint"] for r in models} >= {
        "pollen_receipt", "seed_predation", "final_viable_seeds"
    }
    assert {int(r["independent_patches_2011"]) for r in patch} == {11}
    assert {int(r["sparse_patches_2011"]) for r in patch} == {5}
    assert {int(r["dense_patches_2011"]) for r in patch} == {6}
    m = MANUSCRIPT.read_text(encoding="utf-8")
    for token in (
        "doi:10.1093/aob/mcw097",
        "doi:10.1098/rsbl.2013.0387",
        "**11 spatial patches**",
        "not thousands of independent patches",
        "**Pressure:**",
        "**Trait discrimination:**",
        "**Fitness translation:**",
        "historical fully consumed capsules cannot be reclassified as observed zeros",
    ):
        assert token in m


def test_figure_map_preserves_three_source_lanes_not_pseudo_factorial():
    figure=FIGURE.read_text(encoding="utf-8")
    for s in (
        "2016 **observational**",
        "2015 **experimentally manipulated puncture-plus-drainage**",
        "2013 **observational** 11-patch",
        "THREE separate source-labeled horizontal lanes",
        "not connected into a fictitious experimental z x G surface",
    ):
        assert s in figure
