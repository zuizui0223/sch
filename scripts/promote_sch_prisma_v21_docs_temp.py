from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / 'empirical' / 'prisma'


def read_csv(path: Path):
    with path.open(encoding='utf-8', newline='') as h:
        return [{k: (v or '').strip() for k, v in row.items()} for row in csv.DictReader(h)]


def version(path: Path) -> int:
    return int(re.search(r'SCREENING_DECISIONS_V(\d+)', path.name).group(1))


def merged_rows():
    paths=sorted(PRISMA.glob('SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv'),key=version)
    assert [version(p) for p in paths] == list(range(1,22))
    merged={}
    for path in paths:
        for update in read_csv(path):
            row=merged.setdefault(update['record_id'],{})
            for k,v in update.items():
                if v: row[k]=v
    return merged


def positive_geo(v: str) -> bool:
    u=v.upper(); return bool(v) and v!='NOT_REPORTED' and not u.startswith('NO_') and 'NOT_GEOGRAPHIC' not in u


def positive_receiver(v: str) -> bool:
    u=v.upper(); return bool(v) and v!='NOT_REPORTED' and not u.startswith('NO_')


def one(text: str, old: str, new: str, label: str) -> str:
    n=text.count(old)
    if n != 1: raise RuntimeError(f'{label}: expected 1 anchor, got {n}')
    return text.replace(old,new,1)


def sub(text: str, pat: str, repl: str, label: str) -> str:
    out,n=re.subn(pat,repl,text,count=1,flags=re.M|re.S)
    if n != 1: raise RuntimeError(f'{label}: expected 1 substitution, got {n}')
    return out

rows=merged_rows()
included=[r for r in rows.values() if r.get('screen_fulltext')=='INCLUDE']
assert len(included)==122
geo=[r for r in included if positive_geo(r.get('geographic_contrast',''))]
recv=[r for r in included if positive_receiver(r.get('receiver_assemblage_contrast',''))]
recv_ids={r['record_id'] for r in recv}
joint=sorted([r for r in geo if r['record_id'] in recv_ids],key=lambda r:r['record_id'])
assert (len(geo),len(recv),len(joint))==(27,28,24)
frozen=read_csv(PRISMA/'frozen_v2'/'SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv')
titles={r['record_id']:r.get('title','').replace('\n',' ').strip() for r in frozen}
joint_block='\n'.join(f"{r['record_id']}  {titles.get(r['record_id'],'')}" for r in joint)

# Publication ledger
p=ROOT/'docs'/'PUBLICATION_MATERIAL_LEDGER.md'
t=p.read_text(encoding='utf-8')
for old,new,label in [
('## Current screening state — Batch 4 title/abstract complete under V20','## Current screening state — Batch 4 full-text closure complete under V21','ledger heading'),
('primary studies included:        117','primary studies included:        122','ledger include'),
('formal full-text exclusions:     131','formal full-text exclusions:     155','ledger exclude'),
('full-text undecided:              29','full-text undecided:               0','ledger backlog'),
('DIRECTIONAL_OR_NEAR_PASS:         104','DIRECTIONAL_OR_NEAR_PASS:         108','ledger near'),
('EVOLUTIONARY_OUTCOME:              39','EVOLUTIONARY_OUTCOME:              41','ledger evo'),
('positive geographic contrasts:         25\npositive receiver/interactor contrasts:24\njoint geography + receiver records:    22','positive geographic contrasts:         27\npositive receiver/interactor contrasts:28\njoint geography + receiver records:    24','ledger geo counts'),
('The current formal exclusion ledger contains 131 decisions: 130 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.','The current formal exclusion ledger contains 155 decisions: 154 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.','ledger exclusion prose'),
]: t=one(t,old,new,label)
t=sub(t,r'V18 adjudicates the 57 high-information Batch-4 title/abstract records \(46 retain, 11 exclude\), and V19 closes all 46 retained reports at full text \(28 include, 18 exclude\)\. V20 then adjudicates the remaining 41 genuinely new Batch-4 title/abstract records: 29 are retained for full text and 12 excluded\. Batch 4 is now 100/100 complete at title/abstract stage; the current Batch-4 full-text backlog is 29\. No V20 record is promoted into evidence lanes before full-text adjudication\.',
      'V18 adjudicates the 57 high-information Batch-4 title/abstract records (46 retain, 11 exclude), V19 closes those 46 reports at full text (28 include, 18 exclude), and V20 adjudicates the remaining 41 title/abstract records (29 retain, 12 exclude). V21 now closes all 29 V20-retained reports at full text: five are included and 24 excluded. Batch 4 is therefore closed at both title/abstract and current full-text stages. No V21 study enters the strict linked gate.', 'ledger batch4 paragraph')
