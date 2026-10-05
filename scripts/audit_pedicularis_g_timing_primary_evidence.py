from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_TIMING_PRIMARY_EVIDENCE_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G timing primary evidence ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G timing primary evidence ledger is empty")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    evidence_ids = [row["evidence_id"] for row in rows]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence_id must be unique")

    direct_hour_rows = [
        row for row in rows
        if row["direct_hour_bound_eligible"] != "NO"
    ]
    if direct_hour_rows:
        raise ValueError(
            "current recovered primary evidence must not silently create "
            "a focal hour-scale G timing bound"
        )

    tolerance_rows = [
        row for row in rows
        if row["hard_failure_tolerance_eligible"] != "NO"
    ]
    if tolerance_rows:
        raise ValueError(
            "natural-history evidence must not be promoted directly into "
            "a device hard-failure tolerance"
        )

    focal = [
        row for row in rows
        if row["taxon_scope"] in {
            "Pedicularis_rex",
            "Pedicularis_rex_subsp_rex",
        }
    ]
    focal_axes = {row["evidence_axis"] for row in focal}

    required_focal_axes = {
        "OVIPOSITION_ORDER",
        "FLOWERING_SEASON",
        "CAPSULE_MATURITY_DELAY",
        "POLLINATOR_DEPENDENCE",
        "NATURAL_SEED_PREDATION",
        "POLLINATION_MECHANISM",
    }
    missing = sorted(required_focal_axes - focal_axes)
    if missing:
        raise ValueError(
            "G timing evidence ledger lacks required focal axes: "
            + ", ".join(missing)
        )

    predation = next(
        row for row in focal
        if row["evidence_axis"] == "NATURAL_SEED_PREDATION"
    )
    if predation["reported_value"] != "1.36 to 27.42":
        raise ValueError("natural P. rex predation range changed unexpectedly")

    oviposition = next(
        row for row in focal
        if row["evidence_axis"] == "OVIPOSITION_ORDER"
    )
    if "after flowers open" not in oviposition["reported_value"]:
        raise ValueError("focal oviposition opening-order evidence missing")
    if "before ovaries swell" not in oviposition["reported_value"]:
        raise ValueError("focal pre-swelling oviposition evidence missing")

    evidence_forms = Counter(row["evidence_form"] for row in rows)
    scopes = Counter(row["taxon_scope"] for row in rows)

    return {
        "analysis": "pedicularis_g_timing_primary_evidence_audit_v1",
        "n_evidence_rows": len(rows),
        "evidence_form_counts": dict(sorted(evidence_forms.items())),
        "taxon_scope_counts": dict(sorted(scopes.items())),
        "focal_ordinal_oviposition_window_recovered": True,
        "focal_bumblebee_dependence_recovered": True,
        "focal_pollination_mechanism_recovered": True,
        "focal_hour_scale_lower_bound_recovered": False,
        "focal_hour_scale_upper_bound_recovered": False,
        "natural_predation_range_percent": [1.36, 27.42],
        "natural_predation_can_set_device_hard_failure_tolerance": False,
        "congeneric_flower_longevity_can_set_focal_timing_bound": False,
        "current_timing_gate_state": "FOCAL_HOUR_SCALE_TIMING_REQUIRES_METHOD_PILOT",
        "field_estimands_required": [
            "time_from_anthesis_to_pollination_window_complete",
            "time_from_anthesis_to_first_pre_barrier_attack_or_oviposition",
            "time_from_anthesis_to_ovary_swelling",
        ],
        "interpretation": (
            "Recovered primary literature establishes biological ordering and "
            "strong pollinator dependence, but not a portable hour-scale "
            "post-pollination barrier window. Natural seed-predation pressure "
            "is not a method-failure probability."
        ),
        "claim_ceiling": [
            "bounded_recovered_primary_evidence_only",
            "ordinal_timing_not_numeric_timing",
            "no_direct_F0_timing_value",
            "no_device_failure_tolerance_from_natural_predation",
            "same_context_focal_timing_pilot_still_required",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit recovered primary biological evidence relevant to the "
            "P. rex independent-G timing window without inventing hour bounds"
        )
    )
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read(args.evidence))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
