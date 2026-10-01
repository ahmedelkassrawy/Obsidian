"""Add an auto-generated 'Related' block to vault notes using local embeddings.

Usage:
  python related_links.py --dry  [--folder Database] [--show N]
  python related_links.py --write --folder Database
  python related_links.py --remove [--folder Database]
"""
import os, re, sys, argparse
import numpy as np

ROOT = r"D:\Obsidian\ME"
SKIP_DIRS = ('.git', '.obsidian', '_hubs', '_MOC', '_templates', 'tmp', 'Excalidraw', '.claude')
START = "%% related:start (auto-generated, regenerate with related_links.py) %%"
END = "%% related:end %%"
BLOCK_RE = re.compile(r"\n*%% related:start.*?%% related:end %%\n?", re.S)
K, FLOOR = 5, 0.45
CONCEPT_BONUS, RAW_PENALTY = 0.05, 0.06

ap = argparse.ArgumentParser()
ap.add_argument('--dry', action='store_true'); ap.add_argument('--write', action='store_true')
ap.add_argument('--remove', action='store_true'); ap.add_argument('--folder', default=None)
ap.add_argument('--show', type=int, default=0)
ap.add_argument('--exclude', nargs='*', default=['Concepts', '.'],
                help="top-level folders never written to ('.' = vault root files)")
a = ap.parse_args()

def top(path):
    rel = os.path.relpath(path, ROOT).split(os.sep)
    return rel[0] if len(rel) > 1 else '.'

def in_scope(path):
    if a.folder is not None:
        return top(path) == a.folder
    return top(path) not in a.exclude

notes = []
for r, d, fs in os.walk(ROOT):
    if any(s in r.split(os.sep) or s in r for s in SKIP_DIRS): continue
    for f in fs:
        if not f.endswith('.md') or f.startswith('_archived_') or f.startswith('_Concepts'): continue
        p = os.path.join(r, f)
        raw = open(p, encoding='utf8', errors='ignore', newline='').read()
        t = raw.replace('\r\n', '\n')
        m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
        fm, body = (m.group(1), m.group(2)) if m else ('', t)
        body = BLOCK_RE.sub('', body)
        desc = (re.search(r'description:\s*"?(.*?)"?\s*\n', fm) or [None, ''])[1]
        status = (re.search(r'status/(\w+)', fm) or [None, ''])[1]
        ntype = (re.search(r'type/(\w+)', fm) or [None, ''])[1]
        clean = re.sub(r'```.*?```', ' ', body, flags=re.S)
        clean = re.sub(r'!\[\[.*?\]\]|<[^>]+>|[#>*`|_-]{2,}', ' ', clean)
        notes.append(dict(title=f[:-3], path=p, folder=os.path.relpath(r, ROOT).split(os.sep)[0],
                          status=status, type=ntype, body=body,
                          text=f"{f[:-3]}. {desc}. {' '.join(clean.split())[:1200]}"))

if a.remove:
    n = 0
    for x in notes:
        if not in_scope(x['path']): continue
        raw = open(x['path'], encoding='utf8', newline='').read()
        new = BLOCK_RE.sub('\n', raw).rstrip() + ('\r\n' if '\r\n' in raw else '\n')
        if new != raw and START.split(' (')[0] in raw:
            open(x['path'], 'w', encoding='utf8', newline='').write(new); n += 1
    print('removed blocks from', n, 'notes'); sys.exit()

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
E = model.encode([x['text'] for x in notes], batch_size=64, normalize_embeddings=True, show_progress_bar=False)
S = E @ E.T
np.fill_diagonal(S, -1)

adj = np.zeros(len(notes))
for j, x in enumerate(notes):
    if x['type'] == 'zettel': adj[j] += CONCEPT_BONUS
    if x['status'] in ('raw', 'stub'): adj[j] -= RAW_PENALTY
    if x['status'] == 'empty': adj[j] = -9

def related(i):
    existing = {l.strip() for l in re.findall(r'\[\[([^\]|#]+)', notes[i]['body'])}
    scored = S[i] + adj
    out = []
    for j in np.argsort(-scored):
        if len(out) >= K or S[i, j] < FLOOR: break
        if notes[j]['title'] in existing or notes[j]['title'] == notes[i]['title']: continue
        out.append(j)
    return out

targets = [i for i, x in enumerate(notes) if in_scope(x['path']) and x['status'] != 'empty']
stats = dict(notes=len(targets), links=0, cross=0, zero=0)
shown = 0
for i in targets:
    rel = related(i)
    stats['links'] += len(rel); stats['zero'] += (not rel)
    stats['cross'] += sum(notes[j]['folder'] != notes[i]['folder'] for j in rel)
    if a.dry and shown < a.show:
        print(f"\n== {notes[i]['title']}")
        for j in rel: print(f"    {S[i,j]:.2f}  {notes[j]['title']}  [{notes[j]['folder']}]")
        shown += 1
    if a.write and rel:
        raw = open(notes[i]['path'], encoding='utf8', newline='').read()
        nl = '\r\n' if '\r\n' in raw else '\n'
        base = BLOCK_RE.sub('\n', raw.replace('\r\n', '\n')).rstrip()
        block = "\n".join([START, "## Related"] + [f"- [[{notes[j]['title']}]]" for j in rel] + [END])
        new = (base + "\n\n" + block + "\n").replace('\n', nl)
        if new != raw:
            open(notes[i]['path'], 'w', encoding='utf8', newline='').write(new)
print('\n', stats)
