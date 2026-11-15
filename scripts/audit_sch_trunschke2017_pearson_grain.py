"""Audit printed Pearson r/P versus the 12 independent 2017 orchid populations.

Source: Trunschke, Sletvold & Ågren (2017), New Phytologist 214:1381-1389,
DOI 10.1111/nph.14479. This is a secondary arithmetic audit of *published*
rounded statistics, NOT a plant-level data refit or a claim of author error.

Only the flowering-start source r explicitly says n=12 in the original results
sentence. The other four are in the same across-12-populations paragraph. Thus
n=12 is a defensible conditional independent-unit benchmark, but not a
recovered declaration about the authors' actual testing unit.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/SCH_TRUNSCHKE2017_REPORTED_PL_TRAIT_CORRELATIONS_V1.csv"
TRAITS={
  "Flowering start":(-.763,"<0.001"),
  "Plant height":(-.784,"<0.001"),
  "Flower size":(-.428,"0.040"),
  "Number of flowers":(-.325,"0.116"),
  "Spur length":(-.337,"0.111"),
}
# Published original paper's 12-population partition:
# 6 rewardless/deceptive + 6 rewarding orchids; five deceptive >0.8 PL;
# one deceptive and six rewarding <0.4 PL. No species in [0.4,0.8].
PL_REWARD_TABLE=((5,1),(0,6)) # rows deceptive,rewarding; cols high PL, low PL

def _beta_continued_fraction(a:float,b:float,x:float)->float:
    """Stable continued fraction for regularized incomplete beta."""
    eps=3e-14
    fpmin=1e-300
    qab=a+b
    qap=a+1.0
    qam=a-1.0
    c=1.0
    d=1.0-qab*x/qap
    if abs(d)<fpmin:d=fpmin
    d=1.0/d
    h=d
    for m in range(1,2001):
        m2=2*m
        aa=m*(b-m)*x/((qam+m2)*(a+m2))
        d=1+aa*d
        if abs(d)<fpmin:d=fpmin
        c=1+aa/c
        if abs(c)<fpmin:c=fpmin
        d=1/d
        h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d=1+aa*d
        if abs(d)<fpmin:d=fpmin
        c=1+aa/c
        if abs(c)<fpmin:c=fpmin
        d=1/d
        delta=d*c
        h*=delta
        if abs(delta-1.0)<eps:
            return h
    raise ArithmeticError("incomplete beta continued fraction did not converge")

def _regularized_beta(a:float,b:float,x:float)->float:
    if x<=0:return 0.0
    if x>=1:return 1.0
    factor=math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)
                    +a*math.log(x)+b*math.log1p(-x))
    if x<(a+1)/(a+b+2):
        return factor*_beta_continued_fraction(a,b,x)/a
    return 1.0-factor*_beta_continued_fraction(b,a,1-x)/b

def pearson_two_sided_p(r:float,n:int)->float:
    """Exact ordinary two-sided Pearson-null P via beta distribution, stdlib."""
    if n<3 or not -1 < r < 1:
        raise ValueError("Pearson r / independent population n out of bounds")
    return _regularized_beta((n-2)/2,0.5,1-r*r)

def exact_fisher_posthoc(table:tuple[tuple[int,int],tuple[int,int]])->tuple[float,float]:
    """Conditional Fisher probabilities; two-sided as sum of as-extreme tables."""
    (a,b),(c,d)=table
    row1=a+b
    row2=c+d
    high=a+c
    total=row1+row2
    denominator=math.comb(total,high)
    def prob(x):
        return math.comb(row1,x)*math.comb(row2,high-x)/denominator
    allowed=range(max(0,high-row2),min(row1,high)+1)
    observed=prob(a)
    p_two=sum(prob(x) for x in allowed if prob(x)<=observed+1e-12)
    p_one=sum(prob(x) for x in allowed if x>=a)
    return float(p_two),float(p_one)

def parse_source(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def run(records:list[dict[str,str]])->dict:
    if len(records)!=5:
        raise ValueError("exactly five original published trait correlations")
    names=set()
    out=[]
    for row in records:
        trait=row["trait"]
        if trait not in TRAITS or trait in names:
            raise ValueError("duplicate or non-original trait")
        names.add(trait)
        exact_r,printed_p=TRAITS[trait]
        if (row["paper_doi"]!="10.1111/nph.14479" or
            row["original_source_location"]!="Results_MeanTraits_PL" or
            row["independent_population_count"]!="12" or
            row["original_printed_p"]!=printed_p or
            abs(float(row["pearson_r"])-exact_r)>1e-12 or
            row["original_printed_n"]!=("12" if trait=="Flowering start" else "NOT_REPEATED")):
            raise ValueError("original source r/P/n or DOI differs")
        p12=pearson_two_sided_p(exact_r,12)
        p24=pearson_two_sided_p(exact_r,24)
        lo,hi=sorted((pearson_two_sided_p(exact_r-.0005,12),
                      pearson_two_sided_p(exact_r+.0005,12)))
        if printed_p.startswith("<"):
            reported_class_supported12=p12<float(printed_p[1:])
            reported_class_supported24=p24<float(printed_p[1:])
            n_best=None
            apparent_n24_close=reported_class_supported24
        else:
            original=float(printed_p)
            reported_class_supported12=(p12<=original+.0005)
            reported_class_supported24=(p24<=original+.01)
            n_best=min(range(12,31),key=lambda n:abs(
                     pearson_two_sided_p(exact_r,n)-original))
            apparent_n24_close=abs(p24-original)<.01
        out.append({
          "trait":trait,"published_rounded_r":exact_r,"published_P":printed_p,
          "n12_two_sided_pearson_p":round(p12,8),
          "n12_r_rounding_half_last_decimal_p_range":[round(lo,8),round(hi,8)],
          "n24_two_sided_pearson_p_for_diagnostic_only":round(p24,8),
          "published_P_compatible_with_independent_n12":reported_class_supported12,
          "printed_P_numerically_near_n24_convention":apparent_n24_close,
          "best_integer_n_between_12_and_30_for_exact_printed_P":n_best,
          "conditional_significant_at_0_05_if_n12":p12<.05,
        })
    if names!=set(TRAITS):
        raise ValueError("source trait inventory incomplete")
    by={x["trait"]:x for x in out}
    if (sum(x["conditional_significant_at_0_05_if_n12"] for x in out)!=2 or
        by["Flower size"]["conditional_significant_at_0_05_if_n12"] or
        any(x["published_P_compatible_with_independent_n12"] for x in out)):
        raise ValueError("unexpected Pearson n12 reconciliation signature")
    # The original *Figure 2* PL vs opportunity R2=.63, P=.002 is consistent
    # with n=12, unlike the five trait-vs-PL Pearson P labels.
    figure2_open_n12_p=pearson_two_sided_p(math.sqrt(.63),12)
    if not .0017<figure2_open_n12_p<.0023:
        raise ValueError("published Figure2 source consistency guard failed")
    fisher_two,fisher_one=exact_fisher_posthoc(PL_REWARD_TABLE)
    if abs(fisher_two-1/66)>1e-12:
        raise ValueError("source-defined reward association arithmetic drift")
    return {
      "analysis":"sch_trunschke2017_rounded_pearson_source_grain_v1",
      "original_paper_doi":"10.1111/nph.14479",
      "source_publication_year":2017,
      "n_independent_populations":12,
      "n_original_repeated_trait_correlations":5,
      "published_r_and_P_recalculated_by_independent_population_n12":sorted(out,key=lambda x:x["trait"]),
      "n12_nominal_P_under_0_05_count":2,
      "n12_original_reported_P_labels_recovered_count":0,
      "figure2_open_PL_vs_opportunity_published_R2":.63,
      "figure2_open_PL_vs_opportunity_published_P":.002,
      "figure2_open_recomputed_n12_P":round(figure2_open_n12_p,8),
      "reward_strategy_PL_bimodal_observed_counts":{
          "deceptive_above_0_8":5,
          "deceptive_below_0_4":1,
          "rewarding_above_0_8":0,
          "rewarding_below_0_4":6,
          "species_between_0_4_and_0_8":0},
      "post_hoc_conditional_Fisher_two_sided_P":round(fisher_two,8),
      "post_hoc_conditional_Fisher_one_sided_P":round(fisher_one,8),
      "critical_limits":[
          "rounded_r_and_printed_p_are_not_original_individual_plants",
          "n12_is_a_conditional_independent_species_population_unit_benchmark",
          "matching_n24_p_values_is_not_proof_the_authors_used_n24",
          "possible_treatment_repeated_population_means_not_source_verified",
          "post_hoc_PL_group_cutoffs_do_not_provide_prospective_population_generalization",
          "published_F_statistic_for_PL_selection_is_a_distinct_test_not_recomputed",
          "all_12_species_PL_gradient_pairs_remain_unavailable_without_S5_S6_or_original_XLS",
          "original_2017_paper_does_not_randomize_plant_trait_z",
          "no_new_SCH_L_or_pure_function_optima",
      ],
      "status":"PRINTED_2017_PEARSON_P_DIFFER_FROM_12_UNIT_ARITHMETIC__ORIGINAL_N_PROVENANCE_UNRESOLVED",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    receipt=run(parse_source(a.source))
    out=json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(out,encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
