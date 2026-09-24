from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

PRIMARY_CLASSES = {
    "MULTI_COMPONENT_OR_CONSUMER_TURNOVER",
    "SINGLE_REGISTERED_MODIFIER",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as h:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(h)
        ]


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _delta(q_a: list[float], q_b: list[float]) -> float:
    return _mean(q_a) - _mean(q_b)


def _permutation_upper(
    q_a: list[float],
    q_b: list[float],
    *,
    exact_if_assignments_lte: int,
    monte_carlo_draws: int,
    monte_carlo_seed: int,
) -> dict[str, object]:
    values = q_a + q_b
    n_a = len(q_a)
    n = len(values)
    observed = _delta(q_a, q_b)
    assignments = math.comb(n, n_a)

    def stat(a_idx: set[int]) -> float:
        aa = [values[i] for i in range(n) if i in a_idx]
        bb = [values[i] for i in range(n) if i not in a_idx]
        return _delta(aa, bb)

    if assignments <= exact_if_assignments_lte:
        extreme = 0
        total = 0
        for combo in itertools.combinations(range(n), n_a):
            total += 1
            if stat(set(combo)) >= observed - 1e-12:
                extreme += 1
        return {
            "method_used": "EXACT_PROGRAMME_LABEL_PERMUTATION",
            "n_assignments": total,
            "n_draws": None,
            "observed_delta": observed,
            "p_upper": extreme / total,
        }

    rng = random.Random(monte_carlo_seed)
    extreme = 0
    for _ in range(monte_carlo_draws):
        a_idx = set(rng.sample(range(n), n_a))
        if stat(a_idx) >= observed - 1e-12:
            extreme += 1
    return {
        "method_used": "MONTE_CARLO_PROGRAMME_LABEL_PERMUTATION_FIXED_SEED",
        "n_assignments": assignments,
        "n_draws": monte_carlo_draws,
        "observed_delta": observed,
        "p_upper": (extreme + 1) / (monte_carlo_draws + 1),
    }


