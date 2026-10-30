import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import check_pr_event
from test_pr import GOOD


class PREventTests(unittest.TestCase):
    def test_event_uses_branch_head_and_treats_text_as_data(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'event.json';path.write_text(json.dumps({'pull_request':{'body':GOOD,'head':{'sha':'0'*40}}}))
            with patch.dict(os.environ,{'GITHUB_EVENT_PATH':str(path)}),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check_pr_event.main(),0)
                path.write_text(json.dumps({'pull_request':{'body':GOOD,'head':{'sha':'1'*40}}}))
                self.assertEqual(check_pr_event.main(),1)
    def test_unreadable_event_fails_closed(self):
        with patch.dict(os.environ,{'GITHUB_EVENT_PATH':'missing-event.json'}),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_pr_event.main(),2)
