"""Authentic original experimental colonization records, NOT fabricated data.

Makowski, Lamb & Galloway (2024), American Journal of Botany,
DOI 10.1002/ajb2.16351.
Official Zenodo source record 10814705, DOI 10.5281/zenodo.10814705,
CC-BY-4.0. Dataset has original source-row seed outcomes (individual
flower's natural/control vs hand-supplemented treatment) and separate
pollinator observations per experimental population.

This tool validates exact publisher-listed MD5 before accepting any rows;
it reports actual columns, missingness, provenance, candidate paired
grains and crossfile label structure, but DOES NOT refit results.
No matching at flower-level across pollen observation file (population
visitation data, different risk set). Four original source populations
are not four independent published papers.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter,defaultdict
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

ARTICLE_DOI="10.1002/ajb2.16351"
ZENODO_RECORD=10814705
DATA_DOI="10.5281/zenodo.10814705"
LICENSE="CC-BY-4.0"
BASE="https://zenodo.org/records/10814705/files"
MANIFEST={
    "PLdataindividual.csv":"b84fa5c83513dbe75c0bf7840d1c74aa",
    "pollinator.csv":"81e0deaa78a6a97e1211484cb9d0d3b3",
}
MAX_BYTES=1_000_000
SENTINELS={"","NA","N/A","null","NULL","nan","NaN",".","-"}

def fetch_verified(name):
    if name not in MANIFEST:
        raise ValueError("Only exact original archive file names may be requested")
    url=BASE+"/"+name+"?download=1"
    req=Request(url,headers={"User-Agent":"SCH-2024-Campanula-original-source/1.0",
                             "Accept":"text/csv,application/octet-stream"})
    with urlopen(req,timeout=35) as resp:
        b=resp.read(MAX_BYTES+1)
        provenance={"requested_url":url,"final_url":resp.geturl(),
                    "status":resp.status,
                    "reported_content_type":resp.headers.get("content-type","")}
    if not b or len(b)>MAX_BYTES:
        raise ValueError("Original source CSV empty or oversize")
    if b.lstrip()[:100].lower().startswith((b"<!doctype",b"<html",b"<?xml")):
        raise ValueError("HTML or XML is not the original published data")
    digest=hashlib.md5(b).hexdigest()
    if digest!=MANIFEST[name]:
        raise ValueError("Original 2024 Zenodo published source MD5 changed: "+name)
    provenance.update({
        "original_MD5":digest,
        "original_SHA256":hashlib.sha256(b).hexdigest(),
        "original_source_bytes":len(b),
    })
    return b,provenance

def _csv_rows(b):
    try:
        data=b.decode("utf-8-sig");encoding="utf-8-sig"
    except UnicodeError:
        data=b.decode("latin-1");encoding="latin-1"
    try:
        dialect=csv.Sniffer().sniff(data[:min(8192,len(data))],delimiters=",;\t")
    except csv.Error as exc:
        raise ValueError("Source CSV separator cannot be identified") from exc
    read=csv.DictReader(io.StringIO(data),dialect=dialect)
    fields=read.fieldnames
    if not fields or len(fields)<5 or len(set(fields))!=len(fields):
        raise ValueError("Original CSV headers too short or duplicated")
    rows=list(read)
    if len(rows)<10 or len(rows)>20000 or any(None in x for x in rows):
        raise ValueError("Unexpected published CSV record count or malformed row")
    return rows,fields,encoding

def _normal(x):
    return re.sub(r"[^a-z0-9]","",str(x).lower())

def col(headers,*names):
    mapping={_normal(x):x for x in headers}
    for name in names:
        if _normal(name) in mapping:return mapping[_normal(name)]
    return None

def audit_roles(rows,headers,kind):
    if kind=="PLdataindividual.csv":
        roles={
         "source_population":col(headers,"source.population","source population"),
         "autonomy":col(headers,"autonomy","selfing autonomy"),
         "individual":col(headers,"individual","plant id","plant"),
         "experimental_population":col(headers,"experimental.population","experimental population"),
         "site":col(headers,"site","site ID"),
         "size":col(headers,"size","experimental size"),
         "treatment":col(headers,"treatment","pollination treatment"),
         "seed_count":col(headers,"seed number","seed.number","seednumber","seedset","seeds"),
         "initial_day":col(headers,"dayfromstartofexperiment","dayfromstart"),
        }
        critical=("source_population","autonomy","individual",
                  "experimental_population","site","size","treatment","seed_count")
    else:
        roles={
         "experimental_population":col(headers,"experimental.population","experimental population"),
         "source_population":col(headers,"source population","source.population"),
         "autonomy":col(headers,"autonomy"),
         "site":col(headers,"site"),
         "size":col(headers,"size"),
         "total_visits":col(headers,"total.poll.visits","total poll visits"),
         "visits_per_flower":col(headers,"visits.per.flower","visits per flower"),
        }
        critical=("experimental_population","source_population","autonomy","site","size")
    missing=[k for k in critical if roles[k] is None]
    levels={}
    for k,h in roles.items():
        if h is None:continue
        cnt=Counter(str(row[h]).strip() for row in rows)
        if k in ("site","source_population","autonomy","size","treatment"):
            levels[k]={str(x):int(n) for x,n in cnt.items()}
        else:
            nonmissing=[x for x,n in cnt.items() if x not in SENTINELS]
            levels[k]={"n_original_unique_nonmissing":len(nonmissing),
                       "n_original_missing":sum(n for x,n in cnt.items() if x in SENTINELS),
                       "sample_values":nonmissing[:7]}
    duplicates=None
    if kind=="PLdataindividual.csv":
        if all(roles.get(x) for x in
               ("source_population","experimental_population","site","individual","treatment")):
            grp=Counter(tuple(str(row[roles[x]]).strip() for x in
                              ("source_population","experimental_population","site","individual","treatment"))
                       for row in rows)
            duplicates={
             "n_distinct_original_plant_by_pollination_treatment_labels":len(grp),
             "n_source_label_groups_with_replicate_flower_records":sum(n>1 for n in grp.values()),
             "max_original_flower_records_per_label_group":max(grp.values()),
             "n_flower_rows_in_groups_with_repeated_source_labels":sum(n for n in grp.values() if n>1),
             "original_source_row_is_flower_not_independent_experimental_population":True,
            }
    outcome={}
    if kind=="PLdataindividual.csv" and roles["seed_count"]:
        vals=[]
        errors=0
        for row in rows:
            x=row[roles["seed_count"]].strip()
            if x in SENTINELS:continue
            try:
                v=float(x)
                if v<0 or abs(round(v)-v)>1e-8:errors+=1
                else: vals.append(int(v))
            except ValueError:errors+=1
        outcome={
            "n_original_nonmissing_integer_seed_counts":len(vals),
            "n_source_invalid_nonmissing_seed_counts":errors,
            "source_seed_count_min":min(vals) if vals else None,
            "source_seed_count_max":max(vals) if vals else None,
            "source_seed_count_zero_rows":sum(v==0 for v in vals),
        }
    return {
       "n_original_source_rows":len(rows),
       "n_original_columns":len(headers),
       "original_headers":headers,
       "original_source_roles":roles,
       "required_source_roles_missing":missing,
       "reported_source_levels":levels,
       "seed_outcome_diagnostics":outcome,
       "original_flower_record_grain":duplicates,
       "source_label_roles_qualified":len(missing)==0,
       "regression_on_original_source_plant_records_run":False,
       "causal_ovule_fertilization_per_flower_available":False,
    }

def run(out):
    out.mkdir(parents=True,exist_ok=True)
    files=[]
    for name in MANIFEST:
        raw,provenance=fetch_verified(name)
        rows,headers,encoding=_csv_rows(raw)
        source=audit_roles(rows,headers,name)
        (out/name).write_bytes(raw)
        files.append({
          "original_filename":name,
          "source_provenance":provenance,
          "source_encoding":encoding,
          "source_grain":source,
        })
    results={
      "analysis":"sch_campanula_americana_2024_original_archival_ingress_v1",
      "source_original_article_DOI":ARTICLE_DOI,
      "source_original_zenodo_DOI":DATA_DOI,
      "source_license":LICENSE,
      "source_record":ZENODO_RECORD,
      "n_genuine_original_files":len(files),
      "n_independent_original_published_programmes":1,
      "n_original_source_populations_expected_from_publication":4,
      "original_sources":files,
      "original_pollination_and_visitation_not_same_individual_flower_risk_set":True,
      "original_population_size_contrast_is_experimental_design_not_global_macro_effect":True,
      "original_fitness_component_conflict_L_not_identified":True,
      "status":"GENUINE_SOURCE_MD5_CHECKED_ROLES_PENDING_DESIGN_QA",
    }
    path=out/"original_campanula_2024_ingress.json"
    path.write_text(json.dumps(results,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_2024_CAMPANULA_ORIGINAL_SOURCE")
    print(json.dumps(results,indent=2,sort_keys=True,ensure_ascii=False))
    print("END_SCH_2024_CAMPANULA_ORIGINAL_SOURCE")
    return results

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,default=Path("artifacts/sch_campanula_2024"))
    a=p.parse_args()
    run(a.out)
