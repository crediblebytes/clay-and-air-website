#!/usr/bin/env python3
"""Clay & Air — breath technique library page generator.

Emits static HTML. Nothing here runs in the browser and the site has no build
dependency; this exists so every technique page shares one template and so
activating techniques slot in by adding a dict to TECHNIQUES.

To add a technique:
  1. Add an entry to TECHNIQUES with pillar="activating".
  2. Add a row to STATES if it has a state someone would arrive in.
  3. Run: python3 _dev/generate.py

Fields that may be omitted:
  cadence  — omit where no real protocol exists. Never invent one.
  before   — omit where there is no real risk profile. Never invent one.
  note     — omit where the source has no note.
"""

import html
import json
import os
import re
import time

# generate.py lives in _dev/ and writes the site to the repo root, so
# nothing but the site itself is ever inside the published directory.
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Search and answer-engine descriptions, one per pillar. Written to answer the
# question someone actually typed, not to restate the pillar name.
PILLAR_DESC = {
    "relaxing": ("Eight breathing techniques that bring the nervous system "
                 "down: for anxiety, sleep, and staying steady under "
                 "pressure. Safe to run on your own."),
    "activating": ("Ten breathing techniques that wake the body up: for "
                   "mornings, before training, and shifting a flat day. "
                   "Come back sharper for it."),
    "freedom": ("Sonic Neural Breathwork, a facilitated ceremony rather than "
                "a technique you fit into a lunch break. What it is, what it "
                "does, and how to prepare for one."),
}

PILLARS = {
    "relaxing": ("Pillar one · Relaxing", "relaxing"),
    "activating": ("Pillar two · Activating", "activating"),
    "freedom": ("Pillar three · Freedom", "freedom"),
}

# ---------------------------------------------------------------------------
# Techniques. Copy is verbatim from the approved cards brief.
# ---------------------------------------------------------------------------

