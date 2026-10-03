from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_predator_method import (
    RECEIPT_SCHEMA,
    REQUIRED_FIELDS,
)


ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "empirical" / "architecture"
V3_TEMPLATE = ARCH / "PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V3.csv"
V4_TEMPLATE = ARCH / "PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv"
V3_CONFIG = ARCH / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V3.json"
V4_CONFIG = ARCH / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V4.json"


def _header(path: Path) -> tuple[str, ...]:
    with path.open(encoding="utf-8", newline="") as handle:
        return tuple(next(csv.reader(handle)))


def test_v3_remains_historical_without_new_barrier_failure_fields() -> None:
    header = _header(V3_TEMPLATE)
    assert "pre_barrier_attack_present" not in header
    assert "barrier_integrity_failure_present" not in header


def test_v4_contains_current_barrier_failure_observations() -> None:
    header = _header(V4_TEMPLATE)
    assert header == REQUIRED_FIELDS
    assert "pre_barrier_attack_present" in header
    assert "barrier_integrity_failure_present" in header
    assert RECEIPT_SCHEMA == "SCH_PEDICULARIS_PREDATOR_METHOD_V4"


def test_v3_and_v4_configs_are_separate_protocol_artifacts() -> None:
    v3 = json.loads(V3_CONFIG.read_text(encoding="utf-8"))
    v4 = json.loads(V4_CONFIG.read_text(encoding="utf-8"))

    assert v3["status"] == (
        "TEMPLATE_ONLY_DO_NOT_RUN_UNTIL_THRESHOLDS_ARE_PROSPECTIVELY_FROZEN"
    )
    assert v4["status"] == (
        "TEMPLATE_ONLY_V4_DO_NOT_RUN_UNTIL_THRESHOLDS_ARE_PROSPECTIVELY_FROZEN"
    )
    v4_method = dict(v4["method_gate"])
    assert v4_method.pop("selected_exclusion_method") == "REQUIRED_BEFORE_USE"
    assert v3["method_gate"] == v4_method
    assert v3["predator_weight"] == v4["predator_weight"]


def test_v4_change_is_observation_and_hard_gate_not_new_f0_threshold() -> None:
    v4 = json.loads(V4_CONFIG.read_text(encoding="utf-8"))
    threshold_basis = set(v4["prospective_freeze"]["threshold_basis"])

    assert "method_gate.pre_barrier_attack_present" not in threshold_basis
    assert "method_gate.barrier_integrity_failure_present" not in threshold_basis
    assert "method_gate.selected_exclusion_method" not in threshold_basis
    assert len(threshold_basis) == 19


def test_selected_method_identity_is_protocol_metadata_not_new_f0_threshold() -> None:
    v4 = json.loads(V4_CONFIG.read_text(encoding="utf-8"))
    assert v4["method_gate"]["selected_exclusion_method"] == "REQUIRED_BEFORE_USE"
    assert "method_gate.selected_exclusion_method" not in set(
        v4["prospective_freeze"]["threshold_basis"]
    )
