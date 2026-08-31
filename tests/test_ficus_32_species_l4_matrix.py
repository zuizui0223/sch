from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv"
READOUT = ROOT / "docs" / "SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md"
AUDIT = ROOT / "docs" / "SCH_FICUS_COMPOSITE_HISTORY_BRIDGE_AUDIT_V1.md"


def _rows() -> list[dict[str, str]]:
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _resolved_pollinator_code(row: dict[str, str]) -> bool:
    value = row["private_pollinator_channel"]
    return value in {
        "DIRECT_4_METHYLANISOLE_PRIVATE_CHANNEL",
        "DIRECT_RATIO_SPECIFIC_4_VOC_CODE_NOT_NARROW_PRIVATE_CHANNEL",
    }


def test_fixed_cao_universe_is_complete() -> None:
    rows = _rows()
    assert len(rows) == 32
    assert sum(int(row["cao_sample_n"]) for row in rows) == 242
    assert sum(row["reproductive_system"] == "M" for row in rows) == 15
    assert sum(row["reproductive_system"] == "D" for row in rows) == 17
    assert all(row["phylogenetic_scent_scaffold"] == "YES_32_SPECIES_PHYLOGENY" for row in rows)


def test_two_pollinator_codes_are_resolved_but_narrow_private_label_is_singleton() -> None:
    rows = _rows()
    resolved = [row["species"] for row in rows if _resolved_pollinator_code(row)]
    assert resolved == ["Ficus_carica", "Ficus_semicordata"]
    narrow_private = [
        row["species"]
        for row in rows
        if row["private_pollinator_channel"] == "DIRECT_4_METHYLANISOLE_PRIVATE_CHANNEL"
    ]
    assert narrow_private == ["Ficus_semicordata"]


def test_priority_triangle_separates_code_and_dual_audience_sides() -> None:
    rows = _rows()
    p1 = {row["species"]: row for row in rows if row["priority"].startswith("P1_")}
    assert set(p1) == {"Ficus_carica", "Ficus_semicordata", "Ficus_hispida"}
    assert p1["Ficus_carica"]["priority"] == "P1_RATIO_CODE_HISTORY"
    assert p1["Ficus_semicordata"]["priority"] == "P1_SINGLE_COMPOUND_HISTORY"
    assert p1["Ficus_hispida"]["priority"] == "P1_DUAL_AUDIENCE_HISTORY"
    assert "DIRECT_POLLINATOR_AND_PHILOTRYPESIS_RECEPTIVE_ODOR_RESPONSE" in p1["Ficus_hispida"]["nonpollinator_scent_tracking"]


def test_no_resolved_pollinator_code_has_direct_same_code_npfw_behavior() -> None:
    rows = _rows()
    intersections = [
        row["species"]
        for row in rows
        if _resolved_pollinator_code(row)
        and row["nonpollinator_scent_tracking"].startswith("DIRECT_")
    ]
    assert intersections == []


def test_matrix_remains_fail_closed_for_direct_l4() -> None:
    rows = _rows()
    assert all(row["history_intersection_status"] != "DIRECT_L4" for row in rows)
    readout = READOUT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "previous bottleneck" in readout
    assert "same-code dual-audience intersection" in readout
    assert "resolved pollinator code + direct same-code NPFW behaviour" in readout
    assert "COMPOSITE_NEAR_L4" in audit
    assert "not DIRECT_L4" in audit
    assert "same-code dual-audience cells" in audit
