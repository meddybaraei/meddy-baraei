"""Gen Z-style TikTok cut (1080x1920): hook text, beat-synced punch-zoom cuts, bold captions, phonk beat.
Usage: python3 make_tiktok.py CONFIG.json OUT.mp4
CONFIG: {"hook": "POV: ...", "hook_photo": "path.jpg",
         "clips": [{"photo": "path.jpg", "focus": [x, y], "text": "Caption", "hl": "word to highlight"}],
         "cta": ["Book your install", "novaprohome.com/contact", "link in bio"],
         "bpm": 140, "beats_per_clip": 4}
Writes OUT.mp4 and OUT_thumb.jpg (hook frame)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
ROOT = os.path.abspath(HERE + '../..') + '/'
CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
BEAT = 60 / CFG.get('bpm', 140); BPC = CFG.get('beats_per_clip', 4)
F = '/usr/share/fonts/opentype/inter/'
BLACK = lambda s: ImageFont.truetype(F + 'Inter-Black.otf', s)
YEL, WHITE, INK = (255, 225, 26), (255, 255, 255), (12, 12, 14)

def load(path, focus=(0.5, 0.5)):
    src = ImageOps.exif_transpose(Image.open(ROOT + path)).convert('RGB')
    return ImageOps.fit(src, (int(W * 1.18), int(H * 1.18)), Image.LANCZOS, centering=tuple(focus))

def zoom(base, z):
    cw, ch = int(base.width / 1.18 * z), int(base.height / 1.18 * z)
    cw, ch = min(cw, base.width), min(ch, base.height)
    x, y = (base.width - cw) // 2, (base.height - ch) // 2
    return base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)

def wrap(d, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def caption(im, text, hl='', size=92, cy=0.66, pop=1.0, box=False):
    """Centered bold caption with black stroke; words in `hl` drawn yellow."""
    d = ImageDraw.Draw(im)
    size = int(size * pop); f = BLACK(size); hlw = set(hl.lower().split())
    lines = wrap(d, text.upper(), f, W - 140)
    lh = int(size * 1.12); y = int(H * cy) - lh * len(lines) // 2
    if box:
        d.rounded_rectangle((50, y - 30, W - 50, y + lh * len(lines) + 20), 36, fill=(0, 0, 0, 170))
    for ln in lines:
        words = ln.split(); total = d.textlength(ln, font=f); x = (W - total) / 2
        for i, w in enumerate(words):
            col = YEL if w.strip('.,!?:').lower() in hlw else WHITE
            d.text((x, y), w, font=f, fill=col, stroke_width=max(6, size // 11), stroke_fill=INK)
            x += d.textlength(w + ' ', font=f)
        y += lh

def ease_pop(t):  # 0..1 over first 0.12 s -> scale 1.25 -> 1.0
    return 1.0 + 0.25 * max(0.0, 1 - t / 0.12)

frames = []  # list of (duration_s, fn(t_local)->Image)
hook_base = load(CFG.get('hook_photo', CFG['clips'][0]['photo']), CFG['clips'][0].get('focus', (0.5, 0.5)))
def hook_fn(t):
    im = zoom(hook_base, 1.0 + 0.04 * t)
    dark = Image.new('RGB', (W, H), (0, 0, 0)); im = Image.blend(im, dark, 0.35)
    caption(im, CFG['hook'], CFG.get('hook_hl', ''), size=104, cy=0.42, pop=ease_pop(t))
    return im
frames.append((BEAT * 2, hook_fn))
for c in CFG['clips']:
    base = load(c['photo'], c.get('focus', (0.5, 0.5)))
    def fn(t, base=base, c=c):
        z = 1.0 + 0.16 * max(0.0, 1 - t / 0.18) + 0.05 * t  # punch-in on the cut, slow push after
        im = zoom(base, z)
        if t < 0.05: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.55)  # flash on cut
        # shake on each beat
        bt = (t % BEAT)
        if bt < 0.06:
            dx = int(10 * np.sin(t * 90)); im = ImageOps.expand(im, border=12, fill=0).crop((12 + dx, 12, 12 + dx + W, 12 + H))
        if c.get('text'): caption(im, c['text'], c.get('hl', ''), pop=ease_pop(t))
        return im
    frames.append((BEAT * BPC, fn))
cta = CFG.get('cta', ['Book your install', 'novaprohome.com/contact', 'link in bio'])
logo = Image.open(HERE + 'logo.png').convert('RGBA'); logo.thumbnail((620, 620))
def cta_fn(t):
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    card = Image.new('RGB', (logo.width + 60, logo.height + 40), WHITE); card.paste(logo, (30, 20), logo)
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + card.size, 28, fill=255)
    im.paste(card, ((W - card.width) // 2, 430), m)
    caption(im, cta[0], cta[0], size=96, cy=0.50, pop=ease_pop(t))
    caption(im, cta[1], '', size=62, cy=0.60)
    caption(im, cta[2] + ' 👇'.replace(' 👇', ''), cta[2], size=70, cy=0.68)
    caption(im, '(571) 241-9569', '', size=58, cy=0.76)
    return im
frames.append((BEAT * 6, cta_fn))

total = sum(d for d, _ in frames)
hook_fn(0.5).save(OUT.rsplit('.', 1)[0] + '_thumb.jpg', quality=90)
silent = OUT + '.silent.mp4'
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20', silent], stdin=subprocess.PIPE)
for dur, fn in frames:
    n = int(round(dur * FPS))
    for k in range(n): ff.stdin.write(np.asarray(fn(k / FPS), dtype=np.uint8).tobytes())
ff.stdin.close(); ff.wait()
music = OUT + '.music.wav'
subprocess.run([sys.executable, HERE + 'make_music.py', music, str(total + 1), CFG.get('music', 'phonk')], check=True, stdout=subprocess.DEVNULL)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', music, '-filter_complex',
                f'[1:a]volume=0.8,afade=t=out:st={total - 1.2}:d=1.2[a]', '-map', '0:v', '-map', '[a]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], check=True)
os.remove(silent); os.remove(music)
print(OUT, round(total, 1))
