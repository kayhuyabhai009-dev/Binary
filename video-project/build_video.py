#!/usr/bin/env python3
# Creates by Gulshan style — 40s facts short builder (Hindi VO + English labels)
import imageio_ffmpeg, subprocess, os, re, math

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = "/home/user/Binary/video-project"
A = f"{BASE}/assets"; AUD = f"{BASE}/audio"; TMP = f"{BASE}/tmp"; OUT = f"{BASE}/output"
for d in (TMP, OUT): os.makedirs(d, exist_ok=True)

W, H, FPS = 1080, 1920, 30

# ---------- font ----------
import matplotlib
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
FONT = os.path.join(FDIR, "DejaVuSans-Bold.ttf")
assert os.path.exists(FONT), "font missing"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAIL:", " ".join(cmd)[:300])
        err = [l for l in r.stderr.splitlines() if l.strip()]
        print("ERROR LINES:")
        for l in err[:12]: print("  >", l)
        open(f"{TMP}/last_err.log","w").write(r.stderr)
        raise SystemExit(1)
    return r

# ---------- 1. VO duration ----------
r = subprocess.run([FF, "-i", f"{AUD}/vo.mp3"], capture_output=True, text=True)
m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
D = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
TV = D + 1.2                      # total video length
print(f"VO={D:.2f}s  VIDEO={TV:.2f}s")

# scene boundaries (fractions of TV) -> 9 segments (last = loop echo of img 01)
fr = [0.0, 0.068, 0.145, 0.252, 0.368, 0.494, 0.610, 0.800, 0.905, 1.0]
segs = [round((fr[i+1]-fr[i])*TV, 3) for i in range(9)]
T = [round(f*TV, 3) for f in fr]   # global times
print("SEGMENTS:", segs)

# ---------- 2. synth SFX + music ----------
def aeval(name, expr, dur, extra=None):
    cmd = [FF, "-y", "-f", "lavfi", "-i", f"aevalsrc={expr}:s=44100:d={dur}"]
    if extra: cmd += ["-af", extra]
    cmd += [f"{TMP}/{name}.wav"]
    run(cmd)

aeval("whoosh", "0.6*(sin(2*PI*300*t)+0.7*sin(2*PI*520*t))*exp(-6*t)*(1-exp(-30*t))", 0.8,
      "lowpass=f=2400,afade=t=out:st=0.45:d=0.35")
aeval("boom",   "0.9*sin(2*PI*50*t)*exp(-3.2*t) + 0.35*sin(2*PI*75*t)*exp(-5*t)", 1.4,
      "lowpass=f=220,afade=t=out:st=1.0:d=0.4")
aeval("thud",   "0.8*sin(2*PI*88*t)*exp(-16*t) + 0.5*sin(2*PI*55*t)*exp(-12*t)", 0.5,
      "lowpass=f=600")
aeval("tick",   "0.5*sin(2*PI*2100*t)*exp(-55*t)", 0.12, "highpass=f=1200")
aeval("chord",  "0.16*sin(2*PI*220*t)*(1-exp(-9*t))*exp(-1.15*t) + 0.13*sin(2*PI*277.18*t)*(1-exp(-9*t))*exp(-1.15*t) + 0.11*sin(2*PI*329.63*t)*(1-exp(-9*t))*exp(-1.15*t)", 2.6,
      "lowpass=f=2200,afade=t=out:st=2.1:d=0.5")

# music drone bed (length TV) with slow amplitude motion + twist hole
drone_expr = ("0.20*sin(2*PI*55*t)+0.10*sin(2*PI*82.41*t)"
              "+0.07*sin(2*PI*110*t)*(0.55+0.45*sin(2*PI*0.25*t))")
run([FF,"-y","-f","lavfi","-i",f"aevalsrc={drone_expr}:s=44100:d={TV}",
     "-af", f"lowpass=f=420,volume=1.0,volume='if(between(t,{T[6]},{T[6]+0.30}),0,1)':eval=frame,"
            f"afade=t=in:d=1.2,afade=t=out:st={TV-1.6}:d=1.6",
     f"{TMP}/drone.wav"])

# ---------- 3. text labels ----------
labels = {
 1: ("NOT ACTUALLY HOT", None, "w"),
 2: ("YOUR BRAIN GETS TRICKED", None, "w"),
 3: ("PAIN RECEPTORS TRIPPED", "CAPSAICIN SIGNAL SENT", "w"),
 4: ("FAKE ALARM", "BURNING SIGNAL • ZERO REAL HEAT", "stamp"),
 5: ("WATER SPREADS THE BURN", "IT IS NOT HOTTER", "y"),
 6: ("1,041,427 SCOVILLE", "BHUT JOLOKIA • INDIA", "y"),
 7: ("THE PLANT'S TRICK", "BIRDS CANNOT FEEL THE BURN", "w"),
 8: ("A PLANT'S CLEVER TRICK", "IT WAS NEVER YOUR WEAKNESS", "final"),
}
for i,(main,sub,style) in labels.items():
    open(f"{TMP}/t{i}_m.txt","w").write(main)
    if sub: open(f"{TMP}/t{i}_s.txt","w").write(sub)

