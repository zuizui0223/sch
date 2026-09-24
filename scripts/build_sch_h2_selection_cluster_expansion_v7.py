from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as h:
        return [{k:(v or "").strip() for k,v in r.items()} for r in csv.DictReader(h)]

def _case_ids(row: dict[str,str]) -> list[str]:
    return [x for x in row["case_ids"].split(";") if x]

def _slug(value: str) -> str:
    return value.replace("-", "_").replace(" ", "_").replace("/", "_")

def _measurement_row(*, prefix: str, trait: str, contexts: list[str], cluster: str, source_id: str, source_object: str, notes: str) -> dict[str,str]:
    axis=f"{prefix}_{_slug(trait)}"
    case_ids=";".join(f"{axis}_{_slug(c)}" for c in contexts)
    return {
        "measurement_record_id": axis+"_selection",
        "evidence_id": axis+"_exact",
        "case_ids": case_ids,
        "canonical_trait_axis_id": axis,
        "cluster_id": cluster,
        "source_id": source_id,
        "context_scope": ";".join(contexts),
        "n_contexts_reported": str(len(contexts)),
        "n_contexts_function1_reported": str(len(contexts)),
        "n_contexts_function2_reported": str(len(contexts)),
        "n_contexts_individual_linked": str(len(contexts)),
        "highest_source_supported_layer": "LOCAL_NET_SELECTION",
        "highest_materialized_layer": "LOCAL_NET_SELECTION",
        "local_geometry_cases_materialized": "0",
        "local_net_selection_cases_materialized": str(len(contexts)),
        "local_antagonist_pressure_cases_materialized": "0",
        "source_object_ids": source_object,
        "next_promotion_target": "NONE",
        "notes": notes,
        "estimand_family": "TOTAL_SELECTION_EFFECT",
        "numeric_pooling_family": "STANDARDIZED_SELECTION_GRADIENT",
    }

def _family(rows: list[dict[str,str]], field: str, key: str) -> dict[str,int]:
    selected=[r for r in rows if r[field] == key and _case_ids(r)]
    return {
        "n_cases": sum(len(_case_ids(r)) for r in selected),
        "n_axes": len({r["canonical_trait_axis_id"] for r in selected}),
        "n_clusters": len({r["cluster_id"] for r in selected}),
        "n_repeated_axes": len({r["canonical_trait_axis_id"] for r in selected if len(_case_ids(r)) >= 2}),
    }

def build(base_path: Path, brassica_path: Path, lobelia_path: Path, dalechampia_path: Path | None = None):
    rows=_read(base_path)
    base_axes={r["canonical_trait_axis_id"] for r in rows}
    base_clusters={r["cluster_id"] for r in rows}

    brassica=_read(brassica_path)
    btraits=sorted({r["trait"] for r in brassica})
    for trait in btraits:
        contexts=[r["consumer_regime"] for r in brassica if r["trait"] == trait]
        rows.append(_measurement_row(
            prefix="Brassica_000775", trait=trait, contexts=contexts,
            cluster="Brassica_rapa_Knauer_selection_program", source_id="SCHPRISMA-000775",
            source_object="Knauer_2017_Table2",
            notes="Exact standardized directional selection gradients beta plus SE across three consumer regimes using relative seed set.",
        ))

    lobelia=_read(lobelia_path)
    ltraits=sorted({r["trait"] for r in lobelia})
    for trait in ltraits:
        contexts=[r["pollination_context"] for r in lobelia if r["trait"] == trait]
        rows.append(_measurement_row(
            prefix="Lobelia_000659", trait=trait, contexts=contexts,
            cluster="Lobelia_cardinalis_Bartkowska_selection_program", source_id="SCHPRISMA-000659",
            source_object="Bartkowska_2012_Table2",
            notes="Exact standardized directional selection gradients beta plus SE under natural versus supplemental hand pollination using relative seed number.",
        ))

    if dalechampia_path is not None:
        dalechampia=_read(dalechampia_path)
        for trait in sorted({r["trait"] for r in dalechampia}):
            net=[r for r in dalechampia if r["trait"] == trait and r["selection_component"] == "NET"]
            if not net:
                continue
            rows.append(_measurement_row(
                prefix="Dalechampia_000658", trait=trait, contexts=["NET_FITNESS_SURFACE"],
                cluster="Dalechampia_scandens_Perez_Barrales_selection_program", source_id="SCHPRISMA-000658",
                source_object="Perez_Barrales_2013_Table4",
                notes="Mean-standardized net selection gradient on relative seeds surviving predation; source also decomposes pollinator and seed-predator selection for upper bract area.",
            ))

    total=_family(rows,"estimand_family","TOTAL_SELECTION_EFFECT")
    standardized=_family(rows,"numeric_pooling_family","STANDARDIZED_SELECTION_GRADIENT")
    new_axes={r["canonical_trait_axis_id"] for r in rows}-base_axes
    new_clusters={r["cluster_id"] for r in rows}-base_clusters
    summary={
        "analysis":"sch_h2_selection_cluster_expansion_v7",
        "added_cases": len(brassica)+len(lobelia)+(sum(1 for r in _read(dalechampia_path) if r["selection_component"] == "NET") if dalechampia_path is not None else 0),
        "added_axes": len(new_axes),
        "added_clusters": len(new_clusters),
        "new_clusters": sorted(new_clusters),
        "total_selection_effect": total,
        "standardized_selection_gradient": standardized,
        "registered_min_independent_clusters": 8,
        "h2_commensurate_estimand_gate": "PASS" if total["n_clusters"] >= 8 else "FAIL",
        "remaining_cluster_deficit": max(0,8-total["n_clusters"]),
        "claim_ceiling":[
            "source_resolved_standardized_selection_gradients_added",
            "no_general_prevalence_claim",
            "no_h2_numeric_model_until_registered_cluster_gate_passes",
        ],
    }
    return rows, summary

def _write_csv(path: Path, rows: list[dict[str,str]]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("base",type=Path); p.add_argument("brassica",type=Path); p.add_argument("lobelia",type=Path); p.add_argument("--dalechampia",type=Path)
    p.add_argument("--out-csv",type=Path,required=True); p.add_argument("--out-json",type=Path,required=True)
    a=p.parse_args(); rows,summary=build(a.base,a.brassica,a.lobelia,a.dalechampia)
    _write_csv(a.out_csv,rows)
    a.out_json.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
