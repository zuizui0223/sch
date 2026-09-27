from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _case_ids(row: dict[str, str]) -> list[str]:
    return [value for value in row["case_ids"].split(";") if value]


def _slug(value: str) -> str:
    return value.replace("-", "_").replace(" ", "_").replace("/", "_")


def _measurement_row(
    *,
    prefix: str,
    trait: str,
    contexts: list[str],
    cluster: str,
    source_id: str,
    source_object: str,
    notes: str,
) -> dict[str, str]:
    axis = f"{prefix}_{_slug(trait)}"
    case_ids = ";".join(f"{axis}_{_slug(context)}" for context in contexts)
    return {
        "measurement_record_id": axis + "_selection",
        "evidence_id": axis + "_exact",
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


def _family(rows: list[dict[str, str]], field: str, key: str) -> dict[str, int]:
    selected = [row for row in rows if row.get(field) == key and _case_ids(row)]
    return {
        "n_cases": sum(len(_case_ids(row)) for row in selected),
        "n_axes": len({row["canonical_trait_axis_id"] for row in selected}),
        "n_clusters": len({row["cluster_id"] for row in selected}),
        "n_repeated_axes": len(
            {
                row["canonical_trait_axis_id"]
                for row in selected
                if len(_case_ids(row)) >= 2
            }
        ),
    }


def build(
    base_path: Path,
    brassica_path: Path,
    lobelia_path: Path,
    dalechampia_path: Path | None = None,
    lythrum_path: Path | None = None,
    helianthus_path: Path | None = None,
):
    rows = _read(base_path)
    base_axes = {row["canonical_trait_axis_id"] for row in rows}
    base_clusters = {row["cluster_id"] for row in rows}
    added_cases = 0

    brassica = _read(brassica_path)
    added_cases += len(brassica)
    for trait in sorted({row["trait"] for row in brassica}):
        contexts = [
            row["consumer_regime"] for row in brassica if row["trait"] == trait
        ]
        rows.append(
            _measurement_row(
                prefix="Brassica_000775",
                trait=trait,
                contexts=contexts,
                cluster="Brassica_rapa_Knauer_selection_program",
                source_id="SCHPRISMA-000775",
                source_object="Knauer_2017_Table2",
                notes=(
                    "Exact standardized directional selection gradients beta plus SE "
                    "across three consumer regimes using relative seed set."
                ),
            )
        )

    lobelia = _read(lobelia_path)
    added_cases += len(lobelia)
    for trait in sorted({row["trait"] for row in lobelia}):
        contexts = [
            row["pollination_context"] for row in lobelia if row["trait"] == trait
        ]
        rows.append(
            _measurement_row(
                prefix="Lobelia_000659",
                trait=trait,
                contexts=contexts,
                cluster="Lobelia_cardinalis_Bartkowska_selection_program",
                source_id="SCHPRISMA-000659",
                source_object="Bartkowska_2012_Table2",
                notes=(
                    "Exact standardized directional selection gradients beta plus SE "
                    "under natural versus supplemental hand pollination using relative "
                    "seed number."
                ),
            )
        )

    if dalechampia_path is not None:
        dalechampia = _read(dalechampia_path)
        net_rows = [
            row for row in dalechampia if row["selection_component"] == "NET"
        ]
        added_cases += len(net_rows)
        for trait in sorted({row["trait"] for row in net_rows}):
            rows.append(
                _measurement_row(
                    prefix="Dalechampia_000658",
                    trait=trait,
                    contexts=["NET_FITNESS_SURFACE"],
                    cluster="Dalechampia_scandens_Perez_Barrales_selection_program",
                    source_id="SCHPRISMA-000658",
                    source_object="Perez_Barrales_2013_Table4",
                    notes=(
                        "Mean-standardized net selection gradient on relative seeds "
                        "surviving predation; source also decomposes pollinator and "
                        "seed-predator selection for upper bract area."
                    ),
                )
            )

    if lythrum_path is not None:
        lythrum = _read(lythrum_path)
        totals = [
            row for row in lythrum if row["estimand_role"] == "TOTAL_SELECTION"
        ]
        added_cases += len(totals)
        for trait in sorted({row["trait"] for row in totals}):
            contexts = [
                row["context_or_contrast"]
                for row in totals
                if row["trait"] == trait
            ]
            rows.append(
                _measurement_row(
                    prefix="Lythrum_000284",
                    trait=trait,
                    contexts=contexts,
                    cluster="Lythrum_salicaria_Thomsen_selection_program",
                    source_id="SCHPRISMA-000284",
                    source_object="Thomsen_2017_Table2",
                    notes=(
                        "Exact standardized linear selection gradients beta plus SE "
                        "under clipped versus control herbivory contexts using relative "
                        "total seed production. Pollination-mediated delta-beta "
                        "contrasts are preserved in the source freeze but are not "
                        "counted as total-selection cases."
                    ),
                )
            )

    if helianthus_path is not None:
        helianthus = _read(helianthus_path)
        contexts = [row["context"] for row in helianthus]
        added_cases += len(helianthus)
        row = _measurement_row(
            prefix="Helianthus_000673",
            trait="ray_length",
            contexts=contexts,
            cluster="Helianthus_annuus_texanus_Mitchell_selection_program",
            source_id="SCHPRISMA-000673",
            source_object="Mitchell_2021_maintext_Figure3b",
            notes=(
                "Exact main-text mean direct-selection gradients beta for ray length "
                "across multi-year Sites 1/2 near-versus-far crop contexts. Traits "
                "were standardized within populations and fitness was log relative "
                "whole-plant seed production. Numeric SE for the two context means is "
                "not reported, so these rows do not enter the strict "
                "STANDARDIZED_SELECTION_GRADIENT pooling family."
            ),
        )
        row["numeric_pooling_family"] = "MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE"
        rows.append(row)

    total = _family(rows, "estimand_family", "TOTAL_SELECTION_EFFECT")
    standardized = _family(
        rows, "numeric_pooling_family", "STANDARDIZED_SELECTION_GRADIENT"
    )
    helianthus_family = _family(
        rows,
        "numeric_pooling_family",
        "MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE",
    )
    new_axes = {row["canonical_trait_axis_id"] for row in rows} - base_axes
    new_clusters = {row["cluster_id"] for row in rows} - base_clusters

    summary = {
        "analysis": "sch_h2_selection_cluster_expansion",
        "added_cases": added_cases,
        "added_axes": len(new_axes),
        "added_clusters": len(new_clusters),
        "new_clusters": sorted(new_clusters),
        "total_selection_effect": total,
        "standardized_selection_gradient": standardized,
        "registered_min_independent_clusters": 8,
        "h2_commensurate_estimand_gate": (
            "PASS" if total["n_clusters"] >= 8 else "FAIL"
        ),
        "strict_numeric_pooling_gate": (
            "PASS" if standardized["n_clusters"] >= 8 else "FAIL"
        ),
        "remaining_cluster_deficit": max(0, 8 - total["n_clusters"]),
        "claim_ceiling": [
            "source_resolved_selection_gradients_added",
            "mediated_delta_beta_contrasts_not_counted_as_total_selection_cases",
            "mean_context_gradients_without_uncertainty_excluded_from_strict_numeric_pooling",
            "no_general_prevalence_claim",
        ],
    }
    if helianthus_path is not None:
        summary["helianthus_numeric_family"] = helianthus_family

    return rows, summary


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("brassica", type=Path)
    parser.add_argument("lobelia", type=Path)
    parser.add_argument("--dalechampia", type=Path)
    parser.add_argument("--lythrum", type=Path)
    parser.add_argument("--helianthus", type=Path)
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()

    rows, summary = build(
        args.base,
        args.brassica,
        args.lobelia,
        args.dalechampia,
        args.lythrum,
        args.helianthus,
    )
    _write_csv(args.out_csv, rows)
    args.out_json.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
