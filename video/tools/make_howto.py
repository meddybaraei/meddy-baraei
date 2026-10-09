import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

P = '/home/user/meddy-baraei/facebook-post/'
S = __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '/'
OUT = sys.argv[1]
W, H, FPS = 1920, 1080, 30
NAVY = (19, 33, 56); NAVY2 = (28, 46, 76); BLUE = (58, 155, 213); WHITE = (255, 255, 255)
SOFT = (200, 212, 228); RED = (226, 84, 64); GREEN = (76, 199, 154); YEL = (244, 161, 29)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)
logo = Image.open(S + 'logo.png').convert('RGB')

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

def ctr(d, y, t, font, fill, cx=W / 2):
    w = d.textlength(t, font=font); d.text((cx - w / 2, y), t, font=font, fill=fill)

# ---------- right-panel visuals (860x860) ----------
PW = PH = 860
def panel_bg():
    im = Image.new('RGB', (PW, PH), NAVY2); return im, ImageDraw.Draw(im)

def photo(path):
    return ImageOps.fit(ImageOps.exif_transpose(Image.open(path)).convert('RGB'), (PW, PH), Image.LANCZOS)

def v_check():
    im, d = panel_bg()
    # transformer box
    d.rounded_rectangle((180, 220, 680, 560), 30, fill=(70, 84, 108))
    d.text((250, 300), 'Doorbell', font=fb(56), fill=WHITE)
    d.text((250, 370), 'transformer', font=fb(56), fill=WHITE)
    d.text((250, 460), 'check voltage', font=fm(40), fill=SOFT)
    d.text((250, 505), 'in the Ring manual', font=fm(40), fill=SOFT)
    for x in (300, 560):
        d.line((x, 560, x, 700), fill=YEL, width=14)
    ctr(d, 740, 'Existing wired doorbell? ✓', fb(44), GREEN, PW / 2)
    return im

def v_power():
    im, d = panel_bg()
    d.rounded_rectangle((230, 120, 630, 700), 24, fill=(60, 72, 96))
    for i in range(6):
        y = 170 + i * 85
        d.rounded_rectangle((300, y, 560, y + 60), 10, fill=(40, 50, 70))
        on = i != 2
        d.rounded_rectangle((470 if on else 310, y + 8, 550 if on else 390, y + 52), 8, fill=GREEN if on else RED)
    d.text((570, 340), '← OFF', font=fb(48), fill=RED)
    ctr(d, 750, 'Turn off the doorbell breaker', fb(46), WHITE, PW / 2)
    return im

def v_wires():
    im, d = panel_bg()
    d.rounded_rectangle((300, 140, 560, 560), 30, fill=(90, 100, 120))
    for i, (y, lab) in enumerate(((260, 'A'), (440, 'B'))):
        d.ellipse((400, y - 30, 460, y + 30), fill=(200, 200, 200))
        d.line((430, y, 120, y + 60 * (1 if i else -1) + 200), fill=YEL if i == 0 else (240, 240, 240), width=14)
        d.rounded_rectangle((60, y + 60 * (1 if i else -1) + 170, 190, y + 60 * (1 if i else -1) + 240), 12, fill=BLUE)
        d.text((100, y + 60 * (1 if i else -1) + 175), lab, font=fb(52), fill=WHITE)
    ctr(d, 680, 'Label each wire with tape', fb(46), WHITE, PW / 2)
    ctr(d, 750, 'so they don\'t slip into the wall', fm(38), SOFT, PW / 2)
    return im

def v_chime():
    im, d = panel_bg()
    d.rounded_rectangle((170, 150, 690, 520), 30, fill=(230, 230, 230))
    for x, t in ((260, 'FRONT'), (420, 'TRANS'), (580, 'REAR')):
        d.ellipse((x - 28, 300, x + 28, 356), fill=(150, 150, 150))
        tw = d.textlength(t, font=fs(30)); d.text((x - tw / 2, 370), t, font=fs(30), fill=(60, 60, 60))
    d.rounded_rectangle((300, 420, 560, 490), 14, fill=BLUE)
    ctr(d, 432, 'Ring chime kit', fb(36), WHITE, 430)
    ctr(d, 600, 'Inside: open your chime cover', fb(44), WHITE, PW / 2)
    ctr(d, 665, 'and add the kit that came in the box', fm(38), SOFT, PW / 2)
    return im

