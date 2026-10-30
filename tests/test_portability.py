import json
from pathlib import Path
import shutil
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import adopt
from sdlc_io import digest
from test_adoption import fixture,report_for,run_git


class PortabilityTests(unittest.TestCase):
    def exercise(self,name):
        original=adopt.ROOT/'tests/fixtures/projects'/name
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            shutil.copytree(original,root,dirs_exist_ok=True)
            fixture(root)
            # Restore the fixture's custom instructions after helper initialization.
            shutil.copyfile(original/'AGENTS.md',root/'AGENTS.md')
            run_git(root,'add','.');run_git(root,'commit','-m','Project-specific fixture')
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}
            report=report_for(root);config=json.loads((root/'.sdlc/project.json').read_text());report['risk']['profile']=config['profile']
            proposal=adopt.plan(root,report);data=adopt.encoded(proposal)
            self.assertEqual(adopt.apply(root,data,digest(data))['result'],'INSTALLED')
            self.assertEqual(adopt.apply(root,data,digest(data))['result'],'NOOP')
            for name,content in before.items():self.assertEqual((root/name).read_bytes(),content)
            self.assertIn('preserve-project-invariants',proposal['manifest']['requirements'])
            # Each unrelated repository receives exactly the same core content.
            for name,content in adopt.baseline()[2].items():self.assertEqual((root/name).read_bytes(),content)

    def test_python_cli(self):self.exercise('python-cli')
    def test_react_typescript(self):self.exercise('react-app')
    def test_backend_api(self):self.exercise('backend-api')
    def test_infrastructure(self):self.exercise('infrastructure')
    def test_documentation_only(self):self.exercise('documentation')
