from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

PRIMARY_CLASSES = {
    "MULTI_COMPONENT_OR_ASSEMBLAGE",
    "SINGLE_REGISTERED_MODIFIER",
}
OUTCOMES = {"YES", "NO", "PENDING", ""}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as h:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(h)
        ]


def _fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    row1 = a + b
    row2 = c + d
    col1 = a + c
    n = row1 + row2

    def prob(x: int) -> float:
        return (
            math.comb(row1, x)
            * math.comb(row2, col1 - x)
            / math.comb(n, col1)
        )

    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    p_obs = prob(a)
    return min(
        1.0,
        sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12),
    )


def build(protocol_path: Path, registry_path: Path) -> dict:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    rows = _read_csv(registry_path)
    development = set(protocol["development_programmes"])

    ids = [row["programme_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("held-out programme_id must be unique")

    overlap = sorted(set(ids) & development)
    if overlap:
        raise ValueError(
            "development programme cannot enter held-out registry: "
            + ", ".join(overlap)
        )

    allowed_classes = set(protocol["predictor_classes"])
    for row in rows:
        if row["estimand_family"] != "TOTAL_SELECTION_EFFECT":
            raise ValueError(
                f"held-out programme is not TOTAL_SELECTION_EFFECT: {row['programme_id']}"
            )
        if row["context_dimensionality_class"] not in allowed_classes:
            raise ValueError(
                f"invalid context class for {row['programme_id']}: "
                f"{row['context_dimensionality_class']}"
            )
        if not row["first_qualified_commit"]:
            raise ValueError(
                f"missing first_qualified_commit: {row['programme_id']}"
            )
        if not row["classification_basis"]:
            raise ValueError(
                f"missing classification_basis: {row['programme_id']}"
            )
        if row["classification_frozen_before_outcome"] != "YES":
            raise ValueError(
                f"context class was not frozen before outcome: {row['programme_id']}"
            )
        if row["any_bidirectional_supported_reversal"] not in OUTCOMES:
            raise ValueError(
                f"invalid outcome for {row['programme_id']}"
            )
        if int(row["n_repeated_axes"]) < 1:
            raise ValueError(
                f"held-out programme lacks a repeated axis: {row['programme_id']}"
            )

        expected_eligible = (
            row["context_dimensionality_class"] in PRIMARY_CLASSES
        )
        declared_eligible = row["primary_eligible"] == "YES"
        if expected_eligible != declared_eligible:
            raise ValueError(
                f"primary_eligible mismatch for {row['programme_id']}"
            )
        if (
            row["any_bidirectional_supported_reversal"] in {"YES", "NO"}
            and not row["outcome_adjudication_commit"]
        ):
            raise ValueError(
                f"resolved outcome lacks adjudication commit: {row['programme_id']}"
            )

    resolved = [
        row for row in rows
        if row["primary_eligible"] == "YES"
        and row["any_bidirectional_supported_reversal"] in {"YES", "NO"}
    ]

    class_counts = Counter(row["context_dimensionality_class"] for row in resolved)
    outcome_counts = Counter(row["any_bidirectional_supported_reversal"] for row in resolved)

    gate = protocol["primary_test_gate"]
    gate_pass = (
        len(resolved) >= gate["min_primary_eligible_programmes"]
        and all(
            class_counts.get(group, 0) >= gate["min_programmes_per_predictor_class"]
            for group in PRIMARY_CLASSES
        )
        and outcome_counts.get("YES", 0) >= gate["min_programmes_with_outcome_yes"]
        and outcome_counts.get("NO", 0) >= gate["min_programmes_with_outcome_no"]
    )

    contingency = None
    fisher_p = None
    odds_ratio = None
    if gate_pass:
        a = sum(
            row["context_dimensionality_class"] == "MULTI_COMPONENT_OR_ASSEMBLAGE"
            and row["any_bidirectional_supported_reversal"] == "YES"
            for row in resolved
        )
        b = sum(
            row["context_dimensionality_class"] == "MULTI_COMPONENT_OR_ASSEMBLAGE"
            and row["any_bidirectional_supported_reversal"] == "NO"
            for row in resolved
        )
        c = sum(
            row["context_dimensionality_class"] == "SINGLE_REGISTERED_MODIFIER"
            and row["any_bidirectional_supported_reversal"] == "YES"
            for row in resolved
        )
        d = sum(
            row["context_dimensionality_class"] == "SINGLE_REGISTERED_MODIFIER"
            and row["any_bidirectional_supported_reversal"] == "NO"
            for row in resolved
        )
        contingency = {
            "multi_component_yes": a,
            "multi_component_no": b,
            "single_modifier_yes": c,
            "single_modifier_no": d,
        }
        fisher_p = _fisher_two_sided(a, b, c, d)
        if b * c == 0:
            odds_ratio = "INFINITE" if a * d > 0 else "UNDEFINED_ZERO_CELL"
        else:
            odds_ratio = a * d / (b * c)

    return {
        "analysis": "sch_h2_reversal_holdout_v1",
        "baseline_commit_sha": protocol["baseline_commit_sha"],
        "n_development_programmes_excluded": len(development),
        "n_registered_heldout_programmes": len(rows),
        "n_primary_eligible_resolved_programmes": len(resolved),
        "resolved_predictor_class_counts": dict(sorted(class_counts.items())),
        "resolved_outcome_counts": dict(sorted(outcome_counts.items())),
        "primary_test_gate_pass": gate_pass,
        "contingency_table": contingency,
        "odds_ratio": odds_ratio,
        "fisher_two_sided_p": fisher_p,
        "test_status": (
            "PRIMARY_HOLDOUT_TEST_OPEN_AND_RUN"
            if gate_pass
            else "PRIMARY_HOLDOUT_TEST_NOT_OPEN"
        ),
        "status": "PROSPECTIVE_REVERSAL_HOLDOUT_FROZEN",
        "claim_ceiling": protocol["claim_ceiling"],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("protocol", type=Path)
    p.add_argument("registry", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    result = build(a.protocol, a.registry)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
