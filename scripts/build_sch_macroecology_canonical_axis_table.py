from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

FIXED_ROLE = "NET_ANTAGONISTIC"

OUTPUT_FIELDS = [
    "canonical_trait_axis_id",
    "cluster_id",
    "plant_taxon",
    "trait_coordinate",
    "trait_domain",
    "function_pair_family",
    "antagonist_role_status",
    "pollinator_guild",
    "antagonist_guild",
    "n_source_records",
    "source_ids",
    "source_axis_ids",
    "source_geometry_classes",
    "canonical_geometry",
    "context_shift_detected",
    "cancellation_detected",
    "trait_manipulated",
    "consumer_context_manipulated",
    "common_fitness_endpoint",
    "h1_static_eligible",
    "h2_context_priority",
    "source_coding_statuses",
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _source_geometry(row: dict[str, str]) -> str:
    if row["antagonist_role_status"] != FIXED_ROLE:
        return "ROLE_BOUNDARY"
    labels = {
        "CONFLICT": row["conflict_detected"],
        "ALIGNMENT_REINFORCEMENT": row["alignment_detected"],
        "ONE_SIDED_OR_NULL": row["one_sided_or_null_detected"],
    }
    yes = [name for name, value in labels.items() if value == "YES"]
    if len(yes) > 1:
        raise ValueError(f"geometry collision for {row['trait_axis_id']}")
    return yes[0] if yes else "UNRESOLVED"


def _collapse(values: list[str], *, unresolved: str = "UNRESOLVED") -> str:
    clean = sorted({v for v in values if v})
    if not clean:
        return unresolved
    if len(clean) == 1:
        return clean[0]
    return ";".join(clean)


def _any_yes(values: list[str]) -> str:
    if "YES" in values:
        return "YES"
    if values and all(value == "NO" for value in values):
        return "NO"
    return "UNRESOLVED"


def _canonical_geometry(members: list[dict[str, str]]) -> str:
    roles = {row["antagonist_role_status"] for row in members}
    if roles != {FIXED_ROLE}:
        return "ROLE_BOUNDARY"
    classes = {
        _source_geometry(row)
        for row in members
        if _source_geometry(row) != "UNRESOLVED"
    }
    if not classes:
        return "UNRESOLVED"
    if len(classes) == 1:
        return next(iter(classes))
    return "CONTEXT_VARIABLE"


def build(
    batch_paths: list[Path],
    override_path: Path,
) -> tuple[list[dict[str, str]], dict]:
    source_rows: list[dict[str, str]] = []
    for path in batch_paths:
        source_rows.extend(_read(path))

    overrides = {
        row["source_trait_axis_id"]: row["canonical_trait_axis_id"]
        for row in _read(override_path)
    }

    model_rows = [
        row
        for row in source_rows
        if not row["geometry_eligibility"].startswith("INELIGIBLE_")
    ]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        canonical_id = overrides.get(row["trait_axis_id"], row["trait_axis_id"])
        grouped[canonical_id].append(row)

    output: list[dict[str, str]] = []
    for canonical_id in sorted(grouped):
        members = grouped[canonical_id]
        geometry = _canonical_geometry(members)
        role_status = _collapse([row["antagonist_role_status"] for row in members])
        context = _any_yes([row["context_shift_detected"] for row in members])
        if geometry == "CONTEXT_VARIABLE":
            context = "YES"

        row = {
            "canonical_trait_axis_id": canonical_id,
            "cluster_id": _collapse([r["cluster_id"] for r in members]),
            "plant_taxon": _collapse([r["plant_taxon"] for r in members]),
            "trait_coordinate": _collapse([r["trait_coordinate"] for r in members]),
            "trait_domain": _collapse([r["trait_domain"] for r in members]),
            "function_pair_family": _collapse([r["function_pair_family"] for r in members]),
            "antagonist_role_status": role_status,
            "pollinator_guild": _collapse([r["pollinator_guild"] for r in members]),
            "antagonist_guild": _collapse([r["antagonist_guild"] for r in members]),
            "n_source_records": str(len(members)),
            "source_ids": ";".join(sorted({r["source_id"] for r in members})),
            "source_axis_ids": ";".join(sorted(r["trait_axis_id"] for r in members)),
            "source_geometry_classes": ";".join(sorted({_source_geometry(r) for r in members})),
            "canonical_geometry": geometry,
            "context_shift_detected": context,
            "cancellation_detected": _any_yes([r["cancellation_detected"] for r in members]),
            "trait_manipulated": _any_yes([r["trait_manipulated"] for r in members]),
            "consumer_context_manipulated": _any_yes(
                [r["consumer_context_manipulated"] for r in members]
            ),
            "common_fitness_endpoint": _any_yes([r["common_fitness_endpoint"] for r in members]),
            "h1_static_eligible": (
                "YES"
                if geometry in {
                    "CONFLICT",
                    "ALIGNMENT_REINFORCEMENT",
                    "ONE_SIDED_OR_NULL",
                }
                and role_status == FIXED_ROLE
                else "NO"
            ),
            "h2_context_priority": "YES" if context == "YES" else "NO",
            "source_coding_statuses": ";".join(sorted({r["coding_status"] for r in members})),
        }
        output.append(row)

    geometry_counts = Counter(row["canonical_geometry"] for row in output)
    domain_counts = Counter(row["trait_domain"] for row in output)
    h1_rows = [row for row in output if row["h1_static_eligible"] == "YES"]

    receipt = {
        "analysis": "sch_macroecology_canonical_axis_table_v1",
        "n_canonical_trait_axes": len(output),
        "canonical_geometry_counts": dict(sorted(geometry_counts.items())),
        "trait_domain_counts": dict(sorted(domain_counts.items())),
        "n_h1_static_eligible_axes": len(h1_rows),
        "h1_static_geometry_counts": dict(
            sorted(Counter(row["canonical_geometry"] for row in h1_rows).items())
        ),
        "n_h2_context_priority_axes": sum(
            row["h2_context_priority"] == "YES" for row in output
        ),
        "n_axes_with_multiple_source_records": sum(
            int(row["n_source_records"]) > 1 for row in output
        ),
        "status": "CANONICAL_MODEL_TABLE_READY_PREMODEL_GATE_REQUIRED",
        "claim_ceiling": [
            "table_is_current_P1_source_audit_only",
            "h1_static_eligible_is_not_permission_to_fit_multivariable_model",
            "cluster_dependence_must_be_respected",
            "full_systematic_recode_required_for_final_inference",
        ],
    }
    return output, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_csvs", nargs="+", type=Path)
    parser.add_argument("--overrides", required=True, type=Path)
    parser.add_argument("--out-csv", type=Path)
    parser.add_argument("--out-json", type=Path)
    args = parser.parse_args()

    rows, receipt = build(args.batch_csvs, args.overrides)
    if args.out_csv:
        _write_csv(args.out_csv, rows)
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.out_json:
        args.out_json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
