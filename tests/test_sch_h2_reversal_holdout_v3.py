import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V3.json"
REGISTRY = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_REGISTRY_V3.csv"
ACTIVE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"
ORIGINAL = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_READOUT_V3.json"
SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v3.py"

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
    spec = importlib.util.spec_from_file_location("sch_h2_holdout_v3", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _build(registry: Path = REGISTRY):
    return _mod().build(PROTOCOL, registry, ACTIVE, ORIGINAL)


def _ids(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as h:
        return [row["record_id"] for row in csv.DictReader(h)]


def test_v3_is_pre_screen_amendment_with_zero_registered_programmes():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["amendment_of"] == "SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V2"
    assert protocol["v2_registered_heldout_programmes_at_amendment"] == 0
    assert protocol["amendment_timing"] == (
        "BEFORE_FIRST_HELDOUT_PROGRAMME_REGISTRATION_AND_BEFORE_V25_SCREENING"
    )


def test_v3_active_roster_is_exactly_463_minus_the_seven_pre_screened_records():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    original = _ids(ORIGINAL)
    active = _ids(ACTIVE)
    excluded = protocol["holdout_source"]["pre_v3_formally_screened_record_ids"]
    assert len(original) == 463
    assert len(active) == 456
    assert len(excluded) == 7
    assert active == [record_id for record_id in original if record_id not in set(excluded)]
    assert set(excluded) == {
        "SCHPRISMA-000434",
        "SCHPRISMA-000550",
        "SCHPRISMA-000648",
        "SCHPRISMA-000659",
        "SCHPRISMA-000673",
        "SCHPRISMA-000775",
        "SCHPRISMA-000812",
    }


def test_v3_frozen_readout_preserves_the_pre_registration_state():
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    assert frozen["n_registered_heldout_programmes"] == 0
    assert frozen["n_complete_primary_programmes"] == 0
    assert frozen["primary_test_gate_pass"] is False
    assert frozen["source_derivation"] == {
        "original_queue_n": 463,
        "pre_v3_formally_screened_n": 7,
        "active_holdout_n": 456,
        "review_order_preserved": True,
    }


def test_v3_rejects_a_pre_screened_source_even_if_it_was_in_the_old_463_queue(tmp_path):
    row = {
        "programme_id": "BAD_PRE_V3",
        "primary_source_id": "SCHPRISMA-000648",
        "first_qualified_commit": "future_commit",
        "estimand_family": "TOTAL_SELECTION_EFFECT",
        "context_class": "SINGLE_REGISTERED_MODIFIER",
        "classification_basis": "source design",
        "classification_frozen_before_outcome": "YES",
        "n_eligible_repeated_axes": "",
        "n_bidirectionally_supported_reversal_axes": "",
        "outcome_adjudication_complete": "NO",
        "outcome_adjudication_commit": "",
        "primary_eligible": "YES",
        "notes": "",
    }
    path = tmp_path / "registry.csv"
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=FIELDS)
        w.writeheader()
        w.writerow(row)
    with pytest.raises(ValueError, match="outside frozen holdout queue"):
        _build(path)


def test_v3_source_derivation_is_blob_and_order_guarded(tmp_path):
    altered = tmp_path / "active.csv"
    altered.write_bytes(ACTIVE.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="active 456-record holdout roster blob SHA mismatch"):
        _mod().validate_source_derivation(PROTOCOL, altered, ORIGINAL)
