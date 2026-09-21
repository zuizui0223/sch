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


def build(queue_path: Path, audit_path: Path) -> dict:
    queue = _read(queue_path)
    audit = _read(audit_path)

    queue_by_id = {row["record_id"]: row for row in queue}
    if len(queue_by_id) != len(queue):
        raise ValueError("queue record_id must be unique")

    audited_ids = [row["record_id"] for row in audit]
    if len(audited_ids) != len(set(audited_ids)):
        raise ValueError("audit record_id must be unique")

    unknown = sorted(set(audited_ids) - set(queue_by_id))
    if unknown:
        raise ValueError("audit contains record not in frozen queue: " + ", ".join(unknown))

    tier_mismatch = [
        row["record_id"]
        for row in audit
        if row["recovery_tier"] != queue_by_id[row["record_id"]]["recovery_tier"]
    ]
    if tier_mismatch:
        raise ValueError("audit tier drift: " + ", ".join(sorted(tier_mismatch)))

    decisions = Counter(row["estimand_recovery_decision"] for row in audit)
    reasons = Counter(row["reason_code"] for row in audit)
    tiers = Counter(row["recovery_tier"] for row in audit)

    promoted = [
        row["record_id"]
        for row in audit
        if row["estimand_recovery_decision"] == "PROMOTED_TOTAL_SELECTION_EFFECT"
    ]

    return {
        "analysis": "sch_h2_estimand_recovery_audit_batch1_v1",
        "n_frozen_queue_records": len(queue),
        "n_audited_records": len(audit),
        "n_unaudited_queue_records": len(queue) - len(audit),
        "audited_tier_counts": dict(sorted(tiers.items())),
        "decision_counts": dict(sorted(decisions.items())),
        "reason_counts": dict(sorted(reasons.items())),
        "n_total_selection_effect_promotions": len(promoted),
        "promoted_record_ids": promoted,
        "status": "ESTIMAND_RECOVERY_BATCH1_AUDITED_NO_TOTAL_SELECTION_PROMOTIONS",
        "claim_ceiling": [
            "negative_recovery_yield_does_not_change_formal_prisma_inclusion_by_itself",
            "queue_priority_was_frozen_before_fulltext_outcome_adjudication",
            "title_or_abstract_estimand_signal_is_not_an_estimand",
            "same_trait_consumer_components_and_common_outcome_remain_required",
            "do_not_retune_batch1_priority_rules_after_observing_zero_promotions",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("audit", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.queue, args.audit)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
