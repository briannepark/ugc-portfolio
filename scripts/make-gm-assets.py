"""Gentle Monster collage assets. Sources in site/media/pitches/shared/gm/src-*.png. Run: python3 scripts/make-gm-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'gm')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')
def jpg(im, name, w):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

def grab(img, rect, name, scale=1.0, border=7, iters=7, keep=None, minarea=2000):
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.grabCut(img, mask, rect, np.zeros((1, 65)), np.zeros((1, 65)), iters, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    if keep is not None: m = cv2.bitwise_and(m, keep)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    cn, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    m = np.zeros_like(m); cv2.drawContours(m, [c for c in cn if cv2.contourArea(c) > minarea], -1, 255, -1)
    rough = (cv2.GaussianBlur(m, (0, 0), 2) > 128).astype(np.uint8) * 255
    edge = cv2.dilate(rough, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 2 + 1,) * 2))
    H, W = m.shape; out = np.zeros((H, W, 4), np.uint8)
    inner = cv2.GaussianBlur(rough, (0, 0), 0.8).astype(np.float32) / 255
    for c in range(3): out[..., c] = (img[..., c] * inner + 250 * (1 - inner)).astype(np.uint8)
    out[..., 3] = cv2.GaussianBlur(edge, (0, 0), 0.8)
    ys, xs = np.where(edge > 0); p = 12
    im = Image.fromarray(out[max(ys.min() - p, 0):ys.max() + p, max(xs.min() - p, 0):xs.max() + p], 'RGBA')
    if scale != 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(os.path.join(D, name), optimize=True); print(name, im.size)

jpg(ld('src-shop.png'), 'shop.jpg', 1500); jpg(ld('src-door.png'), 'door.jpg', 800)
jpg(ld('src-coral.png'), 'coral.jpg', 1100)
jpg(ld('src-faces.png'), 'faces.jpg', 900); jpg(ld('src-bison.png'), 'bison.jpg', 1000)
f = np.array(ld('src-faces.png'))   # 800x533
grab(f, (85, 30, 400, 440), 'cut-faces.png', scale=0.8)
b = np.array(ld('src-bison.png'))   # 1000x675
