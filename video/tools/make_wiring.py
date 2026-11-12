"""Simple, clearly labeled wiring diagrams for job videos (1080x1920 PNG, content in the top 65%
so the make_series caption panel doesn't cover it).
Usage: python3 make_wiring.py doorbell OUT.png
Diagrams are TYPICAL setups for teaching, not a record of a specific house; every one carries a
"typical wiring, check your model's manual" note."""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
fm = lambda s: ImageFont.truetype(F + 'Inter-Medium.otf', s)
NAVY, WHITE, SOFT = (19, 33, 56), (255, 255, 255), (200, 212, 228)
BLUE, YEL, RED, GREY, GREEN = (58, 155, 213), (244, 161, 29), (226, 76, 76), (150, 160, 175), (76, 199, 154)


def box(d, xy, title, sub, col):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, 26, fill=(28, 46, 76), outline=col, width=5)
    tw = d.textlength(title, font=fb(40)); d.text(((x0 + x1 - tw) / 2, y0 + 26), title, font=fb(40), fill=WHITE)
    for i, line in enumerate(sub.split('\n')):
        sw = d.textlength(line, font=fm(28)); d.text(((x0 + x1 - sw) / 2, y0 + 82 + i * 36), line, font=fm(28), fill=SOFT)


def wire(d, pts, col, label=None, at=None):
    d.line(pts, fill=col, width=9, joint='curve')
    if label:
        x, y = at; d.text((x, y), label, font=fm(26), fill=col)


def doorbell(out):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.text((70, 290), 'How a wired doorbell gets power', font=fb(52), fill=WHITE)
    d.text((70, 358), 'Low voltage, about 16-24 V AC', font=fm(34), fill=YEL)
    # transformer (left), chime (right), doorbell (bottom center)
    box(d, (60, 440, 470, 630), 'Transformer', 'near the panel or furnace\n120 V in, 16-24 V out', YEL)
    box(d, (610, 440, 1020, 630), 'Indoor chime', 'terminals: TRANS\nand FRONT', BLUE)
    box(d, (330, 880, 750, 1060), 'Video doorbell', 'replaces the old\nbutton or intercom', GREEN)
    # wire 1: transformer -> chime TRANS
    wire(d, [(470, 510), (610, 510)], RED, 'wire 1', (490, 462))
    # wire 2: chime FRONT -> doorbell
    wire(d, [(815, 630), (815, 780), (640, 780), (640, 880)], WHITE, 'wire 2 (FRONT)', (830, 690))
    # wire 3: doorbell -> transformer
    wire(d, [(440, 880), (440, 750), (265, 750), (265, 630)], GREY, 'wire 3', (120, 670))
    d.text((110, 1080), 'Always powered, so the camera stays on. A press rings the chime.', font=fm(28), fill=SOFT)
    d.rounded_rectangle((60, 1120, 1020, 1185), 18, fill=(60, 30, 30))
    d.text((84, 1134), 'Power off at the breaker first. Typical wiring: check your manual.', font=fm(27), fill=(255, 200, 200))
    im.save(out)


def floodlight(out):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.text((70, 290), 'How a wired floodlight cam connects', font=fb(48), fill=WHITE)
    d.text((70, 358), 'House power, 120 V AC: breaker OFF first', font=fm(34), fill=RED)
    box(d, (60, 440, 470, 630), 'Outdoor box', 'the existing\nlight fixture box', YEL)
    box(d, (610, 440, 1020, 630), 'Floodlight cam', 'mounting plate\non the same box', GREEN)
    rows = [('BLACK = hot', (90, 90, 90), 720), ('WHITE = neutral', WHITE, 800), ('GREEN / bare = ground', GREEN, 880)]
    for label, col, y in rows:
        d.ellipse((150, y - 14, 178, y + 14), fill=col); d.ellipse((902, y - 14, 930, y + 14), fill=col)
        d.line([(178, y), (902, y)], fill=col, width=8)
        lw = d.textlength(label, font=fb(30)); d.rounded_rectangle((540 - lw / 2 - 18, y - 26, 540 + lw / 2 + 18, y + 26), 14, fill=NAVY)
        d.text((540 - lw / 2, y - 18), label, font=fb(30), fill=col if col != (90, 90, 90) else SOFT)
    d.text((150, 660), 'box', font=fm(26), fill=YEL); d.text((850, 660), 'camera', font=fm(26), fill=GREEN)
    d.text((70, 960), 'Wire nuts snug, cover sealed against rain.', font=fm(30), fill=SOFT)
    d.text((70, 1010), 'Usually an inside light switch controls it.', font=fm(30), fill=SOFT)
    d.rounded_rectangle((60, 1080, 1020, 1185), 18, fill=(60, 30, 30))
    d.text((84, 1094), 'Line voltage. Typical wiring: check your manual,', font=fm(27), fill=(255, 200, 200))
    d.text((84, 1134), 'and hire a licensed electrician where required.', font=fm(27), fill=(255, 200, 200))
    im.save(out)


if __name__ == '__main__':
    {'doorbell': doorbell, 'floodlight': floodlight}[sys.argv[1]](sys.argv[2])
