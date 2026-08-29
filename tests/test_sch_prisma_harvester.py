from __future__ import annotations

import csv

import scripts.harvest_sch_prisma_candidates as prisma


def test_registered_query_set_is_fixed_and_does_not_require_shared_cue_phrase() -> None:
    assert len(prisma.QUERY_REGISTRY) == 14
    assert prisma.QUERY_REGISTRY[0] == ("Q01", '"floral scent" pollinator herbivore')
    assert prisma.QUERY_REGISTRY[-1] == ("Q14", 'fig scent pollinator "non-pollinating wasp"')
    assert not any("shared cue" in query.lower() for _, query in prisma.QUERY_REGISTRY)


def test_normalization_prefers_doi_then_title_year() -> None:
    a = prisma.Candidate(
        doi="https://doi.org/10.1000/ABC",
        title="Floral scent & pollinators!",
        year="2020",
    )
    a.doi = prisma.normalize_doi(a.doi)
    assert a.doi == "10.1000/abc"
    assert prisma.dedup_key(a) == "doi:10.1000/abc"

    b = prisma.Candidate(doi="", title="Floral scent & pollinators!", year="2020")
    assert prisma.dedup_key(b) == "titleyear:floral scent pollinators|2020"


def test_merge_preserves_multi_database_multi_query_provenance() -> None:
    a = prisma.Candidate(
        doi="10.1000/test",
        title="A title",
        year="2020",
        openalex_id="OA1",
        source_databases={"OPENALEX"},
        query_ids={"Q01"},
    )
    b = prisma.Candidate(
        doi="10.1000/test",
        title="A title",
        year="2020",
        crossref_url="https://doi.org/10.1000/test",
        source_databases={"CROSSREF"},
        query_ids={"Q02"},
    )
    merged = prisma.merge_candidate(a, b)
    assert merged.source_databases == {"OPENALEX", "CROSSREF"}
    assert merged.query_ids == {"Q01", "Q02"}
    assert merged.openalex_id == "OA1"
    assert merged.crossref_url.endswith("10.1000/test")


def test_harvest_marks_truncation_and_never_calls_it_complete(monkeypatch) -> None:
    def fake_openalex(query: str, *, cap: int):
        return (
            [prisma.Candidate(doi="10.1000/a", title="A", year="2020")],
            cap + 10,
        )

    def fake_crossref(query: str, *, cap: int):
        return (
            [prisma.Candidate(doi="10.1000/a", title="A", year="2020")],
            1,
        )

    monkeypatch.setattr(prisma, "fetch_openalex", fake_openalex)
    monkeypatch.setattr(prisma, "fetch_crossref", fake_crossref)
    candidates, receipt = prisma.harvest(cap=1)
    assert len(candidates) == 1
    assert receipt["any_truncated_query"] is True
    assert receipt["systematic_completion_status"] == "PRISMA_IDENTIFICATION_TRUNCATED"
    assert receipt["deduplicated_records"] == 1
    assert candidates[0].source_databases == {"OPENALEX", "CROSSREF"}
    assert len(candidates[0].query_ids) == 14


def test_candidate_csv_is_unscreened_and_contains_no_abstract_field(tmp_path) -> None:
    candidate = prisma.Candidate(
        doi="10.1000/a",
        title="Floral trait conflict",
        year="2021",
        venue="Example Journal",
        source_databases={"OPENALEX"},
        query_ids={"Q01"},
    )
    out = tmp_path / "candidates.csv"
    prisma.write_candidates(out, [candidate])
    with out.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["record_id"] == "SCHPRISMA-000001"
    assert rows[0]["identification_status"] == "UNSCREENED"
    assert rows[0]["screen_title_abstract"] == ""
    assert "abstract" not in {name.lower() for name in rows[0]}
    assert "study_region" in rows[0]
    assert "receiver_assemblage_contrast" in rows[0]
