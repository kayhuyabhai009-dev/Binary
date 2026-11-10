#!/usr/bin/env python3
# V2 — Exact Gulshan editing style: comic visuals + motion graphics + stamps/counters/HUD
import imageio_ffmpeg, subprocess, os, re, struct

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = "/home/user/Binary/video-project"
A = f"{BASE}/assets"; AUD = f"{BASE}/audio"; TMP = f"{BASE}/tmp2"; OUT = f"{BASE}/output"
for d in (TMP, OUT): os.makedirs(d, exist_ok=True)
W, H, FPS = 1080, 1920, 30

import matplotlib
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
FONT = os.path.join(FDIR, "DejaVuSans-Bold.ttf")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", " ".join(map(str, cmd))[:200])
        errs = [x for x in r.stderr.splitlines() if re.search(r"[Ee]rror|nvalid|railing|No such|nknown|nable|yntax|annot", x)]
        for l in (errs[-8:] or r.stderr.splitlines()[-6:]): print("  >", l)
        raise SystemExit(1)
    return r

# ============ 1. VO + micro-acting (pitch/tempo chunks + twist pause) ============
r = subprocess.run([FF, "-i", f"{AUD}/vo.mp3"], capture_output=True, text=True)
m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
D = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
TV = D + 1.2
print(f"VO={D:.2f}  TV={TV:.2f}")

def build_vo():
    try:
        rr = run([FF, "-i", f"{AUD}/vo.mp3", "-af",
                  "silencedetect=n=-33dB:d=0.22", "-f", "null", "-"])
        sil = []
        for a, b in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", rr.stderr):
            sil.append((float(a), float(b)))
        chunks, cur = [], 0.0
        for s, e in sil:
            if s - cur > 0.15: chunks.append((cur, s))
            cur = e
        if D - cur > 0.15: chunks.append((cur, D))
        print("VO chunks:", len(chunks))
        files = []
        tw = max(range(len(chunks)), key=lambda i: -(abs(chunks[i][0] - 0.68*D)))  # chunk near 68%
        for i, (a, b) in enumerate(chunks):
            fx = "atempo=1.0"
            if i == 1: fx = "asetrate=44100*1.035,aresample=44100,atempo=1.0"   # hook tail: pitch up
            if i == tw: fx = "atempo=0.90"                                        # twist: slower, gravity
            if i == len(chunks)-1: fx = "atempo=0.93,volume=0.96"                 # close: soft
            f = f"{TMP}/vc{i}.wav"
            run([FF, "-y", "-ss", str(a), "-t", str(b-a+0.05), "-i", f"{AUD}/vo.mp3",
                 "-af", f"{fx},aformat=sample_rates=44100:channel_layouts=mono", f])
            if i == tw:  # 0.35s dramatic silence BEFORE the twist line
                run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35", f"{TMP}/gap.wav"])
                files.append(f"{TMP}/gap.wav")
            files.append(f)
        with open(f"{TMP}/vlist.txt", "w") as fh:
            fh.write("".join(f"file '{p}'\n" for p in files))
        run([FF, "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/vlist.txt",
             "-c:a", "pcm_s16le", f"{TMP}/vo2.wav"])
        return f"{TMP}/vo2.wav"
    except SystemExit:
        raise
    except Exception as ex:
        print("VO surgery fallback:", ex)
        run([FF, "-y", "-i", f"{AUD}/vo.mp3", "-c:a", "pcm_s16le", f"{TMP}/vo2.wav"])
        return f"{TMP}/vo2.wav"
VO2 = build_vo()

# ============ 2. halftone dots texture ============
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
for yy in [i/60 for i in range(61)]:
    for xx in [i/34 for i in range(35)]:
        ax.plot(xx, yy, marker="o", markersize=2.4, color=(0, 0, 0, 0.16))
fig.savefig(f"{TMP}/halftone.png", transparent=True); plt.close(fig)

# ============ 3. SFX + music ============
def aeval(name, expr, dur, extra=""):
    cmd = [FF, "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={dur}"]
    if extra: cmd += ["-af", extra]
    cmd += [f"{TMP}/{name}.wav"]; run(cmd)

