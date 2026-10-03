from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
YIELD_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CALIBRATION_COLLECTION_YIELD_V1.csv"
)

PACKET_SCHEMA = "SCH_PEDICULARIS_CALIBRATION_FIELD_PACKET_V1"

OUTPUT_NAMES = {
    "COHORT_REGISTRY": "cohort_registry.csv",
    "G_EXPLORATORY": "g_exploratory.csv",
    "P0_EXPLORATORY": "p0_exploratory.csv",
    "CAL_A_REPEATABILITY": "cal_a_repeatability.csv",
    "P1_EXPLORATORY": "p1_exploratory.csv",
}

EXPECTED_ORDER = [
    "COHORT_REGISTRY",
    "G_EXPLORATORY",
    "P0_EXPLORATORY",
    "CAL_A_REPEATABILITY",
    "P1_EXPLORATORY",
]


def _read_yield(path: Path = YIELD_LEDGER) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("calibration collection-yield ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if [row["bundle_id"] for row in rows] != EXPECTED_ORDER:
        raise ValueError(
            "field-packet bundle order drifted from registered collection-yield ledger"
        )
    return rows


def _template_path(row: dict[str, str]) -> Path:
    path = ROOT / row["template_path"]
    if not path.exists():
        raise ValueError(
            f"registered field template does not exist: {row['template_path']}"
        )
    return path


def _header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"field template is empty: {path}") from exc
        data_rows = list(reader)
    if not header:
        raise ValueError(f"field template has blank header: {path}")
    if data_rows:
        raise ValueError(
            f"field template must be header-only before packet materialization: {path}"
        )
    return header


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(
    population_id: str,
    season_id: str,
    *,
    yield_path: Path = YIELD_LEDGER,
) -> dict:
    if not population_id.strip():
        raise ValueError("population_id must be non-empty")
    if not season_id.strip():
        raise ValueError("season_id must be non-empty")

    rows = _read_yield(yield_path)
    bundles = []
    for row in rows:
        bundle_id = row["bundle_id"]
        source = _template_path(row)
        bundles.append(
            {
                "bundle_id": bundle_id,
                "cohort_role": row["cohort_role"],
                "source_template_path": row["template_path"],
                "source_template_sha256": _sha256(source),
                "output_filename": OUTPUT_NAMES[bundle_id],
                "header": _header(source),
                "structural_risk": row["structural_risk"],
                "risk_priority": int(row["risk_priority"]),
                "execution_mode": row["execution_mode"],
                "allowed_flower_overlap": row["allowed_flower_overlap"],
            }
        )

    return {
        "packet_schema_version": PACKET_SCHEMA,
        "population_id": population_id,
        "season_id": season_id,
        "n_required_bundles": len(bundles),
        "bundle_order": EXPECTED_ORDER,
        "bundles": bundles,
        "same_population_and_season_required": True,
        "sample_size_status": "NOT_SET_FIELD_PACKET_DOES_NOT_RUN_CAL_C",
        "threshold_status": "NOT_FROZEN_FIELD_PACKET_PRECEDES_CAL_A_B_C",
        "confirmatory_use": "PROHIBITED_CALIBRATION_ONLY",
        "current_blocker": "COLLECT_NONCONFIRMATORY_CALIBRATION_DATA",
        "next_machine_step_after_collection": (
            "build_pedicularis_calibration_package.py"
        ),
        "claim_ceiling": [
            "field_packet_is_template_provenance_only",
            "risk_priority_is_not_sample_size_or_chronology",
            "no_threshold_or_F0_value_is_created",
            "calibration_rows_must_not_be_reused_as_confirmatory_rows",
        ],
    }


def materialize(
    output_dir: Path,
    population_id: str,
    season_id: str,
    *,
    yield_path: Path = YIELD_LEDGER,
) -> dict:
    if output_dir.exists():
        existing = list(output_dir.iterdir()) if output_dir.is_dir() else [output_dir]
        if existing:
            raise ValueError(
                "field packet output path must be absent or an empty directory; "
                "existing field data are never overwritten"
            )
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(
        population_id,
        season_id,
        yield_path=yield_path,
    )

    for bundle in manifest["bundles"]:
        source = ROOT / bundle["source_template_path"]
        destination = output_dir / bundle["output_filename"]
        if destination.exists():
            raise ValueError(f"refusing to overwrite {destination}")
        shutil.copyfile(source, destination)
        if _sha256(destination) != bundle["source_template_sha256"]:
            raise ValueError(
                f"materialized template checksum mismatch: {destination}"
            )

    manifest_path = output_dir / "packet_manifest.json"
    if manifest_path.exists():
        raise ValueError(f"refusing to overwrite {manifest_path}")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize the registered Pedicularis calibration field packet "
            "without selecting thresholds or sample sizes"
        )
    )
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--population-id", required=True)
    parser.add_argument("--season-id", required=True)
    parser.add_argument("--yield-ledger", type=Path, default=YIELD_LEDGER)
    args = parser.parse_args()

    manifest = materialize(
        args.output_dir,
        args.population_id,
        args.season_id,
        yield_path=args.yield_ledger,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