t=sub(t,r'The .*? joint-positive records are:\n\n```text\n.*?\n```','The twenty-four joint-positive records are:\n\n```text\n'+joint_block+'\n```','ledger joint list')
t=sub(t,r'Thus the JBI axis is no longer resting on one isolated anchor\. V19 yields 22 joint-positive records,.*?A map of study locations cannot rescue a failed geography gate\.',
      'Thus the JBI axis is no longer resting on one isolated anchor. V21 yields 24 joint-positive records, but record count is not an independence count: overlapping research programs must be clustered before quantitative synthesis. JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 463 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.\n\nA map of study locations cannot rescue a failed geography gate.', 'ledger JBI paragraph')
t=t.replace('| Batch 4 | 100/100 TA decisions; V19 closes the high-information FT queue; V20 retains 29 additional reports | Fourth systematic batch | Full-text adjudicate 29 V20-retained reports |','| Batch 4 | 100/100 TA decisions; V21 resolves every currently retained Batch-4 report at full text | Fourth systematic batch | Closed; advance to Batch 5 title/abstract screening |')
t=t.replace('| Formal screening cumulative | 405 TA decisions; 117 primary includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 29 | Evidence lanes and blockers | Close 29 V20-retained Batch-4 full texts, then advance to Batch 5 |','| Formal screening cumulative | 405 TA decisions; 122 primary includes; 154 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Advance to Batch 5 title/abstract screening |')
t=t.replace('| Geography | 22 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |','| Geography | 24 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |')
t=t.replace('Frozen denominator; 405 TA decisions; 117 includes; 130 assessed FT exclusions; 1 not retrieved; 29 FT pending','Frozen denominator; 405 TA decisions; 122 includes; 154 assessed FT exclusions; 1 not retrieved; FT backlog 0')
t=t.replace('22 joint-positive records; independence clustering and full screen remain pending','24 joint-positive records; independence clustering and full screen remain pending')
t=t.replace('405 TA screened; 117 primary includes; 29 FT pending','405 TA screened; 122 primary includes; FT backlog 0')
p.write_text(t,encoding='utf-8')

# JBI readout
p=ROOT/'docs'/'SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md'
t=p.read_text(encoding='utf-8')
for old,new,label in [
('primary full-text inclusions:          117','primary full-text inclusions:          122','JBI include'),
('formal full-text exclusions:           131','formal full-text exclusions:           155','JBI exclude'),
('full-text undecided among retained:     29','full-text undecided among retained:      0','JBI backlog'),
('DIRECTIONAL_OR_NEAR_PASS:              104','DIRECTIONAL_OR_NEAR_PASS:              108','JBI near'),
('EVOLUTIONARY_OUTCOME:                   39','EVOLUTIONARY_OUTCOME:                   41','JBI evo'),
('positive geographic contrast:            25\npositive receiver/interactor contrast:    24\njoint geographic + receiver records:      22','positive geographic contrast:            27\npositive receiver/interactor contrast:    28\njoint geographic + receiver records:      24','JBI geo'),
('current retained full-text backlog:     29','current retained full-text backlog:      0','JBI backlog state'),
('multiple joint geographic records:      YES (22 records; independence count not frozen)','multiple joint geographic records:      YES (24 records; independence count not frozen)','JBI joint state'),
]: t=one(t,old,new,label)
t=sub(t,r'V18 then retains 46 of 57 high-information Batch-4 records, and V19 resolves all 46 at full text: 28 include and 18 exclude\. V20 adjudicates the remaining 41 new Batch-4 title/abstract records, retaining 29 and excluding 12\. Batch 4 is now 100/100 complete at title/abstract stage\. Strict remains 2; near-pass and evolutionary lanes remain 104 and 39, historical transition remains 4, and direct L4 remains unrecovered\.',
      'V18 retains 46 of 57 high-information Batch-4 records, V19 resolves those 46 at full text (28 include, 18 exclude), and V20 adjudicates the remaining 41 title/abstract records (29 retain, 12 exclude). V21 closes all 29 retained reports at full text (five include, 24 exclude). Batch 4 is now closed at title/abstract and current full-text stages. Strict remains 2; near-pass and evolutionary lanes rise to 108 and 41, historical transition remains 4, and direct L4 remains unrecovered.', 'JBI V21 paragraph')
