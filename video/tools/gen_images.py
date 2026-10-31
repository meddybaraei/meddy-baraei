"""Generate illustration images with Google Gemini (Nano Banana) for text-only social posts.
Usage: python3 gen_images.py SPEC.json OUTDIR   (SPEC: list of {"slug", "img": prompt}; skips existing files)
Each image gets a small 'AI-generated illustration' tag so viewers know it isn't a real job photo."""
import base64, io, json, os, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

MODEL = os.environ.get('NPH_IMAGE_MODEL', 'gemini-3.1-flash-image')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
RULES = (" Vertical 9:16 photo. No text, no words, no logos, no brand names, no readable house numbers or license plates."
         " Leave the lower third fairly simple so captions can sit on top.")
spec, out = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(out, exist_ok=True)
tagf = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 30)

for p in spec:
    if 'img' not in p: continue
    dst = f"{out}/{p['slug']}.jpg"
    if os.path.exists(dst): continue
    body = {"contents": [{"parts": [{"text": p['img'] + RULES}]}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": {"aspectRatio": "9:16"}}}
    im = None
    for a in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), {'Content-Type': 'application/json'}), timeout=180))
            im = next(Image.open(io.BytesIO(base64.b64decode(x['inlineData']['data']))) for x in r['candidates'][0]['content']['parts'] if 'inlineData' in x).convert('RGB')
            break
        except Exception as e:
            print('retry', p['slug'], e); time.sleep(5 * (a + 1))
    if im is None: print('FAILED', p['slug']); continue
    im = im.resize((1080, 1920), Image.LANCZOS)
    d = ImageDraw.Draw(im, 'RGBA'); t = 'AI-generated illustration'
    w = d.textlength(t, font=tagf); x, y = 1080 - 110 - w, 150
    d.rounded_rectangle((x - 16, y - 8, x + w + 16, y + 44), 22, fill=(0, 0, 0, 140)); d.text((x, y), t, font=tagf, fill=(255, 255, 255))
    im.save(dst, quality=92); print('ok', p['slug'])
