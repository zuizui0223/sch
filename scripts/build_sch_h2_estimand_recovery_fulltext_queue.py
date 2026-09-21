from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

TIER_ORDER = {
    "FT0_EXPLICIT_SELECTION": 0,
    "FT1_FINAL_PERFORMANCE": 1,
    "FT2_CONTEXT_RICH": 2,
    "FT3_OTHER_RETAINED": 3,
}

PATTERNS = {
    "explicit_selection_signal": re.compile(r"\b(selection|selective)\b", re.I),
    "final_performance_signal": re.compile(
        r"\b(fitness|reproductive success|reproductive output|reproduction|fruit set|seed set|seed production)\b",
        re.I,
    ),
    "repeated_context_signal": re.compile(
        r"\b(geographic|population|populations|spatial|temporal|year|years|variation|vary|varies|mosaic|gradient|gradients|treatment|experiment|experimental|restored|unrestored|fragmentation)\b",
        re.I,
    ),
    "focal_trait_signal": re.compile(
        r"\b(floral|flower|flowers|trait|traits|morph|morphology|scent|color|colour|corolla|nectar|display)\b",
        re.I,
    ),
    "pollinator_signal": re.compile(
        r"\b(pollinat\w*|pollinator\w*|bumblebee\w*|hummingbird\w*|bee\w*)\b",
        re.I,
    ),
    "antagonist_signal": re.compile(
        r"\b(herbiv\w*|floriv\w*|seed pred\w*|nectar rob\w*|robber\w*|graz\w*|antagon\w*|parasit\w*|oviposit\w*|exploit\w*)\b",
        re.I,
    ),
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _flag(text: str, key: str) -> bool:
    return bool(PATTERNS[key].search(text))


def _tier(flags: dict[str, bool]) -> str:
    if (
        flags["explicit_selection_signal"]
        and flags["focal_trait_signal"]
        and flags["pollinator_signal"]
        and flags["antagonist_signal"]
    ):
        return "FT0_EXPLICIT_SELECTION"
    if (
        flags["final_performance_signal"]
        and flags["focal_trait_signal"]
        and flags["pollinator_signal"]
        and flags["antagonist_signal"]
    ):
        return "FT1_FINAL_PERFORMANCE"
    if (
        flags["repeated_context_signal"]
        and flags["focal_trait_signal"]
        and flags["pollinator_signal"]
        and flags["antagonist_signal"]
    ):
        return "FT2_CONTEXT_RICH"
    return "FT3_OTHER_RETAINED"


def build(frozen_path: Path, v20_path: Path) -> tuple[list[dict[str, str]], dict]:
    frozen = {row["record_id"]: row for row in _read(frozen_path)}
    v20 = _read(v20_path)

    pending = [row for row in v20 if row["screen_title_abstract"] == "RETAIN_FULLTEXT"]
    if len(pending) != 29:
        raise ValueError(f"expected 29 V20 retained full-text candidates, found {len(pending)}")

    rows: list[dict[str, str]] = []
    for update in pending:
        source = frozen[update["record_id"]]
        text = f"{source['title']} {update.get('decision_note', '')}"
        flags = {key: _flag(text, key) for key in PATTERNS}
        tier = _tier(flags)

        if tier in {"FT0_EXPLICIT_SELECTION", "FT1_FINAL_PERFORMANCE"}:
            target = "TOTAL_SELECTION_EFFECT_CANDIDATE_UNCONFIRMED"
        elif tier == "FT2_CONTEXT_RICH":
            target = "REPEATED_CONTEXT_ESTIMAND_CANDIDATE_UNCONFIRMED"
        else:
            target = "GENERAL_FULLTEXT_ADJUDICATION"

        rows.append(
            {
                "record_id": source["record_id"],
                "doi": source["doi"],
                "title": source["title"],
                "year": source["year"],
                "venue": source["venue"],
                "query_ids": source["query_ids"],
                "recovery_tier": tier,
                "explicit_selection_signal": "YES" if flags["explicit_selection_signal"] else "NO",
                "final_performance_signal": "YES" if flags["final_performance_signal"] else "NO",
                "repeated_context_signal": "YES" if flags["repeated_context_signal"] else "NO",
                "focal_trait_signal": "YES" if flags["focal_trait_signal"] else "NO",
                "pollinator_signal": "YES" if flags["pollinator_signal"] else "NO",
                "antagonist_signal": "YES" if flags["antagonist_signal"] else "NO",
                "estimand_recovery_target": target,
                "current_title_abstract_decision": update["screen_title_abstract"],
                "decision_note": update.get("decision_note", ""),
                "fulltext_recovery_status": "PENDING",
                "outcome_blind_priority": "YES",
            }
        )

    rows.sort(key=lambda row: (TIER_ORDER[row["recovery_tier"]], row["record_id"]))
    for i, row in enumerate(rows, 1):
        row["review_order"] = str(i)

    tier_counts = Counter(row["recovery_tier"] for row in rows)
    priority_ids = [
        row["record_id"]
        for row in rows
        if row["recovery_tier"] != "FT3_OTHER_RETAINED"
    ]

    receipt = {
        "analysis": "sch_h2_estimand_recovery_fulltext_queue_v1",
        "source_screening_version": 20,
        "n_fulltext_pending": len(rows),
        "tier_counts": dict(sorted(tier_counts.items())),
        "n_selection_or_performance_priority": sum(
            row["recovery_tier"] in {"FT0_EXPLICIT_SELECTION", "FT1_FINAL_PERFORMANCE"}
            for row in rows
        ),
        "n_context_rich_priority": tier_counts["FT2_CONTEXT_RICH"],
        "priority_record_ids": priority_ids,
        "status": "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_FROZEN_OUTCOME_BLIND",
        "claim_ceiling": [
            "priority_changes_review_order_not_inclusion",
            "title_and_existing_title_abstract_notes_only",
            "no_ecological_outcome_sign_used_for_priority",
            "candidate_estimand_family_is_unconfirmed_until_fulltext",
            "fulltext_adjudication_must_preserve_same_axis_and_common_outcome_gates",
        ],
    }
    return rows, receipt


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty estimand recovery queue")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen", type=Path)
    parser.add_argument("v20", type=Path)
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(args.frozen, args.v20)
    write_csv(args.out_csv, rows)
    args.out_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
