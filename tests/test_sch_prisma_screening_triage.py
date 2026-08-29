from __future__ import annotations

import csv

import scripts.build_sch_prisma_screening_triage as triage


def _batch_row(record_id: str, doi: str, title: str, openalex_id: str) -> dict[str, str]:
    return {
        "record_id": record_id,
        "doi": doi,
        "title": title,
        "year": "2020",
        "venue": "Example Journal",
        "source_databases": "OPENALEX",
        "query_ids": "Q01",
        "openalex_id": openalex_id,
        "crossref_url": "",
        "identification_status": "UNSCREENED",
        "screen_title_abstract": "",
        "screen_title_abstract_reason": "",
        "fulltext_status": "",
        "screen_fulltext": "",
        "screen_fulltext_reason": "",
        "evidence_lanes": "",
        "A_trait": "",
        "A_manipulated": "",
        "pollinator_response_measured": "",
        "antagonist_response_measured": "",
        "common_reproductive_outcome": "",
        "selection_form": "",
        "cue_architecture": "",
        "evolutionary_level": "",
        "causal_strength": "",
        "claim_ceiling": "",
        "study_region": "",
        "country_or_ocean_basin": "",
        "latitude_reported": "",
        "longitude_reported": "",
        "spatial_grain": "",
        "spatial_extent": "",
        "single_site_vs_multisite": "",
        "geographic_contrast": "",
        "receiver_assemblage_contrast": "",
        "biogeographic_context": "",
        "historical_or_phylogenetic_context": "",
        "notes": "",
    }


def _write_batch(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_packet_never_writes_abstract_or_formal_decision(monkeypatch, tmp_path) -> None:
    batch = tmp_path / "SCH_PRISMA_V2_SCREEN_BATCH_01.csv"
    rows = [
        _batch_row(
            "SCHPRISMA-000001",
            "10.1000/example",
            "Floral scent changes pollinator visits",
            "https://openalex.org/W1",
        )
    ]
    _write_batch(batch, rows)

    monkeypatch.setattr(
        triage.v1,
        "_request_json",
        lambda url: {
            "title": "Floral scent changes pollinator visits",
            "type": "article",
            "abstract_inverted_index": {
                "florivores": [0],
                "attack": [1],
                "flowers": [2],
                "pollinators": [3],
            },
        },
    )
    packet, receipt = triage.build_packet(batch)
    assert packet[0]["machine_priority"] == "HIGH_TITLE_PAIR"
    assert packet[0]["formal_title_abstract_decision"] == ""
    assert packet[0]["formal_title_abstract_reason"] == ""
    assert "abstract" not in {key.lower() for key in packet[0]}
    assert receipt["stored_abstracts"] is False
    assert receipt["formal_decisions_written"] is False


def test_known_anchor_is_promoted_only_as_priority_control(monkeypatch, tmp_path) -> None:
    batch = tmp_path / "SCH_PRISMA_V2_SCREEN_BATCH_01.csv"
    rows = [
        _batch_row(
            "SCHPRISMA-000001",
            "10.1890/11-0825.1",
            "Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction",
            "https://openalex.org/W2",
        )
    ]
    _write_batch(batch, rows)
    monkeypatch.setattr(
        triage.v1,
        "_request_json",
        lambda url: {
            "title": rows[0]["title"],
            "type": "article",
            "abstract_inverted_index": {"pollinators": [0], "florivores": [1], "flowers": [2]},
        },
    )
    packet, receipt = triage.build_packet(batch)
    assert packet[0]["known_anchor"] == "YES"
    assert packet[0]["machine_priority"] == "KNOWN_ANCHOR"
    assert packet[0]["formal_title_abstract_decision"] == ""
    assert receipt["known_anchor_count"] == 1


def test_concept_filter_drift_fails_closed(monkeypatch, tmp_path) -> None:
    batch = tmp_path / "SCH_PRISMA_V2_SCREEN_BATCH_01.csv"
    rows = [
        _batch_row(
            "SCHPRISMA-000001",
            "10.1000/example",
            "Floral scent only",
            "https://openalex.org/W3",
        )
    ]
    _write_batch(batch, rows)
    monkeypatch.setattr(
        triage.v1,
        "_request_json",
        lambda url: {
            "title": "Floral scent only",
            "type": "article",
            "abstract_inverted_index": {},
        },
    )
    try:
        triage.build_packet(batch)
    except ValueError as exc:
        assert "concept-filter drift" in str(exc)
    else:
        raise AssertionError("concept-filter drift must fail closed")


def test_openalex_url_accepts_canonical_work_id() -> None:
    assert triage._openalex_api_url("https://openalex.org/W123") == "https://api.openalex.org/works/W123"
