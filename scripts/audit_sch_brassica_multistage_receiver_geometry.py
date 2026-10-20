"""One Brassica field-cage experiment: three receiver channels and fitness selection.

Source: Knauer & Schiestl 2017 Evolutionary Ecology 31:285-304
DOI 10.1007/s10682-016-9878-8.

Read ORIGINAL Table 1 all 9 floral axes x 3 receiver responses,
EXISTING Table 2 all 9 axes x 3 insect-composition treatments,
ORIGINAL Table 3 all 6 signal-pairs x 3 treatments,
and two author-fitted main-text nonadditive source tests.

The butterfly (Pieris brassicae) acts as a flower visitor AND oviposits
offspring that damage reproductive fitness. These are different response
channels, not a binary fixed taxonomic "antagonist" label.

Do NOT subtract visitor count beta from binary oviposition beta or from
relative-seed-set gradient. Trait levels were not manipulated. A
non-significant butterfly response is not statistical equivalence.
The 18 correlational selection tests include a nominal mixed-group
p=.029, which does not pass a 5%-FWER Bonferroni check.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOI="10.1007/s10682-016-9878-8"
BEHAVIOUR=ROOT/"data/SCH_BRASSICA_2017_RECEIVER_BEHAVIOUR_TABLE1_V1.csv"
NET=ROOT/"data/SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv"
CORR=ROOT/"data/SCH_BRASSICA_2017_CORRELATIONAL_SELECTION_TABLE3_V1.csv"
NONADD=ROOT/"data/SCH_BRASSICA_2017_NONADDITIVE_SELECTION_PRIMARY_TEXT_V1.csv"
TRAITS=(
    "flower_number","corolla_size","benzaldehyde","phenylacetaldehyde",
    "1_butene_4_isothiocyanate","methyl_benzoate",
    "methyl_salicylate","p_anisaldehyde","e_alpha_farnesene",
)
RESPONSES=(
    "BUMBLE_BEE_FLOWER_VISITS",
    "CABBAGE_BUTTERFLY_FLOWER_VISITS",
    "CABBAGE_BUTTERFLY_OVIPOSITION",
)
REGIMES=(
    "BUMBLE_BEE","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY","CABBAGE_BUTTERFLY",
)
PAIRS=(
    "flower_number__corolla_size",
    "flower_number__phenylacetaldehyde",
    "flower_number__e_alpha_farnesene",
    "corolla_size__phenylacetaldehyde",
    "corolla_size__e_alpha_farnesene",
    "phenylacetaldehyde__e_alpha_farnesene",
)
# Original source Table 1 and Table 3 printed numeric values frozen separately
# in CSV. Keep numerical source identities frozen here to fail on reclassification
# or accidental edit; the author-uploaded full source has both tables verbatim.
EXPECTED_BEHAVIOUR={
    "flower_number":(("0.34","0.04","<0.001"),("0.21","0.03","<0.001"),("0.04","0.14","0.76")),
    "corolla_size":(("0.24","0.05","<0.001"),("0.15","0.04","<0.001"),("0.45","0.16","0.006")),
    "phenylacetaldehyde":(("0.15","0.06","0.010"),("0.09","0.04","0.029"),("0.41","0.17","0.016")),
    "benzaldehyde":(("-0.10","0.08","0.23"),("-0.04","0.06","0.50"),("0.11","0.24","0.64")),
    "1_butene_4_isothiocyanate":(("-0.01","0.05","0.95"),("-0.11","0.04","0.005"),("-0.04","0.16","0.62")),
    "methyl_benzoate":(("0.03","0.07","0.63"),("0.04","0.05","0.37"),("0.01","0.20","0.96")),
    "methyl_salicylate":(("-0.01","0.06","0.82"),("0.03","0.04","0.46"),("0.22","0.17","0.20")),
    "p_anisaldehyde":(("0.03","0.09","0.77"),("-0.02","0.06","0.76"),("-0.17","0.23","0.47")),
    "e_alpha_farnesene":(("0.18","0.05","<0.001"),("-0.05","0.04","0.19"),("-0.16","0.16","0.35")),
}
EXPECTED_CORR={
    "flower_number__corolla_size":(("0.01","0.05","0.79"),("0.02","0.08","0.79"),("-0.09","0.08","0.27")),
    "flower_number__phenylacetaldehyde":(("-0.03","0.05","0.54"),("0.10","0.08","0.20"),("-0.10","0.11","0.38")),
    "flower_number__e_alpha_farnesene":(("0.03","0.04","0.42"),("-0.02","0.07","0.78"),("-0.07","0.10","0.52")),
    "corolla_size__phenylacetaldehyde":(("-0.09","0.05","0.07"),("-0.17","0.08","0.029"),("-0.07","0.10","0.48")),
    "corolla_size__e_alpha_farnesene":(("-0.03","0.05","0.58"),("0.03","0.07","0.69"),("0.06","0.10","0.51")),
    "phenylacetaldehyde__e_alpha_farnesene":(("0.01","0.05","0.73"),("-0.01","0.08","0.90"),("-0.10","0.08","0.23")),
}
EXACT_NET_ANCHORS={
    ("corolla_size","BUMBLE_BEE"):(.22,.04,"<0.001"),
    ("corolla_size","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY"):(.22,.08,"0.005"),
    ("corolla_size","CABBAGE_BUTTERFLY"):(.26,.09,"0.007"),
    ("phenylacetaldehyde","BUMBLE_BEE"):(.15,.05,"0.006"),
    ("phenylacetaldehyde","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY"):(-.09,.08,"0.27"),
    ("phenylacetaldehyde","CABBAGE_BUTTERFLY"):(.08,.10,"0.18"),
    ("1_butene_4_isothiocyanate","BUMBLE_BEE"):(-.11,.04,"0.011"),
    ("1_butene_4_isothiocyanate","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY"):(.07,.08,"0.41"),
    ("1_butene_4_isothiocyanate","CABBAGE_BUTTERFLY"):(-.13,.09,"0.20"),
    ("e_alpha_farnesene","BUMBLE_BEE"):(.11,.04,"0.014"),
    ("e_alpha_farnesene","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY"):(.15,.07,"0.042"),
    ("e_alpha_farnesene","CABBAGE_BUTTERFLY"):(.06,.10,"0.53"),
}
EXPECTED_NONADD={
    "phenylacetaldehyde":(-.20,.08,2.619,"0.009"),
    "1_butene_4_isothiocyanate":(.19,.08,2.363,"0.018"),
}


def read(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def _probability(value:str)->float:
    if value.startswith("<"):
        p=float(value[1:])
        if not 0<p<1:
            raise ValueError("source p upper bound out of domain")
        return p
    p=float(value)
    if not 0<=p<=1:
        raise ValueError("source p out of domain")
    return p


def _num(value:str)->float:
    if not value:
        raise ValueError("missing numeric field")
    n=float(value)
    if not math.isfinite(n):
        raise ValueError("nonfinite source field")
    return n


def _source_index(
    rows:list[dict[str,str]], *,
    key1:str, key2:str, coordinates:tuple[str,...],
    contexts:tuple[str,...], n:int, source_table:str,
    beta_field:str, se_field:str, p_field:str,
    expected:dict|None=None,
)->dict[tuple[str,str],dict]:
    if len(rows)!=n:
        raise ValueError(f"source {source_table} must contain exactly {n} rows")
    out={}
    if expected is not None and set(expected)!=set(coordinates):
        raise ValueError("expected original source coordinates mismatch")
    for r in rows:
        key=(r.get(key1,""),r.get(key2,""))
        if key in out or key[0] not in coordinates or key[1] not in contexts:
            raise ValueError("duplicate or unexpected original source coordinate")
        if r.get("source_table")!=source_table or r.get("source_doi")!=DOI:
            raise ValueError("primary source DOI or Table identity drift")
        v,s,p=r.get(beta_field,""),r.get(se_field,""),r.get(p_field,"")
        b,ser=_num(v),_num(s)
        if ser<=0:
            raise ValueError("nonpositive original source SE")
        _probability(p)
        if expected is not None:
            ref=expected[key[0]][contexts.index(key[1])]
            if (v,s,p)!=ref:
                raise ValueError("original printed Table 1/3 source beta/SE/P drift")
        out[key]={"beta":b,"se":ser,"source_p":p,
                  "nominal_source_positive":b>0 and _probability(p)<.05,
                  "nominal_source_negative":b<0 and _probability(p)<.05}
    if set(out)!={(a,b) for a in coordinates for b in contexts}:
        raise ValueError("incomplete original source table")
    return out


def _behavior(rows:list[dict[str,str]])->dict:
    data=_source_index(rows,key1="trait",key2="receiver_response",
        coordinates=TRAITS,contexts=RESPONSES,n=27,source_table="Table_1",
        beta_field="beta",se_field="se",p_field="source_p",
        expected=EXPECTED_BEHAVIOUR)
    for r in rows:
        role=r["receiver_response"]
        warn=("SOURCE_PRINTED_Z_AND_P_DISAGREE_USE_PRINTED_P"
              if r["trait"]=="methyl_benzoate"
              and role=="CABBAGE_BUTTERFLY_FLOWER_VISITS" else "NONE")
        scale=("EGGS_PRESENT_BINARY" if role=="CABBAGE_BUTTERFLY_OVIPOSITION"
               else "INFLORESCENCE_VISITS_COUNT")
        if r.get("response_scale")!=scale or r.get("source_warning")!=warn:
            raise ValueError("receiver endpoint class or source warning drift")
    return data


def _net(rows:list[dict[str,str]])->dict:
    if len(rows)!=27:
        raise ValueError("source Table 2 requires all 27 selection gradients")
    data={}
    for r in rows:
        key=(r.get("trait",""),r.get("consumer_regime",""))
        if key in data or key[0] not in TRAITS or key[1] not in REGIMES:
            raise ValueError("duplicate or unexpected net fitness source coordinate")
        if (r.get("doi")!=DOI or r.get("source_table")!="Table_2"
            or r.get("fitness_estimate")!="relative_seed_set"):
            raise ValueError("source Table 2 DOI/fitness identity drift")
        b,s=_num(r.get("beta","")),_num(r.get("se",""))
        p=r.get("p_value","")
        if s<=0:
            raise ValueError("nonpositive original seed fitness slope uncertainty")
        _probability(p)
        expected=EXACT_NET_ANCHORS.get(key)
        if expected and (abs(b-expected[0])>1e-10 or abs(s-expected[1])>1e-10
                         or p!=expected[2]):
            raise ValueError("frozen net selection source anchor drift")
        data[key]={"beta":b,"se":s,"source_p":p,
                   "nominal_source_positive":b>0 and _probability(p)<.05,
                   "nominal_source_negative":b<0 and _probability(p)<.05}
    if set(data)!={(a,b) for a in TRAITS for b in REGIMES}:
        raise ValueError("missing original net-seed Table 2 trait/regime")
    return data


def _nonadd(rows:list[dict[str,str]], net:dict)->dict:
    if len(rows)!=len(EXPECTED_NONADD):
        raise ValueError("two source reported nonadditivity contrasts required")
    out={}
    for r in rows:
        trait=r.get("trait","")
        if trait not in EXPECTED_NONADD or trait in out:
            raise ValueError("nonadditivity trait unknown or duplicate")
        if (r.get("source_doi")!=DOI
            or r.get("source_location")!="Main_Text_Results_Nonadditive_Selection"
            or r.get("expected_additive_rule")!="HALF_SUM_OF_TWO_PURE_CONSUMER_SELECTION_GRADIENTS"
            or r.get("source_fit_status")!="AUTHOR_FITTED_NONADDITIVITY_TEST"):
            raise ValueError("original author nonadditive source identity drift")
        expected=EXPECTED_NONADD[trait]
        got=(_num(r["reported_observed_minus_expected_beta"]),_num(r["reported_se"]),
             _num(r["reported_t"]),r["reported_p"])
        if got!=expected:
            raise ValueError("original author-fitted nonadditive source value drift")
        bee=net[(trait,"BUMBLE_BEE")]["beta"]
        butterfly=net[(trait,"CABBAGE_BUTTERFLY")]["beta"]
        mixed=net[(trait,"BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY")]["beta"]
        predicted=(bee+butterfly)/2
        subtraction=mixed-predicted
        if abs(subtraction-expected[0])>.011:
            raise ValueError("published author deviation inconsistent with rounded Table 2")
        out[trait]={
            "source_direct_author_fitted_observed_minus_expected":expected[0],
            "reported_source_se":expected[1],
            "reported_source_t_absolute":expected[2],
            "reported_source_p":expected[3],
            "source_author_additive_reference":"(bee_only_gradient+butterfly_only_gradient)/2",
            "arithmetic_reference_from_printed_table_2":round(predicted,6),
            "arithmetic_mixed_minus_additive":round(subtraction,6),
            "arithmetic_is_not_new_covariance_aware_original_test":True,
        }
    return out


def build(behavior:list[dict[str,str]], net:list[dict[str,str]],
          corr:list[dict[str,str]], nonadd:list[dict[str,str]])->dict:
    visits=_behavior(behavior)
    fitness=_net(net)
    corrdata=_source_index(corr,key1="trait_pair",key2="consumer_regime",
        coordinates=PAIRS,contexts=REGIMES,n=18,source_table="Table_3",
        beta_field="correlational_beta",se_field="se",p_field="source_p",
        expected=EXPECTED_CORR)
    if not all(r.get("fitness_measure")=="relative_seed_set" for r in corr):
        raise ValueError("Table 3 endpoint must be relative seed set")
    author_nonadd=_nonadd(nonadd,fitness)
    triple=sorted(t for t in TRAITS if all(
        visits[(t,role)]["nominal_source_positive"] for role in RESPONSES
    ))
    bee_only=sorted(t for t in TRAITS if
        visits[(t,RESPONSES[0])]["nominal_source_positive"]
        and all(not visits[(t,role)]["nominal_source_positive"]
                and not visits[(t,role)]["nominal_source_negative"]
                for role in RESPONSES[1:])
    )
    net_all=sorted(t for t in TRAITS if all(
        fitness[(t,r)]["nominal_source_positive"] for r in REGIMES
    ))
    corr_n_nominal=sum(_probability(v["source_p"])<.05 for v in corrdata.values())
    corr_n_bonf=sum(_probability(v["source_p"])<.05/len(corrdata) for v in corrdata.values())
    mixed_corr=corrdata[("corolla_size__phenylacetaldehyde",
                         "BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY")]
    pea_net={
        r:fitness[("phenylacetaldehyde",r)] for r in REGIMES
    }
    protected_alpha=.05/(len(corrdata))
    if (
        triple!=["corolla_size","phenylacetaldehyde"]
        or bee_only!=["e_alpha_farnesene"]
        or net_all!=["corolla_size"]
        or corr_n_nominal!=1 or corr_n_bonf!=0
        or mixed_corr["beta"]!=-0.17 or mixed_corr["source_p"]!="0.029"
        or [r for r in REGIMES if pea_net[r]["nominal_source_positive"]]!=["BUMBLE_BEE"]
    ):
        raise ValueError("original Brassica receiver/fitness geometry drift")
    return {
        "analysis":"sch_brassica_2017_one_system_multistage_receiver_geometry_v1",
        "status":"ONE_REAL_SOURCE_MULTISTAGE_ROLE_GEOMETRY_NOT_CAUSAL_PURE_COMPONENTS",
        "source_doi":DOI,
        "source_title":"The effect of pollinators and herbivores on selection for floral signals: a case study in Brassica rapa",
        "source_author_year":"Knauer_Schiestl_2017",
        "n_independent_original_cage_experiments":1,
        "source_table_rows":{"receiver_behavior_Table_1":27,
                             "net_selection_Table_2":27,
                             "correlational_selection_Table_3":18,
                             "nonadditive_author_main_text":2},
        "n_floral_trait_coordinates":len(TRAITS),
        "n_correlation_pair_coordinates":len(PAIRS),
        "n_original_consumer_regimes":len(REGIMES),
        "n_original_receiver_response_classes":len(RESPONSES),
        "nominal_triple_positive_receiver_traits":triple,
        "nominal_bee_positive_without_detected_butterfly_visitation_or_oviposition":bee_only,
        "net_seed_selection_positive_in_all_three_regimes":net_all,
        "receiver_overlap_count_nominal":len(triple),
        "net_coral_positive_all_3_source_p":{
            r:fitness[("corolla_size",r)] for r in REGIMES
        },
        "phenylacetaldehyde_net_selection":{
            r:pea_net[r] for r in REGIMES
        },
        "e_alpha_farnesene_receiver_results":{
            role:visits[("e_alpha_farnesene",role)] for role in RESPONSES
        },
        "two_shared_receiver_traits_response_matrix":{
            trait:{role:visits[(trait,role)] for role in RESPONSES}
            for trait in triple
        },
        "mixed_regime_corolla_x_phenylacetaldehyde":{
            **mixed_corr,
            "18_correlational_tests_nominal_alpha":.05,
            "18_correlational_tests_bonferroni_alpha":round(protected_alpha,9),
            "source_familywise_18_test_significance":False,
            "source_nominal_18_test_significance":True,
            "is_independent_test_of_between_regime_correlational_difference":False,
        },
        "n_table3_source_p_below_0_05":corr_n_nominal,
        "n_table3_bonferroni_18_p_below_0_05":corr_n_bonf,
        "author_reported_nonadditive_selection":author_nonadd,
        "butterfly_ecological_role":"FLOWER_VISITOR_AND_LARVAL_HERBIVORE_PARENT",
        "source_fitness_pathway_results":{
            "bee_visitation_to_seeds_beta":20.5,
            "bee_visitation_to_seeds_se":4.8,
            "butterfly_visitation_to_seeds_beta":6.8,
            "butterfly_visitation_to_seeds_se":2.0,
            "caterpillar_infestation_to_seeds_beta":-104.5,
            "caterpillar_infestation_to_seeds_se":19.0,
            "bee_visits_x_caterpillar_infestation_beta":-18.9,
            "bee_visits_x_caterpillar_infestation_se":9.5,
            "bee_visits_x_caterpillar_infestation_source_p":"0.046",
            "same_model_scale_as_receiver_table_1_beta":False,
            "original_source_results_not_refit_from_plants":True,
        },
        "ecological_observation":(
            "two_flower_signals_predict_mutualist_visits_and_herbivore_oviposition;"
            "corolla_seed_fitness_direction_stays_positive_across_all_insect_regimes;"
            "scent_trait_fitness_and_mixed_signal_pairing_can_change_without_a_"
            "demonstrated_pure_function_optimum"
        ),
        "claim_ceiling":[
            "same_one_cage_study_multiple_tables_not_independent_replication",
            "butterfly_can_pollinate_and_oviposit_no_fixed_functional_sign",
            "positive_receiver_response_beta_not_same_as_reproductive_selection_beta",
            "visitor_count_and_binary_oviposition_beta_scales_not_poolable",
            "trait_levels_not_randomized_visitation_egg_and_selection_are_associations",
            "nominal_source_p_triple_overlap_not_27_test_familywise_certified",
            "mixed_negative_correlational_p_0_029_not_18_test_familywise_significant",
            "original_ANCOVA_detected_no_trait_x_consumer_regime_directional_difference",
            "original_ANCOVA_detected_no_correlational_selection_regime_difference",
            "net_positive_corolla_across_regimes_does_not_demonstrate_equal_slopes",
            "bee_only_farnesene_source_nominal_detections_do_not_certify_butterfly_equivalence",
            "author_nonadditive_comparisons_condition_on_additive_mean_model_assumption",
            "no_individual_level_mediation_deduced_from_cross_stage_tables",
            "no_z_x_P_x_G_randomized_surface_or_functional_optima_or_SCH_L",
            "candidate_receiver_specific_farnesene_not_confirmed_BItA_dimensional_release",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--behavior",type=Path,default=BEHAVIOUR)
    p.add_argument("--net",type=Path,default=NET)
    p.add_argument("--correlation",type=Path,default=CORR)
    p.add_argument("--nonadd",type=Path,default=NONADD)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    v=build(read(a.behavior),read(a.net),read(a.correlation),read(a.nonadd))
    s=json.dumps(v,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s,encoding="utf-8")
    else:
        print(s,end="")


if __name__=="__main__":
    main()
