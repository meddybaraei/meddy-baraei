"""Original royalty-free background music. Usage: python3 make_music.py OUT.wav SECONDS [calm|upbeat]
calm (default): warm synth pads + soft pulse. upbeat: 120 bpm kick/clap/hats, bouncy bass and bright plucks."""
import sys, wave
import numpy as np
SR = 44100
out, dur = sys.argv[1], float(sys.argv[2])
STYLE = sys.argv[3] if len(sys.argv) > 3 else 'calm'
t = np.arange(int(SR * dur)) / SR
rng = np.random.default_rng(7)

def hit(sig, start, wave_fn, length):
    """Add a one-shot sound starting at `start` seconds."""
    s = int(start * SR)
    if s >= len(sig): return
    n = min(int(length * SR), len(sig) - s); tt = np.arange(n) / SR
    sig[s:s + n] += wave_fn(tt)

def upbeat():
    sig = np.zeros_like(t)
    beat = 60 / 120; bar = beat * 4
    # vi - IV - I - V in C major: bright, feel-good loop
    chords = [[220.00, 261.63, 329.63], [174.61, 220.00, 261.63], [261.63, 329.63, 392.00], [196.00, 246.94, 293.66]]
    bass = [110.00, 87.31, 130.81, 98.00]
    kick = lambda tt: 0.9 * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
    clap = lambda tt: 0.35 * rng.standard_normal(len(tt)) * np.exp(-tt * 22)
    hat = lambda tt: 0.12 * np.diff(rng.standard_normal(len(tt) + 1)) * np.exp(-tt * 60)
    nbars = int(dur / bar) + 1
    for i in range(nbars):
        b0 = i * bar; ch = chords[i % 4]
        intro = i < 1  # first bar: no drums, lets the hook land
        for k in range(4):
            if not intro: hit(sig, b0 + k * beat, kick, 0.35)
            if not intro and k in (1, 3): hit(sig, b0 + k * beat, clap, 0.2)
            if not intro: hit(sig, b0 + k * beat + beat / 2, hat, 0.08)
        for k in range(8):  # bouncy eighth-note bass, octave jumps on the offbeats
            f = bass[i % 4] * (2 if k % 2 else 1)
            hit(sig, b0 + k * beat / 2, lambda tt, f=f: 0.32 * np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 * np.exp(-tt * 9), beat / 2)
        for k in (0, 3, 6):  # syncopated chord stabs
            for f in ch:
                hit(sig, b0 + k * beat / 2, lambda tt, f=f: 0.07 * (np.sin(2 * np.pi * f * 2 * tt) + 0.4 * np.sin(2 * np.pi * f * 4.01 * tt)) * np.exp(-tt * 5), 0.5)
        mel = [ch[2] * 2, ch[1] * 2, ch[2] * 2, ch[0] * 4, ch[2] * 2, ch[1] * 2, ch[0] * 2, ch[1] * 2]
        for k, f in enumerate(mel):  # bright pluck melody on 16ths-ish pattern
            if k in (1, 5) and i % 2: continue
            hit(sig, b0 + k * beat / 2, lambda tt, f=f: 0.06 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 10), 0.3)
    return sig
bpm = 96; beat = 60 / bpm; bar = beat * 4
# I - V - vi - IV in C major (frequencies of chord tones)
chords = [[261.63, 329.63, 392.00], [196.00, 246.94, 293.66], [220.00, 261.63, 329.63], [174.61, 220.00, 261.63]]
bass = [65.41, 49.00, 55.00, 43.65]
sig = upbeat() if STYLE == 'upbeat' else np.zeros_like(t)
for i in ([] if STYLE == 'upbeat' else range(int(dur / bar) + 1)):  # calm bed
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
if STYLE == 'upbeat': sig = np.tanh(sig / (np.abs(sig).max() + 1e-9) * 2.5)  # glue + loudness
sig = sig / (np.abs(sig).max() + 1e-9) * 0.6
pcm = (np.stack([sig, sig], 1) * 32767).astype(np.int16)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', dur)