TECHNIQUES = [
    {
        "slug": "foundational-breath",
        "name": "Foundational breath",
        "pillar": "relaxing",
        "start_here": True,
        "cadence": None,  # the hold is the only fixed number; there is no protocol
        "purpose": "The fastest way down, and the base every other technique here "
                   "is built on. If you have not done this before, start with "
                   "this one.",
        "steps": [
            "Breathe in through the nose in one continuous movement: belly "
            "first, then chest, then all the way up behind the eyes.",
            "Hold 5 to 10 seconds at the top.",
            "Open your mouth and sigh it all the way out. Long, and out loud.",
            "Anywhere you cannot make noise, use the Ujjayi exhale instead. Same "
            "length, mouth closed.",
            "Repeat.",
        ],
        "note": "The sigh is doing real work. The voice empties you "
                "faster than the breath alone, so use it wherever you can.",
        "meta": ["3-10 minutes", "Sitting or lying", "Nose in, sigh out"],
        "sideways": "Belly not moving means the air stopped at your chest. Put a hand "
                    "below your navel and breathe into it.",
        "short_use": "The fastest way down. Base for everything else.",
        "video_id": "nSJGe-goQnY",
    },
    {
        "slug": "box-breathing",
        "name": "Box breathing",
        "pillar": "relaxing",
        "cadence": ["5", "5", "5", "5"],
        "purpose": "Quiets the mind and puts you back in the room. This is the one "
                   "used under pressure.",
        "steps": [
            "Take one ordinary breath in through the nose and let it go out of "
            "the mouth. That clears the decks.",
            "Inhale 5 seconds through the nose: belly, chest, head.",
            "Hold 5 seconds.",
            "Exhale 5 seconds through the nose.",
            "Hold 5 seconds. That is one cycle.",
            "Keep the count steady rather than long.",
        ],
        "note": "The number is only a frame. Four works, so does six, and you can "
                "move between them. What matters is that counting keeps "
                "your attention on the breath and off whatever is going on around "
                "you. Run it with the Ujjayi exhale once the count is easy.",
        "meta": ["3-10 minutes", "Sitting upright", "Nose in, nose out"],
        "sideways": "Straining at 5 means start at 3. The evenness matters more than "
                    "the number.",
        "short_use": "Quiets the mind. Used under pressure.",
        "video_id": "hYvEp3OUcAA",
    },
    {
        "slug": "turtle-breath",
        "name": "Turtle breath",
        "pillar": "relaxing",
        "cadence": ["10", "10"],
        "cadence_tail": "&rarr; 20 &middot; 20",
        "purpose": "Deep relaxation and sleep. You slow the breath down in stages "
                   "rather than dropping straight to the bottom.",
        "steps": [
            "Run a few rounds of foundational breath first. You cannot reach the "
            "long counts cold.",
            "Lying down. Inhale through the nose, belly first, then chest, "
            "filling all the way up.",
            "Release from the top down with an Ujjayi exhale.",
            "Start at 10 seconds in, 10 seconds out.",
            "Move to 12, then 15, then 18, then 20 as each one stays comfortable.",
            "Stay at whatever count you can hold without effort.",
        ],
        "note": "Turtle breath is not the 20 seconds. It is the slowing down. "
                "Every breath a little longer than the last, and the number is "
                "where you end up, not where you start.",
        "meta": ["5-10+ minutes", "Lying down", "Nose in, nose out"],
        "sideways": "If a longer count starts to feel like work, or you find "
                    "yourself needing the next breath, you have gone past it. "
                    "Drop back a step. This is meant to settle you, not "
                    "stress you.",
        "short_use": "Deep relaxation and sleep.",
        "video_id": "O2YvGaIeAqM",
    },
    {
        "slug": "nadi-shodhana",
        "name": "Nadi Shodhana",
        "pillar": "relaxing",
        "cadence": ["7", "5", "7"],
        "purpose": "Evens out both sides. Use it when you're wired and can't "
                   "focus, scattered and can't settle, or winding down for "
                   "the night.",
        "steps": [
            "Sit upright, spine long. Rest the index and middle fingers of your "
            "dominant hand on your forehead, between the eyebrows.",
            "Close your right nostril with your thumb.",
            "Inhale 7 seconds through the left: belly, chest, head.",
            "Hold 5 seconds.",
            "Exhale 7 seconds through the left.",
            "Switch. Your middle finger comes down onto the left nostril and "
            "your thumb lifts off the right.",
            "Inhale 7, hold 5, exhale 7 through the right. That is one round.",
            "Keep switching for three to ten minutes.",
        ],
        "progression": "Once the same-nostril round is easy, move to the "
                       "alternating form: inhale left, exhale right, inhale "
                       "right, exhale left, always inhaling through the "
                       "nostril you just exhaled through. Nine rounds, finishing "
                       "on a left-side exhale.",
        "note": "Keep the breath plain. No Ujjayi here. A simpler way in "
                "is to breathe in and out through one nostril for several "
                "minutes before you start switching at all.",
        "note2": "If your nose is blocked, from allergies or a cold, pull "
                 "the outside of the opposite nostril sideways with your free "
                 "hand to open it up, or use a nasal strip. Swapping to your "
                 "other hand can help as well.",
        "meta": ["3-10 minutes", "Sitting upright", "Nose only"],
        "sideways": "If 7 seconds is a strain, run 4 &middot; 4. The evenness "
                    "matters more than the number.",
        "short_use": "Evens out both sides. Settles without sedating.",
        "video_id": "Kz6p47Hat1I",
    },
    {
        "slug": "full-fill",
        "name": "Full-fill",
        "pillar": "relaxing",
        "cadence": None,  # the 10-second hold is the only fixed number
        "purpose": "Foundational breath taken up a level. You stack breaths "
                   "before the hold, and that takes you further down than a "
                   "single round does.",
        "steps": [
            "Breathe in through the nose: belly, chest, head. Let it go.",
            "Second big breath, the same way. Let it go.",
            "Third big breath. This time fill all the way up.",
            "Hold 10 seconds at the top.",
            "Sigh it out, or use a long Ujjayi exhale.",
        ],
        "note": "Three breaths is where to start. More breaths before the hold "
                "makes it stronger. Seven, ten, fifteen. Change the "
                "number until it suits you.",
        "meta": ["3-10 minutes", "Sitting or lying", "Nose in, sigh out"],
        "sideways": "If your chest moves before your belly, the order is "
                    "backwards. Hand below the navel and start there.",
        "short_use": "Stacked breaths and a hold. Goes deeper than one round.",
        "video_id": "q51lSvA7X7o",
    },
    {
        "slug": "4-3-6",
        "name": "4&middot;3&middot;6",
        "plain_name": "4·3·6",
        "pillar": "relaxing",
        "cadence": ["4", "3", "6"],
        "purpose": "The exhale runs longer than the inhale, and that ratio is what "
                   "does the work. Use it when box breathing isn't enough.",
        "steps": [
            "Sitting or lying down. Take one foundational breath first: in "
            "through the nose, hold it, sigh it out.",
            "Inhale 4 seconds through the nose, deep into the belly.",
            "Hold 3 seconds.",
            "Exhale 6 seconds through the nose, slow.",
            "Start again without pausing at the bottom.",
        ],
        "note": "The counts are a starting point, not a rule. Lengthen all "
                "three as you settle: 5, 7, 10. Shorten them if 4, 3, 6 is a "
                "stretch: 3, 2, 5 is easier coming out of a workout or when you "
                "are already wound up. Build back up from there.",
        "meta": ["5-10+ minutes", "Sitting or lying", "Nose in, nose out"],
        "sideways": "If 6 seconds runs out early, shorten the whole pattern and keep "
                    "the exhale the longest part of it.",
        "short_use": "Longer exhale than inhale. When box isn't enough.",
        "video_id": "wuJRcZO3wmM",
    },
    {
        "slug": "cleansing-breath",
        "name": "Cleansing breath",
        "pillar": "relaxing",
        "cadence": None,
        "purpose": "A meditation as much as a breath. You fill up with golden "
                   "light and empty the day out as smoke. Use it when you are "
                   "wound up, worked up, or carrying tension you want gone.",
        "steps": [
            "Sitting or lying down. Breathe in through the nose: belly, chest, "
            "head, filling all the way up.",
            "As you fill, picture a golden light coming in with the air, like "
            "water filling a jar. Take it down to the tips of your toes and "
            "fingers and up to the crown of your head, until you are full of "
            "it. Feel it cleanse and nourish every cell on the way.",
            "Hold it at the top. It helps.",
            "Ujjayi exhale through the nose, and let the tension out with it as "
            "a dark purple cloud of smoke. It goes out into the air and "
            "disperses. It does not come back.",
            "The heavy part sits in a cauldron low in your belly, like a pouch. "
            "Every exhale takes a little more of it. Five to ten minutes, until "
            "the cauldron is empty.",
            "Once it is empty, breathe the golden light down into the cauldron "
            "itself and wash it clean.",
        ],
        "note": "This is neuro-linguistic programming, and the picture is the "
                "technique rather than decoration. You are showing the "
                "subconscious mind what you want, and it takes the instruction.",
        "meta": ["5-10 minutes", "Sitting or lying", "Nose in, nose out"],
        "sideways": "If the picture will not come, do not force it. Run the "
                    "breath on its own and let the image turn up or not.",
        "short_use": "Golden light in, smoke out. Puts the day down.",
        "video_id": "lWhEzJ5wnGY",
    },
    {
        "slug": "priming-breath",
        "name": "Priming breath",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Wakes the system up. Mornings, before training, or any time "
                   "you would otherwise reach for coffee.",
        "before": [
            "This starts a stress response on purpose. That is the point of it, "
            "and it is why it belongs in the morning rather than before bed.",
            "Finish with something from the relaxing pillar. Foundational "
            "breath is enough.",
            "Breathing this hard can make you lightheaded. Sit down to do it, "
            "and stop if your head goes.",
        ],
        "steps": [
            "Sit or stand with room to move your arms.",
            "Take a couple of ordinary breaths first, in through the nose and "
            "out through the mouth.",
            "Forceful inhale through the nose. Belly pushes out, arms go up "
            "overhead.",
            "Forceful exhale through the nose. Belly pulls in, arms come down "
            "with your elbows tucked to your sides.",
            "Keep the arms and the breath on the same beat. Thirty reps is one "
            "set.",
            "As many sets as you want. Then sit still for a few minutes.",
        ],
        "note": "It should feel mechanical, like a piston. The force is in both "
                "halves of the breath, not just the exhale.",
        "meta": ["30 reps a set", "Sitting or standing", "Nose in, nose out"],
        "sideways": "Lightheaded means you are moving more air than you need. "
                    "Slow the rate down, keep the force, and sit if you are not "
                    "already sitting.",
        "short_use": "Wakes the body up. Morning, or before training.",
        "video_id": "p2k6dbyMd3o",
    },
    {
        "slug": "breath-of-fire",
        "name": "Breath of fire",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Fast and forceful in both directions. Builds heat. Mornings, "
                   "before training, or after cold water.",
        "before": [
            "This starts a stress response on purpose. Mornings and before "
            "effort, not before bed.",
            "Finish with something from the relaxing pillar.",
            "Fast forceful breathing can make you lightheaded. Sit down to do "
            "it, and stop if your head goes.",
        ],
        "steps": [
            "Sit upright. Breathe in, then let about three quarters of the air "
            "back out before you start.",
            "Forceful exhale through the nose. Belly pulls in.",
            "Forceful inhale through the nose. Belly pushes out.",
            "Keep both halves equally strong and let them run together.",
            "Start slow, then build the pace up.",
            "One to five minutes. Longer once you are used to it.",
        ],
        "note": "This is the one people confuse with Kapalabhati. Kapalabhati "
                "puts the force on the exhale only and lets the inhale happen "
                "by itself. Here both halves are forced, which is what makes it "
                "hard work.",
        "progression": "Once the pump runs itself, try it with your arms "
                       "overhead, elbows locked and thumbs up. That is Kundalini "
                       "Bhastrika, and it is a different order of effort.",
        "meta": ["1-5 minutes", "Sitting upright", "Nose in, nose out"],
        "sideways": "Lightheaded means the pace has run ahead of you. Slow it "
                    "down and keep the force.",
        "short_use": "Forceful both ways. Builds heat.",
        "video_id": "Sjykb3_8sV8",
    },
    {
        "slug": "buteyko-breathing",
        "name": "Buteyko breathing",
        "pillar": "activating",
        "cadence": None,
        "purpose": "The one you can run while you are moving. Empty the lungs, "
                   "hold, and walk. Use it on the way somewhere when you are "
                   "wound up.",
        "steps": [
            "Breathe in through the nose.",
            "Exhale all the way out through the nose.",
            "Pinch your nose closed and hold.",
            "Walk. Fifteen to twenty-five steps.",
            "Let go, take one good breath in, and let it go.",
            "Repeat as you walk.",
        ],
        "note": "Pick a stretch of pavement where you are not crossing roads. "
                "Walking with your breath held is not the time to be watching "
                "traffic.",
        "note2": "Altitude is the other use. Build the held walk up to 25, 30, "
                 "40 steps over weeks. If you live at sea level, doing this "
                 "before a trip into the mountains is worth the effort.",
        "meta": ["15-25 steps a round", "Walking", "Nose only"],
        "sideways": "If you are gasping when you let go, the walk was too long. "
                    "Cut it back until you finish each round calm.",
        "short_use": "A held walk. Runs while you are moving.",
        "video_id": "AyqqFscd8FE",
    },
    {
        "slug": "kapalabhati",
        "name": "Kapalabhati",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Forceful on the exhale only. Empties the lungs further than "
                   "an ordinary breath does, and works your stomach doing it.",
        "before": [
            "This starts a stress response on purpose. Mornings and before "
            "effort, not before bed.",
            "Finish with something from the relaxing pillar.",
            "Fast forceful breathing can make you lightheaded. Sit down to do "
            "it, and stop if your head goes.",
        ],
        "steps": [
            "Sit upright with one hand flat on your belly.",
            "Take a deep breath in through the nose and let it go out of the "
            "mouth. Twice.",
            "Forceful exhale through the nose. Your belly snaps in under your "
            "hand.",
            "Let the inhale happen by itself. Do not pull it in.",
            "Keep going. The exhale is the only part you work.",
            "Fifty reps, or two to seven minutes.",
        ],
        "note": "The difference from breath of fire is the whole technique. "
                "There you force both halves. Here you force the exhale and let "
                "the inhale fall in on its own, which costs less and is why you "
                "can keep it going longer.",
        "meta": ["50 reps or 2-7 minutes", "Sitting upright", "Nose only"],
        "sideways": "If your belly is not moving under your hand you are "
                    "exhaling from the chest. Push it from lower down.",
        "short_use": "Forceful exhale only. Works the stomach.",
        "video_id": "KxWXJ0gnNPQ",
    },
    {
        "slug": "igniter-breath",
        "name": "Igniter breath",
        "pillar": "activating",
        "cadence": None,
        "purpose": "The fastest way to warm up. After cold water, before "
                   "training, or when your head is stuck.",
        "before": [
            "This starts a stress response on purpose. Mornings and before "
            "effort, not before bed.",
            "Finish with something from the relaxing pillar.",
            "Fast forceful breathing can make you lightheaded. Sit down to do "
            "it, and stop if your head goes.",
        ],
        "steps": [
            "Sit up tall. Palms flat on your knees so your arms have something "
            "to push against.",
            "Take one foundational breath first: in through the nose, sigh it "
            "out.",
            "Intense inhale through the nose. Shoulders rise.",
            "Exhale through the mouth with the same force. Shoulders drop.",
            "Keep both halves equally hard.",
            "Thirty seconds to five minutes, or a hundred reps.",
        ],
        "note": "Three breaths in and you should feel it. It is meant to make "
                "you hot, and it will.",
        "meta": ["30 seconds to 5 minutes", "Sitting upright", "Nose in, mouth out"],
        "sideways": "Lightheaded means the pace has run ahead of you. Slow it "
                    "down and keep the force.",
        "short_use": "Warms you up fast. After cold water, or before training.",
        "video_id": "slnrNhLssKw",
    },
    {
        "slug": "twisting-breath",
        "name": "Twisting breath",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Breath and movement on the same beat. A warm-up that works "
                   "your core, before training or before the day.",
        "steps": [
            "Sit or stand with your arms out in front, palms together.",
            "Twist to one side, breathing in gently through the mouth as you "
            "go.",
            "At the end of the twist, force all the air out through the nose "
            "and pull your stomach in hard.",
            "Twist back the other way, breathing in again on the way across.",
            "Force it out at the end of that side too.",
            "Keep alternating for about ten minutes.",
        ],
        "note": "Pick something to look at and keep it. Your thumbs or your "
                "fingertips both work. What you are after is the breath "
                "starting to happen by itself at each end of the twist.",
        "meta": ["About 10 minutes", "Sitting or standing", "Mouth in, nose out"],
        "sideways": "If the breath and the twist come apart, slow the twist "
                    "down until they line up again.",
        "short_use": "Twist and exhale hard. Warm-up that works the core.",
        "video_id": "bXwVZQmGMCI",
    },
    {
        "slug": "heart-opening-breath",
        "name": "Heart opening breath",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Opens the heart space and uses your voice to do it. For "
                   "mornings, and for anything you are carrying around that you "
                   "have not said out loud.",
        "steps": [
            "Sit or stand with your arms out wide.",
            "Breathe in through the nose, bringing your arms in toward your "
            "chest. Belly, chest, head.",
            "As you draw them in, picture a green light coming into the heart "
            "space. That light is love.",
            "Open your arms and breathe out on a long, audible ah. Send the "
            "light out with it, to everyone you care about and everyone who "
            "needs some.",
            "Keep going. The sound is the technique, not an addition to it.",
            "If something comes up, shake it out. Hands, arms, whole body.",
            "If there is someone you hold a grudge against, breathe the light "
            "in with them in mind and send it to them on the way out. Forgive "
            "them on purpose.",
            "Ten to twenty minutes.",
        ],
        "note": "The voice and the movement are what shift it. An antelope gets "
                "chased, gets away, and shakes the whole thing off. So does a "
                "dog. People hold on to it instead, which is why it stays, and "
                "this is the way back out.",
        "meta": ["10-20 minutes", "Sitting or standing", "Nose in, voice out"],
        "sideways": "If you cannot make noise where you are, this is not the "
                    "technique. Use foundational breath and come back to this "
                    "one later.",
        "short_use": "Loud on the exhale. Clears the deck before the day.",
        "video_id": "kVYw2CYw3HA",
    },
    {
        "slug": "kundalini-bhastrika",
        "name": "Kundalini Bhastrika",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Breath of fire with your arms overhead. The same pump, with "
                   "a great deal more work in the shoulders.",
        "before": [
            "This starts a stress response on purpose. Mornings and before "
            "effort, not before bed.",
            "Finish with something from the relaxing pillar.",
            "Fast forceful breathing can make you lightheaded. Sit down to do "
            "it, and stop if your head goes.",
        ],
        "steps": [
            "Get breath of fire going on its own first. Belly pumps in on the "
            "exhale and fills back up by itself.",
            "Breathe in, then let about three quarters of the air back out.",
            "Raise your arms overhead, elbows locked, thumbs pointing up and "
            "out.",
            "Start the pump and keep the arms where they are.",
            "Thirty seconds to a minute to begin with. Build up to three or "
            "five minutes.",
        ],
        "note": "Your shoulders will give out before your breath does. That is "
                "the technique working rather than a fault in it.",
        "meta": ["30 seconds to 5 minutes", "Sitting or standing", "Nose only"],
        "sideways": "Lightheaded means the pace has run ahead of you. Drop the "
                    "arms, slow down, and start again.",
        "short_use": "Breath of fire, arms overhead. Harder.",
        "video_id": "duFPRf4fYck",
    },
    {
        "slug": "digestion-igniter",
        "name": "Digestion igniter",
        "pillar": "activating",
        "cadence": None,
        "purpose": "Lion's breath, then a stomach vacuum on empty lungs. It "
                   "massages the organs in the gut and gets the digestion "
                   "moving. A hard morning practice besides.",
        "before": [
            "This is a hold on empty lungs. Come up for air the moment you want "
            "it, not a second later.",
            "Do it before you eat, not after.",
        ],
        "steps": [
            "Stand up. Take a breath in through the nose and let it go out of "
            "the mouth. Twice.",
            "Big breath in through the nose.",
            "Lion's breath out: tongue out, Ujjayi, everything emptied.",
            "Hands on your knees with your lungs empty. Draw your stomach in "
            "and up under your ribs.",
            "Move it around while it is held there. That is the massage.",
            "When you want air, stand up and breathe in through the nose at the "
            "same time.",
            "Ten to fifteen minutes.",
        ],
        "note": "The lion's breath looks alarming and sounds worse. Do it "
                "anyway. It is the part that empties you enough for the vacuum "
                "to work at all.",
        "meta": ["10-15 minutes", "Standing", "Nose in, mouth out"],
        "sideways": "If the stomach will not draw in, there is still air in "
                    "your lungs. Empty them further before you try again.",
        "short_use": "Lion's breath and a stomach vacuum. Standing.",
        "video_id": "gdxTwKYmF5Y",
    },
    {
        "slug": "qi-gong-breathing",
        "name": "Qi Gong breathing",
        "pillar": "relaxing",
        "cadence": None,
        "purpose": "A standing breath with a picture that travels. Slow, and "
                   "you can run it anywhere you can stand still.",
        "steps": [
            "Stand with your feet planted and your knees slightly bent, so you "
            "are solid rather than stiff.",
            "Breathe in through the nose: belly, chest, head.",
            "As you fill, picture a warm gold light coming in with the air.",
            "Ujjayi exhale, and follow the light all the way down to the tips "
            "of your toes.",
            "Breathe in again and bring it back up to the top of your head.",
            "Keep it circulating. One to five minutes, longer if you want it.",
        ],
        "note": "Your hands help. Let them travel with the light, down as you "
                "exhale and up as you inhale, and the picture holds more "
                "easily.",
        "meta": ["1-5 minutes", "Standing", "Nose in, nose out"],
        "sideways": "If the picture will not come, run the breath on its own. "
                    "The slow Ujjayi exhale is doing most of the work either "
                    "way.",
        "short_use": "Standing, slow, with a travelling picture.",
        "video_id": "w4MdbO3J7L8",
    },
    {
        "slug": "dynamic-breathwork",
        "name": "Dynamic breathwork",
        "pillar": "activating",
        "signature": True,
        "cadence": None,
        "purpose": "The big one in this pillar, and Ben Holt's own. Built on the "
                   "Wim Hof method, which came from Tummo, the Tibetan practice "
                   "monks use to heat the body in the Himalayas. Forty "
                   "controlled breaths, then holds.",
        "before": [
            "Set up first. Lie down, or sit somewhere soft. Water, a blanket "
            "and comfortable clothes within reach.",
            "If you faint easily, or you have had panic attacks, do this one "
            "lying down.",
            "Mornings. It is a stimulant, and done late it will sit between you "
            "and sleep.",
            "Always finish with something from the relaxing pillar. This winds "
            "the system up on purpose and you want it back down before you "
            "carry on with the day.",
            "If holding your breath frightens you, or you are working with "
            "severe trauma, leave this one for now and stay with the relaxing "
            "pillar. It will still be here later.",
        ],
        "steps": [
            "Forty controlled breaths through the mouth. Fully in, then let it "
            "fall out. Do not push the exhale.",
            "After the fortieth, breathe everything out and hold on empty.",
            "Stay completely still to begin with.",
            "When the stress response arrives, shake your hands out and move "
            "however you need to. Keep holding.",
            "Big breath in, then sip a little more air on top of it. Hold at "
            "the top.",
            "Let it go on an Om. That is one round.",
            "The recording guides the rounds and the timing. Follow it.",
            "Finish with a relaxing technique, then lie still for five or ten "
            "minutes.",
        ],
        "note": "The Om at the end is not decoration. It stimulates the vagus "
                "nerve and settles the body and mind back together, which is "
                "why this practice leaves you ready to meditate rather than "
                "wired.",
        "note2": "Daily is fine, and it is best first thing. Practised every "
                 "morning it changes what your body can do.",
        "meta": ["About 20 minutes", "Lying down or sitting", "Mouth, then holds"],
        "sideways": "The nervous, anxious wave on the empty hold is the "
                    "hormesis arriving, not something going wrong. Stay still, "
                    "then shake your hands and move if you need to, and keep "
                    "holding until the big inhale. You can do more than you "
                    "think you can.",
        "short_use": "Forty breaths and holds. The big one in this pillar.",
        "videos": [
            ("Explanation", "Watch this one before anything else.",
             "ZxeOOSXIsiY"),
            ("The flow, beginner", "Start here. The track guides you through.",
             "JcH1Wg29NNE"),
            ("The flow, advanced", "Once the beginner track is comfortable.",
             "JvScA-ml6lg"),
        ],
        "video_id": None,
    },
    {
        "slug": "sonic-neural",
        "name": "Sonic Neural Breathwork",
        "pillar": "freedom",
        "signature": True,
        "cadence": None,
        "purpose": "The deep one, and Ben Holt's own. Fifty-five minutes of "
                   "connected breathing to music, run as a ceremony. The "
                   "thinking mind quiets down and "
                   "the intuitive one takes over, which is why people describe "
                   "it as mystical, or as the closest thing to a psychedelic "
                   "experience with nothing in your system. One session can "
                   "change how you see something for good.",
        "before": [
            "Done with a facilitator, in a retreat or ceremony setting. Set "
            "aside about two and a half hours: there is time either side for "
            "arriving and for coming back down.",
            "A few conditions mean this is not the right practice for you. Sit "
            "it out if any of these apply: severe heart problems "
            "or a pacemaker; seizures or epilepsy; a detached retina or "
            "glaucoma; aneurysms in your immediate family; fainting easily; "
            "prescription blood thinners; severely low, high or uncontrolled "
            "blood pressure; a history of severe panic attacks; psychosis or "
            "schizophrenia; pregnancy; stroke, TIA or other neurological "
            "conditions; uncontrolled bipolar disorder; osteoporosis.",
            "Severe trauma is best worked with alongside someone qualified for "
            "it.",
            "Once a week is the ceiling. Once a month is closer to right.",
        ],
        "steps": [
            "Lie flat on your back with something over your eyes. Water and "
            "chapstick in reach, good headphones on.",
            "Be on your own, or with someone who understands what this is.",
            "Set an intention. What you are letting go of, and what you are "
            "bringing in.",
            "Breathe in through the nose and out through the mouth, belly then "
            "chest. Then move to breathing in and out through the mouth.",
            "Ninety percent in, ninety percent out. No pause at the top or the "
            "bottom. Keep it circular.",
            "For the first ten to fifteen minutes your head will list every "
            "reason to stop. Keep breathing. After that it goes on autopilot "
            "and you can breathe however you need to.",
            "Move and make noise. Shake, rock, scream into a pillow, cry. That "
            "is the release, not a distraction from it.",
            "The track runs 55 minutes. Come back slowly: fingers and toes, "
            "wrists and ankles, roll to one side, sit up with your eyes closed.",
        ],
        "note": "Tingling, a dry mouth and cramping hands are normal, "
                "especially the first time, and they pass. Most first sessions "
                "are sensory rather than emotional. That is not a failure, it "
                "is the usual way in.",
        "note2": "Some sessions are sensory, some are a release, and some are "
                 "neither: a wide clear view of your own life from somewhere "
                 "above it. There is no goal here and no way to do it wrong.",
        "note3": "Integrate afterwards. Water, bare feet on the ground, food, "
                 "time away from a screen, and no rushing back to work.",
        "meta": ["About 2.5 hours", "Lying down", "Nose in, then mouth"],
        "sideways": "If it tips into panic, this is a roller coaster you can "
                    "get off. Slow the breath down and take it through the "
                    "nose. It settles from there.",
        "short_use": "The deep one. A facilitated ceremony.",
        "videos": [
            ("Explanation", "Watch this one before anything else.",
             "lPg8XpXbwG0"),
            ("The flow, 55 minutes with music", "This is the practice itself.",
             "H-QRfoAjS6o"),
            ("Grounding", "Do this one afterwards, every time.",
             "RPsYpjx2Ts8"),
        ],
        "video_id": None,
    },
]

