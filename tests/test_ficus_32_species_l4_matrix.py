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


def test_fixed_cao_universe_is_complete() -> None:
    rows = _rows()
    assert len(rows) == 32
    assert sum(int(row["cao_sample_n"]) for row in rows) == 242
    assert sum(row["reproductive_system"] == "M" for row in rows) == 15
    assert sum(row["reproductive_system"] == "D" for row in rows) == 17
    assert all(row["phylogenetic_scent_scaffold"] == "YES_32_SPECIES_PHYLOGENY" for row in rows)


def test_direct_private_channel_is_currently_a_singleton() -> None:
    rows = _rows()
    private = [row for row in rows if row["private_pollinator_channel"].startswith("DIRECT_")]
    assert [row["species"] for row in private] == ["Ficus_semicordata"]
    assert private[0]["private_pollinator_channel"] == "DIRECT_4_METHYLANISOLE_PRIVATE_CHANNEL"


def test_priority_pair_separates_private_and_shared_history_sides() -> None:
    rows = _rows()
    p1 = {row["species"]: row for row in rows if row["priority"].startswith("P1_")}
    assert set(p1) == {"Ficus_semicordata", "Ficus_hispida"}
    assert p1["Ficus_semicordata"]["priority"] == "P1_PRIVATE_HISTORY"
    assert p1["Ficus_hispida"]["priority"] == "P1_SHARED_HISTORY"
    assert "DIRECT_POLLINATOR_AND_PHILOTRYPESIS_RECEPTIVE_ODOR_RESPONSE" in p1["Ficus_hispida"]["nonpollinator_scent_tracking"]


def test_matrix_remains_fail_closed_for_direct_l4() -> None:
    rows = _rows()
    assert all(row["history_intersection_status"] != "DIRECT_L4" for row in rows)
    readout = READOUT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "second independently supported private-channel tip is a necessary but not sufficient gate" in readout
    assert "replicated shared-to-private transition test cannot yet be performed" in readout
    assert "COMPOSITE_NEAR_L4" in audit
    assert "not DIRECT_L4" in audit
    assert "fixed-universe evidence expansion" in audit
