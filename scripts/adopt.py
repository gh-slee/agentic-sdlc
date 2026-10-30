"""Read-only discovery/planning, then explicitly reviewed add-only adoption. No model calls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from check_report import validate
from sdlc_io import digest, regular_path, safe_relative

ROOT=Path(__file__).resolve().parents[1]
VENDOR='.sdlc/agentic-sdlc/'
MANIFEST='.sdlc/install.json'
JOURNAL='.sdlc/adoption-pending.json'
DISTRIBUTED=('core/','roles/','profiles/','workflows/','templates/','schemas/','scripts/','.agents/skills/')
ROOT_FILES={'VERSION','LICENSE','NOTICE','THIRD_PARTY_NOTICES.md','requirements.lock'}


def encoded(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()


def git(root,*args):
    result=subprocess.run(['git','-C',str(root),*args],capture_output=True)
    if result.returncode:raise ValueError('Git inspection failed: '+args[0])
    return result.stdout


def repository(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir() or root.resolve()!=Path(git(root,'rev-parse','--show-toplevel').decode().strip()).resolve():
        raise ValueError('Use an existing repository root, not a nested directory or symlink')
    return root


def discover(target):
    target=repository(target)
    revision=git(target,'rev-parse','HEAD').decode().strip()
    refs=[]
    for raw in git(target,'ls-files','-z').split(b'\0'):
        if not raw:continue
        name=raw.decode('utf-8')
        # Do not read application data, ignored overrides or arbitrary source files.
        selected=(name.endswith('/AGENTS.md') or name in ('AGENTS.md','CONTRIBUTING.md','SECURITY.md','.gitignore','.sdlc/project.json') or name.startswith('.agents/skills/') and name.endswith('/SKILL.md') or name.startswith('.github/') and name.endswith(('.md','.yml','.yaml')) or name.startswith('docs/') and any(t in name.casefold() for t in ('agent','spec','develop','publish','security','governance')))
        if not selected:continue
        path=regular_path(target,name)
        if not path.is_file() or path.stat().st_size>1024*1024:raise ValueError('Unsupported policy file')
        refs.append({'path':name,'sha256':digest(path.read_bytes())})
    return {'revision':revision,'policies':sorted(refs,key=lambda r:r['path']),'limits':'Tracked public policy files only; no semantic interpretation or ignored/private instructions.'}


def baseline():
    root=repository(ROOT);revision=git(root,'rev-parse','HEAD').decode().strip()
    entries={}
    for line in git(root,'ls-tree','-r','-z',revision).split(b'\0'):
        if not line:continue
        meta,raw=line.split(b'\t',1);name=raw.decode();mode,kind,oid=meta.decode().split()
        if name not in ROOT_FILES and not name.startswith(DISTRIBUTED):continue
        safe_relative(name)
        if mode!='100644' or kind!='blob':raise ValueError('Baseline contains non-regular distribution file')
        data=git(root,'cat-file','blob',oid)
        entries[VENDOR+name]=data
        if name.startswith('.agents/skills/'):
            entries[name]=data
    version=git(root,'show',revision+':VERSION').decode().strip()
    return revision,version,entries


def project_config(target):
    path=regular_path(target,'.sdlc/project.json',True)
    if not path.exists():return {}
    value=json.loads(path.read_text())
    allowed={'profile','additional_requirements','test_commands','invariants'}
    if not isinstance(value,dict) or set(value)-allowed:raise ValueError('Unknown project configuration field')
    if value.get('profile','STANDARD') not in ('LIGHT','STANDARD','STRICT'):raise ValueError('Invalid project profile')
    for key in allowed-{'profile'}:
        if key in value and (not isinstance(value[key],list) or any(not isinstance(x,str) or not x.strip() for x in value[key])):raise ValueError('Invalid project configuration value')
    return value


def plan(target,report):
    target=repository(target);discovery=discover(target)
    errors=validate(report)
    if errors or report['operation']!='ADOPTION' or report['decision_status']!='READY_FOR_REVIEW':raise ValueError('A valid review-ready adoption report is required')
    revision,version,files=baseline()
    if report['source']['revision']!=discovery['revision'] or report['framework']!={'version':version,'revision':revision}:raise ValueError('Stale source or framework revision')
    observed={r['path']:r['sha256'] for r in discovery['policies']}
    for ref in report['inspected_refs']:
        if observed.get(ref['path'])!=ref['sha256']:raise ValueError('Source evidence missing or changed')
    config=project_config(target);profile=report['risk']['profile'];ranks={'LIGHT':0,'STANDARD':1,'STRICT':2}
    if ranks[profile]<ranks[config.get('profile','LIGHT')]:raise ValueError('Cannot weaken project profile')
    manifest={'schema_version':'1.0.0','framework_source_version':version,'installed_version':version,'framework_revision':revision,'adapter_version':'codex-1','profile':profile,'requirements':sorted(set(json.loads(files[VENDOR+'profiles/risk.json']) [profile]['requirements']) | set(config.get('additional_requirements',[]))),'files':{k:digest(v) for k,v in sorted(files.items())}}
    for name,data in files.items():
        path=regular_path(target,name,True)
        if path.exists() and (not path.is_file() or path.read_bytes()!=data):raise ValueError('Existing file conflict: '+name)
    path=regular_path(target,MANIFEST,True);action='INSTALL'
    if path.exists():
        if not path.is_file() or path.read_bytes()!=encoded(manifest):raise ValueError('Installed provenance differs; manual reviewed update required')
        if any(not regular_path(target,n,True).exists() for n in files):raise ValueError('Installed file missing; inspect before recovery')
        action='NOOP'
    return {'plan_version':'1.0.0','action':action,'source_revision':discovery['revision'],'framework_revision':revision,'report':report,'discovery':discovery,'project_config_sha256':digest(encoded(config)),'manifest':manifest,'files':manifest['files'],'limits':'Add-only; never edits existing instructions, authorizes policy changes, executes project commands or automates upgrades.'}


def write_new(root,name,data):
    # Directory-relative no-follow traversal prevents writes through symlink ancestors.
    safe_relative(name)
    flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
    fd=os.open(root,flags)
    try:
        parts=name.split('/')
        for part in parts[:-1]:
            try:os.mkdir(part,dir_fd=fd)
            except FileExistsError:pass
            next_fd=os.open(part,flags,dir_fd=fd);os.close(fd);fd=next_fd
        try:out=os.open(parts[-1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=fd)
        except FileExistsError:
            path=regular_path(root,name)
            if not path.is_file() or path.read_bytes()!=data:raise ValueError('Existing file changed: '+name)
            return False
        with os.fdopen(out,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        return True
    finally:os.close(fd)


def apply(target,reviewed_bytes,reviewed_digest,after_write=None):
    if digest(reviewed_bytes)!=reviewed_digest:raise ValueError('Reviewed plan digest differs')
    proposal=json.loads(reviewed_bytes)
    current=plan(target,proposal['report'])
    comparable=dict(current);comparable['action']=proposal.get('action')
    if comparable!=proposal:raise ValueError('Reviewed plan differs from current state')
    journal=regular_path(target,JOURNAL,True)
    record=encoded({'plan_sha256':reviewed_digest,'source_revision':current['source_revision'],'framework_revision':current['framework_revision']})
    if journal.exists() and journal.read_bytes()!=record:raise ValueError('Different or partial adoption is pending; inspect before retry')
    if current['action']=='NOOP':
        if journal.exists():journal.unlink()
        return {'result':'NOOP','written':0}
    write_new(target,JOURNAL,record)
    revision,version,files=baseline()
    if revision!=current['framework_revision']:raise ValueError('Baseline changed during apply')
    written=0
    for name,data in sorted(files.items()):
        written+=write_new(target,name,data)
        if after_write:after_write(name)
    # Final receipt is written only after all desired bytes have been checked.
    for name,data in files.items():
        if regular_path(target,name).read_bytes()!=data:raise ValueError('Post-write validation failed')
    write_new(target,MANIFEST,encoded(current['manifest']))
    journal.unlink()
    return {'result':'INSTALLED','written':written,'framework_revision':revision}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for command in ('discover','plan','apply'):
        item=sub.add_parser(command);item.add_argument('--target',type=Path,required=True)
        if command=='plan':item.add_argument('--report',type=Path,required=True)
        if command=='apply':item.add_argument('--plan-file',type=Path,required=True);item.add_argument('--reviewed-plan-sha256',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='discover':result=discover(args.target)
        elif args.command=='plan':result=plan(args.target,json.loads(args.report.read_text()))
        else:result=apply(args.target,args.plan_file.read_bytes(),args.reviewed_plan_sha256)
        print(encoded(result).decode(),end='');return 0
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):
        print(json.dumps({'passed':False,'error':'Adoption refused; inspect report, revisions, paths, existing files and pending journal. No existing file was intentionally replaced.'}));return 2


if __name__=='__main__':raise SystemExit(main())
