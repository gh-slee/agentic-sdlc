"""Validate the fixed local Draft 2020-12 schema and cross-field consistency."""
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sdlc_io import safe_relative

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/'schemas/review-v1.schema.json').read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR=Draft202012Validator(SCHEMA)
ADOPTION={'UNIVERSAL_CORE','GENERIC_CONFIGURABLE','OPTIONAL_WORKFLOW','TOOL_INTEGRATION','PROJECT_SPECIFIC','DOMAIN_SPECIFIC','PRIVATE_LOCAL','CONFLICTING_OR_LEGACY'}
UPSTREAM={'UNIVERSAL_IMPROVEMENT','OPTIONAL_CAPABILITY','TOOL_ADAPTER_IMPROVEMENT','FRAMEWORK_BUG_FIX','PROJECT_SPECIFIC','DOMAIN_SPECIFIC','SECURITY_REGRESSION','CONFLICTING_CHANGE','NO_REUSABLE_CHANGE','NEEDS_REVIEW'}


def validate(report):
    errors=['Schema violation at '+('/'.join(map(str,e.absolute_path)) or 'root') for e in VALIDATOR.iter_errors(report)]
    if errors: return errors
    refs={ref['id']:ref for ref in report['inspected_refs']}
    if len(refs)!=len(report['inspected_refs']):errors.append('Duplicate source reference ID')
    ids=[f['id'] for f in report['findings']]
    if len(set(ids))!=len(ids):errors.append('Duplicate finding ID')
    allowed=ADOPTION if report['operation']=='ADOPTION' else UPSTREAM
    for ref in report['inspected_refs']:
        try: safe_relative(ref['path'])
        except ValueError:errors.append('Unsafe inspected source path')
        if ref['revision']!=report['source']['revision']:errors.append('Source reference revision differs from report source')
    for finding in report['findings']:
        if finding['classification'] not in allowed:errors.append('Classification invalid for operation')
    for item in report['findings']+report['proposed_modifications']:
        if any(e not in refs for e in item['evidence']):errors.append('Unknown source evidence reference')
    for change in report['proposed_modifications']:
        if change['path']=='@discovery':errors.append('Discovery receipt is not a writable repository path')
        try:safe_relative(change['path'])
        except ValueError:errors.append('Unsafe proposed modification path')
    blocking=any(c['blocking'] for c in report['conflicts']) or any(f['classification']=='SECURITY_REGRESSION' for f in report['findings'])
    if blocking and report['decision_status']!='BLOCKED':errors.append('Blocking conflict or security regression must remain BLOCKED')
    if report['missing_information'] and report['decision_status']=='READY_FOR_REVIEW':errors.append('Missing information prevents readiness')
    return errors


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('report',type=Path);args=parser.parse_args(argv)
    try:
        report=json.loads(args.report.read_text());errors=validate(report)
    except (OSError,UnicodeError,ValueError):
        print(json.dumps({'passed':False,'error':'Unable to validate report'}));return 2
    print(json.dumps({'passed':not errors,'violations':errors,'limits':'Shape and internal consistency only; source authenticity, semantic equivalence and human authority require review.'},indent=2))
    return int(bool(errors))


if __name__=='__main__':raise SystemExit(main())
