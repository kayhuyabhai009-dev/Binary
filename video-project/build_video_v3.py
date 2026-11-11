#!/usr/bin/env python3
"""
build_video_v3.py — Gulshan-style MOTION GRAPHICS engine (frame-by-frame renderer).
Unlike v1/v2 (static image + drawtext), every frame is drawn in PIL with tweened
animation: whip transitions, word-by-word kinetic type, rolling counters, slam
stamps with overshoot, punch-in cutaways, particles, speed-line bursts, glitch
FX, flashes, persistent UI frame. Audio: continuous VO (no splices) + synth SFX
+ 102BPM gated music with twist hole.
"""
import os, sys, math, random, struct, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------- config ----------------
ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets")
TMP = os.path.join(ROOT, "tmp3"); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(ROOT, "output"); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"

def run(cmd, err_ok=False):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 and not err_ok:
        errs = [x for x in r.stderr.splitlines()
                if any(k in x for k in ("rror", "nvalid", "No such", "nknown", "Trailing"))]
        print("FAIL:", " ".join(map(str, cmd))[:200])
        for l in (errs[-8:] or r.stderr.splitlines()[-6:]): print("  >", l)
        raise SystemExit(1)
    return r

def probe_dur(p):
    r = run([FF, "-hide_banner", "-i", p], err_ok=True)
    for l in r.stderr.splitlines():
        if "Duration" in l:
            h, m, s = l.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h)*3600 + int(m)*60 + float(s)
    raise SystemExit("no duration " + p)

# ---------------- easing ----------------
def clamp01(x): return max(0.0, min(1.0, x))
def seg(t, t0, t1): return clamp01((t - t0) / max(t1 - t0, 1e-6))
def ease_out_back(u):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3*(u-1)**3 + c1*(u-1)**2
def ease_out_expo(u): return 1.0 if u >= 1 else 1 - 2**(-10*u)
def ease_in_out(u): return u*u*(3 - 2*u)

# ---------------- audio prep (continuous VO — no splices) ----------------
VO_SRC = os.path.join(ROOT, "audio", "vo50.mp3")
VO_A = f"{TMP}/vo_a.wav"
VO_P = f"{TMP}/vo_final.wav"
print("VO processing (continuous)...")
run([FF, "-y", "-i", VO_SRC, "-af",
     "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-33dB:"
     "stop_periods=-1:stop_silence=0.18:stop_threshold=-33dB,"
     "aresample=44100", VO_A])
dur_a = probe_dur(VO_A)
TARGET_VO = 49.0
atempo = max(1.0, min(1.55, dur_a / TARGET_VO))
run([FF, "-y", "-i", VO_A, "-af", f"atempo={atempo:.4f},aresample=44100", VO_P])
VDUR = probe_dur(VO_P)
TV = round(VDUR + 1.3, 2)
print(f"VO: raw->choked {dur_a:.2f}s -> atempo {atempo:.3f} -> {VDUR:.2f}s  | TV={TV}")

# phrase map on final VO (for scene cuts + word sync)
# NOTE: VO was silence-choked to 0.18s gaps, so detect short gaps
r = run([FF, "-y", "-i", VO_P, "-af", "silencedetect=noise=-33dB:d=0.09", "-f", "null", "-"], err_ok=True)
sil = []
for l in r.stderr.splitlines():
    if "silence_start" in l:
        s = float(l.split("silence_start:")[1].strip()); sil.append([s, None])
    if "silence_end" in l and sil and sil[-1][1] is None:
        sil[-1][1] = float(l.split("silence_end:")[1].split("|")[0].strip())
gaps = [(a, b) for a, b in sil if b is not None and b - a >= 0.08]
print(f"detected {len(gaps)} phrase gaps")

# ---------------- scene table ----------------
# semantic cut targets in final-time fractions -> pick nearest detected gaps
N_SCENES = 10
cut_fracs = [0.105, 0.195, 0.295, 0.375, 0.455, 0.545, 0.625, 0.72, 0.835]
cut_times = []
for f in cut_fracs:
    tgt = f * VDUR
    best = min(gaps, key=lambda g: abs(g[0] - tgt)) if gaps else None
    if best and all(abs(best[0] - c) > 0.4 for c in cut_times):
        cut_times.append(best[0])
