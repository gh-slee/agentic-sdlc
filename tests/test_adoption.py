import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import adopt
from sdlc_io import digest


def run_git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()


def fixture(root,custom=True):
    run_git(root,'init','-b','main');run_git(root,'config','user.name','Synthetic');run_git(root,'config','user.email','synthetic@example.invalid')
    (root/'AGENTS.md').write_text('Preserve existing instructions. No remote write without explicit authority.\n' if custom else 'Synthetic project instructions.\n')
    run_git(root,'add','AGENTS.md');run_git(root,'commit','-m','Synthetic baseline')


def report_for(root):
    discovery=adopt.discover(root);revision,version,_=adopt.baseline()
    refs=[dict(r,id='R'+str(i),revision=discovery['revision']) for i,r in enumerate(discovery['policies'])]
    return {'schema_version':'1.0.0','operation':'ADOPTION','source':{'repository':'synthetic/project','revision':discovery['revision']},'framework':{'version':version,'revision':revision},'inspected_refs':refs,'findings':[],'conflicts':[],'preserved_controls':['Existing project instructions remain unchanged.'],'proposed_modifications':[{'path':'.sdlc/agentic-sdlc','action':'ADD','reason':'Namespaced pinned baseline.','evidence':[refs[0]['id']]}],'risk':{'profile':'STANDARD','rationale':'Synthetic adoption mechanics test; semantic judgment is not being evaluated.'},'missing_information':[],'required_validation':['Compare original instructions byte-for-byte.'],'decision_status':'READY_FOR_REVIEW'}


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);fixture(self.root)
    def tearDown(self):self.temp.cleanup()
    def proposal(self):return adopt.plan(self.root,report_for(self.root))
    def apply(self,proposal,callback=None):
        data=adopt.encoded(proposal);return adopt.apply(self.root,data,digest(data),callback)

    def test_new_existing_and_repeat_preserve_local_instructions(self):
        before=(self.root/'AGENTS.md').read_bytes();proposal=self.proposal();self.assertEqual(self.apply(proposal)['result'],'INSTALLED')
        self.assertEqual((self.root/'AGENTS.md').read_bytes(),before)
        self.assertEqual(self.apply(proposal)['result'],'NOOP')
        self.assertEqual(self.proposal()['action'],'NOOP')
        manifest=json.loads((self.root/adopt.MANIFEST).read_text())
        self.assertEqual(manifest['framework_revision'],run_git(adopt.ROOT,'rev-parse','HEAD'))
        for name,expected in manifest['files'].items():self.assertEqual(digest((self.root/name).read_bytes()),expected)

    def test_conflicting_existing_skill_is_not_overwritten(self):
        path=self.root/'.agents/skills/sdlc-pr-write/SKILL.md';path.parent.mkdir(parents=True);path.write_text('Custom instructions')
        with self.assertRaises(ValueError):self.proposal()
        self.assertEqual(path.read_text(),'Custom instructions');self.assertFalse((self.root/adopt.MANIFEST).exists())

    def test_plan_change_and_stale_source_refuse_before_writes(self):
        proposal=self.proposal();data=adopt.encoded(proposal)
        with self.assertRaises(ValueError):adopt.apply(self.root,data,'0'*64)
        (self.root/'AGENTS.md').write_text('Changed rules')
        with self.assertRaises(ValueError):self.apply(proposal)
        self.assertFalse((self.root/'.sdlc').exists())

    def test_report_must_be_ready_and_bound_to_pinned_source(self):
        for field in ('decision','revision','evidence','framework'):
            r=report_for(self.root)
            if field=='decision':r['decision_status']='BLOCKED'
            if field=='revision':r['source']['revision']='0'*40
            if field=='evidence':r['inspected_refs'][0]['sha256']='0'*64
            if field=='framework':r['framework']['revision']='0'*40
            with self.assertRaises(ValueError):adopt.plan(self.root,r)

    def test_project_stronger_profile_and_additions_retained(self):
        path=self.root/'.sdlc/project.json';path.parent.mkdir();path.write_text(json.dumps({'profile':'STRICT','additional_requirements':['isolated-smoke'],'test_commands':['never-run-automatically']}))
        r=report_for(self.root)
        with self.assertRaises(ValueError):adopt.plan(self.root,r)
        r['risk']['profile']='STRICT';proposal=adopt.plan(self.root,r)
        self.assertIn('isolated-smoke',proposal['manifest']['requirements']);self.assertIn('independent_qa',proposal['manifest']['requirements'])
        self.apply(proposal);self.assertEqual(json.loads(path.read_text())['profile'],'STRICT')

    def test_symlink_ancestors_and_nested_target_refused(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root/'.sdlc').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):self.proposal()
            self.assertEqual(list(Path(outside).iterdir()),[])
        nested=self.root/'nested';nested.mkdir()
        with self.assertRaises(ValueError):adopt.discover(nested)

    def test_interrupted_apply_can_finish_matching_files(self):
        proposal=self.proposal();count=0
        def fail(name):
            nonlocal count
            count+=1
            if count==2:raise RuntimeError('Synthetic interruption')
        with self.assertRaises(RuntimeError):self.apply(proposal,fail)
        self.assertTrue((self.root/adopt.JOURNAL).is_file());self.assertFalse((self.root/adopt.MANIFEST).exists())
        self.assertEqual(self.apply(proposal)['result'],'INSTALLED');self.assertFalse((self.root/adopt.JOURNAL).exists())

    def test_partial_or_changed_file_and_different_pending_plan_refused(self):
        proposal=self.proposal()
        def fail(name):raise RuntimeError('Synthetic interruption')
        with self.assertRaises(RuntimeError):self.apply(proposal,fail)
        first=next(iter(sorted(proposal['files'])));(self.root/first).write_text('partial')
        with self.assertRaises(ValueError):self.apply(proposal)
        self.assertEqual((self.root/first).read_text(),'partial')
        (self.root/first).write_bytes(adopt.baseline()[2][first]);(self.root/adopt.JOURNAL).write_text('{}')
        with self.assertRaises(ValueError):self.apply(proposal)

    def test_changed_installed_file_or_baseline_requires_reviewed_manual_update(self):
        proposal=self.proposal();self.apply(proposal)
        name=next(iter(proposal['files']));(self.root/name).write_text('customized')
        with self.assertRaises(ValueError):self.proposal()
        self.assertEqual((self.root/name).read_text(),'customized')

    def test_no_executable_commands_or_report_path_can_change_plan_payload(self):
        proposal=self.proposal();proposal['files']['../escape']='0'*64
        with self.assertRaises(ValueError):self.apply(proposal)
        self.assertFalse((self.root/adopt.MANIFEST).exists())

    def test_non_directory_parent_and_changed_project_config_refused(self):
        (self.root/'.sdlc').write_text('existing file')
        with self.assertRaises(ValueError):self.proposal()
        (self.root/'.sdlc').unlink();(self.root/'.sdlc').mkdir()
        path=self.root/'.sdlc/project.json';path.write_text('{"invariants":["original"]}')
        proposal=self.proposal();path.write_text('{"invariants":["changed"]}')
        with self.assertRaises(ValueError):self.apply(proposal)
        self.assertFalse((self.root/adopt.MANIFEST).exists())
