from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.evaluate_pedicularis_predator_method import REQUIRED_FIELDS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEQUENCE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_FIELD_SEQUENCE_V1.csv"
)


EXPECTED_HARD_METHOD_VALIDITY = {
    "sham_device_applied",
    "pollination_window_complete_before_barrier",
    "ovary_swollen_at_barrier",
    "barrier_covers_pollinator_entry",
    "pre_barrier_attack_present",
    "barrier_integrity_failure_present",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G field sequence ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G field sequence ledger is empty")
    return rows


def build(path: Path = DEFAULT_SEQUENCE) -> dict:
    rows = _read(path)

    field_names = [row["field_name"] for row in rows]
    if len(field_names) != len(set(field_names)):
        raise ValueError("G field sequence field_name must be unique")
    if set(field_names) != set(REQUIRED_FIELDS):
        raise ValueError(
            "G V4 field sequence coverage mismatch: "
            f"missing={sorted(set(REQUIRED_FIELDS) - set(field_names))}, "
            f"extra={sorted(set(field_names) - set(REQUIRED_FIELDS))}"
        )

    phases = {}
    for row in rows:
        try:
            order = int(row["phase_order"])
        except ValueError as exc:
            raise ValueError(
                f"{row['field_name']}.phase_order must be an integer"
            ) from exc
        if order < 0:
            raise ValueError("phase_order must be >= 0")
        phases.setdefault(order, set()).add(row["phase"])

    if set(phases) != set(range(7)):
        raise ValueError(
            "G field sequence must cover phase_order 0 through 6 exactly"
        )
    if any(len(names) != 1 for names in phases.values()):
        raise ValueError(
            "each G phase_order must map to exactly one phase label"
        )

    proxy = next(
        row for row in rows if row["field_name"] == "pollen_grains"
    )
    if proxy["collection_source"] != "PROXY_MATERIALIZED":
        raise ValueError(
            "pollen_grains must remain explicitly proxy-materialized"
        )
    if proxy["destructive_or_endpoint"] != "DESTRUCTIVE_PROXY":
        raise ValueError(
            "pollen_grains must remain a destructive proxy measurement"
        )

    non_proxy = [
        row
        for row in rows
        if row["field_name"] != "pollen_grains"
    ]
    if {row["collection_source"] for row in non_proxy} != {"FOCAL"}:
        raise ValueError(
            "all non-pollen V4 fields must remain focal-field observations"
        )

    hard_method_fields = {
        row["field_name"]
        for row in rows
        if row["fail_fast_role"] == "HARD_METHOD_VALIDITY"
    }
    if hard_method_fields != EXPECTED_HARD_METHOD_VALIDITY:
        raise ValueError(
            "hard method-validity field set drifted"
        )

    role_counts = Counter(row["fail_fast_role"] for row in rows)
    phase_rows = {
        order: sorted(
            (
                row["field_name"],
                row["fail_fast_role"],
                row["collection_action"],
            )
            for row in rows
            if int(row["phase_order"]) == order
        )
        for order in sorted(phases)
    }

    hard_by_phase = {
        order: sorted(
            row["field_name"]
            for row in rows
            if (
                int(row["phase_order"]) == order
                and row["fail_fast_role"] == "HARD_METHOD_VALIDITY"
            )
        )
        for order in sorted(phases)
    }
    hard_by_phase = {
        order: values
        for order, values in hard_by_phase.items()
        if values
    }

    phase_labels = {
        order: next(iter(names))
        for order, names in sorted(phases.items())
    }

    return {
        "analysis": "pedicularis_g_field_sequence_v1",
        "n_v4_fields": len(rows),
        "v4_field_coverage_complete": True,
        "phase_labels": phase_labels,
        "phase_rows": phase_rows,
        "fail_fast_role_counts": dict(sorted(role_counts.items())),
        "hard_method_validity_fields": sorted(hard_method_fields),
        "hard_method_validity_by_phase": hard_by_phase,
        "earliest_hard_method_validity_phase": min(hard_by_phase),
        "pollen_proxy_semantics": {
            "collection_source": proxy["collection_source"],
            "phase": proxy["phase"],
            "destructive_or_endpoint": proxy["destructive_or_endpoint"],
        },
        "field_stop_priority": [
            "REGISTRY_ASSIGNMENT",
            "BARRIER_APPLICATION_METHOD_VALIDITY",
            "POST_BARRIER_INTEGRITY",
            "EARLY_ANTAGONIST_EFFECT",
            "HARVEST_ENDPOINTS",
        ],
        "status": "G_FIELD_SEQUENCE_COVERS_ALL_V4_FIELDS",
        "claim_ceiling": [
            "field_ordering_only_not_sample_size",
            "hard_method_validity_is_not_a_biological_effect_threshold",
            "pollen_proxy_provenance_must_remain_explicit",
            "harvest_endpoints_are_not_needed_to_detect_early_method-invalid_flowers",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the operational field sequence for every registered "
            "Pedicularis G V4 input field"
        )
    )
    parser.add_argument("--sequence", type=Path, default=DEFAULT_SEQUENCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.sequence)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