cut_times = sorted(cut_times)
need = N_SCENES - 1
if len(cut_times) < need:                       # fallback: uniform fractions
    for f in cut_fracs:
        tt = f * VDUR
        if all(abs(tt - c) > 0.4 for c in cut_times):
            cut_times.append(tt)
        if len(cut_times) >= need: break
    cut_times = sorted(cut_times)
while len(cut_times) > need: cut_times.pop()
T = [0.0] + [round(c, 3) for c in cut_times] + [TV]
SC = []
IMG = {0: "c1-hook", 1: "c11-brain-button", 2: "c4-alarm", 3: "c9-water-milk",
       4: "c9-water-milk", 5: "c6-ghost", 6: "c7-bird", 7: "c10-birds-eat",
       8: "c8-tears", 9: "c1-hook"}
STYLE = {  # header/stamp/hud/counter + fx flags
    0: {"stamp": "NOT ACTUALLY HOT", "sub": "THE BURN IS A LIE", "shake": True, "hit": True},
    1: {"header": "YOUR BRAIN GETS TRICKED", "hud": "TRPV1: PAIN SIGNAL SENT"},
    2: {"stamp": "FAKE ALARM", "counter": ["12°", "6°", "2°", "0°"], "sub": "TEMP CHANGE — ZERO REAL HEAT", "shake": True, "hit": True},
    3: {"header": "WATER SPREADS THE BURN", "hud": "CAPSAICIN + WATER = NO MIX"},
    4: {"header": "MILK WASHES THE HEAT", "sub": "CASEIN DISSOLVES CAPSAICIN", "crop_x": 0.62},
    5: {"header": "SCOVILLE SCALE", "roll": ["127,450", "512,900", "884,200", "1,041,427"], "sub": "BHUT JOLOKIA • INDIA"},
    6: {"stamp": "THE PLANT'S TRICK", "hud": "BIRDS FEEL NOTHING", "shake": True, "hit": True, "glitch": True},
    7: {"header": "SEEDS SPREAD BY BIRDS", "sub": "THE BURN TARGETS YOU"},
    8: {"header": "A PLANT'S CLEVER TRICK", "sub": "IT WAS NEVER YOUR WEAKNESS", "soft": True},
    9: {"sub": "IT WAS NEVER YOUR WEAKNESS", "loop": True, "soft": True},
}
for i in range(N_SCENES):
    SC.append({"i": i, "t0": T[i], "t1": T[i+1] if i+1 < len(T) else TV, "img": IMG[i], **STYLE[i]})
print("scene cuts:", [s["t0"] for s in SC])

# ---------------- static assets ----------------
print("preparing art + overlays...")
IMGS = {}
for name in set(IMG.values()):
    IMGS[name] = Image.open(os.path.join(A, name + ".png")).convert("RGB")
IW, IH = 1560, 2773  # work canvas (1.44x) for camera freedom

def art_for(name, crop_focus=None):
    """pre-scale art to work canvas; crop_focus=x-fraction for split compositions"""
    im = IMGS[name]
    tw, th = IW, IH
    if crop_focus is not None:
        # crop a portrait region around x-fraction then fit
        w2 = int(im.width * 0.52)
        x0 = int(im.width * crop_focus) - w2 // 2
        x0 = max(0, min(im.width - w2, x0))
        im = im.crop((x0, 0, x0 + w2, im.height))
    return im.resize((tw, th), Image.LANCZOS)

ART = {}
for i, s in enumerate(SC):
    key = (s["img"], s.get("crop_x"))
    if key not in ART:
        ART[key] = art_for(s["img"], s.get("crop_x"))

# halftone tile
tile = np.zeros((8, 8), dtype=np.float32)
yy, xx = np.mgrid[0:8, 0:8]
tile = ((xx + yy) % 4 < 2).astype(np.float32)
HALF = np.tile(tile, (H // 8 + 1, W // 8 + 1))[:H, :W]
HALF_RGBA = np.zeros((H, W, 4), dtype=np.uint8)
HALF_RGBA[..., 3] = (HALF * 26).astype(np.uint8)

# vignette
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W/2)/(W/2))**2 + ((yy - H/2)/(H/2))**2)
VIG = np.zeros((H, W, 4), dtype=np.uint8)
VIG[..., 3] = (np.clip(r - 0.55, 0, 1) * 150).astype(np.uint8)

F = {}
for sz in (28, 32, 38, 44, 52, 58, 64, 72, 84, 96, 112, 132, 168):
    F[sz] = ImageFont.truetype(FONT, sz)

