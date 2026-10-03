from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.materialize_pedicularis_calibration_field_packet import (
    EXPECTED_ORDER,
    OUTPUT_NAMES,
    PACKET_SCHEMA,
    ROOT,
    build_manifest,
    materialize,
)


def _header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def test_field_packet_manifest_covers_registered_five_bundles() -> None:
    manifest = build_manifest("P_REX_TEST", "S1")

    assert manifest["packet_schema_version"] == PACKET_SCHEMA
    assert manifest["n_required_bundles"] == 5
    assert manifest["bundle_order"] == EXPECTED_ORDER
    assert [row["bundle_id"] for row in manifest["bundles"]] == EXPECTED_ORDER
    assert manifest["same_population_and_season_required"] is True
    assert manifest["sample_size_status"] == (
        "NOT_SET_FIELD_PACKET_DOES_NOT_RUN_CAL_C"
    )
    assert manifest["threshold_status"] == (
        "NOT_FROZEN_FIELD_PACKET_PRECEDES_CAL_A_B_C"
    )
    assert manifest["confirmatory_use"] == "PROHIBITED_CALIBRATION_ONLY"


def test_field_packet_preserves_registered_risk_priority_without_turning_it_into_chronology() -> None:
    manifest = build_manifest("P_REX_TEST", "S1")
    by_id = {row["bundle_id"]: row for row in manifest["bundles"]}

    assert by_id["COHORT_REGISTRY"]["risk_priority"] == 0
    assert by_id["G_EXPLORATORY"]["risk_priority"] == 1
    assert by_id["P0_EXPLORATORY"]["risk_priority"] == 2
    assert by_id["CAL_A_REPEATABILITY"]["risk_priority"] == 2
    assert by_id["P1_EXPLORATORY"]["risk_priority"] == 3
    assert "risk_priority_is_not_sample_size_or_chronology" in (
        manifest["claim_ceiling"]
    )


def test_materialized_packet_is_byte_identical_to_registered_templates(tmp_path: Path) -> None:
    output = tmp_path / "field_packet"
    manifest = materialize(output, "P_REX_TEST", "S1")

    assert (output / "packet_manifest.json").exists()
    saved = json.loads(
        (output / "packet_manifest.json").read_text(encoding="utf-8")
    )
    assert saved == manifest

    for bundle in manifest["bundles"]:
        source = ROOT / bundle["source_template_path"]
        destination = output / bundle["output_filename"]
        assert destination.exists()
        assert destination.read_bytes() == source.read_bytes()
        assert _header(destination) == bundle["header"]


def test_materialized_packet_contains_only_five_blank_csvs_and_manifest(tmp_path: Path) -> None:
    output = tmp_path / "field_packet"
    manifest = materialize(output, "P_REX_TEST", "S1")

    expected = {"packet_manifest.json", *OUTPUT_NAMES.values()}
    assert {path.name for path in output.iterdir()} == expected

    for name in OUTPUT_NAMES.values():
        path = output / name
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        assert len(rows) == 1

    assert manifest["current_blocker"] == (
        "COLLECT_NONCONFIRMATORY_CALIBRATION_DATA"
    )
    assert manifest["next_machine_step_after_collection"] == (
        "build_pedicularis_calibration_package.py"
    )


def test_packet_refuses_to_overwrite_existing_field_data(tmp_path: Path) -> None:
    output = tmp_path / "field_packet"
    output.mkdir()
    (output / "g_exploratory.csv").write_text(
        "existing field data\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="never overwritten"):
        materialize(output, "P_REX_TEST", "S1")


def test_packet_requires_explicit_population_and_season() -> None:
    with pytest.raises(ValueError, match="population_id"):
        build_manifest("", "S1")
    with pytest.raises(ValueError, match="season_id"):
        build_manifest("P_REX_TEST", "")