aeval("whoosh", "0.7*(sin(2*PI*260*t)+0.8*sin(2*PI*430*t))*exp(-5.5*t)*(1-exp(-34*t))", 0.7, "lowpass=f=2600,afade=t=out:st=0.4:d=0.3")
aeval("slam",   "1.0*sin(2*PI*72*t)*exp(-13*t)+0.6*sin(2*PI*46*t)*exp(-9*t)+0.3*(random(0)-0.5)*exp(-40*t)", 0.55, "lowpass=f=900")
aeval("boom",   "0.95*sin(2*PI*48*t)*exp(-3.0*t)+0.4*sin(2*PI*71*t)*exp(-5*t)", 1.5, "lowpass=f=240")
aeval("tick",   "0.55*sin(2*PI*2300*t)*exp(-60*t)", 0.1, "highpass=f=1300")
aeval("beep",   "0.35*sin(2*PI*1450*t)*exp(-22*t)", 0.14, "highpass=f=900")
aeval("zap",    "0.5*(random(0)-0.5)*exp(-18*t)+0.35*sin(2*PI*180*t)*exp(-10*t)", 0.3, "highpass=f=300,lowpass=f=5200")
aeval("glitch", "0.45*(random(0)-0.5)*(0.5+0.5*sin(2*PI*28*t))", 0.32, "bandpass=f=1600:width_type=h:w=2200")
aeval("riser",  "0.5*(sin(2*PI*(180+520*t/1.1)*t))*exp(-0.4*t)", 1.15, "afade=t=out:st=0.95:d=0.2")
aeval("chord",  "0.15*sin(2*PI*220*t)*(1-exp(-8*t))*exp(-1.1*t)+0.12*sin(2*PI*277.18*t)*(1-exp(-8*t))*exp(-1.1*t)+0.10*sin(2*PI*329.63*t)*(1-exp(-8*t))*exp(-1.1*t)", 2.8, "lowpass=f=2400,afade=t=out:st=2.3:d=0.5")

# driving synth-pulse music (102 BPM) with twist hole
pump = ("0.30*sin(2*PI*50*t)*if(lt(mod(t,0.588),0.30),1,0.22)+0.16*sin(2*PI*100*t)*if(lt(mod(t,0.588),0.16),1,0.15)"
        "+0.055*sin(2*PI*8600*t)*if(lt(mod(t+0.294,0.588),0.05),1,0)"
        "+0.05*sin(2*PI*220*t)+0.04*sin(2*PI*277.18*t)")
run([FF, "-y", "-f", "lavfi", "-i", f"aevalsrc='{pump}':s=44100:d={TV}",
     "-af", f"lowpass=f=9000,volume=1.0,volume='if(between(t,{'%.2f'%(0.610*TV)},{'%.2f'%(0.610*TV+0.55)}),0.12,1)':eval=frame,afade=t=in:d=0.8,afade=t=out:st={TV-1.8}:d=1.8",
     f"{TMP}/music.wav"])

# ============ 4. scenes ============
fr = [0.0, 0.068, 0.145, 0.252, 0.368, 0.494, 0.610, 0.800, 0.905, 1.0]
T  = [round(f*TV, 3) for f in fr]
segs = [round(T[i+1]-T[i], 3) for i in range(9)]
imgs = ["c1-hook","c2-brain","c3-receptors","c4-alarm","c5-water","c6-ghost","c7-bird","c8-tears","c1-hook"]
shake_scenes = {0, 3, 6}   # stamp scenes shake on entry

parts = []
for i, (name, seg) in enumerate(zip(imgs, segs)):
    zoom = "1.16-0.16*min(on/14,1)+0.0005*on" if i % 2 == 0 else "max(1.14-0.0011*on,1.0)"
    shake = f"if(lt(t,0.45),sin(t*58)*11,0)" if i in shake_scenes else "0"
    parts.append(
        f"[{i}:v]scale=1120:1976:force_original_aspect_ratio=increase,crop=1120:1976,"
        f"fps={FPS},"
        f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1120x1976:fps={FPS},"
        f"setpts=N/{FPS}/TB,"
        f"crop=1080:1920:x='20+{shake}':y=28,setsar=1,trim=duration={seg},setpts=PTS-STARTPTS[v{i}];")
