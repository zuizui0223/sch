from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "empirical" / "prisma" / "SCH_JBI_GEOGRAPHY_ANCHOR_PREVIEW_V1.csv"
READOUT = ROOT / "docs" / "SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md"


def _rows() -> list[dict[str, str]]:
    with CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_anchor_geography_preview_is_eight_studies_and_fail_closed() -> None:
    rows = _rows()
    assert len(rows) == 8
    assert len({row["record_id"] for row in rows}) == 8
    assert len({row["doi"] for row in rows}) == 8
    assert all(row["claim_boundary"] for row in rows)


def test_only_knauer_is_current_direct_biogeographic_candidate() -> None:
    rows = _rows()
    direct = [row for row in rows if row["direct_biogeographic_synthesis_candidate"] == "YES"]
    assert len(direct) == 1
    assert direct[0]["study"] == "Knauer_Bakhtiari_Schiestl_2018"
    assert direct[0]["doi"] == "10.1038/s41467-018-03792-x"
    assert "PRESENT_VS_ABSENT" in direct[0]["geography_preview"]
    assert "INTERACTOR_REGIME_CONTRAST" in direct[0]["receiver_assemblage_or_interactor_contrast_preview"]


def test_locations_and_experimental_settings_are_not_promoted_to_geography() -> None:
    rows = {row["study"]: row for row in _rows()}
    assert rows["Perez_Barrales_2013"]["direct_biogeographic_synthesis_candidate"] == "NO"
    assert rows["Kessler_et_al_2015"]["direct_biogeographic_synthesis_candidate"] == "NO"
    assert "SINGLE_MEXICAN_POPULATION" in rows["Perez_Barrales_2013"]["geography_preview"]
    assert "EXPERIMENTAL_TENTS" in rows["Kessler_et_al_2015"]["geography_preview"]


def test_readout_keeps_jbi_gate_unresolved_and_fallback_live() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "UNRESOLVED / EMPIRICALLY_SPARSE_IN_ANCHOR_SPINE" in text
    assert "Do **not** conclude from `1/8`" in text
    assert "Ecology and Evolution" in text
    assert "A map of study locations cannot rescue a failed geography gate" in text
