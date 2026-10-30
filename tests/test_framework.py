import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_framework as cf


class FrameworkTests(unittest.TestCase):
    def test_shipped_contracts_and_references(self):
        self.assertEqual(cf.check(), [])

    def test_project_additions_cannot_remove_profile_requirements(self):
        base = set(cf.effective_profile('STRICT'))
        self.assertTrue(base < set(cf.effective_profile('STRICT', ['project-required-smoke'])))
        for name in ('strict', '', 'CUSTOM'):
            with self.assertRaises(ValueError): cf.effective_profile(name)
        with self.assertRaises(ValueError): cf.effective_profile('LIGHT', [False])

    def test_missing_contract_and_broken_reference_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ('roles','profiles','core','workflows','templates'):
                shutil.copytree(cf.ROOT/name, root/name)
            (root/'roles/qa.md').write_text('# QA\n')
            (root/'core/policy.md').write_text('[missing](absent.md)\n')
            errors = cf.check(root)
            self.assertTrue(any('missing contract field' in x for x in errors))
            self.assertTrue(any('missing reference' in x for x in errors))

    def test_weakened_profile_and_domain_assumption_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in ('roles','profiles','core','workflows','templates'):
                shutil.copytree(cf.ROOT/name, root/name)
            f=root/'profiles/risk.json'; data=json.loads(f.read_text());data['STRICT']['requirements']=['scope'];f.write_text(json.dumps(data))
            (root/'core/domain.md').write_text('Use Decimal for finance.\n')
            errors=cf.check(root)
            self.assertTrue(any('STRICT' in x for x in errors))
            self.assertTrue(any('domain/stack' in x for x in errors))
