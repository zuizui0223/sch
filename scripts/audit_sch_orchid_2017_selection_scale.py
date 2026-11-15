"""Audit published Trunschke et al. (2017) original ANCOVA tests and study grain.

The 12 orchid species belong to one published biological programme. This audit
does not infer a pooled mean from the original Caruso 2020 compilation:
the source compilation has only one flowering-time matched edge per species,
whereas author Table 2/4 analyse five trait axes per species.

Primary DOI 10.1111/nph.14479; original Dryad 10.5061/dryad.28n72.
"""
from __future__ import annotations
import csv
import json
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MATCHED=ROOT/"data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
T2=ROOT/"data/SCH_TRUNSCHKE2017_ORIGINAL_AUTHOR_ANCOVA_TABLE2_V1.csv"
T4=ROOT/"data/SCH_TRUNSCHKE2017_ORIGINAL_AUTHOR_PL_SELECTION_TABLE4_V1.csv"
EXPECTED_TRAITS=("Flowering start","Plant height","Number of flowers","Flower size","Spur length")
EXPECTED_T2={
("TRAIT_X_POLLINATION","Flowering start"):(1,6.62,"0.010"),
("TRAIT_X_POLLINATION","Plant height"):(1,1.19,"0.276"),
("TRAIT_X_POLLINATION","Number of flowers"):(1,.06,"0.805"),
("TRAIT_X_POLLINATION","Flower size"):(1,.00,"0.966"),
("TRAIT_X_POLLINATION","Spur length"):(1,3.56,"0.059"),
("TRAIT_X_SPECIES_X_POLLINATION","Flowering start"):(11,1.22,"0.265"),
("TRAIT_X_SPECIES_X_POLLINATION","Plant height"):(11,2.55,"0.003"),
("TRAIT_X_SPECIES_X_POLLINATION","Number of flowers"):(11,2.37,"0.007"),
("TRAIT_X_SPECIES_X_POLLINATION","Flower size"):(11,1.11,"0.353"),
("TRAIT_X_SPECIES_X_POLLINATION","Spur length"):(11,.35,"0.973"),
}
EXPECTED_T4={
("NET","PL"):(1,6.374,"0.015","ABS_BETA_OPEN"),
("NET","TRAIT"):(4,6.728,"<0.001","ABS_BETA_OPEN"),
("NET","PL_X_TRAIT"):(4,.278,"0.891","ABS_BETA_OPEN"),
("POLLINATOR_MEDIATED","PL"):(1,18.79,"<0.001","ABS_DELTA_BETA_OPEN_MINUS_HAND"),
("POLLINATOR_MEDIATED","TRAIT"):(4,.42,"0.793","ABS_DELTA_BETA_OPEN_MINUS_HAND"),
("POLLINATOR_MEDIATED","PL_X_TRAIT"):(4,.69,"0.604","ABS_DELTA_BETA_OPEN_MINUS_HAND"),
("NONPOLLINATOR_MEDIATED","PL"):(1,.0045,"0.947","ABS_BETA_HAND"),
("NONPOLLINATOR_MEDIATED","TRAIT"):(4,40.84,"<0.001","ABS_BETA_HAND"),
("NONPOLLINATOR_MEDIATED","PL_X_TRAIT"):(4,.40,"0.807","ABS_BETA_HAND"),
}

