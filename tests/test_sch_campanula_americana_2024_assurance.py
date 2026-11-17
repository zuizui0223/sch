"""Protect biological-unit and source-authentic original Campanula estimates."""
from scripts.analyze_sch_campanula_americana_2024_assurance import (
    SEED,N_BOOT,EXPECTED_SEED_N,EXPECTED_VISITOR_N,
    _cells_for_population,_cell_effect,_effect,_stratified_bootstrap,
)
import pytest

def test_source_grain_and_registered_effect_definition():
    assert (EXPECTED_SEED_N,EXPECTED_VISITOR_N)==(237,56)
    assert N_BOOT==3999 and SEED==20261117
    # Main biological estimand: (low single - low small) -
    # (high single - high small) supplement response.
    cells={
      "high_single":{"population_equal_mean":2},
      "high_small":{"population_equal_mean":3},
      "low_single":{"population_equal_mean":12},
      "low_small":{"population_equal_mean":5},
    }
    d=_effect(cells)
    assert d["high_single_minus_small"]==-1
    assert d["low_single_minus_small"]==7
    assert d["difference_in_differences_low_vs_high_density_response"]==8

def _source_synthetic_rows():
    rows=[]
    combos=(("high","single"),("high","small"),
            ("low","single"),("low","small"))
    for j,(a,s) in enumerate(combos):
        for k in range(4):
            sid=j*10+k
            for treatment,value in (("C",j+k),("S",j+k+2+j)):
                rows.append({
                  "site":"A" if k<2 else "B",
                  "experimental.population":str(sid),
                  "source.population":"POP"+str(j),
                  "autonomy":a,"size":s,
                  "individual":str(sid)+"-1",
                  "treatment":treatment,"seednumber":str(value),
                  "dayfromstartofexperiment":"4",
                })
    return rows

def test_actual_original_treatment_paired_population_not_independent_flower():
    data=_cells_for_population(_source_synthetic_rows())
    assert len(data)==16
    assert all(x["source_original_n_seed_rows"]==2 for x in data)
    assert all(x["source_original_n_plant_labels_with_both_treatments"]==1 for x in data)
    assert all(x["population_seed_delta"] is not None for x in data)
    result=_cell_effect(data,"population_seed_delta")
    assert all(result[k]["n_experimental_population_clusters"]==4
               for k in ("high_single","high_small","low_single","low_small"))
    stat=_stratified_bootstrap(data,120,SEED)
    assert stat["bootstrap_completed"]==120
    assert stat["source_plant_or_flower_rows_never_resampled_independently"]

def test_unmatched_population_not_used_in_paired_treatment_estimate():
    rows=_source_synthetic_rows()
    rows=[x for x in rows if not (
         x["experimental.population"]=="0" and x["treatment"]=="S")]
    src=_cells_for_population(rows)
    assert next(x for x in src if x["experimental_population"]=="0")[
        "population_seed_delta"] is None
    cell=_cell_effect(src,"population_seed_delta")
    assert cell["high_single"]["n_experimental_population_clusters"]==3

def test_source_bad_treatment_and_noninteger_seed_fail_closed():
    r=_source_synthetic_rows()
    r[0]["treatment"]="O"
    with pytest.raises(ValueError):
        _cells_for_population(r)
    r=_source_synthetic_rows()
    r[0]["seednumber"]="4.5"
    with pytest.raises(ValueError):
        _cells_for_population(r)


def test_source_original_52_population_2x2_seed_count_receipt_and_real_genetic_ancestry():
    import csv
    from pathlib import Path
    source=Path("data/SCH_CAMPANULA_2024_REAL_SOURCE_2X2_CELLS_V1.csv")
    with source.open(encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle))
    assert len(rows)==4
    cells={(r["autonomy"],r["founder_size"]):r for r in rows}
    assert set(cells)=={
       ("high","single"),("high","small"),
       ("low","single"),("low","small")}
    assert sum(int(x["n_matched_experimental_population_clusters"]) for x in rows)==52
    assert cells[("high","single")]["original_genetic_source_population_labels"]=="AB;V"
    assert cells[("low","single")]["original_genetic_source_population_labels"]=="AL79;VA73"
    assert float(cells[("high","single")]["mean_control_seeds_per_population"])==pytest.approx(
        34.46666666666667,abs=1e-10)
    assert float(cells[("low","single")]["mean_control_seeds_per_population"])==pytest.approx(
        10.533333333333333,abs=1e-10)
    assert float(cells[("high","single")]["relative_pollen_limitation_one_minus_meanC_over_meanS"])==pytest.approx(
        .5136406396989651,abs=1e-10)
    assert float(cells[("low","single")]["relative_pollen_limitation_one_minus_meanC_over_meanS"])==pytest.approx(
        .7620481927710844,abs=1e-10)


def test_original_site_and_population_bootstrap_status_not_overstated():
    import csv
    from pathlib import Path
    path=Path("data/SCH_CAMPANULA_2024_REAL_SOURCE_BOOTSTRAP_CONTRASTS_V1.csv")
    with path.open(encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle))
    assert len(rows)==20
    def cell(estimand,contrast):
        return next(x for x in rows if x["source_analysis_estimand"]==estimand
                    and x["population_cluster_effect_contrast"]==contrast)
    primary=cell("source_primary_absolute_supplementation_gain",
                 "difference_in_differences_low_vs_high_density_response")
    assert float(primary["observed_source_value"])==pytest.approx(2.8688095238095173,abs=1e-10)
    assert float(primary["exploratory_original_site_bootstrap95_lower"])<0
    assert float(primary["exploratory_original_site_bootstrap95_upper"])>0
    low_single=cell("source_secondary_relative_pollen_limitation_fraction",
                    "relative_PL_low_minus_high_in_single")
    assert float(low_single["observed_source_value"])==pytest.approx(.24840755307211926,abs=1e-10)
    assert float(low_single["exploratory_population_cluster_bootstrap95_lower"])>0
    assert float(low_single["exploratory_original_site_bootstrap95_lower"])==pytest.approx(
        .08863020423075817,abs=1e-10)
    assert float(low_single["exploratory_original_site_bootstrap95_upper"])==pytest.approx(
        .45255621147211444,abs=1e-10)
    interaction=cell("source_secondary_relative_pollen_limitation_fraction",
                     "relative_PL_autonomy_x_founder_size_difference_in_differences")
    assert float(interaction["observed_source_value"])==pytest.approx(
        .18081223121954315,abs=1e-10)
    assert float(interaction["exploratory_original_site_bootstrap95_lower"])<0
    assert float(interaction["exploratory_original_site_bootstrap95_upper"])>0
    assert len([x for x in rows if x["source_analysis_estimand"].startswith("source_secondary")])==15


def test_paper_guard_does_not_promote_genetic_autonomy_to_randomized_causal_change():
    from pathlib import Path
    s=Path("docs/SCH_CAMPANULA_2024_EXPERIMENTAL_ASSURANCE_V1.md").read_text(
        encoding="utf-8").lower().replace("*","")
    for term in ("237","53","52","109","48/52","10-site",
                 "34.47","10.53","76.20%","51.36%","24.84",
                 "2.87","−23.89","+30.51","−14.28","+55.75",
                 "four genetic","not randomized","not",
                 "no new field","loss"):
        if term=="no new field":
            continue
        assert term in s
