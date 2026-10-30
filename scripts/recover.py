"""Read-only recovery diagnostic for this framework's initial implementation. Never retries writes."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from sdlc_io import digest,regular_path

CHECKPOINT='docs/development/CHECKPOINT.json'
STATE='docs/development/IMPLEMENTATION_STATE.md'


def git(root,*args):return subprocess.run(['git','--no-optional-locks','-C',str(root),*args],capture_output=True)


def diagnose(root,remote=None):
    root=Path(root)
    result={'action':None,'issues':[],'head':None,'branch':None,'dirty':None,'limits':'Read-only consistency diagnostic; cannot authenticate test claims, human approval or supplied remote observations.'}
    def finish(action,issue=None):
        result['action']=action
        if issue:result['issues'].append(issue)
        return result
    top=git(root,'rev-parse','--show-toplevel')
    if top.returncode:return finish('ESTABLISH_FOUNDATION','No Git root; inspect existing files before initialization')
    if Path(top.stdout.decode().strip()).resolve()!=root.resolve():return finish('SELECT_CORRECT_ROOT','Nested directory is not the intended repository root')
    head=git(root,'rev-parse','--verify','HEAD');result['head']=head.stdout.decode().strip() if head.returncode==0 else None
    result['branch']=git(root,'branch','--show-current').stdout.decode().strip()
    status=git(root,'status','--porcelain','-z')
    if status.returncode:return finish('INSPECT_GIT_FAILURE')
    result['dirty']=bool(status.stdout)
    # Do not retry/clear an operation or free an ownership claim automatically.
    for marker,action in (('.local/test-running.json','RECONCILE_INTERRUPTED_TEST'),('.git/index.lock','INSPECT_COMMIT_PREPARATION'),('.local/commit-preparing.json','INSPECT_COMMIT_PREPARATION'),('.sdlc/adoption-pending.json','RECONCILE_ADOPTION')):
        path=root/marker
        if path.exists() or path.is_symlink():return finish(action,'Inspect the marker and live processes; never delete it blindly')
    staged=git(root,'diff','--cached','--name-only','-z')
    if staged.returncode:return finish('INSPECT_GIT_FAILURE')
    if staged.stdout:return finish('INSPECT_COMMIT_PREPARATION','Review staged scope and history before creating another commit')
    if result['dirty']:return finish('INSPECT_DIRTY_WORKTREE','Preserve all changes and reconcile them with the checkpoint')
    try:
        state_path=regular_path(root,STATE);state=state_path.read_text()
        checkpoint=json.loads(regular_path(root,CHECKPOINT).read_text())
    except (OSError,ValueError):return finish('RECONSTRUCT_CHECKPOINT','State or structured evidence is missing or malformed; do not trust DONE labels')
    required={'schema_version','current_task','verified_tasks','anchor_revision','artifact_hashes','verification'}
    if not isinstance(checkpoint,dict) or set(checkpoint)!=required or checkpoint['schema_version']!='1.0.0':return finish('RECONSTRUCT_CHECKPOINT','Unsupported checkpoint shape')
    anchor=checkpoint['anchor_revision']
    if not isinstance(anchor,str) or not re.fullmatch('[0-9a-f]{40}',anchor) or git(root,'cat-file','-e',anchor+'^{commit}').returncode or git(root,'merge-base','--is-ancestor',anchor,'HEAD').returncode:return finish('RECONSTRUCT_CHECKPOINT','Recorded commit is not a verified ancestor of HEAD')
    if not isinstance(checkpoint['artifact_hashes'],dict) or not checkpoint['artifact_hashes']:return finish('REVALIDATE_COMPLETION','Completion lacks artifact evidence')
    try:
        for name,expected in checkpoint['artifact_hashes'].items():
            if not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected) or digest(regular_path(root,name).read_bytes())!=expected:return finish('REVALIDATE_COMPLETION','Artifact missing or changed; notes cannot establish completion')
    except (OSError,ValueError):return finish('REVALIDATE_COMPLETION','Unsafe or missing evidence path')
    verification=checkpoint['verification']
    if not isinstance(verification,dict) or verification.get('outcome')!='PASS' or not isinstance(verification.get('command'),str) or not verification['command'].strip() or any(type(verification.get(k)) is not int or verification[k]<0 for k in ('passed','failed','skipped')) or verification['failed']!=0 or verification['passed']<1:return finish('REVALIDATE_COMPLETION','Verification is absent, incomplete or unsuccessful')
    task=checkpoint['current_task']
    if not isinstance(task,str) or not re.fullmatch(r'M\d+\.\d+|COMPLETE',task) or task not in state:return finish('RECONSTRUCT_CHECKPOINT','State and checkpoint task disagree')
    result['next_task']=task
    if remote is not None:
        if not isinstance(remote,dict) or remote.get('repository')!='gh-slee/agentic-sdlc' or remote.get('authenticated') is not True or type(remote.get('exists')) is not bool:return finish('INSPECT_REMOTE','Missing authenticated target-specific observation; unknown is not absent')
        if not remote['exists']:return finish('REVIEW_AUTHORIZED_CREATE','Confirm release gates and standing scope before the incomplete create step')
        if remote.get('visibility')!='PUBLIC' or remote.get('default_branch') not in ('main',None):return finish('REVIEW_REMOTE_CONFLICT','Never overwrite an unexpected remote')
        if remote.get('head_sha') is None:return finish('REVIEW_AUTHORIZED_INITIAL_PUSH','Remote already exists; inspect branches and push only if authorized, never create again')
        if remote['head_sha']==result['head']:return finish('VERIFY_PUBLICATION_WITHOUT_REPEATING_PUSH','Matching remote commit observed; verify metadata/files/checks and update state')
        return finish('REVIEW_REMOTE_DIVERGENCE','Compare ancestry and identity; never force-push to reconcile')
    if task.startswith('M10'):return finish('INSPECT_REMOTE','Publication phase requires actual remote inspection before create/push')
    return finish('CONTINUE_TASK' if task!='COMPLETE' else 'CHECKPOINT_CONSISTENT')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path.cwd());parser.add_argument('--remote-observation',type=Path);args=parser.parse_args()
    try:
        remote=json.loads(args.remote_observation.read_text()) if args.remote_observation else None
        result=diagnose(args.root,remote)
    except (OSError,ValueError,TypeError,KeyError):
        print(json.dumps({'action':'INSPECT_UNREADABLE_STATE','limits':'No writes attempted; preserve existing work.'}));return 2
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
