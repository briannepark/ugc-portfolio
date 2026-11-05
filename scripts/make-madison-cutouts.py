"""Cut the Madison Square Park photos into collage pieces (paper-edge cut-outs).
Sources live in site/media/pitches/nomad/madison/src-*.png. Outputs are PNGs with
alpha + a thin white paper edge. Run: python3 scripts/make-madison-cutouts.py
"""
import os, numpy as np, cv2
from PIL import Image, ImageFilter

D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'nomad', 'madison')
wide = np.array(Image.open(os.path.join(D, 'src-wide.png')).convert('RGB'))
tall = np.array(Image.open(os.path.join(D, 'src-tall.png')).convert('RGB'))


def hsv(a):
    return cv2.cvtColor(a, cv2.COLOR_RGB2HSV)  # H 0-179


def finish(img, mask, name, border=7, pad=14, scale=1.0):
    """img RGB, mask uint8 0/255 -> RGBA PNG with white paper edge, cropped."""
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    # drop tiny islands
    n, lab, st, _ = cv2.connectedComponentsWithStats((mask > 0).astype(np.uint8), 8)
    keep = np.zeros_like(mask)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 900:
            keep[lab == i] = 255
    mask = keep
    # roughen the edge a little so it reads as hand-cut scissors
    rough = cv2.GaussianBlur(mask, (0, 0), 2.2)
    rough = (rough > 128).astype(np.uint8) * 255
    edge = cv2.dilate(rough, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 2 + 1, border * 2 + 1)))
    H, W = mask.shape
    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = 250
    out[..., 3] = cv2.GaussianBlur(edge, (0, 0), 0.8)
    inner = cv2.GaussianBlur(rough, (0, 0), 0.8).astype(np.float32) / 255
    for c in range(3):
        out[..., c] = (img[..., c] * inner + 250 * (1 - inner)).astype(np.uint8)
    ys, xs = np.where(edge > 0)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, H), max(xs.min() - pad, 0), min(xs.max() + pad, W)
    im = Image.fromarray(out[y0:y1, x0:x1], 'RGBA')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(os.path.join(D, name), optimize=True)
    print(name, im.size)


def solid(m, k=31):
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = np.zeros_like(m)
    cv2.drawContours(out, [c for c in cnts if cv2.contourArea(c) > 2500], -1, 255, -1)
    return out


def poly(shape, pts):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 255)
    return m


# ---- tall photo (906x1212): sky = bright blue
h = hsv(tall)
sky = ((h[..., 0] > 95) & (h[..., 0] < 125) & (h[..., 1] > 60)).astype(np.uint8) * 255
sky = cv2.morphologyEx(sky, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
notsky = 255 - sky

# 2) fountain basin with its railing and plants (+ jet)
fount = poly(tall.shape, [(20, 800), (60, 700), (200, 660), (330, 700), (390, 640), (430, 560), (470, 560), (500, 640), (560, 690), (700, 670), (830, 720), (885, 800),
                          (895, 880), (780, 950), (560, 965), (300, 965), (110, 930), (22, 880)])
finish(tall, fount, 'cut-fountain.png', scale=0.8)

# 3) the Flatiron-ish tower + sunburst trees only (tight crop of the tall building)
tower = poly(tall.shape, [(380, 280), (470, 280), (560, 290), (562, 600), (380, 600)])
finish(tall, cv2.bitwise_and(notsky, tower), 'cut-tower.png', scale=0.9)

# ---- wide photo (1024x576): foliage by hue
h = hsv(wide)
green = ((h[..., 0] > 28) & (h[..., 0] < 75) & (h[..., 1] > 55) & (h[..., 2] > 40)).astype(np.uint8) * 255
# left canopy
left = poly(wide.shape, [(0, 170), (60, 180), (200, 205), (330, 290), (385, 420), (380, 576), (0, 576)])
finish(wide, solid(cv2.bitwise_and(green, left)), 'cut-tree-left.png', scale=0.85)
# bright tree on the right
right = poly(wide.shape, [(575, 190), (680, 120), (860, 95), (1000, 140), (1024, 250), (1000, 390), (640, 400), (575, 330)])
finish(wide, solid(cv2.bitwise_and(green, right), 41), 'cut-tree-right.png', scale=0.85)

# round snip of the fountain + flower bed (a "circle sticker" from the wide photo)
yy, xx = np.mgrid[0:576, 0:1024]
circle = (((xx - 520) ** 2 + (yy - 385) ** 2) < 150 ** 2).astype(np.uint8) * 255
finish(wide, circle, 'cut-circle.png', border=9, scale=0.8)

# the full wide photo, used as a torn "print" backdrop
Image.fromarray(wide).convert('RGB').save(os.path.join(D, 'wide.jpg'), quality=86)
t = Image.fromarray(tall).convert('RGB')
t = t.crop((0, 0, 906, 1120))  # crop off the photographer's watermark
t.save(os.path.join(D, 'tall.jpg'), quality=86)
