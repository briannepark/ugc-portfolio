"""Kith collage assets. Sources in site/media/pitches/shared/kith/src-*.png. Run: python3 scripts/make-kith-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'kith')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')

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

w = ld('src-wall.png'); w.copy().resize((1500, 1001), Image.LANCZOS).save(os.path.join(D, 'wall.jpg'), quality=84)
s = ld('src-shop.png'); s.resize((s.width * 2, s.height * 2), Image.LANCZOS).save(os.path.join(D, 'shop.jpg'), quality=88)

a = np.array(w); yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
finish(a, (((xx - 1850) ** 2 + (yy - 850) ** 2) < 480 ** 2).astype(np.uint8) * 255, 'cut-shelf.png', border=12, scale=0.24)
b = np.array(s); m = np.zeros(b.shape[:2], np.uint8)
cv2.fillPoly(m, [np.array([(212, 205), (248, 178), (338, 180), (360, 208), (360, 365), (212, 365)], np.int32)], 255)
finish(b, m, 'cut-pedestal.png', up=2.0, scale=0.8)
