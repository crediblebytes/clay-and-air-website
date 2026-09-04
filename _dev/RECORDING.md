# Guided meditations, recording plan

Eight recordings, one per relaxing technique. This is the thing that turns the
site from a curation of Ben's work into your practice. Right now a visitor can
tell the library is well made, but they cannot tell why they would work with
you rather than watch Ben on YouTube. Your voice in their ear at 2am is the
answer to that, and it is the only asset here that nobody else can copy.

## Order to record

Not alphabetical, and not the order they sit on the page. Record in order of
who needs it most.

1. **Foundational breath.** It carries START HERE, so it gets the most
   traffic, and it is the shortest to cut. It is also the safest one to be
   bad at, which matters because your first recording will be your worst.
2. **Turtle breath.** The only technique tagged for "Can't sleep" on its own.
   Somebody awake at 3am with your voice in one earbud is the single best use
   this site has. Longest and hardest, so do it second while you still care.
3. **Cleansing breath.** Ben's guided version already sits on that page, so
   yours goes straight up against it. That is uncomfortable and it is exactly
   why it is worth doing third: it will tell you honestly where your delivery
   is at.
4. **Box breathing.** Daytime, under pressure, eyes open, sitting at a desk.
   A different register from the first three. Prove you can do both.
5. **4-3-6**, 6. **Nadi Shodhana**, 7. **Full-fill**, 8. **Qi Gong breathing.**

Stop after the first three and listen back before booking time for the rest.

## Length

Match the duration already on each card, at the short end of the range. If the
card says 5 to 10 minutes, record eight. Somebody in a bad state will not start
a twenty minute file, and a recording that runs shorter than its label feels
like a bait and switch. The duration on the card is a promise.

## The shape of every recording

Same five parts every time, so a listener who has done one knows how the next
one goes. That predictability is the whole point of a series.

**One. Land it. Twenty seconds.**
Name where they probably are. Not a welcome, not your name, not the brand. The
first sentence should sound like it was written for the state they are in.

> It is late and you are still awake. Put the phone face down. You do not have
> to do this well.

**Two. Set the body. Thirty seconds.**
Position, hands, jaw, where the air goes in and out. Everything the meta row on
the page already says, said out loud. No explanation of benefits here. They
have read the page or they have not, and either way they came to do the thing.

**Three. The pattern, counted. The bulk of it.**
You count. Out loud, every round, the whole way through. This is the product.
It is also the part people get wrong by trying to be interesting: your job is
to be a metronome that happens to be warm. Count the first five rounds fully,
then thin out to counting the turns only, then leave stretches where you say
nothing at all.

**Do not talk over the holds.** The silence is not dead air, it is the
practice. Every instinct will tell you to fill it. Do not.

**Four. The drop off. One or two minutes.**
Stop counting. Tell them to let the pattern go and let the breath do what it
wants. Say almost nothing. One line every thirty seconds at most.

**Five. The close. Twenty seconds.**
Bring them back without ceremony. No "when you are ready", no bell, no thank
you. Say what to do next and stop talking.

> That is it. Do not get up fast. If you are going back to sleep, stay where
> you are.

## Voice

The site's rules apply to audio, and harder, because a phrase you would skim
past on a page is unbearable in your ear.

Use: tired, drinking, panic, sleep, mornings, hold it together, function.
Never: journey, sacred, hold space, energy, your truth, high vibration,
warrior, surrender to the moment, beautiful soul.

Second person throughout. First person only if you are telling a specific true
thing about yourself, and at most once per recording. "This one used to make me
angry" earns its place. "I invite you to" does not.

Do not smile into the microphone. The audience is a competent adult having a
bad year, and warmth that sounds like customer service will lose them faster
than being too flat.

## Recording

You do not need a studio, you need a quiet room. In order of what actually
ruins takes:

- **Room noise.** Fridge, HVAC, traffic, a laptop fan. Record at night, kill
  the air conditioning, and record ten seconds of silence at the top of every
  session so noise reduction has room tone to work from.
- **Distance.** A hand span from the mic, consistently, slightly off axis so
  your plosives go past it rather than into it.
- **The room itself.** Hard walls make you sound like a bathroom. Record in a
  closet with clothes in it, or throw a duvet over a clothes rail behind you.

Settings: mono, 48kHz, 24 bit. Export to MP3 at 128kbps mono for the web, which
is plenty for a voice and keeps the files small on a phone connection.

Do one full pass without stopping rather than punching in fixes. A recording
assembled from patched takes has a rhythm problem you can hear but cannot
locate, and the rhythm is the thing you are selling.

## Music

Optional, and start without it. If you add a bed, it sits far enough down that
you would not notice it stopping, and it never swells. No singing bowls, no
binaural claims, no rain. If Sonic Neural is where music does the work, then
keeping the relaxing recordings dry is what makes that contrast mean something.

## Putting one on the site

Upload to YouTube, unlisted or public, then add one line to `MEDITATIONS` in
`_dev/generate.py`:

    MEDITATIONS = {
        "cleansing-breath": ("bKAwu9Yr-Gk", "ben"),
        "turtle-breath": ("YOUR_VIDEO_ID", "clay"),
    }

`"clay"` captions it as yours, `"ben"` as his. Then run `python3 _dev/generate.py`
and the second player appears under the technique video on that page. Nothing
else needs touching.

## Where this goes next

Once four or five exist, they stop being page furniture and become the thing
itself: a set of recordings somebody works through in order. That is when the
email sequence has something to deliver, and when there is a reason for
somebody to come back on day nine rather than reading one page and leaving.
