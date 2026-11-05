"""Chelsea galleries collage assets: resized prints + colour-keyed cut-outs.
Sources: site/media/pitches/nomad/chelsea/src-*.png. Run: python3 scripts/make-chelsea-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'nomad', 'chelsea')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')

def jpg(im, name, w=1600):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

def solid(m, k=15, minarea=1500):
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    cn, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    o = np.zeros_like(m); cv2.drawContours(o, [c for c in cn if cv2.contourArea(c) > minarea], -1, 255, -1); return o

def poly(shape, pts):
    m = np.zeros(shape[:2], np.uint8); cv2.fillPoly(m, [np.array(pts, np.int32)], 255); return m

def finish(img, mask, name, border=6, pad=12, scale=1.0):
    rough = (cv2.GaussianBlur(mask, (0, 0), 1.8) > 128).astype(np.uint8) * 255
    edge = cv2.dilate(rough, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 2 + 1, border * 2 + 1)))
    H, W = mask.shape; out = np.zeros((H, W, 4), np.uint8)
    inner = cv2.GaussianBlur(rough, (0, 0), 0.8).astype(np.float32) / 255
    for c in range(3): out[..., c] = (img[..., c] * inner + 250 * (1 - inner)).astype(np.uint8)
    out[..., 3] = cv2.GaussianBlur(edge, (0, 0), 0.8)
    ys, xs = np.where(edge > 0)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, H), max(xs.min() - pad, 0), min(xs.max() + pad, W)
    im = Image.fromarray(out[y0:y1, x0:x1], 'RGBA')
    if scale != 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(os.path.join(D, name), optimize=True); print(name, im.size)

for src, dst, w in [('src-ext', 'ext.jpg', 1500), ('src-eve', 'eve.jpg', 1000), ('src-night', 'night.jpg', 1000), ('src-branches', 'branches.jpg', 1500),
                    ('src-kaws', 'kaws.jpg', 1000), ('src-koons', 'koons.jpg', 1000), ('src-paint', 'paint.jpg', 1000)]:
    jpg(ld(src + '.png'), dst, w)

# Koons balloon Venus: magenta
k = np.array(ld('src-koons.png')); h = cv2.cvtColor(k, cv2.COLOR_RGB2HSV)
mag = (((h[..., 0] > 150) | (h[..., 0] < 6)) & (h[..., 1] > 70) & (h[..., 2] > 40)).astype(np.uint8) * 255
mag = cv2.bitwise_and(mag, poly(k.shape, [(60, 70), (300, 70), (300, 480), (60, 480)]))
finish(k, solid(mag, 21, 4000), 'cut-koons.png', scale=1.4)

# KAWS companion: lime yellow
w = np.array(ld('src-kaws.png')); h = cv2.cvtColor(w, cv2.COLOR_RGB2HSV)
yel = ((h[..., 0] > 22) & (h[..., 0] < 50) & (h[..., 1] > 110) & (h[..., 2] > 120)).astype(np.uint8) * 255
yel = cv2.bitwise_and(yel, poly(w.shape, [(290, 130), (440, 130), (440, 380), (290, 380)]))
finish(w, solid(yel, 15, 1500), 'cut-kaws.png', scale=1.8)

