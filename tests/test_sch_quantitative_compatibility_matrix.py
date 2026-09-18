from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_sch_quantitative_compatibility_matrix.py"
SOURCE = ROOT / "data" / "SCH_CONFLICT_COMPONENT_EFFECTS_V1.csv"
MATRIX = ROOT / "docs" / "SCH_QUANTITATIVE_COMPATIBILITY_MATRIX_V1.md"
READOUT = ROOT / "data" / "SCH_QUANTITATIVE_COMPATIBILITY_READOUT_V1.json"
AUDIT = ROOT / "docs" / "QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1.md"
RECOVERY = ROOT / "data" / "SCH_PENDING_NUMERIC_SOURCE_RECOVERY_V1.json"
RECOVERY_DOC = ROOT / "docs" / "SCH_PENDING_NUMERIC_SOURCE_RECOVERY_V1.md"


def _load_module():
    assert SCRIPT.exists(), "quantitative compatibility matrix builder is missing"
    spec = importlib.util.spec_from_file_location("sch_quant_compatibility", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_builder_recovers_the_four_registered_strict_conflict_designs() -> None:
    module = _load_module()
    report = module.build_report(SOURCE)

    assert report["n_registered_designs"] == 4
    assert report["n_exact_component_numeric_designs"] == 2
    assert report["n_designs_with_valid_contrast_variance"] == 0
    assert report["n_currently_poolable_designs"] == 0
    assert report["random_effects_gate"] == "FAIL_CLOSED"

    ids = {row["cluster_id"] for row in report["designs"]}
    assert ids == {
        "Dalechampia_shared_bract",
        "Silene_petals_sexual_function",
        "Fragaria_inflorescence_density",
        "Gymnadenia_flowering_phenology",
    }


def test_matrix_makes_each_pooling_blocker_explicit() -> None:
    module = _load_module()
    report = module.build_report(SOURCE)
    by_id = {row["cluster_id"]: row for row in report["designs"]}

    assert by_id["Dalechampia_shared_bract"]["numeric_status"] == "EXACT_COMPONENT_COEFFICIENTS"
    assert "covariance" in by_id["Dalechampia_shared_bract"]["pooling_blocker"].lower()

    assert by_id["Silene_petals_sexual_function"]["numeric_status"] == "EXACT_COMPONENT_COEFFICIENTS"
    assert "se" in by_id["Silene_petals_sexual_function"]["pooling_blocker"].lower()

    assert by_id["Fragaria_inflorescence_density"]["numeric_status"] == "NUMERIC_EXTRACTION_PENDING"
    assert "table s2" in by_id["Fragaria_inflorescence_density"]["pooling_blocker"].lower()

    assert by_id["Gymnadenia_flowering_phenology"]["numeric_status"] == "NUMERIC_EXTRACTION_PENDING"
    assert "appendix" in by_id["Gymnadenia_flowering_phenology"]["pooling_blocker"].lower()


def test_rendered_matrix_and_readout_freeze_fail_closed_pooling_gate() -> None:
    assert MATRIX.exists(), "compatibility matrix markdown is missing"
    assert READOUT.exists(), "compatibility matrix readout is missing"
    text = MATRIX.read_text(encoding="utf-8")
    for token in (
        "Dalechampia_shared_bract",
        "Silene_petals_sexual_function",
        "Fragaria_inflorescence_density",
        "Gymnadenia_flowering_phenology",
        "estimand family",
        "orientation",
        "uncertainty",
        "covariance",
        "CURRENTLY_POOLABLE_DESIGNS = 0",
        "RANDOM_EFFECTS_GATE = FAIL_CLOSED",
        "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED",
        "not evidence that the true cross-system effect is zero",
    ):
        assert token in text


def test_results_discussion_audit_reports_the_inspectable_pooling_state() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    for token in (
        "four strong same-coordinate designs",
        "two have exact component coefficients",
        "zero have a valid contrast variance",
        "zero are currently poolable",
        "SCH_QUANTITATIVE_COMPATIBILITY_MATRIX_V1.md",
        "POOLED_CONFLICT_EFFECT = NOT_ESTIMATED",
    ):
        assert token in text


def test_pending_numeric_sources_are_located_but_not_guessed() -> None:
    assert RECOVERY.exists(), "pending numeric source recovery manifest is missing"
    assert RECOVERY_DOC.exists(), "pending numeric source recovery receipt is missing"
    report = json.loads(RECOVERY.read_text(encoding="utf-8"))
    assert report["n_pending_clusters"] == 2
    assert report["n_source_locations_confirmed"] == 2
    assert report["n_exact_numeric_extractions_completed"] == 0
    assert report["status"] == "SOURCE_ROUTE_RESOLVED_EXTRACTION_FAIL_CLOSED"
    assert report["n_download_routes_resolved"] == 1
    assert report["n_binary_materializations_completed"] == 0

    by_id = {row["cluster_id"]: row for row in report["sources"]}
    fragaria = by_id["Fragaria_inflorescence_density"]
    assert fragaria["source_object"] == "Table S2"
    assert fragaria["source_file"] == "evl3262-sup-0001-suppmat.docx"
    assert fragaria["published_analysis"] == "emtrends differences in beta"
    assert fragaria["download_route_status"] == "SIGNED_OUP_CDN_ROUTE_RESOLVED"
    assert fragaria["resolved_download_object"] == "evl3262-sup-0001-suppmat.docx"
    assert fragaria["numeric_promotion"] == "BLOCKED_UNTIL_SOURCE_TABLE_BYTES_ARE_INSPECTED"

    gym = by_id["Gymnadenia_flowering_phenology"]
    assert gym["source_object"] == "Appendix A Table A2"
    assert gym["archive_id"] == "E096-022-A1"
    assert gym["archive_route_status"] == "ECOLOGICAL_ARCHIVES_OBJECT_RESOLVED"
    assert gym["reported_content"] == "phenotypic linear selection gradients (beta +/- SE) for all four treatment groups"
    assert gym["numeric_promotion"] == "BLOCKED_UNTIL_SOURCE_TABLE_BYTES_ARE_INSPECTED"

    text = RECOVERY_DOC.read_text(encoding="utf-8")
    for token in (
        "SOURCE_ROUTE_RESOLVED_EXTRACTION_FAIL_CLOSED",
        "SIGNED_OUP_CDN_ROUTE_RESOLVED",
        "ECOLOGICAL_ARCHIVES_OBJECT_RESOLVED",
        "do not digitize Figure 1 as if it were Table S2",
        "do not infer missing covariance",
        "Fragaria_inflorescence_density",
        "Gymnadenia_flowering_phenology",
        "NUMERIC_EXTRACTION_PENDING",
        "RANDOM_EFFECTS_GATE = FAIL_CLOSED",
    ):
        assert token in text
