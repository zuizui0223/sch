from __future__ import annotations

import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

DRIVER_REGISTRY = {
    "Gymnadenia_conopsea_agent_selection": {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "context_driver": "POLLINATION_X_HERBIVORY",
        "design_class": "MANIPULATED",
    },
    "Trifolium_repens_selection_program": {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "context_driver": "POLLINATION_OR_HERBIVORY",
        "design_class": "MANIPULATED",
    },
    "Brassica_rapa_Knauer_selection_program": {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "context_driver": "CONSUMER_IDENTITY_COMBINATION",
        "design_class": "MANIPULATED",
    },
    "Lobelia_cardinalis_Bartkowska_selection_program": {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "context_driver": "POLLINATION_SUPPLEMENTATION",
        "design_class": "MANIPULATED",
    },
    "Lythrum_salicaria_Thomsen_selection_program": {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "context_driver": "DAMAGE_TREATMENT",
        "design_class": "MANIPULATED",
    },
    "Erysimum_mediohispanicum_selection_mosaic": {
        "context_family": "NATURAL_SPATIAL_MOSAIC",
        "context_driver": "POPULATION_POLLINATOR_HERBIVORY_MOSAIC",
        "design_class": "OBSERVATIONAL_SPATIAL",
    },
    "Helianthus_annuus_texanus_Mitchell_selection_program": {
        "context_family": "ANTHROPOGENIC_PROXIMITY",
        "context_driver": "NEAR_VS_FAR_CROP",
        "design_class": "OBSERVATIONAL_SPATIAL",
    },
    "Dalechampia_scandens_Perez_Barrales_selection_program": {
        "context_family": "SINGLE_CONTEXT",
        "context_driver": "NO_WITHIN_AXIS_CONTEXT_CONTRAST",
        "design_class": "SINGLE_CONTEXT",
    },
}


def _load_v10(root: Path) -> dict:
    path = root / "scripts" / "analyze_sch_h2_total_selection_direction_v10.py"
    spec = importlib.util.spec_from_file_location("sch_h2_direction_v10", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load V10 analysis from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build(root)


def _family_summary(axis_rows: list[dict], programme_rows: list[dict]) -> list[dict]:
    axis_by_family: dict[str, list[dict]] = defaultdict(list)
    prog_by_family: dict[str, list[dict]] = defaultdict(list)

    for row in axis_rows:
        axis_by_family[row["context_family"]].append(row)
    for row in programme_rows:
        prog_by_family[row["context_family"]].append(row)

    out = []
    for family in sorted(axis_by_family):
        axes = axis_by_family[family]
        progs = prog_by_family[family]
        out.append(
            {
                "context_family": family,
                "n_programmes": len(progs),
                "n_programmes_with_point_switch": sum(
                    p["n_point_switch_axes"] > 0 for p in progs
                ),
                "n_programmes_with_supported_switch": sum(
                    p["n_supported_switch_axes"] > 0 for p in progs
                ),
                "n_repeated_axes": len(axes),
                "n_point_switch_axes": sum(
                    r["point_estimate_sign_switch"] for r in axes
                ),
                "n_supported_switch_axes": sum(
                    r["uncertainty_supported_sign_switch"] for r in axes
                ),
                "n_uncertainty_unresolved_switch_axes": sum(
                    r["point_estimate_sign_switch"]
                    and r["uncertainty_unresolved"]
                    and not r["uncertainty_supported_sign_switch"]
                    for r in axes
                ),
            }
        )
    return out


def build(root: Path) -> dict:
    v10 = _load_v10(root)
    repeated = [dict(r) for r in v10["axis_rows"] if r["n_cases"] >= 2]

    missing = sorted({r["cluster"] for r in repeated} - DRIVER_REGISTRY.keys())
    if missing:
        raise ValueError(f"unregistered repeated-programme context drivers: {missing}")

    for row in repeated:
        row.update(DRIVER_REGISTRY[row["cluster"]])

    by_cluster: dict[str, list[dict]] = defaultdict(list)
    for row in repeated:
        by_cluster[row["cluster"]].append(row)

    programme_rows = []
    for cluster, rows in sorted(by_cluster.items()):
        meta = DRIVER_REGISTRY[cluster]
        programme_rows.append(
            {
                "cluster": cluster,
                **meta,
                "n_repeated_axes": len(rows),
                "n_point_switch_axes": sum(
                    r["point_estimate_sign_switch"] for r in rows
                ),
                "n_supported_switch_axes": sum(
                    r["uncertainty_supported_sign_switch"] for r in rows
                ),
                "n_uncertainty_unresolved_switch_axes": sum(
                    r["point_estimate_sign_switch"]
                    and r["uncertainty_unresolved"]
                    and not r["uncertainty_supported_sign_switch"]
                    for r in rows
                ),
            }
        )

    family_summary = _family_summary(repeated, programme_rows)
    family_lookup = {r["context_family"]: r for r in family_summary}
    biotic = family_lookup["BIOTIC_REGIME_MANIPULATION"]

    result = {
        "analysis": "sch_h2_context_driver_decomposition_v11",
        "n_repeated_axes": len(repeated),
        "n_repeated_programmes": len(programme_rows),
        "n_programmes_with_point_switch": sum(
            r["n_point_switch_axes"] > 0 for r in programme_rows
        ),
        "n_programmes_with_supported_switch": sum(
            r["n_supported_switch_axes"] > 0 for r in programme_rows
        ),
        "n_point_switch_axes": sum(
            r["point_estimate_sign_switch"] for r in repeated
        ),
        "n_supported_switch_axes": sum(
            r["uncertainty_supported_sign_switch"] for r in repeated
        ),
        "n_uncertainty_unresolved_switch_axes": sum(
            r["point_estimate_sign_switch"]
            and r["uncertainty_unresolved"]
            and not r["uncertainty_supported_sign_switch"]
            for r in repeated
        ),
        "manipulated_biotic_programmes": biotic,
        "context_family_summary": family_summary,
        "programme_rows": programme_rows,
        "status": "CONTEXT_DRIVER_DECOMPOSITION_READY_NO_FAMILY_COMPARISON",
        "claim_ceiling": [
            "programme_is_the_independent_biological_unit",
            "context_family_is_design_metadata_not_an_outcome",
            "family_counts_are_descriptive_not_prevalence_estimates",
            "no_statistical_test_of_context_family_differences",
            "spatial_mosaics_are_not_promoted_to_causal_driver_effects",
            "point_sign_switch_is_not_uncertainty_supported_reversal",
            "strict_cross_study_numeric_pooling_remains_fail_closed",
        ],
    }
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out-json", type=Path)
    args = p.parse_args()

    result = build(args.root)
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
