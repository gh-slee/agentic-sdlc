import contextlib
import io
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import check_pr as pr
GOOD=(pr.ROOT/'tests/fixtures/pr/valid.md').read_text()


class PRTests(unittest.TestCase):
    def test_valid_and_invalid_fixtures(self):
        self.assertTrue(pr.validate(GOOD)['passed'])
        self.assertFalse(pr.validate((pr.ROOT/'tests/fixtures/pr/invalid.md').read_text())['passed'])

    def test_missing_duplicate_reordered_and_nested_categories_fail(self):
        for body in (GOOD.replace('## Files Changed','## Other'), GOOD+ '\n## Change Summary\nDuplicate', GOOD.replace('### CI Verification','#### CI Verification'), GOOD.replace('### CI Verification','### Local Verification')):
            with self.subTest(body=body): self.assertFalse(pr.validate(body)['passed'])

    def test_hidden_headings_do_not_count(self):
        for body in ('```md\n'+GOOD+'\n```','~~~markdown\n'+GOOD+'\n~~~','<!--'+GOOD.replace('<!-- sdlc-head: 0000000000000000000000000000000000000000 -->','')+'-->'):
            self.assertFalse(pr.validate(body)['passed'])

    def test_fence_closure_requires_matching_character_and_length(self):
        body=GOOD.replace('## Files Changed','````md\n```\n## Files Changed')
        self.assertFalse(pr.validate(body)['passed'])

    def test_revision_and_body_digest_bind_exact_text(self):
        self.assertTrue(pr.validate(GOOD,'0'*40)['passed'])
        self.assertFalse(pr.validate(GOOD,'1'*40)['passed'])
        self.assertNotEqual(pr.validate(GOOD)['body_sha256'],pr.validate(GOOD+'\n')['body_sha256'])
        self.assertFalse(pr.validate(GOOD+'\n<!-- sdlc-head: '+'0'*40+' -->')['passed'])

    def test_executed_checks_need_command_counts_and_ci_pending_only(self):
        line='- NOT RUN: Format fixture only; no product tests are claimed.'
        for replacement in ('- PASS: Everything looks good.','- PENDING: Running tests.'):
            self.assertFalse(pr.validate(GOOD.replace(line,replacement))['passed'])
        body=GOOD.replace(line,'- PASS: `python -m unittest` passed=3 failed=0 skipped=0; synthetic shape claim only.')
        self.assertTrue(pr.validate(body)['passed'])
        self.assertIn('no proof',pr.validate(body)['limits'])
        self.assertTrue(pr.validate(GOOD.replace('- NOT RUN: Synthetic fixture has no CI run.','- PENDING: Example run in progress.'))['passed'])

    def test_optional_sections_need_content_and_order(self):
        self.assertFalse(pr.validate(GOOD+'\n## Rollback\n')['passed'])
        self.assertTrue(pr.validate(GOOD+'\n## Rollback\n\nRevert the reviewed change.\n')['passed'])
        self.assertFalse(pr.validate(GOOD+'\n## Rollback\nRevert.\n## Breaking Changes\nChanged.\n')['passed'])

    def test_cli_input_errors_and_template_is_not_a_finished_body(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(pr.main(['--body-file',str(pr.ROOT/'absent.md')]),2)
            self.assertEqual(pr.main(['--body-file',str(pr.ROOT/'tests/fixtures/pr/valid.md'),'--head','bad']),2)
        self.assertFalse(pr.validate((pr.ROOT/'templates/pull_request.md').read_text())['passed'])
