# Clay & Air breath technique library

Static HTML. No runtime dependency, no framework, no build step in production.
`_generate.py` is a local dev tool that writes the `.html` files, and the
`.html` files are what ship.

    python3 _generate.py

## Structure

    index.html              the library: every technique, filtered by pills
    relaxing/index.html     pillar page, plain list
    relaxing/*.html         8 technique pages
    activating/index.html   pillar page, plain list
    activating/*.html       9 technique pages
    freedom/index.html      pillar page
    freedom/sonic-neural.html
    assets/breath.css       tokens and components
    assets/mark-*.svg       simplified cut of MARK-01, used below 180px
    _generate.py            page generator, and all the content
    qa.py, qa2.py           the checks

19 techniques across 3 pillars, 23 pages, 24 embedded videos.

## The index

A grid of every technique. The card heading is the technique name, with the
one-line use and duration and position underneath. Foundational breath carries
START HERE; Dynamic breathwork and Sonic Neural carry BEN HOLT SIGNATURE.

Above the grid sit the feeling pills. Nothing selected shows everything;
selecting pills narrows the grid. Matching is **OR**, not AND, so picking
several feelings shows everything that helps with any of them. An empty result
is the worst thing to hand someone in a bad state.

Edit `FEELINGS` (the pill list) and `TAGS` (slug to feelings) to change them.

**Sonic Neural is deliberately untagged.** It appears in the unfiltered grid but
no feeling ever surfaces it, because a facilitated 55 minute ceremony should
never be the answer to how someone feels at 2am. `qa2.py` asserts this.

## Page order

Pillar label, heading, meta band, purpose, pills, before-you-start, video,
the pattern, how it lands, what it does, the rest of the pillar.

## Adding a technique

1. Add a dict to `TECHNIQUES` in `_generate.py`.
2. Add its feelings to `TAGS`.
3. Add `FEELS` and `BENEFITS` entries.
4. `python3 _generate.py`

### Fields

Required: `slug`, `name`, `pillar`, `purpose`, `steps`, `meta` (three parts:
duration, position, nose or mouth), `sideways`, `short_use`.

Optional, and omitted rather than invented where the source is silent:

- `before` — the setup and health block. Renders above everything, in a paper
  panel with a terracotta edge. Used by the activating techniques, Dynamic and
  Sonic Neural.
- `note`, `note2`, `note3` — small text under the steps. The correction line
  (`sideways`) is appended here too; it has no section of its own.
- `progression` — a "when that is easy" block. Nadi Shodhana and breath of fire
  use it.
- `signature` — marks it as Ben Holt's own design.
- `start_here` — the entry point. Foundational breath only.
- `cadence` — kept as data but **not rendered anywhere**. Switch it back on in
  `technique_page` if that ever changes.
- `video_id` for one recording, or `videos` for an ordered set of
  `(label, caption, id)`. Sonic Neural and Dynamic both use `videos`.

### Side maps

`FEELS`, `BENEFITS`, `BASICS` and `MEDITATIONS` sit outside `TECHNIQUES`
because they came from a different source: the course videos rather than the
original cards brief.

- `FEELS[slug]` — one sentence on how it lands in the body.
- `BENEFITS[slug]` — short lines specific to that technique. `PILLAR_BENEFITS`
  is a shared tail appended to every technique in the pillar, so the
  physiological benefits appear on every card without being retyped.
- `BASICS[slug]` + `BASICS_INTRO` — the foundations block, on the start-here
  card only.
- `MEDITATIONS[slug]` — `(youtube id, "ben" | "clay")`. Adds a second player
  under the technique video, captioned by whose recording it is. Only cleansing
  breath has one so far; the plan is one per relaxing technique, recorded by
  Clay & Air, which is what `"clay"` is for.

## Checks

    pip install pyspellchecker --break-system-packages
    python3 qa.py && python3 qa2.py

`qa.py` covers the output: broken internal links, long dashes, curly quotes,
unresolved entities, duplicate titles, unbalanced tags, images without alt, and
spelling across every word of rendered text.

`qa2.py` covers the data: required fields, meta shape, sentence-ending
punctuation, double spaces, video id format, tags pointing at nothing, empty
pillars, and the Sonic Neural tagging rule.

Known false positives: `holt's`, `neuro`, `org` in the speller, and `4-3-6`
tripping the name-case check because it starts with a digit.

## House rules

- **No long dashes.** No em or en dashes anywhere in the output. Ranges use a
  hyphen. Rewrite the sentence rather than swapping the character.
- **Straight apostrophes**, not curly. Keyboard characters only.
- **No cadence notation** on the site.
- The only non-alphabetic characters in the copy are the middot separating meta
  items and the ampersand in the name.

## Attribution

Every technique is Ben Holt's, learned through Awakened Breath and the 21 Day
Breathwork Academy. Dynamic breathwork and Sonic Neural are his own designs and
are marked as such. Credit sits in the footer of all 23 pages and in a section
on the index.

## Deployment

The site is a folder of static files. Anything that serves a directory works.
Open it over a local server rather than double-clicking a file, or the YouTube
embeds fail with a configuration error:

    python3 -m http.server 8000

## Open items

- Guided meditations for the rest of the relaxing pillar. Add a line to
  `MEDITATIONS` as each is recorded.
- Two lines in the health blocks are not from Ben: the lightheaded caution on
  the forceful techniques, and "pick a stretch where you are not crossing
  roads" on Buteyko.
- Twisting breath and heart opening breath have no `before` block. Neither
  creates a stress response the way the others do, but worth a second look.
