from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / 'empirical' / 'prisma'


def read_csv(path: Path):
    with path.open(encoding='utf-8', newline='') as h:
        return [{k:(v or '').strip() for k,v in row.items()} for row in csv.DictReader(h)]


def version(path: Path) -> int:
    return int(re.search(r'SCREENING_DECISIONS_V(\d+)', path.name).group(1))


def merged_rows():
    paths=sorted(PRISMA.glob('SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv'), key=version)
    assert [version(p) for p in paths] == list(range(1,20))
    merged={}
    for path in paths:
        for update in read_csv(path):
            row=merged.setdefault(update['record_id'], {})
            for k,v in update.items():
                if v: row[k]=v
    return merged


def positive_geo(v: str) -> bool:
    u=v.upper(); return bool(v) and v!='NOT_REPORTED' and not u.startswith('NO_') and 'NOT_GEOGRAPHIC' not in u


def positive_receiver(v: str) -> bool:
    u=v.upper(); return bool(v) and v!='NOT_REPORTED' and not u.startswith('NO_')


def replace_once(text, old, new, label):
    n=text.count(old)
    if n != 1: raise RuntimeError(f'{label}: expected 1 anchor, found {n}')
    return text.replace(old,new,1)


def sub_once(text, pattern, repl, label):
    out,n=re.subn(pattern,repl,text,count=1,flags=re.M|re.S)
    if n != 1: raise RuntimeError(f'{label}: expected 1 substitution, found {n}')
    return out

rows=merged_rows()
included=[r for r in rows.values() if r.get('screen_fulltext')=='INCLUDE']
assert len(included)==117
geo=[r for r in included if positive_geo(r.get('geographic_contrast',''))]
receiver=[r for r in included if positive_receiver(r.get('receiver_assemblage_contrast',''))]
receiver_ids={r['record_id'] for r in receiver}
joint=sorted([r for r in geo if r['record_id'] in receiver_ids],key=lambda r:r['record_id'])
assert (len(geo),len(receiver),len(joint))==(25,24,22)
frozen=read_csv(PRISMA/'frozen_v2'/'SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv')
titles={r['record_id']:(r.get('title') or '').replace('\n',' ').strip() for r in frozen}
joint_block='\n'.join(f"{r['record_id']}  {titles.get(r['record_id'],'')}" for r in joint)

# Publication ledger
p=ROOT/'docs'/'PUBLICATION_MATERIAL_LEDGER.md'
text=p.read_text(encoding='utf-8')
for old,new,label in [
('## Current screening state — Batch 3 full-text closure complete under V17','## Current screening state — Batch 4 high-information full-text closure under V19','ledger heading'),
('title/abstract screened:         307','title/abstract screened:         364','ledger TA screened'),
('retained for full text:          202','retained for full text:          248','ledger retained'),
('title/abstract excluded:         105','title/abstract excluded:         116','ledger TA excluded'),
('unscreened:                      561','unscreened:                      504','ledger unscreened'),
('full-text eligible:              202','full-text eligible:              248','ledger FT eligible'),
('primary studies included:         89','primary studies included:        117','ledger includes'),
('formal full-text exclusions:     113','formal full-text exclusions:     131','ledger exclusions'),
('DIRECTIONAL_OR_NEAR_PASS:          77','DIRECTIONAL_OR_NEAR_PASS:         104','ledger near'),
('EVOLUTIONARY_OUTCOME:              29','EVOLUTIONARY_OUTCOME:              39','ledger evo'),
('The current formal exclusion ledger contains 113 decisions: 112 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.','The current formal exclusion ledger contains 131 decisions: 130 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.','ledger exclusion prose'),
('positive geographic contrasts:         20\npositive receiver/interactor contrasts:19\njoint geography + receiver records:    17','positive geographic contrasts:         25\npositive receiver/interactor contrasts:24\njoint geography + receiver records:    22','ledger geo counts'),
('| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 561 records |','| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 504 records |','ledger framing'),
('| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 561 records remain title/abstract unscreened |','| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 504 records remain title/abstract unscreened |','ledger prisma'),
('| Formal screening cumulative | 307 TA decisions; 89 primary includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Advance to Batch 4 title/abstract screening |','| Formal screening cumulative | 364 TA decisions; 117 primary includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Close the remaining 41 Batch-4 title/abstract records |','ledger formal'),
('| Geography | 17 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |','| Geography | 22 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |','ledger geo row'),
('| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 307 TA decisions; 89 includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 |','| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 364 TA decisions; 117 includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 0 |','ledger fig2'),
('| Figure 3 | Geographic receiver-regime synthesis | 17 joint-positive records; independence clustering and full screen remain pending |','| Figure 3 | Geographic receiver-regime synthesis | 22 joint-positive records; independence clustering and full screen remain pending |','ledger fig3'),
('| Table 1 | Systematic study decisions/blockers | 307 TA screened; 89 primary includes; FT backlog 0 |','| Table 1 | Systematic study decisions/blockers | 364 TA screened; 117 primary includes; FT backlog 0 |','ledger table1'),
]: text=replace_once(text,old,new,label)
anchor='Batch 2 remains closed. V16 completed Batch-3 title/abstract screening, and V17 now resolves all 44 reports retained by V16 at full text: 16 are included and 28 excluded. Batch 3 is therefore closed at both title/abstract and current full-text stages. The next work object is Batch-4 title/abstract screening. This does not authorize pooled effects and does not mean the 868-record screen is complete.'
replacement=anchor+'\n\nV18 adjudicates the 57 high-information Batch-4 title/abstract records (46 retain, 11 exclude), and V19 closes all 46 retained reports at full text (28 include, 18 exclude). The remaining Batch-4 work object is 41 title/abstract records outside the high-information queue. No V19 study is promoted to the strict linked gate.'
text=replace_once(text,anchor,replacement,'ledger V19 paragraph')
text=sub_once(text,r'The seventeen joint-positive records are:\n\n```text\n.*?\n```','The twenty-two joint-positive records are:\n\n```text\n'+joint_block+'\n```','ledger joint list')
text=sub_once(text,r'Thus the JBI axis is no longer resting on one isolated anchor\. V17 yields 17 joint-positive records,.*?A map of study locations cannot rescue a failed geography gate\.',
'''Thus the JBI axis is no longer resting on one isolated anchor. V19 yields 22 joint-positive records, but record count is not an independence count: overlapping *Collaea*, *Gelsemium*, *Primula*, *Lithophragma*, dissertation/published, and other research-program representations must be clustered before quantitative synthesis. JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 504 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.\n\nA map of study locations cannot rescue a failed geography gate.''','ledger JBI paragraph')
# add Batch 4 row after Batch 3
batch3='| Batch 3 | 100/100 TA decisions; V17 resolves every retained Batch-3 report at full text | Third systematic batch | Closed; advance to Batch 4 title/abstract screening |'
if '| Batch 4 |' not in text:
    text=replace_once(text,batch3,batch3+'\n| Batch 4 | high-information 57 TA decisions under V18; all 46 retained reports closed at full text under V19 | Fourth systematic batch in progress | Screen remaining 41 title/abstract records |','ledger batch4 row')
