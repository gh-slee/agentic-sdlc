"""Validate public PR event JSON without interpolating it into shell commands."""
import json
import os
from pathlib import Path
from check_pr import validate


def main():
    try:
        event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text());pr=event['pull_request']
        result=validate(pr.get('body') or '',pr['head']['sha'])
    except (OSError,KeyError,ValueError,TypeError):
        print('Unable to validate PR event');return 2
    print(json.dumps({'passed':result['passed'],'violations':result['violations']},indent=2))
    return int(not result['passed'])


if __name__=='__main__':raise SystemExit(main())
