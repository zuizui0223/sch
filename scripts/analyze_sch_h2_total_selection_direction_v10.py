from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

BASE_CASE_FILES = [
    ("data/SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH4_V1.csv", "SCHPRISMA-000030"),
    ("data/SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH6_V1.csv", "SCHPRISMA-000391"),
    ("data/SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH7_V1.csv", "SCHPRISMA-000008"),
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def _parse_p(value: str) -> float | None:
    if not value:
        return None
    t = value.strip().upper()
    if t == "NS":
        return 1.0
    if t.startswith("P_LT_"):
        try:
            return float(t.removeprefix("P_LT_").replace("_", "."))
        except ValueError:
            return None
    m = re.search(r"P\s*<\s*([0-9.]+)", t)
    if m:
        return float(m.group(1)) / 2.0
    m = re.search(r"P\s*=\s*([0-9.]+)", t)
    if m:
        return float(m.group(1))
    try:
        return float(t)
    except ValueError:
        return None


def _uncertainty_support(
    beta: float,
    *,
    se: str = "",
    p_value: str = "",
    significance: str = "",
    ci_low: str = "",
    ci_high: str = "",
    notes: str = "",
) -> tuple[str, str]:
    if se:
        s = float(se)
        if s > 0:
            status = "SUPPORTED_POSITIVE" if beta > 0 else "SUPPORTED_NEGATIVE"
            if abs(beta / s) <= 1.96:
                status = "NOT_SUPPORTED"
            return status, "WALD_95_APPROX_FROM_REPORTED_SE"

    for raw, method in ((p_value, "SOURCE_REPORTED_P"), (significance, "SOURCE_REPORTED_SIGNIFICANCE")):
        p = _parse_p(raw)
        if p is not None:
            if p < 0.05:
                return ("SUPPORTED_POSITIVE" if beta > 0 else "SUPPORTED_NEGATIVE"), method
            return "NOT_SUPPORTED", method

    if ci_low and ci_high:
        lo, hi = float(ci_low), float(ci_high)
        if lo > 0:
            return "SUPPORTED_POSITIVE", "SOURCE_REPORTED_INTERVAL"
        if hi < 0:
            return "SUPPORTED_NEGATIVE", "SOURCE_REPORTED_INTERVAL"
        return "NOT_SUPPORTED", "SOURCE_REPORTED_INTERVAL"

    if "significant_p_lt_0.05=YES" in notes:
        return ("SUPPORTED_POSITIVE" if beta > 0 else "SUPPORTED_NEGATIVE"), "SOURCE_REPORTED_SIGNIFICANCE_FLAG"
    if "significant_p_lt_0.05=NO" in notes:
        return "NOT_SUPPORTED", "SOURCE_REPORTED_SIGNIFICANCE_FLAG"

    p = _parse_p(notes)
    if p is not None:
        if p < 0.05:
            return ("SUPPORTED_POSITIVE" if beta > 0 else "SUPPORTED_NEGATIVE"), "SOURCE_REPORTED_P_IN_NOTES"
        return "NOT_SUPPORTED", "SOURCE_REPORTED_P_IN_NOTES"

    return "UNCERTAINTY_UNRESOLVED", "NO_NUMERIC_UNCERTAINTY"


def _add_case(cases: list[dict], *, axis: str, cluster: str, context: str, beta: float, numeric_family: str, **support_kwargs) -> None:
    support, method = _uncertainty_support(beta, **support_kwargs)
    cases.append(
        {
            "axis": axis,
            "cluster": cluster,
            "context": context,
            "beta": beta,
            "point_sign": "POSITIVE" if beta > 0 else ("NEGATIVE" if beta < 0 else "ZERO"),
            "support_status": support,
            "support_method": method,
            "numeric_pooling_family": numeric_family,
        }
    )


def _collect_cases(root: Path) -> list[dict]:
    cases: list[dict] = []

    for rel, source_id in BASE_CASE_FILES:
        for r in _read(root / rel):
            if r.get("source_id") != source_id or not r.get("effect_1"):
                continue
            beta = float(r["effect_1"])
            family = (
                "TOTAL_SELECTION_PATH_COEFFICIENT"
                if source_id == "SCHPRISMA-000008"
                else "STANDARDIZED_SELECTION_GRADIENT"
            )
            _add_case(
                cases,
                axis=r["canonical_trait_axis_id"],
                cluster=r["cluster_id"],
                context=r["case_id"],
                beta=beta,
                numeric_family=family,
                se=r.get("effect_1_se", ""),
                notes=r.get("notes", ""),
            )

    for r in _read(root / "data/SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv"):
        _add_case(
            cases,
            axis="Brassica_000775_" + r["trait"],
            cluster="Brassica_rapa_Knauer_selection_program",
            context=r["consumer_regime"],
            beta=float(r["beta"]),
            numeric_family="STANDARDIZED_SELECTION_GRADIENT",
            se=r.get("se", ""),
            p_value=r.get("p_value", ""),
        )

    for r in _read(root / "data/SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv"):
        _add_case(
            cases,
            axis="Lobelia_000659_" + r["trait"],
            cluster="Lobelia_cardinalis_Bartkowska_selection_program",
            context=r["pollination_context"],
            beta=float(r["beta"]),
            numeric_family="STANDARDIZED_SELECTION_GRADIENT",
            se=r.get("se", ""),
            p_value=r.get("p_value", ""),
        )

    for r in _read(root / "data/SCH_H2_DALECHAMPIA_PEREZ_BARRALES_2013_SELECTION_GRADIENTS_V1.csv"):
        if r["selection_component"] != "NET":
            continue
        _add_case(
            cases,
            axis="Dalechampia_000658_" + r["trait"],
            cluster="Dalechampia_scandens_Perez_Barrales_selection_program",
            context="NET_FITNESS_SURFACE",
            beta=float(r["beta_percent_fitness"]),
            numeric_family="STANDARDIZED_SELECTION_GRADIENT",
            ci_low=r.get("ci_low", ""),
            ci_high=r.get("ci_high", ""),
        )

    for r in _read(root / "data/SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv"):
        if r["estimand_role"] != "TOTAL_SELECTION":
            continue
        _add_case(
            cases,
            axis="Lythrum_000284_" + r["trait"],
            cluster="Lythrum_salicaria_Thomsen_selection_program",
            context=r["context_or_contrast"],
            beta=float(r["beta_or_delta"]),
            numeric_family="STANDARDIZED_SELECTION_GRADIENT",
            se=r.get("se", ""),
            significance=r.get("significance", ""),
        )

    for r in _read(root / "data/SCH_H2_HELIANTHUS_TEXANUS_SELECTION_GRADIENTS_V1.csv"):
        _add_case(
            cases,
            axis="Helianthus_000673_" + r["trait"],
            cluster="Helianthus_annuus_texanus_Mitchell_selection_program",
            context=r["context"],
            beta=float(r["beta"]),
            numeric_family=r["numeric_pooling_family"],
        )

    return cases


def build(root: Path) -> dict:
    cases = _collect_cases(root)
    by_axis: dict[str, list[dict]] = defaultdict(list)
    for row in cases:
        by_axis[row["axis"]].append(row)

    axis_rows = []
    for axis, rows in sorted(by_axis.items()):
        has_pos = any(r["beta"] > 0 for r in rows)
        has_neg = any(r["beta"] < 0 for r in rows)
        supported_pos = any(r["support_status"] == "SUPPORTED_POSITIVE" for r in rows)
        supported_neg = any(r["support_status"] == "SUPPORTED_NEGATIVE" for r in rows)
        uncertainty_unresolved = any(r["support_status"] == "UNCERTAINTY_UNRESOLVED" for r in rows)
        axis_rows.append(
            {
                "axis": axis,
                "cluster": rows[0]["cluster"],
                "n_cases": len(rows),
                "point_estimate_sign_switch": has_pos and has_neg,
                "uncertainty_supported_sign_switch": supported_pos and supported_neg,
                "uncertainty_unresolved": uncertainty_unresolved,
                "numeric_pooling_families": sorted({r["numeric_pooling_family"] for r in rows}),
            }
        )

    repeated = [r for r in axis_rows if r["n_cases"] >= 2]
    point_switch = [r for r in repeated if r["point_estimate_sign_switch"]]
    supported_switch = [r for r in repeated if r["uncertainty_supported_sign_switch"]]
    unresolved_switch = [
        r for r in point_switch
        if r["uncertainty_unresolved"] and not r["uncertainty_supported_sign_switch"]
    ]

    return {
        "analysis": "sch_h2_total_selection_direction_v10",
        "n_cases": len(cases),
        "n_axes": len(axis_rows),
        "n_clusters": len({r["cluster"] for r in axis_rows}),
        "n_repeated_axes": len(repeated),
        "n_point_estimate_sign_switch_axes": len(point_switch),
        "n_same_sign_repeated_axes": len(repeated) - len(point_switch),
        "n_point_estimate_sign_switch_clusters": len({r["cluster"] for r in point_switch}),
        "n_uncertainty_supported_sign_switch_axes": len(supported_switch),
        "n_uncertainty_supported_sign_switch_clusters": len({r["cluster"] for r in supported_switch}),
        "supported_switch_axes": sorted(r["axis"] for r in supported_switch),
        "uncertainty_unresolved_switch_axes": sorted(r["axis"] for r in unresolved_switch),
        "point_switch_axes": sorted(r["axis"] for r in point_switch),
        "status": "TOTAL_SELECTION_DIRECTIONAL_CONTEXT_ANALYSIS_READY_POOLING_FAIL_CLOSED",
        "claim_ceiling": [
            "directional_context_analysis_is_scale_invariant_within_trait_axis",
            "point_sign_switch_is_not_uncertainty_supported_reversal",
            "does_not_pool_incompatible_numeric_families",
            "not_a_literature_prevalence_estimate",
            "cluster_dependence_retained",
        ],
        "axis_rows": axis_rows,
    }


def _write_axis_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "axis", "cluster", "n_cases", "point_estimate_sign_switch",
        "uncertainty_supported_sign_switch", "uncertainty_unresolved",
        "numeric_pooling_families",
    ]
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for row in rows:
            out = dict(row)
            out["numeric_pooling_families"] = ";".join(row["numeric_pooling_families"])
            w.writerow(out)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out-json", type=Path)
    p.add_argument("--out-csv", type=Path)
    a = p.parse_args()
    result = build(a.root)
    if a.out_json:
        a.out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if a.out_csv:
        _write_axis_csv(a.out_csv, result["axis_rows"])
    if not a.out_json and not a.out_csv:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
