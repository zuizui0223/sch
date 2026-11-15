"""Original 137-source-pair audit: selection-direction identity across contexts.

New, genuinely computed source-data contrast:
Within ORIGINAL paper × species × setting × fitness × experiment/treatment
strata containing one distinct matched pair PER trait, are the signs of
selection gradients concordant across interventions more often than they
would be after *re-pairing trait identities* within that same source stratum?

This is a conditional sign-identity permutation diagnostic, not an actual
randomized permutation of selection treatments. Exchangeability of trait
labels under the diagnostic null is conceptual; experimental trait labels
are not random, and source β estimates are correlated and uncertain.

Data: Caruso et al. (2020) original Dryad 10.5061/dryad.sn02v6x0q,
frozen 137-pair source matched ledger in this repo; NO new field data.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from fractions import Fraction
import hashlib
import json
from math import comb, isfinite, lcm
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
BASE_GROUP_FIELDS=(
    "paper_id","species","source_context","fitness_component",
    "fitness_measure","source_agent","treatment1_name","treatment2_name"
)
N_FROZEN_PAIRS=137
N_FROZEN_PAPERS=26
N_FROZEN_SAME_SIGN=96
N_FROZEN_POINT_SIGN_FLIP=41


def read_source(path:Path):
    with path.open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream))


def group_key(row,keys=BASE_GROUP_FIELDS):
    return tuple(row.get(name,"") for name in keys)


def source_audit(rows):
    if len(rows)!=N_FROZEN_PAIRS:
        raise ValueError("2020 original matched source denominator drift")
    if len({x["paper_id"] for x in rows}) != N_FROZEN_PAPERS:
        raise ValueError("original study count drift")
    keys=set()
    same=flips=0
    for r in rows:
        k=(r["paper_id"],r["source_row_id_1"],r["source_row_id_2"])
        if k in keys:
            raise ValueError("original source row IDs duplicated")
        keys.add(k)
        for field in BASE_GROUP_FIELDS+("trait","trait_class"):
            if not r.get(field):
                raise ValueError("blank original source grouping key "+field)
        b1,b2,se1,se2=(float(r[k]) for k in ("beta1","beta2","se1","se2"))
        if not all(isfinite(x) for x in (b1,b2,se1,se2)):
            raise ValueError("source beta or SE not finite")
        if not (se1>0 and se2>0 and b1!=0 and b2!=0):
            raise ValueError("unexpected source coefficient zero or missing SE")
        if ((b1*b2<0) != (r["point_sign_flip"].lower()=="true")):
            raise ValueError("source-sign ledger differs from source beta")
        same += b1*b2>0
        flips += b1*b2<0
    if (same,flips)!=(N_FROZEN_SAME_SIGN,N_FROZEN_POINT_SIGN_FLIP):
        raise ValueError("published 137-source directional classification drift")


def select_matched_trait_blocks(rows):
    groups=defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)
    selected,excluded_repeat,excluded_single=[],[],[]
    for key,items in sorted(groups.items()):
        distinct={x["trait"] for x in items}
        if len(items)<2:
            excluded_single.extend(items)
        elif len(items)!=len(distinct):
            # Repeated trait labels imply multiple non-exchangeable cohorts.
            excluded_repeat.extend(items)
        else:
            selected.append(items)
    if len(selected)!=11 or len({x[0]["paper_id"] for x in selected})!=10:
        raise ValueError("original homogeneous distinct-trait source grouping drift")
    if sum(len(g) for g in selected)!=43:
        raise ValueError("original distinct-trait matched-source-pair denominator drift")
    if len(excluded_repeat)+len(excluded_single)+43!=137:
        raise ValueError("excluded source rows do not reconcile")
    return selected,{
        "all_original_homogeneous_context_blocks":len(groups),
        "repeated_trait_blocks_excluded_as_cohort_ambiguous_pairs":len(excluded_repeat),
        "one_trait_blocks_excluded_as_nonpermutable_pairs":len(excluded_single),
        "selected_blocks":len(selected),
        "selected_original_papers":len({x[0]["paper_id"] for x in selected}),
        "selected_original_pairs":sum(len(g) for g in selected),
    }


def sign_indicator(row):
    return float(row["beta1"])*float(row["beta2"])>0


def block_distribution(block):
    """Exact fixed-margins hypergeometric distribution of same-sign matches.

    If β1 has n1 positive signs, and β2 has n2 positives on n trait labels,
    random re-pairing β2 positions gives K overlap-positive
    ~ Hypergeom(n,n1,n2), same count = n-n1-n2+2K.
    """
    n=len(block)
    pos1=sum(float(r["beta1"])>0 for r in block)
    pos2=sum(float(r["beta2"])>0 for r in block)
    out={}
    den=comb(n,pos2)
    for k in range(max(0,pos1+pos2-n),min(pos1,pos2)+1):
        c=n-pos1-pos2+2*k
        out[c]=out.get(c,Fraction())+Fraction(
            comb(pos1,k)*comb(n-pos1,pos2-k),den)
    if sum(out.values()) != 1:
        raise ValueError("source-margins permutation probability invalid")
    obs=sum(sign_indicator(r) for r in block)
    expected=Fraction(pos1*pos2+(n-pos1)*(n-pos2),n)
    return {"n":n,"obs":obs,"expected":expected,"pmf":out,
            "n_positive_beta1":pos1,"n_positive_beta2":pos2}


def convolve(a,b):
    d=defaultdict(Fraction)
    for x,p in a.items():
        for y,q in b.items():
            d[x+y]+=p*q
    return dict(d)


def local_permutation(blocks):
    dist={0:Fraction(1)}
    obs=0
    exp=Fraction()
    for b in blocks:
        v=block_distribution(b)
        dist=convolve(dist,v["pmf"])
        obs+=v["obs"]
        exp+=v["expected"]
    return {"pmf":dist,"obs":obs,"expected":exp}


def probability_tail(dist,observed,expected):
    p_upper=sum((p for v,p in dist.items() if v>=observed),Fraction())
    p_two=sum((p for v,p in dist.items()
               if abs(Fraction(v)-expected)>=abs(Fraction(observed)-expected)),
              Fraction())
    return float(p_upper),float(p_two)


def summarize_plain(blocks):
    perm=local_permutation(blocks)
    one,two=probability_tail(perm["pmf"],perm["obs"],perm["expected"])
    return {"n_pairs":sum(len(g) for g in blocks),"n_blocks":len(blocks),
            "n_studies":len({g[0]["paper_id"] for g in blocks}),
            "observed_same_sign":perm["obs"],
            "permutation_expected_same_sign":float(perm["expected"]),
            "observed_same_sign_fraction":perm["obs"]/sum(len(g) for g in blocks),
            "permutation_expected_same_sign_fraction":float(perm["expected"])/sum(len(g) for g in blocks),
            "source_pair_count_excess_same_sign":float(perm["obs"]-perm["expected"]),
            "exact_upper_tail_p_conditional_label_exchangeability":one,
            "exact_two_sided_p_conditional_label_exchangeability":two,
            "conditional_null_support_size":len(perm["pmf"])}


def equal_paper_weight_permutation(blocks):
    by_paper=defaultdict(list)
    for b in blocks:
        by_paper[b[0]["paper_id"]].append(b)
    n_p={p:sum(len(b) for b in pb) for p,pb in by_paper.items()}
    common=lcm(*n_p.values())
    distribution={0:Fraction(1)}
    obs_scaled=0
    exp_scaled=Fraction()
    paper_rows=[]
    for paper,subgroups in sorted(by_paper.items(),key=lambda x:int(x[0])):
        per=local_permutation(subgroups)
        multiplier=common//n_p[paper]
        altered={multiplier*k:p for k,p in per["pmf"].items()}
        distribution=convolve(distribution,altered)
        obs_scaled+=per["obs"]*multiplier
        exp_scaled+=per["expected"]*multiplier
        paper_rows.append({
            "paper_id":paper,
            "original_pairs_in_permutable_blocks":n_p[paper],
            "observed_same_sign":per["obs"],
            "expected_same_sign_under_paper_internal_trait_repairing":float(per["expected"]),
            "observed_same_sign_fraction":per["obs"]/n_p[paper],
            "expected_same_sign_fraction":float(per["expected"])/n_p[paper],
            "excess_same_sign_fraction":float(Fraction(per["obs"]-per["expected"],n_p[paper])),
            "nondegenerate_paper_under_repairing":len(per["pmf"])>1,
        })
    one,two=probability_tail(distribution,obs_scaled,exp_scaled)
    n=len(by_paper)
    return {
        "n_papers":n,
        "paper_equal_weight_observed_same_sign_fraction":float(Fraction(obs_scaled,common*n)),
        "paper_equal_weight_expected_same_sign_fraction":float(Fraction(exp_scaled,common*n)),
        "paper_equal_weight_excess_fraction":float(Fraction(obs_scaled-exp_scaled,common*n)),
        "exact_paper_equal_upper_tail_p":one,
        "exact_paper_equal_two_sided_p":two,
        "paper_equal_permutation_lattice_common_denominator":common,
        "paper_source_receipts":paper_rows,
    }


def run(rows):
    source_audit(rows)
    blocks,grain=select_matched_trait_blocks(rows)
    full=summarize_plain(blocks)
    paper=equal_paper_weight_permutation(blocks)
    # SAME 43 pairs, but only permute treatment arm β2 signs *within trait class*.
    # Singleton class rows remain deterministic rather than being discarded.
    by_class=[]
    for b in blocks:
        classes=defaultdict(list)
        for row in b:
            classes[row["trait_class"]].append(row)
        by_class.extend(classes.values())
    class_null=summarize_plain(by_class)
    # Entire paper is omitted, including its multiple environment contexts.
    dropped={}
    for paper_id in sorted({b[0]["paper_id"] for b in blocks},key=int):
        reduced=[b for b in blocks if b[0]["paper_id"]!=paper_id]
        dropped[paper_id]=summarize_plain(reduced)
    # Two arms individually supported, same-sign, are not direct
    # author-fitted treatment interactions.
    eligible=[x for b in blocks for x in b]
    two_supported=[x for x in eligible
                   if abs(float(x["beta1"])/float(x["se1"]))>1.96
                   and abs(float(x["beta2"])/float(x["se2"]))>1.96]
    if (full["observed_same_sign"]!=35 or
        len(two_supported)!=13 or
        sum(sign_indicator(x) for x in two_supported)!=13 or
        full["n_pairs"]!=43 or
        full["n_studies"]!=10 or
        class_null["n_pairs"]!=43):
        raise ValueError("source identity or directional signal drift")
    if abs(full["exact_upper_tail_p_conditional_label_exchangeability"]-.00024112654320987653)>1e-12:
        raise ValueError("independent exact combinatorial source test changed")
    if abs(paper["exact_paper_equal_upper_tail_p"]-.00014467592592592592)>1e-12:
        raise ValueError("paper-equal exact conditional test changed")
    if abs(class_null["exact_upper_tail_p_conditional_label_exchangeability"]-.011904761904761904)>1e-12:
        raise ValueError("trait-class-constrained conditional null changed")
    if max(x["exact_upper_tail_p_conditional_label_exchangeability"] for x in dropped.values())>.00171:
        raise ValueError("leave-one-paper-out conditional robustness changed")
    return {
        "analysis":"sch_original_2020_trait_identity_sign_persistence_v1",
        "source_meta_article_doi":"10.1086/706199",
        "source_data_doi":"10.5061/dryad.sn02v6x0q",
        "n_original_unduplicated_matched_pairs_unchanged":N_FROZEN_PAIRS,
        "n_original_independent_papers_unchanged":N_FROZEN_PAPERS,
        "n_original_all_same_sign_pairs":N_FROZEN_SAME_SIGN,
        "n_original_all_point_sign_crossings":N_FROZEN_POINT_SIGN_FLIP,
        "source_homogeneous_distinct_trait_selection":grain,
        "primary_pair_sign_matching":full,
        "paper_equal_weight":paper,
        "same_cohort_trait_class_constrained_repairing":class_null,
        "leave_one_entire_paper_out":dropped,
        "eligible_two_arm_approx_nominal_supported_same_sign_count":len(two_supported),
        "eligible_two_arm_approx_nominal_supported_opposite_sign_count":0,
        "null_interpretation":"conditional_trait_label_repairing_within_original_source_cohort",
        "randomized_trait_assignment_performed":False,
        "cross_study_effect_size_meta_pooling_performed":False,
        "new_field_plants_or_source_gradients_measured":False,
        "original_trait_specific_treatment_interaction_tests_recovered_by_this_analysis":False,
        "critical_limits":[
            "permutation_is_not_a_randomization_test_of_the_ecological_treatment",
            "trait_labels_not_randomized_across_natural_populations",
            "source_published_studies_selected_not_random_species_or_literature_sample",
            "conditional_label_exchangeability_of_traits_is_a_diagnostic_assumption",
            "blocks_may_still_contain_unobserved_trait_sampling_covariance",
            "restricted_43_pair_10_paper_scope_not_137_pair_prevalence",
            "beta_signs_are_source_point_estimates_not_two_sided_reversal_certificates",
            "two_supported_arm_slopes_do_not_verify_interaction_significance",
            "paper_equal_weights_do_not_correct_source_publication_bias",
            "no_direct_same_coordinate_function_conflict_or_SCH_L",
        ],
        "status":"EXPLORATORY_SOURCE_COMPUTED_TRAIT_SIGN_IDENTITY_PERSISTS_BEYOND_CONDITIONAL_REPAIRING_NULL"
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=run(read_source(a.source))
    payload=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf-8")
    print(payload)


if __name__=="__main__":
    main()
