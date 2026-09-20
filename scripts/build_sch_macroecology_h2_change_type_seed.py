from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ALLOWED_CHANGE_TYPES = {
    "GEOMETRY_CLASS_SWITCH",
    "GEOMETRY_DISAPPEARANCE",
    "COMPONENT_WEIGHT_SHIFT",
    "COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def build(path: Path) -> dict:
    rows = _read(path)
    ids = [row["change_record_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("change_record_id must be unique")

    invalid = sorted({
        row["change_type"]
        for row in rows
        if row["change_type"] not in ALLOWED_CHANGE_TYPES
    })
    if invalid:
        raise ValueError("invalid H2 change type(s): " + ", ".join(invalid))

    type_counts = Counter(row["change_type"] for row in rows)
    local_cases = sum(int(row["local_cases_materialized"]) for row in rows)

    return {
        "analysis": "sch_macroecology_h2_change_type_seed_v1",
        "n_change_records": len(rows),
        "n_canonical_axes": len({row["canonical_trait_axis_id"] for row in rows}),
        "change_type_counts": dict(sorted(type_counts.items())),
        "n_change_records_with_materialized_local_cases": sum(
            int(row["local_cases_materialized"]) > 0 for row in rows
        ),
        "n_materialized_local_cases_represented": local_cases,
        "n_change_records_without_materialized_local_cases": sum(
            int(row["local_cases_materialized"]) == 0 for row in rows
        ),
        "status": "H2_CHANGE_TYPE_SEED_DESCRIPTIVE_ONLY",
        "claim_ceiling": [
            "change_types_are_mechanistic_descriptive_classes_not_frequencies",
            "source_level_change_can_exist_without_materialized_local_cases",
            "geometry_class_switch_is_not_equivalent_to_component_weight_shift",
            "geometry_disappearance_is_not_equivalent_to_static_null_geometry",
            "H2_change_type_model_not_ready",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.seed)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
