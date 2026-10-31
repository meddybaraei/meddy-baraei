"""Build a 16:9 lesson video for Run It With AI from a script JSON.

Each segment = one Gemini TTS take + one slide whose bullets appear one by one.
Usage: python3 make_lesson.py SCRIPT.json OUT.mp4   (FRESH_VOICE=1 re-records all takes)
"""
import base64, json, os, subprocess, sys, time, urllib.request, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TTS_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-tts:streamGenerateContent?alt=sse"
RATE, GAP = 24000, 0.45
W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
BLACK = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
if not os.path.exists(BLACK):
    BLACK = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
SEMI = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
MED = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BLUE, WHITE, SOFT = (0, 175, 255), (255, 255, 255), (205, 215, 235)


def tts(text, voice, style):
    body = {"contents": [{"parts": [{"text": f"{style}\n\n{text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(TTS_URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
    for attempt in range(8):
        try:
            pcm = b""
            for line in urllib.request.urlopen(req, timeout=300):
                if line.startswith(b"data: "):
                    for c in json.loads(line[6:]).get("candidates", []):
                        pcm += b"".join(base64.b64decode(p["inlineData"]["data"])
                                        for p in c.get("content", {}).get("parts", []) if "inlineData" in p)
            if pcm:
                return pcm
            raise RuntimeError("empty audio")
        except Exception as e:
            print("tts retry", attempt, e, flush=True)
            time.sleep(15 * (attempt + 1))
    raise SystemExit("TTS failed")


def background():
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(8 + 12 * t), int(10 + 14 * t), int(25 + 35 * t)))
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W * 0.45, -300, W + 300, H * 0.8], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(220)).point(lambda v: int(v * 0.35))
    return Image.composite(Image.new('RGB', (W, H), (20, 90, 200)), img, glow)


def wrap(d, text, font, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            test = (cur + " " + word).strip()
            if d.textlength(test, font=font) <= maxw:
                cur = test
            else:
                lines.append(cur); cur = word
        lines.append(cur)
    return lines


def slide(bg, seg, shown, idx, total):
    img = bg.copy(); d = ImageDraw.Draw(img)
    # brand mark
    r = 26; cx, cy = 110, 90
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    d.polygon([(cx - r * .38, cy - r * .6), (cx - r * .38, cy + r * .6), (cx + r * .62, cy)], fill=WHITE)
    d.text((150, 72), "RUN IT WITH AI", font=ImageFont.truetype(BLACK, 32), fill=WHITE)
    # progress bar
    d.rounded_rectangle([110, H - 60, W - 110, H - 52], radius=4, fill=(40, 50, 85))
    d.rounded_rectangle([110, H - 60, 110 + (W - 220) * (idx + 1) / total, H - 52], radius=4, fill=BLUE)
    bullets = seg["bullets"]
    if not bullets:  # title card
        f = ImageFont.truetype(BLACK, 108)
        lines = wrap(d, seg["title"], f, W - 300)
        y = H / 2 - len(lines) * 62 - 30
        for ln in lines:
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=WHITE); y += 124
        k = ImageFont.truetype(SEMI, 44)
        d.text(((W - d.textlength(seg["kicker"], font=k)) / 2, y + 30), seg["kicker"], font=k, fill=BLUE)
        return img
    k = ImageFont.truetype(SEMI, 40)
    d.text((150, 200), seg["kicker"].upper(), font=k, fill=BLUE)
    ft = ImageFont.truetype(BLACK, 76 if len(seg["title"]) < 40 else 64)
    y = 260
    for ln in wrap(d, seg["title"], ft, W - 300):
        d.text((150, y), ln, font=ft, fill=WHITE); y += ft.size + 14
    y += 40
    fb = ImageFont.truetype(MED, 46 if len(bullets) <= 4 else 38)
    for i, b in enumerate(bullets[:shown]):
        d.ellipse([155, y + fb.size * .35, 175, y + fb.size * .35 + 20], fill=BLUE)
        for j, ln in enumerate(wrap(d, b, fb, W - 420)):
            d.text((205, y), ln, font=fb, fill=WHITE if i == shown - 1 else SOFT); y += fb.size + 10
        y += 18
    return img


def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    work = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "build"); os.makedirs(work, exist_ok=True)
    segs = spec["segments"]; bg = background()
    durs = []
    for i, s in enumerate(segs):
        wav = f"{work}/seg{i:02d}.wav"
        if not os.path.exists(wav) or os.environ.get("FRESH_VOICE"):
            pcm = tts(s["say"], spec.get("voice", "Charon"), spec.get("style", ""))
            w = wave.open(wav, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm); w.close()
            time.sleep(7)  # TTS quota ~10 requests/minute
        w = wave.open(wav); d = w.getnframes() / RATE; w.close(); durs.append(d + GAP)
        print(f"seg {i}: {d:.1f}s", flush=True)
    # images + concat list
    lst = open(f"{work}/frames.txt", "w")
    for i, s in enumerate(segs):
        n = len(s["bullets"]); steps = max(n, 1); first = 0.6 if n else 0
        times = [durs[i]] if not n else [first + (durs[i] - first) / n] * n
        if n: times[0] = first + (durs[i] - first) / n
        for k in range(steps):
            p = f"{work}/s{i:02d}_{k}.png"; slide(bg, s, k + 1 if n else 0, i, len(segs)).save(p)
            lst.write(f"file '{p}'\nduration {times[k]:.3f}\n")
    lst.write(f"file '{p}'\n"); lst.close()
    # audio: segments with gaps
    pad = f"{work}/gap.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={RATE}:cl=mono", "-t", str(GAP), pad], check=True)
    al = open(f"{work}/audio.txt", "w")
    for i in range(len(segs)):
        al.write(f"file '{work}/seg{i:02d}.wav'\nfile '{pad}'\n")
    al.close()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/audio.txt", f"{work}/voice.wav"], check=True)
    total = sum(durs)
    music = f"{work}/music.wav"
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
