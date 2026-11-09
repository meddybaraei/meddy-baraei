"""Transcribe each beat's audio window and print it next to the script line: python3 verify.py shorts/<name>"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from build import transcribe

out = sys.argv[1]
spec = json.loads(re.search(r"const SPEC=(.*?);\n", open(f"{out}/motion-graphics.html").read()).group(1))
with ThreadPoolExecutor(6) as ex:
    heard = list(ex.map(lambda b: transcribe(f"{out}/voiceover.mp3", b["start"], b["end"]), spec["beats"]))
for b, h in zip(spec["beats"], heard):
    print(f'{b["start"]:6.2f}-{b["end"]:6.2f}\n  script: {b["text"]}\n  heard:  {h.strip()}')


def full_check(out):
    """Transcribe the whole voiceover as one wav (short snippets can make the transcriber invent words)
    and confirm it starts with the script's first words, i.e. no spoken style direction."""
    import base64, subprocess, urllib.request
    from build import TEXT_URL, words
    wav = f"{out}/.full.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{out}/voiceover.mp3", "-ac", "1", "-ar", "16000", wav], check=True)
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(wav, "rb").read()).decode()}},
                                    {"text": "Transcribe this audio verbatim. Only the words."}]}]}
    os.remove(wav)
    d = json.load(urllib.request.urlopen(urllib.request.Request(TEXT_URL, json.dumps(body).encode(), {"Content-Type": "application/json"}), timeout=120))
    heard = d["candidates"][0]["content"]["parts"][-1]["text"].strip()
    # spoken direction would come before the script, so the first word must match
    # (only one word: numbers like "5 PM" vs "5:00 p.m." tokenize differently)
    ok = words(heard)[:1] == words(spec["beats"][0]["text"])[:1]
    print(f"\nFULL TRANSCRIPT ({'OK: starts with the script' if ok else 'CHECK: does not start with the script'}):\n{heard}")
    return ok


import os
if not full_check(out):
    sys.exit(1)