# Techniques named in the training whose mechanics are not captured. They get a
# row on their pillar page and no page of their own until the content exists.
#
# Flags for whoever writes these:
#   Buteyko  — resolved. His video teaches the breath-hold walk, which is a
#              genuine Buteyko exercise and is reduced breathing, not
#              hyperventilation. It sits in activating because the training puts
#              it there and because he frames the hold as a deliberate stress.
#   Kapalabhati vs Bhastrika — also resolved. He states the difference himself:
#              Kapalabhati forces the exhale only, Bhastrika (breath of fire)
#              forces both halves. The site teaches Bhastrika.
#   Dynamic breathwork and Sonic Neural are deliberately absent from this
#              library and get their own dedicated pages elsewhere. Dynamic has a
#              real risk profile (fainting history, panic attacks, severe trauma,
#              claustrophobia or fear of holding the breath, fragile nervous
#              system), must be followed by a relaxing technique, and belongs in
#              the morning — all of which goes in the "before" field, which the
#              template already renders above the steps.
PENDING = []

# ---------------------------------------------------------------------------
# The state map — the 2am entry. One state, one technique, no ranking logic.
# Ordered most acute first. Add rows as techniques land; nothing restructures.
# ---------------------------------------------------------------------------

# The state lines that used to head the index rows are gone: the card heading
# is the technique name and the pills carry the state.

# ---------------------------------------------------------------------------
# Feeling pills. Multi-select; selecting none shows everything, so the one-click
# path from the state list is unchanged. Keep this list short — a filter with
# fifteen options is not a filter.
#
# TAGS is derived from the approved purpose and state copy, nothing invented.
# ---------------------------------------------------------------------------

FEELINGS = [
    "Anxious",
    "Angry",
    "Can't sleep",
    "Under pressure",
    "Wired",
    "Scattered",
    "Breathing shallow",
    "Carrying something",
    "Flat",
    "Before training",
    "Cold",
]

TAGS = {
    "foundational-breath": ["Anxious", "Angry", "Breathing shallow"],
    "turtle-breath": ["Can't sleep"],
    "box-breathing": ["Under pressure", "Scattered", "Angry"],
    "4-3-6": ["Anxious", "Under pressure"],
    "nadi-shodhana": ["Wired", "Scattered", "Can't sleep"],
    "full-fill": ["Breathing shallow", "Anxious", "Can't sleep"],
    "cleansing-breath": ["Anxious", "Under pressure", "Can't sleep",
                         "Carrying something"],
    "qi-gong-breathing": ["Wired", "Scattered"],
    "priming-breath": ["Flat", "Before training"],
    "breath-of-fire": ["Flat", "Cold", "Before training"],
    "kundalini-bhastrika": ["Flat", "Before training"],
    "kapalabhati": ["Flat"],
    "igniter-breath": ["Flat", "Cold", "Before training"],
    "twisting-breath": ["Before training", "Flat"],
    "heart-opening-breath": ["Carrying something", "Angry", "Flat"],
    "buteyko-breathing": ["Anxious", "Under pressure"],
    "digestion-igniter": ["Flat"],
    "dynamic-breathwork": ["Flat", "Before training"],
    # Sonic Neural is deliberately untagged. It is a facilitated ceremony and
    # must never surface as the answer to a feeling someone has right now.
}

