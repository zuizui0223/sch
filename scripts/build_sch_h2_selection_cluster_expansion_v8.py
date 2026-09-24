from __future__ import annotations
import argparse, csv, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V7=ROOT/"scripts"/"build_sch_h2_selection_cluster_expansion_v7.py"

def _v7():
    spec=importlib.util.spec_from_file_location("h2v7",V7)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod); return mod

def _read(path: Path):
    with path.open(encoding="utf-8",newline="") as h:
        return [{k:(v or "").strip() for k,v in r.items()} for r in csv.DictReader(h)]

def build(base_path, brassica_path, lobelia_path, dalechampia_path, lythrum_path):
    v7=_v7()
    rows,_=v7.build(base_path,brassica_path,lobelia_path,dalechampia_path)
    base=_read(base_path)
    base_axes={r["canonical_trait_axis_id"] for r in base}
    base_clusters={r["cluster_id"] for r in base}

    lyr=_read(lythrum_path)
    totals=[r for r in lyr if r["estimand_role"]=="TOTAL_SELECTION"]
    for trait in sorted({r["trait"] for r in totals}):
        contexts=[r["context_or_contrast"] for r in totals if r["trait"]==trait]
        rows.append(v7._measurement_row(
            prefix="Lythrum_000284",
            trait=trait,
            contexts=contexts,
            cluster="Lythrum_salicaria_Thomsen_selection_program",
            source_id="SCHPRISMA-000284",
            source_object="Thomsen_2017_Table2",
            notes="Exact standardized linear selection gradients beta plus SE under clipped versus control herbivory contexts using relative total seed production. Pollination-mediated delta-beta contrasts are preserved in the source freeze but are not counted as total-selection cases.",
        ))

    total=v7._family(rows,"estimand_family","TOTAL_SELECTION_EFFECT")
    standardized=v7._family(rows,"numeric_pooling_family","STANDARDIZED_SELECTION_GRADIENT")
    new_axes={r["canonical_trait_axis_id"] for r in rows}-base_axes
    new_clusters={r["cluster_id"] for r in rows}-base_clusters
    summary={
        "analysis":"sch_h2_selection_cluster_expansion_v8",
        "added_cases":49,
        "added_axes":len(new_axes),
        "added_clusters":len(new_clusters),
        "new_clusters":sorted(new_clusters),
        "total_selection_effect":total,
        "standardized_selection_gradient":standardized,
        "registered_min_independent_clusters":8,
        "h2_commensurate_estimand_gate":"PASS" if total["n_clusters"]>=8 else "FAIL",
        "remaining_cluster_deficit":max(0,8-total["n_clusters"]),
        "claim_ceiling":[
            "lythrum_total_gradients_are_standardized_trait_relative_fitness_coefficients",
            "mediated_delta_beta_contrasts_not_counted_as_total_selection_cases",
            "no_h2_numeric_model_until_registered_cluster_gate_passes",
        ],
    }
    return rows,summary

def _write_csv(path,rows):
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("base",type=Path); p.add_argument("brassica",type=Path); p.add_argument("lobelia",type=Path)
    p.add_argument("dalechampia",type=Path); p.add_argument("lythrum",type=Path)
    p.add_argument("--out-csv",type=Path,required=True); p.add_argument("--out-json",type=Path,required=True)
    a=p.parse_args(); rows,summary=build(a.base,a.brassica,a.lobelia,a.dalechampia,a.lythrum)
    _write_csv(a.out_csv,rows); a.out_json.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
