"""SHA/MD5-pinned flower-level blueberry experiment source ingress (no modeling).

Kendall et al. 2020, Journal of Applied Ecology,
article DOI:10.1111/1365-2664.13751.
Original archived dataset on Zenodo record 3987488 (CC0), original Dryad
dataset DOI:10.5061/dryad.tmpg4f4wj.
Three file names and MD5 digests were independently verified against
the live original Zenodo landing-page file manifest (2026-11-17).

Original sample unit for the target is the *tagged flower*, NOT visit
number or the individual plant. The same flower may be followed to
fruit set. A new source-specific analysis cannot begin until exact
column schemas, missingness, duplicate tag identities and documented
flower-level risk-set alignment pass this audit.

No invented data, no arbitrary CSV file substitution.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

ZENODO_RECORD_ID=3987488
ARTICLE_DOI="10.1111/1365-2664.13751"
DATA_DOI="10.5061/dryad.tmpg4f4wj"
BASE="https://zenodo.org/records/3987488/files"
EXPECTED={
 "fruit_set_multiple_visits_experiments_JAPPL-2020-00197.csv":
      "5617777fcef1c46bb4e0bab5ccc22ce6",
 "fruit_set_pollination_experiments_JAPPL-2020-00197.csv":
      "e630cd466935e7709e874ff6706f7ce0",
 "fruit_set_single_visit_experiments_JAPPL-2020-00197.csv":
      "d7ed02c7aa254a963043539c06c99ed7",
}
MAX_BYTES=1_000_000
UA="SCH-verifiable-original-blueberry-flower-gate/1.0"


def get(url):
    req=Request(url,headers={"User-Agent":UA,"Accept":"text/csv,*/*"})
    with urlopen(req,timeout=35) as r:
        b=r.read(MAX_BYTES+1)
        info={"requested_url":url,"http":r.status,
              "final_url":r.geturl(),"content_type":r.headers.get("Content-Type",""),
              "bytes":len(b)}
    if not b or len(b)>MAX_BYTES:
        raise ValueError("Original source file empty/oversized")
    if b[:100].lstrip().lower().startswith((b"<!doctype",b"<html",b"<?xml")):
        raise ValueError("HTML or XML is not a source CSV")
    return b,info


def parse_original(data):
    try:
        s=data.decode("utf-8-sig")
        encoding="utf-8-sig"
    except UnicodeDecodeError:
        s=data.decode("latin-1")
        encoding="latin-1"
    dialect=csv.Sniffer().sniff(s[:min(8192,len(s))],delimiters=",;\t")
    rdr=csv.DictReader(io.StringIO(s),dialect=dialect)
    names=rdr.fieldnames
    if not names or len(set(names))!=len(names) or len(names)<7:
        raise ValueError("Original source CSV has invalid/unrecognized columns")
    records=list(rdr)
    if len(records)<20 or len(records)>150_000:
        raise ValueError("Original source CSV source row count implausible")
    if any(None in r for r in records):
        raise ValueError("Source original CSV row has extra parsed columns")
    return records,names,encoding


def field(names,candidates):
    normalized={n.lower().strip():n for n in names}
    for c in candidates:
        if c.lower().strip() in normalized:
            return normalized[c.lower().strip()]
    return None


def source_schema(rows,names):
    tag=field(names,("Tag","Tag_id","flower_id","flowerID"))
    species=field(names,("Species","blueberry_type","type"))
    plant=field(names,("RP","plant_id","plant.number","Plant.number","Plant","Plant.ID"))
    fruit=field(names,("FS","fruit_set","fruitset","Fruit_set"))
    visits=field(names,("Sumvisits","visits","N_visits"))
    year=field(names,("Year",))
    block=field(names,("Block",))
    visitor=field(names,("SPEC.COM","SPEC_COM","visitor","pollinator"))
    treat=field(names,("Treatment","pollination","pollination_treatment"))
    if not (species and fruit and tag):
        raise ValueError("Original tagged-flower source species/fruit/tag absent")
    if visits and any(r[visits].strip() not in ("","NA","NaN","na")
                      and not (r[visits].strip().isdigit() or
                               r[visits].strip().replace(".","",1).isdigit())
                      for r in rows):
        raise ValueError("Original visits column contains nonnumeric unqualified counts")
    vals=Counter(r[fruit].strip() for r in rows)
    if not set(vals).issubset({"0","1","","NA","NaN","na"}):
        raise ValueError("Original fruit outcome is not 0/1/missing")
    species_n=Counter(r[species].strip() for r in rows)
    vars=[species,tag,plant,year,block]
    composite=[x for x in vars if x is not None]
    label_counts=Counter(tuple(r[x].strip() for x in composite) for r in rows)
    duplicates={str(k):v for k,v in label_counts.items() if v>1}
    visitor_count=Counter(r[visitor].strip() for r in rows) if visitor else {}
    visits_count=Counter(r[visits].strip() for r in rows) if visits else {}
    treat_count=Counter(r[treat].strip() for r in rows) if treat else {}
    return {
       "n_original_rows":len(rows),
       "n_original_columns":len(names),
       "original_column_names":names,
       "qualified_column_roles":{
          "tagged_flower_id":tag,"plant_id":plant,"species":species,
          "binary_fruit_set":fruit,"visit_count":visits,"visitor_taxon":visitor,
          "year":year,"block":block,"treatment":treat,
       },
       "n_nonmissing_original_fruit_outcomes":int(vals["0"]+vals["1"]),
       "n_original_fruit_positive":int(vals["1"]),
       "n_original_fruit_zero":int(vals["0"]),
       "original_species_counts":dict(species_n),
       "original_visitor_counts":dict(visitor_count),
       "original_treatment_counts":dict(treat_count),
       "original_flower_visitation_count_distribution":dict(visits_count),
       "composite_flower_identity_fields":composite,
       "n_composite_flower_identity_unique":len(label_counts),
       "n_composite_flower_identity_ambiguous_duplicate_keys":len(duplicates),
       "examples_ambiguous_composite_flower_IDs":dict(list(duplicates.items())[:20]),
       "flower_level_risk_set_verified_unique":len(duplicates)==0,
       "same_flower_reproductive_transition_with_pollen_deposition_observed":False,
       "pollen_deposition_grain_count_observed":False,
       "not_plant_level_independent_paper_sample":True,
    }


def run(outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    results=[]
    for filename,expected in EXPECTED.items():
        url=f"{BASE}/{filename}?download=1"
        try:
            b,info=get(url)
        except (HTTPError,URLError,TimeoutError,ValueError) as e:
            raise RuntimeError(
                f"Genuine Zenodo source file access blocked for {filename}: "
                f"{type(e).__name__}: {str(e)[:200]}") from e
        observed=hashlib.md5(b).hexdigest()
        if observed!=expected:
            raise ValueError(f"Original source MD5 drift for {filename}: {observed}")
        rows,names,encoding=parse_original(b)
        schema=source_schema(rows,names)
        out=outdir/filename
        out.write_bytes(b)
        results.append({
            "zenodo_record_id":ZENODO_RECORD_ID,"article_DOI":ARTICLE_DOI,
            "data_DOI":DATA_DOI,"original_filename":filename,
            "original_MD5":observed,"original_SHA256":hashlib.sha256(b).hexdigest(),
            "original_source_bytes":len(b),"source_data_encoding":encoding,
            "original_source_url":url,"fetch_provenance":info,
            "source_schema":schema,
        })
    if len(results)!=3:
        raise ValueError("Three original source files required")
    result={
        "status":"THREE_GENUINE_ZENODO_FLOWER_LEVEL_DATASETS_VERIFIED_SCHEMA_ONLY",
        "n_original_source_files":len(results),"source_files":results,
        "n_original_independent_published_programmes":1,
        "raw_plant_or_flower_regression_fitted":False,
        "original_data_new_ecological_statistics_estimated":False,
        "source_flower_to_fruit_plant_matched":True,
        "self_compatibility_directly_randomized":False,
        "same_flower_pollinium_to_fruit_conversion_measured":False,
        "true_SCH_functional_optima_or_loss_L_measured":False,
    }
    path=outdir/"source_record_and_flower_schema.json"
    path.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
                    encoding="utf-8")
    print("BEGIN_SCH_ZENODO_FLOWER_SOURCE")
    print(path.read_text(encoding="utf-8"))
    print("END_SCH_ZENODO_FLOWER_SOURCE")
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir",type=Path,default=Path("artifacts/sch_original_blueberry_flower"))
    args=p.parse_args()
    run(args.outdir)