# ---------------------------------------------------------------------------
# Content that comes from the course videos rather than the cards brief. Both
# render only when populated, exactly like the "before" block — an empty entry
# means the section is absent from the page, never a placeholder.
#
#   FEELS    slug -> one sentence, second person, on how it lands in the body
#   BENEFITS slug -> list of short benefit lines ("Enhances vitality")
#
# Everything below is empty because it is not in the cards brief or the
# workbook. Do not fill it from general knowledge — it has to come from the
# source material.
# ---------------------------------------------------------------------------

# Guided meditations. One per technique eventually, sitting under the technique
# video. slug -> (youtube id, whose recording it is).
#   "ben"  - Ben Holt's own guided version
#   "clay" - a Clay & Air recording, credited to us
# Only cleansing breath has one so far. Add a line here as each is recorded and
# it appears on that page automatically.
MEDITATIONS = {
    "cleansing-breath": ("bKAwu9Yr-Gk", "ben"),
}

MEDITATION_CAPTION = {
    "ben": "Ben Holt's guided version. Follow along with it.",
    "clay": "A Clay & Air recording. Follow along with it.",
}

FEELS = {
    "foundational-breath":
        "The drop comes on the exhale, not the inhale. By the third round your "
        "shoulders are lower than you left them and the noise in your head has "
        "thinned out.",
    "box-breathing":
        "The count is the point. Five numbers is just enough to hold your "
        "attention, and while it is holding your attention it is not on the "
        "room. Things get quiet from the outside in.",
    "turtle-breath":
        "It arrives in stages rather than all at once. Each step up the ladder "
        "takes a bit more of the day with it, and the last few rounds are the "
        "ones that put you out.",
    "nadi-shodhana":
        "It settles without sedating. The static clears, and where that leaves "
        "you depends on when you run it. Clear enough to work in the "
        "afternoon, quiet enough for bed at night.",
    "4-3-6":
        "Easy to keep going, which is the whole point. It is the one you can "
        "run for ten minutes without it turning into a job, and the long exhale "
        "does the rest.",
    "cleansing-breath":
        "Slower to arrive than the counted techniques. The change tends to show "
        "up around the point the cauldron feels empty, and it keeps going after "
        "you stop.",
    "kundalini-bhastrika":
        "The arms are the hard part. Somewhere past a minute the burn in your "
        "shoulders takes over and the breathing starts running itself.",
    "dynamic-breathwork":
        "Tingling in the hands and the face after the first round, then a wave "
        "of nervous anxiety on the empty hold. That wave is the whole point. "
        "Past it you come out light, warm and very awake.",
    "sonic-neural":
        "The first ten minutes are work and your head argues the whole way. "
        "Then it stops arguing and something else takes over. Most first times "
        "are sensory rather than emotional, tingling and cramping hands, which "
        "is the usual way in. Later ones can go somewhere else entirely.",
    "digestion-igniter":
        "Odd, and unmistakable. You feel the vacuum up under your ribs rather "
        "than in the stomach muscles, and standing up on the inhale is the part "
        "that wakes you.",
    "qi-gong-breathing":
        "Steady rather than sedating. The stance is half of it, and you finish "
        "more awake than you started.",
    "kapalabhati":
        "Your stomach does the work and you feel it there first. Past five "
        "minutes it goes very quiet.",
    "igniter-breath":
        "Heat, fast. Three breaths in and you feel it in your face. As good for "
        "shifting a stuck head as a cold body.",
    "twisting-breath":
        "Your stomach is doing most of it. It also puts you somewhere your body "
        "does not usually go, which is half the point.",
    "heart-opening-breath":
        "Loud, and faintly ridiculous for the first minute. Then it stops being "
        "ridiculous and you notice how much you were holding on to.",
    "breath-of-fire":
        "Heat first, then your stomach starts to burn. Afterwards there is a "
        "lightness that takes a minute to settle.",
    "buteyko-breathing":
        "It pulls you out of your head and into your legs. By the second or "
        "third hold the chatter has stopped and you are just counting steps.",
    "priming-breath":
        "You feel it fast. Warm, awake, and buzzing slightly, the way you do "
        "after the first minute of a hard walk.",
    "full-fill":
        "The stack does something a single breath does not. By the hold you are "
        "already further down than one round of foundational breath takes you, "
        "and the sigh finishes it.",
}

# Benefits shared by everything in the pillar. A technique with its own list in
# BENEFITS overrides this; anything else falls back to it.
# Appended to every technique in the pillar, after its own lines, so the
# physiological benefits appear on every card rather than only where they were
# written out longhand.
PILLAR_BENEFITS = {
    "relaxing": [
        "Lowers blood pressure and brings inflammation down",
    ],
    "activating": [
        "Boosts immunity and brings inflammation down",
    ],
}

BENEFITS = {
    "foundational-breath": [
        "The base every other technique here is built on",
        "Settles the fight-or-flight response",
        "Slows the heart rate",
        "Works anywhere, in under three minutes",
    ],
    "box-breathing": [
        "Holds your attention on the count and off the room",
        "Settles the fight-or-flight response",
        "Slows the heart rate",
        "Steady enough to run in the middle of something",
    ],
    "nadi-shodhana": [
        "Evens out both sides",
        "Settles the fight-or-flight response",
        "Slows the heart rate",
        "Works before sleep, or before anything that needs focus",
    ],
    "full-fill": [
        "Goes deeper than a single round of foundational breath",
        "Settles the fight-or-flight response",
        "Slows the heart rate",
        "Scales: more breaths before the hold, stronger effect",
    ],
    "buteyko-breathing": [
        "Runs while you are moving, so it fits a walk to work",
        "Gets you out of your head and into your body",
        "Builds tolerance for altitude and effort over time",
        "A small deliberate stress, the useful kind",
    ],
    "priming-breath": [
        "Gets the blood moving",
        "Expands and contracts the lungs hard",
        "Wakes you up without reaching for coffee",
        "Leaves you alert enough to sit and meditate afterwards",
    ],
    "qi-gong-breathing": [
        "Energizing and settling at the same time",
        "The rooted stance does half the work",
        "Runs anywhere you can stand still",
        "One to five minutes is enough",
    ],
    "kundalini-bhastrika": [
        "Breath of fire with a lot more load",
        "Builds heat fast",
        "Works the shoulders hard",
        "Wakes the body up before training",
    ],
    "dynamic-breathwork": [
        "Brings inflammation down",
        "Wakes the immune system up",
        "Boosts stamina and athletic performance by clearing CO2",
        "Alkalises the blood",
        "Builds lung capacity, which tracks with longevity",
        "Leaves you ready to meditate rather than wired",
    ],
    "sonic-neural": [
        "A mystical or psychedelic experience, with nothing in your system",
        "Discharges what the body has been holding on to",
        "Brings up what got buried, so it can be dealt with",
        "One session can change the course of something",
    ],
    "digestion-igniter": [
        "Massages the organs in the gut",
        "Gets the digestion moving",
        "Works the deep abdominal muscles",
        "A morning practice, and it wakes you up",
    ],
    "kapalabhati": [
        "Empties the lungs further than an ordinary breath",
        "Works the stomach hard",
        "Costs less than breath of fire, so you can run it longer",
        "Wakes the body up",
    ],
    "igniter-breath": [
        "Warms you up after cold water",
        "Gets you out of a stuck head",
        "Short enough to fit anywhere",
        "Wakes the body up before training",
    ],
    "twisting-breath": [
        "Warms you up before training",
        "Works the core",
        "Puts breath and movement on the same beat",
        "Takes you out of your usual range",
    ],
    "heart-opening-breath": [
        "Gets it out through the voice, which is the fastest way",
        "Opens the heart space",
        "Clears the deck before the day starts",
        "Forgiveness on purpose, which changes how the day goes",
    ],
    "breath-of-fire": [
        "Builds heat fast",
        "Wakes the body up in the morning",
        "Works after cold water, or before training",
        "Your stomach does real work",
    ],
    "4-3-6": [
        "The exhale runs longest, which is what settles you",
        "Easy enough to keep running for a long stretch",
        "Settles the fight-or-flight response",
        "Works sitting or lying down",
    ],
    "cleansing-breath": [
        "Cleanses and nourishes every cell on the way through",
        "Settles the fight-or-flight response",
        "Closes out a hard day, or a hard session",
        "Gives your attention somewhere to be",
    ],
    "turtle-breath": [
        "Slows the breath until the nervous system unwinds",
        "Built for lying down at the end of the day",
        "Settles the fight-or-flight response",
        "Slows the heart rate",
    ],
}

# ---------------------------------------------------------------------------
# The basics. Renders above the steps on the start-here technique only.
# Sourced from the course videos and the practitioner's own notes.
# ---------------------------------------------------------------------------

BASICS_INTRO = (
    "You have been breathing badly all day and it has been feeding the thing "
    "you are trying to fix. Sharp and shallow, high in the chest, through the "
    "mouth. That is the pattern your body reads as a threat, so it keeps "
    "you braced, and being braced makes you breathe that way again. Five things "
    "break the loop. Get them right and every other technique here works."
)

BASICS = {
    "foundational-breath": [
        ("Nose, not mouth",
         "In through the nose and out through the nose. The nose filters the air "
         "and slows it down; mouth breathing does the opposite and your body "
         "reads it as a stress signal."),
        ("Belly out on the way in",
         "Put a hand flat below your navel. The belly should push into your hand "
         "on the inhale and come back in on the exhale, not your chest "
         "rising first. If the hand does not move, nothing else on this page will "
         "work properly."),
        ("Slow and low",
         "Five seconds in, six seconds out. The exhale is the half that does the "
         "work. That is where the body lets go, so keep it the "
         "longer one."),
        ("The Ujjayi exhale",
         "Open your mouth and breathe out like you are fogging a pane of glass. "
         "Feel the slight squeeze at the back of the throat. Now do the same "
         "thing with your mouth closed. It sounds like the ocean, quiet enough "
         "that nobody nearby will notice, and having something to hear keeps you "
         "with the breath instead of in your head."),
        ("If the air will not go low",
         "Put your hands behind your head. It opens the front of the chest and "
         "the breath drops on its own. Do it a few times and it starts happening "
         "without the hands."),
    ],
}

BY_SLUG = {t["slug"]: t for t in TECHNIQUES}

# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Newsreader:wght@400;600'
         '&amp;family=IBM+Plex+Sans:wght@400;500&amp;family=IBM+Plex+Mono:wght@500'
         '&amp;display=swap" rel="stylesheet">')


def cadence_html(parts, tail=None, cls=""):
    if not parts:
        return ""
    joined = ' <span class="dot">&middot;</span> '.join(parts)
    if tail:
        joined += " " + tail
    return f'<span class="cadence {cls}">{joined}</span>'


