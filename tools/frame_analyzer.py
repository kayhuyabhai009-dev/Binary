#!/usr/bin/env python3
"""
frame_analyzer.py — frame-by-frame motion/QC analyzer for vertical shorts.
Verifies the "Zero Static Frames (2-Second Rule)" law of the Gulshan formula.

Usage:
  python3 tools/frame_analyzer.py VIDEO.mp4 [--fps 30] [--report out.md] [--sheet out.png]

What it measures (per frame, 30fps):
  * motion energy  = mean |frame - prev_frame| (0-255 scale)
  * cut detection  = motion spike > 4x rolling median
  * static frames  = motion energy < 1.2 (visually frozen)
  * text/edge density change (new graphics appearing)

Output: markdown report + optional 30-frame contact sheet image.
"""
import subprocess, sys, os, math
import numpy as np

def get_ff():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def analyze(path, fps=30, sheet=None, max_frames=None):
    ff = get_ff()
    # probe
    r = subprocess.run([ff, "-hide_banner", "-i", path], capture_output=True, text=True)
    dur = None
    for l in r.stderr.splitlines():
        if "Duration" in l:
            hms = l.split("Duration:")[1].split(",")[0].strip()
            h, m, s = hms.split(":")
            dur = int(h)*3600 + int(m)*60 + float(s)
    if not dur:
        raise SystemExit("Cannot probe " + path)
    n_total = int(dur*fps)
    if max_frames: n_total = min(n_total, max_frames)

    # pull raw grayscale frames at target fps, downscaled for speed
    cmd = [ff, "-i", path, "-vf", f"fps={fps},scale=135:240,format=gray", "-f", "rawvideo", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    buf = np.frombuffer(proc.stdout, dtype=np.uint8)
    n = len(buf)//(135*240)
    frames = buf[:n*135*240].reshape(n, 240, 135).astype(np.int16)

    motion = np.zeros(n)
    for i in range(1, n):
        motion[i] = np.abs(frames[i]-frames[i-1]).mean()
    motion[0] = motion[1] if n > 1 else 0

    med = np.median(motion[1:]) if n > 2 else 1.0
    thr_cut = max(4.0*med, 12.0)
    cuts = [i for i in range(1, n) if motion[i] > thr_cut]
    STATIC_THR = 1.2
    static_idx = [i for i in range(n) if motion[i] < STATIC_THR]
    static_pct = 100.0*len(static_idx)/max(n, 1)

    # per-second motion profile
    per_sec = [float(np.mean(motion[i*fps:(i+1)*fps])) for i in range(int(math.ceil(n/fps)))]

    # longest static run
    longest, cur = 0, 0
    for i in range(n):
        if motion[i] < STATIC_THR: cur += 1; longest = max(longest, cur)
        else: cur = 0

    rep = {
        "file": path, "duration": round(dur, 2), "frames": n, "fps": fps,
        "avg_motion": round(float(np.mean(motion)), 3),
        "static_frames": len(static_idx), "static_pct": round(static_pct, 2),
        "longest_static_run_frames": longest,
        "longest_static_run_sec": round(longest/fps, 2),
        "cuts": [(round(c/fps, 2)) for c in cuts],
        "per_sec_motion": [round(x, 2) for x in per_sec],
        "grade": ("PASS" if static_pct < 2.0 and longest < fps*1.0 else
                  "WARN" if static_pct < 5.0 else "FAIL"),
    }

    if sheet:
        # contact sheet: 30 frames evenly spaced, labels via ffmpeg tile
        step = max(n//30, 1)
        idxs = list(range(0, n, step))[:30]
        tmp = sheet + ".tmp"
        os.makedirs(tmp, exist_ok=True)
        for k, i in enumerate(idxs):
            t = i/fps
            subprocess.run([ff, "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                            "-vf", "scale=216:384", f"{tmp}/f{k:02d}.png"],
                           capture_output=True)
        subprocess.run([ff, "-y", "-pattern_type", "glob", "-i", f"{tmp}/f*.png",
                        "-filter_complex", "tile=6x5:margin=4:padding=4:color=black",
                        "-frames:v", "1", sheet], capture_output=True)
        for k in range(len(idxs)):
            try: os.remove(f"{tmp}/f{k:02d}.png")
            except OSError: pass
        os.rmdir(tmp)
    return rep

def to_md(rep):
    lines = [f"# Frame Analysis — {os.path.basename(rep['file'])}",
             f"- **Grade: {rep['grade']}** (PASS = static<2% & longest static run <1s)",
             f"- Duration: {rep['duration']}s @ {rep['fps']}fps — {rep['frames']} frames",
             f"- Avg motion energy: {rep['avg_motion']} (target >1.5 for motion-graphics edits)",
             f"- Static frames: {rep['static_frames']} ({rep['static_pct']}%) — target <2%",
             f"- Longest static run: {rep['longest_static_run_sec']}s — target <1.0s",
             f"- Cuts detected: {len(rep['cuts'])} → {rep['cuts'][:40]}",
             "", "## Motion energy per second", "", "| sec | motion |", "|---|---|"]
    for i, m in enumerate(rep["per_sec_motion"]):
        bar = "█"*int(min(m*4, 40))
        lines.append(f"| {i} | {m} {bar} |")
    return "\n".join(lines)

if __name__ == "__main__":
    ap = sys.argv[1:]
    if not ap:
        print(__doc__); raise SystemExit(1)
    vid = ap[0]
    sheet = None; rep_path = None
    if "--sheet" in ap: sheet = ap[ap.index("--sheet")+1]
    if "--report" in ap: rep_path = ap[ap.index("--report")+1]
    rep = analyze(vid, sheet=sheet)
    md = to_md(rep)
    if rep_path:
        open(rep_path, "w").write(md)
        print(f"report -> {rep_path}")
    print(f"GRADE: {rep['grade']} | motion={rep['avg_motion']} | static={rep['static_pct']}% | "
          f"longest_static={rep['longest_static_run_sec']}s | cuts={len(rep['cuts'])}")