def font(sz):
    if sz not in F: F[sz] = ImageFont.truetype(FONT, sz)
    return F[sz]

# ---------------- drawing primitives ----------------
def fit_size(text, base, frac=0.90):
    L = max(len(w) for w in text.split(" "))
    chars = len(text)
    return max(22, min(base, int(W * frac / (max(chars, 1) * 0.60))))

def draw_word_line(d, words, t, t_start, y, base_size, fill, stroke=8,
                   stroke_fill="black", x_center=W/2, spacing=0.105, box=None, pop=0.22):
    """word-by-word pop-in. returns total width drawn."""
    sizes = [base_size] * len(words)
    fnt = font(base_size)
    widths = [d.textlength(w, font=fnt) for w in words]
    gap = base_size * 0.32
    total = sum(widths) + gap * (len(words) - 1)
    x = x_center - total / 2
    for k, w in enumerate(words):
        tw = t_start + k * spacing
        u = seg(t, tw, tw + pop)
        if u <= 0:
            x += widths[k] + gap
            continue
        s = 1.62 - 0.62 * ease_out_back(u)      # overshoot pop
        alpha_drop = (1 - u) * base_size * 0.9   # drop from above
        f2 = font(max(12, int(base_size * s)))
        ww = d.textlength(w, font=f2)
        wx = x + widths[k] / 2 - ww / 2
        wy = y - (f2.size - base_size) * 0.8 - alpha_drop
        if box:
            pad = 22
            d.rounded_rectangle([wx - pad, wy - 8, wx + ww + pad, wy + f2.size + 12],
                                radius=12, fill=box)
        d.text((wx, wy), w, font=f2, fill=fill,
               stroke_width=max(2, int(stroke * s / 1.2)), stroke_fill=stroke_fill)
        x += widths[k] + gap
    return total

