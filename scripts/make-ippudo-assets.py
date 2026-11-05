"""Ippudo collage assets. Sources in site/media/pitches/shared/ippudo/src-*.png. Run: python3 scripts/make-ippudo-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'ippudo')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')
def jpg(im, name, w):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

def finish(img, mask, name, border=8, scale=1.0):
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

jpg(ld('src-room1.png'), 'room1.jpg', 1100); jpg(ld('src-room2.png'), 'room2.jpg', 1000); jpg(ld('src-store.png'), 'store.jpg', 1100)
r = np.array(ld('src-ramen.png'))                  # 2000x1500, four bowls from above
circle(r, 2160, 745, 1000, 'cut-bowl-black.png', scale=0.24)
circle(r, 900, 2310, 1000, 'cut-bowl-red.png', scale=0.24)
