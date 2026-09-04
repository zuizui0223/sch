from __future__ import annotations

import scripts.harvest_sch_prisma_candidates as base
import scripts.harvest_sch_prisma_ci as ci


def _candidate(doi: str = "10.1000/test") -> base.Candidate:
    return base.Candidate(doi=doi, title="Floral conflict", year="2024")


def test_missing_openalex_key_yields_blocked_receipt_not_false_completion(monkeypatch) -> None:
    def fake_crossref(query: str, *, cap: int):
        return [_candidate()], 1

    monkeypatch.setattr(base, "fetch_crossref", fake_crossref)
    candidates, receipt = ci.harvest_ci(cap=1, openalex_api_key="")

    assert len(candidates) == 1
    assert receipt["systematic_completion_status"] == "PRISMA_IDENTIFICATION_BLOCKED_EXTERNAL_SOURCE"
    assert receipt["registered_source_retrieval_complete"] is False
    assert len(receipt["external_source_failures"]) == len(base.QUERY_REGISTRY)
    assert all(item["error_code"] == "OPENALEX_API_KEY_NOT_CONFIGURED" for item in receipt["external_source_failures"])
    assert any(row["database"] == "CROSSREF" and row["retrieval_status"] == "OK" for row in receipt["query_results"])


def test_keyed_openalex_and_crossref_can_complete_wrapper(monkeypatch) -> None:
    def fake_openalex(query: str, *, cap: int, api_key: str):
        assert api_key == "test-key"
        return [_candidate("10.1000/openalex")], 1

    def fake_crossref(query: str, *, cap: int):
        return [_candidate("10.1000/crossref")], 1

    monkeypatch.setattr(ci, "fetch_openalex_with_key", fake_openalex)
    monkeypatch.setattr(base, "fetch_crossref", fake_crossref)
    candidates, receipt = ci.harvest_ci(cap=2, openalex_api_key="test-key")

    assert len(candidates) == 2
    assert receipt["external_source_failures"] == []
    assert receipt["registered_source_retrieval_complete"] is True
    assert receipt["systematic_completion_status"] == "PRISMA_IDENTIFICATION_ONLY"


def test_openalex_failure_with_key_is_recorded_without_secret_or_false_completion(monkeypatch) -> None:
    def fake_openalex(query: str, *, cap: int, api_key: str):
        raise ci.SourceUnavailable("OPENALEX_RETRIEVAL_FAILED")

    def fake_crossref(query: str, *, cap: int):
        return [_candidate()], 1

    monkeypatch.setattr(ci, "fetch_openalex_with_key", fake_openalex)
    monkeypatch.setattr(base, "fetch_crossref", fake_crossref)
    _, receipt = ci.harvest_ci(cap=1, openalex_api_key="super-secret")

    text = str(receipt)
    assert "super-secret" not in text
    assert receipt["systematic_completion_status"] == "PRISMA_IDENTIFICATION_BLOCKED_EXTERNAL_SOURCE"
    assert all(item["error_code"] == "OPENALEX_RETRIEVAL_FAILED" for item in receipt["external_source_failures"])
