"""Build a 9:16 Short for Run It With AI from a script JSON (same format as make_lesson.py).

Each segment = one Gemini TTS take + one vertical slide whose bullets appear one by one.
Optional "chat" {user, ai} shows a mock chat panel under the bullets.
Usage: python3 make_short.py SCRIPT.json OUT.mp4   (FRESH_VOICE=1 re-records all takes)
"""
import json, os, subprocess, sys, time, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_lesson import tts, wrap, chat_panel, rounded, BLACK, SEMI, MED, BLUE, WHITE, SOFT, RATE, HERE

W, H, GAP = 1080, 1920, 0.3


def background():
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(8 + 12 * t), int(10 + 14 * t), int(25 + 35 * t)))
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W * 0.2, -400, W + 400, H * 0.45], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(200)).point(lambda v: int(v * 0.35))
    return Image.composite(Image.new('RGB', (W, H), (20, 90, 200)), img, glow)


def slide(bg, seg, shown, idx, total, show_ai=True):
    img = bg.copy(); d = ImageDraw.Draw(img)
    acc = tuple(seg.get("accent", BLUE))
    r = 30; cx, cy = 120, 150
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    d.polygon([(cx - r * .38, cy - r * .6), (cx - r * .38, cy + r * .6), (cx + r * .62, cy)], fill=WHITE)
    d.text((165, 128), "RUN IT WITH AI", font=ImageFont.truetype(BLACK, 40), fill=WHITE)
    d.rounded_rectangle([90, 230, W - 90, 240], radius=5, fill=(40, 50, 85))
    d.rounded_rectangle([90, 230, 90 + (W - 180) * (idx + 1) / total, 240], radius=5, fill=acc)
    textw = W - 180
    k = ImageFont.truetype(SEMI, 40); kt = seg["kicker"].upper(); kw = d.textlength(kt, font=k)
    d.rounded_rectangle([90, 300, 90 + kw + 44, 366], radius=33, fill=acc); d.text((112, 309), kt, font=k, fill=(10, 15, 35))
    ft = ImageFont.truetype(BLACK, 92 if len(seg["title"]) < 30 else 76)
    y = 410
    for ln in wrap(d, seg["title"], ft, textw):
        d.text((90, y), ln, font=ft, fill=WHITE); y += ft.size + 14
    y += 40
    bullets = seg["bullets"]
    fb = ImageFont.truetype(MED, 50 if len(bullets) <= 4 else 42)
    for i, b in enumerate(bullets[:shown]):
        d.ellipse([92, y + fb.size * .3, 120, y + fb.size * .3 + 28], fill=acc)
        for ln in wrap(d, b, fb, textw - 60):
            d.text((150, y), ln, font=fb, fill=WHITE if i == shown - 1 else SOFT); y += fb.size + 12
        y += 20
    if seg.get("big"):
        bf = ImageFont.truetype(BLACK, 300); bw = d.textlength(seg["big"], font=bf)
        cy2 = max(y + 330, 1250); rr = 260
        d.ellipse([W / 2 - rr, cy2 - rr, W / 2 + rr, cy2 + rr], fill=acc)
        d.text((W / 2 - bw / 2, cy2 - 190), seg["big"], font=bf, fill=(10, 15, 35))
    if seg.get("chat"):
        pw = W - 180
        full = chat_panel(seg["chat"], acc, True, size=(pw, 900))
        px_ = full.load(); ph = 900
        while ph > 120 and all(px_[x, ph - 1] == (246, 248, 252) for x in range(0, pw, 7)):
            ph -= 1
        ph = min(900, ph + 30)
        pnl = chat_panel(seg["chat"], acc, show_ai, size=(pw, 900)).crop((0, 0, pw, ph))
        py = max(y + 40, (y + H - 120 - ph) // 2)
        d.rounded_rectangle([80, py - 10, 80 + pw + 20, py + ph + 10], radius=46, fill=acc)
        img.paste(pnl, (90, py), rounded(pnl, 38))
    return img


def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    work = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "build_" + os.path.splitext(os.path.basename(out))[0])
    os.makedirs(work, exist_ok=True)
    segs = spec["segments"]; bg = background(); durs = []
    for i, s in enumerate(segs):
        wav = f"{work}/seg{i:02d}.wav"
        if not os.path.exists(wav) or os.environ.get("FRESH_VOICE"):
            pcm = tts(s["say"], spec.get("voice", "Charon"), spec.get("style", ""))
            w = wave.open(wav, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm); w.close()
            time.sleep(7)
        w = wave.open(wav); dd = w.getnframes() / RATE; w.close(); durs.append(dd + GAP)
        print(f"seg {i}: {dd:.1f}s", flush=True)
    lst = open(f"{work}/frames.txt", "w")
    for i, s in enumerate(segs):
        n = len(s["bullets"]); steps = max(n, 1)
        times = [durs[i]] if not n else [0.4 + (durs[i] - 0.4) / n] + [(durs[i] - 0.4) / n] * (n - 1)
        for k in range(steps):
            p = f"{work}/s{i:02d}_{k}.png"
            slide(bg, s, k + 1 if n else 0, i, len(segs), show_ai=(k >= n // 2)).save(p)
            lst.write(f"file '{p}'\nduration {times[k]:.3f}\n")
    lst.write(f"file '{p}'\n"); lst.close()
    pad = f"{work}/gap.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={RATE}:cl=mono", "-t", str(GAP), pad], check=True)
    with open(f"{work}/audio.txt", "w") as al:
        for i in range(len(segs)):
            al.write(f"file '{work}/seg{i:02d}.wav'\nfile '{pad}'\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/audio.txt", f"{work}/voice.wav"], check=True)
    total = sum(durs); music = f"{work}/music.wav"
    if not os.path.exists(music):
        subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "video", "tools", "make_music.py"), music, str(total + 2), "calm"], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/frames.txt",
                    "-i", f"{work}/voice.wav", "-i", music,
                    "-filter_complex", "[2:a]volume=0.10[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
                    "-map", "0:v", "-map", "[a]", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    print("done", out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
