"""SCH Am Nat Major Article soft-format and ecological source-to-claim audit.

Source of format thresholds: the journal's current Instructions for Authors:
https://www.journals.uchicago.edu/journals/an/instruct
Major Article guideline: abstract <= 200 words; text ordinarily <= 7500
words, excluding literature cited; at most 6 figures and/or tables.
Using the full editable Markdown file as a conservative word-count proxy
(including its abstract/headings/Markdown tokens) avoids undercounting.

This checks article readiness only in these limited dimensions. It does
NOT mean figures, literature references, anonymization or editorial
submission are complete. Figures are currently a storyboard, not 5
camera-ready figures. The original SCH 16-cluster source universe is not
re-estimated here.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"
FIGURE_MAP=ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md"
PATTERN=ROOT/"data/SCH_PATTERN_LEDGER_V1.csv"
GYM=ROOT/"data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
LYTHRUM_PHENOTYPE=ROOT/"data/SCH_LYTHRUM_THOMSEN_2017_TREATMENT_MEANS_TABLE1_V1.csv"
LYTHRUM_SELECTION=ROOT/"data/SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv"
BRASSICA_BEHAVIOUR=ROOT/"data/SCH_BRASSICA_2017_RECEIVER_BEHAVIOUR_TABLE1_V1.csv"
BRASSICA_SELECTION=ROOT/"data/SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv"
PEDICULARIS=ROOT/"data/PEDICULARIS_2015_CROSS_ENDPOINT_TABLE2_V1.csv"
JOURNAL="The American Naturalist"
ABSTRACT_LIMIT=200
MAJOR_ARTICLE_WORD_TARGET=7500
COMBINED_FIGURE_TABLE_LIMIT=6


def source(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream))


def unique(rows:list[dict[str,str]],**match:str)->dict[str,str]:
    found=[r for r in rows if all(r.get(k)==v for k,v in match.items())]
    if len(found)!=1:
        raise ValueError("original source row not uniquely found: "+repr(match))
    return found[0]


def wordcount(text:str)->int:
    return len(text.split())


def _close(s:str,expected:float)->bool:
    return abs(float(s)-expected)<1e-9


def original_biological_numbers()->dict:
    gym=source(GYM)
    g_open=unique(gym,trait="flowering_start",treatment="C+E")
    g_hand=unique(gym,trait="flowering_start",treatment="HP+E")
    if (not _close(g_open["beta"],.094) or not _close(g_hand["beta"],-.066)
        or g_open["herbivory_state"]!="HERBIVORES_EXCLUDED"
        or g_hand["herbivory_state"]!="HERBIVORES_EXCLUDED"):
        raise ValueError("Gymnadenia source phenotype selection drift")
    l_pheno=source(LYTHRUM_PHENOTYPE)
    inf=unique(l_pheno,trait="number_of_inflorescences")
    if (not _close(inf["control_mean"],5.4)
        or not _close(inf["clipped_mean"],8.0)):
        raise ValueError("Lythrum source average phenotype drift")
    lsel=source(LYTHRUM_SELECTION)
    clip=unique(lsel,trait="number_of_inflorescences",context_or_contrast="CLIPPED")
    control=unique(lsel,trait="number_of_inflorescences",context_or_contrast="CONTROL")
    if (not _close(clip["beta_or_delta"],.20)
        or not _close(control["beta_or_delta"],.47)):
        raise ValueError("Lythrum source gradient drift")
    beh=source(BRASSICA_BEHAVIOUR)
    corolla=unique(beh,trait="corolla_size",receiver_response="CABBAGE_BUTTERFLY_OVIPOSITION")
    if not _close(corolla["beta"],.45) or corolla["source_p"]!="0.006":
        raise ValueError("Brassica original oviposition association drift")
    seed=source(BRASSICA_SELECTION)
    cells=[unique(seed,trait="corolla_size",consumer_regime=r) for r in (
        "BUMBLE_BEE","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY",
        "CABBAGE_BUTTERFLY",
    )]
    if [float(x["beta"]) for x in cells]!=[.22,.22,.26]:
        raise ValueError("Brassica original seed fitness gradients drift")
    pred=source(PEDICULARIS)
    attack=unique(pred,endpoint="seed_predation",term="SITE_X_TREATMENT")
    final=unique(pred,endpoint="final_seed_set",term="SITE_X_TREATMENT")
    if not _close(attack["reported_chi2"],36.782) or final["reported_p"]!="0.4265":
        raise ValueError("Pedicularis endpoint-heterogeneity tests drift")
    return {
        "Gymnadenia_fixed_herbivory_open_hand_beta":[.094,-.066],
        "Lythrum_control_clipped_inflorescence_mean":[5.4,8.0],
        "Lythrum_control_clipped_inflorescence_selection_beta":[.47,.20],
        "Brassica_butterfly_oviposition_corolla_beta":.45,
        "Brassica_corolla_seed_selection_all_regimes":[.22,.22,.26],
        "Pedicularis_attack_site_interaction_chi2":36.782,
        "Pedicularis_final_seed_site_interaction_source_p":"0.4265",
    }


def build(paper:str,figure_map:str)->dict:
    if paper.count("## Abstract\n")!=1 or paper.count("**Keywords:**")!=1:
        raise ValueError("unique manuscript abstract and keyword boundary required")
    abstract=paper.split("## Abstract\n",1)[1].split("**Keywords:**",1)[0].strip()
    abstract_words=wordcount(abstract)
    paper_words=wordcount(paper)
    if abstract_words>ABSTRACT_LIMIT:
        raise ValueError(f"Am Nat Major Article abstract {abstract_words}>{ABSTRACT_LIMIT}")
    if paper_words>MAJOR_ARTICLE_WORD_TARGET:
        raise ValueError(f"Am Nat soft major-article word target {paper_words}>{MAJOR_ARTICLE_WORD_TARGET}")
    figures=re.findall(r"^## Figure ([0-9]+)\b",figure_map,flags=re.MULTILINE)
    unique_figures={int(i) for i in figures}
    if len(figures)!=len(unique_figures) or unique_figures!=set(range(1,6)):
        raise ValueError("expected 5 distinct schematic figures; verify figure map")
    table_lines=re.findall(r"^\|[^\n]+\|$",paper,flags=re.MULTILINE)
    table_starts=sum("Context-sensitive link" in x for x in table_lines)
    if table_starts!=1:
        raise ValueError("source-backed ecological Table 1 missing or duplicated")
    table_number=1
    if len(figures)+table_number>COMBINED_FIGURE_TABLE_LIMIT:
        raise ValueError("Am Nat combined tables/figures threshold crossed")
    if len(source(PATTERN))!=16:
        raise ValueError("published source universe changed without a new review")
    for anchor in (
        "### 7.6 A focal biological anchor:",
        "### 7.7 Experimentally changing one ecological input",
        "### 7.8 Independent pollination-treatment programmes",
        "### 7.9 From a striking reversal",
        "### 7.10 Compensation and phenological debt",
        "### 7.11 Stage-dependent ecological roles",
        "### 7.12 A unifying ecological test",
        "do **not** constitute one crossed",
        "none can be promoted to a measured L",
        "These alternatives are hypotheses",
    ):
        if anchor not in paper:
            raise ValueError("missing ecological causal-ceiling claim "+anchor)
    return {
        "analysis":"sch_amnat_major_article_science_format_v1",
        "target_journal":JOURNAL,
        "current_official_instructions":"https://www.journals.uchicago.edu/journals/an/instruct",
        "article_type":"Major Article (target, not accepted/submitted)",
        "full_markdown_whitespace_word_proxy":paper_words,
        "abstract_whitespace_word_proxy":abstract_words,
        "word_proxy_is_not_journal_final_rendered_count":True,
        "abstract_word_limit":ABSTRACT_LIMIT,
        "soft_full_article_word_target":MAJOR_ARTICLE_WORD_TARGET,
        "figure_map_described_figures":len(figures),
        "new_ecological_synthesis_tables_in_manuscript":table_number,
        "combined_figure_table_limit":COMBINED_FIGURE_TABLE_LIMIT,
        "original_16_cluster_ledger_unchanged":True,
        "source_verified_cross_system_individual_figures":original_biological_numbers(),
        "submission_ready":False,
        "remaining_before_submission":[
            "five_camera_ready_figures_not_created_by_this_audit",
            "journal_formatted_literature_cited_and_article_type_positioning_not_certified",
            "author_metadata_and_ethics_or_data_statements_not_checked",
            "full manuscript source-by-source journal stylistic review pending",
        ],
        "science_claim_boundary":[
            "source-selected_four_system_synthesis_is_not_replicated_causal_mechanism",
            "sign_of_receiver_attraction_is_not_sign_of_final_seed_fitness_selection",
            "phenotype_change_not_identical_to_selection_gradient_change",
            "cross_endpoint_nondetection_not_effect_equality",
            "trait_and_consumer_z_x_P_x_G_factorial_outcome_absent",
            "no_empirical_SCH_L_or_Slk_architecture_value",
        ],
        "status":"AMNAT_LENGTH_GATES_MET_SOURCE_ANCHORS_VERIFIED_NOT_YET_SUBMISSION_READY",
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manuscript",type=Path,default=PAPER)
    ap.add_argument("--figures",type=Path,default=FIGURE_MAP)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    report=build(
        args.manuscript.read_text(encoding="utf-8"),
        args.figures.read_text(encoding="utf-8"),
    )
    payload=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")


if __name__=="__main__":
    main()
