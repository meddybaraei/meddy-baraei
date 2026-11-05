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