def drawtext_seg(i, t0, t1):
    """drawtext filters for scene i in global time [t0,t1] — fade in AND out"""
    fs = []
    main, sub, style = labels[i]
    fade = (f"if(lt(t,{t0}),0,if(lt(t,{t0}+0.3),(t-{t0})/0.3,"
            f"if(lt(t,{t1}-0.25),1,if(lt(t,{t1}),max(0,({t1}-t)/0.25),0))))")
    def fit(text, base, width=0.90):
        return min(base, int(W*width/(len(text)*0.62)))
    if style == "stamp":
        fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_m.txt:fontcolor=white:fontsize={fit(main,110)}:"
                  f"x=(w-text_w)/2:y=360:box=1:boxcolor=0xC1121F@0.92:boxborderw=26:alpha='{fade}'")
        fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_s.txt:fontcolor=white:fontsize={fit(sub,50)}:"
                  f"x=(w-text_w)/2:y=560:alpha='{fade}'")
    elif style == "final":
        fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_m.txt:fontcolor=white:fontsize={fit(main,96)}:"
                  f"x=(w-text_w)/2:y=820:borderw=7:bordercolor=black:alpha='{fade}'")
        fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_s.txt:fontcolor=0xFFD700:fontsize={fit(sub,52)}:"
                  f"x=(w-text_w)/2:y=980:borderw=5:bordercolor=black:alpha='{fade}'")
    else:
        col = "white" if style == "w" else "0xFFD700"
        fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_m.txt:fontcolor={col}:fontsize={fit(main,86)}:"
                  f"x=(w-text_w)/2:y=380:borderw=7:bordercolor=black:alpha='{fade}'")
        if sub:
            fs.append(f"drawtext=fontfile={FONT}:textfile={TMP}/t{i}_s.txt:fontcolor=white:fontsize={fit(sub,52)}:"
                      f"x=(w-text_w)/2:y=540:borderw=5:bordercolor=black:alpha='{fade}'")
    return fs

# ---------- 4. video filter graph ----------
imgs = ["01-hook-chilli","02-brain-trick","03-pain-receptors","04-fake-alarm",
        "05-water","06-ghost-pepper","07-bird-seed","08-tears","01-hook-chilli"]
parts = []
for i,(name,seg) in enumerate(zip(imgs, segs)):
    zoom = (f"1+0.0011*on" if i % 2 == 0 else f"max(1.13-0.0009*on,1.0)")
    parts.append(
        f"[{i}:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
        f"fps={FPS},"
        f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
        f"setpts=N/{FPS}/TB,"
        f"vignette=angle=0.68,setsar=1,trim=duration={seg},setpts=PTS-STARTPTS[v{i}];")
vc = "".join(parts)
vc += "".join(f"[v{i}]" for i in range(9)) + "concat=n=9:v=1:a=0[vcat];"
fx = "[vcat]"
# progress bar (top) + labels
fx += f"drawbox=x=0:y=0:w={W}:h=16:color=black@0.55:t=fill,"
fx += f"drawbox=x=0:y=0:w='min(t/{TV},1)*{W}':h=16:color=FF6600@0.95:t=fill,"
for i in range(1, 9):
    if i in labels:
        t0, t1 = T[i-1], (TV if i == 8 else T[i])   # label i belongs to image[i-1] window
        fx += ",".join(drawtext_seg(i, t0, t1)) + ","
fx = fx.rstrip(",") + "[vout]"
filter_complex = vc + fx

# ---------- 5. audio mix ----------
# whoosh at scene boundaries (skip 1st), thud at scenes 4 & 6, ticks scene 6, boom at twist T[6], chord at T[8]
mix = "[9:a]volume=1.0[vo];[10:a]volume=0.17[dr];"
inputs_ad = []
n = 11
def add_adelay(fname, t, vol, key):
    global n, mix
    ms = int(t*1000)
    mix += f"[{n}:a]volume={vol},adelay={ms}|{ms}[{key}];"
    inputs_ad.append(f"{TMP}/{fname}.wav"); n += 1

bnd = [T[i] for i in range(1, 9)]
for j, t in enumerate(bnd):
    add_adelay("whoosh", max(t-0.05, 0), 0.32, f"wh{j}")
add_adelay("boom",  T[6]+0.30, 0.85, "bm")
add_adelay("thud",  T[3],      0.60, "th3")
add_adelay("thud",  T[5],      0.60, "th5")
for k in range(3):
    add_adelay("tick",  T[5]+0.15+k*0.28, 0.5, f"tk{k}")
add_adelay("chord", T[8],      0.75, "ch")

keys = ["vo","dr"] + [f"wh{j}" for j in range(len(bnd))] + ["bm","th3","th5","tk0","tk1","tk2","ch"]
mix += "".join(f"[{k}]" for k in keys) + f"amix=inputs={len(keys)}:duration=first:normalize=0[mix];"
mix += "[mix]loudnorm=I=-14:TP=-1.2:LRA=11[aout]"

# ---------- 6. assemble ----------
cmd = [FF, "-y"]
for i in range(9): cmd += ["-loop","1","-t",str(segs[i]),"-i",f"{A}/{imgs[i]}.png"]
cmd += ["-i", f"{AUD}/vo.mp3", "-i", f"{TMP}/drone.wav"]
for p in inputs_ad: cmd += ["-i", p]
cmd += ["-filter_complex", filter_complex+";"+mix,
        "-map","[vout]","-map","[aout]",
        "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-movflags","+faststart",
        "-t", str(TV), f"{OUT}/mirchi-brain-hack-40s.mp4"]
run(cmd)
sz = os.path.getsize(f"{OUT}/mirchi-brain-hack-40s.mp4")/1e6
print(f"DONE -> {OUT}/mirchi-brain-hack-40s.mp4 ({sz:.1f} MB, {TV:.1f}s)")
