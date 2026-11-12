"""Upgrade real job photos with Google Gemini (Nano Banana), without faking anything.
Usage: python3 enhance_photos.py [photo paths relative to repo root...]   (default: every photo used by a video config)

Gemini re-grades the photo (exposure, white balance, color, haze). We then keep ONLY its low-frequency
tone/color and put it on top of the ORIGINAL pixels' fine detail, so nothing can be added, removed or
un-blurred (privacy blurs on faces, house numbers and Wi-Fi names stay exactly as they were).
Output: video/enhanced/<same path>.jpg. The video tools use it automatically when it exists."""
import base64, glob, io, json, os, sys, time, urllib.request
import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
ROOT = os.path.abspath(HERE + '../..') + '/'
OUTDIR = ROOT + 'video/enhanced/'
MODEL = os.environ.get('NPH_IMAGE_MODEL', 'gemini-3.1-flash-image')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
PROMPT = ("Professionally color-correct and relight this real installation photo for a home-services company. "
          "Fix exposure, white balance, shadows and haze so it looks bright, clean and natural. "
          "Do NOT add, remove, move or redraw anything. Do not change any text, screens, faces or blurred areas. "
          "Keep the exact same framing and composition.")


def config_photos():
    out = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('photo', 'hook_photo') and isinstance(v, str): out.add(v)
                walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    for f in glob.glob(ROOT + 'video/**/*.json', recursive=True):
        try: walk(json.load(open(f)))
        except Exception: pass
    return sorted(out)


def gemini_regrade(img):
    small = img.copy(); small.thumbnail((1536, 1536))
    buf = io.BytesIO(); small.save(buf, 'JPEG', quality=92)
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}},
                                    {"text": PROMPT}]}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}}
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL, json.dumps(body).encode(), {'Content-Type': 'application/json'})
            r = json.load(urllib.request.urlopen(req, timeout=180))
            for p in r['candidates'][0]['content']['parts']:
                if 'inlineData' in p:
                    return Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB')
            raise RuntimeError('no image in response')
        except Exception as e:
            print('  retry', attempt + 1, e); time.sleep(4 * (attempt + 1))
    return None


def tone_transfer(orig, graded):
    """orig detail + graded low-frequency tone/color."""
    g = graded.resize(orig.size, Image.LANCZOS)
    r = max(4, orig.width // 60)
    lo_o = np.asarray(orig.filter(ImageFilter.GaussianBlur(r)), np.float32)
    lo_g = np.asarray(g.filter(ImageFilter.GaussianBlur(r)), np.float32)
    o = np.asarray(orig, np.float32)
    out = Image.fromarray(np.clip(o + (lo_g - lo_o), 0, 255).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=3))


def main():
    paths = sys.argv[1:] or config_photos()
    for p in paths:
        dst = OUTDIR + p
        if os.path.exists(dst): continue
        orig = ImageOps.exif_transpose(Image.open(ROOT + p)).convert('RGB')
        print('enhancing', p)
        g = gemini_regrade(orig)
        if g is None: print('  FAILED, keeping original'); continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        tone_transfer(orig, g).save(dst, 'JPEG', quality=92)


if __name__ == '__main__':
    main()
