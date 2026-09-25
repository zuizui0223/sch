import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_REGISTRY_V3.csv"
PROTOCOL = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V3.json"
ACTIVE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"
ORIGINAL = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
SOURCE = ROOT / "data" / "SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv"
OUTCOME_READOUT = ROOT / "data" / "SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json"
HOLDOUT_READOUT = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_READOUT_V27.json"
OUTCOME_SCRIPT = ROOT / "scripts" / "analyze_sch_h2_holdout_v27_outcomes.py"
HOLDOUT_SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v3.py"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def _mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_v27_registry_matches_frozen_numeric_adjudication_and_keeps_impatiens_pending():
    registry = {row["programme_id"]: row for row in _rows(REGISTRY)}
    outcome = {
        row["programme_id"]: row
        for row in json.loads(OUTCOME_READOUT.read_text(encoding="utf-8"))["programme_rows"]
    }

    for programme in (
        "Dactylorhiza_lapponica_000649_selection_program",
        "Primula_alpicola_000651_selection_program",
        "Trillium_discolor_000661_selection_program",
    ):
        row = registry[programme]
        assert row["outcome_adjudication_complete"] == "YES"
        assert row["outcome_adjudication_commit"] == "9101a334c420f082506c2f627c5c76a27d6ef1b5"
        assert int(row["n_eligible_repeated_axes"]) == outcome[programme]["n_eligible_repeated_axes"]
        assert int(row["n_bidirectionally_supported_reversal_axes"]) == outcome[programme]["n_bidirectionally_supported_reversal_axes"]

    impatiens = registry["Impatiens_capensis_000723_selection_program"]
    assert impatiens["outcome_adjudication_complete"] == "NO"
    assert impatiens["n_eligible_repeated_axes"] == ""
    assert impatiens["n_bidirectionally_supported_reversal_axes"] == ""
    assert impatiens["outcome_adjudication_commit"] == ""


def test_v27_predictor_classes_remain_the_methods_only_v26_freeze():
    rows = _rows(REGISTRY)
    assert {row["first_qualified_commit"] for row in rows} == {
        "613f65648829b098d8884667ffad3b23b60fcaf4"
    }
    assert {row["classification_frozen_before_outcome"] for row in rows} == {"YES"}
    classes = {row["programme_id"]: row["context_class"] for row in rows}
    assert classes["Dactylorhiza_lapponica_000649_selection_program"] == "SINGLE_REGISTERED_MODIFIER"
    assert classes["Primula_alpicola_000651_selection_program"] == "SINGLE_REGISTERED_MODIFIER"
    assert classes["Trillium_discolor_000661_selection_program"] == "SINGLE_REGISTERED_MODIFIER"
    assert classes["Impatiens_capensis_000723_selection_program"] == "MULTI_COMPONENT_OR_CONSUMER_TURNOVER"


def test_v27_numeric_analyzer_is_reproducible():
    built = _mod(OUTCOME_SCRIPT, "v27_outcome").build(SOURCE)
    frozen = json.loads(OUTCOME_READOUT.read_text(encoding="utf-8"))
    for key in frozen:
        assert built[key] == frozen[key]


def test_v27_current_holdout_state_has_three_complete_single_modifier_programmes_and_closed_gate():
    built = _mod(HOLDOUT_SCRIPT, "v3_holdout").build(PROTOCOL, REGISTRY, ACTIVE, ORIGINAL)
    frozen = json.loads(HOLDOUT_READOUT.read_text(encoding="utf-8"))
    assert built == frozen
    assert built["n_registered_heldout_programmes"] == 4
    assert built["n_complete_primary_programmes"] == 3
    assert built["complete_primary_class_counts"] == {"SINGLE_REGISTERED_MODIFIER": 3}
    assert built["complete_primary_any_supported_reversal_counts"] == {"NO": 2, "YES": 1}
    assert built["primary_test_gate_pass"] is False
    assert built["primary_test"] is None


def test_v27_source_freeze_contains_no_impatiens_numeric_rows():
    assert {row["record_id"] for row in _rows(SOURCE)} == {
        "SCHPRISMA-000649",
        "SCHPRISMA-000651",
        "SCHPRISMA-000661",
    }