# same-code near pass addition
junker='- **Junker & Blüthgen 2010**: the same synthetic floral-scent coordinate attracts bumblebees while repelling ants; this is a clean opposite-receiver same-code near-pass, but it lacks a common plant reproductive outcome.\n'
thistle='- **Theis 2006, Canada thistle**: synthetic benzaldehyde and phenylacetaldehyde baits attract both pollinators and floral herbivores on the same chemical coordinate. This strengthens shared-code recurrence but lacks a common plant reproductive outcome.\n'
if thistle not in text: text=replace_once(text,junker,junker+thistle,'ledger thistle')
p.write_text(text,encoding='utf-8')

# JBI readout
p=ROOT/'docs'/'SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md'
text=p.read_text(encoding='utf-8')
for old,new,label in [
('title/abstract screened:               307','title/abstract screened:               364','jbi screened'),
('retained for full text:                202','retained for full text:                248','jbi retained'),
('title/abstract excluded:               105','title/abstract excluded:               116','jbi ta excluded'),
('unscreened:                            561','unscreened:                            504','jbi unscreened'),
('primary full-text inclusions:           89','primary full-text inclusions:          117','jbi incl'),
('formal full-text exclusions:           113','formal full-text exclusions:           131','jbi excl'),
('DIRECTIONAL_OR_NEAR_PASS:               77','DIRECTIONAL_OR_NEAR_PASS:              104','jbi near'),
('EVOLUTIONARY_OUTCOME:                   29','EVOLUTIONARY_OUTCOME:                   39','jbi evo'),
('positive geographic contrast:            20\npositive receiver/interactor contrast:    19\njoint geographic + receiver records:      17','positive geographic contrast:            25\npositive receiver/interactor contrast:    24\njoint geographic + receiver records:      22','jbi geo'),
('current retained full-text backlog:      0','current retained full-text backlog:      0','jbi backlog'),
('multiple joint geographic records:      YES (17 records; independence count not frozen)','multiple joint geographic records:      YES (22 records; independence count not frozen)','jbi joint status'),
('full title/abstract screening:          NO (561 remaining)','full title/abstract screening:          NO (504 remaining)','jbi remaining'),
]: text=replace_once(text,old,new,label)
text=sub_once(text,r'The seventeen current joint-positive records are:\n\n```text\n.*?\n```','The twenty-two current joint-positive records are:\n\n```text\n'+joint_block+'\n```','jbi joint list')
text=sub_once(text,r'The change from historical `1/8` to seventeen joint-positive records means the geography axis is worth developing,.*?It is \*\*not\*\* permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks\.',
'The change from historical `1/8` to twenty-two joint-positive records means the geography axis is worth developing, but overlapping research programs must be clustered before any independent-system count is frozen. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.','jbi decision')
text=sub_once(text,r'## Next systematic priority\n\nBatch 3 is now closed at title/abstract and current full-text stages under V17\. The next work object is \*\*Batch-4 title/abstract screening\*\*\.',
'## Next systematic priority\n\nV18 and V19 close the Batch-4 high-information path through full text. The next work object is **title/abstract adjudication of the remaining 41 genuinely new Batch-4 records**.','jbi next')
# insert V19 paragraph
anchor='Batch 2 remains closed. V16 completes Batch-3 title/abstract screening and V17 closes all 44 newly retained Batch-3 reports at full text: 16 are included and 28 excluded. Strict remains 2, while near-pass and evolutionary lanes rise to 77 and 29; the historical-transition lane reaches four records without satisfying shared-cue → private-cue L4.'
replacement=anchor+'\n\nV18 then retains 46 of 57 high-information Batch-4 records, and V19 resolves all 46 at full text: 28 include and 18 exclude. Strict remains 2; near-pass and evolutionary lanes rise to 104 and 39, while historical transition remains 4 and direct L4 remains unrecovered.'
text=replace_once(text,anchor,replacement,'jbi v19 paragraph')
p.write_text(text,encoding='utf-8')

