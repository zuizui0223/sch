"""Build the fail-closed one-trait shared-cue coverage audit.

The canonical A/D manuscript is not modified by these classifications. This
script groups the committed route ledger by biological independence cluster,
requires a manual source adjudication for every A-route cluster, and writes
coverage diagnostics rather than effect estimates or prevalence claims.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "source_exports" / "BITA_TABLE_S3_MECHANISM_PATTERN_LEDGER.csv"
ADJUDICATION = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_SOURCE_ADJUDICATION_V1.csv"
HIGH_INFORMATION = ROOT / "data" / "source_exports" / "BITA_HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv"
HIGH_INFORMATION_RESCREEN = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_HIGH_INFORMATION_RESCREEN_V1.csv"
OUTPUT_CSV = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_COVERAGE_AUDIT_V1.csv"
OUTPUT_JSON = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_COVERAGE_SUMMARY_V1.json"
OUTPUT_MD = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_COVERAGE_READOUT_V1.md"
SOURCE_MANIFEST = ROOT / "data" / "source_exports" / "SOURCE_EXPORT_MANIFEST.json"

A_ROUTES = {"A_to_pollination", "A_to_antagonism"}
REQUIRED_ADJUDICATION_FIELDS = {
    "independence_cluster",
    "source",
    "one_trait_A_axis",
    "A_manipulated",
    "same_A_coordinate",
    "pollinator_response_measured",
    "antagonist_response_measured",
    "common_reproductive_outcome",
    "strict_status",
    "primary_blocker",
    "source_basis",
    "notes",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {str(key): str(value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _validate_source_exports() -> dict[str, object]:
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("source-export manifest is empty or malformed")
    for relative_path, declaration in artifacts.items():
        path = ROOT / relative_path
        expected = str(declaration.get("sha256", "")).lower()
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if not expected or observed != expected:
            raise ValueError(
                json.dumps({
                    "source_export_hash_mismatch": relative_path,
                    "expected": expected,
                    "observed": observed,
                })
            )
    return manifest


def _yes(value: str) -> bool:
    return value == "yes" or value.startswith("yes_")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("refusing to write an empty one-trait audit")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _validate_adjudications(rows: list[dict[str, str]], a_clusters: set[str]) -> dict[str, dict[str, str]]:
    if not rows or set(rows[0]) != REQUIRED_ADJUDICATION_FIELDS:
        raise ValueError("one-trait adjudication schema drift")
    by_cluster: dict[str, dict[str, str]] = {}
    for row in rows:
        cluster = row["independence_cluster"]
        if not cluster or cluster in by_cluster:
            raise ValueError(f"missing or duplicate adjudication cluster: {cluster!r}")
        by_cluster[cluster] = row
    missing = sorted(a_clusters - set(by_cluster))
    extra = sorted(set(by_cluster) - a_clusters)
    if missing or extra:
        raise ValueError(json.dumps({"missing_A_cluster_adjudications": missing, "extra_adjudications": extra}))
    return by_cluster


def _audit_rows() -> tuple[list[dict[str, str]], dict[str, object]]:
    source_manifest = _validate_source_exports()
    ledger_rows = _read(LEDGER)
    routes_by_cluster: dict[str, set[str]] = defaultdict(set)
    for row in ledger_rows:
        cluster = row["independence_cluster"]
        route = row["route"]
        if not cluster:
            raise ValueError("ledger row without independence_cluster")
        routes_by_cluster[cluster].add(route)

    clusters = set(routes_by_cluster)
    a_clusters = {cluster for cluster, routes in routes_by_cluster.items() if routes & A_ROUTES}
    adjudications = _validate_adjudications(_read(ADJUDICATION), a_clusters)

    output: list[dict[str, str]] = []
    for cluster in sorted(clusters):
        routes = routes_by_cluster[cluster]
        adjudication = adjudications.get(cluster)
        has_pollinator = "A_to_pollination" in routes
        has_antagonist = "A_to_antagonism" in routes
        if adjudication is None:
            output.append({
                "independence_cluster": cluster,
                "A_to_pollination_route": "yes" if has_pollinator else "no",
                "A_to_antagonism_route": "yes" if has_antagonist else "no",
                "one_trait_A_axis": "not_evaluated",
                "A_manipulated": "not_evaluated",
                "same_A_coordinate": "not_evaluated",
                "pollinator_response_measured": "no_current_route" if not has_pollinator else "not_evaluated",
                "antagonist_response_measured": "no_current_route" if not has_antagonist else "not_evaluated",
                "common_reproductive_outcome": "not_evaluated",
                "audit_status": "NOT_EVALUABLE_NO_A_ROUTE",
                "primary_blocker": "no_committed_A_route",
                "source_basis": "data/source_exports/BITA_TABLE_S3_MECHANISM_PATTERN_LEDGER.csv",
            })
            continue

        computed_pass = all((
            _yes(adjudication["A_manipulated"]),
            _yes(adjudication["same_A_coordinate"]),
            _yes(adjudication["pollinator_response_measured"]),
            _yes(adjudication["antagonist_response_measured"]),
            _yes(adjudication["common_reproductive_outcome"]),
            has_pollinator,
            has_antagonist,
        ))
        declared_pass = adjudication["strict_status"].startswith("PASS")
        if computed_pass != declared_pass:
            raise ValueError(f"declared/computed strict-status mismatch for {cluster}")
        output.append({
            "independence_cluster": cluster,
            "A_to_pollination_route": "yes" if has_pollinator else "no",
            "A_to_antagonism_route": "yes" if has_antagonist else "no",
            "one_trait_A_axis": adjudication["one_trait_A_axis"],
            "A_manipulated": adjudication["A_manipulated"],
            "same_A_coordinate": adjudication["same_A_coordinate"],
            "pollinator_response_measured": adjudication["pollinator_response_measured"],
            "antagonist_response_measured": adjudication["antagonist_response_measured"],
            "common_reproductive_outcome": adjudication["common_reproductive_outcome"],
            "audit_status": adjudication["strict_status"],
            "primary_blocker": adjudication["primary_blocker"],
            "source_basis": adjudication["source_basis"],
        })

    high_information_ids = {row["study_id"] for row in _read(HIGH_INFORMATION)}
    high_rescreen = _read(HIGH_INFORMATION_RESCREEN)
    rescreen_ids = {row["study_id"] for row in high_rescreen}
    if high_information_ids != rescreen_ids:
        raise ValueError(json.dumps({
            "missing_high_information_rescreens": sorted(high_information_ids - rescreen_ids),
            "extra_high_information_rescreens": sorted(rescreen_ids - high_information_ids),
        }))

    strict_passes = [row for row in output if row["audit_status"].startswith("PASS")]
    dual_route = [
        row for row in output
        if row["A_to_pollination_route"] == "yes" and row["A_to_antagonism_route"] == "yes"
    ]
    summary: dict[str, object] = {
        "ledger_record_count": len(ledger_rows),
        "independent_cluster_count": len(clusters),
        "A_route_cluster_count": len(a_clusters),
        "dual_A_route_cluster_count": len(dual_route),
        "strict_coverage_pass_count": len(strict_passes),
        "strict_coverage_pass_clusters": [row["independence_cluster"] for row in strict_passes],
        "directional_only_pass_count": sum(row["audit_status"] == "PASS_DIRECTIONAL_ONLY" for row in output),
        "high_information_system_count": len(high_rescreen),
        "high_information_strict_pass_count": sum(row["one_trait_rescreen_status"].startswith("PASS") for row in high_rescreen),
        "theis_2012_present_in_high_information_matrix": "Theis_Adler_2012_Cucurbita" in high_information_ids,
        "bita_source_commit": source_manifest["source_commit"],
        "claim_ceiling": "coverage_existence_only_not_effect_estimation_prevalence_or_channel_identification",
    }
    return output, summary


def _render(rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    candidates = [row for row in rows if row["audit_status"] != "NOT_EVALUABLE_NO_A_ROUTE"]
    lines = [
        "# One-trait shared-cue coverage readout v1",
        "",
        "## Result",
        "",
        f"- frozen BITA route-ledger clusters screened: **{summary['independent_cluster_count']}**",
        f"- clusters with at least one A route: **{summary['A_route_cluster_count']}**",
        f"- clusters with both `A_to_pollination` and `A_to_antagonism`: **{summary['dual_A_route_cluster_count']}**",
        f"- strict one-trait coverage passes: **{summary['strict_coverage_pass_count']}**",
        f"- original 16-system identification matrix strict passes: **{summary['high_information_strict_pass_count']}/{summary['high_information_system_count']}**",
        "",
        "The strict pass is **Theis & Adler (2012), directional source evidence only**. The same field experiment manipulated floral fragrance, recorded florivore and pollinator attraction, and reported seed production. The publisher-linked public deposit does not contain the main experiment's raw table, so this audit does not manufacture an uncertainty-bearing effect.",
        "",
        "The 0/16 result does not contradict the 1/25 result. The 16-system matrix was assembled around the two-trait identification frontier and does not include Theis & Adler (2012). It is therefore not a complete one-trait source universe.",
        "",
        "## Candidate adjudications",
        "",
        "| Cluster | A manipulated | pollinator response | antagonist response | common reproductive outcome | result |",
        "|---|---|---|---|---|---|",
    ]
    for row in candidates:
        lines.append(
            f"| `{row['independence_cluster']}` | {row['A_manipulated']} | "
            f"{row['pollinator_response_measured']} | {row['antagonist_response_measured']} | "
            f"{row['common_reproductive_outcome']} | `{row['audit_status']}` |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "The original one-trait hypothesis was not tested by BITA's two-trait estimand. It is nevertheless not evidence-free: the frozen source export contains one directional experiment meeting the predeclared coverage fields, plus several observational or comparative shared-tracking systems.",
        "",
        "The one-trait accounting identity is `Delta_A W = Delta_A M - Delta_A G - Delta_A C`. A reduced biotic balance `S_A = Delta_A M - Delta_A G` requires direct attraction cost to be standardized or measured; it must not be assumed away. Total `W(A)` alone still does not allocate the channels.",
        "",
        "## Claim ceiling",
        "",
        "This result establishes **coverage existence in the committed screened evidence**, not a pooled effect, natural prevalence, causal cue-overlap coefficient, or point identification of pollinator benefit and antagonist cost. Kessler et al. (2015) remains a strong experimental shared-tracking example but fails the strict common-outcome field because pollinator-mediated seed production and oviposition come from different assay structures. Sasidharan et al. (2023) remains a cross-study assembled response synthesis and is not a same-experiment coverage pass.",
        "",
        "## Next gate for a companion paper",
        "",
        "Before meta-analysis, expand the audit beyond the A/D-oriented 25-cluster universe with the same four fields and preserve `FAIL`, `NOT_EVALUABLE`, and source-access limits. If enough linked experiments remain, define route-compatible effect-size lanes. If not, report the paired-channel measurement gap rather than weakening the gate.",
        "",
    ]
    return "\n".join(lines)


def run() -> dict[str, object]:
    rows, summary = _audit_rows()
    _write_csv(OUTPUT_CSV, rows)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(_render(rows, summary), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
