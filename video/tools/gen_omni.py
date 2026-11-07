"""Generate a labeled AI video clip with Gemini Omni 1.2 Flash (Veo is no longer listed on our key).
Background-mode Interactions API, because a single long request times out at the proxy (HTTP 502).
Usage: python3 gen_omni.py OUT.mp4 "prompt (say 8-second, 9:16 or 16:9, photorealistic, no text/logos)"
Output so far: 720x1280, 8 s, with audio. Cost: about 46k video output tokens per clip; log each run in video/GEMINI_SPEND.md."""
import base64, json, sys, time, urllib.request, urllib.error
API = 'https://generativelanguage.googleapis.com/v1beta/interactions'
out, prompt = sys.argv[1], sys.argv[2]
def call(url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None, {'Content-Type': 'application/json'})
    for a in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (502, 503) and a < 3: time.sleep(10); continue
            raise SystemExit(f'HTTP {e.code}: {e.read()[:600]}')
r = call(API, {'model': 'gemini-omni-1.2-flash', 'background': True, 'response_modalities': ['video'], 'input': prompt})
iid = r['id']; print('started', iid, flush=True)
for _ in range(80):
    time.sleep(15)
    r = call(f'{API}/{iid}')
    if r.get('status') != 'in_progress':
        break
if r.get('status') != 'completed':
    raise SystemExit(f"status {r.get('status')}: {json.dumps(r)[:600]}")
for step in r.get('steps', []):
    for c in step.get('content', []) if step.get('type') == 'model_output' else []:
        if c.get('type') == 'video':
            open(out, 'wb').write(base64.b64decode(c['data'])); print('saved', out, r.get('usage', {}).get('total_output_tokens'), 'output tokens'); sys.exit(0)
raise SystemExit('no video in response')
