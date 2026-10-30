"""Structural governance checks; these do not authenticate agent behavior or consent."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ROLE_FIELDS = ('Purpose', 'Activation criteria', 'Inputs', 'Outputs', 'Responsibilities', 'Permissions', 'Prohibited actions', 'Decision authority', 'Handoff format', 'Completion criteria', 'Escalation conditions')
PROFILES = ('LIGHT', 'STANDARD', 'STRICT')


def effective_profile(name, additional=()):
    profiles = json.loads((ROOT / 'profiles/risk.json').read_text())
    if name not in PROFILES or not isinstance(additional, (tuple, list)) or any(not isinstance(x, str) or not x.strip() for x in additional):
        raise ValueError('Unknown profile or invalid additional requirements')
    return sorted(set(profiles[name]['requirements']) | set(additional))


def check(root=ROOT):
    errors = []
    roles = ('requirements', 'architect', 'developer', 'qa', 'coordinator')
    for name in roles:
        path = root / 'roles' / (name + '.md')
        if not path.is_file():
            errors.append('Missing role: ' + name)
            continue
        text = path.read_text()
        for field in ROLE_FIELDS:
            if not re.search(r'^## ' + re.escape(field) + r'\n\n\S', text, re.M):
                errors.append(name + ': missing contract field ' + field)
    try:
        profiles = json.loads((root / 'profiles/risk.json').read_text())
        if set(profiles) != set(PROFILES):
            errors.append('Expected exactly three risk profiles')
        previous = set()
        for name in PROFILES:
            requirements = set(profiles[name]['requirements'])
            if not previous <= requirements or not requirements:
                errors.append('Profiles must retain requirements as rigor increases')
            previous = requirements
        if not {'human_gates', 'independent_qa', 'security_review', 'rollback', 'exact_spec'} <= previous:
            errors.append('STRICT missing mandatory safeguards')
    except (OSError, ValueError, KeyError, TypeError):
        errors.append('Malformed profiles')
    for folder in ('core', 'roles', 'workflows'):
        for path in (root / folder).glob('*.md'):
            text = path.read_text()
            if re.search(r'wealth.?ledger|Decimal|SQLite|PostgreSQL|BTC|FastAPI|React|finance', text, re.I):
                errors.append(str(path.relative_to(root)) + ': domain/stack assumption')
            for target in re.findall(r'\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)', text):
                if '://' not in target and not (path.parent / target).is_file():
                    errors.append(str(path.relative_to(root)) + ': missing reference ' + target)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = check()
    print(json.dumps({'passed': not errors, 'violations': errors, 'limits': 'Structure and configured requirements only; no proof of consent or agent compliance.'}, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