def stamp_layer(t, t0, text, y, base_size, box_fill=(193, 18, 31, 235)):
    """slamming stamp: falls in with overshoot + jitter + dust ring"""
    u = seg(t, t0, t0 + 0.26)
    if u <= 0: return None
    size = fit_size(text, base_size, 0.82)
    lay = Image.new("RGBA", (W, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fnt = font(size)
    tw = d.textlength(text, font=fnt)
    pad = 30
    bx = (W - tw) / 2 - pad
    jx = 0
    if u < 1:
        jx = random.uniform(-1, 1) * (1 - u) * 9
    d.rounded_rectangle([bx + jx, 22, bx + tw + 2 * pad + jx, size + 62], radius=16, fill=box_fill)
    d.text(((W - tw) / 2 + jx, 34), text, font=fnt, fill="white",
           stroke_width=3, stroke_fill=(120, 8, 18))
    yoff = -(1 - ease_out_back(u)) * 640
    lay = lay.rotate(-(1 - u) * 2.4, expand=True, resample=Image.BICUBIC)
    return lay, int(y + yoff - 40)

def hud_anim(d, t, t0, label, y, x0=170, ln=700, label_color=(255, 215, 0)):
    u = seg(t, t0, t0 + 0.5)
    if u <= 0: return
    w = min(int((t - t0) * 2600), ln)
    d.rectangle([x0, y, x0 + w, y + 5], fill=(255, 255, 255, 230))
    d.rectangle([x0 - 10, y - 8, x0 + 10, y + 13], fill=(255, 255, 255, 245))
    u2 = seg(t, t0 + 0.22, t0 + 0.6)
    if u2 > 0:
        fs = fit_size(label, 42, 0.72)
        fnt = font(fs)
        alpha = int(255 * u2)
        d.text((x0 + (1 - ease_out_expo(u2)) * -26, y + 34), label, font=fnt,
               fill=(*label_color, alpha), stroke_width=3, stroke_fill=(0, 0, 0, alpha))

def rolling_number(d, t, t0, t_snap, final_txt, y, base=128):
    """money-meter style counter: noisy intermediates -> snap at t_snap"""
    if t < t0: return
    if t < t_snap:
        v = int(seg(t, t0, t_snap) * int(final_txt.replace(",", "").replace("°", "") or 0))
        noise = int(v * 0.35 * random.random())
        txt = f"{v + noise:,}"
        if final_txt.endswith("°"): txt += "°"
        size = base
    else:
        txt = final_txt
        size = base
    u = seg(t, t_snap, t_snap + 0.2)
    size = int(size * (1 + 0.18 * (1 - ease_out_back(u)) if u < 1 else 1))
    fnt = font(max(24, size))
    tw = d.textlength(txt, font=fnt)
    d.text(((W - tw) / 2, y), txt, font=fnt, fill=(255, 215, 0),
           stroke_width=7, stroke_fill="black")

def stepped_counter(d, t, steps, y, base=132):
    """steps = [(txt, t0, t1)]"""
    for txt, t0, t1 in steps:
        if t0 <= t < t1:
            u = seg(t, t0, t0 + 0.18)
            size = int(base * (1 + 0.25 * (1 - ease_out_back(u)) if u < 1 else 1))
            fnt = font(size)
            tw = d.textlength(txt, font=fnt)
            d.text(((W - tw) / 2, y), txt, font=fnt, fill=(255, 215, 0),
                   stroke_width=8, stroke_fill="black")

def particles(d, t, seed, n=28, color=(255, 210, 120)):
    rnd = random.Random(seed)
    for k in range(n):
        x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
        vx, vy = rnd.uniform(-22, 22), rnd.uniform(-46, -12)
        ph = rnd.uniform(0, 6.28)
        sz = rnd.uniform(2.5, 7)
        x = (x0 + vx * t) % W
        y = (y0 + vy * t) % H
        a = int(155 + 85 * math.sin(t * 2.1 + ph))
        d.ellipse([x - sz, y - sz, x + sz, y + sz], fill=(*color, max(0, a)))

def speed_lines(d, t, t0, cx=W/2, cy=H/2, n=16, spread=1.0):
    u = seg(t, t0, t0 + 0.55)
    if u <= 0: return
    alpha = int(210 * (1 - u))
    rnd = random.Random(int(t0 * 100))
    for k in range(n):
        ang = rnd.uniform(0, math.pi * 2) + t * 1.2
        r0 = 260 + 420 * u * spread
        r1 = r0 + 190 + 160 * (1 - u)
        x1, y1 = cx + math.cos(ang) * r0, cy + math.sin(ang) * r0
        x2, y2 = cx + math.cos(ang) * r1, cy + math.sin(ang) * r1
        d.line([x1, y1, x2, y2], fill=(255, 255, 255, alpha), width=5)

def starburst(d, x, y, r, u, color=(255, 220, 80)):
    if u <= 0: return
    a = int(230 * (1 - abs(u - 0.5) * 2))
    for k in range(12):
        ang = k * math.pi / 6 + u * 0.8
        d.line([x + math.cos(ang) * r * 0.35, y + math.sin(ang) * r * 0.35,
                x + math.cos(ang) * r * (0.6 + u), y + math.sin(ang) * r * (0.6 + u)],
               fill=(*color, max(0, a)), width=6)

# ---------------- camera ----------------
def draw_camera(base, s, deg, dx, dy):
    th = math.radians(deg)
    ct, st = math.cos(th), math.sin(th)
    a, b = ct / s, st / s
    c = IW / 2 - a * (W / 2 + dx) - b * (H / 2 + dy)
    d_, e = -st / s, ct / s
    f = IH / 2 - d_ * (W / 2 + dx) - e * (H / 2 + dy)
    return base.transform((W, H), Image.AFFINE, (a, b, c, d_, e, f), resample=Image.BICUBIC)

# ---------------- main render ----------------
NFR = int(TV * FPS)
raw = f"{TMP}/raw.h264"
if os.path.exists(raw) and not os.environ.get("RERENDER"):
    print(f"skip render (reuse {raw})")
else:
  proc = subprocess.Popen([FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                         "-pix_fmt", "yuv420p", raw], stdin=subprocess.PIPE)
  for fi in range(NFR):
    t = fi / FPS
    # scene lookup
    sc = SC[0]
    for s in SC:
        if s["t0"] <= t: sc = s
    lt = t - sc["t0"]
    dur = sc["t1"] - sc["t0"]
    base = ART[(sc["img"], sc.get("crop_x"))]

    # --- camera: push/pull + wobble + whip entry ---
    i = sc["i"]
    push = 1.34 - 0.16 * ease_in_out(seg(t, sc["t0"], sc["t1"])) if i % 2 == 0 else 1.18 + 0.16 * ease_in_out(seg(t, sc["t0"], sc["t1"]))
    push *= 1 + 0.014 * math.sin(t * 2.6 + i)          # constant breathing pulse
    wob = 1.15 * math.sin(t * 1.9 + i * 1.7) + 0.5 * math.sin(t * 3.3 + i)
    dx = 18 * math.sin(t * 0.7 + i) + 26 * math.sin(t * 2.2 + i * 3) + 6 * math.sin(t * 4.1 + i * 5)
    dy = 22 * math.cos(t * 0.55 + i * 2) + 6 * math.cos(t * 3.7 + i * 4)
    # whip entry slide
    whip = seg(t, sc["t0"], sc["t0"] + 0.26)
    if whip < 1 and not sc.get("loop") and i > 0:
        dirn = 1 if i % 2 == 0 else -1
        dx += dirn * W * 1.25 * (1 - ease_out_expo(whip))
    if sc.get("loop"):
        whip = seg(t, sc["t0"], sc["t0"] + 0.3)
        dx += W * 1.3 * (1 - ease_out_expo(whip))
    # hit pulses (stamp scenes): scale bounce
    if sc.get("hit"):
        pu = seg(t, sc["t0"], sc["t0"] + 0.34)
        push *= 1 + 0.05 * (1 - ease_out_back(pu)) if pu < 1 else 1
    # shake on stamp entry
    if sc.get("shake") and lt < 0.42:
        dx += math.sin(t * 55) * 15 * (1 - lt / 0.42)
        dy += math.cos(t * 49) * 12 * (1 - lt / 0.42)
    # soft ending slow-out
    if sc.get("soft"):
        push *= 1.03 - 0.03 * ease_in_out(seg(t, sc["t0"], sc["t1"]))

    frame = draw_camera(base, push, wob, dx + random.uniform(-2.2, 2.2),
                        dy + random.uniform(-2.2, 2.2))   # film-weave jitter

    # punch-in cutaway: second half of content scenes -> quick zoom frame
    if dur > 3.2 and not sc.get("soft") and not sc.get("loop"):
        pu2 = seg(t, sc["t0"] + dur * 0.58, sc["t0"] + dur * 0.78)
        if 0 < pu2 < 1:
            frame = draw_camera(base, push * 1.65, wob * 0.3, dx * 0.2, dy * 0.2 - 120)

    arr = np.array(frame)
    # glitch FX on twist
    if sc.get("glitch") and lt < 0.4:
        g = 1 - lt / 0.4
        arr[:, :, 0] = np.roll(arr[:, :, 0], int(9 * g), axis=1)
        arr[:, :, 2] = np.roll(arr[:, :, 2], int(-9 * g), axis=1)
        for k in range(3):
            y0 = random.randint(0, H - 120)
            arr[y0:y0 + 70] = np.roll(arr[y0:y0 + 70], random.randint(-26, 26), axis=1)
    frame = Image.fromarray(arr)

    # --- FX overlay ---
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # flash at scene cuts
    for s2 in SC:
        fl = seg(t, s2["t0"], s2["t0"] + 0.13)
        if 0 < fl < 1:
            d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(150 * (1 - fl))))
    # particles + speed lines + starbursts
    particles(d, t + i * 13, seed=i)
    if sc.get("hit") or sc.get("stamp"):
        speed_lines(d, t, sc["t0"])
    # stamp
    if sc.get("stamp"):
        res = stamp_layer(t, sc["t0"], sc["stamp"], y=330, base_size=112)
        if res:
            lay, yy_ = res
            ov.alpha_composite(lay, (0, yy_))
            d = ImageDraw.Draw(ov)
            u = seg(t, sc["t0"], sc["t0"] + 0.5)
            starburst(d, W * 0.16, yy_ + 120, 130, u)
            starburst(d, W * 0.84, yy_ + 120, 130, u * 0.8)
    # header (word-by-word)
    if sc.get("header"):
        fs = fit_size(sc["header"], 92, 0.90)
        draw_word_line(d, sc["header"].split(), t, sc["t0"] + 0.12, 340, fs, "white")
    if sc.get("hud"):
        hud_anim(d, t, sc["t0"] + 0.35, sc["hud"], y=560)
    if sc.get("counter"):
        yy2 = 700
        vals = sc["counter"]
        tstep = (min(dur * 0.5, 1.5)) / max(len(vals) - 1, 1)
        steps = [(v, sc["t0"] + 0.55 + k * tstep, sc["t0"] + 0.55 + (k + 1) * tstep) for k, v in enumerate(vals)]
        steps[-1] = (vals[-1], steps[-1][1], sc["t1"])
        stepped_counter(d, t, steps, yy2, base=118)
    if sc.get("roll"):
        rolling_number(d, t, sc["t0"] + 0.4, sc["t0"] + min(dur * 0.62, 2.6), sc["roll"][-1], y=470, base=112)
        if t > sc["t0"] + 0.4:
            pass
    if sc.get("sub"):
        st0 = sc["t0"] + 0.55
        u = seg(t, st0, st0 + 0.4)
        if u > 0:
            fs = fit_size(sc["sub"], 52, 0.88)
            fnt = font(fs)
            tw = d.textlength(sc["sub"], font=fnt)
            d.text(((W - tw) / 2, 900 + (1 - ease_out_back(u)) * 40), sc["sub"],
                   font=fnt, fill=(255, 215, 0, int(255 * u)), stroke_width=6,
                   stroke_fill=(0, 0, 0, int(255 * u)))

    frame = Image.alpha_composite(frame.convert("RGBA"), ov)

    # persistent UI
    ui = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    du = ImageDraw.Draw(ui)
    du.rectangle([0, 0, W, 14], fill=(10, 12, 20, 170))
    du.rectangle([0, 0, int(W * min(t / TV, 1)), 14], fill=(255, 102, 0, 245))
    du.rounded_rectangle([36, 46, 320, 122], radius=10, fill=(11, 15, 26, 215))
    du.rectangle([58, 76, 80, 98], fill=(229, 9, 20, 255))
    du.text((94, 62), "FACT DOSSIER // 001", font=font(36), fill=(255, 255, 255, 235))
    for k in range(8):
        x = W - 330 + k * 40
        du.line([x, 62, x, 96], fill=(255, 255, 255, 120), width=3)
    frame = Image.alpha_composite(frame, ui)

    # print texture + vignette (print-boil: halftone phase crawls every frame)
    half = np.roll(np.roll(HALF_RGBA, (fi * 3) % 8, axis=0), (fi * 5) % 8, axis=1)
    frame = Image.alpha_composite(frame, Image.fromarray(half))
    frame = Image.alpha_composite(frame, Image.fromarray(VIG))
    # ending glow
    if t > TV - 3.2:
        g = seg(t, TV - 3.2, TV - 1.2)
        gl = Image.new("RGBA", (W, H), (255, 170, 60, int(26 * g)))
        frame = Image.alpha_composite(frame, gl)

    proc.stdin.write(frame.convert("RGB").tobytes())
    if fi % 150 == 0: print(f"  frame {fi}/{NFR}  t={t:.1f}s")

  proc.stdin.close()
  proc.wait()
  print("video pass done")

