"""Small shared path and digest primitives. Never evaluate analyzed repository text."""
import hashlib
from pathlib import Path, PurePosixPath


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(value):
    if not isinstance(value,str) or not value or '\\' in value or any(ord(c)<32 for c in value):
        raise ValueError('Unsafe repository-relative path')
    path=PurePosixPath(value)
    if path.is_absolute() or not path.parts or path.as_posix()!=value or any(x.casefold() in ('.','..','.git','.local') for x in path.parts):
        raise ValueError('Unsafe repository-relative path')
    if any(x.casefold() in ('agents.override.md','.env') for x in path.parts):
        raise ValueError('Private path excluded')
    return path


def regular_path(root,relative,allow_missing=False):
    safe_relative(relative)
    root=Path(root)
    if root.is_symlink() or not root.is_dir(): raise ValueError('Root must be a real directory')
    current=root
    parts=PurePosixPath(relative).parts
    for position,part in enumerate(parts):
        current=current/part
        if current.is_symlink(): raise ValueError('Symlink component refused')
        if current.exists() and position < len(parts)-1 and not current.is_dir(): raise ValueError('Non-directory ancestor refused')
        if not current.exists() and allow_missing: continue
        if not current.exists(): raise ValueError('Missing path')
    return current
