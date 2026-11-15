"""Strict source-scope audit: 2014 within species, 2016 manipulated intensity,
2017 between species pollen limitation and selection.

No synthetic cross-study meta effect, causal trait optimum or raw-data refit.
"""
from __future__ import annotations
import csv
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPERIMENT=ROOT/"data/SCH_POLLINATION_INTENSITY_2016_EXPERIMENT_SOURCE_V1.csv"
OPPORTUNITY=ROOT/"data/SCH_POLLINATION_INTENSITY_2017_OPPORTUNITY_TABLE1_V1.csv"
PUBLISHED=ROOT/"data/SCH_TRUNSCHKE2017_ORIGINAL_AUTHOR_PL_SELECTION_TABLE4_V1.csv"
EXPECTED_2016={
 ("N_POLLINATION_TREATMENTS","NA"):5.0,
 ("POLLEN_LIMITATION_MAX_MINUS_MIN","NA"):.77,
 ("OPPORTUNITY_SELECTION_FOLD","NA"):5.0,
 ("INCREASE_POLLINATOR_MEDIATED_SELECTION_PERCENT","Plant height"):91.0,
 ("INCREASE_POLLINATOR_MEDIATED_SELECTION_PERCENT","Corolla size"):34.0,
 ("INCREASE_POLLINATOR_MEDIATED_SELECTION_PERCENT","Spur length"):330.0,
}
EXPECTED_2017={
 "PL":(16.78,"<0.001"),
 "POLLINATION_TREATMENT":(14.34,"0.001"),
 "PL_X_POLLINATION_TREATMENT":(15.60,"<0.001"),
}
EXPECTED_SELECTION_PL={
 "NET":(6.374,"0.015"),
 "POLLINATOR_MEDIATED":(18.79,"<0.001"),
 "NONPOLLINATOR_MEDIATED":(.0045,"0.947"),
}

def csv_read(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def run(exp,opp,selection):
    if [len(exp),len(opp),len(selection)]!=[6,3,9]:
        raise ValueError("source-row scope drift")
    seen=set()
    for row in exp:
        key=(row["original_reported_measure"],row["trait"])
        if key not in EXPECTED_2016 or key in seen:
            raise ValueError("unexpected/duplicated experimental result")
        seen.add(key)
        if (row["doi"]!="10.1002/ecy.1554" or row["year"]!="2016" or
            row["species"]!="Gymnadenia conopsea" or
            row["design"]!="POLLINATOR_EXCLUSION_FIVE_INTENSITIES" or
            row["unit"]!="ONE_EXPERIMENTAL_POPULATION" or
            row["source_location"]!="Published_Abstract" or
            abs(float(row["original_value"])-EXPECTED_2016[key])>1e-9):
            raise ValueError("2016 source identity or reported value drift")
    if seen != set(EXPECTED_2016):
        raise ValueError("2016 source record incomplete")
    seen=set()
    for row in opp:
        key=row["original_term"]
        if key not in EXPECTED_2017 or key in seen:
            raise ValueError("2017 Table 1 duplicate or unknown effect")
        seen.add(key)
        F,p=EXPECTED_2017[key]
        if (row["doi"]!="10.1111/nph.14479" or
            row["year"]!="2017" or row["study_species"]!="12" or
            row["n_source_fit_units"]!="24" or
            row["trait_test_family"]!="OPPORTUNITY" or
            row["source_location"]!="Table1" or
            row["source_model"]!="OPPORTUNITY_VARIANCE_OF_RELATIVE_FEMALE_FITNESS" or
            row["df_num"]!="1" or row["df_den"]!="20" or
            row["source_p"]!=p or abs(float(row["F"])-F)>1e-9):
            raise ValueError("2017 original opportunity ANCOVA identity drift")
    if seen!=set(EXPECTED_2017):
        raise ValueError("2017 source opportunity incomplete")
    fitted=[r for r in selection if r["term"]=="PL"]
    if len(fitted)!=3:
        raise ValueError("wrong 2017 selection outcome components")
    comp_seen=set()
    for row in fitted:
        k=row["selection_component"]
        if k in comp_seen or k not in EXPECTED_SELECTION_PL:
            raise ValueError("duplicated or unfamiliar selection component")
        comp_seen.add(k)
        val,p=EXPECTED_SELECTION_PL[k]
        if (row["source_paper_doi"]!="10.1111/nph.14479" or
            row["source_table"]!="Table_4" or row["df_num"]!="1" or
            row["df_den"]!="50" or row["p"]!=p or
            abs(float(row["F"])-val)>1e-9):
            raise ValueError("2017 already-frozen original selection results mismatch")
    return {
      "analysis":"sch_pollen_intensity_context_scaling_v1",
      "n_distinct_original_published_programmes_considered":3,
      "original_source_years":[2014,2016,2017],
      "source_2014_doi":"10.1111/evo.12405",
      "source_2014_population_year_units":14,
      "source_2014_species":2,
      "source_2014_within_species_PL_gradient_detected":False,
      "source_2016_doi":"10.1002/ecy.1554",
      "source_2016_experiment_sites":1,
      "source_2016_pollination_intensity_treatments":5,
      "source_2016_PL_range_observed":[0,.77],
      "source_2016_opportunity_selection_approx_fold":5,
      "source_2016_increased_pollinator_mediated_selection_percent":{
        "plant_height":91,"corolla_size":34,"spur_length":330},
      "source_2017_doi":"10.1111/nph.14479",
      "source_2017_species":12,
      "source_2017_PL_by_pollination_opportunity_interaction_F":15.60,
      "source_2017_PL_by_pollination_opportunity_interaction_p":"<0.001",
      "source_2017_PL_selection_F_components":{
        r["selection_component"]:float(r["F"]) for r in fitted},
      "species_cluster_robust_raw_refit_executed":False,
      "between_vs_within_effect_difference_tested":False,
      "trait_specific_covariance_measured_from_raw":False,
      "cross_study_numeric_pooling_performed":False,
      "no_causal_trait_optima_or_SCH_L":True,
      "status":"REAL_WITHIN_POPULATION_INTENSITY_MANIPULATION_SUPPORTED__MULTISCALE_CONTRAST_DESCRIPTIVE_ONLY",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--experiment",type=Path,default=EXPERIMENT)
    p.add_argument("--opportunity",type=Path,default=OPPORTUNITY)
    p.add_argument("--source-selection",type=Path,default=PUBLISHED)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=run(csv_read(a.experiment),csv_read(a.opportunity),csv_read(a.source_selection))
    out=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(out,encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