# ---------------- audio ----------------
print("audio...")
def aeval(name, expr, dur, extra=""):
    run([FF, "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={dur}",
         "-af", extra or "anull", f"{TMP}/{name}.wav"])
    return f"{TMP}/{name}.wav"

tw_t = SC[6]["t0"]  # twist moment
sfx_files = {}
sfx_files["whoosh"] = aeval("whoosh", "0.7*(random(0)-0.5)*exp(-9*t)*sin(2*PI*340*t)+0.5*sin(2*PI*420*t)*exp(-7*t)", 0.5)
sfx_files["slam"]   = aeval("slam", "1.0*sin(2*PI*72*t)*exp(-13*t)+0.6*sin(2*PI*46*t)*exp(-9*t)+0.3*(random(0)-0.5)*exp(-40*t)", 0.6)
sfx_files["boom"]   = aeval("boom", "1.1*sin(2*PI*42*t)*exp(-4.2*t)+0.5*sin(2*PI*28*t)*exp(-3*t)", 1.3)
sfx_files["riser"]  = aeval("riser", "0.5*sin(2*PI*(180+520*t/1.1)*t)*t", 1.1)
sfx_files["tick"]   = aeval("tick", "0.7*sin(2*PI*1550*t)*exp(-30*t)", 0.09)
sfx_files["pop"]    = aeval("pop", "0.85*sin(2*PI*640*t)*exp(-24*t)", 0.12)
sfx_files["blip"]   = aeval("blip", "0.5*(sin(2*PI*1220*t)+0.6*sin(2*PI*1880*t))*exp(-22*t)", 0.12)
sfx_files["zap"]    = aeval("zap", "0.5*(random(0)-0.5)*exp(-18*t)+0.4*sin(2*PI*(2600-1500*t)*t)*exp(-11*t)", 0.3)
sfx_files["glitch"] = aeval("glitch", "0.65*(random(0)-0.5)*(0.5+0.5*sin(2*PI*28*t))*exp(-7*t)", 0.32)
sfx_files["chord"]  = aeval("chord", "0.5*sin(2*PI*220*t)*exp(-1.8*t)+0.4*sin(2*PI*277.18*t)*exp(-1.8*t)+0.3*sin(2*PI*329.63*t)*exp(-1.5*t)", 1.8)

