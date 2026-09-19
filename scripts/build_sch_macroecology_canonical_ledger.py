from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

FIXED_ROLE = "NET_ANTAGONISTIC"
TRI = {"YES", "NO", "UNRESOLVED"}


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


def _aggregate_tri(values: list[str]) -> str:
    values = [value for value in values if value]
    invalid = sorted(set(values) - TRI)
    if invalid:
        raise ValueError(f"invalid tri-state values: {invalid}")
    if "YES" in values:
        return "YES"
    if values and set(values) == {"NO"}:
        return "NO"
    return "UNRESOLVED"


def _one_or_join(values: list[str], sep: str = ";") -> str:
    unique = sorted({value for value in values if value})
    return unique[0] if len(unique) == 1 else sep.join(unique)


def _role_family(guild: str) -> str:
    text = guild.lower()
    if not text:
        return "UNRESOLVED"
    if "seed predator" in text or "seed-predator" in text or "weevil" in text:
        return "SEED_PREDATOR"
    if "nectar robber" in text or "robbing" in text:
        if "florivore" in text or "herbivore" in text:
            return "MULTIPLE_ANTAGONISTS"
        return "NECTAR_ROBBER"
    if "florivore" in text or "florivorous" in text:
        return "FLORIVORE"
    if "grazer" in text or "herbivore" in text:
        return "HERBIVORE_GRAZER"
    if "brood" in text or "oviposit" in text or "seed parasite" in text:
        return "BROOD_EXPLOITER"
    return "OTHER_OR_UNRESOLVED"


