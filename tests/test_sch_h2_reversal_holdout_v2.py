import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V2.json"
REGISTRY = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_REGISTRY_V2.csv"
READOUT = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_READOUT_V2.json"
QUEUE = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v2.py"

FIELDS = [
    "programme_id",
    "primary_source_id",
    "first_qualified_commit",
    "estimand_family",
    "context_class",
    "classification_basis",
    "classification_frozen_before_outcome",
    "n_eligible_repeated_axes",
    "n_bidirectionally_supported_reversal_axes",
    "outcome_adjudication_complete",
    "outcome_adjudication_commit",
    "primary_eligible",
    "notes",
]


def _mod():
    spec = importlib.util.spec_from_file_location("sch_h2_holdout_v2", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _source_ids():
    with QUEUE.open(encoding="utf-8", newline="") as h:
        return [row["record_id"] for row in csv.DictReader(h)]


def _write_registry(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def _row(
    i: int,
    cls: str,
    *,
    n_axes: int = 1,
    n_rev: int = 0,
    complete: bool = True,
) -> dict[str, str]:
    primary = cls in {
        "MULTI_COMPONENT_OR_CONSUMER_TURNOVER",
        "SINGLE_REGISTERED_MODIFIER",
    }
    return {
        "programme_id": f"HOLDOUT_V2_{i:02d}",
        "primary_source_id": _source_ids()[i],
        "first_qualified_commit": f"post_v2_commit_{i}",
        "estimand_family": "TOTAL_SELECTION_EFFECT",
        "context_class": cls,
        "classification_basis": "source design frozen before sign extraction",
        "classification_frozen_before_outcome": "YES",
        "n_eligible_repeated_axes": str(n_axes) if complete else "",
        "n_bidirectionally_supported_reversal_axes": str(n_rev) if complete else "",
        "outcome_adjudication_complete": "YES" if complete else "NO",
        "outcome_adjudication_commit": f"outcome_commit_{i}" if complete else "",
        "primary_eligible": "YES" if primary else "NO",
        "notes": "",
    }


def _build(path: Path = REGISTRY, queue: Path = QUEUE):
    return _mod().build(PROTOCOL, path, queue)


def test_v2_amendment_is_pre_data_and_pins_the_463_record_holdout():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["amendment_timing"] == "BEFORE_FIRST_HELDOUT_PROGRAMME_REGISTRATION"
    assert protocol["v1_registered_heldout_programmes_at_amendment"] == 0
    assert protocol["holdout_source"]["n_records"] == 463
    assert protocol["holdout_source"]["git_blob_sha"] == (
        "1ffd1849b4381a43bb85b2d3473161caabdac510"
    )
    assert protocol["holdout_source"]["v11_outcomes_must_not_reprioritize"] is True


def test_empty_v2_registry_matches_frozen_readout_and_keeps_test_closed():
    built = _build()
    assert built["n_registered_heldout_programmes"] == 0
    assert built["primary_test_gate_pass"] is False
    assert built["test_status"] == "PRIMARY_HOLDOUT_TEST_NOT_OPEN"
    assert built == json.loads(READOUT.read_text(encoding="utf-8"))


def test_v2_rejects_primary_source_outside_frozen_holdout(tmp_path):
    row = _row(0, "SINGLE_REGISTERED_MODIFIER")
    row["primary_source_id"] = "SCHPRISMA-NOT-IN-HOLDOUT"
    path = tmp_path / "registry.csv"
    _write_registry(path, [row])
    with pytest.raises(ValueError, match="outside frozen holdout queue"):
        _build(path)


def test_v2_rejects_modified_holdout_queue_bytes(tmp_path):
    altered = tmp_path / "queue.csv"
    altered.write_bytes(QUEUE.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="blob SHA mismatch"):
        _build(REGISTRY, altered)


def test_v2_spatial_programmes_are_external_replication_not_primary(tmp_path):
    row = _row(
        0,
        "EXTERNAL_SPATIAL_REPLICATION",
        n_axes=4,
        n_rev=2,
    )
    path = tmp_path / "registry.csv"
    _write_registry(path, [row])
    built = _build(path)
    assert built["n_complete_primary_programmes"] == 0
    assert built["n_complete_external_spatial_programmes"] == 1
    assert built["primary_test_gate_pass"] is False


def test_v2_predictor_class_must_be_frozen_before_outcome(tmp_path):
    row = _row(0, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER")
    row["classification_frozen_before_outcome"] = "NO"
    path = tmp_path / "registry.csv"
    _write_registry(path, [row])
    with pytest.raises(ValueError, match="not frozen before outcome"):
        _build(path)


def test_v2_normalizes_axis_count_within_programme(tmp_path):
    rows = [
        _row(0, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=10, n_rev=5),
        _row(1, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=1),
    ]
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    mod = _mod()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["programme_score"]["definition"].startswith(
        "n_bidirectionally_supported_reversal_axes"
    )
    built = mod.build(PROTOCOL, path, QUEUE)
    assert built["complete_primary_any_supported_reversal_counts"] == {"YES": 2}


def test_v2_gate_depends_only_on_design_breadth_and_zero_reversal_is_valid(tmp_path):
    rows = []
    for i in range(5):
        rows.append(
            _row(i, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=0)
        )
    for i in range(5, 10):
        rows.append(
            _row(i, "SINGLE_REGISTERED_MODIFIER", n_axes=3, n_rev=0)
        )
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    built = _build(path)

    assert built["primary_test_gate_pass"] is True
    assert built["test_status"] == "PRIMARY_HOLDOUT_TEST_OPEN_AND_RUN"
    assert built["complete_primary_any_supported_reversal_counts"] == {"NO": 10}
    assert built["primary_test"]["observed_delta"] == 0.0
    assert built["primary_test"]["p_upper"] == 1.0


def test_v2_gate_stays_closed_with_four_programmes_in_either_class(tmp_path):
    rows = []
    for i in range(4):
        rows.append(
            _row(i, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=1, n_rev=0)
        )
    for i in range(4, 9):
        rows.append(
            _row(i, "SINGLE_REGISTERED_MODIFIER", n_axes=1, n_rev=0)
        )
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    built = _build(path)
    assert built["primary_test_gate_pass"] is False
    assert built["primary_test"] is None


def test_v2_directional_permutation_uses_programme_scores(tmp_path):
    rows = [
        _row(0, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=2),
        _row(1, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=2),
        _row(2, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=1),
        _row(3, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=1),
        _row(4, "MULTI_COMPONENT_OR_CONSUMER_TURNOVER", n_axes=2, n_rev=0),
        _row(5, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=0),
        _row(6, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=0),
        _row(7, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=0),
        _row(8, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=0),
        _row(9, "SINGLE_REGISTERED_MODIFIER", n_axes=2, n_rev=0),
    ]
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    built = _build(path)
    assert built["primary_test_gate_pass"] is True
    assert built["primary_test"]["method_used"] == "EXACT_PROGRAMME_LABEL_PERMUTATION"
    assert built["primary_test"]["observed_delta"] > 0
    assert 0 < built["primary_test"]["p_upper"] <= 1