def build(
    protocol_path: Path,
    registry_path: Path,
    holdout_queue_path: Path,
) -> dict[str, object]:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    rows = _read_csv(registry_path)
    holdout_rows = _read_csv(holdout_queue_path)

    holdout = protocol["holdout_source"]
    if _git_blob_sha(holdout_queue_path) != holdout["git_blob_sha"]:
        raise ValueError("frozen holdout queue blob SHA mismatch")
    if len(holdout_rows) != holdout["n_records"]:
        raise ValueError("frozen holdout queue record count mismatch")
    holdout_ids = {row["record_id"] for row in holdout_rows}
    if len(holdout_ids) != holdout["n_records"]:
        raise ValueError("frozen holdout queue record IDs are not unique")
    if {row["current_title_abstract_decision"] for row in holdout_rows} != {"UNSCREENED"}:
        raise ValueError("frozen holdout queue contains a screened record")
    if {row["outcome_blind_priority"] for row in holdout_rows} != {"YES"}:
        raise ValueError("frozen holdout queue is not outcome blind")

    development = set(protocol["development_programmes"])
    programme_ids = [row["programme_id"] for row in rows]
    if len(programme_ids) != len(set(programme_ids)):
        raise ValueError("held-out programme_id must be unique")

    overlap = sorted(set(programme_ids) & development)
    if overlap:
        raise ValueError(
            "development programme cannot enter held-out registry: "
            + ", ".join(overlap)
        )

    allowed_classes = set(protocol["predictor_classes"])
    scored_rows = []

    for row in rows:
        pid = row["programme_id"]
        if row["primary_source_id"] not in holdout_ids:
            raise ValueError(f"primary source is outside frozen holdout queue: {pid}")
        if row["estimand_family"] != "TOTAL_SELECTION_EFFECT":
            raise ValueError(f"held-out programme is not TOTAL_SELECTION_EFFECT: {pid}")
        if row["context_class"] not in allowed_classes:
            raise ValueError(f"invalid context class for {pid}: {row['context_class']}")
        if not row["first_qualified_commit"]:
            raise ValueError(f"missing first_qualified_commit: {pid}")
        if row["first_qualified_commit"] == protocol["development_baseline_commit_sha"]:
            raise ValueError(f"programme is not post-development holdout: {pid}")
        if not row["classification_basis"]:
            raise ValueError(f"missing classification_basis: {pid}")
        if row["classification_frozen_before_outcome"] != "YES":
            raise ValueError(f"context class was not frozen before outcome: {pid}")

        expected_primary = row["context_class"] in PRIMARY_CLASSES
        declared_primary = row["primary_eligible"] == "YES"
        if expected_primary != declared_primary:
            raise ValueError(f"primary_eligible mismatch for {pid}")

        state = row["outcome_adjudication_complete"]
        if state not in {"YES", "NO"}:
            raise ValueError(f"invalid outcome_adjudication_complete for {pid}")

        scored = dict(row)
        scored["q_j"] = None

        if state == "YES":
            if not row["outcome_adjudication_commit"]:
                raise ValueError(f"complete outcome lacks adjudication commit: {pid}")
            n_axes = int(row["n_eligible_repeated_axes"])
            n_rev = int(row["n_bidirectionally_supported_reversal_axes"])
            if n_axes < 1:
                raise ValueError(f"complete programme lacks eligible repeated axes: {pid}")
            if n_rev < 0 or n_rev > n_axes:
                raise ValueError(f"invalid reversal-axis count for {pid}")
            scored["q_j"] = n_rev / n_axes
        else:
            if row["n_eligible_repeated_axes"] or row["n_bidirectionally_supported_reversal_axes"]:
                raise ValueError(f"pending programme must not contain outcome counts: {pid}")
            if row["outcome_adjudication_commit"]:
                raise ValueError(f"pending programme must not contain outcome commit: {pid}")

        scored_rows.append(scored)

    complete_primary = [
        row for row in scored_rows
        if row["primary_eligible"] == "YES"
        and row["outcome_adjudication_complete"] == "YES"
    ]
    complete_external = [
        row for row in scored_rows
        if row["context_class"] == "EXTERNAL_SPATIAL_REPLICATION"
        and row["outcome_adjudication_complete"] == "YES"
    ]

    class_counts = Counter(row["context_class"] for row in complete_primary)
    gate = protocol["primary_test_gate"]
    gate_pass = all(
        class_counts.get(group, 0) >= gate["min_complete_programmes_per_primary_class"]
        for group in PRIMARY_CLASSES
    )

    test = None
    if gate_pass:
        q_a = [
            float(row["q_j"]) for row in complete_primary
            if row["context_class"] == "MULTI_COMPONENT_OR_CONSUMER_TURNOVER"
        ]
        q_b = [
            float(row["q_j"]) for row in complete_primary
            if row["context_class"] == "SINGLE_REGISTERED_MODIFIER"
        ]
        spec = protocol["primary_test"]
        test = _permutation_upper(
            q_a,
            q_b,
            exact_if_assignments_lte=spec["exact_if_assignments_lte"],
            monte_carlo_draws=spec["otherwise_monte_carlo_draws"],
            monte_carlo_seed=spec["monte_carlo_seed"],
        )

    any_reversal_counts = Counter(
        "YES" if float(row["q_j"]) > 0 else "NO"
        for row in complete_primary
    )

    return {
        "analysis": "sch_h2_reversal_holdout_v2",
        "protocol_status": protocol["status"],
        "n_development_programmes_excluded": len(development),
        "n_registered_heldout_programmes": len(rows),
        "n_complete_primary_programmes": len(complete_primary),
        "n_complete_external_spatial_programmes": len(complete_external),
        "complete_primary_class_counts": dict(sorted(class_counts.items())),
        "complete_primary_any_supported_reversal_counts": dict(
            sorted(any_reversal_counts.items())
        ),
        "primary_test_gate_pass": gate_pass,
        "primary_test": test,
        "test_status": (
            "PRIMARY_HOLDOUT_TEST_OPEN_AND_RUN"
            if gate_pass
            else "PRIMARY_HOLDOUT_TEST_NOT_OPEN"
        ),
        "status": "PROSPECTIVE_REVERSAL_HOLDOUT_V2_FROZEN",
        "claim_ceiling": protocol["claim_ceiling"],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("protocol", type=Path)
    p.add_argument("registry", type=Path)
    p.add_argument("holdout_queue", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    result = build(a.protocol, a.registry, a.holdout_queue)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
