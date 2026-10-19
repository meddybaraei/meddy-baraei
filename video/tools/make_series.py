"""Photo-led video (vertical Short or 16:9) from a JSON config, with royalty-free music.
Usage: python3 make_series.py CONFIG.json OUT.mp4 [v|h]
CONFIG: {"badge": "Smart Home Starter Series · 1/10",
         "scenes": [{"photo": "facebook-post/x.jpg", "crop": [l, t, r, b] (fractions, optional),
                     "focus": [x, y] (optional), "kicker": "...", "title": "...", "body": "...", "dur": 4.0},
                    {"art": "thermostat|lock|list|why", "kicker": "...", "title": "...", "body": "...",
                     "items": [...] (for list), "dur": 4.0}],
         "end": ["Shop it & book your install", "novaprohome.com"]}
Writes OUT.mp4 and OUT_thumb.jpg (first scene)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
ROOT = os.path.abspath(HERE + '../..') + '/'
CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]
ORIENT = sys.argv[3] if len(sys.argv) > 3 else 'v'
W, H = (1080, 1920) if ORIENT == 'v' else (1920, 1080)
FPS = 30
NAVY = (19, 33, 56); NAVY2 = (28, 46, 76); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
SOFT = (200, 212, 228); GREEN = (76, 199, 154); YEL = (244, 161, 29); GREY = (120, 132, 150)
# Theme: "navy" (default, Starter Series / jobs) or "warm" (Installer's Review series: cream, white panels, orange).
WARM = CFG.get('theme') == 'warm'
if WARM:
    BG, PANEL, CARD2, ACC, TXT, SUB = (246, 241, 233), (255, 255, 255), (255, 255, 255), (232, 93, 4), (28, 28, 30), (88, 88, 96)
else:
    BG, PANEL, CARD2, ACC, TXT, SUB = NAVY, NAVY, NAVY2, BLUE, WHITE, SOFT
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)
CK = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
logo = Image.open(HERE + 'logo.png').convert('RGB')
V = ORIENT == 'v'

def logo_card(maxw):
    l = logo.copy(); l.thumbnail((maxw, maxw))
    c = Image.new('RGB', (l.width + 36, l.height + 20), WHITE); c.paste(l, (18, 10))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + c.size, 16, fill=255)
    return c, m
SMALL = logo_card(260 if V else 240)

def wrap(d, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def ctr(d, y, t, font, fill, cx=None):
    cx = W / 2 if cx is None else cx
    w = d.textlength(t, font=font); d.text((cx - w / 2, y), t, font=font, fill=fill)

def top(im):
    d = ImageDraw.Draw(im, 'RGBA')
    c, m = SMALL; im.paste(c, (50, 50), m)
    b = CFG.get('badge')
    if b:
        f = fs(34 if V else 30); w = d.textlength(b, font=f)
        x = W - 50 - w - 44 if not V else 50; y = 50 + c.height + 24 if V else 64
        d.rounded_rectangle((x, y, x + w + 44, y + 64), 32, fill=ACC + (240,))
        d.text((x + 22, y + 13), b, font=f, fill=WHITE)
    return d

def panel(d, s):
    """Text panel: kicker / title / body."""
    if V:
        tl = wrap(d, s.get('title', ''), fb(74), W - 180)
        bl = wrap(d, s.get('body', ''), fs(46), W - 180) if s.get('body') else []
        h = 70 + (56 if s.get('kicker') else 0) + 88 * len(tl) + (20 + 60 * len(bl) if bl else 0)
        y0 = H - 260 - h
        d.rounded_rectangle((50, y0, W - 50, H - 260), 34, fill=PANEL + (238,))
        if WARM: d.rounded_rectangle((50, y0, 64, H - 260), 7, fill=ACC)
        y = y0 + 36
        if s.get('kicker'): d.text((90, y), s['kicker'], font=fs(40), fill=ACC); y += 56
        for ln in tl: d.text((90, y), ln, font=fb(74), fill=TXT); y += 88
        y += 20
        for ln in bl: d.text((90, y), ln, font=fs(46), fill=SUB); y += 60
    else:
        tl = wrap(d, s.get('title', ''), fb(66), 1060)
        bl = wrap(d, s.get('body', ''), fs(40), 1060) if s.get('body') else []
        h = 60 + (52 if s.get('kicker') else 0) + 80 * len(tl) + (16 + 54 * len(bl) if bl else 0)
        y0 = H - 70 - h
        d.rounded_rectangle((70, y0, 1210, H - 70), 30, fill=PANEL + (238,))
        if WARM: d.rounded_rectangle((70, y0, 84, H - 70), 7, fill=ACC)
        y = y0 + 30
        if s.get('kicker'): d.text((110, y), s['kicker'], font=fs(36), fill=ACC); y += 52
        for ln in tl: d.text((110, y), ln, font=fb(66), fill=TXT); y += 80
        y += 16
        for ln in bl: d.text((110, y), ln, font=fs(40), fill=SUB); y += 54

def photo_scene(s):
    src = ImageOps.exif_transpose(Image.open(ROOT + s['photo'])).convert('RGB')
    if s.get('crop'):
        l, t, r, b = s['crop']; src = src.crop((int(l * src.width), int(t * src.height), int(r * src.width), int(b * src.height)))
    base = ImageOps.fit(src, (int(W * 1.1), int(H * 1.1)), Image.LANCZOS, centering=tuple(s.get('focus', (0.5, 0.5))))
    def f(t):
        z = 1.1 - 0.08 * t
        cw, ch = int(base.width / 1.1 * z), int(base.height / 1.1 * z)
        x, y = (base.width - cw) // 2, (base.height - ch) // 2
        im = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)
        d = top(im); panel(d, s); return im
    return f

def draw_art(d, kind, cx, cy, r):
    """Simple drawn product art (no brand logos)."""
    if kind == 'thermostat':
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(205, 212, 222))
        d.ellipse((cx - r * .9, cy - r * .9, cx + r * .9, cy + r * .9), fill=(14, 16, 22))
        ctr(d, cy - r * .42, '70', fb(int(r * .62)), WHITE, cx)
        ctr(d, cy + r * .3, 'HEAT SET', fs(int(r * .12)), (244, 120, 60), cx)
        d.arc((cx - r * .75, cy - r * .75, cx + r * .75, cy + r * .75), 130, 300, fill=(244, 120, 60), width=int(r * .05))
    elif kind == 'lock':
        w, h = r * .9, r * 1.7
        d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(r * .18), fill=(40, 44, 52), outline=(150, 156, 168), width=6)
        for i in range(4):
            for j in range(3):
                x = cx - w * .3 + j * w * .3; y = cy - h * .3 + i * h * .16
                d.ellipse((x - r * .09, y - r * .09, x + r * .09, y + r * .09), fill=(90, 96, 108))
                ctr(d, y - r * .07, str(i * 3 + j + 1) if i < 3 else '*0#'[j], fs(int(r * .11)), WHITE, x)
        d.rounded_rectangle((cx - r * .08, cy + h * .33, cx + r * .08, cy + h * .45), 6, fill=GREEN)
    elif kind == 'why':
        # house outline with smart icons
        d.polygon([(cx - r, cy - r * .1), (cx, cy - r), (cx + r, cy - r * .1)], fill=BLUE)
        d.rectangle((cx - r * .8, cy - r * .1, cx + r * .8, cy + r * .85), fill=NAVY2)
        d.rectangle((cx - r * .18, cy + r * .35, cx + r * .18, cy + r * .85), fill=(14, 22, 38))
        for (x, y, c) in ((-.5, .2, YEL), (.5, .2, GREEN), (0, .05, BLUE)):
            d.ellipse((cx + x * r - r * .12, cy + y * r - r * .12, cx + x * r + r * .12, cy + y * r + r * .12), fill=c)

def card_scene(s):
    im = Image.new('RGB', (W, H), BG); d = top(im)
    if s['art'] == 'chapter':
        cx = W / 2; y = (720 if V else 300)
        if s.get('num'):
            d.ellipse((cx - 70, y - 70, cx + 70, y + 70), fill=ACC); ctr(d, y - 38, str(s['num']), fb(72), WHITE, cx); y += 130
        for ln in wrap(d, s.get('title', ''), fb(84), W - 260): ctr(d, y, ln, fb(84), TXT, cx); y += 104
        if s.get('body'):
            y += 20
            for ln in wrap(d, s['body'], fs(44), W - 300): ctr(d, y, ln, fs(44), SUB, cx); y += 60
        return lambda t: im
    if s['art'] == 'qr':
        import qrcode
        q = qrcode.make(s['url'], border=2).convert('RGB').resize((560, 560) if V else (480, 480), Image.NEAREST)
        cx = W / 2 if V else 1440; y = 380 if V else 200
        if not V: cx_t, y_t = 140, 300
        if V:
            for ln in wrap(d, s.get('title', ''), fb(76), W - 200): ctr(d, y, ln, fb(76), TXT, cx); y += 94
            y += 30
        d.rounded_rectangle((cx - q.width / 2 - 24, y - 24, cx + q.width / 2 + 24, y + q.height + 24), 28, fill=WHITE)
        im.paste(q, (int(cx - q.width / 2), int(y)))
        if V:
            y += q.height + 70
            for ln in wrap(d, s.get('body', ''), fs(46), W - 220): ctr(d, y, ln, fs(46), SUB, cx); y += 62
            y += 20
            for ln in wrap(d, s.get('note', ''), fs(32), W - 220): ctr(d, y, ln, fs(32), SUB, cx); y += 44
        else:
            for ln in wrap(d, s.get('title', ''), fb(72), 900): d.text((cx_t, y_t), ln, font=fb(72), fill=TXT); y_t += 90
            y_t += 20
            for ln in wrap(d, s.get('body', ''), fs(44), 900): d.text((cx_t, y_t), ln, font=fs(44), fill=SUB); y_t += 60
            y_t += 20
            for ln in wrap(d, s.get('note', ''), fs(30), 900): d.text((cx_t, y_t), ln, font=fs(30), fill=SUB); y_t += 42
        return lambda t: im
    if s['art'] == 'list':
        y = 520 if V else 220
        d.text((80 if V else 140, y - 10), s.get('title', ''), font=fb(72 if V else 70), fill=TXT)
        y += 120 if V else 110
        for i, t in enumerate(s['items']):
            x = 80 if V else 140 + (i // 3) * 860; yy = y + (i if V else i % 3) * (150 if V else 150)
            d.rounded_rectangle((x, yy, x + (W - 160 if V else 800), yy + 120), 24, fill=CARD2, outline=(226, 218, 206) if WARM else None, width=2)
            d.ellipse((x + 24, yy + 22, x + 100, yy + 98), fill=ACC)
            ctr(d, yy + 32, str(i + 1), fb(44), WHITE, x + 62)
            d.text((x + 130, yy + 32), t, font=fs(48 if V else 46), fill=TXT)
        if s.get('body'):
            yy = y + (len(s['items']) if V else 3) * 150 + 30
            for ln in wrap(d, s['body'], fs(44), W - 200): ctr(d, yy, ln, fs(44), SUB); yy += 58
        return lambda t: im
    if V: draw_art(d, s['art'], W / 2, 760, 300)
    else: draw_art(d, s['art'], 1480, 520, 300)
    if s.get('note'):
        f = fm(30); x, y = (W / 2, 1110) if V else (1480, 880); ctr(d, y, s['note'], f, GREY, x)
    if V: panel(d, s)
    else:
        y = 300
        if s.get('kicker'): d.text((140, y), s['kicker'], font=fs(40), fill=ACC); y += 70
        for ln in wrap(d, s.get('title', ''), fb(72), 1000): d.text((140, y), ln, font=fb(72), fill=TXT); y += 90
        y += 20
        for ln in wrap(d, s.get('body', ''), fs(44), 1000): d.text((140, y), ln, font=fs(44), fill=SUB); y += 60
    return lambda t: im

def product_scene(s):
    """Official product photo on a card (for small screenshots that can't fill the frame)."""
    src = Image.open(ROOT + s['product']).convert('RGB')
    bg = src.getpixel((2, 2))
    if V: box = (90, 330, W - 90, 1180)
    else: box = (1260, 140, 1860, 940)
    bw, bh = box[2] - box[0], box[3] - box[1]
    im0 = src.copy(); sc = min((bw - 80) / im0.width, (bh - 80) / im0.height); im0 = im0.resize((int(im0.width * sc), int(im0.height * sc)), Image.LANCZOS)
    def f(t):
        im = Image.new('RGB', (W, H), BG); d = top(im)
        if WARM: d.rounded_rectangle((box[0] + 10, box[1] + 14, box[2] + 10, box[3] + 14), 36, fill=(225, 216, 202))
        d.rounded_rectangle(box, 36, fill=bg)
        z = 0.96 + 0.04 * t; pi = im0.resize((int(im0.width * z), int(im0.height * z)), Image.BILINEAR)
        im.paste(pi, (box[0] + (bw - pi.width) // 2, box[1] + (bh - pi.height) // 2))
        if s.get('note'): ctr(d, box[3] + 14, s['note'], fm(26), GREY, (box[0] + box[2]) / 2)
        if V: panel(d, s)
        else:
            y = 300
            if s.get('kicker'): d.text((140, y), s['kicker'], font=fs(40), fill=ACC); y += 70
            for ln in wrap(d, s.get('title', ''), fb(72), 1000): d.text((140, y), ln, font=fb(72), fill=TXT); y += 90
            y += 20
            for ln in wrap(d, s.get('body', ''), fs(44), 1000): d.text((140, y), ln, font=fs(44), fill=SUB); y += 60
        return im
    return f

def end_card():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    c, m = logo_card(620 if V else 560); y0 = 420 if V else 110
    im.paste(c, ((W - c.width) // 2, y0), m); y = y0 + c.height + 70
    a, b = CFG.get('end', ['Shop it & book your install', 'novaprohome.com'])
    ctr(d, y, a, fb(60), TXT); y += 90
    ctr(d, y, b, fb(84), ACC); y += 120
    ctr(d, y, 'Meddy@novaprohome.com', fb(64), TXT); y += 110
    ctr(d, y, 'Ring Authorized Dealer · Google Nest Pro', fs(40), SUB); y += 90
    sub = CFG.get('subscribe', 'LIKE & SUBSCRIBE')
    if sub:
        f = fb(52); w = d.textlength(sub, font=f); x0 = (W - w) / 2 - 40
        d.rounded_rectangle((x0, y - 14, x0 + w + 80, y + 76), 44, fill=(220, 38, 38)); ctr(d, y, sub, f, WHITE); y += 100
        ctr(d, y, 'for more smart home tips', fs(40), TXT)
    return lambda t: im

scenes = [(s.get('dur', 4.0), photo_scene(s) if 'photo' in s else product_scene(s) if 'product' in s else card_scene(s)) for s in CFG['scenes']]
if CFG.get('shop_qr', True):  # QR to the website shop (affiliate products) before the end card
    scenes.append((4.0, card_scene({'art': 'qr', 'url': 'https://novaprohome.com/shop?utm_source=qr&utm_medium=video',
                                     'title': 'Shop the products we install', 'body': 'Scan or visit novaprohome.com/shop',
                                     'note': 'Some shop links are affiliate links: NovaProHome may earn a commission.'})))
scenes.append((3.5, end_card()))
total = sum(d for d, _ in scenes)
scenes[0][1](0.0).save(OUT.rsplit('.', 1)[0] + '_thumb.jpg', quality=90)
silent = OUT + '.silent.mp4'
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '21', silent], stdin=subprocess.PIPE)
prev = None
for dur, fn in scenes:
    n = int(dur * FPS)
    for k in range(n):
        fr = np.asarray(fn(k / max(1, n - 1)), dtype=np.float32)
        if prev is not None and k < 0.35 * FPS:
            al = k / (0.35 * FPS); fr = fr * al + prev * (1 - al)
        ff.stdin.write(fr.astype(np.uint8).tobytes())
    prev = np.asarray(fn(1.0), dtype=np.float32)
ff.stdin.close(); ff.wait()
music = OUT + '.music.wav'
subprocess.run([sys.executable, HERE + 'make_music.py', music, str(total + 1), CFG.get('music', 'calm')], check=True, stdout=subprocess.DEVNULL)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', music, '-filter_complex',
                f'[1:a]volume=0.55,afade=t=out:st={total - 1.5}:d=1.5[a]', '-map', '0:v', '-map', '[a]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUT], check=True)
os.remove(silent); os.remove(music)
print(OUT, round(total, 1))
