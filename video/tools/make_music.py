"""Original royalty-free background bed (warm synth pads + soft pulse). Usage: python3 make_music.py OUT.wav SECONDS"""
import sys, wave
import numpy as np
SR = 44100
out, dur = sys.argv[1], float(sys.argv[2])
t = np.arange(int(SR * dur)) / SR
bpm = 96; beat = 60 / bpm; bar = beat * 4
# I - V - vi - IV in C major (frequencies of chord tones)
chords = [[261.63, 329.63, 392.00], [196.00, 246.94, 293.66], [220.00, 261.63, 329.63], [174.61, 220.00, 261.63]]
bass = [65.41, 49.00, 55.00, 43.65]
sig = np.zeros_like(t)
for i in range(int(dur / bar) + 1):
    s, e = int(i * bar * SR), int(min((i + 1) * bar, dur) * SR)
    if s >= len(t): break
    tt = t[s:e] - t[s]
    env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.6)
    pad = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.003 * tt) for f in chords[i % 4])
    sig[s:e] += 0.10 * pad * env
    b = bass[i % 4]
    for k in range(4):  # soft bass pulse on each beat
        bs = int(k * beat * SR); seg = tt[bs:] - tt[bs] if bs < len(tt) else None
        if seg is None: continue
        sig[s + bs:e] += 0.22 * np.sin(2 * np.pi * b * seg) * np.exp(-seg * 3.5)
    for k in range(8):  # light pluck arpeggio
        ps = int(k * beat / 2 * SR)
        if ps >= len(tt): continue
        seg = tt[ps:] - tt[ps]; f = chords[i % 4][k % 3] * 2
        sig[s + ps:e] += 0.05 * np.sin(2 * np.pi * f * seg) * np.exp(-seg * 6)
fade = np.minimum(1, np.minimum(t / 1.5, (dur - t) / 2.5))
sig = sig * fade
sig = sig / (np.abs(sig).max() + 1e-9) * 0.6
pcm = (np.stack([sig, sig], 1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', dur)
