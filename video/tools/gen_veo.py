"""Generate a labeled AI b-roll clip with Veo (Gemini API; key injected by the proxy).
Usage: python3 gen_veo.py OUT.mp4 "prompt" [9:16|16:9] [model]
Cost: veo-3.1-fast ~$0.12-0.15/s (8 s clip ~$1-1.20). Log every run in video/GEMINI_SPEND.md."""
import json, sys, time, urllib.request, urllib.error
API = 'https://generativelanguage.googleapis.com/v1beta'
out, prompt = sys.argv[1], sys.argv[2]
ar = sys.argv[3] if len(sys.argv) > 3 else '9:16'
model = sys.argv[4] if len(sys.argv) > 4 else 'veo-3.1-fast-generate-preview'
def call(url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None, {'Content-Type': 'application/json'})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'HTTP {e.code}: {e.read()[:600]}')
op = call(f'{API}/models/{model}:predictLongRunning', {'instances': [{'prompt': prompt}],
          'parameters': {'aspectRatio': ar, 'durationSeconds': 8, 'resolution': '1080p'}})
name = op['name']; print('op', name, flush=True)
while True:
    time.sleep(15)
    st = call(f'{API}/{name}')
    if st.get('done'):
        break
if 'error' in st:
    raise SystemExit(f"Veo error: {st['error']}")
samples = st['response']['generateVideoResponse']['generatedSamples']
uri = samples[0]['video']['uri']
with urllib.request.urlopen(urllib.request.Request(uri), timeout=300) as r, open(out, 'wb') as f:
    f.write(r.read())
print('saved', out)
