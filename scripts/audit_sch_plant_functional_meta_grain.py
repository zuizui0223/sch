"""Adjudicate unduplicated plant functional-trait meta source grain BEFORE models.

Original archived source: Caruso, Maherali & Martin, 2020,
doi:10.1086/706199; Dryad doi:10.5061/dryad.sn02v6x0q,
Zenodo 5000217 checksum-verified original files.
The 572-row experimental master and 815-row observational file are
SEPARATE. The original duplicated 1014-row analytic table is NOT an
additional experiment or source population.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path

ORIGINAL_DOI="10.5061/dryad.sn02v6x0q"
SOURCE_MASTER="Plant_functional_traits_experimental_database_master_Dryad.xlsx"
SOURCE_OBS="Plant_functional_traits_observational_database_Dryad.xlsx"
SOURCE_DUP="Plant_functional_traits_experimental_database_duplicated_Dryad.xlsx"
REQUIRED_SCHEMA=(
"row.id","authors","Paper ID","pub.year","journal","vol.page",
"species","within.study.id","generic.year","generic.spp",
"generic.population","generic.trait","generic.sex",
"generic.fitness.measure","generic.treatment","trait.name","trait.class",
"fitness.measure.defined","fitness.component","agent.selection.defined",
"treatment.defined","experimental.context","grad.linear.value",
"grad.linear.se","diff.linear.value","diff.linear.sterr",
)
ID_FIELDS=(
    "Paper ID","generic.year","generic.spp","generic.population",
    "generic.trait","generic.sex","generic.fitness.measure",
)
CONTEXT_FIELDS=("agent.selection.defined","treatment.defined",
                "experimental.context")
MISSING={"","NA","na","N/A","n/a","."}


def source_rows(path:Path):
    import openpyxl
    book=openpyxl.load_workbook(path,read_only=True,data_only=True)
    sheet=book["Database"]
    data=list(sheet.values)
    book.close()
    headers=tuple(str(v).strip() if v is not None else "" for v in data[0])
    if path.name==SOURCE_MASTER and headers!=REQUIRED_SCHEMA:
        raise ValueError("original unduplicated selection master schema drift")
    if len(headers)!=len(set(headers)):
        raise ValueError("duplicate original meta field names")
    return [dict(zip(headers,row)) for row in data[1:]],headers


def valid(value)->bool:
    return value is not None and str(value).strip() not in MISSING


def number(value)->float|None:
    if not valid(value):return None
    try: x=float(value)
    except (ValueError,TypeError):return None
    return x if math.isfinite(x) else None


def strkey(value)->str:
    return str(value).strip() if value is not None else ""


def _counts(rows:list[dict],field:str)->list[dict]:
    c=collections.Counter(strkey(x.get(field,"")) for x in rows)
    return [{"label":k,"n_rows":v}
            for k,v in sorted(c.items(),key=lambda x:(-x[1],x[0]))]


def summarize(rows:list[dict],keyfields:tuple[str,...])->dict:
    groups=collections.defaultdict(list)
    for row in rows:
        key=tuple(strkey(row.get(k)) for k in keyfields)
        groups[key].append(row)
    sizes=collections.Counter(len(x) for x in groups.values())
    validpairs=0
    validtriples=0
    pairs_by_agent=collections.Counter()
    for key,xx in groups.items():
        treatments=collections.Counter(strkey(x.get("generic.treatment")) for x in xx)
        if len(xx)==2 and len(treatments)==2:
            validpairs+=1
            agent=strkey(xx[0].get("agent.selection.defined"))
            pairs_by_agent[agent]+=1
        if len(xx)==3 and len(treatments)==3:validtriples+=1
    return {
        "grouping_columns":keyfields,
        "n_groups":len(groups),
        "group_size_distribution":dict(sorted(sizes.items())),
        "n_groups_exact_two_distinct_treatments":validpairs,
        "n_groups_exact_three_distinct_treatments":validtriples,
        "pair_by_agent":dict(pairs_by_agent.most_common()),
        "sample_first_ten_multirow_group_keys":[
           {"key":dict(zip(keyfields,k)),
            "n":len(xx),
            "treatment_codes":[strkey(x.get("generic.treatment")) for x in xx],
            "gradients":[strkey(x.get("grad.linear.value")) for x in xx],
            "SEs":[strkey(x.get("grad.linear.se")) for x in xx],
           } for k,xx in list(groups.items()) if len(xx)>=2
        ][:10],
    }


def original_column_dictionary(path:Path)->list[dict[str,str]]:
    import openpyxl
    book=openpyxl.load_workbook(path,read_only=True,data_only=True)
    table=book["Sheet1"]
    out=[]
    for row in table.values:
        if row[0] is None: continue
        out.append({"column":str(row[0]).strip(),
                    "source_definition":str(row[1]) if len(row)>1 and row[1] is not None else ""})
    book.close()
    return out


def profile_source(root:Path)->dict:
    master,mheaders=source_rows(root/SOURCE_MASTER)
    observational,oheaders=source_rows(root/SOURCE_OBS)
    duplicated,dheaders=source_rows(root/SOURCE_DUP)
    if len(master)!=572 or len(observational)!=815 or len(duplicated)!=1014:
        raise ValueError("original source workbook denominators not retained")
    if len({strkey(x["row.id"]) for x in master})!=572:
        raise ValueError("unduplicated original source has nonunique row ID")
    x=[]
    for row in master:
        b=number(row["grad.linear.value"])
        s=number(row["grad.linear.se"])
        if b is not None and s is not None and s<=0:
            raise ValueError("invalid source original SE")
        x.append({"beta":b,"se":s,"row":row})
    matched_grad=sum(i["beta"] is not None and i["se"] is not None for i in x)
    groups_simple=summarize(master,ID_FIELDS)
    groups_tighter=summarize(master,ID_FIELDS+CONTEXT_FIELDS)
    trends={
        "n_original_experimental_master_rows":len(master),
        "n_original_author_duplicated_analysis_rows":len(duplicated),
        "n_original_observational_rows":len(observational),
        "n_source_meta_unique_Paper_ID":len({strkey(r["Paper ID"]) for r in master}),
        "n_unique_named_species_in_experimental_master":len({strkey(r["species"]) for r in master}),
        "n_original_rows_with_numeric_gradient_and_SE":matched_grad,
        "n_original_rows_with_numeric_selection_differential_and_SE":
            sum(number(r["diff.linear.value"]) is not None and
                number(r["diff.linear.sterr"]) is not None for r in master),
        "source_master_column_dictionary":original_column_dictionary(root/SOURCE_MASTER),
        "column_names_experimental_master":mheaders,
        "column_names_observational":oheaders,
        "column_names_original_duplicated":dheaders,
        "metadata_fields":{
            f:_counts(master,f) for f in (
                "Paper ID","pub.year","trait.class",
                "fitness.component","agent.selection.defined",
                "treatment.defined","experimental.context",
                "generic.treatment"
            )
        },
        "candidate_pairing_by_paper_year_species_population_trait_sex_fitness":
            groups_simple,
        "candidate_pairing_with_full_original_agent_treatment_context":
            groups_tighter,
        "status":"ARCHIVE_MASTER_GRAIN_PROFILE_ONLY_NOT_YET_A_META_TEST",
        "source_DOI":ORIGINAL_DOI,
        "observational_and_experimental_data_not_pooled":True,
        "source_original_duplicate_analysis_records_excluded":True,
    }
    return trends


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    report=profile_source(a.outdir)
    value=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(value,encoding="utf-8")
    print("BEGIN_SCH_ORIGINAL_FUNCTIONAL_META_GRAIN")
    print(value)
    print("END_SCH_ORIGINAL_FUNCTIONAL_META_GRAIN")


if __name__=="__main__":
    main()