def meta_html(parts):
    return ' <span class="dot">&middot;</span> '.join(parts)


# Analytics. Plausible sets no cookies, so there is no consent banner to
# design, and it takes custom events, which is the point: the pill somebody
# taps at 2am is the most useful number this site can produce. Set
# ANALYTICS_ON to False and no script is emitted anywhere.
ANALYTICS_ON = True

PLAUSIBLE = """
  <!-- Privacy-friendly analytics by Plausible -->
  <script async src="https://plausible.io/js/pa-VSqWa9Bp7sjkwzZ91EFkO.js"></script>
  <script>
  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
  plausible.init()
  </script>"""


def analytics():
    return PLAUSIBLE if ANALYTICS_ON else ""


# Social profiles. Each one feeds two places: the footer column and the
# Organization schema's sameAs, which is how a search or answer engine ties
# the site and the accounts into one entity. Add a line and both update.
SOCIALS = [
    ("Instagram", "https://www.instagram.com/clayandairnow/"),
    ("YouTube", "https://www.youtube.com/@clayandairnow"),
    ("TikTok", "https://www.tiktok.com/@clayandairnow"),
]


SITE_URL = "https://clayandair.com"
SITE_NAME = "Clay & Air"
SITE_TAGLINE = "Breathwork for men who hold it together."


def canonical(path):
    """Clean URLs. Netlify serves /x and /x.html with a 200 either way, so
    without a canonical every page exists at two addresses and the ranking
    signal splits between them."""
    p = path.replace("index.html", "").replace(".html", "")
    return f"{SITE_URL}/{p}".rstrip("/") if p else SITE_URL