vc = "".join(parts)
vc += "".join(f"[v{i}]" for i in range(9)) + "concat=n=9:v=1:a=0[vcat];"

# ============ 5. motion-graphic text system ============
def fit(text, base, width=0.92):
    L = max(len(l) for l in text.strip().split("\n"))
    return min(base, int(W*width/(max(L,1)*0.62)))
def tfit(tf, base, frac=0.90): return fit(open(tf).read(), base, frac)

def fade(t0, t1):
    return (f"if(lt(t,{t0}),0,if(lt(t,{t0}+0.28),(t-{t0})/0.28,"
            f"if(lt(t,{t1}-0.25),1,if(lt(t,{t1}),max(0,({t1}-t)/0.25),0))))")

def header(t0, t1, txtfile, y=340, size=92, color="white", style="slide"):
    size = tfit(txtfile, size, 0.90)
    if style == "slide":
        x = f"min((w-text_w)/2,-950+(t-{t0})*3200)"
    else:
        x = "(w-text_w)/2"
    return (f"drawtext=fontfile={FONT}:textfile={txtfile}:fontcolor={color}:fontsize={size}:"
            f"x='{x}':y={y}:borderw=8:bordercolor=black:alpha='{fade(t0,t1)}'")

def stamp(t0, t1, txtfile, y=380, size=112, box="0xC1121F@0.94"):
    size = tfit(txtfile, size, 0.84)
    yy = f"if(lt(t,{t0}+0.22),-420+(t-{t0})/0.22*800,{y})"
    return (f"drawtext=fontfile={FONT}:textfile={txtfile}:fontcolor=white:fontsize={size}:"
            f"x=(w-text_w)/2:y='{yy}':box=1:boxcolor={box}:boxborderw=28:alpha='{fade(t0,t1)}'")

def hudline(t0, t1, y=560, x0=180, ln=640, label_tf=None, label_y=600, label_size=44, label_color="white"):
    fs = [f"drawbox=x={x0}:y={y}:w='min((t-{t0})*2600,{ln})':h=5:color=white@0.9:t=fill:enable='between(t,{t0},{t1})'",
          f"drawbox=x={x0-9}:y={y-7}:w=19:h=19:color=white@0.95:t=fill:enable='between(t,{t0},{t1})'"]
    if label_tf:
        L = max(len(l) for l in open(label_tf).read().strip().split("\n"))
        label_size = min(label_size, int((W-x0-60)/(max(L,1)*0.62)))
        fs.append(f"drawtext=fontfile={FONT}:textfile={label_tf}:fontcolor={label_color}:fontsize={label_size}:"
                  f"x={x0}:y={label_y}:borderw=4:bordercolor=black:alpha='{fade(t0+0.18,t1)}'")
    return fs

def counter(t0, t1, steps, y=430, base=128):
    fs = []
    n = len(steps)
    for k, (tf, ta, tb) in enumerate(steps):
        size = tfit(tf, base, 0.88)
        fs.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontcolor=0xFFD700:fontsize={size}:"
                  f"x=(w-text_w)/2:y={y}:borderw=8:bordercolor=black:enable='between(t,{ta},{tb})'")
    return fs

fx = "[vcat]"
fx += f"drawbox=x=0:y=0:w={W}:h={H}:color=white@0.5:t=fill:enable='between(t,{T[0]},{T[0]+0.07})',"
fx += f"drawbox=x=0:y=0:w={W}:h={H}:color=white@0.5:t=fill:enable='between(t,{T[3]},{T[3]+0.07})',"
fx += f"drawbox=x=0:y=0:w={W}:h={H}:color=white@0.45:t=fill:enable='between(t,{T[6]},{T[6]+0.07})',"

