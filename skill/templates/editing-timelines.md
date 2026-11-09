# Editing Timeline Templates (Frame-Level)

> CapCut Pro / Premiere Pro / DaVinci Resolve — teeno mein same structure. Tracks:
> **V1** main footage | **V2** overlays/text | **V3** graphics/stat cards | **A1** VO | **A2** music | **A3** SFX | **A4** ambience

---

## 1. SHORTS TIMELINE — ~2-3 Minute Master Template

> ⚠️ Confirmed (frame-level docs): shorts ~2-3 min ke hain (300-400 word Hindi scripts), 60s ke nahi. Neeche 90s ka core skeleton hai — same rhythm extend hota hai 2-3 min tak (escalation zone mein 2-3 aur fact-blocks add karo). **Har block mein 2-second rule** (kuch na kuch motion).

> **Face-Cam Blocks (Engine B):** 0:00-0:08 split-screen (upar visual, neeche face-cam) → 0:09 se full-bleed → twist par 2s face-cam reset. **Stamps (Engine A/C):** strong words par THUD. **Counters:** numbers par running meters.

```
TIME     VISUAL (V1)                 TEXT (V2/V3)           AUDIO (A1-A4)
─────────────────────────────────────────────────────────────────────────
0:00.0   [STRONGEST SHOT — motion]   HOOK WORD (pop-in)     VO: "Would you believe..."
         punch-in 1.10→1.00                                   A3: sub-boom (0:00.2)
         (Engine B: split-screen      (contrast pair ka       A2: dark pulse starts
          face-cam bottom 0-8s)        dusra hissa)
0:02.5   shot 2 (2.5s)               keyword highlight       VO continues
0:05.0   shot 3 (2.5s) + zoom        —                        A3: whoosh on cut
0:08.0   SLOW PUSH-IN (3s)           STINGER text strip       VO: "A truth of science..."
         (face-cam out, full-bleed)                            A2: music swell ↑
0:11.0   shot 5 (2s)                 —                        VO: setup line 1
0:13.0   shot 6 (2s)                 —                        A3: soft whoosh
0:15.0   CONTRAST GRAPHIC (3s)       X vs Y split text        VO: "For humans..."
0:18.0   shot 8 (2.5s)               —                        VO
0:20.5   COUNTER/METER (2s)          NUMBER runs 0→X          A3: cash-register tick
0:22.5   shot 10 (2.5s)              —                        VO: fact 1
0:25.0   STAMP DROP (1.5s)           "BANNED"/strong word     A3: heavy stamp THUD
0:27.5   AI still + Ken Burns (3s)   —                        VO: fact 2 escalate
0:30.5   STAT CARD #2 (2s)           BIGGER NUMBER            A3: riser → hit
0:32.5   shot 14 (2s)                —                        VO
0:34.5   map/diagram (3s)            location labels          VO: fact 3
         (travelling line + dots)                              A3: digital tick
0:37.5   shot 16 (2.5s)              —                        A3: whoosh
0:40.0   ARCHIVAL LOOK (3s)          date text (1955 etc.)    VO: fact 4 (biggest)
0:43.0   STAT CARD #3 (2s)           BIGGEST NUMBER           A3: riser → BOOM
0:45.0   shot 19 (2s)                —                        VO: micro-cliffhanger
0:47.0   shot 20 (2s)                —                        A2: music build phase
0:49.0   DIALOGUE MOMENT (3.5s)      quote text on screen     VO: reenacted dialogue
0:52.5   shot 22 (2s)                —                        VO
0:54.5   shot 23 (2.5s)              —                        A3: whoosh
0:57.0   DIAGRAM/EXPLAINER (4s)      HUD labels (⦿---)        VO: mechanism
1:01.0   shot 25 (2s)                —                        VO
1:03.0   ── TWIST ZONE ──
         DARK SHOT (2.5s)            —                        ⚠ SILENCE 0.2s (1:03.0-3.2)
         (Engine B: 2s FACE-CAM                                A3: IMPACT BOOM @1:03.2
          reset right here)                                     VO: "But the real truth..."
1:05.5   reveal shot (3s)            KEYWORD RED              A2: beat drop
1:08.5   shot 28 (2.5s)              —                        VO: twist detail
1:11.0   ── EMOTIONAL ZONE ──
         SLOW CINEMATIC (4s)         —                        A2: piano swell enters
                                                               VO softens: emotional turn
1:15.0   close-up (3.5s)             —                        VO
1:18.5   slow motion (3s)            —                        A2: strings ↑
1:21.5   ── CLOSE ──
         FINAL SHOT (3.5s)           QUOTE TEXT (full line)   VO: poetic close
                                                               A2: resolve chord
1:25.0   FREEZE/BLUR (2s)            —                        A3: soft shimmer
1:27.0   LOOP ECHO (3s)              —                        (first shot ka visual
         [SHOT 1 ka mirrored frame]                            echo, music fade)
         (Engine B: fetus→womb morph jaisa loop)              ⚠ NO CTA — punchline par end
1:30.0   END (ya 2-3 min tak escalate zone repeat)
```

**Totals:** ~28-30 shots | avg 2.6s/shoot | 3 stat cards | 8 whooshes | 1 silence-drop | 1 dialogue | 1 diagram | 1 loop echo

