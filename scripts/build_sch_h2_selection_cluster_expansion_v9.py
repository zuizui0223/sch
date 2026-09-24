from __future__ import annotations
import argparse, csv, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V8=ROOT/"scripts"/"build_sch_h2_selection_cluster_expansion_v8.py"

def _v8():
    spec=importlib.util.spec_from_file_location("h2v8",V8)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod); return mod

def _read(path: Path):
    with path.open(encoding="utf-8",newline="") as h:
        return [{k:(v or "").strip() for k,v in r.items()} for r in csv.DictReader(h)]

def build(base_path, brassica_path, lobelia_path, dalechampia_path, lythrum_path, helianthus_path):
    v8=_v8()
    rows,_=v8.build(base_path,brassica_path,lobelia_path,dalechampia_path,lythrum_path)
    v7=v8._v7()
    hel=_read(helianthus_path)
    contexts=[r["context"] for r in hel]
    row=v7._measurement_row(
        prefix="Helianthus_000673",
        trait="ray_length",
        contexts=contexts,
        cluster="Helianthus_annuus_texanus_Mitchell_selection_program",
        source_id="SCHPRISMA-000673",
        source_object="Mitchell_2021_maintext_Figure3b",
        notes="Exact main-text mean direct-selection gradients beta for ray length across multi-year Sites 1/2 near-versus-far crop contexts. Traits were standardized within populations and fitness was log relative whole-plant seed production. Numeric SE for the two context means is not reported, so these rows do not enter the strict STANDARDIZED_SELECTION_GRADIENT pooling family.",
    )
    row["numeric_pooling_family"]="MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE"
    rows.append(row)

    total=v7._family(rows,"estimand_family","TOTAL_SELECTION_EFFECT")
    standardized=v7._family(rows,"numeric_pooling_family","STANDARDIZED_SELECTION_GRADIENT")
    helfam=v7._family(rows,"numeric_pooling_family","MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE")
    summary={
        "analysis":"sch_h2_selection_cluster_expansion_v9",
        "total_selection_effect":total,
        "standardized_selection_gradient":standardized,
        "helianthus_numeric_family":helfam,
        "registered_min_independent_clusters":8,
        "h2_commensurate_estimand_gate":"PASS" if total["n_clusters"]>=8 else "FAIL",
        "strict_numeric_pooling_gate":"PASS" if standardized["n_clusters"]>=8 else "FAIL",
        "remaining_cluster_deficit":max(0,8-total["n_clusters"]),
        "new_clusters":["Helianthus_annuus_texanus_Mitchell_selection_program"],
        "claim_ceiling":[
            "registered_TOTAL_SELECTION_EFFECT_estimand_family_gate_passes",
            "strict_numeric_pooling_gate_remains_fail_closed_without_context_mean_uncertainty",
            "supplementary_population_level_coefficients_not_imputed_or_digitized",
            "no_general_prevalence_claim",
        ],
    }
    return rows,summary

def _write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("base",type=Path); p.add_argument("brassica",type=Path); p.add_argument("lobelia",type=Path)
    p.add_argument("dalechampia",type=Path); p.add_argument("lythrum",type=Path); p.add_argument("helianthus",type=Path)
    p.add_argument("--out-csv",type=Path,required=True); p.add_argument("--out-json",type=Path,required=True)
    a=p.parse_args(); rows,summary=build(a.base,a.brassica,a.lobelia,a.dalechampia,a.lythrum,a.helianthus)
    _write_csv(a.out_csv,rows); a.out_json.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
