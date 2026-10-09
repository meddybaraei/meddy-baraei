import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

P = '/home/user/meddy-baraei/facebook-post/'
S = __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '/'
OUT = sys.argv[1]
W, H, FPS = 1080, 1920, 30
NAVY = (19, 33, 56); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)

logo = Image.open(S + 'logo.png').convert('RGB')

def logo_card(maxw):
    l = logo.copy(); l.thumbnail((maxw, maxw))
    c = Image.new('RGB', (l.width + 36, l.height + 20), WHITE); c.paste(l, (18, 10))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + c.size, 18, fill=255)
    return c, m

SMALL_LOGO = logo_card(300)

def ctr(d, y, t, font, fill):
    w = d.textlength(t, font=font); d.text(((W - w) / 2, y), t, font=font, fill=fill)

def title_card(lines, sub=None, extra=None):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(640); im.paste(c, ((W - c.width) // 2, 430), m)
    y = 430 + c.height + 110
    for t in lines:
        ctr(d, y, t, fb(92), WHITE); y += 112
    if sub:
        y += 20
        for t in sub:
            ctr(d, y, t, fs(48), BLUE); y += 66
    if extra:
        y += 70
        for t, f, col in extra:
            ctr(d, y, t, f, col); y += f.size + 30
    return im

def photo_scene(path, title, sub):
    src = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    base = ImageOps.fit(src, (int(W * 1.12), int(H * 1.12)), Image.LANCZOS)
    def frame(t):  # t in 0..1, slow zoom-in (Ken Burns)
        z = 1.12 - 0.10 * t
        cw = int(base.width / 1.12 * z); ch = int(base.height / 1.12 * z)
        x = (base.width - cw) // 2; y = (base.height - ch) // 2
        im = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)
        d = ImageDraw.Draw(im, 'RGBA')
        # caption bar
        d.rounded_rectangle((60, H - 470, W - 60, H - 220), 32, fill=NAVY + (235,))
        ctr(d, H - 430, title, fb(64), WHITE)
        ctr(d, H - 330, sub, fs(44), BLUE)
        c, m = SMALL_LOGO; im.paste(c, (60, 110), m)
        return im
    return frame

scenes = [
    (2.8, lambda t: INTRO),
    (2.6, photo_scene(P + 'extras/ring_spotlight_cam_stone.jpg', 'Ring Spotlight Cam', 'Arlington, VA')),
    (2.6, photo_scene(P + '04_installer_on_ladder.jpg', 'Clean, pro installs', 'Mounted, wired & tested')),
    (2.6, photo_scene(P + '07_ring_floodlight.jpg', 'Ring Floodlight Cam', 'Northern Virginia')),
    (2.6, photo_scene(P + 'extras/nest_floodlight_garage.jpg', 'Nest Cam with Floodlight', 'Vienna, VA')),
    (2.6, photo_scene(P + '06_nest_cam.jpg', 'Google Nest Cam', 'Hardwired & set up')),
    (2.6, photo_scene(P + 'extras/ring_solar_stucco.jpg', 'Ring Solar Panels', 'McLean, VA · no wiring needed')),
    (2.6, photo_scene(P + '08_ring_doorbell_brick.jpg', 'Ring Video Doorbell', 'Wired the right way')),
    (2.6, photo_scene(P + '05_installer_garage.jpg', 'Ring Authorized Dealer', 'Google Nest Pro')),
    (4.0, lambda t: OUTRO),
]

INTRO = title_card(['Ring & Google Nest', 'Installation'], ['Northern Virginia'])
OUTRO = title_card(['Get a free quote'], None, [
    ('novaprohome.com', fb(70), WHITE),
    ('(571) 241-9569', fb(70), WHITE),
    ('Ring Authorized Dealer · Google Nest Pro', fs(40), BLUE),
    ('Loudoun · Fairfax · Arlington · Prince William', fm(36), (200, 212, 228)),
])

XF = 0.4  # crossfade seconds
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
    '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)

prev_last = None
for i, (dur, fn) in enumerate(scenes):
    n = int(dur * FPS)
    for k in range(n):
        fr = np.asarray(fn(k / (n - 1)), dtype=np.float32)
        if prev_last is not None and k < XF * FPS:
            a = k / (XF * FPS); fr = fr * a + prev_last * (1 - a)
        ff.stdin.write(fr.astype(np.uint8).tobytes())
    prev_last = np.asarray(fn(1.0), dtype=np.float32)
    if i == 0: INTRO.save(S + 'video_cover.jpg', quality=90)
ff.stdin.close(); ff.wait()
print('done', ff.returncode)
