"""last_leaf_sound.py: the score and sound effects for "The Last Leaf", synthesized in code (no samples, no services).

    python audio/last_leaf_sound.py          → assets/last_leaf.wav (15 s, 44.1 kHz, stereo)

Every time below is in video seconds and matches src/scenes/last_leaf.js (shot B starts at 5.0, shot C at 9.6).
Needs numpy and scipy. The output is deterministic: the same script makes the same file.
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 44100, 15.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
music = np.zeros((2, N))
sfx = np.zeros((2, N))


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def add(bus, sig, t, gain=1.0, pan=0.0):
    """Mix a mono signal into a bus at time t, equal-power panned (-1 left … 1 right)."""
    i = int(t * SR)
    if i >= N or len(sig) == 0:
        return
    sig = sig[: N - i] * gain
    a = (pan + 1) * np.pi / 4
    bus[0, i:i + len(sig)] += sig * np.cos(a) * np.sqrt(2)
    bus[1, i:i + len(sig)] += sig * np.sin(a) * np.sqrt(2)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'lowpass', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'highpass', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)


def sweep_noise(dur, fc, q=2.0, amp=None):
    """Band-passed noise whose centre (Hz) and level follow fc(t) and amp(t): wind, whooshes, skids."""
    n = int(dur * SR)
    x, y, zi, B = rng.standard_normal(n), np.zeros(n), None, 256
    for s in range(0, n, B):
        tm = (s + B / 2) / SR
        f = float(np.clip(fc(tm), 60, SR / 2.3))
        sos = butter(2, [f / (1 + .5 / q), f * (1 + .5 / q)], 'bandpass', fs=SR, output='sos')
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        y[s:s + B], zi = sosfilt(sos, x[s:s + B], zi=zi)
    if amp is not None:
        y *= amp(np.arange(n) / SR)
    return y


# ---------- instruments ----------
def harp(f, dur=2.5, bright=1.0, decay=1.0):
    """A plucked string: harmonics that die away faster the higher they are."""
    t = tt(dur)
    s = sum((1 / k ** 1.5) * (bright ** (k - 1)) * np.sin(2 * np.pi * f * k * (1 + .0004 * k * k) * t) * np.exp(-t * decay * (1.1 + .9 * k))
            for k in range(1, 11) if f * k < 16000)
    return s * (1 - np.exp(-t / .002)) * .55


def pizz(f, dur=.6):
    return harp(f, dur, bright=.8, decay=4.0)


def glock(f, dur=2.2):
    t = tt(dur)
    parts = [(1, 1, 1.4), (2.76, .45, 3.5), (5.40, .22, 7), (8.93, .1, 12)]
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in parts if f * r < 18000)
    return s * (1 - np.exp(-t / .0008)) * .5


def bass(f, dur=1.2):
    t = tt(dur)
    s = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t) + .08 * np.sin(6 * np.pi * f * t)
    return s * (1 - np.exp(-t / .008)) * np.exp(-t / .9) * np.clip((dur - t) / .08, 0, 1)


def pad(notes, dur, a=.6, r=.8):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * midi(m) * d * t) + .15 * np.sin(6 * np.pi * midi(m) * d * t) for m in notes for d in (1, 1.004))
    env = np.clip(t / a, 0, 1) * np.clip((dur - t) / r, 0, 1)
    return lp(s * env, 1800) / (2 * len(notes))


def glide(f0, f1, dur, vib=0.0, vib_hz=6.0, curve=1.0):
    """Phase-continuous pitch glide from f0 to f1, with optional vibrato (in semitones)."""
    t = tt(dur)
    f = f0 * (f1 / f0) ** ((t / dur) ** curve) * 2 ** (vib * np.sin(2 * np.pi * vib_hz * t) / 12)
    return 2 * np.pi * np.cumsum(f) / SR


def trombone(f0, f1, dur, vib=0.0):
    ph = glide(f0, f1, dur, vib, 5.5)
    t = tt(dur)
    s = sum(np.sin(k * ph) / k for k in range(1, 14))
    s = bp(lp(s, 1500), 120, 4000)
    return s * np.clip(t / .04, 0, 1) * np.clip((dur - t) / .08, 0, 1) * .5


# ---------- sound effects ----------
def boing(f=420, dur=.45, size=1.0):
    """A cartoon take: a springy wobble in pitch that settles."""
    t = tt(dur)
    f_t = f * (1 + .35 * size * np.sin(2 * np.pi * 16 * t) * np.exp(-t * 7)) * (1 + .25 * np.exp(-t * 20))
    s = np.sin(2 * np.pi * np.cumsum(f_t) / SR)
    return s * (1 - np.exp(-t / .003)) * np.exp(-t * 7) * .6


def pop(dur=.07):
    ph = glide(1400, 350, dur, curve=.5)
    t = tt(dur)
    return np.sin(ph) * np.exp(-t * 45) * .7


def snap():
    t = tt(.05)
    return (hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 180) * .5 + np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 90) * .3)


def step(pitch=1.0):
    t = tt(.08)
    click = bp(rng.standard_normal(len(t)), 700 * pitch, 2800 * pitch) * np.exp(-t * 90)
    thud = np.sin(2 * np.pi * 130 * pitch * t) * np.exp(-t * 60)
    return (click * .8 + thud * .6) * .5


def thump():
    t = tt(.5)
    ph = glide(95, 42, .5, curve=.4)
    return np.sin(ph) * np.exp(-t * 9) * .9 + lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 25) * .4


def whoosh(dur, f0, f1, peak=.5, gain=1.0):
    def fc(x):
        return f0 * (f1 / f0) ** (x / dur)

    def amp(x):
        k = np.clip(x / dur, 0, 1)
        return np.where(k < peak, (k / peak) ** 2, ((1 - k) / (1 - peak)) ** 1.5) * gain
    return sweep_noise(dur, fc, 1.6, amp)


def slide_whistle(f0, f1, dur, curve=1.0):
    ph = glide(f0, f1, dur, vib=.25, vib_hz=7, curve=curve)
    t = tt(dur)
    breath = bp(rng.standard_normal(len(t)), 1500, 6000) * .05
    return (np.sin(ph) + .12 * np.sin(2 * ph) + breath) * np.clip(t / .03, 0, 1) * np.clip((dur - t) / .05, 0, 1) * .35


# ---------- wind: the same gusts that bend the grass in the scene ----------
GUSTS = [(2.75, .45), (4.3, 1.0), (5.0 + 1.55, 1.0)]


def gust_env(x):
    x = np.asarray(x, float)
    rise = np.clip(x / .2, 0, 1)
    return np.where(x < 0, 0, np.where(x < .2, rise * rise * (3 - 2 * rise), np.exp(-(x - .2) * 2.5)))


def breeze(t):
    return .25 * np.sin(t * 1.7) + .15 * np.sin(t * 2.9 + 1)


bed = sweep_noise(DUR, lambda x: 380 + 120 * np.sin(x * .7), 1.2)
tb = np.arange(N) / SR
bed *= .045 * (1 + 1.3 * breeze(tb)) * np.where(tb < 9.6, 1.0, .55)   # shot C is calm
add(sfx, bed, 0, pan=-.15)
for e, a in GUSTS:
    d = 2.2
    body = sweep_noise(d, lambda x: 300 + 1100 * gust_env(x), 1.4, lambda x: .36 * a * gust_env(x))
    howl = sweep_noise(d, lambda x: 900 + 1500 * gust_env(x), 7.0, lambda x: .18 * a * gust_env(x))
    sig = body + howl
    half = len(sig) // 2   # the gust blows left to right, like the wind lines
    add(sfx, sig[:half], e, pan=-.6)
    add(sfx, sig[half:], e + half / SR, pan=.5)

# ---------- shot A (0–5): the last leaf ----------
add(sfx, snap(), 3.0, .8, pan=.15)                       # the leaf lets go
add(sfx, boing(520, .4, .7), 3.05, .5)                   # Clawd's take
add(sfx, pop(), 3.12, .35, pan=.35)                      # the "!" emote
add(sfx, boing(380, .5, 1.2), 4.38, .65)                 # the snatch: a bigger take
add(sfx, pop(), 4.45, .35, pan=.35)
add(sfx, whoosh(.25, 900, 2500, .5), 4.58, .25)          # the turn's smear
for i, ts in enumerate(np.arange(4.78, 5.0, .11)):       # off running
    add(sfx, step(1 + .08 * (i % 2)), ts, .5, pan=.1)
w = whoosh(.55, 600, 3800, .6, 1.4)                      # the whip pan, sweeping left → right
add(sfx, w[: len(w) // 2], 4.62, .35, pan=-.7)
add(sfx, w[len(w) // 2:], 4.62 + len(w) // 2 / SR, .35, pan=.7)

# ---------- shot B (5–9.6): the chase ----------
for i, ts in enumerate(np.arange(5.0, 6.28, .11)):
    add(sfx, step(1 + .08 * (i % 2) + .02 * rng.standard_normal()), ts, .45, pan=-.2)
add(sfx, step(.8), 6.3, .5, pan=-.2)                     # crouch
add(sfx, slide_whistle(560, 1500, .36, .7), 6.42, .7)    # the leap…
add(sfx, slide_whistle(1500, 420, .3, 1.4), 6.78, .6)    # …and the near miss, falling
add(sfx, thump(), 7.0, .9)                               # landing
skid = sweep_noise(.5, lambda x: 2200 - 1400 * x, 2.5, lambda x: .6 * np.exp(-x * 4) * (.7 + .3 * np.sin(x * 2 * np.pi * 35)))
add(sfx, skid, 7.0, .5, pan=-.1)
add(sfx, boing(600, .35, .6), 7.05, .4)                  # surprised, looking up
add(sfx, pop(), 7.12, .3, pan=.3)
add(sfx, whoosh(.2, 800, 1800, .5), 7.48, .15)           # turns toward us
# the sad trombone, as Clawd slumps
for t0, m0, m1, d, vib in [(7.92, 62, 62, .28, 0), (8.22, 61, 61, .28, 0), (8.52, 60, 60, .28, 0), (8.82, 59, 58.6, .75, .35)]:
    add(music, trombone(midi(m0 - 12), midi(m1 - 12), d, vib), t0, .4)
add(sfx, whoosh(.6, 400, 2200, .45, 1.2), 9.3, .45, pan=0)   # brush wipe

# ---------- shot C (9.6–15): it comes back ----------
add(sfx, lp(rng.standard_normal(int(.03 * SR)), 2500) * np.exp(-tt(.03) * 120), 12.6, .25)   # the leaf lands: pat
add(sfx, pop(.09), 12.95, .45, pan=.3)                   # surprised
add(sfx, boing(700, .3, .5), 12.95, .3)
add(sfx, glock(midi(91), 1.2), 14.75, .08, pan=0)        # the iris shuts: tink

# ---------- score (100 bpm, a beat is 0.6 s) ----------
H, G, P, BS = .22, .16, .2, .32   # harp, glock, pizz, bass levels


def harp_at(t, m, g=1.0, dur=2.5):
    add(music, harp(midi(m), dur), t, H * g, pan=np.clip((m - 64) / 40, -.4, .4))


# A: hopeful arpeggio under the leaf, then lifting to F as Clawd appears
arp = {0.0: [48, 55, 60, 64, 67, 71, 67, 64], 2.4: [41, 48, 53, 57, 60, 64, 60, 57]}
for t0, notes in arp.items():
    for i, m in enumerate(notes[: 8 if t0 == 0 else 2]):
        harp_at(.15 + t0 + i * .3, m, .8)
add(music, bass(midi(36), 2.4), .15, BS * .6)
add(music, bass(midi(41), .6), 2.55, BS)
# the leaf motif: a slow sway down, left hanging (it returns, resolved, when the leaf lands in shot C)
for t0, m in [(.6, 81), (.9, 79), (1.2, 76), (1.65, 74)]:
    add(music, glock(midi(m)), t0, G, pan=.25)
# the fall: bouncy pizzicato sways down with the leaf; oom-pah bass as Clawd bounces underneath
for i, m in enumerate([81, 79, 77, 76, 77, 74, 72, 74, 71]):
    add(music, pizz(midi(m)), 3.05 + i * .15, P, pan=.2)
for t0, m in zip([3.0, 3.3, 3.6, 3.9, 4.2], [41, 48, 43, 50, 43]):
    add(music, pizz(midi(m), .5), t0, P * 1.3, pan=-.2)
for m in [44, 56, 60, 63]:   # the snatch: an Ab-major stab
    add(music, pizz(midi(m), .8), 4.3, P * 1.1)
for t0, m in [(4.62, 57), (4.72, 59)]:   # pickup into the chase
    add(music, pizz(midi(m), .3), t0, P)

# B: the chase, driving sixteenths in A minor → F → G, then a held E-major tremolo for the leap
for t0, notes, root in [(4.8, [57, 64, 69, 64], 45), (5.4, [53, 60, 65, 60], 41), (6.0, [55, 62, 67, 62], 43)]:
    for k in range(4 if t0 < 6 else 2):
        add(music, pizz(midi(notes[k % 4]), .3), t0 + k * .15, P * .9, pan=.15)
    for k in range(2 if t0 < 6 else 1):
        add(music, bass(midi(root), .3), t0 + k * .3, BS * .8)
for k, ts in enumerate(np.arange(6.3, 6.95, .05)):   # suspense, getting louder
    add(music, pizz(midi([52, 56, 59, 64][k % 4] + 12), .2), ts, P * (.3 + .7 * k / 13))
# (silence after the landing, then the sad trombone above)

# C: sad and sparse; then the leaf motif returns as the leaf drifts down, and resolves when it lands
add(music, pad([57, 60, 64], 1.9), 9.7, .5)
add(music, pad([53, 57, 60], .75), 11.4, .5)
add(music, pad([55, 59, 62], .75), 12.0, .5)
harp_at(9.9, 45, .7)
harp_at(10.5, 52, .5)
for t0, m in [(10.6, 81), (11.05, 79), (11.5, 76), (12.0, 74)]:
    add(music, glock(midi(m)), t0, G, pan=-.2)
add(music, glock(midi(72), 2.4), 12.6, G * 1.1)          # landed: the motif resolves
harp_at(12.6, 48, .6)
# happy: a harp roll up, the motif answered in major, and a warm C chord to the end
for i, m in enumerate([48, 55, 60, 64, 67, 72, 76, 79, 84]):
    harp_at(13.55 + i * .055, m, .9)
for t0, m in [(13.65, 76), (13.8, 79), (13.95, 81), (14.15, 84)]:
    add(music, glock(midi(m)), t0, G, pan=.2)
add(music, bass(midi(36), 1.45), 13.55, BS)
add(music, pad([60, 64, 67], 1.45, .3, .5), 13.55, .6)
for i, m in enumerate([36, 48, 55, 59, 62, 64, 67]):
    harp_at(14.4 + i * .04, m, .7)

# ---------- mix ----------
def reverb(x, length=2.2, rt=2.3, pre=.015):
    t = tt(length)
    ir = np.zeros((2, len(t)))
    for c in range(2):
        ir[c] = lp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 6.9 / rt)
    ir[:, : int(pre * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    return np.stack([fftconvolve(x[c], ir[c])[:N] for c in range(2)])


out = music + reverb(music) * .35 + sfx + reverb(sfx) * .12
out[:, -int(.5 * SR):] *= np.linspace(1, 0, int(.5 * SR)) ** 2   # fade with the iris
out = hp(out, 30)
out = np.tanh(out / np.abs(out).max() * 1.2) / np.tanh(1.2) * .89   # gentle limiting, peak ≈ -1 dBFS

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'last_leaf.wav')
os.makedirs(os.path.dirname(path), exist_ok=True)
with wave.open(path, 'wb') as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((out.T * 32767).astype('<i2').tobytes())
print(f'wrote {os.path.normpath(path)}  ({DUR:.1f} s)')
for s in range(int(DUR)):
    seg_ = out[:, s * SR:(s + 1) * SR]
    print(f'{s:2d}s  rms {20 * np.log10(np.sqrt((seg_ ** 2).mean()) + 1e-9):6.1f} dB  peak {20 * np.log10(np.abs(seg_).max() + 1e-9):6.1f} dB')