def jsonld(obj):
    return ('\n  <script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


def org_schema():
    return {
        "@type": "Organization",
        "@id": f"{SITE_URL}/#org",
        "name": SITE_NAME,
        "url": SITE_URL,
        "description": SITE_TAGLINE,
        "logo": f"{SITE_URL}/assets/share.png",
        "founder": {"@type": "Person", "name": "Don Page"},
        "sameAs": [u for _, u in SOCIALS],
    }


def crumbs(trail):
    """trail is [(name, path), ...] ending at the current page."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             "item": canonical(p)}
            for i, (n, p) in enumerate(trail)
        ],
    }


def head(title, desc, depth, path, schema=None):
    up = "../" * depth
    url = canonical(path)
    graph = [org_schema(), {
        "@type": "WebSite", "@id": f"{SITE_URL}/#site",
        "url": SITE_URL, "name": SITE_NAME,
        "publisher": {"@id": f"{SITE_URL}/#org"},
    }]
    graph += schema or []
    ld = jsonld({"@context": "https://schema.org", "@graph": graph})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#EDE7DC">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE_URL}/assets/share.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Clay &amp; Air, breathwork for men who hold it together">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE_URL}/assets/share.png">
  <link rel="icon" href="{up}assets/favicon.ico" sizes="any">
  <link rel="icon" href="{up}assets/favicon-32.png" type="image/png">
  <link rel="icon" href="{up}assets/mark-01-micro.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{up}assets/favicon-32.png">
  {FONTS}
  <link rel="stylesheet" href="{up}assets/breath.css">{analytics()}{ld}
</head>
<body>"""


def header(depth, current=None):
    up = "../" * depth
    def nav(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'<a href="{up}{href}"{cur}>{label}</a>'
    return f"""
<header class="site-header">
  <div class="wrap">
    <a class="lockup" href="{up}index.html" aria-label="Clay &amp; Air">
      <img src="{up}assets/lockup-horizontal-compact-outlined.svg"
        alt="Clay &amp; Air" width="171" height="60">
    </a>
    <nav class="site-nav">
      {nav('index.html', 'Library', 'states')}
      {nav('relaxing/index.html', 'Relaxing', 'relaxing')}
      {nav('activating/index.html', 'Activating', 'activating')}
      {nav('freedom/index.html', 'Freedom', 'freedom')}
      {nav('sessions.html', 'Sessions', 'sessions')}
    </nav>
  </div>
</header>"""


def footer(depth):
    """Follows ui_kits/website/Chrome.jsx > Footer."""
    up = "../" * depth
    social_col = ""
    if SOCIALS:
        rows = "\n".join(
            f'          <li><a href="{u}" rel="me noopener">{n}</a></li>'
            for n, u in SOCIALS)
        social_col = f"""
      <div class="footer-col">
        <p class="label label--tertiary">Follow</p>
        <ul>
{rows}
        </ul>
      </div>"""
    return f"""
<footer class="site-footer ca-invert">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <img class="footer-lockup" src="{up}assets/lockup-reversed-outlined.svg"
          alt="Clay &amp; Air" width="475" height="167">
        <p class="label label--tertiary lockup-line">Breath <span class="dot">&middot;</span> Discipline <span class="dot">&middot;</span> Daylight</p>
        <p class="bio">Breathwork for men who hold it together.</p>
      </div>
      <div class="footer-col">
        <p class="label label--tertiary">Practice</p>
        <ul>
          <li><a href="{up}relaxing/index.html">Relaxing</a></li>
          <li><a href="{up}activating/index.html">Activating</a></li>
          <li><a href="{up}freedom/index.html">Freedom</a></li>
          <li><a href="{up}relaxing/foundational-breath.html">Start here</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <p class="label label--tertiary">Source</p>
        <ul>
          <li><a href="https://www.awakenedbreath.org/" rel="noopener">Ben Holt</a></li>
          <li><a href="https://www.awakenedbreath.org/" rel="noopener">Awakened Breath</a></li>
        </ul>
      </div>{social_col}
    </div>
    <div class="footer-bottom">
      <p class="disclaimer">Techniques taught by Ben Holt. If you have a heart or
      lung condition, high or low blood pressure, epilepsy, or you are pregnant,
      talk to a doctor before holding your breath.</p>
      <span class="copyright">&copy; 2026 Clay &amp; Air</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def video_block(t, depth):
    """Placeholder plate until a real recording exists. Drop the ID into
    video_id and the iframe replaces the plate."""
    label = re.sub("<[^>]+>", "", t.get("plain_name", t["name"])).upper()
    def embed(vid, label, caption):
        return f"""
      <figure class="video">
        <p class="label">{label}</p>
        <div class="video-plate video-plate--embed">
          <iframe src="https://www.youtube.com/embed/{vid}"
            title="{t['name']}" loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen></iframe>
        </div>
        <figcaption class="small tertiary">{caption}
        <a href="https://www.youtube.com/watch?v={vid}" rel="noopener">Watch it on
        YouTube</a>.</figcaption>
      </figure>"""

    # an explicit ordered set of recordings wins
    reel = t.get("videos")
    if not reel and t.get("video_id"):
        reel = [("The technique", "Not playing?", t["video_id"])]
        med = MEDITATIONS.get(t["slug"])
        if med:
            reel.append(("Guided meditation",
                         MEDITATION_CAPTION[med[1]], med[0]))
    if reel:
        if len(reel) == 1:
            return embed(reel[0][2], "Watch", reel[0][1])
        out = []
        for i, (lab, cap, vid) in enumerate(reel, 1):
            label = f'{i:02d} <span class="dot">&middot;</span> {lab}'
            out.append(embed(vid, label, cap))
        return "\n".join(out)

    # No recording yet. A slim marker, not an empty 16:9 hole above the steps.
    return f"""
      <p class="video-pending">Video: {label} <span class="dot">&middot;</span> to come</p>"""


def iso_duration(text):
    """Best effort ISO 8601 duration from the meta line, for HowTo totalTime.
    Returns None when the line is reps rather than minutes."""
    m = re.search(r"(\d+)(?:\s*-\s*(\d+))?\+?\s*minutes?", text, re.I)
    if m:
        return f"PT{m.group(2) or m.group(1)}M"
    m = re.search(r"(\d+(?:\.\d+)?)\s*hours?", text, re.I)
    if m:
        return f"PT{int(float(m.group(1)) * 60)}M"
    m = re.search(r"(\d+)\s*seconds?", text, re.I)
    if m:
        return f"PT{m.group(1)}S"
    return None


def technique_schema(t):
    """A breath technique is a procedure with ordered steps, so HowTo is the
    honest match. It is also what makes the steps eligible to be quoted back
    by an assistant that is asked how to do one of these."""
    path = f"{t['pillar']}/{t['slug']}.html"
    url = canonical(path)
    steps = [re.sub("<[^>]+>", "", s).strip() for s in t["steps"]]
    how = {
        "@type": "HowTo",
        "@id": f"{url}#howto",
        "name": re.sub("<[^>]+>", "", t.get("plain_name", t["name"])),
        "description": re.sub("<[^>]+>", "", t["purpose"]),
        "url": url,
        "inLanguage": "en",
        "isPartOf": {"@id": f"{SITE_URL}/#site"},
        "publisher": {"@id": f"{SITE_URL}/#org"},
        "step": [
            {"@type": "HowToStep", "position": i + 1, "name": s.split(".")[0][:60],
             "text": s, "url": f"{url}#step{i + 1}"}
            for i, s in enumerate(steps)
        ],
    }
    dur = iso_duration(t["meta"][0])
    if dur:
        how["totalTime"] = dur
    out = [how]
    vids = t.get("videos") or ([("Watch", "", t["video_id"])] if t.get("video_id") else [])
    for label, caption, vid in vids:
        out.append({
            "@type": "VideoObject",
            "name": f"{re.sub('<[^>]+>', '', t['name'])} - {label}",
            "description": re.sub("<[^>]+>", "", caption or t["purpose"]),
            "thumbnailUrl": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "uploadDate": "2026-01-01",
            "publisher": {"@id": f"{SITE_URL}/#org"},
        })
    label = PILLARS[t["pillar"]][0].split(chr(183))[1].strip()
    out.append(crumbs([("Breath library", "index.html"),
                       (label, f"{t['pillar']}/index.html"),
                       (re.sub("<[^>]+>", "", t["name"]), path)]))
    return out


def technique_page(t):
    depth = 1
    up = "../" * depth
    pillar_label, pillar_dir = PILLARS[t["pillar"]]
    plain = re.sub("<[^>]+>", "", t.get("plain_name", t["name"]))

    # Cadence notation is deliberately not rendered anywhere on the site.
    # The data stays in TECHNIQUES so it can be switched back on in one place.

    before = ""
    if t.get("before"):
        items = "\n".join(f"          <li>{i}</li>" for i in t["before"])
        before = f"""
      <div class="before">
        <p class="label">Before you start</p>
        <ul>
{items}
        </ul>
      </div>"""

    steps = "\n".join(
        f'          <li><span class="num">{i:02d}</span>'
        f'<span class="text">{s}</span></li>'
        for i, s in enumerate(t["steps"], 1)
    )

    # the correction line no longer gets its own section — it sits with the note,
    # under the steps, where it is actually needed
    note_bits = []
    if t.get("note"):
        note_bits.append(t["note"])
    if t.get("note2"):
        note_bits.append(t["note2"])
    if t.get("note3"):
        note_bits.append(t["note3"])
    if t.get("sideways"):
        note_bits.append(t["sideways"])
    note = ""
    if note_bits:
        paras = "\n".join(f'        <p class="small muted">{b}</p>'
                          for b in note_bits)
        note = f'\n      <div class="note">\n{paras}\n      </div>'

    tags = ""
    if TAGS.get(t["slug"]):
        chips = "".join(f'<span class="tag">{f}</span>' for f in TAGS[t["slug"]])
        tags = f'\n      <p class="tags">{chips}</p>'

    feels = ""
    if FEELS.get(t["slug"]):
        feels = f"""
      <div class="block">
        <p class="label">How it lands</p>
        <p>{FEELS[t['slug']]}</p>
      </div>"""

    benefits = ""
    blist = list(BENEFITS.get(t["slug"], []))
    for tail in PILLAR_BENEFITS.get(t["pillar"], []):
        if tail not in blist:
            blist.append(tail)
    if blist:
        items = "\n".join(f"          <li>{b}</li>" for b in blist)
        benefits = f"""
      <div class="benefits">
        <p class="label">What it does</p>
        <ul>
{items}
        </ul>
      </div>"""

    basics = ""
    if BASICS.get(t["slug"]):
        rows = "\n".join(
            f"""          <div class="basic">
            <p class="label">{title}</p>
            <p>{body}</p>
          </div>"""
            for title, body in BASICS[t["slug"]]
        )
        basics = f"""
      <section class="basics">
        <p class="label">The basics</p>
        <p class="basics-intro">{BASICS_INTRO}</p>
        <div class="basics-list">
{rows}
        </div>
      </section>"""

    start = ""
    if t.get("start_here"):
        start = '\n      <p class="start-here">Start here</p>'
    elif t.get("signature"):
        start = ('\n      <p class="start-here">Ben Holt signature '
                 'technique</p>')

    links = ""
    if t.get("links"):
        rows = "\n".join(
            f'          <li><a href="{href}" rel="noopener">{text}</a></li>'
            for text, href in t["links"]
        )
        links = f"""
      <div class="benefits">
        <p class="label">Also</p>
        <ul>
{rows}
        </ul>
      </div>"""

    progression = ""
    if t.get("progression"):
        progression = f"""
      <div class="block block--tight">
        <p class="label">When that is easy</p>
        <p class="small muted">{t['progression']}</p>
      </div>"""

    siblings = [x for x in TECHNIQUES
                if x["pillar"] == t["pillar"] and x["slug"] != t["slug"]
                and not x.get("placeholder")]
    # the quiet close. Someone who read to the bottom of a technique is the
    # only person on the site who has shown you anything. One line, no banner.
    if t["slug"] == "sonic-neural":
        next_step = f"""
      <div class="next-step">
        <p class="label">Sitting one of these</p>
        <p>This one is not a solo practice. It runs at the long workshop and
        on retreat, with people holding the room. Say the word and you will
        hear when the next one is on.</p>
        <a class="btn btn--primary"
          href="{up}sessions.html?about=retreat">Tell me when the next one is</a>
      </div>"""
    else:
        next_step = f"""
      <div class="next-step">
        <p class="label">If you want a hand with it</p>
        <p>This one works on your own. Some of it lands harder with someone
        in the room, and that is what the workshops are for.</p>
        <a class="btn btn--primary" href="{up}sessions.html">Sessions</a>
      </div>"""

    sib_block = ""
    if siblings:
        sib_rows = "\n".join(
            f"""        <li><a href="{s['slug']}.html">
          <span class="dur">{s['meta'][0]}</span>
          <span class="body">
            <span class="name">{s['name']}</span>
            <span class="use">{s['short_use']}</span>
          </span>
          <span class="aside"><span class="state-meta">{s['meta'][1]}</span></span>
        </a></li>"""
            for s in siblings
        )
        sib_block = f"""
    <hr class="rule">

    <section class="section section--tight">
      <div class="wrap">
        <p class="label">The rest of this pillar</p>
        <ul class="tech-list">
{sib_rows}
        </ul>
      </div>
    </section>"""

    # search snippets are cut around 155 characters, so budget for the meta
    # tail and trim the purpose on a word boundary to fit
    tail = f" {t['meta'][0]}, {t['meta'][1].lower()}."
    desc = re.sub('<[^>]+>', '', t['purpose'])
    room = 155 - len(tail)
    if len(desc) > room:
        cut = desc[:room]
        # prefer the last complete sentence, so the snippet never ends on a
        # fragment; fall back to a word boundary only if there is no sentence
        end = cut.rfind('. ')
        desc = (cut[:end + 1] if end > 40
                else cut.rsplit(' ', 1)[0].rstrip('.,;:') + '.')
    desc += tail
    tpath = f"{t['pillar']}/{t['slug']}.html"
    use = re.sub('<[^>]+>', '', t['short_use']).rstrip('.')
    title = f'{plain}: {use[0].lower() + use[1:]} - Clay & Air'
    if len(title) > 62:
        title = f'{plain} - Clay & Air'
    return f"""{head(title, desc, depth, tpath, technique_schema(t))}
{header(depth, t['pillar'])}

<main>
  <article class="technique">
    <div class="wrap">
      <p class="label">{pillar_label}</p>{start}
      <h1>{t['name']}</h1>
      <p class="meta-row"><span class="meta-items">{meta_html(t['meta'])}</span></p>
      <p class="purpose">{t['purpose']}</p>{tags}
{before}{basics}
{video_block(t, depth)}
      <div class="pattern">
        <p class="label">The pattern</p>
        <ol class="steps">
{steps}
        </ol>
      </div>{note}{progression}{feels}{benefits}
{next_step}
    </div>
{sib_block}
  </article>
</main>
{footer(depth)}"""


# ---------------------------------------------------------------------------
# Flashcard backs. The line for each step is its first sentence, which turns
# out to be the instruction with the explanation stripped off. Where that
# reads badly, or the technique carries more steps than a card face can hold,
# an override goes here and wins.
# ---------------------------------------------------------------------------

FLASH = {
    "foundational-breath": [
        "In through the nose: belly, chest, then up behind the eyes",
        "Hold 5 to 10 seconds at the top",
        "Open your mouth and sigh it all the way out",
        "Ujjayi exhale instead anywhere you cannot make noise",
        "Repeat",
    ],
    "cleansing-breath": [
        "Sitting or lying down",
        "In through the nose, a golden light coming in with the air",
        "Hold it at the top",
        "Ujjayi exhale, the tension leaving as dark purple smoke",
        "The heavy part settles in a cauldron low in the belly",
        "Breathe the light down into the cauldron and wash it clean",
    ],
    "heart-opening-breath": [
        "Sit or stand with your arms out wide",
        "In through the nose, arms drawing in toward the chest",
        "A green light coming into the heart space as they close",
        "Open the arms and breathe out on a long, audible ah",
        "Shake it out if something comes up",
        "Ten to twenty minutes",
    ],
    "qi-gong-breathing": [
        "Stand with your feet planted and your knees soft",
        "In through the nose: belly, chest, head",
        "A warm gold light coming in with the air",
        "Ujjayi exhale, following it down to the tips of your toes",
        "Breathe in and bring it back to the top of your head",
        "Keep it circulating",
    ],
    "twisting-breath": [
        "Arms out in front, palms together",
        "Twist to one side, breathing in gently through the mouth",
        "At the end, force it all out through the nose, stomach in hard",
        "Twist back the other way, breathing in across",
        "Force it out at the end of that side too",
        "Alternate for about ten minutes",
    ],
    "digestion-igniter": [
        "Stand up",
        "Big breath in through the nose",
        "Lion's breath out: tongue out, Ujjayi, everything emptied",
        "Hands on your knees with your lungs empty",
        "Move it around while it is held there",
        "Stand and breathe in through the nose when you want air",
    ],
    "dynamic-breathwork": [
        "Forty controlled breaths through the mouth",
        "Breathe everything out and hold on empty",
        "Stay completely still to begin with",
        "Shake out and move when the stress response arrives",
        "Big breath in, sip a little more on top, let it go on an Om",
        "Finish with a relaxing technique and lie still",
    ],
    "sonic-neural": [
        "Flat on your back with something over your eyes",
        "Someone with you who understands what this is",
        "Set an intention",
        "In through the nose, out through the mouth: belly then chest",
        "Ninety percent in, ninety percent out",
        "Move and make noise. The track runs 55 minutes",
    ],
}


def flash_lines(t):
    """The back of the card. Override first, else the instruction clause of
    each step."""
    if t["slug"] in FLASH:
        return FLASH[t["slug"]]
    out = []
    for s in t["steps"]:
        s = re.sub("<[^>]+>", "", s).strip()
        out.append(re.split(r"(?<=[a-z0-9)])\. ", s)[0].rstrip("."))
    return out[:6]


def library_cards():
    """Every technique, as a filterable grid. The card heading is the technique
    name, not a state line: the pills carry the state."""
    order = list(PILLARS)
    cards = sorted(
        (t for t in TECHNIQUES if not t.get("placeholder")),
        key=lambda t: (order.index(t["pillar"]),
                       1 if t.get("signature") else 0,
                       TECHNIQUES.index(t)),
    )
    out = []
    for t in cards:
        if False:
            continue
        label = PILLARS[t["pillar"]][0].split(chr(183))[1].strip()
        tags = "|".join(feel_key(x) for x in TAGS.get(t["slug"], []))
        badge = ""
        if t.get("start_here"):
            badge = '<p class="card-badge"><span class="badge badge--start">Start here</span></p>'
        elif t.get("signature"):
            badge = '<p class="card-badge"><span class="badge badge--signature">Signature</span></p>'
        href = f"{t['pillar']}/{t['slug']}.html"
        lines = "\n".join(f"              <li>{x}</li>" for x in flash_lines(t))
        cid = f"back-{t['slug']}"
        lands = ""
        if FEELS.get(t["slug"]):
            lands = f'\n              <p class="lands">{FEELS[t["slug"]]}</p>'
        feels = TAGS.get(t["slug"], [])
        for_line = ""
        if feels:
            chips = "".join(f"<span>{x}</span>" for x in feels)
            for_line = f'\n              <div class="for">{chips}</div>'
        out.append(f"""        <article class="card tech-card" data-feelings="{tags}">
          <div class="card-head">
            <p class="label">{label}</p>
            <h3><a class="card-link" href="{href}">{t['name']}</a></h3>
          </div>

          <div class="card-body">
            <div class="face face--front">
              <p class="use">{t['short_use']}</p>{lands}{for_line}
            </div>
            <div class="face face--back" id="{cid}" data-off>
              <ol class="flash">
{lines}
              </ol>
            </div>
            {badge}
          </div>

          <div class="card-foot">
            <span class="state-meta">{t['meta'][0]}</span>
            <button type="button" class="turn" aria-expanded="false"
              aria-controls="{cid}"><span>Pattern</span></button>
          </div>
        </article>""")
    return "\n".join(out)


def feel_key(f):
    """Machine key for a feeling. Data attributes carry these, never the
    display label: the label has an apostrophe in it ("Can't sleep") and any
    host that re-serialises the HTML can escape that in a way the attribute
    parser truncates. Netlify's pretty-URL pass did exactly that and silently
    broke the sleep filter in production."""
    return re.sub(r"[^a-z0-9]+", "-", f.lower()).strip("-")


def pill_row():
    pills = "\n".join(
        f'        <button type="button" class="pill" data-feeling="{feel_key(f)}"'
        f' aria-pressed="false">{f}</button>'
        for f in FEELINGS
    )
    return f"""      <div class="pills" role="group" aria-label="Filter by how you feel">
{pills}
        <button type="button" class="pill pill--clear" data-clear hidden>Clear</button>
      </div>"""


FILTER_JS = """<script>
(function () {
  var pills = Array.prototype.slice.call(document.querySelectorAll('.pill[data-feeling]'));
  var rows = Array.prototype.slice.call(document.querySelectorAll('.tech-card'));
  var clear = document.querySelector('.pill--clear');
  var empty = document.querySelector('.library-empty');
  var active = [];

  function apply() {
    var shown = 0;
    rows.forEach(function (row) {
      var has = (row.getAttribute('data-feelings') || '').split('|');
      // OR, not AND: pick everything you are feeling and see all of it. An
      // empty result is the worst thing to hand someone in a bad state.
      var match = active.length === 0 || active.some(function (f) {
        return has.indexOf(f) !== -1;
      });
      row.hidden = !match;
      if (match) { shown++; }
    });
    if (empty) { empty.hidden = shown !== 0; }
    if (clear) { clear.hidden = active.length === 0; }
  }

  // Turn a card over. DESIGN.md bans transforms, so the faces swap in place
  // rather than rotating. They share a grid cell, so the card keeps its
  // height and nothing below it moves.
  function face(card, showBack) {
    var front = card.querySelector('.face--front');
    var back = card.querySelector('.face--back');
    var btn = card.querySelector('.turn');
    if (!front || !back || !btn) { return; }
    if (showBack) {
      front.setAttribute('data-off', '');
      back.removeAttribute('data-off');
    } else {
      back.setAttribute('data-off', '');
      front.removeAttribute('data-off');
    }
    btn.setAttribute('aria-expanded', showBack ? 'true' : 'false');
    btn.firstChild.textContent = showBack ? 'Back' : 'Pattern';
  }

  rows.forEach(function (card) {
    var btn = card.querySelector('.turn');
    if (!btn) { return; }
    btn.addEventListener('click', function () {
      face(card, btn.getAttribute('aria-expanded') !== 'true');
    });
  });

  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      var f = pill.getAttribute('data-feeling');
      var i = active.indexOf(f);
      if (i === -1) { active.push(f); } else { active.splice(i, 1); }
      pill.setAttribute('aria-pressed', i === -1 ? 'true' : 'false');
      rows.forEach(function (c) { face(c, false); });
      apply();
      // Which feeling, and at what hour. No-ops when analytics is off.
      if (i === -1 && window.plausible) {
        window.plausible('Feeling', {
          props: { feeling: f, hour: String(new Date().getHours()) }
        });
      }
    });
  });

  if (clear) {
    clear.addEventListener('click', function () {
      active = [];
      pills.forEach(function (p) { p.setAttribute('aria-pressed', 'false'); });
      apply();
    });
  }
})();
</script>"""


def index_page():
    listed = [t for t in TECHNIQUES if not t.get('placeholder')]
    index_schema = [{
        "@type": "CollectionPage",
        "@id": f"{SITE_URL}/#library",
        "name": "Breath technique library",
        "url": SITE_URL,
        "isPartOf": {"@id": f"{SITE_URL}/#site"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(listed),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": re.sub('<[^>]+>', '', t['name']),
                 "url": canonical(f"{t['pillar']}/{t['slug']}.html")}
                for i, t in enumerate(listed)
            ],
        },
    }]
    return f"""{head('Breath techniques for anxiety, sleep and focus - Clay & Air',
       '19 breathing techniques you can run on your own tonight. Pick how you '
       'feel and get the technique for it, with the pattern and a video.',
       0, 'index.html', index_schema)}
{header(0, 'states')}