def build(
    batch_paths: list[Path],
    override_path: Path,
) -> tuple[list[dict[str, str]], dict]:
    rows: list[dict[str, str]] = []
    for path in batch_paths:
        rows.extend(_read(path))

    source_ids = [row["trait_axis_id"] for row in rows]
    if len(source_ids) != len(set(source_ids)):
        dupes = sorted(k for k, n in Counter(source_ids).items() if n > 1)
        raise ValueError("duplicate source trait_axis_id: " + ", ".join(dupes))

    overrides = {
        row["source_trait_axis_id"]: row["canonical_trait_axis_id"]
        for row in _read(override_path)
    }
    unknown = sorted(set(overrides) - set(source_ids))
    if unknown:
        raise ValueError("canonical override references unknown source axes: " + ", ".join(unknown))

    excluded = [
        row for row in rows
        if row.get("geometry_eligibility", "").startswith("INELIGIBLE_")
    ]
    model_rows = [row for row in rows if row not in excluded]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        grouped[overrides.get(row["trait_axis_id"], row["trait_axis_id"])].append(row)

    output: list[dict[str, str]] = []
    for canonical_id, members in sorted(grouped.items()):
        cluster_ids = {row["cluster_id"] for row in members}
        if len(cluster_ids) != 1:
            raise ValueError(f"canonical axis crosses biological clusters: {canonical_id}")

        role_states = {row["antagonist_role_status"] for row in members}
        source_geometries = [_source_geometry(row) for row in members]

        if role_states == {FIXED_ROLE}:
            resolved = {g for g in source_geometries if g != "UNRESOLVED"}
            if len(resolved) == 0:
                canonical_geometry = "UNRESOLVED"
            elif len(resolved) == 1:
                canonical_geometry = next(iter(resolved))
            else:
                canonical_geometry = "CONTEXT_VARIABLE"
            canonical_role = FIXED_ROLE
        else:
            canonical_geometry = "ROLE_BOUNDARY"
            canonical_role = _one_or_join(list(role_states))

        trait_domains = {row["trait_domain"] for row in members if row["trait_domain"]}
        if len(trait_domains) != 1:
            raise ValueError(
                f"canonical axis has inconsistent trait_domain: {canonical_id}: {sorted(trait_domains)}"
            )

        guilds = [row["antagonist_guild"] for row in members if row["antagonist_guild"]]
        guild_families = {_role_family(value) for value in guilds}

        output.append(
            {
                "canonical_trait_axis_id": canonical_id,
                "cluster_id": next(iter(cluster_ids)),
                "plant_taxon": _one_or_join([row["plant_taxon"] for row in members]),
                "trait_coordinate": _one_or_join([row["trait_coordinate"] for row in members], " | "),
                "trait_domain": next(iter(trait_domains)),
                "function_pair_family": _one_or_join([row["function_pair_family"] for row in members]),
                "shared_coordinate_status": _one_or_join([row["shared_coordinate_status"] for row in members]),
                "antagonist_role_status": canonical_role,
                "antagonist_guild": _one_or_join(guilds, " | "),
                "antagonist_guild_family": (
                    next(iter(guild_families))
                    if len(guild_families) == 1
                    else "MULTIPLE_ANTAGONIST_GUILDS"
                ),
                "pollinator_guild": _one_or_join([row["pollinator_guild"] for row in members], " | "),
                "interaction_timing": _one_or_join([row["interaction_timing"] for row in members]),
                "canonical_geometry": canonical_geometry,
                "source_geometry_classes": ";".join(sorted(set(source_geometries))),
                "context_shift_status": _aggregate_tri(
                    [row["context_shift_detected"] for row in members]
                ),
                "cancellation_status": _aggregate_tri(
                    [row["cancellation_detected"] for row in members]
                ),
                "trait_manipulated_any": _aggregate_tri(
                    [row["trait_manipulated"] for row in members]
                ),
                "consumer_context_manipulated_any": _aggregate_tri(
                    [row["consumer_context_manipulated"] for row in members]
                ),
                "common_fitness_endpoint_any": _aggregate_tri(
                    [row["common_fitness_endpoint"] for row in members]
                ),
                "source_count": str(len(members)),
                "source_ids": ";".join(sorted({row["source_id"] for row in members})),
                "source_trait_axis_ids": ";".join(
                    sorted(row["trait_axis_id"] for row in members)
                ),
                "source_verification_states": ";".join(
                    sorted({row["source_verification_state"] for row in members})
                ),
                "model_h1_status": (
                    "STATIC_RESOLVED_FIXED_ROLE"
                    if canonical_role == FIXED_ROLE
                    and canonical_geometry
                    in {"CONFLICT", "ALIGNMENT_REINFORCEMENT", "ONE_SIDED_OR_NULL"}
                    else "CONTEXT_VARIABLE_FIXED_ROLE"
                    if canonical_role == FIXED_ROLE and canonical_geometry == "CONTEXT_VARIABLE"
                    else "UNRESOLVED_FIXED_ROLE"
                    if canonical_role == FIXED_ROLE
                    else "ROLE_BOUNDARY_EXCLUDED_FROM_FIXED_H1"
                ),
            }
        )

    geometry_counts = Counter(row["canonical_geometry"] for row in output)
    fixed = [row for row in output if row["antagonist_role_status"] == FIXED_ROLE]
    static = [
        row for row in fixed
        if row["canonical_geometry"]
        in {"CONFLICT", "ALIGNMENT_REINFORCEMENT", "ONE_SIDED_OR_NULL"}
    ]

    receipt = {
        "analysis": "sch_macroecology_canonical_ledger_v1",
        "n_source_axis_records": len(rows),
        "n_excluded_source_axis_records": len(excluded),
        "n_model_source_axis_records": len(model_rows),
        "n_canonical_trait_axes": len(output),
        "canonical_geometry_counts": dict(sorted(geometry_counts.items())),
        "n_fixed_role_axes": len(fixed),
        "n_static_resolved_fixed_role_axes": len(static),
        "n_static_resolved_fixed_role_clusters": len({row["cluster_id"] for row in static}),
        "static_geometry_counts": dict(
            sorted(Counter(row["canonical_geometry"] for row in static).items())
        ),
        "trait_domain_counts_static": dict(
            sorted(Counter(row["trait_domain"] for row in static).items())
        ),
        "antagonist_guild_family_counts_static": dict(
            sorted(Counter(row["antagonist_guild_family"] for row in static).items())
        ),
        "status": "CANONICAL_LEDGER_MATERIALIZED_INFERENCE_DIAGNOSTIC_READY",
        "claim_ceiling": [
            "canonical_rows_are_model_units_not_prevalence_units",
            "static_H1_excludes_context_variable_and_role_boundary_axes",
            "unresolved_geometry_is_missing_not_negative",
            "cluster_dependence_must_be_respected",
            "full_frozen_screen_still_required_for_final_inference",
        ],
    }
    return output, receipt


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty canonical ledger")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_csvs", type=Path, nargs="+")
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(args.batch_csvs, args.overrides)
    write_csv(args.out_csv, rows)
    args.out_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
