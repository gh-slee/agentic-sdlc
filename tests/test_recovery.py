import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import recover
from sdlc_io import digest
from test_adoption import fixture,run_git


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def setup_checkpoint(self,task='M3.1'):
        fixture(self.root)
        path=self.root/'docs/development';path.mkdir(parents=True)
        (path/'IMPLEMENTATION_STATE.md').write_text('Current task: '+task+'\nPrevious unit VERIFIED; completion requires evidence.\n')
        record={'schema_version':'1.0.0','current_task':task,'verified_tasks':['M0.1'],'anchor_revision':run_git(self.root,'rev-parse','HEAD'),'artifact_hashes':{'AGENTS.md':digest((self.root/'AGENTS.md').read_bytes())},'verification':{'command':'Synthetic recovery fixture consistency check (not product tests)','outcome':'PASS','passed':1,'failed':0,'skipped':0}}
        (path/'CHECKPOINT.json').write_text(json.dumps(record));run_git(self.root,'add','.');run_git(self.root,'commit','-m','Verified recovery fixture')
    def snapshot(self):
        return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file() and '.git' not in p.relative_to(self.root).parts}
    def check(self,action,remote=None):
        before=self.snapshot();history=run_git(self.root,'rev-parse','HEAD') if (self.root/'.git').exists() else None
        result=recover.diagnose(self.root,remote);self.assertEqual(result['action'],action);self.assertEqual(before,self.snapshot())
        if history:self.assertEqual(run_git(self.root,'rev-parse','HEAD'),history)
        return result

    def test_01_fresh_project_without_checkpoint(self):self.check('ESTABLISH_FOUNDATION')
    def test_02_partial_milestone_preserved(self):
        self.setup_checkpoint('M3.1');self.assertEqual(self.check('CONTINUE_TASK')['next_task'],'M3.1')
    def test_03_completed_unit_valid_git_evidence(self):
        self.setup_checkpoint('M4.1');self.assertEqual(self.check('CONTINUE_TASK')['next_task'],'M4.1')
    def test_04_dirty_worktree_after_interruption(self):
        self.setup_checkpoint();(self.root/'draft.txt').write_text('uncommitted work');self.check('INSPECT_DIRTY_WORKTREE')
    def test_05_false_completion_without_evidence(self):
        self.setup_checkpoint();path=self.root/'docs/development/CHECKPOINT.json';r=json.loads(path.read_text());r['artifact_hashes']={};path.write_text(json.dumps(r));run_git(self.root,'add','.');run_git(self.root,'commit','-m','Synthetic unsupported completion')
        self.check('REVALIDATE_COMPLETION')
    def test_06_interrupted_tests(self):
        self.setup_checkpoint();path=self.root/'.local';path.mkdir();(path/'test-running.json').write_text('{"status":"RUNNING"}');self.check('RECONCILE_INTERRUPTED_TEST')
    def test_07_interrupted_commit_preparation(self):
        self.setup_checkpoint();(self.root/'staged.txt').write_text('review before commit');run_git(self.root,'add','staged.txt');self.check('INSPECT_COMMIT_PREPARATION')
    def test_08_interrupted_adoption(self):
        self.setup_checkpoint();path=self.root/'.sdlc';path.mkdir();(path/'adoption-pending.json').write_text('{}');self.check('RECONCILE_ADOPTION')
    def test_09_missing_or_stale_state(self):
        self.setup_checkpoint();path=self.root/'docs/development/IMPLEMENTATION_STATE.md';path.write_text('Current task: M9.1');run_git(self.root,'add','.');run_git(self.root,'commit','-m','Synthetic stale notes');self.check('RECONSTRUCT_CHECKPOINT')
        path.unlink();run_git(self.root,'add','-u');run_git(self.root,'commit','-m','Synthetic missing state');self.check('RECONSTRUCT_CHECKPOINT')
    def test_10_remote_exists_push_incomplete(self):
        self.setup_checkpoint('M10.1');self.check('REVIEW_AUTHORIZED_INITIAL_PUSH',{'repository':'gh-slee/agentic-sdlc','authenticated':True,'exists':True,'visibility':'PUBLIC','default_branch':None,'head_sha':None})
    def test_11_push_complete_confirmation_interrupted(self):
        self.setup_checkpoint('M10.2');self.check('VERIFY_PUBLICATION_WITHOUT_REPEATING_PUSH',{'repository':'gh-slee/agentic-sdlc','authenticated':True,'exists':True,'visibility':'PUBLIC','default_branch':'main','head_sha':run_git(self.root,'rev-parse','HEAD')})
    def test_12_fresh_process_without_chat_context(self):
        self.setup_checkpoint('M8.2');result=subprocess.check_output([sys.executable,str(Path(recover.__file__)),'--root',str(self.root)])
        self.assertEqual(json.loads(result)['next_task'],'M8.2');self.assertEqual(json.loads(result)['action'],'CONTINUE_TASK')
    def test_unknown_remote_and_divergence_never_grant_write(self):
        self.setup_checkpoint('M10.1');self.check('INSPECT_REMOTE',{'exists':False})
        self.check('REVIEW_REMOTE_DIVERGENCE',{'repository':'gh-slee/agentic-sdlc','authenticated':True,'exists':True,'visibility':'PUBLIC','default_branch':'main','head_sha':'0'*40})
    def test_changed_artifact_and_failed_verification_invalidate_done(self):
        self.setup_checkpoint();(self.root/'AGENTS.md').write_text('Changed after verification');run_git(self.root,'add','.');run_git(self.root,'commit','-m','Synthetic changed artifact');self.check('REVALIDATE_COMPLETION')

import sys