def read_csv(p):
    with p.open(newline="",encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def p_upper(x):
    return float(x[1:] if x.startswith("<") else x)

def run(matched,table2,table4):
    if len(matched)!=137 or len(table2)!=10 or len(table4)!=9:
        raise ValueError("denominator or primary source table count drift")
    focused=[row for row in matched if row["paper_id"]=="33"]
    if len(focused)!=12 or len({x["species"] for x in focused})!=12 or any(
       x["trait"]!="Flowering start" or x["source_agent"]!="Pollinators" or
       x["agent_category"]!="BIOTIC" or x["fitness_component"]!="F" for x in focused):
        raise ValueError("original Caruso compilation: 12 species x flowering start source-identity drift")
    two_seen=set()
    for x in table2:
        k=(x["author_test"],x["trait"])
        if k not in EXPECTED_T2 or k in two_seen:
            raise ValueError("noncanonical or duplicate original Table2 trait interaction")
        two_seen.add(k)
        d,f,p=EXPECTED_T2[k]
        if not (x["source_paper_doi"]=="10.1111/nph.14479" and
                x["source_table"]=="Table_2" and
                x["study_populations"]=="12" and
                x["model_family"]=="RELATIVE_FEMALE_FITNESS_ANCOVA" and
                x["df_num"]==str(d) and x["df_den"]=="2353" and
                abs(float(x["F"])-f)<1e-8 and x["p"]==p):
            raise ValueError("original Table2 F/p/df or model identity drift")
    if two_seen!=set(EXPECTED_T2):
        raise ValueError("original Table2 trait interaction omitted")
    four_seen=set()
    for x in table4:
        k=(x["selection_component"],x["term"])
        if k not in EXPECTED_T4 or k in four_seen:
            raise ValueError("noncanonical or duplicate original Table4 component/term")
        four_seen.add(k)
        d,f,p,definition=EXPECTED_T4[k]
        if not (x["source_paper_doi"]=="10.1111/nph.14479" and
                x["source_table"]=="Table_4" and
                x["n_species"]=="12" and x["n_trait_axes"]=="5" and
                x["df_num"]==str(d) and x["df_den"]=="50" and
                x["definition"]==definition and
                abs(float(x["F"])-f)<1e-8 and x["p"]==p):
            raise ValueError("original Table4 F/p/df or outcome family drift")
    if four_seen!=set(EXPECTED_T4):
        raise ValueError("source Table4 outcome missing")
    t4_pl=[r for r in table4 if r["term"]=="PL"]
    pl_results={x["selection_component"]:{
      "original_F":float(x["F"]), "author_p_bound":x["p"],
      "passes_three_predeclared_component_Bonferroni_if_source_p_valid":p_upper(x["p"])<=.05/3
    } for x in t4_pl}
    if (set(pl_results)!={"NET","POLLINATOR_MEDIATED","NONPOLLINATOR_MEDIATED"}
        or not pl_results["NET"]["passes_three_predeclared_component_Bonferroni_if_source_p_valid"]
        or not pl_results["POLLINATOR_MEDIATED"]["passes_three_predeclared_component_Bonferroni_if_source_p_valid"]
        or pl_results["NONPOLLINATOR_MEDIATED"]["passes_three_predeclared_component_Bonferroni_if_source_p_valid"]):
        raise ValueError("published between-species pollen limitation conclusion changed")
    t2_full_family=[{"author_test":r["author_test"],"trait":r["trait"],"p":r["p"]}
       for r in table2 if p_upper(r["p"])<=.05/10]
    if len(t2_full_family)!=1 or t2_full_family[0]["trait"]!="Plant height" or (
        t2_full_family[0]["author_test"]!="TRAIT_X_SPECIES_X_POLLINATION"):
        raise ValueError("original author trait heterogeneity family sensitivity changed")
    return {
      "analysis":"sch_orchid_2017_between_species_selection_scale_audit_v1",
      "published_source_doi":"10.1111/nph.14479",
      "published_data_doi":"10.5061/dryad.28n72",
      "n_source_compiled_papers":1,
      "compiled_137_pair_base_unchanged":137,
      "n_in_compilation_matched_pairs":12,
      "n_original_named_species_in_compilation":12,
      "n_compiled_trait_types_from_this_paper":1,
      "n_original_author_table2_trait_axes":5,
      "original_author_table2_direct_interactions":10,
      "original_author_table4_trait_component_test_rows":9,
      "original_author_PL_association_by_fitness_selection_component":pl_results,
      "direct_trait_interaction_10_comparison_sensitivity_passes":t2_full_family,
      "population_year_comparison_2014_source_doi":"10.1111/evo.12405",
      "population_year_comparison_2014_n_species":2,
      "population_year_comparison_2014_n_population_years":14,
      "cross_study_pooled_scale_regression_performed":False,
      "new_individual_plant_observations_collected":False,
      "independent_2017_source_raw_fitness_model_refitted":False,
      "critical_limits":[
         "2017_between_species_gradient_vs_2014_within_species_nonassociation_are_different_levels",
         "2014_and_2017_share_some_taxa_but_not_the_same_population_year_sampling_units",
         "5_trait_axes_per_species_are_not_60_independent_species",
         "2017_trait_specific_selection_gradients_standardized_by_species_and_treatment",
         "original_ANCOVA_p_values_may_need_species_cluster_robust_reanalysis",
         "observed_pollen_limitation_is_not_randomized_as_an_independent_species_predictor",
         "no_new_SCH_same_coordinate_conflict_or_L",
         "no_pure_function_optima",
      ],
      "status":"ONE_12_ORCHID_BETWEEN_SPECIES_SOURCE_SUPPORT__CLUSTER_REANALYSIS_REQUIRED_FOR_GENERALITY",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--matched",type=Path,default=MATCHED)
    p.add_argument("--table2",type=Path,default=T2)
    p.add_argument("--table4",type=Path,default=T4)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=run(read_csv(a.matched),read_csv(a.table2),read_csv(a.table4))
    s=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s,encoding="utf-8")
    print(s)

if __name__=="__main__":
    main()
