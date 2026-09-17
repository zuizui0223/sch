"""Build the fail-closed SCH quantitative compatibility matrix.

The source table contains the four registered same-coordinate conflict designs.
This script does not create missing effects or uncertainty.  It makes the
meta-analytic compatibility gate inspectable by separating: estimand family,
orientation, numeric completeness, uncertainty, covariance handling, and current
poolability.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


STRICT_IDS = (
    "Dalechampia_shared_bract",
    "Silene_petals_sexual_function",
    "Fragaria_inflorescence_density",
    "Gymnadenia_flowering_phenology",
)


def _number(value: str) -> float | None:
    value = value.strip()
    return None if not value else float(value)


def _estimand_family(effect_scale: str) -> str:
    scale = effect_scale.strip()
    if scale.startswith("mean-standardized selection gradient"):
        return "mean-standardized selection gradient"
    if scale.startswith("variance-standardized"):
        return "variance-standardized selection gradient"
    return scale or "UNRESOLVED"


def _numeric_status(row: dict[str, str]) -> str:
    return (
        "EXACT_COMPONENT_COEFFICIENTS"
        if _number(row["component_1_effect"]) is not None
        and _number(row["component_2_effect"]) is not None
        else "NUMERIC_EXTRACTION_PENDING"
    )


def _orientation(row: dict[str, str]) -> str:
    first = _number(row["component_1_effect"])
    second = _number(row["component_2_effect"])
    if first is not None and second is not None:
        if first * second < 0:
            return "OPPOSING_SIGNS_NUMERIC"
        return "NOT_OPPOSING_NUMERIC"
    # Admission to SCH_CONFLICT_COMPONENT_EFFECTS_V1.csv is itself source-adjudicated
    # as a strict same-coordinate conflict candidate.  Pending numerical extraction
    # must not be converted into invented coefficients.
    return "OPPOSING_DIRECTION_SOURCE_ADJUDICATED"


def _uncertainty_status(row: dict[str, str]) -> str:
    raw = row["contrast_uncertainty_status"]
    cluster = row["cluster_id"]
    if cluster == "Dalechampia_shared_bract":
        return "COMPONENT_INTERVALS_AVAILABLE_CONTRAST_VARIANCE_MISSING"
    if cluster == "Silene_petals_sexual_function":
        return "COMPONENT_UNCERTAINTY_MISSING"
    if cluster == "Fragaria_inflorescence_density":
        return "SUPPLEMENT_EXTRACTION_PENDING"
    if cluster == "Gymnadenia_flowering_phenology":
        return "TREATMENT_GROUP_UNCERTAINTY_AVAILABLE_CONTRAST_RECONSTRUCTION_PENDING"
    return raw.upper()


def _covariance_status(row: dict[str, str]) -> str:
    cluster = row["cluster_id"]
    if cluster == "Dalechampia_shared_bract":
        return "NOT_REPORTED"
    if cluster == "Silene_petals_sexual_function":
        return "NOT_AVAILABLE_WITH_CURRENT_COMPONENT_UNCERTAINTY"
    if cluster == "Fragaria_inflorescence_density":
        return "PENDING_TABLE_S2_EXTRACTION"
    if cluster == "Gymnadenia_flowering_phenology":
        return "PENDING_MEDIATED_CONTRAST_RECONSTRUCTION"
    return "UNRESOLVED"


def _pooling_blocker(row: dict[str, str]) -> str:
    cluster = row["cluster_id"]
    if cluster == "Dalechampia_shared_bract":
        return "covariance between component estimates not reported; valid contrast variance unavailable"
    if cluster == "Silene_petals_sexual_function":
        return "component SE or CI not reported in table text; valid contrast variance unavailable"
    if cluster == "Fragaria_inflorescence_density":
        return "exact beta and CI reside in Table S2; numeric extraction and contrast uncertainty pending"
    if cluster == "Gymnadenia_flowering_phenology":
        return "Appendix A treatment-group beta plus SE require mediated-contrast reconstruction with covariance retained"
    return row["contrast_uncertainty_status"].replace("_", " ")


def _has_valid_contrast_variance(row: dict[str, str]) -> bool:
    status = row["contrast_uncertainty_status"].upper()
    return status.startswith("VALID_CONTRAST_VARIANCE")


def _load_rows(source: Path) -> list[dict[str, str]]:
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_id = {row["cluster_id"]: row for row in rows}
    missing = [cluster for cluster in STRICT_IDS if cluster not in by_id]
    if missing:
        raise ValueError(f"registered strict designs missing from source: {missing}")
    return [by_id[cluster] for cluster in STRICT_IDS]


def build_report(source: Path) -> dict[str, object]:
    rows = _load_rows(source)
    designs: list[dict[str, object]] = []
    for row in rows:
        numeric_status = _numeric_status(row)
        valid_variance = _has_valid_contrast_variance(row)
        family = _estimand_family(row["effect_scale"])
        currently_poolable = numeric_status == "EXACT_COMPONENT_COEFFICIENTS" and valid_variance
        designs.append(
            {
                "cluster_id": row["cluster_id"],
                "doi": row["doi"],
                "taxon": row["taxon"],
                "shared_coordinate": row["shared_coordinate"],
                "component_1": row["component_1"],
                "component_1_effect": _number(row["component_1_effect"]),
                "component_2": row["component_2"],
                "component_2_effect": _number(row["component_2_effect"]),
                "within_study_conflict_contrast": _number(row["within_study_conflict_contrast"]),
                "estimand_family": family,
                "orientation": _orientation(row),
                "numeric_status": numeric_status,
                "uncertainty_status": _uncertainty_status(row),
                "covariance_status": _covariance_status(row),
                "valid_contrast_variance": valid_variance,
                "currently_poolable": currently_poolable,
                "pooling_blocker": _pooling_blocker(row),
                "source_basis": row["source_basis"],
                "claim_ceiling": row["claim_ceiling"],
            }
        )

    poolable_by_family = Counter(
        str(row["estimand_family"]) for row in designs if row["currently_poolable"]
    )
    maximum_poolable_family_size = max(poolable_by_family.values(), default=0)
    family_counts = Counter(str(row["estimand_family"]) for row in designs)

    return {
        "analysis": "sch_quantitative_compatibility_matrix_v1",
        "source": str(source),
        "n_registered_designs": len(designs),
        "n_exact_component_numeric_designs": sum(
            row["numeric_status"] == "EXACT_COMPONENT_COEFFICIENTS" for row in designs
        ),
        "n_designs_with_valid_contrast_variance": sum(
            bool(row["valid_contrast_variance"]) for row in designs
        ),
        "n_currently_poolable_designs": sum(bool(row["currently_poolable"]) for row in designs),
        "estimand_family_counts": dict(sorted(family_counts.items())),
        "maximum_poolable_same_estimand_family_size": maximum_poolable_family_size,
        "random_effects_minimum_independent_clusters": 3,
        "random_effects_gate": (
            "PASS" if maximum_poolable_family_size >= 3 else "FAIL_CLOSED"
        ),
        "pooled_conflict_effect": "NOT_ESTIMATED",
        "designs": designs,
        "claim_ceiling": (
            "The matrix diagnoses current compatibility and missing information. "
            "It does not estimate a grand conflict effect, prevalence, or bounded function-specific optima."
        ),
    }


def _fmt(value: object) -> str:
    if value is None:
        return "pending"
    if isinstance(value, float):
        return f"{value:+.4f}"
    return str(value)


def render_markdown(report: dict[str, object]) -> str:
    designs = report["designs"]
    assert isinstance(designs, list)
    lines = [
        "# SCH quantitative compatibility matrix V1",
        "",
        "## Purpose",
        "",
        "This matrix separates **estimand family**, **orientation**, numerical completeness, **uncertainty**, and **covariance** handling for the four registered strict same-coordinate conflict designs. It is a pooling gate, not a meta-analysis.",
        "",
        "```text",
        f"REGISTERED_DESIGNS = {report['n_registered_designs']}",
        f"EXACT_COMPONENT_NUMERIC_DESIGNS = {report['n_exact_component_numeric_designs']}",
        f"VALID_CONTRAST_VARIANCE_DESIGNS = {report['n_designs_with_valid_contrast_variance']}",
        f"CURRENTLY_POOLABLE_DESIGNS = {report['n_currently_poolable_designs']}",
        f"RANDOM_EFFECTS_GATE = {report['random_effects_gate']}",
        "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED",
        "```",
        "",
        "## Compatibility matrix",
        "",
        "| cluster | coordinate | estimand family | orientation | numeric status | uncertainty | covariance | poolable now? | blocker |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in designs:
        assert isinstance(row, dict)
        lines.append(
            "| {cluster_id} | {shared_coordinate} | {estimand_family} | {orientation} | "
            "{numeric_status} | {uncertainty_status} | {covariance_status} | {poolable} | {pooling_blocker} |".format(
                **row,
                poolable="YES" if row["currently_poolable"] else "NO",
            )
        )

    lines += [
        "",
        "## Native within-study numbers, deliberately not pooled",
        "",
        "| cluster | component 1 | estimate | component 2 | estimate | direct within-study contrast | native scale |",
        "|---|---|---:|---|---:|---:|---|",
    ]
    for row in designs:
        assert isinstance(row, dict)
        lines.append(
            f"| {row['cluster_id']} | {row['component_1']} | {_fmt(row['component_1_effect'])} | "
            f"{row['component_2']} | {_fmt(row['component_2_effect'])} | "
            f"{_fmt(row['within_study_conflict_contrast'])} | {row['estimand_family']} |"
        )

    lines += [
        "",
        "## Why the random-effects gate remains closed",
        "",
        "The largest registered estimand family contains three variance-standardized selection-gradient designs, but this is not a three-study meta-analytic stratum: Silene lacks the component uncertainty needed for a valid contrast variance, Fragaria still requires exact Table S2 extraction, and Gymnadenia requires Appendix A mediated-contrast reconstruction with covariance retained. Dalechampia additionally sits on a mean-standardized rather than variance-standardized selection-gradient scale and lacks the covariance needed to propagate the difference of its two component gradients.",
        "",
        "Therefore the current result is **quantitative incompatibility, not quantitative absence**. `RANDOM_EFFECTS_GATE = FAIL_CLOSED` is not evidence that the true cross-system effect is zero. It means the present evidence cannot support a defensible pooled effect without inventing a common scale or missing covariance.",
        "",
        "Promotion requires at least three independent biological clusters with a common estimand family and orientation, exact effect extraction, valid uncertainty for the pooled contrast, and correct within-study covariance handling.",
        "",
        "```text",
        "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED",
        "NATURAL_PREVALENCE = NOT_ESTIMATED",
        "META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED",
        "```",
        "",
        "## Claim ceiling",
        "",
        str(report["claim_ceiling"]),
        "",
    ]
    return "\n".join(lines)


def write_outputs(report: dict[str, object], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/SCH_CONFLICT_COMPONENT_EFFECTS_V1.csv"),
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path("data/SCH_QUANTITATIVE_COMPATIBILITY_READOUT_V1.json"),
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=Path("docs/SCH_QUANTITATIVE_COMPATIBILITY_MATRIX_V1.md"),
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = build_report(args.source)
    write_outputs(report, args.json, args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
