from __future__ import annotations

import json
from pathlib import Path

from scripts.diagnose_sch_interaction_timing_modelability import (
    DEFAULT_LEDGER,
    build,
    _read,
)


READOUT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "SCH_INTERACTION_TIMING_MODELABILITY_V1.json"
)


def test_current_fixed_role_timing_is_almost_entirely_simultaneous() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_canonical_axes"] == 48
    assert result["n_fixed_role_axes"] == 35
    assert result["fixed_role_timing_counts"] == {
        "SIMULTANEOUS_OR_OVERLAPPING": 34,
        "SPATIAL_CONTEXT": 1,
    }


def test_static_resolved_timing_has_no_sequential_or_temporally_separated_axes() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_static_resolved_fixed_role_axes"] == 19
    assert result["n_static_resolved_fixed_role_clusters"] == 13
    assert result["static_resolved_timing_counts"] == {
        "SIMULTANEOUS_OR_OVERLAPPING": 18,
        "SPATIAL_CONTEXT": 1,
    }
    assert (
        result[
            "n_fixed_role_axes_with_sequential_or_temporally_separated_timing"
        ]
        == 0
    )
    assert (
        result[
            "n_static_axes_with_sequential_or_temporally_separated_timing"
        ]
        == 0
    )


def test_timing_moderator_is_fail_closed_not_posthoc_collapsed() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["timing_moderator_modelable"] is False
    assert result["timing_generalization_supported"] is False
    assert result["status"] == (
        "TIMING_CONTRAST_NOT_MODELABLE_IN_CURRENT_CANONICAL_LEDGER"
    )
    assert result["pedicularis_temporal_window_role"] == (
        "focal_mechanism_hypothesis_not_cross_system_generalization"
    )
    assert "do_not_fit_interaction_timing_as_H1_moderator" in (
        result["claim_ceiling"]
    )


def test_simultaneous_static_geometry_contains_conflict_and_nonconflict() -> None:
    result = build(_read(DEFAULT_LEDGER))
    simultaneous = result["static_geometry_by_timing"][
        "SIMULTANEOUS_OR_OVERLAPPING"
    ]

    assert simultaneous == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 7,
    }


def test_frozen_timing_readout_matches_current_canonical_ledger() -> None:
    expected = json.loads(READOUT.read_text(encoding="utf-8"))
    assert build(_read(DEFAULT_LEDGER)) == expected
