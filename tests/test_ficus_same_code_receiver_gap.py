from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_SAME_CODE_RECEIVER_GAP_V1.csv"
READOUT = ROOT / "docs" / "SCH_FICUS_SAME_CODE_RECEIVER_GAP_READOUT_V1.md"
MATRIX_READOUT = ROOT / "docs" / "SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md"
POWER = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_SAME_CODE_ASSAY_POWER_V1.json"


def _rows() -> dict[str, dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return {row["species"]: row for row in csv.DictReader(handle)}


def test_same_code_frontier_is_the_three_declared_ficus_systems() -> None:
    rows = _rows()
    assert set(rows) == {"Ficus_semicordata", "Ficus_carica", "Ficus_hispida"}
    assert rows["Ficus_semicordata"]["pollinator_code_status"] == "RESOLVED_DIRECT_BEHAVIORAL"
    assert rows["Ficus_carica"]["pollinator_code_status"] == "RESOLVED_DIRECT_BEHAVIORAL"
    assert rows["Ficus_hispida"]["pollinator_code_status"] == "KEY_SYNTHETIC_CODE_UNRESOLVED"


def test_semicordata_temporal_separation_is_positive_but_not_same_code_behavior() -> None:
    row = _rows()["Ficus_semicordata"]
    assert row["pollinator_code"] == "SINGLE_COMPOUND_4_METHYLANISOLE"
    assert row["nonpollinator_temporal_evidence"].startswith("DIRECT_DELAYED_OVIPOSITION")
    assert "10_DAYS" in row["nonpollinator_temporal_evidence"]
    assert "14_TO_32_DAYS" in row["nonpollinator_temporal_evidence"]
    assert row["nonpollinator_same_code_behavior"] == "NOT_TESTED_ON_4_METHYLANISOLE"
    assert row["same_code_intersection_status"] == "NO_SAME_CODE_BEHAVIOR"
    assert "YanPengYang2012" in row["source_basis"]


def test_carica_and_hispida_close_complementary_cells_only() -> None:
    rows = _rows()
    carica = rows["Ficus_carica"]
    hispida = rows["Ficus_hispida"]
    assert carica["pollinator_code"] == "RATIO_SPECIFIC_4_VOC_BLEND"
    assert "Philotrypesis_caricae" in carica["nonpollinator_taxa_evidence"]
    assert carica["nonpollinator_same_code_behavior"] == "NOT_TESTED_ON_VALIDATED_4_VOC_RATIO"
    assert hispida["nonpollinator_same_code_behavior"] == "DIRECT_TO_WHOLE_RECEPTIVE_ODOR_BUT_KEY_CODE_UNRESOLVED"
    assert hispida["same_code_intersection_status"] == "NOT_EVALUABLE_SAME_CODE_UNTIL_CODE_RESOLVED"


def test_same_code_intersection_and_direct_l4_remain_fail_closed() -> None:
    rows = _rows()
    assert not any(row["same_code_intersection_status"] == "DIRECT_SAME_CODE_BEHAVIOR" for row in rows.values())
    text = READOUT.read_text(encoding="utf-8")
    matrix_text = MATRIX_READOUT.read_text(encoding="utf-8")
    assert "resolved pollinator code + direct NPFW behaviour to that same code = 0 species" in text
    assert "Temporal separation and chemical privatization" in text
    assert "FICUS_SAME_CODE_RECEIVER_GAP_V1.csv" in matrix_text
    assert "temporal separation" in matrix_text.lower()
    assert "DIRECT_L4" in text
    assert "NOT_EVALUABLE" in text


def test_same_code_gap_has_distinct_power_for_interception_and_privacy() -> None:
    data = json.loads(POWER.read_text(encoding="utf-8"))
    eq = {row["target_power"]: row for row in data["equivalence_rows"]}
    attraction = {
        (row["true_choice_probability"], row["target_power"]): row
        for row in data["attraction_rows"]
    }
    assert eq[0.8]["decisive_choices"] == 206
    assert eq[0.9]["decisive_choices"] == 260
    assert attraction[(0.65, 0.8)]["decisive_choices"] == 82
    assert attraction[(0.70, 0.8)]["decisive_choices"] == 43
    assert eq[0.8]["decisive_choices"] > attraction[(0.65, 0.8)]["decisive_choices"]
    text = READOUT.read_text(encoding="utf-8")
    assert "failure to detect attraction at those sample sizes does **not** support a private-channel state" in text
    assert "prospectively powered missing intersection" in text