# Manuscript
p=ROOT/'manuscript'/'MANUSCRIPT_SHARED_CUE_FRAMEWORK.md'
text=p.read_text(encoding='utf-8')
text=replace_once(text,'Systematic expansion through V17 yields four bounded `HISTORICAL_TRANSITION` records spanning receiver-role, mating-system and trait-history transitions, but none reconstructs shared-cue → private-cue evolution.','Systematic expansion through V19 retains four bounded `HISTORICAL_TRANSITION` records spanning receiver-role, mating-system and trait-history transitions, but none reconstructs shared-cue → private-cue evolution.','manuscript v19 hist')
junker='- **Junker & Blüthgen 2010:** a same-synthetic-scent near-pass in which bumblebees are attracted while ants are repelled; the opposite receiver responses are on the same chemical coordinate, but no common plant reproductive outcome is measured.\n'
thistle='- **Theis 2006, Canada thistle:** synthetic floral-scent baits show that benzaldehyde and phenylacetaldehyde attract both pollinators and floral herbivores. This is direct shared-code recurrence on a manipulated chemical coordinate, but no common plant reproductive outcome is measured.\n'
if thistle not in text: text=replace_once(text,junker,junker+thistle,'manuscript thistle')
hap='- **Haplopappus elevation mosaic:** floral volatile blends, insect olfactory preference, fertilized seeds and predated seeds covary across an Andean elevation gradient; because floral `A` is comparative rather than randomized, this strengthens the geographic/evolutionary layer rather than the strict gate.\n'
extra='- **Collaea cipoensis:** pollinators favor larger and more numerous flowers while nectar robbers/florivores impose opposing selection on the same attractiveness traits and female fitness; the shared display axis is observational rather than randomized.\n- **Pedicularis rex and Gelsemium sempervirens geographic mosaics:** replicated populations/common gardens show that pollinator benefit, seed predation or nectar robbing, floral traits and reproduction vary geographically. These systems strengthen the biogeographic/evolutionary layer without satisfying `do(A)`.\n'
if extra not in text: text=replace_once(text,hap,hap+extra,'manuscript v19 geo')
p.write_text(text,encoding='utf-8')

# V19 readout
(ROOT/'docs'/'SCH_PRISMA_V19_BATCH4_HIGH_INFORMATION_FULLTEXT_READOUT.md').write_text('''# SCH PRISMA V19 — Batch-4 high-information full-text closure\n\n## Machine-audited state\n\n```text\nfrozen denominator:                    868\ntitle/abstract screened:               364\nretained for full text:                248\ntitle/abstract excluded:               116\nTA unscreened:                         504\n\nreports sought for retrieval:          248\nreports not retrieved:                   1\nreports assessed for eligibility:      247\nprimary studies included:              117\nassessed full-text exclusions:         130\nformal full-text EXCLUDE decisions:    131\ncurrent full-text undecided:             0\n\nSTRICT_LINKED_EXPERIMENT:                2\nDIRECTIONAL_OR_NEAR_PASS:              104\nEVOLUTIONARY_OUTCOME:                   39\nHISTORICAL_TRANSITION:                    4\n\npositive geographic records:           25\npositive receiver records:              24\njoint geography + receiver records:     22\n```\n\nV19 adjudicates all 46 reports retained by the V18 high-information title/abstract screen: 28 are included and 18 excluded. No new strict linked experiment is admitted. The same manipulated-`A` positive pollinator + positive antagonist + common reproductive-outcome chain therefore remains unrecovered.\n\nA particularly strong new same-code near-pass is Canada thistle: synthetic scent baits identify compounds attractive to both pollinators and floral herbivores, but the experiment has no common plant reproductive outcome. Geographic conflict evidence also expands through Collaea, Pedicularis, Polygala, Lamium/Meehania and Gelsemium.\n\nThe 22 joint geography–receiver records remain report-level counts, not independence-corrected biological systems. The next systematic work object is title/abstract screening of the remaining 41 new Batch-4 records.\n''',encoding='utf-8')
print({'included':len(included),'geo':len(geo),'receiver':len(receiver),'joint':len(joint)})
