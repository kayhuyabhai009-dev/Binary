# Motion-Engine Playbook — "Fully Animated" Editing Ka Poora System

> **Origin:** 10 Nov 2026 ko v1/v2 videos reject hue — "kitna jyada animations hai uspe, tumhara 1% bhi nahi". Root cause: static-photo slideshow ≠ Gulshan's motion-graphics fingerprint. Yeh playbook woh complete system hai jo uske baad banaya (v3 engine) — frame-by-frame verified.
>
> Reference implementation: `video-project/build_video_v3.py` + QC tool `tools/frame_analyzer.py`

---

## 1. ⚖️ The Motion Standard (Quantified — opinion nahi, metrics)

| Gate | Target | Kyun |
|---|---|---|
| Avg motion energy (mean abs frame-diff @135x240 gray) | **> 5.0** (v3 = 8.85) | Gulshan-style = constant movement; <4 = slideshow |
| Static frames % (diff < 1.2) | **< 5%** | Scattered singles OK; runs not |
| Longest static run | **< 1.0s** | "2-Second Rule" ka hard version |
| Cut/transition spikes per 50s | **8-12** (whips + hits) | Har scene boundary = visible transition |
| SFX events | **≥ 1 per 1.5s** (54 @ 50s) | "Har chhoti animation ke neeche ek crisp SFX" |

**Tool:** `python3 tools/frame_analyzer.py VIDEO.mp4 --report out.md --sheet out.png`
Har deliverable ISI tool se gate karo. Report commit karo (qc/ folder, gitignored) — numbers client ko dikhao.

## 2. 🎞️ Animation Primitives (PIL frame-renderer se — ffmpeg drawtext se kaafi upar)

ffmpeg drawtext/zoompan = LIMITED (static labels, slow Ken Burns). Asli motion chahiye to **har frame PIL se render karo** (1080x1920 @30fps ≈ 1500 frames ≈ 6-7 min CPU) → rawvideo pipe → libx264.

### Camera (har frame — ZERO static frames ka asli raaz)
- **Push/pull** per scene (ease-in-out, alternate in/out direction)
- **Wobble**: `1.15*sin(1.9t) + 0.5*sin(3.3t)` degrees — organic drift
- **Breathing pulse**: `1 + 0.014*sin(2.6t)` scale — sub-pixel life
- **Film-weave jitter**: ±2.2px random dx/dy per frame (film-gate weave — invisible but kills frozen frames)
- **Hit shake**: stamp scenes par `sin(55t)` decay 0.4s
- **Punch-in cutaway**: scene ke 58-78% par 1.65x zoom crop (0.2s = "close-up shot" feel)

### Transitions
- **Whip-pan**: scene entry par dx = ±W*1.25 → 0 (ease-out-expo, 0.26s) — direction alternate
- **White flash** 0.13s decay at cuts
- **Glitch** (twist par): RGB channel roll ±9px + horizontal slice displacement 0.4s

### Kinetic Type (static text = SABSE BADA rejection reason)
- **Word-by-word pop**: har word scale 1.62→1.0 (ease-out-back overshoot) + drop-in, stagger 0.105s
- **Slam stamp**: y -640px → 0 ease-out-back 0.26s + rotate -2.4°→0 + jitter + box
- **Rolling counter (money-meter)**: value noisy intermediates se guzarta hai (v+35% random) phir snap — "127,450 → 1,041,427" rukta nahi
- **Stepped counter**: step windows par scale-punch 1.25→1
- **HUD callout**: dot box + growing line (`min((t-t0)*2600, ln)`) + label slide-26px fade
- Labels **hamesha fit-fraction** se auto-shrink: `min(base, W*0.9/(len*0.60))` — clipping = amateur

### FX Layers
- **Starbursts** (12-ray, rotate + alpha arc) stamp/label entries par
- **Speed lines** (manga radial, 16 lines, rotate) hits par
- **Particles**: 28 drifting dots, twinkling alpha, per-scene seed
- **Print-boil halftone**: dot pattern ka phase HAR frame crawl karta hai (risograph print-jitter — comic animation ka classic technique)
- **Vignette** + warm glow ending par

## 3. 🎙️ VO Rule — "Bich mein tutne mat dena" (CLIENT LAW)
- VO = **ek continuous take**. Chunk-mat-karo, gap-mat-daalo, reorder-mat-karo.
- Duration adjust = **continuous filters only**: `silenceremove` (gaps→0.18s) + `atempo` (1.2-1.35 max). Pitch preserved, flow intact.
- Verify: final audio pe `silencedetect=noise=-38dB:d=0.6` → **0 gaps** hona chahiye. Yeh QC step mandatory hai.
- Micro-acting (pitch/speed per phrase) tabhi karo jab ho sake continuous FIR filters se; warna chhodo. Continuity > acting.

## 4. 🔊 Audio Architecture (54 events / 50s)
- **Synth SFX set** (aevalsrc se — koi library nahi): whoosh (transition), slam (stamp), boom (twist), riser (pre-twist), tick (counter), pop (label), blip (HUD), zap, glitch, chord (ending)
- Schedule = scene table se derived: har cut par whoosh, har label par pop, har counter-step par tick
- **Music**: 102BPM gated bass+pump; **twist par 0.85s music hole** (0.10 volume) + boom — silence hi sabse tez effect hai
- loudnorm I=-14:TP=-1.2 (YouTube standard)

## 5. 🖼️ Visual Assets
- **Flat 2D comic/risograph** style (halftone dots, bold outlines, flat palettes) — photoreal AI images style tod dete hain
- Per-scene color mood (mustard/crimson/midnight/teal) — psychology table analysis/05 mein
- 10-12 images enough; **punch-in crops** hi "extra shots" hain (same art, alag framing)
- NO TEXT in generated images — sab text engine se aata hai (crisp + animatable)

## 6. 📐 Scene Table (source of truth — code mein dict)
Har scene: `{img, t0, t1, stamp/header, sub, hud, counter/roll, fx flags (shake/hit/glitch/soft/loop/crop_x)}`.
- Scene boundaries = **VO phrase gaps se auto-derived** (silencedetect → nearest-gap matching to semantic targets)
- Labels English 2-4 words; VO Hindi — dual-channel law
- Structure: hook 0-10% | body beats | twist ~45-55% | emotional punchline ~75-82% | **visual loop echo** last 10% | NO CTA

## 7. 🚫 Rejection Triggers (client-tested)
1. Static photo + caption text = "1% bhi nahi" — **turant reject**
2. Text jo clip ho ya ek baar aake baithe — reject
3. VO mein gaps/splices — reject
4. Scene cuts hard-cut bina transition — "editing nahi aata"
5. Counter jo seedha final value dikhaye — real editing mein numbers **bhaagte hain**
6. End pe CTA/like-mango — Gulshan law: punchline + loop

## 8. ✅ Delivery Checklist
- [ ] frame_analyzer: motion > 5.0, longest static < 1s, grade report saved
- [ ] VO continuity: 0 silence gaps ≥0.6s in final audio
- [ ] Text fit: koi label screen se clip nahi
- [ ] Loop ending: last scene hook-art pe wapas + final line persists
- [ ] Music twist-hole sync'd with VO twist phrase
- [ ] Output: 1080x1920, 30fps, crf 19-20, loudnorm -14, faststart
