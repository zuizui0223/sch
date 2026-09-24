import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V1.json"
REGISTRY = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_REGISTRY_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v1.py"
V10 = ROOT / "scripts" / "analyze_sch_h2_total_selection_direction_v10.py"

FIELDS = [
    "programme_id",
    "primary_source_id",
    "first_qualified_commit",
    "estimand_family",
    "context_dimensionality_class",
    "classification_basis",
    "classification_frozen_before_outcome",
    "n_repeated_axes",
    "any_bidirectional_supported_reversal",
    "outcome_adjudication_commit",
    "primary_eligible",
    "notes",
]


def _mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _build(registry: Path = REGISTRY):
    return _mod(SCRIPT, "sch_h2_holdout").build(PROTOCOL, registry)


def _write_registry(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def _row(i: int, cls: str, outcome: str) -> dict[str, str]:
    return {
        "programme_id": f"HOLDOUT_PROGRAMME_{i:02d}",
        "primary_source_id": f"SCHPRISMA-H{i:03d}",
        "first_qualified_commit": f"heldout_commit_{i}",
        "estimand_family": "TOTAL_SELECTION_EFFECT",
        "context_dimensionality_class": cls,
        "classification_basis": "source design classified before selection-sign adjudication",
        "classification_frozen_before_outcome": "YES",
        "n_repeated_axes": "1",
        "any_bidirectional_supported_reversal": outcome,
        "outcome_adjudication_commit": f"outcome_commit_{i}",
        "primary_eligible": "YES",
        "notes": "",
    }


def test_current_eight_programmes_are_frozen_as_development_only():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    v10 = _mod(V10, "sch_h2_v10").build(ROOT)
    current = {row["cluster"] for row in v10["axis_rows"]}
    assert current == set(protocol["development_programmes"])
    assert len(current) == 8
    assert protocol["development_result_role"] == "HYPOTHESIS_GENERATION_ONLY"


def test_empty_holdout_registry_keeps_primary_test_closed():
    built = _build()
    assert built["n_registered_heldout_programmes"] == 0
    assert built["n_primary_eligible_resolved_programmes"] == 0
    assert built["primary_test_gate_pass"] is False
    assert built["test_status"] == "PRIMARY_HOLDOUT_TEST_NOT_OPEN"
    assert built == json.loads(READOUT.read_text(encoding="utf-8"))


def test_development_programme_cannot_reenter_holdout(tmp_path):
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    row = _row(1, "SINGLE_REGISTERED_MODIFIER", "NO")
    row["programme_id"] = protocol["development_programmes"][0]
    path = tmp_path / "registry.csv"
    _write_registry(path, [row])
    with pytest.raises(ValueError, match="development programme cannot enter held-out registry"):
        _build(path)


def test_predictor_classification_must_precede_outcome(tmp_path):
    row = _row(1, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES")
    row["classification_frozen_before_outcome"] = "NO"
    path = tmp_path / "registry.csv"
    _write_registry(path, [row])
    with pytest.raises(ValueError, match="context class was not frozen before outcome"):
        _build(path)


def test_registered_gate_prevents_small_holdout_test(tmp_path):
    rows = [
        _row(1, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES"),
        _row(2, "MULTI_COMPONENT_OR_ASSEMBLAGE", "NO"),
        _row(3, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES"),
        _row(4, "SINGLE_REGISTERED_MODIFIER", "NO"),
        _row(5, "SINGLE_REGISTERED_MODIFIER", "NO"),
        _row(6, "SINGLE_REGISTERED_MODIFIER", "YES"),
    ]
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    built = _build(path)
    assert built["n_primary_eligible_resolved_programmes"] == 6
    assert built["primary_test_gate_pass"] is False
    assert built["fisher_two_sided_p"] is None


def test_primary_test_opens_only_after_programme_level_gate(tmp_path):
    rows = [
        _row(1, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES"),
        _row(2, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES"),
        _row(3, "MULTI_COMPONENT_OR_ASSEMBLAGE", "YES"),
        _row(4, "MULTI_COMPONENT_OR_ASSEMBLAGE", "NO"),
        _row(5, "SINGLE_REGISTERED_MODIFIER", "YES"),
        _row(6, "SINGLE_REGISTERED_MODIFIER", "NO"),
        _row(7, "SINGLE_REGISTERED_MODIFIER", "NO"),
        _row(8, "SINGLE_REGISTERED_MODIFIER", "NO"),
    ]
    path = tmp_path / "registry.csv"
    _write_registry(path, rows)
    built = _build(path)

    assert built["primary_test_gate_pass"] is True
    assert built["test_status"] == "PRIMARY_HOLDOUT_TEST_OPEN_AND_RUN"
    assert built["contingency_table"] == {
        "multi_component_yes": 3,
        "multi_component_no": 1,
        "single_modifier_yes": 1,
        "single_modifier_no": 3,
    }
    assert built["odds_ratio"] == 9.0
    assert built["fisher_two_sided_p"] is not None
