from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def rep(text, old, new, label):
    n=text.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected 1 anchor, got {n}')
    return text.replace(old,new,1)

# Publication ledger
p=ROOT/'docs/PUBLICATION_MATERIAL_LEDGER.md'
text=p.read_text(encoding='utf-8')
for old,new,label in [
('## Current screening state — Batch 4 high-information full-text closure under V19','## Current screening state — Batch 4 title/abstract complete under V20','ledger heading'),
('title/abstract screened:         364','title/abstract screened:         405','ledger TA screened'),
('retained for full text:          248','retained for full text:          277','ledger retained'),
('title/abstract excluded:         116','title/abstract excluded:         128','ledger TA excluded'),
('unscreened:                      504','unscreened:                      463','ledger unscreened'),
('full-text eligible:              248','full-text eligible:              277','ledger FT eligible'),
('full-text undecided:               0','full-text undecided:              29','ledger FT backlog'),
('V18 adjudicates the 57 high-information Batch-4 title/abstract records (46 retain, 11 exclude), and V19 closes all 46 retained reports at full text (28 include, 18 exclude). The remaining Batch-4 work object is 41 title/abstract records outside the high-information queue. No V19 study is promoted to the strict linked gate.',
 'V18 adjudicates the 57 high-information Batch-4 title/abstract records (46 retain, 11 exclude), and V19 closes all 46 retained reports at full text (28 include, 18 exclude). V20 then adjudicates the remaining 41 genuinely new Batch-4 title/abstract records: 29 are retained for full text and 12 excluded. Batch 4 is now 100/100 complete at title/abstract stage; the current Batch-4 full-text backlog is 29. No V20 record is promoted into evidence lanes before full-text adjudication.','ledger Batch4 paragraph'),
('JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 504 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.',
 'JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 463 records remain title/abstract unscreened, 29 newly retained Batch-4 reports await full-text adjudication, and no common geography-by-cue-overlap estimand has passed independence/scale checks.','ledger JBI state'),
('| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 504 records |',
 '| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 463 records |','ledger framing'),
('| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 504 records remain title/abstract unscreened |',
 '| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 463 records remain title/abstract unscreened |','ledger PRISMA row'),
('| Batch 4 | high-information 57 TA decisions under V18; all 46 retained reports closed at full text under V19 | Fourth systematic batch in progress | Screen remaining 41 title/abstract records |',
 '| Batch 4 | 100/100 TA decisions under V20; V19 closed the high-information FT path and V20 retains 29 additional reports | Fourth systematic batch | Full-text adjudicate 29 newly retained reports |','ledger Batch4 row'),
('| Formal screening cumulative | 364 TA decisions; 117 primary includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Close the remaining 41 Batch-4 title/abstract records |',
 '| Formal screening cumulative | 405 TA decisions; 117 primary includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 29 | Evidence lanes and blockers | Close 29 newly retained Batch-4 full texts, then advance to Batch 5 |','ledger formal row'),
('| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 364 TA decisions; 117 includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 0 |',
 '| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 405 TA decisions; 117 includes; 130 assessed FT exclusions; 1 not retrieved; FT backlog 29 |','ledger fig2'),
('| Table 1 | Systematic study decisions/blockers | 364 TA screened; 117 primary includes; FT backlog 0 |',
 '| Table 1 | Systematic study decisions/blockers | 405 TA screened; 117 primary includes; FT backlog 29 |','ledger table1'),
]:
    text=rep(text,old,new,label)
p.write_text(text,encoding='utf-8')

# JBI readout
p=ROOT/'docs/SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md'
text=p.read_text(encoding='utf-8')
for old,new,label in [
('title/abstract screened:               364','title/abstract screened:               405','JBI TA screened'),
('retained for full text:                248','retained for full text:                277','JBI retained'),
('title/abstract excluded:               116','title/abstract excluded:               128','JBI excluded'),
('unscreened:                            504','unscreened:                            463','JBI unscreened'),
('full-text undecided among retained:      0','full-text undecided among retained:     29','JBI FT backlog'),
('V18 then retains 46 of 57 high-information Batch-4 records, and V19 resolves all 46 at full text: 28 include and 18 exclude. Strict remains 2; near-pass and evolutionary lanes rise to 104 and 39, while historical transition remains 4 and direct L4 remains unrecovered.',
 'V18 then retains 46 of 57 high-information Batch-4 records, and V19 resolves all 46 at full text: 28 include and 18 exclude. V20 adjudicates the remaining 41 new Batch-4 title/abstract records, retaining 29 and excluding 12. Batch 4 is now 100/100 complete at title/abstract stage. Strict remains 2; near-pass and evolutionary lanes remain 104 and 39, historical transition remains 4, and direct L4 remains unrecovered.','JBI V20 paragraph'),
('current retained full-text backlog:      0','current retained full-text backlog:     29','JBI decision backlog'),
('full title/abstract screening:          NO (504 remaining)','full title/abstract screening:          NO (463 remaining)','JBI remaining'),
('V18 and V19 close the Batch-4 high-information path through full text. The next work object is **title/abstract adjudication of the remaining 41 genuinely new Batch-4 records**. Independence and outcome-scale coding continue in parallel; screening progress alone does not authorize pooling.',
 'V20 closes Batch 4 at title/abstract stage. The next work object is **full-text adjudication of the 29 reports newly retained by V20**; after that, advance to Batch 5 title/abstract screening. Independence and outcome-scale coding continue in parallel; screening progress alone does not authorize pooling.','JBI next priority'),
]:
    text=rep(text,old,new,label)
p.write_text(text,encoding='utf-8')

# V20 readout
(ROOT/'docs/SCH_PRISMA_V20_BATCH4_REMAINDER_TITLE_ABSTRACT_READOUT.md').write_text('''# SCH PRISMA V20 — Batch-4 remainder title/abstract closure

## Machine-audited state

```text
frozen denominator:                    868
title/abstract screened:               405
retained for full text:                277
title/abstract excluded:               128
TA unscreened:                         463

primary studies included:              117
assessed full-text exclusions:         130
reports not retrieved:                   1
current full-text undecided:            29

STRICT_LINKED_EXPERIMENT:                2
DIRECTIONAL_OR_NEAR_PASS:              104
EVOLUTIONARY_OUTCOME:                   39
HISTORICAL_TRANSITION:                    4

positive geographic records:           25
positive receiver records:              24
joint geography + receiver records:     22
```

V20 adjudicates the 41 genuinely new Batch-4 title/abstract records that were outside the V18 high-information queue: 29 are retained for full text and 12 excluded. Together with the two prior decisions and the 57 V18 decisions, Batch 4 is now 100/100 complete at title/abstract stage.

V20 is screening progress only. No V20 record is promoted into the evidence lanes, geography counters, or historical-transition claims before full-text adjudication. The positive same-manipulated-`A` dual-audience strict chain remains unrecovered and direct shared-cue → private-cue L4 remains unrecovered.

The next work object is full-text adjudication of the 29 V20-retained reports. Screening completion alone does not authorize pooling.
''',encoding='utf-8')
print('V20 docs synchronized')
