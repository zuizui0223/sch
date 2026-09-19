import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH1_V1.csv"
CASES = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH1_READOUT_V1.json"
TEMPLATE = ROOT / "data" / "SCH_MACROECOLOGY_CONTEXT_CASE_TEMPLATE_V1.csv"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_evidence_batch1.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_context_batch1", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(EVIDENCE, CASES)


def test_h2_context_batch1_separates_evidence_from_model_cases():
    built = _build()
    assert built["n_context_evidence_rows"] == 6
    assert built["n_canonical_axes_with_evidence"] == 5
    assert built["n_source_records"] == 5
    assert built["n_local_context_cases_materialized"] == 1
    assert built["n_context_evidence_rows_not_yet_model_cases"] == 5
    assert built["h2_model_ready"] is False


def test_h2_context_batch1_fails_closed_on_pending_sources():
    built = _build()
    assert built["local_case_resolution_counts"] == {
        "CONTEXT_STRUCTURE_RESOLVED_LOCAL_OUTCOMES_PENDING": 2,
        "LOCAL_CONTEXT_GEOMETRY_RESOLVED": 1,
        "LOCAL_CONTEXT_SOURCE_EXTRACTION_REQUIRED": 1,
        "LOCAL_CONTEXT_TABLE_REQUIRED": 2,
    }
    assert built["n_evidence_rows_requiring_source_object"] == 5
    assert "reported_context_count_is_not_model_case_count" in built["claim_ceiling"]


def test_only_gentiana_focal_context_is_materialized_in_batch1():
    built = _build()
    assert built["materialized_case_ids"] == ["Gentiana_lutea_color_Torrestio"]
    assert built["materialized_canonical_axes"] == ["Gentiana_lutea_color_axis"]


def test_context_case_template_has_canonical_axis_key():
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        fields = set(csv.DictReader(handle).fieldnames or ())
    assert "canonical_trait_axis_id" in fields
    assert "trait_axis_id" in fields


def test_h2_context_batch1_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))