bpm = 102; beat = 60 / bpm
pump = ("0.30*sin(2*PI*50*t)*if(lt(mod(t,0.588),0.30),1,0.22)+0.16*sin(2*PI*100*t)*if(lt(mod(t,0.588),0.16),1,0.15)"
        "+0.055*sin(2*PI*8600*t)*if(lt(mod(t+0.294,0.588),0.05),1,0)"
        "+0.05*sin(2*PI*220*t)+0.04*sin(2*PI*277.18*t)")
run([FF, "-y", "-f", "lavfi", "-i", f"aevalsrc='{pump}':s=44100:d={TV}",
     "-af", "lowpass=f=9000,"
     f"volume='if(between(t,{tw_t-0.35:.2f},{tw_t+0.5:.2f}),0.10,1)':eval=frame,"
     f"afade=t=in:d=0.7,afade=t=out:st={TV-2.2}:d=2.2", f"{TMP}/music.wav"])

# SFX schedule
ev = []  # (file, time, vol)
for s in SC:
    ev.append(("whoosh", s["t0"] - 0.05, 0.32))
    if s.get("stamp"): ev.append(("slam", s["t0"], 0.9)); ev.append(("pop", s["t0"] + 0.30, 0.5))
    if s.get("header"): ev.append(("pop", s["t0"] + 0.12, 0.55))
    if s.get("hud"): ev.append(("blip", s["t0"] + 0.35, 0.5)); ev.append(("blip", s["t0"] + 0.75, 0.4))
    if s.get("counter"):
        tstep = (min((s["t1"] - s["t0"]) * 0.5, 1.5)) / max(len(s["counter"]) - 1, 1)
        for k in range(len(s["counter"]) + 2):
            ev.append(("tick", s["t0"] + 0.55 + k * tstep * 0.55, 0.5))
    if s.get("roll"):
        for k in range(7):
            ev.append(("tick", s["t0"] + 0.5 + k * 0.22, 0.42))
        ev.append(("pop", s["t0"] + min((s["t1"] - s["t0"]) * 0.62, 2.6), 0.7))
    if s.get("sub"): ev.append(("pop", s["t0"] + 0.55, 0.42))
