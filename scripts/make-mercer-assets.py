"""Mercer Labs collage assets. Sources in site/media/pitches/shared/mercer/src-*.png. Run: python3 scripts/make-mercer-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'mercer')
ld = lambda n: Image.open(os.path.join(D, n)).convert('RGB')
def jpg(im, name, w):
    im = im.copy(); im.thumbnail((w, w)); im.save(os.path.join(D, name), quality=84)

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

for src, dst, w in [('src-cave', 'cave.jpg', 900), ('src-room', 'room.jpg', 1000), ('src-robot', 'robot.jpg', 1000)]:
    jpg(ld(src + '.png'), dst, w)

e = np.array(ld('src-ext.png'))                      # 399x501 building facade, torn top-left corner
m = np.zeros(e.shape[:2], np.uint8)
cv2.fillPoly(m, [np.array([(0, 30), (60, 12), (120, 0), (300, 0), (399, 14), (399, 398), (0, 404)], np.int32)], 255)
finish(e, m, 'cut-exterior.png', up=2.0, scale=0.8)

n = np.array(ld('src-neon.png'))                     # 670x504 mirrored neon room, round sticker
yy, xx = np.mgrid[0:n.shape[0], 0:n.shape[1]]
c = (((xx - 335) ** 2 + (yy - 250) ** 2) < 235 ** 2).astype(np.uint8) * 255
finish(n, c, 'cut-neon.png', border=9, up=1.5, scale=0.7)

r = np.array(ld('src-room.png'))                     # 839x1024 flower room, round sticker
yy, xx = np.mgrid[0:r.shape[0], 0:r.shape[1]]
c = (((xx - 420) ** 2 + (yy - 330) ** 2) < 240 ** 2).astype(np.uint8) * 255
finish(r, c, 'cut-tunnel.png', border=11, up=1.0, scale=0.9)
