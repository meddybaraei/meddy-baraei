"""Seven vertical topic Shorts with voiceover + music.
Usage: python3 make_shorts.py VOICE.mp3 OUTDIR"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
P = os.path.abspath(HERE + '../../facebook-post') + '/'
VOICE, OUTDIR = sys.argv[1], sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)
W, H, FPS = 1080, 1920, 30
NAVY = (19, 33, 56); NAVY2 = (28, 46, 76); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
SOFT = (200, 212, 228); GREEN = (76, 199, 154); YEL = (244, 161, 29)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
logo = Image.open(HERE + 'logo.png').convert('RGB')

def logo_card(maxw):
    l = logo.copy(); l.thumbnail((maxw, maxw))
    c = Image.new('RGB', (l.width + 36, l.height + 20), WHITE); c.paste(l, (18, 10))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + c.size, 18, fill=255)
    return c, m
SMALL = logo_card(280)

def wrap(d, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def ctr(d, y, t, font, fill):
    w = d.textlength(t, font=font); d.text(((W - w) / 2, y), t, font=font, fill=fill)

def header(im, hook):
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, 0, W, 330), fill=NAVY + (225,))
    c, m = SMALL; im.paste(c, (60, 60), m)
    y = 180
    for ln in wrap(d, hook, fb(58), W - 120):
        d.text((60, y), ln, font=fb(58), fill=WHITE); y += 70
    return d

def caption(d, text):
    lines = wrap(d, text, fb(66), W - 200)
    h = 60 + 82 * len(lines)
    d.rounded_rectangle((60, H - 300 - h, W - 60, H - 300), 30, fill=NAVY + (235,))
    y = H - 300 - h + 30
    for ln in lines: ctr(d, y, ln, fb(66), WHITE); y += 82

def photo(path, hook, text):
    src = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    base = ImageOps.fit(src, (int(W * 1.1), int(H * 1.1)), Image.LANCZOS)
    def f(t):
        z = 1.1 - 0.08 * t
        cw, ch = int(base.width / 1.1 * z), int(base.height / 1.1 * z)
        x, y = (base.width - cw) // 2, (base.height - ch) // 2
        im = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)
        d = header(im, hook); caption(d, text); return im
    return f

def card(hook, big, small='', badge=None, color=BLUE):
    im = Image.new('RGB', (W, H), NAVY)
    d = header(im, hook)
    y = 620
    if badge is not None:
        d.ellipse((W / 2 - 120, 520, W / 2 + 120, 760), fill=color)
        ctr(d, 570, str(badge), fb(130), WHITE); y = 830
    for ln in wrap(d, big, fb(86), W - 160):
        ctr(d, y, ln, fb(86), WHITE); y += 104
    y += 20
    for ln in wrap(d, small, fs(46), W - 200):
        ctr(d, y, ln, fs(46), SOFT); y += 62
    return lambda t: im

def end_card():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(640); im.paste(c, ((W - c.width) // 2, 460), m)
    ctr(d, 800, 'Shop the gear we install', fb(64), WHITE)
    ctr(d, 885, '& book your free install quote', fs(48), BLUE)
    ctr(d, 1040, 'novaprohome.com', fb(84), WHITE)
    ctr(d, 1150, '(571) 241-9569', fb(72), WHITE)
    ctr(d, 1290, 'Ring Authorized Dealer · Google Nest Pro', fs(40), SOFT)
    return lambda t: im

SHORTS = [
    ('01_where_to_put_security_cameras', 'Where should your cameras go?', [
        photo(P + '08_ring_doorbell_brick.jpg', 'Where should your cameras go?', '1. Front door'),
        photo(P + '07_ring_floodlight.jpg', 'Where should your cameras go?', '2. Driveway or garage'),
        photo(P + 'extras/ring_solar_floodlight.jpg', 'Where should your cameras go?', '3. Back door')]),
    ('02_battery_vs_wired_ring_doorbell', 'Battery or wired Ring doorbell?', [
        card('Battery or wired Ring doorbell?', 'Battery', 'Easiest to install. Recharge it now and then.', 'B'),
        card('Battery or wired Ring doorbell?', 'Wired', 'Never needs charging.', 'W', GREEN),
        photo(P + '08_ring_doorbell_brick.jpg', 'Battery or wired Ring doorbell?', 'We install both')]),
    ('03_ring_solar_panel_no_outlet', 'No outlet? Go solar.', [
        photo(P + 'extras/ring_solar_stucco.jpg', 'No outlet? Go solar.', 'Ring solar panel'),
        photo(P + '03_mclean_solar_install.jpg', 'No outlet? Go solar.', 'Keeps the battery topped up'),
        photo(P + 'extras/ring_solar_floodlight.jpg', 'No outlet? Go solar.', 'No wires to run')]),
    ('04_ring_doorbell_not_working_3_checks', 'Ring doorbell acting up?', [
        card('Ring doorbell acting up?', 'Wi-Fi signal', 'Is your router close enough?', 1),
        card('Ring doorbell acting up?', 'Power or battery', 'Charged? Breaker on?', 2),
        card('Ring doorbell acting up?', 'App update', 'Update the Ring app & device', 3)]),
    ('05_nest_thermostat_compatibility', 'Buying a Nest thermostat?', [
        card('Buying a Nest thermostat?', 'Check compatibility first', "Use Google's Nest compatibility checker", '✓' if False else 1),
        card('Buying a Nest thermostat?', 'C-wire or adapter?', 'The checker tells you what your wiring needs', 2, GREEN)]),
    ('06_smart_locks_for_airbnb_hosts', 'Airbnb hosts:', [
        card('Airbnb hosts:', 'A new code for every guest', 'Set and change codes from your phone', 1),
        card('Airbnb hosts:', 'No more lost keys', 'Smart locks installed & set up', 2, GREEN)]),
    ('07_why_hire_a_pro_installer', 'Why hire a pro?', [
        photo(P + '04_installer_on_ladder.jpg', 'Why hire a pro?', 'Clean mounting'),
        photo(P + '08_ring_doorbell_brick.jpg', 'Why hire a pro?', 'Correct wiring'),
        photo(P + '05_installer_garage.jpg', 'Why hire a pro?', 'App setup & a walkthrough')]),
]
STARTS = [0.0, 8.62, 17.67, 27.26, 35.81, 44.50, 50.17]
VEND = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VOICE]).decode())
ENDS = [8.18, 17.15, 26.57, 35.04, 43.88, 49.18, VEND]

for (slug, hook, vis), a, b in zip(SHORTS, STARTS, ENDS):
    vo = os.path.join(OUTDIR, slug + '_vo.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', VOICE, '-ss', str(a), '-to', str(b + 0.15), '-af', 'afade=t=in:d=0.05,afade=t=out:st=%f:d=0.12' % (b - a), vo], check=True)
    talk = b - a + 0.6
    END = 3.0
    total = talk + END
    per = talk / len(vis)
    scenes = [(per, f) for f in vis] + [(END, end_card())]
    silent = os.path.join(OUTDIR, slug + '_silent.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '21', silent], stdin=subprocess.PIPE)
    prev = None
    for dur, fn in scenes:
        n = int(dur * FPS)
        for k in range(n):
            fr = np.asarray(fn(k / max(1, n - 1)), dtype=np.float32)
            if prev is not None and k < 0.3 * FPS:
                al = k / (0.3 * FPS); fr = fr * al + prev * (1 - al)
            ff.stdin.write(fr.astype(np.uint8).tobytes())
        prev = np.asarray(fn(1.0), dtype=np.float32)
    ff.stdin.close(); ff.wait()
    vis[0](0.0).save(os.path.join(OUTDIR, slug + '_thumb.jpg'), quality=88)
    music = os.path.join(OUTDIR, slug + '_music.wav')
    subprocess.run([sys.executable, HERE + 'make_music.py', music, str(total + 1)], check=True, stdout=subprocess.DEVNULL)
    out = os.path.join(OUTDIR, slug + '.mp4')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', silent, '-i', vo, '-i', music, '-filter_complex',
                    '[1:a]adelay=300|300[v];[2:a]volume=0.16[m];[v][m]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], check=True)
    for tmp in (vo, silent, music): os.remove(tmp)
    print(slug, round(total, 1))
