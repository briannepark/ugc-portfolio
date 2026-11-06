"""Aura reading collage assets. Source: site/media/pitches/shared/aura/src-cards.png. Run: python3 scripts/make-aura-assets.py"""
import os, numpy as np, cv2
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', 'site', 'media', 'pitches', 'shared', 'aura')
img = np.array(Image.open(os.path.join(D, 'src-cards.png')).convert('RGB'))
Image.fromarray(img).resize((1200, 900), Image.LANCZOS).save(os.path.join(D, 'cards.jpg'), quality=86)

def finish(img, mask, name, border=8, scale=1.0, up=2.0):
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

def quad(pts):
    m = np.zeros(img.shape[:2], np.uint8); cv2.fillPoly(m, [np.array(pts, np.int32)], 255); return m
finish(img, quad([(25, 45), (285, 28), (318, 340), (80, 428)]), 'cut-card-blue.png', scale=0.7)
finish(img, quad([(318, 42), (578, 48), (552, 378), (312, 392)]), 'cut-card-red.png', scale=0.7)
