"""Build a vertical Short from a spec JSON: one-take Gemini TTS, beats aligned by transcribing the speech between pauses -> timed motion graphics -> MP4.

Usage: python3 build.py specs/<name>.json out_dir
"""
import base64, json, os, re, subprocess, sys, time, urllib.request, wave
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"
TTS_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-tts:streamGenerateContent?alt=sse"
RATE, TAIL = 24000, 0.8


def tts(text, voice):
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(TTS_URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
    for attempt in range(8):
        try:
            pcm = b""  # streamed so long takes don't hit the proxy's idle timeout
            for line in urllib.request.urlopen(req, timeout=300):
                if line.startswith(b"data: "):
                    for c in json.loads(line[6:]).get("candidates", []):
                        pcm += b"".join(base64.b64decode(p["inlineData"]["data"])
                                        for p in c.get("content", {}).get("parts", []) if "inlineData" in p)
            return pcm
        except Exception as e:
            print("tts retry", attempt, e)
            time.sleep(15 * (attempt + 1))  # TTS quota is 10 requests/minute
    raise SystemExit("TTS failed: " + text)


def silences(wav):
    out = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-40dB:d=0.2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(l.split("silence_start: ")[1]) for l in out.splitlines() if "silence_start" in l]
    en = [float(l.split("silence_end: ")[1].split()[0]) for l in out.splitlines() if "silence_end" in l]
    return list(zip(st, en))


def transcribe(mp3, start, end):
    clip = mp3[:-4] + f".{start:.2f}.mp3"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-to", str(end), "-i", mp3, clip], check=True)
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/mp3", "data": base64.b64encode(open(clip, "rb").read()).decode()}},
                                    {"text": "Write down every spoken word in this audio clip, verbatim. Only the words."}]}]}
    os.remove(clip)
    for attempt in range(5):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(TEXT_URL, json.dumps(body).encode(), {"Content-Type": "application/json"}), timeout=60))
            return d["candidates"][0]["content"]["parts"][-1]["text"]
        except Exception as e:
            print("transcribe retry", attempt, e); time.sleep(5 * (attempt + 1))
    return ""


def words(t):
    return re.findall(r"[a-z0-9]+", t.lower().replace("-", " "))


def align(beats, sil, total, mp3):
    """Transcribe the speech between pauses and map each script line to the chunks that hold its words."""
    edges = [0.0] + [x for s in sil for x in s] + [total]
    chunks = [(a, b) for a, b in zip(edges[::2], edges[1::2]) if b - a > 0.08]
    with ThreadPoolExecutor(6) as ex:
        heard = list(ex.map(lambda c: words(transcribe(mp3, max(0, c[0] - 0.05), c[1] + 0.05)), chunks))
    said, script = sum(map(len, heard)), sum(len(words(b["text"])) for b in beats)
    if abs(said - script) > 0.15 * script or "narrator" in sum(heard, []):
        raise SystemExit(f"voiceover does not match script ({said} words heard vs {script}); rebuild with FRESH_VOICE=1")
    cum, offs = [0], [0]
    for h in heard: cum.append(cum[-1] + len(h))
    for b in beats[:-1]: offs.append(offs[-1] + len(words(b["text"])))
    def cost(j, i):  # distance from the expected word offset, minus a bonus when the chunk opens with the line's first words
        lead = words(beats[i]["text"])[:2]
        return abs(cum[j] * script / said - offs[i]) - (4 if heard[j][:2] == lead else 1.5 if heard[j][:1] == lead[:1] else 0)
    first = [0]
    for i in range(1, len(beats)):
        first.append(min(range(first[-1] + 1, len(chunks)), key=lambda j: cost(j, i)))
    for i, b in enumerate(beats):
        last = (first[i + 1] if i + 1 < len(beats) else len(chunks)) - 1
        b["start"], b["end"] = round(chunks[first[i]][0], 3), round(chunks[max(last, first[i])][1], 3)


def main(spec_path, out):
    spec = json.load(open(spec_path))
    os.makedirs(out, exist_ok=True)
    voice = spec.get("voice", "Charon")
    if os.path.exists(f"{out}/voiceover.mp3") and not os.environ.get("FRESH_VOICE"):  # keep an approved take
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{out}/voiceover.mp3", "-ac", "1", "-ar", str(RATE), f"{out}/voiceover.wav"], check=True)
        w = wave.open(f"{out}/voiceover.wav"); total = w.getnframes() / RATE; w.close()
    else:
        pcm = tts("\n\n".join(b["text"] for b in spec["beats"]), voice)
        audio = b"\0\0" * int(RATE * 0.3) + pcm + b"\0\0" * int(RATE * TAIL)
        total = len(audio) / 2 / RATE
        w = wave.open(f"{out}/voiceover.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(audio); w.close()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{out}/voiceover.wav", "-b:a", "160k", f"{out}/voiceover.mp3"], check=True)
    align(spec["beats"], silences(f"{out}/voiceover.wav"), total, f"{out}/voiceover.mp3")
    for b in spec["beats"]:
        print(f'{b["start"]:6.2f}-{b["end"]:6.2f}  {b["text"]}')

    html = open(f"{HERE}/template.html").read().replace("/*SPEC*/null", json.dumps(spec))
    open(f"{out}/motion-graphics.html", "w").write(html)
    open(f"{out}/script.txt", "w").write("\n\n".join(b["text"] for b in spec["beats"]) + "\n")

    frames = f"{out}/.frames"
    subprocess.run(["rm", "-rf", frames]); os.makedirs(frames)
    subprocess.run(["node", f"{HERE}/render.js", os.path.abspath(f"{out}/motion-graphics.html"), frames, str(total)], check=True)
    mp4 = f"{out}/{spec['slug']}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", f"{frames}/f%05d.jpg", "-i", f"{out}/voiceover.wav",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", mp4], check=True)
    subprocess.run(["rm", "-rf", frames, f"{out}/voiceover.wav"])
    print(f"done {mp4} {total:.1f}s")


if __name__ == "__main__":
    main(*sys.argv[1:3])
