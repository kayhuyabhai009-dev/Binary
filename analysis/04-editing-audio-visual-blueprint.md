# 04 — Editing, Visuals & Sound Design Blueprint (A-Z)

> **Evidence base:** 7 full transcripts ke pacing/beat structure, auto-captions ke `[संगीत]` (music) markers, thumbnail frames, YouTube ka "Made with AI" disclosure, aur is genre (AI facts-documentary) ke standard production stack. Video files sandbox mein download nahi ho paye (network restriction) — isliye kuchh specifics *inferred* hain, aur `skill/SKILL.md` mein yt-dlp commands diye hain jisse tum frame-level khud verify kar sakte ho.

---

## 1. Overall Editing Philosophy

**"Documentary trailer in 60 seconds."** Har second mein visual change, har 5-7 second mein emotional beat change, aur sound hi batata hai kab "wow" karna hai.

3 pillars:
1. **Pacing:** VO ke saath har clause par visual match (text-to-visual literalism)
2. **Audio-first design:** music swells + SFX hi retention kheenchte hain (captions ke `[संगीत]` markers yahi prove karte hain)
3. **Cinematic polish:** colour grade + vignette + slow zoom = "premium documentary" feel over slideshow

## 2. Visual Layer Kit (Kya Screen Par Hota Hai)

| Layer | Use | Source (AI pipeline) |
|---|---|---|
| 🎬 **Cinematic stock footage** | B-roll: nature, cities, industry, crowds | Pexels/Pixabay free stock |
| 🖼️ **AI-generated stills** | Jo stock mein nahi milta (1990 Kuwait war, underground cavern interiors, historical scenes) | Midjourney / Leonardo / DALL·E |
| 🎥 **AI video clips** | Slow motion, atmosphere, "camera moves" | Runway / Kling / Pika / Hailuo |
| 🗺️ **Maps & data graphics** | Locations (Vizag/Mangaluru/Padur), numbers, capacity bars | After Effects templates / Canva / AI-gen + motion |
| 📰 **Archival/photo-real** | History segments (Salk, Saddam, 1991) | Public domain + AI stylized re-creation |
| ✍️ **On-screen text** | Keywords, stats, names, shock numbers | CapCut/Premiere text presets |
| 🔲 **Diagram/explainer** | Hydrostatic trap, rumen process | AI image + animated arrows/layers |

**Visual rules (confirmed by genre + thumbnails):**
- Har 2-4 second mein cut ya camera move (zoom/pan) — static frame **kabhi nahi**
- Still images pe **Ken Burns** (slow push-in 3-5% per second) — "alive" feel
- Key words par **punch-in zoom** (1.0x → 1.08x, 0.3s ease)
- Shock facts par **full-screen stat card** (bada number + 2-3 words)
- Colour: **teal-orange cinematic grade**, high contrast, vignette, slight film grain
- Text: heavy sans-serif (Anton/Bebas/Montserrat ExtraBold), white + yellow/red keyword highlights
- Subject framing: center ya rule-of-thirds, negative space for text

## 3. Sound Design (Sabse Important Layer)

### 3.1 Music Bed
| Segment | Music type |
|---|---|
| Hook (0-8s) | Dark cinematic pulse / mysterious drone (tension) |
| Escalation | Driving rhythmic trailer bed (100-120 BPM, staccato strings/synth) |
| Science reveal | Wonder texture (light bells/synth pads) |
| Twist ("asli sach") | **Beat drop / impact hit** + sub-bass |
| Emotional turn | Piano/strings warm swell (sad-awe) |
| Poetic close | Resolve chord + fade, ya echo final word |
| Long-form chapters | Full arc: tension bed → build → triumph orchestral |

**Confirmed placement evidence:** Hindi auto-captions mein `[संगीत]` markers exactly in jagah aate hain:
- reveal se pehle ("घास पचा ही [संगीत] नहीं सकती" — pause before the twist)
- big number se pehle ("थन से [संगीत] 500 लीटर खून" — swell before the stat)
- punchline answer ("जवाब [संगीत] है बिल्कुल नहीं" — beat hit on "absolutely not")
- ending ("सफेद अमृत [संगीत]" — final swell + cut)

→ **Music rule:** VO ke dramatic pauses ko swell/impact se bharo. Vocal pauses = music ka spotlight.

### 3.2 SFX Library Map (kahan kaunsa effect)

| Trigger | SFX | Level (vs VO) |
|---|---|---|
| Scene/cut change (2-4s) | Whoosh / soft swish | -12 dB |
| Shock statement | Sub-bass impact / boom | -6 dB (feel it) |
| Number/stat reveal | Tick + riser → hit | -10 dB |
| "Twist" line | Reverse riser → silence 0.2s → impact | -8 dB |
| Historical flashback | Film projector crackle / vinyl dust (subtle) | -20 dB texture |
| Nature scenes | Ambient layer (birds, wind, water) | -22 dB texture |
| Map/zoom motion | Tech whoosh + digital tick | -14 dB |
| Emotional turn | Soft piano note / string swell | -12 dB |
| End card / CTA | Upbeat resolve chord | -10 dB |
| Horror-ish facts (polio, bacteria) | Low drone pulse, heartbeat | -18 dB bed |

### 3.3 Mix Rules
- VO: **-14 to -16 LUFS** (forward, compressed, presence boost 2-5 kHz), de-esser on
- Music bed: **-22 to -18 LUFS** under VO (sidechain ducking 3-4 dB)
- SFX transients can peak louder than music momentarily
- Loudness final: **-14 LUFS integrated** (YouTube standard)
- Voice EQ: high-pass 80 Hz, presence +2 dB @ 3 kHz, air +1.5 dB @ 10 kHz
- AI voice "cleanliness" ke liye: light room reverb (5-8% wet) taaki robotic na lage

