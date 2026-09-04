import glob, os, re, html, collections
import os, pathlib
os.chdir(pathlib.Path(__file__).resolve().parent.parent)  # repo root
from spellchecker import SpellChecker

files = sorted(glob.glob('**/*.html', recursive=True))
issues = collections.defaultdict(list)

# --- links, dashes, placeholders, structure ---
titles = {}
for f in files:
    s = open(f, encoding='utf-8').read()
    for m in re.findall(r'(?:href|src)="([^"#]+)"', s):
        if m.startswith(('http', 'mailto')): continue
        m = m.split('?')[0]           # the file is the path, not the query
        if not m: continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), m))):
            issues['broken link'].append(f'{f}: {m}')
    for ch in ['—', '–', '&mdash;', '&ndash;']:
        if ch in s: issues['long dash'].append(f'{f}: {ch}')
    if 'PLACEHOLDER' in s: issues['placeholder'].append(f)
    if '&rsquo;' in s and "'" in re.sub(r'<[^>]+>|&\w+;', '', s):
        issues['mixed apostrophes'].append(f)
    t = re.search(r'<title>(.*?)</title>', s)
    if not t: issues['no title'].append(f)
    else: titles.setdefault(t.group(1), []).append(f)
    if not re.search(r'<meta name="description"', s): issues['no description'].append(f)
    for tag in ['div', 'section', 'ul', 'ol', 'li', 'p', 'figure', 'a', 'article']:
        o = len(re.findall(rf'<{tag}[\s>]', s)); c = len(re.findall(rf'</{tag}>', s))
        if o != c: issues['tag mismatch'].append(f'{f}: <{tag}> {o} open / {c} close')
    for m in re.findall(r'<img [^>]*>', s):
        if 'alt=' not in m: issues['img no alt'].append(f'{f}: {m[:50]}')
    if '  ' in re.sub(r'\n\s*', ' ', re.sub(r'<[^>]+>', '', s)).strip():
        pass
for t, fs in titles.items():
    if len(fs) > 1: issues['duplicate title'].append(f'{t}: {fs}')

# --- spelling over visible text ---
sp = SpellChecker()
# Real words the dictionary does not carry: brand and platform names, and the
# possessive forms it splits badly. Kept here so the report stays empty unless
# something is actually wrong, which is the only way a check gets read.
sp.word_frequency.load_words([
    "holt", "holt's", "ujjayi", "nadi", "shodhana", "kapalabhati",
    "bhastrika", "buteyko", "kundalini", "pranayama", "qi", "gong",
    "breathwork", "neuro", "linguistic", "immersive",
    "instagram", "tiktok", "youtube", "netlify", "plausible", "org",
    "clayandair", "clayandairnow",
])
allow = set("""ujjayi nadi shodhana bhastrika kapalabhati buteyko qi gong tummo
kundalini pranayama savasana hormesis parasympathetic vagus namaste clay
awakenedbreath holt wim hof himalayas sedona youtube favicon svg html css
breathwork nostril nostrils exhale exhales inhale inhales exhaling inhaling
diaphragmatic alkalises alkalise visualisation nocookie tia tias om
prefrontal subconscious lightheaded reps cadence bone soot terracotta
ochre newsreader ibm plex mono chapstick tetany""".split())
words = collections.Counter()
for f in files:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    for w in re.findall(r"[A-Za-z][A-Za-z']+", txt):
        lw = w.lower().strip("'")
        if lw in allow or len(lw) < 3: continue
        words[lw] += 1
unknown = sp.unknown(words.keys())
for w in sorted(unknown):
    issues['spelling?'].append(f'{w} ({words[w]}x)')

for k in sorted(issues):
    print(f'\n== {k} ({len(issues[k])})')
    for v in issues[k][:40]: print('  ', v)
if not issues: print('clean')
