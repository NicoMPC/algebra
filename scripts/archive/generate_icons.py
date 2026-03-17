#!/usr/bin/env python3
"""Génère les icônes PWA Matheux — carré indigo #4338ca avec "M" blanc."""
import os, sys

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

os.makedirs('icons', exist_ok=True)

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
COLOR = (67, 56, 202)   # #4338ca
WHITE = (255, 255, 255)

def make_icon(size, padding_ratio=0.0, out_path=None):
    img = Image.new('RGBA', (size, size), COLOR)
    draw = ImageDraw.Draw(img)
    pad = int(size * padding_ratio)
    # Carré intérieur (pour maskable, fond plein avec padding safe zone)
    if padding_ratio > 0:
        draw.rectangle([pad, pad, size-pad-1, size-pad-1], fill=COLOR)
    # Texte "M"
    font_size = int((size - 2*pad) * 0.55)
    font = None
    if HAS_PILLOW:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        except Exception:
            try:
                font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationSans-Bold.ttf', font_size)
            except Exception:
                font = ImageFont.load_default()
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), 'M', font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), 'M', fill=WHITE, font=font)
    img.save(out_path or f'icons/icon-{size}.png')
    print(f'  ✓ {out_path or f"icons/icon-{size}.png"}')

if not HAS_PILLOW:
    print('⚠ Pillow absent — génération d\'icônes 1×1 de remplacement')
    # Icône PNG 1×1 minimale valide
    PNG_1X1 = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x4f'
        b'\x43\x07\x00\x00\x19\x01\x05\x18\xd5N\xa1\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    for s in SIZES:
        p = f'icons/icon-{s}.png'
        open(p, 'wb').write(PNG_1X1)
        print(f'  ✓ {p} (placeholder)')
    for name in ['icon-maskable-512.png', 'apple-touch-icon.png', 'favicon-32.png']:
        open(f'icons/{name}', 'wb').write(PNG_1X1)
        print(f'  ✓ icons/{name} (placeholder)')
    print('\n⚠ ICÔNES PLACEHOLDER — remplacer par des vraies icônes avant le lancement')
    sys.exit(0)

print('Génération des icônes PWA Matheux...')
for s in SIZES:
    make_icon(s)

make_icon(512, padding_ratio=0.2, out_path='icons/icon-maskable-512.png')
make_icon(180, out_path='icons/apple-touch-icon.png')
make_icon(32,  out_path='icons/favicon-32.png')

print('\n✅ Toutes les icônes générées dans icons/')
