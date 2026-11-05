"""Printemps collage assets. Sources in site/media/pitches/shared/printemps/src-*.png. Run: python3 scripts/make-printemps-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'printemps')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')
def jpg(im, name, w):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

def finish(img, mask, name, border=8, scale=1.0, up=1.0):
    if up != 1:
        img = cv2.resize(img, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC); mask = cv2.resize(mask, None, fx=up, fy=up, interpolation=cv2.INTER_NEAREST)
    rough = (cv2.GaussianBlur(mask, (0, 0), 2) > 128).astype(np.uint8) * 255
    edge = cv2.dilate(rough, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 2 + 1,) * 2))
    H, W = mask.shape; out = np.zeros((H, W, 4), np.uint8)
    inner = cv2.GaussianBlur(rough, (0, 0), 0.8).astype(np.float32) / 255
    for c in range(3): out[..., c] = (img[..., c] * inner + 250 * (1 - inner)).astype(np.uint8)
    out[..., 3] = cv2.GaussianBlur(edge, (0, 0), 0.8)
    ys, xs = np.where(edge > 0); p = 10
    im = Image.fromarray(out[max(ys.min() - p, 0):ys.max() + p, max(xs.min() - p, 0):xs.max() + p], 'RGBA')
    if scale != 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(os.path.join(D, name), optimize=True); print(name, im.size)

def circle(img, cx, cy, r, name, **kw):
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    finish(img, (((xx - cx) ** 2 + (yy - cy) ** 2) < r * r).astype(np.uint8) * 255, name, **kw)

jpg(ld('src-beauty.png'), 'beauty.jpg', 1500); jpg(ld('src-hall.png'), 'hall.jpg', 1100)
jpg(ld('src-door.png'), 'door.jpg', 900); jpg(ld('src-lounge.png'), 'lounge.jpg', 800)

d = np.array(ld('src-door.png'))                    # 1494x2000 art-deco entrance, cut along the door + steps
m = np.zeros(d.shape[:2], np.uint8)
cv2.fillPoly(m, [np.array([(540, 580), (750, 565), (935, 600), (940, 1420), (1175, 1655), (1175, 1705), (285, 1705), (285, 1655), (505, 1420)], np.int32)], 255)
finish(d, m, 'cut-door.png', scale=0.34)
h = np.array(ld('src-hall.png'))                     # 1024x768, lantern lamp
circle(h, 830, 240, 150, 'cut-lamp.png', border=9, up=2.0, scale=0.55)
b = np.array(ld('src-beauty.png'))                   # 3600x2483, pedestal of gold boxes
circle(b, 1870, 1640, 620, 'cut-beauty.png', border=12, scale=0.24)