t=sub(t,r'The .*? current joint-positive records are:\n\n```text\n.*?\n```','The twenty-four current joint-positive records are:\n\n```text\n'+joint_block+'\n```','JBI joint list')
t=sub(t,r'The change from historical `1/8` to .*? joint-positive records means the geography axis is worth developing,.*?It is \*\*not\*\* permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks\.',
      'The change from historical `1/8` to twenty-four joint-positive records means the geography axis is worth developing, but overlapping research programs must be clustered before any independent-system count is frozen. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.', 'JBI decision')
t=sub(t,r'V20 closes Batch 4 at title/abstract stage\. The next work object is \*\*full-text adjudication of the 29 reports newly retained by V20\*\*; after that, advance to Batch 5 title/abstract screening\.',
      'Batch 4 is now closed at title/abstract and current full-text stages under V21. The next work object is **Batch-5 title/abstract screening**.', 'JBI next priority')
p.write_text(t,encoding='utf-8')

# Manuscript: add only high-value V21 systems while preserving strict/L4 boundary
p=ROOT/'manuscript'/'MANUSCRIPT_SHARED_CUE_FRAMEWORK.md'
t=p.read_text(encoding='utf-8')
anchor='- **Haplopappus elevation mosaic:** floral volatile blends, insect olfactory preference, fertilized seeds and predated seeds covary across an Andean elevation gradient; because floral `A` is comparative rather than randomized, this strengthens the geographic/evolutionary layer rather than the strict gate.\n'
addition=(
'- **Willmer floral-VOC receiver filter:** isolated/synthetic floral and pollen volatiles are compatible with beneficial bee visitation while repelling ants, providing a same-coordinate receiver-filtering near-pass without a common plant reproductive outcome.\n'
'- **Roscoea geographic syndrome divergence:** geographically and phenologically isolated species differ in floral syndrome together with Bombus pollination and lepidopteran nectar-robbing roles; this is comparative geographic divergence, not randomized `A` or ancestral cue reconstruction.\n'
'- **Brassica floral-VOC artificial selection:** bidirectional artificial selection demonstrates heritable evolvability and pleiotropic architecture of floral volatile emission, but the experiment contains no direct pollinator or antagonist receiver assay and therefore enters only the evolutionary lane.\n'
)
if addition not in t: t=one(t,anchor,anchor+addition,'manuscript V21 insert')
p.write_text(t,encoding='utf-8')

# V21 readout
(ROOT/'docs'/'SCH_PRISMA_V21_BATCH4_REMAINDER_FULLTEXT_READOUT.md').write_text('''# SCH PRISMA V21 — Batch-4 full-text closure\n\n## Machine-audited state\n\n```text\nfrozen denominator:                    868\ntitle/abstract screened:               405\nretained for full text:                277\ntitle/abstract excluded:               128\nTA unscreened:                         463\n\nreports sought for retrieval:          277\nreports not retrieved:                   1\nreports assessed for eligibility:      276\nprimary studies included:              122\nassessed full-text exclusions:         154\nformal full-text EXCLUDE decisions:    155\ncurrent full-text undecided:             0\n\nSTRICT_LINKED_EXPERIMENT:                2\nDIRECTIONAL_OR_NEAR_PASS:              108\nEVOLUTIONARY_OUTCOME:                   41\nHISTORICAL_TRANSITION:                    4\n\npositive geographic records:           27\npositive receiver records:              28\njoint geography + receiver records:     24\n```\n\nV21 adjudicates all 29 reports retained by V20: five are included and 24 excluded. No new strict linked experiment is admitted. The same manipulated-`A` positive pollinator + positive antagonist chain therefore remains unrecovered.\n\nThe five new primary inclusions add a same-VOC ant-filtering near-pass, two geographic receiver-regime systems, an induced herbivory–pollinator–antagonist–fitness pathway, and experimental floral-VOC evolvability. None establishes reconstructed shared-cue → private-cue L4.\n\nThe 24 joint geography–receiver records are record-level evidence, not an independence-corrected system count. Batch 4 is closed at title/abstract and current full-text stages. The next systematic work object is Batch-5 title/abstract screening. Screening completion alone does not authorize pooling.\n''',encoding='utf-8')
print({'included':len(included),'geo':len(geo),'receiver':len(recv),'joint':len(joint)})
