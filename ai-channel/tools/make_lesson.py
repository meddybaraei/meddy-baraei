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


IMG_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent"


def gen_image(prompt, dst):
    import io
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": {"aspectRatio": "1:1"}}}
    for a in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(IMG_URL, json.dumps(body).encode(), {"Content-Type": "application/json"}), timeout=180))
            im = next(Image.open(io.BytesIO(base64.b64decode(x["inlineData"]["data"]))) for x in r["candidates"][0]["content"]["parts"] if "inlineData" in x)
            im.convert("RGB").resize((800, 800), Image.LANCZOS).save(dst, quality=92); return
        except Exception as e:
            print("img retry", a, e, flush=True); time.sleep(6 * (a + 1))
    raise SystemExit("image failed")


def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=r, fill=255)
    return m


def chat_panel(c, accent, show_ai, size=(820, 820)):
    pw, ph = size
    pnl = Image.new("RGB", size, (246, 248, 252)); d = ImageDraw.Draw(pnl)
    d.rectangle([0, 0, pw, 70], fill=(232, 236, 245))
    d.ellipse([24, 22, 50, 48], fill=tuple(accent)); d.text((64, 20), "AI Assistant", font=ImageFont.truetype(SEMI, 30), fill=(40, 50, 70))
    f = ImageFont.truetype(MED, 27)
    def bubble(text, y, right, fill, color):
        lines = []
        for para in text.split("\n"):
            lines += wrap(d, para, f, pw - 220) if para else [""]
        lh = f.size + 9; bh = len(lines) * lh + 30
        bw = max(d.textlength(l, font=f) for l in lines) + 44
        x0 = pw - 30 - bw if right else 30
        d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=22, fill=fill)
        yy = y + 15
        for l in lines:
            d.text((x0 + 22, yy), l, font=f, fill=color); yy += lh
        return y + bh + 22
    y = bubble(c["user"], 100, True, tuple(accent), (255, 255, 255))
    if show_ai:
        bubble(c["ai"], y, False, (255, 255, 255), (30, 40, 60))
    else:
        d.text((40, y + 6), "typing…", font=ImageFont.truetype(MED, 26), fill=(140, 150, 170))
    return pnl


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


def slide(bg, seg, shown, idx, total, art=None, show_ai=True):
    img = bg.copy(); d = ImageDraw.Draw(img)
    acc = tuple(seg.get("accent", BLUE))
    r = 26; cx, cy = 110, 90
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    d.polygon([(cx - r * .38, cy - r * .6), (cx - r * .38, cy + r * .6), (cx + r * .62, cy)], fill=WHITE)
    d.text((150, 72), "RUN IT WITH AI", font=ImageFont.truetype(BLACK, 32), fill=WHITE)
    d.rounded_rectangle([110, H - 60, W - 110, H - 52], radius=4, fill=(40, 50, 85))
    d.rounded_rectangle([110, H - 60, 110 + (W - 220) * (idx + 1) / total, H - 52], radius=4, fill=acc)
    panel = None
    if seg.get("chat"):
        panel = chat_panel(seg["chat"], acc, show_ai)
    elif art is not None:
        panel = art.resize((820, 820), Image.LANCZOS)
        pd = ImageDraw.Draw(panel, "RGBA"); tf = ImageFont.truetype(SEMI, 20); t = "AI-generated illustration"
        tw = pd.textlength(t, font=tf); pd.rounded_rectangle([820 - tw - 40, 780, 800, 812], 14, fill=(0, 0, 0, 130)); pd.text((820 - tw - 30, 783), t, font=tf, fill=WHITE)
    textw = W - 300 if panel is None else 790
    if panel is not None:
        px, py = W - 110 - 820, 150
        d.rounded_rectangle([px - 10, py - 10, px + 830, py + 830], radius=46, fill=acc)
        img.paste(panel, (px, py), rounded(panel, 38))
    bullets = seg["bullets"]
    if not bullets:
        f = ImageFont.truetype(BLACK, 96 if panel else 108)
        lines = wrap(d, seg["title"], f, textw)
        y = H / 2 - len(lines) * 56 - 40
        x = 150
        for ln in lines:
            xx = x if panel else (W - d.textlength(ln, font=f)) / 2
            d.text((xx, y), ln, font=f, fill=WHITE); y += f.size + 18
        k = ImageFont.truetype(SEMI, 46)
        xx = 150 if panel else (W - d.textlength(seg["kicker"], font=k)) / 2
        d.rounded_rectangle([xx - 18, y + 22, xx + d.textlength(seg["kicker"], font=k) + 18, y + 92], radius=34, fill=acc)
        d.text((xx, y + 30), seg["kicker"], font=k, fill=(10, 15, 35))
        return img
    k = ImageFont.truetype(SEMI, 34); kt = seg["kicker"].upper(); kw = d.textlength(kt, font=k)
    d.rounded_rectangle([140, 168, 140 + kw + 36, 222], radius=27, fill=acc); d.text((158, 176), kt, font=k, fill=(10, 15, 35))
    ft = ImageFont.truetype(BLACK, 72 if len(seg["title"]) < 34 else 60)
    y = 250
    for ln in wrap(d, seg["title"], ft, textw):
        d.text((150, y), ln, font=ft, fill=WHITE); y += ft.size + 12
    y += 34
    fb = ImageFont.truetype(MED, 42 if len(bullets) <= 4 else 34)
    for i, b in enumerate(bullets[:shown]):
        d.ellipse([152, y + fb.size * .3, 176, y + fb.size * .3 + 24], fill=acc)
        for ln in wrap(d, b, fb, textw - 60):
            d.text((200, y), ln, font=fb, fill=WHITE if i == shown - 1 else SOFT); y += fb.size + 10
        y += 16
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
    arts = {}
    for i, s in enumerate(segs):
        if s.get("img"):
            dst = f"{work}/img{i:02d}.jpg"
            if not os.path.exists(dst):
                gen_image(s["img"], dst); print("img", i, flush=True)
            arts[i] = Image.open(dst).convert("RGB")
    # images + concat list
    lst = open(f"{work}/frames.txt", "w")
    for i, s in enumerate(segs):
        n = len(s["bullets"]); steps = max(n, 1); first = 0.6 if n else 0
        times = [durs[i]] if not n else [first + (durs[i] - first) / n] * n
        if n: times[0] = first + (durs[i] - first) / n
        for k in range(steps):
            p = f"{work}/s{i:02d}_{k}.png"
            slide(bg, s, k + 1 if n else 0, i, len(segs), arts.get(i), show_ai=(k >= n // 2)).save(p)
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
