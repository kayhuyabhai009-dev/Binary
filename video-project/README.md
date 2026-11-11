# video-project — "The Fruit That Hacked Your Brain 🌶️" (50s, Gulshan motion-graphics style)

## Files
| File | Kya hai |
|---|---|
| `build_video_v3.py` | ⭐ **Production engine** — frame-by-frame PIL motion-graphics renderer (whip transitions, kinetic type, rolling counters, slam stamps, glitch, print-boil, particles) + continuous-VO audio pipeline + 54-event synth SFX. `python3 build_video_v3.py` (re-render: `RERENDER=1`) |
| `build_video_v2.py` | v2 drawtext-engine (rejected — static feel). Reference only |
| `build_video.py` | v1 photo-slideshow (rejected). Reference only |
| `output/mirchi-gulshan-V3.mp4` | ⭐ FINAL — 50.3s, 1080x1920@30fps, motion energy 8.85, VO continuous, loudnorm -14 |
| `assets/c1-c11*.png` | Flat 2D comic/risograph scene art (text-free) |
| `audio/vo50.mp3` | Hindi VO raw take (voice-00). Engine isse silence-choke + atempo se continuous rakhta hai |
| `qc2/` | QC frames + `v3-motion-report.md` (frame_analyzer output) |

## Rebuild
```bash
pip install --break-system-packages numpy pillow imageio-ffmpeg
python3 build_video_v3.py                 # ~7 min render
python3 ../tools/frame_analyzer.py output/mirchi-gulshan-V3.mp4 --report qc2/motion.md
```

## Publish Package
- **Title:** "मिर्च खाने से जलन होती ही नहीं! 🌶️" / "The Fruit That Hacked Your Brain 🌶️ #facts"
- **Desc:** मिर्च में आग नहीं होती — ये सिर्फ़ एक धोखा है। जानिए कैप्साइसिन, TRPV1 और एक पौधे की सबसे पुरानी चाल के बारे में। 🌶️🧠 #mirchi #facts #science #hindi #shorts #didyouknow #capsaicin #bhutjolokia
- **Pinned comment:** "मिर्च खाने के बाद पानी पीते हो या दूध? 👇🔥"
- **Note:** "Made with AI" label ON rakho (channel policy + trust)

## Style Compliance (Gulshan 4 Laws)
✅ Contrast hook first 10s | ✅ Hindi VO + English labels | ✅ Zero static frames (frame_analyzer verified) | ✅ Twist + emotional punchline + visual loop, NO CTA