def v_drill():
    im, d = panel_bg()
    d.rounded_rectangle((330, 120, 530, 560), 26, outline=WHITE, width=8)
    for y in (180, 500):
        d.ellipse((410, y - 22, 450, y + 22), fill=YEL)
    d.line((430, 220, 430, 460), fill=SOFT, width=4)
    d.rectangle((560, 120, 620, 560), fill=(110, 120, 140))
    for y in range(140, 560, 40): d.line((560, y, 620, y), fill=NAVY2, width=3)
    ctr(d, 620, 'Level the bracket, mark & drill', fb(44), WHITE, PW / 2)
    ctr(d, 685, 'Brick or stucco? Use the masonry bit + anchors', fm(34), SOFT, PW / 2)
    return im

def v_connect():
    im, d = panel_bg()
    d.rounded_rectangle((320, 120, 540, 640), 40, fill=(30, 30, 30))
    d.ellipse((380, 180, 480, 280), fill=(70, 70, 70)); d.ellipse((410, 210, 450, 250), fill=(20, 20, 40))
    for y in (420, 520):
        d.ellipse((400, y - 24, 460, y + 24), fill=(190, 190, 190))
        d.line((120, y + (y - 470) * 2, 400, y), fill=YEL if y == 420 else (240, 240, 240), width=14)
    ctr(d, 700, 'Either wire → either screw', fb(46), WHITE, PW / 2)
    ctr(d, 765, 'Tighten until snug. No polarity.', fm(38), SOFT, PW / 2)
    return im

def v_app():
    im, d = panel_bg()
    d.rounded_rectangle((280, 80, 580, 640), 44, fill=(20, 20, 24))
    d.rounded_rectangle((300, 130, 560, 590), 22, fill=(235, 240, 246))
    ctr(d, 170, 'Set Up a Device', fs(28), NAVY, 430)
    for i, t in enumerate(('1  Scan QR code', '2  Connect Wi-Fi', '3  Name: Front Door')):
        d.rounded_rectangle((320, 240 + i * 100, 540, 310 + i * 100), 14, fill=WHITE, outline=(200, 210, 222), width=2)
        d.text((336, 258 + i * 100), t, font=fm(24), fill=NAVY)
    ctr(d, 690, 'Power on, then set up in the Ring app', fb(42), WHITE, PW / 2)
    return im

def v_test():
    im = photo(P + 'extras/ring_doorbell_trim.jpg'); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((40, PH - 190, PW - 40, PH - 40), 26, fill=NAVY + (230,))
    ctr(d, PH - 170, 'Press the button: chime rings', fb(40), WHITE, PW / 2)
    ctr(d, PH - 110, 'Check live view & motion zones', fm(34), BLUE, PW / 2)
    return im

