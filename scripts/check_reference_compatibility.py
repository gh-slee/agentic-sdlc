"""Optional read-only source audit simulation. All writes stay in a disposable local copy."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from sdlc_io import digest

ROOT=Path(__file__).resolve().parents[1]


def run(args,cwd=None):
    return subprocess.run(args,cwd=cwd,capture_output=True)


def source_git(source,*args):
    result=run(['git','--no-optional-locks','-C',str(source),*args])
    if result.returncode:raise ValueError('Source inspection failed')
    return result.stdout


def check(source):
    provenance=json.loads((ROOT/'docs/audit/source-provenance.json').read_text())
    before=(source_git(source,'rev-parse','HEAD'),source_git(source,'status','--porcelain'))
    if before[0].decode().strip()!=provenance['revision']:raise ValueError('Source revision changed; revalidate audit')
    local=ROOT/'.local';local.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='compatibility-',dir=local) as d:
        target=Path(d)
        hashes={}
        for item in provenance['files']:
            data=source_git(source,'show',provenance['revision']+':'+item['path'])
            if digest(data)!=item['sha256']:raise ValueError('Source audit hash mismatch')
            path=target/item['path'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);hashes[item['path']]=digest(data)
        for args in (['init','-b','main'],['config','user.name','Synthetic'],['config','user.email','synthetic@users.noreply.github.com'],['add','.'],['commit','-m','Synthetic tracked workflow snapshot']):
            result=run(['git','-C',str(target),*args])
            if result.returncode:raise ValueError('Disposable setup failed')
        guard=['python3',str(target/'scripts/check_publication.py'),'--root',str(target),'--staged']
        initial=run(guard)
        if initial.returncode:raise ValueError('Source baseline guard did not pass')
        candidate=target/'.agents/skills/sdlc-adopt-review/SKILL.md';candidate.parent.mkdir(parents=True);candidate.write_text('---\nname: synthetic-sdlc-adopt-review\ndescription: Synthetic publication boundary probe.\n---\n\nDo not publish this probe.\n')
        staged=run(['git','-C',str(target),'add','--force',str(candidate)])
        if staged.returncode:raise ValueError('Disposable staging failed')
        result=run(guard)
        denied=json.loads(result.stdout)
        rejected=result.returncode==1 and any(v['path']=='.agents/skills/sdlc-adopt-review/SKILL.md' for v in denied['violations'])
        preserved=all(digest((target/name).read_bytes())==sha for name,sha in hashes.items())
        if not rejected or not preserved:raise ValueError('Compatibility preservation failed')
    after=(source_git(source,'rev-parse','HEAD'),source_git(source,'status','--porcelain'))
    if before!=after:raise ValueError('Source state changed during read-only check')
    return {'source_revision':provenance['revision'],'baseline_publication_guard':'PASS','candidate_skill_publication_guard':'REJECTED_AS_REQUIRED','original_workflow_files_preserved':len(hashes),'source_state_unchanged':True,'result':'BLOCKED_FOR_REAL_ADOPTION','reason':'New skill paths require deliberate project allowlist review; no source safeguards were weakened.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=Path,required=True);args=parser.parse_args()
    try:result=check(args.source)
    except (OSError,ValueError,KeyError):print(json.dumps({'passed':False,'error':'Compatibility check could not complete'}));return 2
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