# scene labels (0-based windows)
LBL = {}
def wtxt(i, key, text):
    p = f"{TMP}/s{i}_{key}.txt"; open(p, "w").write(text); return p

# s0 hook: SLAM header + sub
fx += ",".join([
    stamp(T[0], T[1], wtxt(0, "h", "NOT ACTUALLY HOT"), y=360),
    header(T[0]+0.28, T[1], wtxt(0, "s", "THE BURN IS A LIE"), y=560, size=54, color="0xFFD700", style="pop"),
]) + ","
# s1 brain: slide header + HUD
fx += ",".join([
    header(T[1], T[2], wtxt(1, "h", "YOUR BRAIN GETS TRICKED"), y=330, size=86),
    *hudline(T[1]+0.3, T[2], y=520, x0=210, ln=560, label_tf=wtxt(1, "s", "PAIN ALARM: FAKE SIGNAL"), label_y=560),
]) + ","
# s2 receptors: header + sub + zap moment label
fx += ",".join([
    header(T[2], T[3], wtxt(2, "h", "PAIN RECEPTORS TRIPPED"), y=330, size=84, style="pop"),
    header(T[2]+0.35, T[3], wtxt(2, "s", "CAPSAICIN SENDS THE ALARM"), y=520, size=52, color="0xFFD700", style="pop"),
]) + ","
# s3 alarm: SLAM stamp + stepped counter 0 degrees
fx += ",".join([
    stamp(T[3], T[4], wtxt(3, "h", "FAKE ALARM"), y=330, size=116),
    header(T[3]+0.3, T[4], wtxt(3, "s", "BURNING SIGNAL • ZERO REAL HEAT"), y=520, size=48, style="pop"),
    *counter(T[3]+0.5, T[4], [
        (wtxt(3, "c1", "TEMP CHANGE: 12°"), T[3]+0.5, T[3]+0.9),
        (wtxt(3, "c2", "TEMP CHANGE: 3°"),  T[3]+0.9, T[3]+1.25),
        (wtxt(3, "c3", "TEMP CHANGE: 0°"),  T[3]+1.25, T[4]),
    ], y=660, base=96),
]) + ","
# s4 water: header + HUD
fx += ",".join([
    header(T[4], T[5], wtxt(4, "h", "WATER SPREADS THE BURN"), y=330, size=84, style="pop"),
    *hudline(T[4]+0.35, T[5], y=520, x0=210, ln=560, label_tf=wtxt(4, "s", "IT IS NOT HOTTER"), label_y=560),
]) + ","
# s5 ghost: running counter + sub
fx += ",".join([
    header(T[5], T[5]+2.0, wtxt(5, "h", "SCOVILLE SCALE"), y=300, size=64, style="pop"),
    *counter(T[5]+0.3, T[6], [
        (wtxt(5, "c1", "127,450"),     T[5]+0.3,  T[5]+0.75),
        (wtxt(5, "c2", "512,900"),     T[5]+0.75, T[5]+1.15),
        (wtxt(5, "c3", "884,200"),     T[5]+1.15, T[5]+1.5),
        (wtxt(5, "c4", "1,041,427"),   T[5]+1.5,  T[6]),
    ], y=420, base=132),
    header(T[5]+1.6, T[6], wtxt(5, "s", "BHUT JOLOKIA • INDIA"), y=640, size=54, color="white", style="pop"),
]) + ","
# s6 bird: SLAM stamp + HUD
fx += ",".join([
    stamp(T[6], T[7], wtxt(6, "h", "THE PLANT'S TRICK"), y=330, size=110),
    *hudline(T[6]+0.35, T[7], y=540, x0=180, ln=680, label_tf=wtxt(6, "s", "BIRDS CANNOT FEEL THE BURN"), label_y=580, label_size=46, label_color="0xFFD700"),
]) + ","
# s7 tears + s8 loop: final quote spans to end
fx += ",".join([
    header(T[7], TV, wtxt(7, "h", "A PLANT'S CLEVER TRICK"), y=820, size=94, style="pop"),
    header(T[7]+0.4, TV, wtxt(7, "s", "IT WAS NEVER YOUR WEAKNESS"), y=990, size=52, color="0xFFD700", style="pop"),
]) + ","