## 4. Cut & Pacing Map (Shorts — 90 second example)

```
0:00-0:02  Visual hook (most striking image) + text-on-screen hook word
0:02-0:08  Hook VO — 2-3 cuts (2.5s each), punch-ins on key words
0:08-0:15  Stinger line — 1 slow push-in + music swell
0:15-0:30  Setup — 4-6 cuts (2-3s), contrast graphics (human vs shark side-by-side)
0:30-0:60  Escalation — cut EVERY 2-2.5s, stat cards at each number, whooshes
0:60-0:75  Twist — 0.2s silence → impact → dark visual shift
0:75-0:88  Emotional turn — slow shots (3-4s), piano, warm grade
0:88-0:95  Poetic close — freeze/blur + final text line
0:95-1:00  Loop point: last shot visually echoes first shot (re-watch bait)
```

**Cut rate:** avg 2.5-3s per shot (~25-30 shots per short) | **Long-form:** 3-5s per shot, chapter transitions = 1s black + whoosh.

## 5. Text & Typography System

| Element | Spec |
|---|---|
| Font primary | Anton / Bebas Neue (headlines), Montserrat (body) |
| **Dual-channel rule** | **On-screen text 100% English** (2-3 word punch labels) jab VO Hindi ho — Dual-Coding |
| HUD callouts (Engine B) | Target dot ⦿ + thin line + tiny clean label (noisy big captions nahi) |
| Comic headers (Engine A) | Bold comic-book caps (POISON ON PLATE) + pink/red stamps (BANNED, SMUGGLED) with THUD |
| Stamps/ribbons (Engine C) | Red/pink stamps (HEADACHE, OUCH) + slanted ribbon + ruler ticks |
| Hook text | 3-5 words, screen center, 1.2s pop-in with slight scale bounce |
| Keyword highlights | Yellow (#FFD700) ya red (#FF3B30) inline color |
| Stat cards | Dark translucent bg (70% black), huge number (Bebas), unit small — ya running counter |
| Names/locations | Lower-third strip, left aligned |
| Animation | Pop-in (scale 1.1→1.0), slide-up, never plain fade |
| Position | Lower 40% safe zone (Shorts UI ke liye top clear + bottom UI clear) |

## 6. Thumbnails (Long-form) & Shorts Covers

**Long-form thumbnail pattern (from visible frames):**
- Cinematic still (cavern/oil/mountain) + dark moody grade
- 3-5 word bold text, yellow/white, high contrast
- Face/emoji optional; curiosity object central (oil drop, mountain cutaway)
- Pattern: **image + "secret/unreal" text + number** ("₹5000 करोड़", "5.33 Million Tons")

**Shorts cover (sardefault frames se):** video ka strongest visual + title text overlay (YouTube auto-picks; custom frame choose karo = 1% improvement)

## 7. AI Production Stack (End-to-End)

| Step | Tool Options | Notes |
|---|---|---|
| 1. Research | ChatGPT/Perplexity + fact-check | sources rakho |
| 2. Script | Claude/GPT (prompts: `skill/prompts/`) | formula templates use karo |
| 3. VO | ElevenLabs (Multilingual v2/v3), Murf, PlayHT | Hindi+English voices, stable voice ID |
| 4. Visuals gen | Midjourney/Leonardo (stills), Runway/Kling/Pika (clips) | consistent style prompt |
| 5. Stock | Pexels/Pixabay/PixVerse | missing shots |
| 6. Edit | **CapCut Pro / Premiere Pro / DaVinci Resolve** | timeline templates: `skill/templates/` |
| 7. Music/SFX | Epidemic Sound / Artlist / Pixabay Music / Freesound | license track rakho |
| 8. Captions | CapCut auto-captions → styled keywords | Hindi Devanagari + EN |
| 9. Thumbnail | Midjourney + Photoshop/Canva | 3 variants, A/B |
| 10. Publish | YouTube Studio — "Made with AI" label ON, hashtags, chapters (long-form) | honest disclosure |

## 8. Frame-Level Verification Commands (Local Machine Par)

```bash
# Video download (analysis ke liye)
yt-dlp -f "bestvideo[height<=1080]+bestaudio" -o "%(title)s.%(ext)s" https://youtube.com/watch?v=DatHe3G0CNk

# Transcript + timestamps
yt-dlp --write-auto-subs --sub-lang en,hi --skip-download https://youtube.com/watch?v=5DQrYzv9FlQ

# Har 2 second ka frame nikalo → cut rate analyze karo
ffmpeg -i video.mp4 -vf fps=0.5 frames/frame_%03d.jpg

# Scene change detect (cut count per minute)
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo | wc -l

# Audio waveform → music swells/SFX peaks
ffmpeg -i video.mp4 -filter_complex showwavespic=s=1200x300 waveform.png

# LUFS loudness check
ffmpeg -i video.mp4 -af ebur128 -f null -
```

## 9. Quality Checklist (Har Video Ke Liye)

- [ ] Visual static 3s+ nahi kahin bhi
- [ ] Har number par on-screen text
- [ ] Music swells VO pauses par (captions mein [music] jaisa feel)
- [ ] Twist par silence→impact moment
- [ ] Ending line quotable hai
- [ ] Loop potential (last frame → first frame echo)
- [ ] Loudness -14 LUFS, VO clear on phone speaker
- [ ] Hindi/English choice topic ke hisaab se
- [ ] "Made with AI" label sahi
- [ ] Thumbnail/title curiosity gap complete karta hai (koi spoiler nahi)
