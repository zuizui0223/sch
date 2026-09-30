from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CONGENERIC_QUANTITATIVE_PRIORS_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("congeneric quantitative prior ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("congeneric quantitative prior ledger is empty")
    return rows


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)

    ids = [row["prior_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("congeneric prior_id must be unique")

    if {row["direct_P_rex_effect"] for row in rows} != {"NO"}:
        raise ValueError(
            "congeneric quantitative priors must not be labelled as direct P. rex effects"
        )
    if {row["direct_F0_freeze_eligible"] for row in rows} != {"NO"}:
        raise ValueError(
            "congeneric quantitative priors must not directly freeze F0"
        )

    species_counts = Counter(row["species"] for row in rows)
    stage_counts = Counter()
    for row in rows:
        for stage in (part.strip() for part in row["stage"].split(";")):
            if stage:
                stage_counts[stage] += 1

    p0 = sorted(row["prior_id"] for row in rows if "P0" in row["stage"])
    p1 = sorted(row["prior_id"] for row in rows if "P1" in row["stage"])

    relative_effects = sorted(
        row["prior_id"]
        for row in rows
        if row["estimate_type"] in {"RELATIVE_RATIO", "RELATIVE_INCREASE"}
    )
    exact_mean_se = sorted(
        row["prior_id"]
        for row in rows
        if row["estimate_type"] == "MEAN" and row["uncertainty_type"] == "SE"
    )
    near_zero_effect_precedents = sorted(
        row["prior_id"]
        for row in rows
        if "near-zero" in row["external_use"].lower()
        or row["estimate_type"] == "NULL_EFFECT_RESULT"
    )

    p1_design_families = {
        "within_plant_or_flower_level_supplementation": [
            "PCQ_P1_MONB2005_OPEN_SEED",
            "PCQ_P1_MONB2005_GEIT_SEED",
            "PCQ_P1_MONB2005_SUPP_TEST",
            "PCQ_P1_DAI2017_PLX_INTERACTION",
        ],
        "whole_plant_supplementation": [
            "PCQ_P1_MONB2011_FRUIT_F",
            "PCQ_P1_MONB2011_SEED_F",
            "PCQ_P1_MONB2011_PURE_SPARSE",
            "PCQ_P1_MONB2011_PURE_DENSE",
            "PCQ_P1_MONB2011_MIXED_SPARSE",
            "PCQ_P1_MONB2011_MIXED_DENSE",
            "PCQ_P1_MONB2011_INTERACTION",
        ],
        "patch_context_supplementation": [
            "PCQ_P1_DENSISPICA_VISITS_MIXED",
            "PCQ_P1_DENSISPICA_VISITS_PURE",
            "PCQ_P1_DENSISPICA_PL_S",
        ],
        "whole_plant_exclosure_hand_natural_context": [
            "PCQ_P1_PALUSTRIS_EXCLOSURE",
            "PCQ_P1_PALUSTRIS_SELF_COMPAT_LOW",
            "PCQ_P1_PALUSTRIS_SELF_COMPAT_HIGH",
            "PCQ_P1_PALUSTRIS_DISPLAY",
        ],
    }

    return {
        "analysis": "pedicularis_congeneric_quantitative_prior_audit_v1",
        "n_quantitative_prior_rows": len(rows),
        "n_species": len(species_counts),
        "species_counts": dict(sorted(species_counts.items())),
        "stage_counts": dict(sorted(stage_counts.items())),
        "p0_prior_rows": p0,
        "p1_prior_rows": p1,
        "n_p0_prior_rows": len(p0),
        "n_p1_prior_rows": len(p1),
        "relative_effect_rows": relative_effects,
        "exact_mean_se_rows": exact_mean_se,
        "near_zero_effect_precedents": near_zero_effect_precedents,
        "p1_design_families": p1_design_families,
        "p1_effect_range_statement": (
            "Congeneric supplementation spans effectively null responses "
            "through large positive responses (up to 2.1x control in a "
            "reported context), so no single congeneric effect is portable "
            "to P. rex."
        ),
        "n_direct_P_rex_effect_rows": 0,
        "n_direct_F0_values": 0,
        "status": (
            "CONGENERIC_QUANTITATIVE_PRIORS_RECOVERED_"
            "P_REX_EFFECT_STILL_REQUIRED"
        ),
        "claim_ceiling": [
            "quantitative_external_prior_only",
            "congeneric_effects_are_not_P_rex_effects",
            "null_and_large_effect_precedents_both_exist",
            "resource_reallocation_and_experimental_unit_change_the_estimand",
            "do_not_pool_all_congeneric_effects_into_one_expected_effect",
            "whole_plant_seed_production_and_capsule_level_pollen_limitation_can_diverge",
            "no_row_directly_freezes_F0",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit quantitative Pedicularis congener experiments for bounded "
            "use as P0/P1 external priors"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