<main>
  <section class="section--tight section--pad">
    <div class="wrap">
      <p class="label">Breath library</p>
      <h1 class="lede">The one system you can reach directly.</h1>
      <p class="lede-sub">Your breathing runs itself all day and drags your
      nervous system along with it. Take it over for three minutes and the whole
      thing changes gear. {sum(1 for t in TECHNIQUES if not t.get("placeholder"))}
      ways to do that, sorted by what is actually wrong.</p>
      <p class="label label--gap">Pick what is true right now</p>
{pill_row()}
      <div class="library">
{library_cards()}
      </div>
      <p class="library-empty small muted" hidden>Nothing here yet. Pick another pillar.</p>
    </div>
  </section>

  <hr class="rule">

  <section class="section">
    <div class="wrap">
      <p class="label">The library</p>
      <h2>What these are</h2>
      <div class="copy">
      <p class="lead">Breathing patterns you can
      run with nothing you do not already have. You have probably tried one of them
      badly under pressure and found it did nothing. Most of them take three
      minutes when you run them properly.</p>
      <p class="muted">Every technique here is written so you can follow it alone,
      at the point you need it, without reading an essay first. Read one all the
      way through once while you are calm. Then it is there at 3am.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <p class="label">Where these come from</p>
      <h2>Ben Holt</h2>
      <div class="copy">
      <p class="lead">Every technique on this
      site is one of his, learned through Awakened Breath and the 21 Day
      Breathwork Academy. The three pillars are his framework. The counts, the
      mechanics and the order they are taught in are his. Two of them are his own
      designs: Dynamic breathwork, built on the Wim Hof method, and Sonic
      Neural.</p>
      <p class="muted">What is ours is the wording and the way it is arranged
      here, so you can find the right one quickly and follow it on your own. If
      you want the source, go to him:
      <a href="https://www.awakenedbreath.org/" rel="noopener">awakenedbreath.org</a>.</p>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="wrap">
      <p class="label">Three pillars</p>
      <div class="cards cards--spaced">
        <a class="card" href="relaxing/index.html">
          <p class="label">Pillar one</p>
          <h3>Relaxing</h3>
          <p>Bring the nervous system down. {sum(1 for t in TECHNIQUES if t["pillar"] == "relaxing" and not t.get("placeholder"))} techniques,
          all safe to run on your own.</p>
        </a>
        <a class="card" href="activating/index.html">
          <p class="label">Pillar two</p>
          <h3>Activating</h3>
          <p>Energy, focus and performance. A deliberate stress response, for
          mornings and before effort.</p>
        </a>
        <a class="card" href="freedom/index.html">
          <p class="label">Pillar three</p>
          <h3>Freedom</h3>
          <p>One technique. A facilitated ceremony, about two and a half
          hours, with time either side to arrive and to come back.</p>
        </a>
      </div>
    </div>
  </section>
</main>
{FILTER_JS}
{footer(0)}"""


# The commercial pages. Structure follows ui_kits/website/Intake.jsx: facts on
# the left, the form in a paper card on the right. The form posts to Netlify
# Forms, which needs no backend on a static host: the hidden form-name field
# and data-netlify are what Netlify's build-time HTML parse looks for.
#
# ---------------------------------------------------------------------------
# PLACEHOLDERS. These are structure and voice, not approved business facts.
# Fill in SESSION_FACTS and SESSION_OPTIONS with the real ones before launch.
# ---------------------------------------------------------------------------

# Don's own words, his final wording.
SESSION_WHY = """I know what it is to watch the life I spent decades building
          become unrecognizable. Over a short stretch, I buried people I
          loved, lost my marriage, my financial foundation, nearly every
          relationship I had, and the day-to-day life I knew with my kids. I
          found myself in a spare bedroom, starting again from scratch, while
          the responsibility to work, provide, and keep going remained.</p>

          <p class="why">I found breathwork through plant medicine. Plant
          medicine saved me. Breathwork empowered me by showing me I could
          bring my body into a deep meditative state with nothing but my own
          breath. It became a practice I could return to anywhere, even at
          three in the morning when there was no one to call. When almost
          everything else was gone, my breath was still mine. That is why I
          teach it."""

SESSION_FACTS = [
    ("Workshop", "about an hour", [
        "The workshop is a place to begin. We move, use Dynamic Breathwork, "
        "and finish with a guided meditation so you can experience what your "
        "breath is capable of in your own body.",
        "You do not need to know how to meditate or be good at slowing down. "
        "Bring a mat, wear something you can move in, and come as you are.",
    ]),
    ("Retreat", "coming soon", [
        "Some things need more than an hour.",
        "Sonic Neural is an immersive retreat for men who need enough time "
        "and distance from ordinary life to stop managing everything and "
        "listen to what is underneath it. Breath, sound, movement, nature, "
        "rest, and honest conversation create the conditions. Nothing is "
        "forced, and there is room for whatever surfaces to settle.",
        "This is the deeper work I am building toward now. It will be held "
        "in small groups, in a setting that gives us the space to do it "
        "properly.",
    ]),
]

SESSION_OPTIONS = [
    ("workshop", "Attend a workshop"),
    ("retreat", "Hear about the Sonic Neural retreat"),
    ("group", "Bring a workshop to my group"),
    ("unsure", "I am not sure yet"),
]


def sessions_page():
    facts = "\n".join(
        f"""        <div>
          <p class="label">{when}</p>
          <h2>{k}</h2>
          {"".join(f"<p>{x}</p>" for x in paras)}
        </div>"""
        for k, when, paras in SESSION_FACTS
    )
    options = "\n".join(
        f'            <option value="{v}">{lab}</option>'
        for v, lab in SESSION_OPTIONS
    )
    sessions_schema = [{
        "@type": "Service",
        "@id": f"{SITE_URL}/sessions#service",
        "name": "Breathwork workshops and retreats",
        "serviceType": "Breathwork facilitation",
        "provider": {"@id": f"{SITE_URL}/#org"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "Audience", "audienceType": "Men"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Sessions",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": k,
                 "description": paras[0]}}
                for k, when, paras in SESSION_FACTS
            ],
        },
    }, crumbs([("Breath library", "index.html"), ("Sessions", "sessions.html")])]
    return f"""{head('Breathwork workshops and retreats for men - Clay & Air',
                     'Breathwork you do with someone in the room. Workshops '
                     'about an hour, and an immersive Sonic Neural retreat.',
                     0, 'sessions.html', sessions_schema)}
{header(0, 'sessions')}