### Shorts ke liye Hard Rules
1. Shot kabhi 3s+ nahi (emotional zone ko chhod ke) — **2-second rule**: har 2s kuch motion
2. Har number = counter/stat card (V3); har strong word = stamp drop
3. Twist mein mandatory: silence → impact (+ face-cam reset possible)
4. Hook shot hi sabse visually striking hona chahiye (thumbnail-level quality)
5. Bottom 25% + top 15% text-free (Shorts UI) — **UI overlay track** (progress bar, 🔴 dot + ribbon) top 8% mein
6. **Shorts mein CTA nahi** — end = punchline + visual loop
7. Ek video = ek visual engine (A/B/C mix nahi)

### UI Overlay Track (V4 — Engine C par, optional others)
```
P0:00-END  [TOP: orange progress bar 0→100%]  [🔴 REC DOT + slanted ribbon + ruler ticks |  |  |  |]
```
Yeh track poore video mein fix rehti hai — completion bias + "classified dossier" look.

---

## 2. LONG-FORM TIMELINE — 8 Minute Master Template

```
CHAPTER 1 — COLD OPEN (0:00-0:50)
  V1: 8-10 cinematic shots (3-5s each), slow push-ins
  V2: no text (imagination zone) — ya ek word: "IMAGINE..."
  A2: mysterious drone + soft pulse
  A1: VO scene-painting pace (slightly slow, 0.95x)
  ★ 0:45-0:50: IDENTITY REVEAL — hard cut to best shot + title text slam + BOOM

CHAPTER 2 — ORIGIN (0:50-3:30)
  V1: archival look footage + date lower-thirds ("AUGUST 1990")
  V3: map animations (country pins, routes), 2-3 stat cards
  A2: tension bed (ostinato strings)
  A3: page-turn/film texture on era transitions, whoosh on map moves
  ★ 3:20: crisis peak — dark grade + slow zoom + music drop

CHAPTER 3 — PROBLEM (3:30-4:40)
  V1: failure scenarios (missile, rust, fireball visuals via AI)
  V2: question text on screen ("WHERE TO STORE IT?")
  A2: darker, heavier

CHAPTER 4 — SOLUTION + SCIENCE (4:40-6:20)
  V1: engineering visuals + AI cavern interiors
  V3: SPEC CARDS (capacity numbers), animated diagram (hydrostatic trap:
      water arrows pressing inward, oil floating — 6-8s animated explainer)
  A2: wonder shift (lighter synths)
  A3: dig/drill ambience texture
  ★ "Now, understand this carefully" — visual zoom into diagram + VO slow

CHAPTER 5 — TWIST (6:20-7:10)
  ★ 6:20: "But the story doesn't end here" — music cut 0.3s → new upbeat bed
  V1: 2020 lockdown visuals, tanker ships, deal handshake
  V3: savings stat card ("₹ THOUSANDS CRORES")

CHAPTER 6 — SCALE + FUTURE (7:10-7:45)
  V3: BIG comparison graphic ("9-10 DAYS" vs "74 DAYS"), future map
  A2: build to triumph

CHAPTER 7 — CALLBACK + CTA (7:45-8:01)
  V1: mirror cold-open shot (same composition, transformed subject)
  V2: closing quote text + subscribe animation (2s)
  A2: resolve orchestral chord + fade
  ★ Last frame = cold open ka echo (thumbnail consistency)
```

**Long-form pacing rules:**
- Chapter change = 0.5s black + whoosh + music shift
- Retention checkpoint har 60s: koi na koi "pattern interrupt" (graphic, zoom, text, silence)
- B-roll variety: stock 50% / AI 30% / graphics 15% / text cards 5%
- End screens (20s): next video card + subscribe circle

---

## 3. Reusable Project Presets

### Colour Grade (teal-orange documentary)
```
Contrast +12 | Highlights -20 | Shadows +8 | Whites +5 | Blacks -10
Temp +4 (warm) | Tint -2 (teal shadows) | Saturation -5
Vignette 15% | Grain 2-3% | Sharpen 10
```

### Text Presets
```
HOOK:     Anton 96pt, white, stroke 4px black, shadow, pop-in (scale 1.15→1.0, 0.25s)
KEYWORD:  Montserrat ExtraBold 72pt, #FFD700, inline
STAT:     Bebas 140pt number + Montserrat 48pt unit, dark card 70% opacity
QUOTE:    Montserrat SemiBold 64pt italic, center, fade-up 0.4s
LOWER3:   Montserrat Bold 44pt, left, slide-in 0.3s
```

### Audio Chain (VO)
```
De-esser → EQ (HPF 80Hz, +2dB @3kHz, +1.5dB @10kHz) → Compressor (3:1, fast) → Limiter (-1dB)
Reverb send: 6% wet (small room)
```

### Music Ducking
```
Sidechain from VO: threshold -24dB, ratio 3:1, release 200ms (natural)
Manual swells at: stinger line, twist, emotional turn, close
```

### Export
```
Shorts:  1080x1920, H.264, 12-16 Mbps, AAC 320k, -14 LUFS
Long:    1920x1080, H.264, 16-20 Mbps, AAC 320k, -14 LUFS
```

---

## 4. Shot List Spreadsheet Columns (production ke liye)

| # | Script line | Visual type | AI prompt / stock keyword | Duration | Text overlay | SFX | Music state |
|---|---|---|---|---|---|---|---|
| 1 | "Would you believe..." | AI clip | dramatic shark underwater... | 2.5s | "WOULD YOU BELIEVE" | sub-boom | dark pulse |
| ... | ... | ... | ... | ... | ... | ... | ... |
