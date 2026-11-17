"""Append a 4 s NovaProHome contact end card to an owner video.
Usage: python3 add_endcard.py IN.mp4 OUT.mp4 "Headline?" [--no-phone]   (--no-phone for YouTube)"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
src, out, head = sys.argv[1], sys.argv[2], sys.argv[3]; phone = '--no-phone' not in sys.argv
W, H = 1080, 1920
im = Image.new('RGB', (W, H), (14, 20, 38)); d = ImageDraw.Draw(im)
F = '/usr/share/fonts/opentype/inter/'
fb = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s); fs = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
logo = Image.open(HERE + 'logo.png').convert('RGB'); logo.thumbnail((620, 620))
card = Image.new('RGB', (logo.width + 60, logo.height + 40), 'white'); card.paste(logo, (30, 20))
im.paste(card, ((W - card.width) // 2, 560))
def c(y, t, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)
y = 560 + card.height + 90
c(y, head, fb(54), (255, 255, 255)); y += 110
c(y, 'novaprohome.com/contact', fb(60), (58, 155, 213)); y += 95
c(y, '(571) 241-9569 · Meddy@novaprohome.com' if phone else 'Meddy@novaprohome.com', fs(40), (200, 212, 228)); y += 80
c(y, 'Ring Authorized Dealer · Google Nest Pro', fs(36), (200, 212, 228))
png = tempfile.mktemp(suffix='.png'); im.save(png)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-loop', '1', '-t', '4', '-i', png, '-f', 'lavfi', '-t', '4', '-i', 'anullsrc=r=48000:cl=stereo',
    '-filter_complex', '[0:v]scale=1080:1920,setsar=1,fps=30[v0];[1:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v1];'
    '[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[v0][a0][v1][2:a]concat=n=2:v=1:a=1[v][a]',
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
os.remove(png); print(out)
