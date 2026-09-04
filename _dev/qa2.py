import re, sys, importlib.util, collections, glob, html
import os, pathlib
os.chdir(pathlib.Path(__file__).resolve().parent.parent)  # repo root
spec = importlib.util.spec_from_file_location("g", "_dev/generate.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

issues = collections.defaultdict(list)
REQ = ["slug","name","pillar","purpose","steps","meta","sideways","short_use"]
slugs = set()
for t in g.TECHNIQUES:
    for k in REQ:
        if not t.get(k): issues['missing field'].append(f"{t.get('slug')}: {k}")
    if t["slug"] in slugs: issues['duplicate slug'].append(t["slug"])
    slugs.add(t["slug"])
    if len(t["meta"]) != 3: issues['meta not 3 parts'].append(t["slug"])
    for i, st in enumerate(t["steps"], 1):
        if not st.rstrip().endswith(('.', '?', '!', ':')):
            issues['step no end punctuation'].append(f"{t['slug']} {i:02d}: {st[-40:]}")
        if '  ' in st: issues['double space'].append(f"{t['slug']} {i:02d}")
    for fld in ("purpose","note","note2","note3","sideways","progression"):
        v = t.get(fld)
        if isinstance(v,str):
            if '  ' in v: issues['double space'].append(f"{t['slug']} {fld}")
            if not v.rstrip().endswith(('.','?','!')): issues['no end punctuation'].append(f"{t['slug']} {fld}")
    if not t["name"][0].isupper(): issues['name case'].append(t["slug"])
    vids = [v[2] for v in t.get("videos", [])] + ([t["video_id"]] if t.get("video_id") else [])
    for v in vids:
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', v):
            issues['bad video id'].append(f"{t['slug']}: {v}")
    if not vids and t["slug"] not in ():
        issues['no video'].append(t["slug"])

for slug in g.TAGS:
    if slug not in slugs: issues['tag for unknown slug'].append(slug)
for slug, tags in g.TAGS.items():
    for tag in tags:
        if tag not in g.FEELINGS: issues['tag not in FEELINGS'].append(f"{slug}: {tag}")
for f in list(g.FEELS)+list(g.BENEFITS)+list(g.MEDITATIONS)+list(g.BASICS):
    if f not in slugs: issues['side-map unknown slug'].append(f)
untagged = [t["slug"] for t in g.TECHNIQUES if t["slug"] not in g.TAGS]
if untagged != ["sonic-neural"]:
    issues['unexpected untagged'].extend(untagged)

# every pillar in PILLARS has a page and at least one technique
for pil in g.PILLARS:
    if not any(t["pillar"]==pil for t in g.TECHNIQUES): issues['empty pillar'].append(pil)

# rendered text: double spaces and stray entities
for f in sorted(glob.glob('**/*.html', recursive=True)):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    txt = html.unescape(re.sub(r'<[^>]+>', '\n', s))
    for line in txt.split('\n'):
        line = line.strip()
        if '  ' in line: issues['rendered double space'].append(f'{f}: {line[:60]}')
    if re.search(r'&[a-zA-Z]+;', re.sub(r'&(amp|lt|gt|quot|middot|rarr|nbsp|copy);','',s)):
        issues['unresolved entity'].append(f)

# Filter keys must be plain slugs. A display label in a data attribute puts an
# apostrophe in the markup, and a host that re-serialises the HTML (Netlify's
# pretty-URL pass does) escapes it into something the attribute parser cuts
# short, which silently empties the filter in production.
for f in sorted(glob.glob('**/*.html', recursive=True)):
    s = open(f, encoding='utf-8').read()
    for attr, val in re.findall(r'\b(data-feelings?)="([^"]*)"', s):
        if not re.fullmatch(r'[a-z0-9|-]*', val):
            issues['filter key not a slug'].append(f'{f}: {attr}="{val[:40]}"')

# every pill on the index must be reachable: some card carries its key
for f in ['index.html']:
    s = open(f, encoding='utf-8').read()
    keys = set()
    for v in re.findall(r'\bdata-feelings="([^"]*)"', s):
        keys.update(x for x in v.split('|') if x)
    for p in re.findall(r'\bdata-feeling="([^"]*)"', s):
        if p not in keys:
            issues['pill matches no card'].append(f'{f}: {p}')

print(f"techniques: {len(g.TECHNIQUES)}  pills: {len(g.FEELINGS)}  pillars: {len(g.PILLARS)}")
for k in sorted(issues):
    print(f'\n== {k} ({len(issues[k])})')
    for v in issues[k][:15]: print('  ', v)
if not issues: print('\nALL CLEAN')