# persistent UI: progress bar + REC pill + ruler ticks + halftone overlay
fx += (f"drawbox=x=0:y=0:w={W}:h=16:color=black@0.6:t=fill,"
       f"drawbox=x=0:y=0:w='min(t/{TV},1)*{W}':h=16:color=FF6600@0.95:t=fill,"
       f"drawbox=x=40:y=52:w=228:h=66:color=0x0B0F1A@0.85:t=fill,"
       f"drawbox=x=62:y=80:w=18:h=18:color=0xE50914@1:t=fill,"
       f"drawtext=fontfile={FONT}:text='FACT DOSSIER // 001':fontcolor=white:fontsize=38:x=92:y=86,"
       f"drawtext=fontfile={FONT}:text='|  |  |  |  |  |  |  |':fontcolor=white@0.55:fontsize=34:x={W-330}:y=66"
       f"[vui];[vui][11:v]overlay=0:0:format=auto[vout]")

# ============ 6. audio mix ============
NB_SFX = 12   # whoosh x9, slam x3, boom, tick x5, beep x4, zap, glitch, riser, chord -> count computed below
mix = "[9:a]volume=1.04[vo];[10:a]volume=0.30[mus];"
ad = []
n = 12  # sfx inputs start at 12 (0-8 imgs, 9 vo2, 10 music, 11 halftone png)
def sfx(fname, t, vol, key):
    global n, mix
    ms = int(max(t, 0)*1000)
    mix += f"[{n}:a]volume={vol},adelay={ms}|{ms}[{key}];"
    ad.append(f"{TMP}/{fname}.wav"); n += 1

for j in range(9):
    sfx("whoosh", T[j]-0.06, 0.34, f"wh{j}")
sfx("slam", T[0],       0.85, "sl0"); sfx("slam", T[3],  0.85, "sl3"); sfx("slam", T[6], 0.85, "sl6")
sfx("boom", T[6]+0.55,  0.9,  "bm")      # twist impact after music hole
sfx("riser", T[6]-1.1,  0.5,  "rs")
for k in range(5): sfx("tick", T[5]+0.3+k*0.38, 0.55, f"tk{k}")
for k in range(4): sfx("beep", T[1]+0.35+k*1.1, 0.35, f"bp{k}")
sfx("zap",    T[2]+0.4, 0.55, "zp")
sfx("glitch", T[3]+0.05, 0.6, "gl")
sfx("chord",  T[7],      0.8,  "ch")

keys = ["vo","mus"] + [f"wh{j}" for j in range(9)] + ["sl0","sl3","sl6","bm","rs"] + \
       [f"tk{k}" for k in range(5)] + [f"bp{k}" for k in range(4)] + ["zp","gl","ch"]
mix += "".join(f"[{k}]" for k in keys) + f"amix=inputs={len(keys)}:duration=first:normalize=0[mx];"
mix += "[mx]loudnorm=I=-14:TP=-1.2:LRA=11[aout]"

# ============ 7. assemble ============
cmd = [FF, "-y"]
for i in range(9): cmd += ["-loop", "1", "-t", str(segs[i]), "-i", f"{A}/{imgs[i]}.png"]
cmd += ["-i", VO2, "-i", f"{TMP}/music.wav", "-i", f"{TMP}/halftone.png"]
for p in ad: cmd += ["-i", p]
import json
open(f"{TMP}/fc.txt", "w").write(vc + fx + ";" + mix)
open(f"{TMP}/cmd.json", "w").write(json.dumps(cmd))
cmd += ["-filter_complex", vc + fx + ";" + mix,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-ar", "44100",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(TV),
        f"{OUT}/mirchi-gulshan-style-V2.mp4"]
run(cmd)
print("DONE:", f"{OUT}/mirchi-gulshan-style-V2.mp4",
      f"{os.path.getsize(f'{OUT}/mirchi-gulshan-style-V2.mp4')/1e6:.1f}MB")