ev.append(("riser", tw_t - 1.15, 0.55))
ev.append(("boom", tw_t + 0.42, 0.95))
ev.append(("glitch", tw_t + 0.04, 0.62))
ev.append(("zap", T[2] + 0.2, 0.5))
ev.append(("chord", T[8], 0.85))
ev = [(f, max(0.0, t), v) for f, t, v in ev if t < TV]

mix = "[1:a]volume=1.06[vo];[2:a]volume=0.30[mus];"
inputs = [VO_P, f"{TMP}/music.wav"]
keys = ["vo", "mus"]
for k, (fname, tt, vv) in enumerate(ev):
    p = sfx_files[fname]
    inputs.append(p)
    ms = int(tt * 1000)
    mix += f"[{k+3}:a]volume={vv},adelay={ms}|{ms}[e{k}];"
    keys.append(f"e{k}")
mix += "".join(f"[{k}]" for k in keys) + f"amix=inputs={len(keys)}:duration=first:normalize=0[mx];"
mix += "[mx]loudnorm=I=-14:TP=-1.2:LRA=11[aout]"

cmd = [FF, "-y", "-i", raw]
for p in inputs: cmd += ["-i", p]
final = os.path.join(OUT, "mirchi-gulshan-V3.mp4")
cmd += ["-filter_complex", mix, "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-movflags", "+faststart", "-t", str(TV), final]
run(cmd)
print("DONE:", final, f"{os.path.getsize(final)/1e6:.1f}MB  TV={TV}s  events={len(ev)}")
