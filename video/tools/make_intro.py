"""Channel intro video for @NovaProHome (16:9). Usage: python3 make_intro.py OUT.mp4"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
P = os.path.abspath(HERE + '../../facebook-post') + '/'
OUT = sys.argv[1]
W, H, FPS = 1920, 1080, 30
NAVY = (19, 33, 56); NAVY2 = (28, 46, 76); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
SOFT = (200, 212, 228); GREEN = (76, 199, 154)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)
CK = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44)
logo = Image.open(HERE + 'logo.png').convert('RGB')

def logo_card(maxw):
    l = logo.copy(); l.thumbnail((maxw, maxw))
    c = Image.new('RGB', (l.width + 36, l.height + 20), WHITE); c.paste(l, (18, 10))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + c.size, 16, fill=255)
    return c, m

def ctr(d, y, t, font, fill, cx=W / 2):
    w = d.textlength(t, font=font); d.text((cx - w / 2, y), t, font=font, fill=fill)

def still(img):
    return lambda t: img

def zoom_photo(path, title, sub):
    src = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    base = ImageOps.fit(src, (int(W * 1.1), int(H * 1.1)), Image.LANCZOS)
    small = logo_card(250)
    def frame(t):
        z = 1.1 - 0.08 * t
        cw, ch = int(base.width / 1.1 * z), int(base.height / 1.1 * z)
        x, y = (base.width - cw) // 2, (base.height - ch) // 2
        im = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)
        d = ImageDraw.Draw(im, 'RGBA')
        d.rounded_rectangle((80, H - 290, 1180, H - 80), 28, fill=NAVY + (235,))
        d.text((120, H - 260), title, font=fb(68), fill=WHITE)
        d.text((120, H - 168), sub, font=fs(40), fill=BLUE)
        c, m = small; im.paste(c, (80, 70), m)
        return im
    return frame

def card(lines_big, lines_small=(), color=BLUE, logo_w=460):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(logo_w); im.paste(c, ((W - c.width) // 2, 110), m)
    y = 110 + c.height + 90
    for t in lines_big: ctr(d, y, t, fb(84), WHITE); y += 104
    y += 20
    for t in lines_small: ctr(d, y, t, fs(44), color); y += 62
    return im

def about():
    im = ImageOps.fit(Image.open(P + '04_installer_on_ladder.jpg').convert('RGB'), (W, H), Image.LANCZOS)
    im = Image.blend(im, Image.new('RGB', (W, H), NAVY), 0.7); d = ImageDraw.Draw(im)
    d.text((140, 150), 'Who we are', font=fs(40), fill=BLUE)
    d.text((140, 210), 'Locally owned in Sterling, VA', font=fb(80), fill=WHITE)
    for i, t in enumerate(['Founded by an Electrical Engineer',
                           'Ring Authorized Dealer',
                           'Google Nest Pro',
                           'Clean installs, full app setup, a walkthrough every time']):
        y = 380 + i * 100
        d.text((150, y), '✓', font=CK, fill=GREEN)
        d.text((220, y), t, font=fs(50), fill=WHITE)
    return im

def icon_card(title, sub, items):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(250); im.paste(c, (80, 70), m)
    d.text((140, 260), title, font=fb(80), fill=WHITE)
    d.text((140, 365), sub, font=fs(42), fill=BLUE)
    for i, t in enumerate(items):
        x = 140 + (i % 2) * 820; y = 500 + (i // 2) * 150
        d.rounded_rectangle((x, y, x + 760, y + 120), 22, fill=NAVY2)
        d.text((x + 40, y + 34), t, font=fs(46), fill=WHITE)
    return im

def steps():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    ctr(d, 140, 'How it works', fb(84), WHITE)
    for i, (t, s) in enumerate([('Send photos', 'of your door, wall or thermostat'),
                                ('Get a fixed quote', 'free, in writing, no surprises'),
                                ('We install & set up', 'then walk you through the app')]):
        x = 150 + i * 560
        d.rounded_rectangle((x, 330, x + 500, 800), 30, fill=NAVY2)
        d.ellipse((x + 190, 380, x + 310, 500), fill=BLUE)
        ctr(d, 398, str(i + 1), fb(72), WHITE, x + 250)
        ctr(d, 560, t, fb(46), WHITE, x + 250)
        ctr(d, 640, s.split(',')[0], fm(32), SOFT, x + 250)
        if ',' in s: ctr(d, 685, s.split(',', 1)[1].strip(), fm(32), SOFT, x + 250)
    ctr(d, 880, 'Serving Loudoun · Fairfax · Arlington · Prince William', fs(42), BLUE)
    return im

def website():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    ctr(d, 90, 'Book online in 2 minutes', fb(80), WHITE)
    d.rounded_rectangle((360, 230, 1560, 900), 26, fill=(236, 241, 247))
    d.rounded_rectangle((360, 230, 1560, 300), 26, fill=(205, 214, 226)); d.rectangle((360, 270, 1560, 300), fill=(205, 214, 226))
    for i, col in enumerate(((235, 98, 86), (244, 190, 79), (98, 197, 84))):
        d.ellipse((395 + i * 40, 252, 419 + i * 40, 276), fill=col)
    d.rounded_rectangle((540, 246, 1380, 284), 19, fill=WHITE)
    d.text((570, 250), 'novaprohome.com/contact', font=fm(28), fill=(60, 70, 90))
    c, m = logo_card(300); im.paste(c, (420, 340), m)
    d.text((420, 500), 'Get your free quote', font=fb(60), fill=NAVY)
    for i, lab in enumerate(('Name', 'Phone', 'What would you like installed?')):
        y = 600 + i * 80
        d.rounded_rectangle((420, y, 1180, y + 60), 12, fill=WHITE, outline=(190, 200, 214), width=2)
        d.text((440, y + 14), lab, font=fm(28), fill=(140, 150, 166))
    d.rounded_rectangle((1240, 760, 1500, 840), 18, fill=BLUE)
    ctr(d, 778, 'Get Quote', fb(36), WHITE, 1370)
    ctr(d, 950, 'Or call / text (571) 241-9569', fb(52), WHITE)
    return im

scenes = [
    (6.5, still(card(['Welcome to Nova Pro Home'], ['Ring & Google Nest installation · Northern Virginia']))),
    (8.2, still(about())),
    (3.4, zoom_photo(P + '08_ring_doorbell_brick.jpg', 'Video doorbells', 'Ring & Nest · wired the right way')),
    (2.2, zoom_photo(P + '07_ring_floodlight.jpg', 'Security cameras', 'Floodlight · spotlight · indoor')),
    (3.3, zoom_photo(P + 'extras/nest_floodlight_garage.jpg', 'Google Nest cameras', 'Hardwired & set up in the app')),
    (3.4, zoom_photo(P + 'extras/ring_solar_stucco.jpg', 'Solar-powered cameras', 'No outlet? No problem')),
    (5.8, zoom_photo(P + '10_security_collage.jpg', 'Ring Alarm', 'Base station, sensors & keypad')),
    (7.3, still(icon_card('More smart home', 'Installed, connected and explained',
                          ['Nest thermostats', 'Smart locks & keypads', 'Smart lighting', 'Wi-Fi checks & app setup']))),
    (8.4, still(steps())),
    (8.6, still(website())),
    (7.5, still(card(['New videos every', 'Tuesday & Sunday'], ['How-tos, quick fixes & real installs. Subscribe!'], BLUE, 380))),
    (5.4, still(card(['Get a free quote'], ['novaprohome.com  ·  (571) 241-9569', 'Ring Authorized Dealer · Google Nest Pro'], SOFT, 520))),
]

if __name__ == '__main__':
    scenes[0][1](0).save(OUT.rsplit('.', 1)[0] + '_thumb.jpg', quality=90)
    XF = 0.4
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20',
        '-c:a', 'aac', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    prev = None
    for dur, fn in scenes:
        n = int(dur * FPS)
        for k in range(n):
            fr = np.asarray(fn(k / (n - 1)), dtype=np.float32)
            if prev is not None and k < XF * FPS:
                a = k / (XF * FPS); fr = fr * a + prev * (1 - a)
            ff.stdin.write(fr.astype(np.uint8).tobytes())
        prev = np.asarray(fn(1.0), dtype=np.float32)
    ff.stdin.close(); ff.wait(); print('done', ff.returncode)
