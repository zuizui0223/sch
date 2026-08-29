from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "SCH_FICUS_SAME_CODE_EXPERIMENT_PROTOCOL_V1.md"


def test_protocol_preserves_source_specific_receiver_assays() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "8-cm stem, 9-cm arms" in text
    assert "200 mL/min" in text
    assert "5 min" in text
    assert "4-cm diameter, 14-cm lateral arms" in text
    assert "75 mL/min" in text
    assert "40 mm in diameter with 200-mm lateral arms" in text
    assert "10 min" in text


def test_protocol_matches_chemical_coordinate_not_apparatus() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "same chemical coordinate" in text
    assert "not necessarily one universal apparatus" in text
    assert "exact frozen B1-style ratio" in text
    assert "generic four-compound mixture is not the same code" in text


def test_protocol_preserves_fail_closed_nonresponse_boundary() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "nonsignificant NPFW response is not called a private channel" in text
    assert "no-choice rate" in text
    assert "Delayed oviposition does not count as chemical nonresponse" in text
    assert "Until then the Ficus result remains `COMPOSITE_NEAR_L4`" in text
