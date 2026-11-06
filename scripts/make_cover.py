#!/usr/bin/env python3
"""Make a branded 1200x675 WebP cover image for a post.

Usage: python3 scripts/make_cover.py <slug> "<headline>" "<category name>"
Writes public/images/covers/<slug>.webp and prints its site path.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "scripts/fonts")
W, H = 1200, 675
INK, GREEN, LIME, WHITE = (17, 17, 17), (108, 200, 42), (166, 239, 57), (255, 255, 255)

# a different accent glow per section so covers do not all look the same
ACCENTS = {
    "SEO": (108, 200, 42), "Paid Media": (10, 102, 194), "Content": (230, 140, 30),
    "Social": (214, 41, 118), "Digital Marketing": (0, 166, 153),
    "Artificial Intelligence": (124, 77, 255), "Development": (255, 196, 0),
}


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, "OpenSans-%d.ttf" % weight), size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main(slug, headline, category, section=None):
    accent = ACCENTS.get(section or category, GREEN)
    img = Image.new("RGB", (W, H), INK)
    glow = Image.new("RGB", (W, H), INK)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W - 520, -380, W + 380, 420), fill=accent)
    gd.ellipse((-300, H - 160, 260, H + 300), fill=(40, 40, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)

    # grid texture
    for x in range(0, W, 48):
        d.line((x, 0, x, H), fill=(28, 28, 28), width=1)
    for y in range(0, H, 48):
        d.line((0, y, W, y), fill=(28, 28, 28), width=1)

    pad = 72
    kick = font(800, 26)
    label = category.upper()
    tw = d.textlength(label, font=kick)
    d.rounded_rectangle((pad, 70, pad + tw + 36, 70 + 46), radius=23, fill=LIME)
    d.text((pad + 18, 70 + 7), label, font=kick, fill=INK)

    size = 66
    while size > 40:
        fnt = font(800, size)
        lines = wrap(d, headline, fnt, W - 2 * pad)
        if len(lines) <= 4:
            break
        size -= 4
    lh = int(size * 1.22)
    y = 150 + (4 - len(lines)) * lh // 3
    for line in lines[:4]:
        d.text((pad, y), line, font=fnt, fill=WHITE)
        y += lh

    # footer: logo mark and name
    by = H - 96
    d.line((pad, by - 22, pad + 120, by - 22), fill=GREEN, width=6)
    d.rounded_rectangle((pad, by, pad + 48, by + 48), radius=11, fill=GREEN)
    d.text((pad + 24, by + 22), "B", font=font(800, 34), fill=WHITE, anchor="mm")
    d.ellipse((pad + 37, by + 37, pad + 45, by + 45), fill=LIME)
    d.text((pad + 64, by + 6), "Brandella", font=font(800, 30), fill=WHITE)
    bw = d.textlength("Brandella ", font=font(800, 30))
    d.text((pad + 64 + bw, by + 6), "Journal", font=font(600, 30), fill=GREEN)

    out_dir = os.path.join(ROOT, "public/images/covers")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, slug + ".webp"), "WEBP", quality=84, method=6)
    print("/images/covers/%s.webp" % slug)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
