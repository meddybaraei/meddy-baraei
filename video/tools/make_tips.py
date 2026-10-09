"""Text-led tip video (16:9 + vertical Short) with drawn icons and royalty-free music.
Usage: python3 make_tips.py CONFIG.json OUT_PREFIX
CONFIG: {"title": [...lines], "sub": "...", "safety": [...lines] | null,
         "steps": [{"title": "...", "body": "...", "icon": "app|battery|wifi|router|reset|phone|check"}],
         "outro": ["line1", "line2"]}
Writes OUT_PREFIX.mp4 (1920x1080), OUT_PREFIX_short.mp4 (1080x1920) and OUT_PREFIX_thumb.jpg."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]
NAVY = (19, 33, 56); NAVY2 = (28, 46, 76); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
SOFT = (200, 212, 228); GREEN = (76, 199, 154); YEL = (244, 161, 29); RED = (226, 84, 64)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)
logo = Image.open(HERE + 'logo.png').convert('RGB')
FPS = 30

def logo_card(maxw):
    l = logo.copy(); l.thumbnail((maxw, maxw))
    c = Image.new('RGB', (l.width + 36, l.height + 20), WHITE); c.paste(l, (18, 10))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + c.size, 16, fill=255)
    return c, m

def wrap(d, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def ctr(d, y, t, font, fill, cx):
    w = d.textlength(t, font=font); d.text((cx - w / 2, y), t, font=font, fill=fill)

def icon(kind, size):
    """Simple drawn icon on a rounded panel (no brand logos)."""
    im = Image.new('RGB', (size, size), NAVY2); d = ImageDraw.Draw(im)
    s = size / 860.0; S = lambda *v: [int(x * s) for x in v]
    if kind == 'app':
        d.rounded_rectangle(S(290, 90, 570, 700), int(40 * s), fill=(20, 20, 24))
        d.rounded_rectangle(S(308, 140, 552, 650), int(20 * s), fill=(235, 240, 246))
        ctr(d, 170 * s, 'Device Health', fs(int(28 * s)), NAVY, size / 2)
        for i, (t, c) in enumerate((('Network', BLUE), ('Reconnect', GREEN), ('Reboot', YEL))):
            d.rounded_rectangle(S(328, 240 + i * 110, 532, 320 + i * 110), int(14 * s), fill=c)
            ctr(d, (258 + i * 110) * s, t, fb(int(30 * s)), WHITE, size / 2)
    elif kind == 'battery':
        d.rounded_rectangle(S(230, 250, 590, 470), int(30 * s), outline=WHITE, width=int(14 * s))
        d.rectangle(S(590, 320, 630, 400), fill=WHITE)
        d.rounded_rectangle(S(255, 275, 345, 445), int(14 * s), fill=RED)
        d.polygon(S(420, 270, 360, 380, 410, 380, 380, 460, 470, 330, 415, 330, 450, 270), fill=YEL)
        ctr(d, 560 * s, 'Charge it fully', fb(int(44 * s)), WHITE, size / 2)
        ctr(d, 625 * s, 'or check the wiring & transformer', fm(int(32 * s)), SOFT, size / 2)
    elif kind == 'wifi':
        cx, cy = size / 2, 520 * s
        for i, r in enumerate((340, 240, 140)):
            d.arc((cx - r * s, cy - r * s, cx + r * s, cy + r * s), 225, 315, fill=GREEN if i else YEL, width=int(36 * s))
        d.ellipse((cx - 38 * s, cy - 38 * s, cx + 38 * s, cy + 38 * s), fill=GREEN)
        ctr(d, 640 * s, 'Signal strength matters', fb(int(44 * s)), WHITE, size / 2)
    elif kind == 'router':
        d.rounded_rectangle(S(200, 330, 660, 470), int(26 * s), fill=(60, 72, 96))
        for x in (260, 320, 380):
            d.ellipse(S(x, 385, x + 30, 415), fill=GREEN)
        for x in (300, 560):
            d.line(S(x, 330, x - 40, 180), fill=WHITE, width=int(14 * s))
        d.arc(S(460, 140, 640, 320), 200, 340, fill=YEL, width=int(16 * s))
        d.polygon(S(625, 205, 655, 245, 600, 250), fill=YEL)
        ctr(d, 560 * s, 'Unplug 30 sec, plug back in', fb(int(42 * s)), WHITE, size / 2)
    elif kind == 'reset':
        d.ellipse(S(280, 170, 580, 470), outline=WHITE, width=int(14 * s))
        d.ellipse(S(380, 270, 480, 370), fill=BLUE)
        ctr(d, 540 * s, 'Hold the setup button', fb(int(44 * s)), WHITE, size / 2)
        ctr(d, 605 * s, 'then Set Up a Device in the app', fm(int(32 * s)), SOFT, size / 2)
    elif kind == 'check':
        d.ellipse(S(270, 140, 590, 460), fill=GREEN)
        d.line(S(350, 300, 410, 370, 520, 230), fill=WHITE, width=int(36 * s), joint='curve')
        ctr(d, 540 * s, 'Back online', fb(int(48 * s)), WHITE, size / 2)
    else:
        ctr(d, 380 * s, '?', fb(int(220 * s)), WHITE, size / 2)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size, size), int(36 * s), fill=255)
    return im, m

def wide_frames():
    W, H = 1920, 1080; frames = []
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(420); im.paste(c, ((W - c.width) // 2, 150), m)
    y = 430
    for t in CFG['title']: ctr(d, y, t, fb(96), WHITE, W / 2); y += 112
    ctr(d, y + 30, CFG['sub'], fs(44), BLUE, W / 2)
    frames.append((4.5, im))
    if CFG.get('safety'):
        im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
        ctr(d, 300, 'Before you start', fb(80), YEL, W / 2)
        y = 450
        for t in CFG['safety']: ctr(d, y, t, fm(44), SOFT, W / 2); y += 70
        frames.append((5.0, im))
    n = len(CFG['steps'])
    for i, st in enumerate(CFG['steps'], 1):
        im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
        c, m = logo_card(240); im.paste(c, (80, 60), m)
        d.text((80, 230), f'FIX {i} OF {n}', font=fs(34), fill=BLUE)
        y = 290
        for ln in wrap(d, st['title'], fb(70), 820): d.text((80, y), ln, font=fb(70), fill=WHITE); y += 86
        y += 24
        for ln in wrap(d, st['body'], fm(40), 820): d.text((80, y), ln, font=fm(40), fill=SOFT); y += 56
        d.rounded_rectangle((80, 990, 900, 1004), 7, fill=NAVY2)
        d.rounded_rectangle((80, 990, 80 + int(820 * i / n), 1004), 7, fill=BLUE)
        ic, icm = icon(st['icon'], 860); im.paste(ic, (W - 940, 110), icm)
        frames.append((7.0, im))
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(520); im.paste(c, ((W - c.width) // 2, 120), m)
    ctr(d, 400, CFG['outro'][0], fb(84), WHITE, W / 2)
    ctr(d, 510, CFG['outro'][1], fb(84), BLUE, W / 2)
    ctr(d, 680, 'novaprohome.com   •   (571) 241-9569', fb(60), WHITE, W / 2)
    ctr(d, 790, 'Ring Authorized Dealer · Google Nest Pro · Northern Virginia', fs(40), SOFT, W / 2)
    frames.append((6.0, im))
    return (W, H), frames

def tall_frames():
    W, H = 1080, 1920; frames = []
    def head(d, im):
        c, m = logo_card(280); im.paste(c, (60, 70), m)
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im); head(d, im)
    y = 620
    for t in CFG['title']:
        for ln in wrap(d, t, fb(92), W - 120): ctr(d, y, ln, fb(92), WHITE, W / 2); y += 110
    ctr(d, y + 40, CFG['sub'], fs(46), BLUE, W / 2)
    frames.append((3.0, im))
    n = len(CFG['steps'])
    for i, st in enumerate(CFG['steps'], 1):
        im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im); head(d, im)
        d.text((60, 280), f'FIX {i} OF {n}', font=fs(40), fill=BLUE)
        y = 340
        for ln in wrap(d, st['title'], fb(72), W - 120): d.text((60, y), ln, font=fb(72), fill=WHITE); y += 88
        ic, icm = icon(st['icon'], 860); im.paste(ic, ((W - 860) // 2, 640), icm)
        y = 1540
        for ln in wrap(d, st['body'], fm(42), W - 120): ctr(d, y, ln, fm(42), SOFT, W / 2); y += 58
        frames.append((5.0, im))
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(640); im.paste(c, ((W - c.width) // 2, 460), m)
    ctr(d, 800, CFG['outro'][0], fb(64), WHITE, W / 2)
    ctr(d, 885, CFG['outro'][1], fs(54), BLUE, W / 2)
    ctr(d, 1040, 'novaprohome.com', fb(84), WHITE, W / 2)
    ctr(d, 1150, '(571) 241-9569', fb(72), WHITE, W / 2)
    frames.append((3.5, im))
    return (W, H), frames

def render(size, frames, out):
    W, H = size; total = sum(f[0] for f in frames)
    silent = out + '.silent.mp4'; music = out + '.music.wav'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20', silent], stdin=subprocess.PIPE)
    prev = None
    for dur, img in frames:
        cur = np.asarray(img, dtype=np.float32); n = int(dur * FPS)
        for k in range(n):
            fr = cur if prev is None or k >= 0.4 * FPS else cur * (k / (0.4 * FPS)) + prev * (1 - k / (0.4 * FPS))
            ff.stdin.write(fr.astype(np.uint8).tobytes())
        prev = cur
    ff.stdin.close(); ff.wait()
    subprocess.run([sys.executable, HERE + 'make_music.py', music, str(total + 1)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', music, '-filter_complex', '[1:a]volume=0.55[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(silent); os.remove(music)
    return total

sz, fr = wide_frames(); fr[0][1].save(OUT + '_thumb.jpg', quality=90)
print('wide', render(sz, fr, OUT + '.mp4'))
sz, fr = tall_frames(); print('short', render(sz, fr, OUT + '_short.mp4'))
