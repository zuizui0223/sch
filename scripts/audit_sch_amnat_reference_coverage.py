"""Reference identity and citation-coverage audit for the SCH Major Article.

This deliberately does NOT claim that ten verified focal items constitute a
complete 16-cluster literature bibliography. Primary sources must be
publisher/PubMed-checked before being added to verified metadata CSV.

Run:
  python scripts/audit_sch_amnat_reference_coverage.py
  python scripts/audit_sch_amnat_reference_coverage.py --output /tmp/receipt.json

The full Markdown manuscript may contain reference text and code examples,
so cite matching is done separately in the prose and the Literature Cited
section. DOI uniqueness is checked by normalization, not string occurrence
count. This is source-identity and completeness auditing, not an assessment
of scientific findings or editorial formatting acceptance.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"
VERIFIED=ROOT/"data/SCH_AMNAT_CORE_BIBLIOGRAPHY_VERIFIED_20261028.csv"
SOURCE_NOTE=ROOT/"manuscript/AMNAT_CORE_REFERENCES_VERIFIED_20261028.md"
LEDGER=ROOT/"data/SCH_PATTERN_LEDGER_V1.csv"

DOI_RE=re.compile(r"10\.\d{4,9}/[a-zA-Z0-9._;()/:-]+")
PRIMARY_DOIS={
    "10.1093/aob/mcw097",
    "10.1093/aobpla/plv019",
    "10.1098/rsbl.2013.0387",
    "10.1890/14-0119.1",
    "10.1111/j.1469-8137.2010.03296.x",
    "10.1038/s41598-017-13340-0",
    "10.1002/ajb2.16101",
    "10.1093/aob/mcx026",
    "10.1007/s10682-016-9878-8",
}
CORRECTION_DOI="10.1038/s41598-019-43381-6"


def read_csv(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as fh:
        return list(csv.DictReader(fh))


def doi_set(text:str)->set[str]:
    return {m.group(0).rstrip(".,);").lower() for m in DOI_RE.finditer(text)}


def visible(text:str)->str:
    """Normalize Markdown bibliography typography without changing metadata."""
    return " ".join(text.replace("*","").replace("–","-").split()).casefold()


def build(paper:str,metadata:list[dict[str,str]],
          patterns:list[dict[str,str]],note:str)->dict:
    if paper.count("## Literature Cited\n")!=1:
        raise ValueError("unique core Literature Cited section required")
    body,bib=paper.split("## Literature Cited\n",1)
    if re.search(r"^##\s+",bib,re.MULTILINE):
        raise ValueError("unexpected later section after bibliography")
    if len(metadata)!=10 or len({r["doi"].lower() for r in metadata})!=10:
        raise ValueError("ten source-verified independent DOI identities required")
    if len(patterns)!=16 or len({r["cluster_id"] for r in patterns})!=16:
        raise ValueError("original 16 biological-cluster design must remain unchanged")
    expected=PRIMARY_DOIS|{CORRECTION_DOI}
    if {r["doi"].lower() for r in metadata}!=expected:
        raise ValueError("reference metadata DOI set was unexpectedly changed")
    if doi_set(body)!=expected or doi_set(bib)!=expected:
        raise ValueError("all verified DOI source items must occur both in text and bibliography")
    if "## Core Literature Cited\n" not in note or "\n## Corrections, identity" not in note:
        raise ValueError("verified note core reference section missing")
    note_core=note.split("## Core Literature Cited\n",1)[1].split(
        "\n## Corrections, identity",1)[0]
    # Publisher link URLs can themselves contain a DOI followed by a
    # page-path suffix (e.g. /200213). Only the actual reference list
    # represents bibliographic DOI identities, not that lookup URL.
    if doi_set(note_core)!=expected:
        raise ValueError("independent core source-verification citations disagree")

    # Every paragraph is one bibliography item; require both identity and
    # key journal-year-volume-locator metadata, avoiding title guesses.
    biblio_lines=[x.strip() for x in bib.strip().split("\n") if x.strip()]
    if len(biblio_lines)!=len(metadata):
        raise ValueError("bibliography entry count does not match verified records")
    checked={}
    for line in biblio_lines:
        found=doi_set(line)
        if len(found)!=1:
            raise ValueError("one and only one DOI expected per bibliography entry")
        doi=next(iter(found))
        if doi in checked:
            raise ValueError("duplicate core bibliography DOI")
        record=next((r for r in metadata if r["doi"].lower()==doi),None)
        if record is None:
            raise ValueError("unknown bibliography DOI")
        before_doi=line.split("https://doi.org/",1)[0]
        displayed=visible(before_doi)
        required=(
            record["first_author"],record["issue_year"],record["journal"],
            record["volume"],record["locator"],record["article_title"],
        )
        for token in required:
            if visible(token) not in displayed:
                raise ValueError(f"bibliography DOI {doi} has unverified or missing {token}")
        if not displayed.startswith(record["first_author"].casefold()+","):
            raise ValueError("first author of citation must match publisher metadata")
        if not re.search(r"\.\s+"+re.escape(record["issue_year"])+r"\.\s+",before_doi):
            raise ValueError("publisher issue year missing from citation identity")
        checked[doi]=record
    if set(checked)!=expected:
        raise ValueError("some bibliography entries are missing")

    if (
        "Koski 2023" not in body
        or re.search(r"Koski 2022",body)
        or "Chen, Zhang and Li 2019" not in body
        or "Table 3 notation" not in body
        or "Sletvold, Grindeland and Ågren 2010" not in body
    ):
        raise ValueError("original author-year or correction citation missing")
    if checked[CORRECTION_DOI]["reference_role"]!="CORRECTION":
        raise ValueError("2019 Primula correction improperly categorized")
    if len([r for r in metadata if r["reference_role"]=="PRIMARY"])!=9:
        raise ValueError("original-source denominator changed")
    if not all(r["verification_url"].startswith("https://") for r in metadata):
        raise ValueError("publisher/PubMed verification URLs are missing")

    # A manuscript can make unsupported or uncited literature claims even
    # when every explicit DOI has a corresponding bibliography entry.
    # This check reports that *coverage* issue, not absent ecological results.
    missing=[]
    explicit=doi_set(body)
    for row in patterns:
        from_ledger=doi_set(row["source_id"])
        if not from_ledger or not from_ledger.issubset(explicit):
            missing.append({
                "cluster_id":row["cluster_id"],
                "plant_taxon":row["plant_taxon"],
                "source_doi_in_existing_cluster_id":sorted(from_ledger),
                "missing_source_doi_in_manuscript_prose":sorted(from_ledger-explicit),
                "needs_source_verified_author_year_bibliography":True,
            })
    named_omissions=(
        "Satyrium","Silene","Dalechampia","Fragaria",
        "16 independent biological clusters",
    )
    if not all(x in body for x in named_omissions):
        raise ValueError("16-cluster paper science coverage changed")
    if len(missing)<1:
        raise ValueError("unexpectedly declare complete conceptual bibliography")
    words_paper=len(body.split())
    words_total=len(paper.split())
    return {
        "analysis":"sch_amnat_20261028_primary_core_reference_audit_v1",
        "n_verified_source_records":len(metadata),
        "n_original_experiment_references":9,
        "n_linked_author_correction_references":1,
        "n_unique_prose_dois":len(explicit),
        "n_unique_bibliography_dois":len(doi_set(bib)),
        "complete_prose_doi_to_core_bibliography_match":True,
        "known_issue_year_exception":{
            "doi":"10.1002/ajb2.16101","publisher_issue_citation_year":2023,
            "online_first_year":2022,"field_years":[2020,2021],
        },
        "primula_2019_correction_does_not_change_used_table2_linear_beta":True,
        "body_before_references_whitespace_words":words_paper,
        "whole_manuscript_including_references_whitespace_words":words_total,
        "original_pattern_clusters":len(patterns),
        "clusters_not_explicitly_doi_supported_in_prose":missing,
        "n_such_clusters":len(missing),
        "all_16_cluster_references_completed":False,
        "external_herbivory_meta_analysis_citations_verified":False,
        "submission_ready":False,
        "blocking_next_action":(
            "verify and cite sources for missing conceptual pattern clusters,"
            " named external meta-analyses, and author-year references"
        ),
        "status":"CORE_10_REFS_VERIFIED_CONCEPTUAL_SYNTHESIS_REFERENCE_COMPLETENESS_OPEN",
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--paper",type=Path,default=PAPER)
    p.add_argument("--verified",type=Path,default=VERIFIED)
    p.add_argument("--patterns",type=Path,default=LEDGER)
    p.add_argument("--source-note",type=Path,default=SOURCE_NOTE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    report=build(a.paper.read_text(encoding="utf-8"),
                 read_csv(a.verified),read_csv(a.patterns),
                 a.source_note.read_text(encoding="utf-8"))
    result=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result,encoding="utf-8")
    else:
        print(result,end="")


if __name__=="__main__":
    main()
