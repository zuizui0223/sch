from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V10 = ROOT / "scripts" / "analyze_sch_h2_total_selection_direction_v10.py"

MECHANISM_ORDER = (
    "MIXED_POLLINATION_X_HERBIVORY",
    "POLLINATION_SUPPLEMENTATION",
    "HERBIVORY_REDUCTION",
    "SPATIAL_MULTI_AGENT_MOSAIC",
    "CONSUMER_IDENTITY_COMPOSITION",
    "ANTAGONIST_DAMAGE_MANIPULATION",
    "LANDSCAPE_CROP_PROXIMITY",
    "SINGLE_NET_CONTEXT",
)

EVIDENCE_LEVELS = (
    "NO_POINT_REVERSAL",
    "POINT_REVERSAL_BOTH_SIDES_UNSUPPORTED",
    "POINT_REVERSAL_ONE_SIDE_SUPPORTED",
    "POINT_REVERSAL_BIDIRECTIONAL_SUPPORTED",
    "POINT_REVERSAL_UNCERTAINTY_UNRESOLVED",
)


def _load_v10():
    spec = importlib.util.spec_from_file_location("sch_h2_direction_v10", V10)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _mechanism(axis: str, cluster: str) -> tuple[str, str]:
    if cluster == "Gymnadenia_conopsea_agent_selection":
        return "MIXED_POLLINATION_X_HERBIVORY", "EXPERIMENTAL_FACTORIAL"
    if cluster == "Trifolium_repens_selection_program":
        if axis.endswith("inflorescence_production"):
            return "HERBIVORY_REDUCTION", "EXPERIMENTAL_SINGLE_FACTOR"
        if axis.endswith("flowering_time"):
            return "POLLINATION_SUPPLEMENTATION", "EXPERIMENTAL_SINGLE_FACTOR_WITH_DEFENCE_STRATUM"
        raise ValueError(f"unregistered Trifolium axis: {axis}")
    if cluster == "Erysimum_mediohispanicum_selection_mosaic":
        return "SPATIAL_MULTI_AGENT_MOSAIC", "OBSERVATIONAL_SPATIAL_MULTI_AGENT"
    if cluster == "Brassica_rapa_Knauer_selection_program":
        return "CONSUMER_IDENTITY_COMPOSITION", "EXPERIMENTAL_CONSUMER_REGIME"
    if cluster == "Lobelia_cardinalis_Bartkowska_selection_program":
        return "POLLINATION_SUPPLEMENTATION", "EXPERIMENTAL_SINGLE_FACTOR"
    if cluster == "Dalechampia_scandens_Perez_Barrales_selection_program":
        return "SINGLE_NET_CONTEXT", "SINGLE_CONTEXT"
    if cluster == "Lythrum_salicaria_Thomsen_selection_program":
        return "ANTAGONIST_DAMAGE_MANIPULATION", "EXPERIMENTAL_SINGLE_FACTOR"
    if cluster == "Helianthus_annuus_texanus_Mitchell_selection_program":
        return "LANDSCAPE_CROP_PROXIMITY", "OBSERVATIONAL_LANDSCAPE"
    raise ValueError(f"unregistered H2 directional cluster: {cluster}")


def _evidence_level(rows: list[dict]) -> str:
    has_pos = any(r["beta"] > 0 for r in rows)
    has_neg = any(r["beta"] < 0 for r in rows)
    if not (has_pos and has_neg):
        return "NO_POINT_REVERSAL"

    supported_pos = any(r["support_status"] == "SUPPORTED_POSITIVE" for r in rows)
    supported_neg = any(r["support_status"] == "SUPPORTED_NEGATIVE" for r in rows)
    if supported_pos and supported_neg:
        return "POINT_REVERSAL_BIDIRECTIONAL_SUPPORTED"
    if supported_pos or supported_neg:
        return "POINT_REVERSAL_ONE_SIDE_SUPPORTED"
    if any(r["support_status"] == "UNCERTAINTY_UNRESOLVED" for r in rows):
        return "POINT_REVERSAL_UNCERTAINTY_UNRESOLVED"
    return "POINT_REVERSAL_BOTH_SIDES_UNSUPPORTED"


