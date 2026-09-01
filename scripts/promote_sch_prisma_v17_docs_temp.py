from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / 'empirical' / 'prisma'


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8', newline='') as h:
        return [{k: (v or '').strip() for k, v in row.items()} for row in csv.DictReader(h)]


def version(path: Path) -> int:
    return int(re.search(r'SCREENING_DECISIONS_V(\d+)', path.name).group(1))


def merged_rows() -> dict[str, dict[str, str]]:
    paths = sorted(PRISMA.glob('SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv'), key=version)
    assert [version(p) for p in paths] == list(range(1, 18))
    merged: dict[str, dict[str, str]] = {}
    for path in paths:
        for update in read_csv(path):
            row = merged.setdefault(update['record_id'], {})
            for key, value in update.items():
                if value:
                    row[key] = value
    return merged


def positive_geo(value: str) -> bool:
    u = value.upper()
    return bool(value) and value != 'NOT_REPORTED' and not u.startswith('NO_') and 'NOT_GEOGRAPHIC' not in u


def positive_receiver(value: str) -> bool:
    u = value.upper()
    return bool(value) and value != 'NOT_REPORTED' and not u.startswith('NO_')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {text.count(old)}')
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, repl: str, label: str) -> str:
    new, n = re.subn(pattern, repl, text, count=1, flags=re.M | re.S)
    if n != 1:
        raise RuntimeError(f'{label}: expected one substitution, got {n}')
    return new


rows = merged_rows()
included = [row for row in rows.values() if row.get('screen_fulltext') == 'INCLUDE']
assert len(included) == 89
geo = [row for row in included if positive_geo(row.get('geographic_contrast', ''))]
receiver = [row for row in included if positive_receiver(row.get('receiver_assemblage_contrast', ''))]
receiver_ids = {row['record_id'] for row in receiver}
joint = sorted([row for row in geo if row['record_id'] in receiver_ids], key=lambda r: r['record_id'])
assert (len(geo), len(receiver), len(joint)) == (20, 19, 17)

frozen = read_csv(PRISMA / 'frozen_v2' / 'SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv')
titles = {row['record_id']: row.get('title', '').replace('\n', ' ').strip() for row in frozen}
joint_block = '\n'.join(f"{row['record_id']}  {titles.get(row['record_id'], '')}" for row in joint)

# Publication ledger
p = ROOT / 'docs' / 'PUBLICATION_MATERIAL_LEDGER.md'
text = p.read_text(encoding='utf-8')
for old, new, label in [
    ('## Current screening state — Batch 3 title/abstract complete under V16', '## Current screening state — Batch 3 full-text closure complete under V17', 'ledger heading'),
    ('primary studies included:         73', 'primary studies included:         89', 'ledger includes'),
    ('formal full-text exclusions:      85', 'formal full-text exclusions:     113', 'ledger exclusions'),
    ('full-text undecided:              44', 'full-text undecided:               0', 'ledger backlog'),
    ('DIRECTIONAL_OR_NEAR_PASS:          64', 'DIRECTIONAL_OR_NEAR_PASS:          77', 'ledger near'),
    ('EVOLUTIONARY_OUTCOME:              22', 'EVOLUTIONARY_OUTCOME:              29', 'ledger evolutionary'),
    ('HISTORICAL_TRANSITION:               1', 'HISTORICAL_TRANSITION:               4', 'ledger historical'),
    ('### Batch-3 title/abstract closure under V16', '### Batch-3 full-text closure under V17', 'ledger Batch3 heading'),
    ('The current formal exclusion ledger contains 85 decisions: 84 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.', 'The current formal exclusion ledger contains 113 decisions: 112 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome.', 'ledger exclusion prose'),
    ('positive geographic contrasts:         13\npositive receiver/interactor contrasts:12\njoint geography + receiver records:    11', 'positive geographic contrasts:         20\npositive receiver/interactor contrasts:19\njoint geography + receiver records:    17', 'ledger geography counts'),
    ('| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 627 records |', '| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 561 records |', 'ledger framing row'),
    ('| Batch 3 | 100/100 TA decisions; V15 closes the 28 high-information full texts; V16 retains 44 additional reports | Third systematic batch | Full-text adjudicate 44 newly retained reports |', '| Batch 3 | 100/100 TA decisions; V17 resolves every retained Batch-3 report at full text | Third systematic batch | Closed; advance to Batch 4 title/abstract screening |', 'ledger Batch3 row'),
    ('| Formal screening cumulative | 307 TA decisions; 73 primary includes; 84 assessed FT exclusions; 1 not retrieved; FT backlog 44 | Evidence lanes and blockers | Close 44 newly retained Batch-3 full texts, then advance to Batch 4 |', '| Formal screening cumulative | 307 TA decisions; 89 primary includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Advance to Batch 4 title/abstract screening |', 'ledger formal row'),
    ('| Geography | 11 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |', '| Geography | 17 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |', 'ledger geography row'),
]:
    text = replace_once(text, old, new, label)
