import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import check_publication as guard
from sdlc_io import regular_path
from test_adoption import run_git


class SecurityTests(unittest.TestCase):
    def repo(self,root):
        run_git(root,'init','-b','main');run_git(root,'config','user.name','Synthetic');run_git(root,'config','user.email','synthetic@users.noreply.github.com')
        (root/'README.md').write_text('Synthetic public source.\n');(root/'PUBLIC_FILES.json').write_text(json.dumps({'paths':['README.md','PUBLIC_FILES.json']}))
        run_git(root,'add','.');run_git(root,'commit','-m','Synthetic public baseline')
    def test_safe_source_passes_all_modes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.repo(root)
            for mode in ('worktree','index','history'):self.assertTrue(guard.audit(root,mode)['passed'])
    def test_ignored_force_staged_private_file_blocked_by_full_index(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.repo(root);(root/'.gitignore').write_text('.local/\n');path=root/'.local';path.mkdir();(path/'private.txt').write_text('private local record')
            run_git(root,'add','--force','.local/private.txt');self.assertFalse(guard.audit(root,'index')['passed'])
    def test_deleted_secret_remains_in_reachable_history(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.repo(root);(root/'README.md').write_text('gh'+'p_'+'A'*32);run_git(root,'add','.');run_git(root,'commit','-m','Synthetic credential case')
            (root/'README.md').write_text('Removed synthetic marker');run_git(root,'add','.');run_git(root,'commit','-m','Synthetic removal')
            self.assertTrue(guard.audit(root,'index')['passed']);self.assertFalse(guard.audit(root,'history')['passed'])
    def test_private_paths_never_allowed_even_in_manifest(self):
        for name in ['.local/state.json','nested/AGENTS.override.md','.env.production','key.pem','../escape','.GIT/config']:
            self.assertFalse(guard.allowed_path(name,{name}))
    def test_symlink_modes_and_repeated_ancestors_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.repo(root);(root/'README.md').unlink();(root/'README.md').symlink_to('PUBLIC_FILES.json');run_git(root,'add','README.md')
            self.assertFalse(guard.audit(root,'index')['passed']);self.assertFalse(guard.audit(root,'worktree')['passed'])
            (root/'same').write_text('not a directory')
            with self.assertRaises(ValueError):regular_path(root,'same/same',True)
    def test_sensitive_content_and_commit_identity_checks(self):
        values=[('-----BEGIN '+'PRIVATE KEY-----').encode(),('https'+'://'+'name:credential@host.invalid').encode(),('/'+'/'.join(['Users','synthetic','private','file'])).encode(),('AK'+'IA'+'A'*16).encode()]
        for data in values:self.assertTrue(guard.content_issues(data))
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.repo(root);run_git(root,'config','user.email','private@example.invalid');(root/'README.md').write_text('Changed');run_git(root,'add','.');run_git(root,'commit','-m','Synthetic identity failure');self.assertFalse(guard.audit(root,'history')['passed'])
