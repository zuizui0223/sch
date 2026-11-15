"""Source-author hurdle stage interactions versus compilation's total-seed gradients."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
STAGE = ROOT / "data/SCH_2020_WADGYMAR_AUTHOR_STAGE_INTERACTIONS_V1.csv"
TOTAL = ROOT / "data/SCH_2020_WADGYMAR_LANDE_ARNOLD_SOURCE_ALIGNMENT_V1.csv"
FROZEN = {
    ("Flowering onset", "SURVIVAL"): ("NOT_REPORTED", "NS", -.80, .65, -1.10, .84),
    ("Flowering onset", "SEED_COUNT"): ("6.99", "P_LT_0.01", -.45, .23, -.19, .21),
    ("Fruiting onset", "SURVIVAL"): ("NOT_TESTED", "NOT_TESTED", None, None, None, None),
    ("Fruiting onset", "SEED_COUNT"): ("NOT_REPORTED", "NS", -.69, .14, -.51, .17),
    ("Biomass", "SURVIVAL"): ("6.77", "P_LT_0.01", .25, .33, 1.72, .64),
    ("Biomass", "SEED_COUNT"): ("NOT_REPORTED", "NS", 1.00, .14, .90, .10),
}
FROZEN_TOTAL = {
    "Flowering onset": (351, 354, -.89, .19, -.13, .21),
    "Fruiting onset": (352, 355, -.45, .15, -.58, .18),
    "Biomass": (353, 356, 1.21, .18, .81, .10),
}


def csv_rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def near(a, b):
    return abs(float(a)-b) < 1e-10


def run(meta, stage, total):
    if len(meta) != 137 or len(stage) != 6 or len(total) != 3:
        raise ValueError("frozen 137/6/3 source denominator changed")
    eligible = {(r["paper_id"], r["source_row_id_1"], r["source_row_id_2"]):r for r in meta}
    if len(eligible) != 137:
        raise ValueError("duplicate matched source rows")
    total_seen = set()
    for row in total:
        trait = row["trait"]
        if trait not in FROZEN_TOTAL or trait in total_seen:
            raise ValueError("unexpected or duplicated source total-selection trait")
        total_seen.add(trait)
        a,b,c,d,e,f=FROZEN_TOTAL[trait]
        orig=eligible.get(("29",str(a),str(b)))
        if (orig is None or orig["trait"] != trait or row["paper_id"] != "29" or
            row["source_row_id_1"] != str(a) or row["source_row_id_2"] != str(b) or
            row["original_compilation_family"] != "LINEAR_RELATIVE_TOTAL_SEED" or
            row["original_table"] != "Table4_MultipleRegression"):
            raise ValueError("wrong original-total-beta source or model family")
        for rcol, original_col, expected in (
            ("beta_ambient", "beta1", c), ("se_ambient", "se1", d),
            ("beta_heated", "beta2", e), ("se_heated", "se2", f)):
            if not near(row[rcol],expected) or not near(orig[original_col],expected):
                raise ValueError("published relative-fitness beta source drift")
    if total_seen != set(FROZEN_TOTAL):
        raise ValueError("missing total-selection original trait")

    stage_seen, summary = set(), []
    for row in stage:
        key=(row["trait"],row["fitness_stage"])
        if key not in FROZEN or key in stage_seen:
            raise ValueError("wrong or repeated author-fitted hurdle model stage")
        stage_seen.add(key)
        sig, level, *coefficients=FROZEN[key]
        a,b,*_=FROZEN_TOTAL[row["trait"]]
        if (row["paper_id"] != "29" or row["doi"] != "10.1111/gcb.12988" or
            row["source_row_id_1"] != str(a) or row["source_row_id_2"] != str(b) or
            row["source_location"] != "Table3_Table4" or
            row["interaction_chi2"] != sig or
            row["interaction_significance"] != level or row["interaction_df"] != "1" or
            row["source_link"] != ("HURDLE_LOGIT" if key[1] == "SURVIVAL" else "HURDLE_NEG_BIN_LOG")):
            raise ValueError("source hurdle interaction provenance changed")
        for col, expected in zip(("beta_ambient", "se_ambient", "beta_heated", "se_heated"),coefficients):
            if expected is None:
                if row[col] != "NA":
                    raise ValueError("inapplicable fruiting/survival outcome populated")
            elif not near(row[col], expected):
                raise ValueError("source hurdle slope drift")
        summary.append({"trait":key[0],"fitness_stage":key[1],
                        "original_author_chi2":sig,"interaction_support":level,
                        "direct_model_family":row["source_link"]})
    if stage_seen != set(FROZEN):
        raise ValueError("missing source stage")
    supported={(x["trait"],x["fitness_stage"]) for x in summary if x["interaction_support"]=="P_LT_0.01"}
    expected_support={("Flowering onset","SEED_COUNT"),("Biomass","SURVIVAL")}
    if supported != expected_support:
        raise ValueError("stage-specific interaction pattern lost")
    return {"analysis":"sch_wadgymar_author_fitted_stage_context_v1",
            "doi":"10.1111/gcb.12988","original_programmes":1,
            "n_source_matched_total_seed_traits":3,
            "n_original_hurdle_stage_cells":6,"n_applicable_interaction_cells":5,
            "n_source_reported_p_lt_0_01_interactions":2,
            "supported_trait_stage_pairs":sorted([list(k) for k in supported]),
            "source_hurdle_stage_summary":sorted(summary,key=lambda x:(x["trait"],x["fitness_stage"])),
            "source_total_selection_and_hurdle_model_families_must_not_be_pooled":True,
            "source_total_seed_coefficients_preserved":True,
            "supported_interaction_does_not_certify_two_nonzero_opposite_slopes":True,
            "no_new_SCH_L_or_pure_function_optimum":True,
            "status":"SECOND_INDEPENDENT_PAPER_STAGE_SPECIFIC_SELECTION_MODERATION__NO_COMMON_META_ESTIMAND"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--meta",type=Path,default=META)
    p.add_argument("--stage",type=Path,default=STAGE)
    p.add_argument("--total",type=Path,default=TOTAL)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=run(csv_rows(a.meta),csv_rows(a.stage),csv_rows(a.total))
    report=json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(report,encoding="utf-8")
    print(report)

if __name__=="__main__":
    main()
