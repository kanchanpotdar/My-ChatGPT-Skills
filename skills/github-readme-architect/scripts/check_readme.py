#!/usr/bin/env python3
"""Read-only bounded inventory and Markdown checks. Python standard library only."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = {'.git', '.venv', 'venv', 'env', 'node_modules', '__pycache__',
        '.cache', 'dist', 'build', '.next', 'vendor', 'target'}
SENSITIVE = re.compile(r'(^\.env($|\.)|credentials|\.pem$|\.key$|^id_rsa$)', re.I)


def inside(path, root):
    return path.resolve().is_relative_to(root)


def inventory(root):
    """Git honors ignore rules. Non-Git fallback requires rg to honor ignore files."""
    probe = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                           capture_output=True, text=True)
    if probe.returncode == 0 and Path(probe.stdout.strip()).resolve() == root:
        result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--cached',
                                 '--others', '--exclude-standard'], capture_output=True)
        method = 'git ls-files (tracked and non-ignored untracked)'
    else:
        try:
            result = subprocess.run(['rg', '--files', '--hidden', '--no-require-git', '-0', str(root)],
                                    capture_output=True)
        except FileNotFoundError:
            return [], 'unavailable: non-Git inventory requires rg; no unsafe fallback'
        method = 'rg --files --hidden (ignore-aware; no symlink traversal)'
    if result.returncode not in (0, 1):
        return [], 'inventory command failed'
    paths = []
    for raw in result.stdout.decode('utf-8', errors='replace').split('\0'):
        if not raw:
            continue
        p = Path(raw)
        p = p if p.is_absolute() else root / p
        if not inside(p, root):
            continue
        rel = p.relative_to(root)
        if any(part in SKIP or SENSITIVE.search(part) for part in rel.parts):
            continue
        paths.append(rel.as_posix())
    return sorted(set(paths)), method


def prose(text):
    """Mask fenced and inline code before extracting ordinary Markdown links."""
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append('' if fence else re.sub(r'`+[^`]*`+', '', line))
    return '\n'.join(lines), fence is not None


def check(root, readme):
    if not inside(readme, root) or not readme.is_file():
        raise ValueError('README must be an existing file inside the repository')
    if readme.stat().st_size > 2_000_000:
        raise ValueError('README exceeds 2 MB inspection limit')
    text = readme.read_text(encoding='utf-8')
    clean, unclosed = prose(text)
    findings = []
    if unclosed:
        findings.append({'kind': 'fence', 'line': None, 'detail': 'Unclosed code fence'})
    # Report location and type only: never echo potentially sensitive lines or values.
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
                r'\bAKIA[A-Z0-9]{16}\b',
                r'(?i)\b(?:api[_-]?key|password|secret|token)\s*[:=]\s*["\x27]?[A-Za-z0-9_+/=-]{20,}']
    for number, line in enumerate(text.splitlines(), 1):
        if any(re.search(pattern, line) for pattern in patterns):
            findings.append({'kind': 'secret-review', 'line': number,
                             'detail': 'Possible credential; inspect privately (value redacted)'})
    definitions = {}
    for m in re.finditer(r'^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)', clean, re.M):
        definitions[m.group(1).casefold()] = m.group(2).strip('<>')
    links = []
    # Handles ordinary inline paths, including balanced parentheses one level deep.
    for m in re.finditer(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|(?:[^\s()]|\([^()]*\))+)(?:\s+["\x27].*?["\x27])?\s*\)', clean):
        links.append((m.start(), m.group(1).strip('<>')))
    for m in re.finditer(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]', clean):
        key = (m.group(2) or m.group(1)).casefold()
        if key in definitions:
            links.append((m.start(), definitions[key]))
        else:
            findings.append({'kind': 'reference', 'line': clean.count('\n', 0, m.start()) + 1,
                             'detail': 'Undefined Markdown reference'})
    checked = external = anchors = 0
    for pos, target in links:
        url = urlsplit(target)
        if url.scheme or url.netloc:
            external += 1
            continue
        if not url.path:
            anchors += bool(url.fragment)
            continue
        # GitHub leading-slash links resolve relative to the repository root.
        path = (root / unquote(url.path).lstrip('/') if url.path.startswith('/')
                else readme.parent / unquote(url.path))
        checked += 1
        if not inside(path, root):
            detail = 'Local target escapes repository boundary'
        elif not path.exists():
            detail = 'Local target does not exist'
        else:
            continue
        findings.append({'kind': 'path', 'line': clean.count('\n', 0, pos) + 1,
                         'detail': detail})
    return {'local_paths_checked': checked, 'external_links_not_requested': external,
            'same_document_anchor_links_not_validated': anchors, 'findings': findings,
            'limits': ['Heuristic Markdown parser; review HTML, shortcut references, complex links and anchors manually.',
                       'No external requests, command execution, metric verification, or Mermaid rendering.',
                       'Secret patterns are incomplete and can flag placeholders; a clean scan is not a privacy guarantee.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--readme', default='README.md', help='Path relative to root')
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--limit', type=int, default=150)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        report = check(root, root / args.readme)
        if args.inventory:
            files, method = inventory(root)
            report['inventory'] = {'method': method, 'count': len(files),
                                   'paths': files[:max(0, args.limit)],
                                   'truncated': len(files) > max(0, args.limit)}
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report['findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
