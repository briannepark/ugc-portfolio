"""Rok Matcha collage assets. Sources in site/media/pitches/shared/rok/src-*.png. Run: python3 scripts/make-rok-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'rok')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')

def finish(img, mask, name, border=7, scale=1.0, up=1.0):
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

ld('src-store.png').resize((1192, 670), Image.LANCZOS).save(os.path.join(D, 'store.jpg'), quality=86)

c = np.array(ld('src-cup.png'))                      # whisk + iced cup on a plain wall
mask = np.zeros(c.shape[:2], np.uint8)
cv2.grabCut(c, mask, (70, 0, 250, 420), np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_RECT)
m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
cn, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
m = np.zeros_like(m); cv2.drawContours(m, [max(cn, key=cv2.contourArea)], -1, 255, -1)
finish(c, m, 'cut-cup.png', up=2.0, scale=0.85)

s = np.array(ld('src-store.png'))                    # round snip of the entrance
yy, xx = np.mgrid[0:s.shape[0], 0:s.shape[1]]
finish(s, (((xx - 330) ** 2 + (yy - 215) ** 2) < 120 ** 2).astype(np.uint8) * 255, 'cut-door.png', border=9, up=2.0, scale=0.7)
