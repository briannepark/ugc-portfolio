"""CJ Hendry Flower Market collage assets. Sources: /mnt attachments copied to site/media/pitches/shared/cj/src-*.png
Run: python3 scripts/make-cj-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'cj')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')

def jpg(im, name, w):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

def grab(img, rect, name, scale=1.0, border=7, iters=6, extra_bg=None):
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.grabCut(img, mask, rect, np.zeros((1, 65)), np.zeros((1, 65)), iters, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    if extra_bg is not None: m[extra_bg > 0] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    cn, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big = max(cn, key=cv2.contourArea); m = np.zeros_like(m); cv2.drawContours(m, [big], -1, 255, -1)
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

jpg(ld('src-tent.png'), 'tent.jpg', 1500); jpg(ld('src-tiers.png'), 'tiers.jpg', 1100)
jpg(ld('src-close.png').crop((0, 0, 1334, 1500)), 'close.jpg', 900)

b = np.array(ld('src-hand.png'))          # 452x678
keep = np.zeros(b.shape[:2], np.uint8)
cv2.ellipse(keep, (270, 235), (185, 175), 0, 0, 360, 255, -1)
cv2.fillPoly(keep, [np.array([(205, 330), (300, 330), (292, 560), (212, 560)], np.int32)], 255)
hx = 255 - keep
grab(b, (110, 120, 330, 560), 'cut-bouquet-hand.png', scale=1.0, extra_bg=hx)
p = np.array(ld('src-plush.png'))         # 1600x1280, crop off the watermark
wm = np.zeros(p.shape[:2], np.uint8); wm[1150:, :260] = 255
grab(p, (160, 120, 1100, 1240), 'cut-bouquet-plush.png', scale=0.38, extra_bg=wm)
