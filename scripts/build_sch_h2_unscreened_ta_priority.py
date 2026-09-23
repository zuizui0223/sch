from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

TIER_ORDER = {
    "TA0_EXPLICIT_SELECTION": 0,
    "TA1_FINAL_PERFORMANCE": 1,
    "TA2_REPEATED_CONTEXT": 2,
    "TA3_REMAINDER": 3,
}

PATTERNS = {
    "explicit_selection_signal": re.compile(
        r"\b(selection|selective|selected|natural selection|phenotypic selection|selection gradient|selection gradients)\b",
        re.I,
    ),
    "final_performance_signal": re.compile(
        r"\b(fitness|reproductive success|reproductive output|reproduction|fruit set|seed set|seed production|fecundity)\b",
        re.I,
    ),
    "repeated_context_signal": re.compile(
        r"\b(geographic|geographical|population|populations|spatial|temporal|year|years|variation|vary|varies|mosaic|gradient|gradients|treatment|experiment|experimental|multisite|multi-site)\b",
        re.I,
    ),
    "title_trait_signal": re.compile(
        r"\b(floral|flower|flowers|corolla|petal|scape|nectar|scent|odor|odour|volatile|color|colour|display|morph|morphology|trait|traits|spur|inflorescence)\b",
        re.I,
    ),
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise ValueError(f"cannot parse screening version from {path.name}")
    return int(match.group(1))


def _decision_files(prisma_dir: Path, max_version: int = 20) -> list[Path]:
    files = [
        path
        for path in prisma_dir.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv")
        if _version(path) <= max_version
    ]
    files.sort(key=_version)
    versions = sorted({_version(path) for path in files})
    if versions != list(range(1, max_version + 1)):
        raise ValueError(f"expected screening versions 1..{max_version}, found {versions}")
    return files


def _screened_title_abstract_ids(prisma_dir: Path) -> set[str]:
    screened: set[str] = set()
    for path in _decision_files(prisma_dir):
        for row in _read(path):
            if row.get("screen_title_abstract"):
                screened.add(row["record_id"])
    return screened


def _flags(title: str) -> dict[str, bool]:
    return {key: bool(pattern.search(title)) for key, pattern in PATTERNS.items()}


def _tier(flags: dict[str, bool]) -> str:
    if flags["explicit_selection_signal"] and flags["title_trait_signal"]:
        return "TA0_EXPLICIT_SELECTION"
    if flags["final_performance_signal"] and flags["title_trait_signal"]:
        return "TA1_FINAL_PERFORMANCE"
    if flags["repeated_context_signal"] and flags["title_trait_signal"]:
        return "TA2_REPEATED_CONTEXT"
    return "TA3_REMAINDER"


def build(
    frozen_path: Path,
    prisma_dir: Path,
) -> tuple[list[dict[str, str]], dict]:
    frozen = _read(frozen_path)
    if len(frozen) != 868:
        raise ValueError(f"expected frozen denominator 868, found {len(frozen)}")

    screened = _screened_title_abstract_ids(prisma_dir)
    if len(screened) != 405:
        raise ValueError(f"expected 405 title/abstract-screened IDs through V20, found {len(screened)}")

    rows: list[dict[str, str]] = []
    for source in frozen:
        if source["record_id"] in screened:
            continue
        flags = _flags(source["title"])
        tier = _tier(flags)
        if tier in {"TA0_EXPLICIT_SELECTION", "TA1_FINAL_PERFORMANCE"}:
            target = "TOTAL_SELECTION_EFFECT_CANDIDATE_UNCONFIRMED"
        elif tier == "TA2_REPEATED_CONTEXT":
            target = "REPEATED_CONTEXT_ESTIMAND_CANDIDATE_UNCONFIRMED"
        else:
            target = "GENERAL_TITLE_ABSTRACT_SCREENING"

        rows.append(
            {
                "record_id": source["record_id"],
                "doi": source["doi"],
                "title": source["title"],
                "year": source["year"],
                "venue": source["venue"],
                "query_ids": source["query_ids"],
                "priority_tier": tier,
                "explicit_selection_signal": "YES" if flags["explicit_selection_signal"] else "NO",
                "final_performance_signal": "YES" if flags["final_performance_signal"] else "NO",
                "repeated_context_signal": "YES" if flags["repeated_context_signal"] else "NO",
                "title_trait_signal": "YES" if flags["title_trait_signal"] else "NO",
                "registered_query_context": "YES",
                "estimand_recovery_target": target,
                "current_title_abstract_decision": "UNSCREENED",
                "title_abstract_screening_status": "PENDING",
                "outcome_blind_priority": "YES",
                "priority_basis": "TITLE_PLUS_FROZEN_QUERY_METADATA_ONLY",
            }
        )

    rows.sort(key=lambda row: (TIER_ORDER[row["priority_tier"]], row["record_id"]))
    for i, row in enumerate(rows, 1):
        row["review_order"] = str(i)

    tiers = Counter(row["priority_tier"] for row in rows)
    receipt = {
        "analysis": "sch_h2_unscreened_title_abstract_priority_v1",
        "source_screening_version": 20,
        "frozen_denominator": len(frozen),
        "n_already_title_abstract_screened": len(screened),
        "n_unscreened_priority_queue": len(rows),
        "tier_counts": dict(sorted(tiers.items())),
        "n_total_selection_priority": sum(
            row["priority_tier"] in {"TA0_EXPLICIT_SELECTION", "TA1_FINAL_PERFORMANCE"}
            for row in rows
        ),
        "n_repeated_context_priority": tiers["TA2_REPEATED_CONTEXT"],
        "top_tier_record_ids": [
            row["record_id"]
            for row in rows
            if row["priority_tier"] == "TA0_EXPLICIT_SELECTION"
        ],
        "status": "UNSCREENED_463_PRIORITY_QUEUE_FROZEN_OUTCOME_BLIND",
        "claim_ceiling": [
            "priority_changes_review_order_not_title_abstract_inclusion",
            "title_and_frozen_query_metadata_only",
            "no_ecological_result_sign_or_significance_used_for_priority",
            "candidate_estimand_family_is_unconfirmed_until_screening_and_fulltext",
            "formal_prisma_denominator_remains_868",
            "existing_405_title_abstract_decisions_are_not_modified",
        ],
    }
    return rows, receipt


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty title/abstract priority queue")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen", type=Path)
    parser.add_argument("prisma_dir", type=Path)
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(args.frozen, args.prisma_dir)
    write_csv(args.out_csv, rows)
    args.out_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
