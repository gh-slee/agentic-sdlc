"""Validate PR shape and optional source freshness; never authenticate evidence claims."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / 'templates/pr-standard.json').read_text())


def blocks(markdown):
    # Remove HTML comments before parsing, including an unfinished final comment.
    clean = re.sub(r'<!--.*?(?:-->|$)', '', markdown, flags=re.S)
    fence = None
    sections = []
    current = None
    for line in clean.splitlines():
        token = re.match(r' {0,3}(`{3,}|~{3,})(.*)$', line)
        if token:
            run, tail = token.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is not None:
            continue
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if heading:
            current = {'level': len(heading[1]), 'title': heading[2], 'lines': []}
            sections.append(current)
        elif current is not None and line.strip():
            current['lines'].append(line)
    return sections


def validate(body, expected_head=None):
    errors = []
    pins = re.findall(r'<!-- sdlc-head: ([0-9a-f]{40}) -->', body)
    if len(pins) != 1:
        errors.append('Include exactly one full source revision in sdlc-head metadata')
    elif expected_head is not None and pins[0] != expected_head:
        errors.append('PR evidence is stale for the expected source revision')
    if re.search(r'<(?:STATUS|SHA|HEAD|command|path|result)[^>]*>|\bTODO\b|\bTBD\b', body):
        errors.append('Replace unfinished placeholders')
    sections = blocks(body)
    top = [b for b in sections if b['level'] == 2]
    titles = [b['title'] for b in top]
    order = SPEC['required'] + SPEC['optional']
    if titles[:3] != SPEC['required'] or len(set(titles)) != len(titles):
        errors.append('Use each required section once in canonical order')
    if any(t not in order for t in titles) or [order.index(t) for t in titles if t in order] != sorted(order.index(t) for t in titles if t in order):
        errors.append('Unknown or out-of-order section')
    by_name = {b['title']: b for b in top}
    summary = by_name.get('Change Summary', {}).get('lines', [])
    if not summary or summary[0].startswith(('-', '*', '#')):
        errors.append('Change Summary needs a problem/outcome sentence')
    files = by_name.get('Files Changed', {}).get('lines', [])
    if not files or any(not re.fullmatch(r'[-*] `[^`\n]+`(?:, `[^`\n]+`)*: \S.+', line) for line in files):
        errors.append('Describe changed modules with path-and-explanation bullets')
    test_index = next((i for i,b in enumerate(sections) if b['level']==2 and b['title']=='Testing & Evidence'), None)
    evidence = []
    if test_index is not None:
        for block in sections[test_index+1:]:
            if block['level'] == 2: break
            evidence.append(block)
    if [(b['level'],b['title']) for b in evidence] != [(3,t) for t in SPEC['evidence']]:
        errors.append('Separate all evidence categories under Testing & Evidence')
    for block in evidence:
        entries = block['lines']
        if not entries:
            errors.append('Empty evidence category: '+block['title'])
        for line in entries:
            match = re.fullmatch(r'[-*] (PASS|FAIL|NOT RUN|PENDING): (\S.*)', line)
            if not match or (match[1]=='PENDING' and block['title']!='CI Verification'):
                errors.append('Use explicit evidence status and explanation: '+block['title'])
            elif block['title']=='Local Verification' and match[1] in ('PASS','FAIL'):
                if not re.search(r'`[^`]+`', line) or any(not re.search(r'\b'+key+r'=\d+\b',line) for key in ('passed','failed','skipped')):
                    errors.append('Executed local checks need command and passed/failed/skipped counts')
    for block in top:
        if block['title'] in SPEC['optional'] and not block['lines']:
            errors.append('Remove empty optional section: '+block['title'])
    if any(b['level'] not in (2,3) for b in sections):
        errors.append('Use level two sections and level three evidence categories')
    return {'passed': not errors, 'violations': errors, 'body_sha256': hashlib.sha256(body.encode()).hexdigest(), 'source_revision': pins[0] if len(pins)==1 else None, 'limits': 'Format and optional revision equality only; no proof of test truth, independent QA, CI success or publication authority.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--body-file',type=Path,required=True)
    parser.add_argument('--head',help='Full source SHA expected by the author; use current reviewed git HEAD')
    args=parser.parse_args(argv)
    try:
        if args.head is not None and not re.fullmatch(r'[0-9a-f]{40}',args.head): raise ValueError('Invalid --head')
        result=validate(args.body_file.read_text(), args.head)
    except (OSError,UnicodeError,ValueError):
        print(json.dumps({'passed':False,'error':'Unable to validate input'}));return 2
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