<main>
  <section class="technique">
    <div class="wrap">
      <div class="intake-open">
          <p class="label">Sessions</p>
          <h1>This is the part I do in person.</h1>
          <p class="purpose">The library gives you practices you can use on
          your own. In person, I can see when you are forcing, holding back,
          or ready to go further. I guide the pace, help you stay with what
          comes up, and leave enough time for you to land before you walk back
          into your life. That is what a screen cannot do.</p>
          <p class="label label--gap">Why I teach this</p>
          <p class="why">{SESSION_WHY}</p>
      </div>

      <div class="intake">
        <div class="intake-facts">
{facts}
        </div>

        <div class="form-card">
          <form class="intake-form" name="sessions" method="POST"
            action="/thanks.html" data-netlify="true"
            netlify-honeypot="bot-field">
            <input type="hidden" name="form-name" value="sessions">
            <p class="pot">
              <label>Leave this empty <input name="bot-field"></label>
            </p>

            <p class="label">Start here</p>
            <p class="small muted">Tell me what you are
              looking for and what has been going on. Plain words are enough.
              I read every message myself.</p>

            <div class="field">
              <label for="f-name">Name</label>
              <input id="f-name" name="name" type="text" required>
            </div>

            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email"
                placeholder="you@work.com" required>
            </div>

            <div class="field">
              <label for="f-about">What you are after</label>
              <select id="f-about" name="about">
{options}
              </select>
            </div>

            <div class="field">
              <label for="f-notes">Tell me what has been going on</label>
              <textarea id="f-notes" name="notes"></textarea>
            </div>

            <label class="check">
              <input type="checkbox" name="list" value="yes" checked>
              <span class="check-body">Send me the occasional note
                <span class="hint">A few times a month. One practice, and why
                it works. Unsubscribe from any of them.</span>
              </span>
            </label>

            <button type="submit" class="btn btn--primary btn--full">Start the conversation</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</main>
<script>
(function () {{
  // arriving from the Sonic Neural page preselects the ceremony
  var want = new URLSearchParams(location.search).get('about');
  var sel = document.getElementById('f-about');
  if (want && sel) {{
    var ok = Array.prototype.some.call(sel.options, function (o) {{
      return o.value === want;
    }});
    if (ok) {{ sel.value = want; }}
  }}

}})();
</script>
{footer(0)}"""


def thanks_page():
    return f"""{head('Received - Clay & Air',
                     'Your message reached Clay & Air.', 0,
                     'thanks.html').replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="robots" content="noindex, follow">')}
{header(0)}

<main>
  <section class="technique">
    <div class="wrap">
      <p class="label">Received</p>
      <h1>It arrived.</h1>
      <p class="purpose">You will hear back within a few days. If you do not,
      send it again and it will be found.</p>
      <p class="label--gap">
        <a class="btn btn--secondary" href="index.html">Back to the library</a>
      </p>
    </div>
  </section>
</main>
{footer(0)}"""


def pillar_page(pillar):
    label, _ = PILLARS[pillar]
    items = [t for t in TECHNIQUES if t["pillar"] == pillar]
    pend = [p for p in PENDING if p["pillar"] == pillar]

    rows = "\n".join(
        f"""        <li><a href="{t['slug']}.html">
          <span class="dur">{t['meta'][0]}</span>
          <span class="body">
            <span class="name">{t['name']}</span>
            <span class="use">{t['short_use']}</span>
          </span>
          <span class="aside"><span class="state-meta">{t['meta'][1]}</span></span>
        </a></li>"""
        for t in items
    )
    rows += "\n" + "\n".join(
        f"""        <li><div class="pending">
          <span class="dur">{p['meta']}</span>
          <span class="body">
            <span class="name">{p['name']}</span>
          </span>
          <span class="aside"><span class="state-meta">Not written</span></span>
        </div></li>"""
        for p in pend
    )

    if pillar == "freedom":
        intro = ("<h1>Freedom</h1>\n      <p class=\"purpose\">One technique, "
                 "and it works differently to everything else here. Sonic "
                 "Neural is a ceremony rather than something you fit into a "
                 "lunch break: fifty-five minutes of connected breathing to "
                 "music, with someone holding the room, and time either side "
                 "to arrive and to come back.</p>")
    elif pillar == "relaxing":
        intro = ("<h1>Relaxing</h1>\n      <p class=\"purpose\">Bring the nervous "
                 "system down and keep it there. This is the pillar you use most. "
                 "On an ordinary day it should be the only breathing you "
                 "are doing on purpose. Everything here is safe to run on your "
                 "own, as often as you want.</p>")
    else:
        intro = ("<h1>Activating</h1>\n      <p class=\"purpose\">These do the "
                 "opposite. They start a stress response on purpose, the same way "
                 "cold water and hard training do, and you come back sharper for "
                 "it. Mornings and before effort, never before bed, and always "
                 "finished with something from the relaxing pillar. Buteyko is the "
                 "exception: it is a breath hold rather than hard breathing, and "
                 "it settles you as much as it wakes you.</p>")

    pname = label.split(chr(183))[1].strip()
    pillar_schema = [{
        "@type": "CollectionPage",
        "@id": canonical(f"{pillar}/index.html") + "#page",
        "name": f"{pname} breathing techniques",
        "url": canonical(f"{pillar}/index.html"),
        "isPartOf": {"@id": f"{SITE_URL}/#site"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": re.sub('<[^>]+>', '', t['name']),
                 "url": canonical(f"{t['pillar']}/{t['slug']}.html")}
                for i, t in enumerate(items)
            ],
        },
    }, crumbs([("Breath library", "index.html"), (pname, f"{pillar}/index.html")])]
    return f"""{head(f'{pname} breathing techniques - Clay & Air',
       PILLAR_DESC[pillar],
       1, f'{pillar}/index.html', pillar_schema)}
{header(1, pillar)}

<main>
  <section class="technique technique--index">
    <div class="wrap">
      <p class="label">{label}</p>
      {intro}
      <ul class="tech-list tech-list--spaced">
{rows}
      </ul>
    </div>
  </section>
</main>
{footer(1)}"""


def not_found_page():
    """Netlify serves 404.html for any unmatched route automatically."""
    return f"""{head('Not found - Clay & Air',
                     'That page does not exist.', 0, '404.html').replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="robots" content="noindex, follow">')}
{header(0)}

<main>
  <section class="technique">
    <div class="wrap">
      <p class="label">404</p>
      <h1>That page is not here.</h1>
      <p class="purpose">It may have moved, or the link may be wrong. The
      library is the best place to start again.</p>
      <p class="label--gap">
        <a class="btn btn--secondary" href="index.html">Breath library</a>
      </p>
    </div>
  </section>
</main>
{footer(0)}"""


def redirects_txt():
    """Netlify uploads everything in the publish directory, so these rules do
    not stop _dev/ being deployed, they stop it being served. The trailing !
    is required: without it Netlify serves an existing file and never reaches
    the rule. The only way to keep a file off the CDN entirely is to keep it
    out of the publish directory."""
    hidden = ["/_dev/*", "/README.md"]
    lines = ["# Source is in git, not on the web. The ! forces the rule to win",
             "# over the real file that is sitting there.", ""]
    lines += [f"{p}  /404.html  404!" for p in hidden]
    lines.append("")
    return "\n".join(lines)


def robots_txt():
    """Search crawlers and answer engines both welcome. The assistant crawlers
    are named explicitly because some of them read a bare Allow as ambiguous,
    and because being quoted by an assistant is a distribution channel this
    site actually wants."""
    agents = ["Googlebot", "Bingbot", "DuckDuckBot", "Applebot",
              "GPTBot", "OAI-SearchBot", "ChatGPT-User",
              "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai",
              "PerplexityBot", "Perplexity-User",
              "Google-Extended", "Applebot-Extended", "meta-externalagent",
              "Amazonbot", "Bytespider", "CCBot", "cohere-ai", "Diffbot",
              "YouBot", "Timpibot"]
    lines = ["# Everything here is meant to be found and quoted.", ""]
    for a in agents:
        lines += [f"User-agent: {a}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "Disallow: /thanks", "",
              f"Sitemap: {SITE_URL}/sitemap.xml", ""]
    return "\n".join(lines)


def sitemap_xml(paths):
    today = time.strftime("%Y-%m-%d")
    rows = []
    for p in paths:
        if p == "thanks.html":
            continue                      # a form receipt is not a landing page
        pri = "1.0" if p == "index.html" else (
            "0.9" if p in ("sessions.html",) or p.endswith("/index.html") else "0.8")
        rows.append(f"  <url>\n    <loc>{canonical(p)}</loc>\n"
                    f"    <lastmod>{today}</lastmod>\n"
                    f"    <priority>{pri}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def llms_txt():
    """The llms.txt convention: a plain text map of the site for language
    models, so an assistant asked "what should I do for 3am panic" can find
    the right page instead of guessing from rendered HTML."""
    out = [f"# {SITE_NAME}", "",
           f"> {SITE_TAGLINE} A library of {len([t for t in TECHNIQUES if not t.get('placeholder')])} "
           "breathing techniques you can run on your own, organised by how you "
           "feel, plus workshops and retreats run in person.", "",
           "Every technique is taught by Ben Holt, learned through Awakened "
           "Breath and the 21 Day Breathwork Academy. Dynamic Breathwork and "
           "Sonic Neural Breathwork are his own designs. Clay & Air is Don "
           "Page's practice; the wording and the arrangement here are his.", "",
           "## How to pick one", "",
           "Techniques are tagged by state. The tags in use are: "
           + ", ".join(FEELINGS) + ".", ""]
    for pil, (label, _) in PILLARS.items():
        name = label.split(chr(183))[1].strip()
        out += [f"## {name}", "", PILLAR_DESC[pil], ""]
        for t in TECHNIQUES:
            if t["pillar"] != pil or t.get("placeholder"):
                continue
            plain = html.unescape(re.sub("<[^>]+>", "", t["name"]))
            use = html.unescape(re.sub("<[^>]+>", "", t["short_use"]))
            tags = ", ".join(TAGS.get(t["slug"], [])) or "not state tagged"
            url = canonical(f"{pil}/{t['slug']}.html")
            out.append(f"- [{plain}]({url}): {use} {t['meta'][0]}, "
                       f"{t['meta'][1].lower()}. For: {tags}.")
        out.append("")
    if SOCIALS:
        out += ["## Elsewhere", ""]
        out += [f"- {n}: {u}" for n, u in SOCIALS]
        out.append("")
    out += ["## Working with Clay & Air", "",
            f"- [Sessions]({canonical('sessions.html')}): workshops of about an "
            "hour, and an immersive Sonic Neural retreat for men, in small "
            "groups. Contact form on the page.", "",
            "## Safety", "",
            "Breath holds and forceful breathing are not for everyone. Anyone "
            "with a heart or lung condition, high or low blood pressure, "
            "epilepsy, or who is pregnant should talk to a doctor before "
            "holding their breath. Never practise these in or near water, or "
            "while driving.", ""]
    return "\n".join(out)


def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


if __name__ == "__main__":
    paths = ["index.html", "sessions.html", "thanks.html"]
    write("index.html", index_page())
    write("sessions.html", sessions_page())
    write("thanks.html", thanks_page())
    for pillar in PILLARS:
        write(f"{pillar}/index.html", pillar_page(pillar))
        paths.append(f"{pillar}/index.html")
    for t in TECHNIQUES:
        write(f"{t['pillar']}/{t['slug']}.html", technique_page(t))
        paths.append(f"{t['pillar']}/{t['slug']}.html")

    write("robots.txt", robots_txt())
    write("sitemap.xml", sitemap_xml(paths))
    write("llms.txt", llms_txt())
    write("404.html", not_found_page())
    write("_redirects", redirects_txt())