text = sub_once(
    text,
    r'Batch 2 remains closed\. V15 closed all 28 high-information Batch-3 full texts\. V16 now adjudicates the remaining 66 genuinely new Batch-3 title/abstract records: 44 are retained for full text and 22 excluded\. Batch 3 is therefore 100/100 complete at title/abstract stage, and the current Batch-3 full-text backlog is 44\. This does not authorize pooled effects and does not mean the 868-record screen is complete\.',
    'Batch 2 remains closed. V16 completed Batch-3 title/abstract screening, and V17 now resolves all 44 reports retained by V16 at full text: 16 are included and 28 excluded. Batch 3 is therefore closed at both title/abstract and current full-text stages. The next work object is Batch-4 title/abstract screening. This does not authorize pooled effects and does not mean the 868-record screen is complete.',
    'ledger Batch3 paragraph',
)
text = sub_once(
    text,
    r'The eleven joint-positive records are:\n\n```text\n.*?\n```',
    'The seventeen joint-positive records are:\n\n```text\n' + joint_block + '\n```',
    'ledger joint list',
)
text = sub_once(
    text,
    r'Thus the JBI axis is no longer resting on one isolated anchor\. V15 yields 11 joint-positive records,.*?A map of study locations cannot rescue a failed geography gate\.',
    'Thus the JBI axis is no longer resting on one isolated anchor. V17 yields 17 joint-positive records, but record count is not an independence count: overlapping *Primula*, *Lithophragma*, dissertation/published, and other research-program representations must be clustered before quantitative synthesis. JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 561 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.\n\nA map of study locations cannot rescue a failed geography gate.',
    'ledger JBI paragraph',
)
text = replace_once(
    text,
    '- component/stamen functional partitioning and conditional cue deployment.\n\n**lineage branching untested** remains the claim ceiling.',
    '- component/stamen functional partitioning and conditional cue deployment.\n- mating-system-associated cue vestigialization and additional geographic cue/receiver mosaics recovered under V17.\n\nV17 expands the `HISTORICAL_TRANSITION` lane to four records, but these are role, mating-system or trait-history transitions rather than reconstructed shared-cue → private-cue transitions. **lineage branching untested** remains the claim ceiling.',
    'ledger evolutionary boundary',
)
text = text.replace('| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 241 TA decisions; 53 includes; 76 assessed FT exclusions; 1 not retrieved; 28 FT pending |', '| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 307 TA decisions; 89 includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 |')
text = text.replace('| Figure 3 | Geographic receiver-regime synthesis | 8 joint-positive systems; final analysis waits for full screen |', '| Figure 3 | Geographic receiver-regime synthesis | 17 joint-positive records; independence clustering and full screen remain pending |')
text = text.replace('| Table 1 | Systematic study decisions/blockers | 241 TA screened; 53 primary includes; 28 FT pending |', '| Table 1 | Systematic study decisions/blockers | 307 TA screened; 89 primary includes; FT backlog 0 |')
p.write_text(text, encoding='utf-8')

# JBI readout
p = ROOT / 'docs' / 'SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md'
text = p.read_text(encoding='utf-8')
for old, new, label in [
    ('primary full-text inclusions:           73', 'primary full-text inclusions:           89', 'JBI includes'),
    ('formal full-text exclusions:            85', 'formal full-text exclusions:           113', 'JBI exclusions'),
    ('full-text undecided among retained:     44', 'full-text undecided among retained:      0', 'JBI backlog'),
    ('DIRECTIONAL_OR_NEAR_PASS:               64', 'DIRECTIONAL_OR_NEAR_PASS:               77', 'JBI near'),
    ('EVOLUTIONARY_OUTCOME:                   22', 'EVOLUTIONARY_OUTCOME:                   29', 'JBI evo'),
    ('HISTORICAL_TRANSITION:                    1', 'HISTORICAL_TRANSITION:                    4', 'JBI historical'),
    ('positive geographic contrast:            13\npositive receiver/interactor contrast:    12\njoint geographic + receiver records:      11', 'positive geographic contrast:            20\npositive receiver/interactor contrast:    19\njoint geographic + receiver records:      17', 'JBI geography counts'),
    ('current retained full-text backlog:     44', 'current retained full-text backlog:      0', 'JBI current backlog'),
    ('multiple joint geographic records:      YES (11 records; independence count not frozen)', 'multiple joint geographic records:      YES (17 records; independence count not frozen)', 'JBI joint status'),
]:
    text = replace_once(text, old, new, label)
