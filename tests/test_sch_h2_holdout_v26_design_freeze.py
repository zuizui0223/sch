import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "SCH_H2_HOLDOUT_V26_METHODS_ONLY_DESIGN_FREEZE.csv"
PROTOCOL = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V3.json"
REGISTRY = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_REGISTRY_V3.csv"
ACTIVE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"
ORIGINAL = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
V25 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V25_TA0_HOLDOUT.csv"
READOUT = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_READOUT_V26.json"
SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v3.py"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def _mod():
    spec = importlib.util.spec_from_file_location("sch_h2_holdout_v3", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_v26_freezes_four_methods_only_classes_without_outcome_signs():
    rows = _rows(DESIGN)
    assert len(rows) == 4
    assert Counter(row["context_class"] for row in rows) == {
        "SINGLE_REGISTERED_MODIFIER": 3,
        "MULTI_COMPONENT_OR_CONSUMER_TURNOVER": 1,
    }
    assert {row["classification_evidence_scope"] for row in rows} == {"METHODS_ONLY"}
    assert {row["outcome_sign_or_significance_used_for_classification"] for row in rows} == {"NO"}
    assert {row["repeated_total_selection_context_signal"] for row in rows} == {"YES"}


def test_v26_design_sources_are_v25_retained_and_v3_active():
    design_ids = {row["record_id"] for row in _rows(DESIGN)}
    v25 = {row["record_id"]: row for row in _rows(V25)}
    active = {row["record_id"] for row in _rows(ACTIVE)}
    assert design_ids == {
        "SCHPRISMA-000649",
        "SCHPRISMA-000651",
        "SCHPRISMA-000661",
        "SCHPRISMA-000723",
    }
    assert design_ids <= active
    assert all(v25[record_id]["screen_title_abstract"] == "RETAIN_FULLTEXT" for record_id in design_ids)


def test_v26_registry_uses_design_freeze_commit_and_keeps_outcomes_blank():
    rows = _rows(REGISTRY)
    assert len(rows) == 4
    assert {row["first_qualified_commit"] for row in rows} == {
        "613f65648829b098d8884667ffad3b23b60fcaf4"
    }
    assert {row["estimand_family"] for row in rows} == {"TOTAL_SELECTION_EFFECT"}
    assert {row["classification_frozen_before_outcome"] for row in rows} == {"YES"}
    assert {row["outcome_adjudication_complete"] for row in rows} == {"NO"}
    assert all(row["n_eligible_repeated_axes"] == "" for row in rows)
    assert all(row["n_bidirectionally_supported_reversal_axes"] == "" for row in rows)
    assert all(row["outcome_adjudication_commit"] == "" for row in rows)
    assert {row["primary_eligible"] for row in rows} == {"YES"}


def test_v26_holdout_evaluator_registers_programmes_but_keeps_gate_closed():
    result = _mod().build(PROTOCOL, REGISTRY, ACTIVE, ORIGINAL)
    assert result["n_registered_heldout_programmes"] == 4
    assert result["n_complete_primary_programmes"] == 0
    assert result["complete_primary_class_counts"] == {}
    assert result["primary_test_gate_pass"] is False
    assert result["primary_test"] is None
    assert result["test_status"] == "PRIMARY_HOLDOUT_TEST_NOT_OPEN"
    assert result == json.loads(READOUT.read_text(encoding="utf-8"))
