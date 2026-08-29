from __future__ import annotations

import scripts.harvest_sch_prisma_candidates_v2 as v2


def test_reconstruct_abstract_preserves_position_order() -> None:
    inverted = {
        "pollinators": [3],
        "Floral": [0],
        "attract": [2],
        "traits": [1],
        "herbivores": [4],
    }
    assert v2.reconstruct_abstract(inverted) == "Floral traits attract pollinators herbivores"


def test_concept_filter_requires_all_three_blocks() -> None:
    assert v2.passes_concept_filter(
        "Floral scent mediates pollinator and herbivore responses", ""
    )
    assert v2.passes_concept_filter(
        "A plant interaction study",
        "Flower visitors pollinate flowers while seed predators consume developing seeds.",
    )
    assert not v2.passes_concept_filter("Floral scent and pollinator attraction", "")
    assert not v2.passes_concept_filter("Herbivore responses and floral scent", "")
    assert not v2.passes_concept_filter("Pollinator and herbivore interactions", "")


def test_fig_nonpollinating_query_terms_are_recognized() -> None:
    flags = v2.concept_flags(
        "Fig scent and pollinating wasps",
        "Non-pollinating fig wasps exploit the same host.",
    )
    assert flags == {"floral_signal": True, "pollinator": True, "antagonist": True}


def test_harvest_deduplicates_passes_and_preserves_query_ids(monkeypatch) -> None:
    def fake_fetch(query: str, *, cap: int):
        candidate = v2.v1.Candidate(
            doi="10.1000/shared",
            title="Floral traits, pollinators and herbivores",
            year="2020",
            source_databases={"OPENALEX"},
        )
        return [candidate], {
            "reported_total_results": 1,
            "retrieved_records": 1,
            "concept_pass_hits": 1,
            "concept_filter_fail_hits": 0,
            "truncated_at_registered_cap": False,
        }

    monkeypatch.setattr(v2, "fetch_openalex_v2", fake_fetch)
    candidates, receipt = v2.harvest(cap=2500)
    assert len(candidates) == 1
    assert len(candidates[0].query_ids) == len(v2.v1.QUERY_REGISTRY)
    assert receipt["systematic_completion_status"] == "PRISMA_V2_IDENTIFICATION_COMPLETE"
    assert receipt["deduplicated_unscreened_candidates"] == 1
    assert receipt["stored_abstracts"] is False
    assert receipt["crossref_discovery"] is False


def test_any_cap_hit_blocks_v2_completion(monkeypatch) -> None:
    calls = {"n": 0}

    def fake_fetch(query: str, *, cap: int):
        calls["n"] += 1
        candidate = v2.v1.Candidate(
            doi=f"10.1000/{calls['n']}",
            title="Floral traits, pollinators and herbivores",
            year="2020",
            source_databases={"OPENALEX"},
        )
        truncated = calls["n"] == 1
        return [candidate], {
            "reported_total_results": cap + 1 if truncated else 1,
            "retrieved_records": cap if truncated else 1,
            "concept_pass_hits": 1,
            "concept_filter_fail_hits": (cap - 1) if truncated else 0,
            "truncated_at_registered_cap": truncated,
        }

    monkeypatch.setattr(v2, "fetch_openalex_v2", fake_fetch)
    _, receipt = v2.harvest(cap=2500)
    assert receipt["any_truncated_query"] is True
    assert receipt["systematic_completion_status"] == "PRISMA_V2_IDENTIFICATION_TRUNCATED"
