"""Reolink use-case carousel (1080x1350) in the NovaProHome navy card style."""
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)) + '/'
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
NAVY, NAVY2, BLUE, WHITE, SOFT, RED = (19, 33, 56), (28, 46, 76), (58, 155, 213), (255, 255, 255), (200, 212, 228), (220, 38, 38)
W, H = 1080, 1350
logo = Image.open(D + '../../tools/logo.png').convert('RGB'); logo.thumbnail((300, 300))

def wrap(d, t, f, mw):
    out, cur = [], ''
    for w in t.split():
        nxt = (cur + ' ' + w).strip()
        if d.textlength(nxt, font=f) <= mw: cur = nxt
        else: out.append(cur); cur = w
    return out + [cur] if cur else out

def base(n, total):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c = Image.new('RGB', (logo.width + 36, logo.height + 20), WHITE); c.paste(logo, (18, 10)); im.paste(c, (60, 60))
    d.text((W - 60, 80), f'{n}/{total}', font=fs(34), fill=SOFT, anchor='ra')
    return im, d

def ctr(d, y, t, f, c): d.text((W / 2, y), t, font=f, fill=c, anchor='ma')

SLIDES = [
    ('cover', 'Which Reolink camera fits your property?', 'Business or home: 6 setups we design and install across Northern Virginia', 'Swipe →'),
    (1, 'Shops, offices & restaurants', 'PoE cameras wired to an NVR recorder. 24/7 local recording on a hard drive, no required monthly fee.'),
    (2, 'Parking lots & warehouses', 'Dual-lens 180° panoramic cameras cover a wide area with fewer cameras.'),
    (3, 'Entrances & driveways', 'Auto-tracking cameras follow people and cars and zoom in on details like faces and plates.'),
    (4, 'Dark corners at night', 'Color night vision cameras show real colors in very low light, not just black and white.'),
    (5, 'No power or Wi-Fi?', '4G LTE cellular + solar cameras for construction sites, farms, barns and vacant properties.'),
    (6, 'Homes & rentals', 'Video doorbell, Wi-Fi and battery cameras with smart alerts for people, vehicles and pets.'),
    ('compat', 'Works with what you already use', ['Synology & QNAP NAS', 'Blue Iris', 'Milestone', 'Digital Watchdog', 'SecuritySpy (Mac)', 'iSpy · tinyCam · IP Cam Viewer'], 'Support varies by model. We check yours before we install.'),
    ('cta', 'Not sure which setup you need?', 'Free on-site assessment. We design, install and set up the app for you.'),
]

def render(slides, phone, out):
    n = len(slides)
    for i, s in enumerate(slides, 1):
        im, d = base(i, n)
        if s[0] == 'cover':
            y = 420
            for ln in wrap(d, s[1], fb(92), W - 160): ctr(d, y, ln, fb(92), WHITE); y += 110
            y += 30
            for ln in wrap(d, s[2], fs(46), W - 200): ctr(d, y, ln, fs(46), SOFT); y += 62
            d.rounded_rectangle((W / 2 - 150, 1130, W / 2 + 150, 1220), 45, fill=BLUE); ctr(d, 1150, s[3], fb(46), WHITE)
        elif s[0] == 'compat':
            y = 230
            for ln in wrap(d, s[1], fb(76), W - 160): ctr(d, y, ln, fb(76), WHITE); y += 92
            y += 40
            for t in s[2]:
                d.rounded_rectangle((110, y, W - 110, y + 100), 24, fill=NAVY2); d.ellipse((140, y + 30, 180, y + 70), fill=BLUE)
                d.text((210, y + 26), t, font=fs(44), fill=WHITE); y += 116
            y += 20
            for ln in wrap(d, s[3], fs(36), W - 200): ctr(d, y, ln, fs(36), SOFT); y += 48
        elif s[0] == 'cta':
            y = 330
            for ln in wrap(d, s[1], fb(84), W - 160): ctr(d, y, ln, fb(84), WHITE); y += 102
            y += 30
            for ln in wrap(d, s[2], fs(44), W - 200): ctr(d, y, ln, fs(44), SOFT); y += 60
            y += 60; ctr(d, y, 'novaprohome.com/contact', fb(64), BLUE); y += 100
            for ln in phone.split(' · '): ctr(d, y, ln, fb(54), WHITE); y += 72
            y += 30
            ctr(d, y, 'NovaProHome · Sterling, VA', fs(38), SOFT); y += 56
            ctr(d, y, 'Serving Loudoun & Fairfax County', fs(38), SOFT)
        else:
            d.ellipse((W / 2 - 80, 360, W / 2 + 80, 520), fill=BLUE); ctr(d, 392, str(s[0]), fb(90), WHITE)
            y = 600
            for ln in wrap(d, s[1], fb(84), W - 160): ctr(d, y, ln, fb(84), WHITE); y += 102
            y += 30
            for ln in wrap(d, s[2], fs(46), W - 200): ctr(d, y, ln, fs(46), SOFT); y += 64
        im.save(f'{out}/slide-{i:02d}.jpg', quality=92)

os.makedirs(D + 'carousel', exist_ok=True)
render(SLIDES, '(571) 241-9569 · Meddy@novaprohome.com', D + 'carousel')
