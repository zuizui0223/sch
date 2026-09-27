from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f"malformed CSV row in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def build(queue_path: Path, audit_paths: list[Path]) -> dict:
    queue = _read(queue_path)
    queue_by_id = {row["record_id"]: row for row in queue}
    if len(queue_by_id) != len(queue):
        raise ValueError("queue record_id must be unique")

    audit: list[dict[str, str]] = []
    for path in audit_paths:
        audit.extend(_read(path))

    audited_ids = [row["record_id"] for row in audit]
    if len(audited_ids) != len(set(audited_ids)):
        raise ValueError("audited record_id must be unique across batches")

    unknown = sorted(set(audited_ids) - set(queue_by_id))
    if unknown:
        raise ValueError(
            "audit contains record not in frozen queue: " + ", ".join(unknown)
        )

    tier_mismatch = [
        row["record_id"]
        for row in audit
        if row["recovery_tier"] != queue_by_id[row["record_id"]]["recovery_tier"]
    ]
    if tier_mismatch:
        raise ValueError(
            "audit tier drift: " + ", ".join(sorted(tier_mismatch))
        )

    decisions = Counter(row["estimand_recovery_decision"] for row in audit)
    reasons = Counter(row["reason_code"] for row in audit)
    tiers = Counter(row["recovery_tier"] for row in audit)

    promoted = sorted(
        row["record_id"]
        for row in audit
        if row["estimand_recovery_decision"]
        == "PROMOTED_TOTAL_SELECTION_EFFECT"
    )
    unaudited = len(queue) - len(audit)
    complete = unaudited == 0

    claim_ceiling = [
        "zero_promotion_yield_is_a_development_result_not_a_prevalence_estimate",
        "formal_prisma_inclusion_is_not_changed_by_estimand_recovery_audit",
        "queue_priority_rules_remain_frozen",
        "shared_trait_coordinate_failure_is_distinct_from_null_ecological_effect",
        "estimand_family_bottleneck_is_identification_not_raw_case_count",
    ]
    if complete:
        claim_ceiling.extend(
            [
                "current_29_fulltext_pending_records_cannot_expand_TOTAL_SELECTION_EFFECT_under_current_audit",
                "next_expansion_must_return_to_frozen_unscreened_cohort_outcome_blind",
            ]
        )

    result = {
        "analysis": "sch_h2_estimand_recovery_audit_cumulative_v2",
        "n_frozen_queue_records": len(queue),
        "n_audit_batches": len(audit_paths),
        "n_audited_records": len(audit),
        "n_unaudited_queue_records": unaudited,
        "audited_tier_counts": dict(sorted(tiers.items())),
        "decision_counts": dict(sorted(decisions.items())),
        "reason_counts": dict(sorted(reasons.items())),
        "n_total_selection_effect_promotions": len(promoted),
        "promoted_record_ids": promoted,
        "n_shared_trait_coordinate_failures": reasons[
            "NO_SHARED_TRAIT_COORDINATE"
        ],
        "promotion_rate": len(promoted) / len(audit) if audit else None,
        "fulltext_queue_audit_complete": complete,
        "next_screening_frontier": (
            "463_TITLE_ABSTRACT_UNSCREENED_RECORDS"
            if complete
            else "REMAINING_V20_FULLTEXT_PENDING"
        ),
        "status": (
            "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_COMPLETE_ZERO_TOTAL_SELECTION_PROMOTIONS"
            if complete and len(promoted) == 0
            else "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_PARTIAL_OR_PROMOTED"
        ),
        "claim_ceiling": claim_ceiling,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--audits", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.queue, args.audits)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
