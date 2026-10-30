"""Audit explicit public files, whole index or reachable history. Scans do not prove privacy."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from sdlc_io import regular_path,safe_relative

ROOT=Path(__file__).resolve().parents[1]
PATTERNS=(('private key',rb'-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----'),('GitHub credential',rb'\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{30,}\b'),('cloud credential',rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),('credential URL',rb'https?://[^\s/:]+:[^\s/@]+@'),('machine home path',rb'/(?:Users|home)/[A-Za-z0-9_.-]+/'))
NOREPLY=re.compile(r'(?:[0-9]+\+)?[A-Za-z0-9-]+@users\.noreply\.github\.com\Z')


def git(root,*args):
    result=subprocess.run(['git','--no-optional-locks','-C',str(root),*args],capture_output=True)
    if result.returncode:raise ValueError('Unable to inspect Git '+args[0])
    return result.stdout


def allowed_path(name,allowed):
    try:safe_relative(name)
    except ValueError:return False
    parts=Path(name).parts
    if any(x.casefold() in {'private','__pycache__','node_modules','.codex','.venv','.local'} or x.startswith('.venv') for x in parts):return False
    if any(x.casefold().startswith('.env') for x in parts):return False
    if Path(name).suffix.casefold() in {'.pem','.key','.db','.sqlite','.sqlite3','.p12','.pfx','.log','.zip','.pyc'}:return False
    return name in allowed


def content_issues(data):
    errors=[label for label,pattern in PATTERNS if re.search(pattern,data)]
    if b'\0' in data:errors.append('Unexpected binary data')
    if re.search(rb'''(?im)^\s*["']?(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)["']?\s*[:=]\s*["'][A-Za-z0-9/+_=-]{12,}["']''',data):errors.append('Possible literal credential')
    return errors


def audit(root=ROOT,mode='worktree'):
    root=Path(root);manifest=json.loads(regular_path(root,'PUBLIC_FILES.json').read_text());paths=manifest['paths']
    if not isinstance(paths,list) or any(not isinstance(x,str) for x in paths) or len(set(paths))!=len(paths):raise ValueError('Malformed public manifest')
    allowed=set(paths)
    if any(not allowed_path(n,allowed) for n in allowed):raise ValueError('Manifest contains forbidden private path')
    errors=[];seen=set()
    def inspect(name,data,origin,kind='100644'):
        key=(name,origin,kind)
        if key in seen:return
        seen.add(key)
        if not allowed_path(name,allowed):errors.append({'path':name,'reason':'Path outside reviewed public manifest or explicitly private'});return
        if kind not in ('100644','100755'):errors.append({'path':name,'reason':'Symlink, submodule or unresolved index mode'});return
        for reason in content_issues(data):errors.append({'path':name,'reason':reason})
    if mode=='worktree':
        candidates={x.decode() for x in git(root,'ls-files','--cached','--others','--exclude-standard','-z').split(b'\0') if x}
        for name in sorted(candidates|allowed):
            if not allowed_path(name,allowed):inspect(name,b'',name);continue
            try:
                path=regular_path(root,name);cursor=root
                for component in Path(name).parts:
                    if component not in {p.name for p in cursor.iterdir()}:raise ValueError('Path spelling differs')
                    cursor=cursor/component
                if not path.is_file() or path.stat().st_size>2*1024*1024:raise ValueError('Unsupported public file')
                inspect(name,path.read_bytes(),name)
            except (OSError,ValueError):errors.append({'path':name,'reason':'Missing, symlinked, unsafe or unsupported worktree file'})
    elif mode=='index':
        for entry in git(root,'ls-files','--stage','-z').split(b'\0'):
            if not entry:continue
            meta,raw=entry.split(b'\t',1);kind,oid,stage=meta.decode().split();name=raw.decode()
            inspect(name,git(root,'cat-file','blob',oid) if kind in ('100644','100755') and stage=='0' else b'',oid,kind if stage=='0' else 'unmerged')
    elif mode=='history':
        commits=git(root,'rev-list','--all').decode().splitlines()
        if not commits:raise ValueError('No reachable history to audit')
        for commit in commits:
            fields=git(root,'show','-s','--format=%ae%x00%ce%x00%B',commit).decode().split('\0',2)
            if not NOREPLY.fullmatch(fields[0]) or not (NOREPLY.fullmatch(fields[1]) or fields[1]=='noreply@github.com'):errors.append({'path':'(commit metadata)','reason':'Non-noreply commit identity'})
            for reason in content_issues(fields[2].encode()):errors.append({'path':'(commit message)','reason':reason})
            for entry in git(root,'ls-tree','-r','-z',commit).split(b'\0'):
                if not entry:continue
                meta,raw=entry.split(b'\t',1);kind,typ,oid=meta.decode().split();name=raw.decode()
                if (name,oid,kind) not in seen:inspect(name,git(root,'cat-file','blob',oid) if typ=='blob' else b'',oid,kind)
    else:raise ValueError('Unsupported mode')
    return {'passed':not errors,'mode':mode,'inspected_entries':len(seen),'violations':errors,'limits':'Path/pattern/mode/identity checks only. Manual provenance and content review remain necessary.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--mode',choices=['worktree','index','history'],required=True);args=parser.parse_args(argv)
    try:result=audit(args.root,args.mode)
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):print(json.dumps({'passed':False,'error':'Publication audit could not complete'}));return 2
    print(json.dumps(result,indent=2));return int(not result['passed'])


if __name__=='__main__':raise SystemExit(main())