def build(root: Path) -> dict:
    v10 = _load_v10()
    cases = v10._collect_cases(root)
    by_axis: dict[str, list[dict]] = defaultdict(list)
    for row in cases:
        by_axis[row["axis"]].append(row)

    axis_rows = []
    for axis, rows in sorted(by_axis.items()):
        cluster = rows[0]["cluster"]
        mechanism, attribution = _mechanism(axis, cluster)
        level = _evidence_level(rows)
        point_switch = level != "NO_POINT_REVERSAL"
        axis_rows.append(
            {
                "axis": axis,
                "cluster": cluster,
                "mechanism": mechanism,
                "attribution_design": attribution,
                "n_cases": len(rows),
                "repeated_axis": len(rows) >= 2,
                "point_estimate_sign_switch": point_switch,
                "reversal_evidence_level": level,
                "supported_positive_contexts": sum(
                    r["support_status"] == "SUPPORTED_POSITIVE" for r in rows
                ),
                "supported_negative_contexts": sum(
                    r["support_status"] == "SUPPORTED_NEGATIVE" for r in rows
                ),
                "uncertainty_unresolved_contexts": sum(
                    r["support_status"] == "UNCERTAINTY_UNRESOLVED" for r in rows
                ),
                "contexts": ";".join(r["context"] for r in rows),
            }
        )

    repeated = [r for r in axis_rows if r["repeated_axis"]]
    switches = [r for r in repeated if r["point_estimate_sign_switch"]]

    evidence_counts = Counter(r["reversal_evidence_level"] for r in repeated)

    mechanism_rows = []
    for mechanism in MECHANISM_ORDER:
        rows = [r for r in repeated if r["mechanism"] == mechanism]
        if not rows:
            continue
        sw = [r for r in rows if r["point_estimate_sign_switch"]]
        mechanism_rows.append(
            {
                "mechanism": mechanism,
                "n_repeated_axes": len(rows),
                "n_point_switch_axes": len(sw),
                "n_bidirectional_supported_axes": sum(
                    r["reversal_evidence_level"]
                    == "POINT_REVERSAL_BIDIRECTIONAL_SUPPORTED"
                    for r in rows
                ),
                "n_one_side_supported_axes": sum(
                    r["reversal_evidence_level"]
                    == "POINT_REVERSAL_ONE_SIDE_SUPPORTED"
                    for r in rows
                ),
                "n_both_sides_unsupported_axes": sum(
                    r["reversal_evidence_level"]
                    == "POINT_REVERSAL_BOTH_SIDES_UNSUPPORTED"
                    for r in rows
                ),
                "n_uncertainty_unresolved_switch_axes": sum(
                    r["reversal_evidence_level"]
                    == "POINT_REVERSAL_UNCERTAINTY_UNRESOLVED"
                    for r in rows
                ),
                "n_clusters": len({r["cluster"] for r in rows}),
                "n_switch_clusters": len({r["cluster"] for r in sw}),
            }
        )

    return {
        "analysis": "sch_h2_switch_mechanisms_v11",
        "n_cases": len(cases),
        "n_axes": len(axis_rows),
        "n_repeated_axes": len(repeated),
        "n_point_switch_axes": len(switches),
        "n_point_switch_clusters": len({r["cluster"] for r in switches}),
        "reversal_evidence_counts": {
            key: evidence_counts.get(key, 0) for key in EVIDENCE_LEVELS
        },
        "mechanism_rows": mechanism_rows,
        "switch_axis_rows": [r for r in axis_rows if r["point_estimate_sign_switch"]],
        "status": "H2_SWITCH_MECHANISM_TAXONOMY_READY_DESCRIPTIVE_ONLY",
        "claim_ceiling": [
            "context_mechanism_taxonomy_is_post_hoc_descriptive",
            "mechanism_cells_are_cluster_confounded",
            "do_not_compare_mechanism_rates_inferentially",
            "point_reversal_is_not_bidirectional_support",
            "supported_reversal_requires_supported_opposite_directions",
            "observational_spatial_mosaics_do_not_identify_one_causal_modifier",
            "not_a_literature_prevalence_estimate",
        ],
    }


def write_axis_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "axis",
        "cluster",
        "mechanism",
        "attribution_design",
        "n_cases",
        "repeated_axis",
        "point_estimate_sign_switch",
        "reversal_evidence_level",
        "supported_positive_contexts",
        "supported_negative_contexts",
        "uncertainty_unresolved_contexts",
        "contexts",
    ]
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row[k] for k in fields})


def write_mechanism_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("empty mechanism rows")
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out-json", type=Path)
    p.add_argument("--out-axis-csv", type=Path)
    p.add_argument("--out-mechanism-csv", type=Path)
    a = p.parse_args()

    result = build(a.root)
    if a.out_json:
        payload = {k: v for k, v in result.items() if k not in {"switch_axis_rows", "mechanism_rows"}}
        payload["mechanism_rows"] = result["mechanism_rows"]
        a.out_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if a.out_axis_csv:
        write_axis_csv(a.out_axis_csv, result["switch_axis_rows"])
    if a.out_mechanism_csv:
        write_mechanism_csv(a.out_mechanism_csv, result["mechanism_rows"])
    if not any((a.out_json, a.out_axis_csv, a.out_mechanism_csv)):
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
