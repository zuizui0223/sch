from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

HOLDOUT_QUEUE = "data/SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
HOLDOUT_QUEUE_BLOB_SHA = "1ffd1849b4381a43bb85b2d3473161caabdac510"

PILOT_PROGRAMMES = (
    "Gymnadenia_conopsea_agent_selection",
    "Trifolium_repens_selection_program",
    "Erysimum_mediohispanicum_selection_mosaic",
    "Brassica_rapa_Knauer_selection_program",
    "Lobelia_cardinalis_Bartkowska_selection_program",
    "Dalechampia_scandens_Perez_Barrales_selection_program",
    "Lythrum_salicaria_Thomsen_selection_program",
    "Helianthus_annuus_texanus_Mitchell_selection_program",
)

PRIMARY_CLASSES = (
    "MULTIWEIGHT_OR_CONSUMER_TURNOVER",
    "SINGLE_FACTOR_INTENSITY",
)

MIN_NEW_PROGRAMMES_PER_PRIMARY_CLASS = 5


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def classify_context_design(
    *,
    experimental: bool,
    observational_spatial: bool,
    n_manipulated_biotic_dimensions: int,
    consumer_identity_or_composition_changes: bool,
) -> str:
    """Classify design before any selection sign or significance is extracted."""
    if observational_spatial:
        return "EXTERNAL_SPATIAL_REPLICATION"
    if not experimental:
        return "UNCLASSIFIABLE_FAIL_CLOSED"
    if consumer_identity_or_composition_changes:
        return "MULTIWEIGHT_OR_CONSUMER_TURNOVER"
    if n_manipulated_biotic_dimensions >= 2:
        return "MULTIWEIGHT_OR_CONSUMER_TURNOVER"
    if n_manipulated_biotic_dimensions == 1:
        return "SINGLE_FACTOR_INTENSITY"
    return "UNCLASSIFIABLE_FAIL_CLOSED"


def confirmatory_gate(
    *,
    n_multiweight_programmes: int,
    n_single_factor_programmes: int,
) -> dict[str, object]:
    class_gate = (
        n_multiweight_programmes >= MIN_NEW_PROGRAMMES_PER_PRIMARY_CLASS
        and n_single_factor_programmes >= MIN_NEW_PROGRAMMES_PER_PRIMARY_CLASS
    )
    return {
        "class_breadth_pass": class_gate,
        "primary_inference_licensed": class_gate,
    }


def build(root: Path) -> dict[str, object]:
    queue = _read_csv(root / HOLDOUT_QUEUE)

    if len(queue) != 463:
        raise ValueError(f"holdout queue must contain 463 records, found {len(queue)}")
    if len({row["record_id"] for row in queue}) != 463:
        raise ValueError("holdout queue record IDs are not unique")
    if {row["current_title_abstract_decision"] for row in queue} != {"UNSCREENED"}:
        raise ValueError("holdout queue contains a previously screened record")
    if {row["title_abstract_screening_status"] for row in queue} != {"PENDING"}:
        raise ValueError("holdout queue contains a non-pending record")
    if {row["outcome_blind_priority"] for row in queue} != {"YES"}:
        raise ValueError("holdout priority must remain outcome blind")

    tier_counts = Counter(row["priority_tier"] for row in queue)
    expected_tiers = {
        "TA0_EXPLICIT_SELECTION": 32,
        "TA1_FINAL_PERFORMANCE": 25,
        "TA2_REPEATED_CONTEXT": 20,
        "TA3_REMAINDER": 386,
    }
    if dict(tier_counts) != expected_tiers:
        raise ValueError(
            f"holdout tier counts changed: {dict(tier_counts)} != {expected_tiers}"
        )

    return {
        "analysis": "sch_h2_prospective_reversal_hypothesis_v12",
        "hypothesis": (
            "new experimental programmes that alter multiple biotic weights or "
            "consumer identity/composition will show a larger programme-level "
            "fraction of uncertainty-supported directional-reversal axes than "
            "new single-factor intensity programmes"
        ),
        "pilot_status": "V11_HYPOTHESIS_GENERATING_ONLY",
        "n_pilot_programmes_excluded": len(PILOT_PROGRAMMES),
        "pilot_programmes_excluded": list(PILOT_PROGRAMMES),
        "holdout_source": HOLDOUT_QUEUE,
        "holdout_source_blob_sha": HOLDOUT_QUEUE_BLOB_SHA,
        "formal_prisma_denominator": 868,
        "n_holdout_records": len(queue),
        "holdout_tier_counts": expected_tiers,
        "screening_rule": (
            "retain the pre-existing frozen review order and title/abstract "
            "eligibility rules; do not reprioritize using V11 outcomes"
        ),
        "design_classification_timing": "BEFORE_SELECTION_SIGN_OR_SIGNIFICANCE_EXTRACTION",
        "primary_classes": list(PRIMARY_CLASSES),
        "external_replication_class": "EXTERNAL_SPATIAL_REPLICATION",
        "fail_closed_class": "UNCLASSIFIABLE_FAIL_CLOSED",
        "primary_unit": "INDEPENDENT_BIOLOGICAL_PROGRAMME",
        "axis_eligibility": (
            "same TOTAL_SELECTION_EFFECT trait axis observed in at least two "
            "source-defined qualified contexts with usable uncertainty; all "
            "uncertainty-resolved source-defined contexts are evaluated without "
            "selecting a favorable pair after sign inspection"
        ),
        "axis_event": (
            "at least one supported-positive context and at least one "
            "supported-negative context on the same eligible trait axis"
        ),
        "programme_score": (
            "q_j = bidirectionally_supported_reversal_axes / eligible_repeated_axes"
        ),
        "primary_estimand": (
            "mean(q_j | MULTIWEIGHT_OR_CONSUMER_TURNOVER) - "
            "mean(q_j | SINGLE_FACTOR_INTENSITY)"
        ),
        "directional_prediction": "PRIMARY_ESTIMAND_GT_0",
        "secondary_programme_event": (
            "programme contains at least one bidirectionally supported reversal axis"
        ),
        "minimum_new_programmes_per_primary_class": MIN_NEW_PROGRAMMES_PER_PRIMARY_CLASS,
        "primary_inference": (
            "upper-tail exact programme-label permutation test for the difference in "
            "equal-programme-weighted mean q_j, only after the design-breadth gate passes; "
            "zero observed reversal is retained as a valid result"
        ),
        "before_gate_output": "DESCRIPTIVE_COUNTS_ONLY_FAIL_CLOSED",
        "spatial_rule": (
            "observational spatial/landscape programmes are external replication "
            "and are never pooled into the primary causal class comparison"
        ),
        "status": "PROSPECTIVE_HOLDOUT_HYPOTHESIS_FROZEN",
        "claim_ceiling": [
            "current_8_programme_v11_family_is_pilot_only",
            "all_463_previously_unscreened_records_are_the_holdout_source",
            "screening_order_must_not_use_v11_outcomes",
            "design_class_is_frozen_before_selection_outcome_extraction",
            "programme_is_the_inferential_unit",
            "trait_axes_are_not_independent_replicates",
            "no_primary_inference_before_registered_design_breadth_gate",
            "observational_spatial_programmes_are_external_replication_only",
            "a_failed_directional_prediction_is_a_valid_confirmatory_result",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--out-json", type=Path)
    args = parser.parse_args()

    result = build(args.root)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