text = sub_once(
    text,
    r'Batch 2 remains closed\. V15 now also closes the 28 high-information Batch-3 full texts retained by V14: 20 are included and eight excluded\. Strict remains 2, while near-pass and evolutionary lanes rise to 64 and 22; one role-transition study enters the historical-transition lane without satisfying L4\.',
    'Batch 2 remains closed. V16 completes Batch-3 title/abstract screening and V17 closes all 44 newly retained Batch-3 reports at full text: 16 are included and 28 excluded. Strict remains 2, while near-pass and evolutionary lanes rise to 77 and 29; the historical-transition lane reaches four records without satisfying shared-cue → private-cue L4.',
    'JBI V17 closure paragraph',
)
text = sub_once(
    text,
    r'The eleven current joint-positive records are:\n\n```text\n.*?\n```',
    'The seventeen current joint-positive records are:\n\n```text\n' + joint_block + '\n```',
    'JBI joint list',
)
text = sub_once(
    text,
    r'The change from historical `1/8` to eleven joint-positive records means the geography axis is worth developing,.*?It is \*\*not\*\* permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks\.',
    'The change from historical `1/8` to seventeen joint-positive records means the geography axis is worth developing, but overlapping research programs must be clustered before any independent-system count is frozen. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.',
    'JBI decision paragraph',
)
text = sub_once(
    text,
    r'The Batch-3 high-information queue is now closed through full text under V15\. The next work object is the \*\*remaining 66 genuinely new Batch-3 title/abstract records\*\*\.',
    'Batch 3 is now closed at title/abstract and current full-text stages under V17. The next work object is **Batch-4 title/abstract screening**.',
    'JBI next priority',
)
p.write_text(text, encoding='utf-8')

# Manuscript evidence spine
p = ROOT / 'manuscript' / 'MANUSCRIPT_SHARED_CUE_FRAMEWORK.md'
text = p.read_text(encoding='utf-8')
anchor = '- **Syngonium plant-bug transition:** comparative and behavioural evidence links recruitment of ancestrally florivorous plant bugs as specialized pollinators to a novel attractive floral volatile. This is a receiver-role transition and floral-trait divergence, not a reconstructed shared-cue → private-cue transition.\n'
addition = (
    '- **Abronia mating-system transition:** field and common-garden comparisons associate the transition toward selfing with near-complete floral-fragrance vestigialization. This is a historical attraction-syndrome transition, not evidence that an ancestral shared cue became private.\n'
    '- **Haplopappus elevation mosaic:** floral volatile blends, insect olfactory preference, fertilized seeds and predated seeds covary across an Andean elevation gradient; because floral `A` is comparative rather than randomized, this strengthens the geographic/evolutionary layer rather than the strict gate.\n'
)
if addition not in text:
    text = replace_once(text, anchor, anchor + addition, 'manuscript V17 evidence insertion')
text = replace_once(
    text,
    'Current evidence reaches L2 directly in several conflict systems and reaches L3 on the historical trait-divergence side. V15 also recovers a bounded receiver-role transition from florivory to pollination, but that transition does not reconstruct shared-cue → private-cue evolution. The strict L4 endpoint remains unrecovered.',
    'Current evidence reaches L2 directly in several conflict systems and reaches L3 on the historical trait-divergence side. Systematic expansion through V17 yields four bounded `HISTORICAL_TRANSITION` records spanning receiver-role, mating-system and trait-history transitions, but none reconstructs shared-cue → private-cue evolution. The strict L4 endpoint remains unrecovered.',
    'manuscript historical ceiling',
)
p.write_text(text, encoding='utf-8')

# V17 readout
(ROOT / 'docs' / 'SCH_PRISMA_V17_BATCH3_REMAINDER_FULLTEXT_READOUT.md').write_text(
    '''# SCH PRISMA V17 — Batch-3 remainder full-text closure\n\n## Machine-audited state\n\n```text\nfrozen denominator:                    868\ntitle/abstract screened:               307\nretained for full text:                202\ntitle/abstract excluded:               105\nTA unscreened:                         561\n\nreports sought for retrieval:          202\nreports not retrieved:                   1\nreports assessed for eligibility:      201\nprimary studies included:               89\nassessed full-text exclusions:         112\nformal full-text EXCLUDE decisions:    113\ncurrent full-text undecided:             0\n\nSTRICT_LINKED_EXPERIMENT:                2\nDIRECTIONAL_OR_NEAR_PASS:               77\nEVOLUTIONARY_OUTCOME:                   29\nHISTORICAL_TRANSITION:                    4\n\npositive geographic records:           20\npositive receiver records:              19\njoint geography + receiver records:     17\n```\n\nV17 adjudicates all 44 reports retained by V16: 16 are included and 28 excluded. No new strict linked experiment is admitted. The same manipulated-`A` positive pollinator + positive antagonist chain therefore remains unrecovered.\n\nV17 expands lower evidence layers, including mating-system-associated floral-fragrance vestigialization and additional elevation/geographic cue–receiver mosaics. Four records now carry the bounded `HISTORICAL_TRANSITION` lane, but none is a reconstructed shared-cue → private-cue transition; direct L4 remains zero/not evaluable.\n\nThe 17 joint geography–receiver records are record-level evidence, not an independence-corrected system count. Overlapping research programs must be clustered before quantitative synthesis.\n\nBatch 3 is closed at title/abstract and current full-text stages. The next systematic work object is Batch-4 title/abstract screening. Screening completion alone does not authorize pooling.\n''',
    encoding='utf-8',
)

print({'included': len(included), 'geo': len(geo), 'receiver': len(receiver), 'joint': len(joint)})