# ---------- slides ----------
def step_slide(n, total, title, body, visual):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(240); im.paste(c, (80, 60), m)
    d.text((80, 230), f'STEP {n} OF {total}', font=fs(34), fill=BLUE)
    y = 290
    for ln in wrap(d, title, fb(70), 820):
        d.text((80, y), ln, font=fb(70), fill=WHITE); y += 86
    y += 24
    for ln in wrap(d, body, fm(40), 820):
        d.text((80, y), ln, font=fm(40), fill=SOFT); y += 56
    # progress bar
    d.rounded_rectangle((80, 990, 900, 1004), 7, fill=NAVY2)
    d.rounded_rectangle((80, 990, 80 + int(820 * n / total), 1004), 7, fill=BLUE)
    pm = Image.new('L', (PW, PH), 0); ImageDraw.Draw(pm).rounded_rectangle((0, 0, PW, PH), 36, fill=255)
    im.paste(visual, (W - PW - 80, (H - PH) // 2), pm)
    return im

def title_slide():
    im = photo(P + '08_ring_doorbell_brick.jpg').resize((W, W)).crop((0, 420, W, 420 + H))
    im = Image.blend(im, Image.new('RGB', (W, H), NAVY), 0.72); d = ImageDraw.Draw(im)
    c, m = logo_card(420); im.paste(c, ((W - c.width) // 2, 150), m)
    ctr(d, 430, 'How to Install a', fb(96), WHITE)
    ctr(d, 540, 'Ring Wired Doorbell', fb(110), WHITE)
    ctr(d, 700, '9 steps  •  about 30–45 minutes  •  basic tools', fs(44), BLUE)
    return im

def safety_slide():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    ctr(d, 260, '⚠  Before you start', fb(80), YEL)
    lines = ['This is a general guide. Always follow the instructions',
             'that came with your Ring doorbell.',
             'Doorbell wiring is low voltage, but your transformer connects to',
             'household power. If anything looks damaged or unclear, call a pro.']
    y = 420
    for ln in lines: ctr(d, y, ln, fm(44), SOFT); y += 70
    return im

def outro_slide():
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    c, m = logo_card(520); im.paste(c, ((W - c.width) // 2, 120), m)
    ctr(d, 400, 'Not comfortable with wiring?', fb(88), WHITE)
    ctr(d, 510, "We'll install it for you.", fb(88), BLUE)
    ctr(d, 680, 'novaprohome.com   •   (571) 241-9569', fb(60), WHITE)
    ctr(d, 790, 'Ring Authorized Dealer · Google Nest Pro · Northern Virginia', fs(40), SOFT)
    return im

steps = [
    ('Check what you have', 'You need an existing wired doorbell and a working doorbell transformer. Your Ring manual lists the voltage it needs.', v_check()),
    ('Turn off the power', 'Switch off the breaker for the doorbell, then press the old button to confirm the chime is silent.', v_power()),
    ('Remove the old button', 'Unscrew the old doorbell and disconnect the two wires. Tape them to the wall so they don\'t fall back inside.', v_wires()),
    ('Prep the indoor chime', 'Open your chime cover and install the chime kit from the Ring box exactly as its insert shows.', v_chime()),
    ('Mount the bracket', 'Hold the bracket level over the wires, mark the holes and drill. Use anchors on brick or stucco.', v_drill()),
    ('Connect the wires', 'Attach one wire to each screw terminal on the back of the doorbell. Either wire can go on either screw.', v_connect()),
    ('Attach the doorbell', 'Click the doorbell onto the bracket and tighten the security screw at the bottom.', photo(P + '08_ring_doorbell_brick.jpg')),
    ('Power on & set up', 'Turn the breaker back on. In the Ring app tap Set Up a Device, scan the QR code and join your Wi-Fi.', v_app()),
    ('Test everything', 'Press the button and listen for your chime. Check live view, then set motion zones in the app.', v_test()),
]

import json, os
D = json.loads(os.environ['DURS']) if os.environ.get('DURS') else [4.0, 5.0] + [6.5] * len(steps) + [6.0]
scenes = [(D[0], title_slide()), (D[1], safety_slide())]
for i, (t, b, v) in enumerate(steps, 1):
    scenes.append((D[i + 1], step_slide(i, len(steps), t, b, v)))
scenes.append((D[-1], outro_slide()))
scenes[0][1].save(S + 'howto_thumb.jpg', quality=90)

XF = 0.4
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
    '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
prev = None
for dur, img in scenes:
    cur = np.asarray(img, dtype=np.float32)
    n = int(dur * FPS)
    for k in range(n):
        if prev is not None and k < XF * FPS:
            a = k / (XF * FPS); fr = cur * a + prev * (1 - a)
        else:
            fr = cur
        ff.stdin.write(fr.astype(np.uint8).tobytes())
    prev = cur
ff.stdin.close(); ff.wait(); print('done', ff.returncode)
