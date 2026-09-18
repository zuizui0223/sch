from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"

MACRO_FIELDS = [
    "cluster_id",
    "trait_domain",
    "function_pair_family",
    "antagonist_guild",
    "pollinator_guild",
    "shared_coordinate_status",
    "context_axes_present",
    "conflict_detected",
    "alignment_detected",
    "context_shift_detected",
    "compromise_detected",
    "cancellation_detected",
    "macro_design_eligible",
    "macro_eligibility_reason",
    "coding_status",
    "coding_note",
]

SOURCE_FIELDS = [
    "record_id",
    "doi",
    "title",
    "year",
    "venue",
    "query_ids",
    "evidence_lanes",
    "A_trait",
    "A_manipulated",
    "pollinator_response_measured",
    "antagonist_response_measured",
    "common_reproductive_outcome",
    "selection_form",
    "cue_architecture",
    "study_region",
    "country_or_ocean_basin",
    "latitude_reported",
    "longitude_reported",
    "geographic_contrast",
    "receiver_assemblage_contrast",
    "claim_ceiling",
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _version(path: Path) -> int:
    match = re.search(r"SCREENING_DECISIONS_V(\d+)", path.name)
    if not match:
        raise ValueError(path.name)
    return int(match.group(1))


def _decision_files(prisma_dir: Path) -> list[Path]:
    return sorted(prisma_dir.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"), key=_version)


def _merge_decisions(files: list[Path]) -> dict[str, dict[str, str]]:
    loaded = [_read(path) for path in files]
    fields = {key for rows in loaded for row in rows for key in row}
    merged: dict[str, dict[str, str]] = {}
    for rows in loaded:
        for update in rows:
            row = merged.setdefault(update["record_id"], {key: "" for key in fields})
            for key, value in update.items():
                if value:
                    row[key] = value
    return merged


def build_queue(prisma_dir: Path = PRISMA, frozen_path: Path = FROZEN) -> list[dict[str, str]]:
    candidates = {row["record_id"]: row for row in _read(frozen_path)}
    decisions = _merge_decisions(_decision_files(prisma_dir))
    queue: list[dict[str, str]] = []

    for record_id, decision in sorted(decisions.items()):
        if decision.get("screen_fulltext") != "INCLUDE":
            continue
        source = dict(candidates[record_id])
        source.update({key: value for key, value in decision.items() if value})
        row = {field: source.get(field, "") for field in SOURCE_FIELDS}
        row.update({field: "" for field in MACRO_FIELDS})
        queue.append(row)

    return queue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build_queue()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_FIELDS + MACRO_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
