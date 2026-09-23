from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

VERSION_RE = re.compile(r"SCREENING_DECISIONS_V(\d+)")

SELECTION_TERMS = ("selection", "selective", "fitness")
PERFORMANCE_TERMS = (
    "reproductive success",
    "reproductive output",
    "reproductive performance",
    "fecundity",
    "fruit set",
    "fruit production",
    "seed set",
    "seed production",
    "seed output",
)
CONTEXT_TERMS = (
    "population",
    "populations",
    "geographic",
    "geographical",
    "spatial",
    "temporal",
    "year",
    "years",
    "gradient",
    "habitat",
    "environment",
    "environmental",
    "fragmentation",
    "landscape",
    "variation",
    "context",
    "community",
    "communities",
)
TRAIT_TERMS = (
    "floral trait",
    "floral signal",
    "floral scent",
    "flower scent",
    "floral volatile",
    "floral color",
    "floral colour",
    "flower color",
    "flower colour",
    "floral display",
    "flower size",
    "floral morphology",
    "flower morphology",
    "corolla",
    "spur",
    "nectar",
    "reward",
    "phenology",
    "flower height",
    "floral architecture",
    "orientation",
)
POLLINATOR_TERMS = (
    "pollinator",
    "pollinators",
    "pollination",
    "pollinating",
    "flower visitor",
    "floral visitor",
)
ANTAGONIST_TERMS = (
    "herbivore",
    "herbivory",
    "florivore",
    "florivory",
    "seed predator",
    "seed predators",
    "nectar robber",
    "nectar robbing",
    "antagonist",
    "antagonists",
    "parasite",
    "parasites",
    "oviposition",
    "exploit",
)

TIER_RANK = {
    "TA0_EXPLICIT_SELECTION_FITNESS": 0,
    "TA1_FINAL_REPRODUCTIVE_PERFORMANCE": 1,
    "TA2_REPEATED_CONTEXT": 2,
    "TA3_OTHER_UNSCREENED": 3,
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _version(path: Path) -> int:
    match = VERSION_RE.search(path.name)
    if not match:
        raise ValueError(f"cannot parse screening version: {path.name}")
    return int(match.group(1))


def _matched(text: str, phrases: tuple[str, ...]) -> list[str]:
    return [phrase for phrase in phrases if phrase in text]


def classify_title(title: str) -> dict[str, object]:
    text = " ".join(title.lower().split())
    selection = _matched(text, SELECTION_TERMS)
    performance = _matched(text, PERFORMANCE_TERMS)
    context = _matched(text, CONTEXT_TERMS)
    trait = _matched(text, TRAIT_TERMS)
    pollinator = _matched(text, POLLINATOR_TERMS)
    antagonist = _matched(text, ANTAGONIST_TERMS)

    if selection:
        tier = "TA0_EXPLICIT_SELECTION_FITNESS"
    elif performance:
        tier = "TA1_FINAL_REPRODUCTIVE_PERFORMANCE"
    elif context:
        tier = "TA2_REPEATED_CONTEXT"
    else:
        tier = "TA3_OTHER_UNSCREENED"

    return {
        "priority_tier": tier,
        "selection_title_matches": ";".join(selection),
        "performance_title_matches": ";".join(performance),
        "context_title_matches": ";".join(context),
        "trait_title_matches": ";".join(trait),
        "pollinator_title_matches": ";".join(pollinator),
        "antagonist_title_matches": ";".join(antagonist),
        "title_triple_signal": bool(trait and pollinator and antagonist),
        "title_trait_signal": bool(trait),
        "title_context_signal": bool(context),
        "n_priority_phrase_matches": len(set(selection + performance + context)),
    }


def build(frozen_path: Path, prisma_dir: Path) -> tuple[list[dict[str, str]], dict]:
    frozen = _read(frozen_path)

    files = sorted(
        prisma_dir.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"),
        key=_version,
    )
    versions = [_version(path) for path in files]
    if versions != list(range(1, max(versions, default=0) + 1)):
        raise ValueError(f"screening overlay versions are not contiguous: {versions}")

    screened_ids: set[str] = set()
    for path in files:
        for row in _read(path):
            if row.get("screen_title_abstract") in {"RETAIN_FULLTEXT", "EXCLUDE"}:
                screened_ids.add(row["record_id"])

    unscreened = [row for row in frozen if row["record_id"] not in screened_ids]

    queue: list[dict[str, str]] = []
    for row in unscreened:
        signals = classify_title(row["title"])
        queue.append(
            {
                "record_id": row["record_id"],
                "doi": row["doi"],
                "title": row["title"],
                "year": row["year"],
                "venue": row["venue"],
                "query_ids": row["query_ids"],
                "priority_tier": str(signals["priority_tier"]),
                "selection_title_matches": str(signals["selection_title_matches"]),
                "performance_title_matches": str(signals["performance_title_matches"]),
                "context_title_matches": str(signals["context_title_matches"]),
                "trait_title_matches": str(signals["trait_title_matches"]),
                "pollinator_title_matches": str(signals["pollinator_title_matches"]),
                "antagonist_title_matches": str(signals["antagonist_title_matches"]),
                "title_triple_signal": "YES" if signals["title_triple_signal"] else "NO",
                "title_trait_signal": "YES" if signals["title_trait_signal"] else "NO",
                "title_context_signal": "YES" if signals["title_context_signal"] else "NO",
                "n_priority_phrase_matches": str(signals["n_priority_phrase_matches"]),
                "formal_title_abstract_decision": "",
                "priority_status": "OUTCOME_BLIND_REVIEW_ORDER_ONLY",
            }
        )

    queue.sort(
        key=lambda row: (
            TIER_RANK[row["priority_tier"]],
            0 if row["title_triple_signal"] == "YES" else 1,
            0 if row["title_trait_signal"] == "YES" else 1,
            0 if row["title_context_signal"] == "YES" else 1,
            -int(row["n_priority_phrase_matches"]),
            row["record_id"],
        )
    )

    for index, row in enumerate(queue, start=1):
        row["review_order"] = str(index)

    tier_counts = Counter(row["priority_tier"] for row in queue)
    receipt = {
        "analysis": "sch_ta_unscreened_estimand_priority_v1",
        "n_frozen_candidates": len(frozen),
        "n_formally_ta_screened": len(screened_ids),
        "n_unscreened_priority_queue": len(queue),
        "tier_counts": dict(sorted(tier_counts.items())),
        "n_title_triple_signal": sum(row["title_triple_signal"] == "YES" for row in queue),
        "n_title_trait_signal": sum(row["title_trait_signal"] == "YES" for row in queue),
        "n_title_context_signal": sum(row["title_context_signal"] == "YES" for row in queue),
        "n_formal_decisions_generated": sum(bool(row["formal_title_abstract_decision"]) for row in queue),
        "status": "UNSCREENED_ESTIMAND_PRIORITY_QUEUE_FROZEN_OUTCOME_BLIND",
        "claim_ceiling": [
            "priority_changes_review_order_only",
            "no_title_abstract_decision_is_generated",
            "no_fulltext_decision_is_generated",
            "no_ecological_outcome_sign_is_used",
            "same_axis_common_outcome_and_estimand_rules_are_unchanged",
            "priority_rule_is_frozen_before_next_title_abstract_screen",
        ],
    }
    return queue, receipt


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("empty unscreened priority queue")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["review_order"] + [key for key in rows[0] if key != "review_order"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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
    args.out_json.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
