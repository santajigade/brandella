#!/usr/bin/env python3
"""Make a branded in-article infographic (1200 px wide WebP) from a JSON spec.

Usage: python3 scripts/make_infographic.py <spec.json>
Writes public/images/infographics/<name>.webp and prints its site path.

Spec keys:
  name      file name without extension, e.g. "<slug>-1" (the script saves it as ig-<slug>-1;
            the ig- prefix matters: a body image whose name starts with the cover's name hides the featured image)
  type      "stats" | "compare" | "steps"
  title     heading shown at the top
  section   top section name (picks the accent colour, same as covers)
  source    short source line shown at the bottom, e.g. "Source: Tripadvisor Q3 2026 release"
  stats     [{"value": "$436.4M", "label": "Total revenue, down 11%"}]  (type stats, 2 to 4 items)
  headers   ["Before", "Now"]                                         (type compare)
  rows      [["old thing", "new thing"]]                              (type compare, 2 to 6 rows)
  steps     ["Step text", "..."]                                      (type steps, 3 to 7 items)

Only put facts in a spec that are in the article and come from a source opened in the run.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "scripts/fonts")
W, PAD = 1200, 64
INK, CARD, LINE = (17, 17, 17), (30, 30, 30), (48, 48, 48)
GREEN, LIME, WHITE, GREY = (108, 200, 42), (166, 239, 57), (255, 255, 255), (170, 170, 170)
ACCENTS = {
    "SEO": (108, 200, 42), "Paid Media": (10, 102, 194), "Content": (230, 140, 30),
    "Social": (214, 41, 118), "Digital Marketing": (0, 166, 153),
    "Artificial Intelligence": (124, 77, 255), "Development": (255, 196, 0),
}
DASHES = (chr(0x2013), chr(0x2014))


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, "OpenSans-%d.ttf" % weight), size)


_probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))


def wrap(text, fnt, width):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if _probe.textlength(test, font=fnt) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def text_block(d, x, y, text, fnt, width, fill, lh):
    for line in wrap(text, fnt, width):
        if d:
            d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def render(spec, d, accent):
    """Draw the body. With d=None only measure. Returns the y where the body ends."""
    kind = spec["type"]
    inner = W - 2 * PAD
    y = 0
    if kind == "stats":
        items = spec["stats"]
        n = len(items)
        cols = 2 if n == 4 else n
        gap = 24
        cw = (inner - gap * (cols - 1)) // cols
        vf, lf = font(800, 54 if cols <= 2 else 46), font(600, 24)
        row_h = 0
        for i, it in enumerate(items):
            r, c = divmod(i, cols)
            h = 40 + 70 + len(wrap(it["label"], lf, cw - 48)) * 34 + 32
            row_h = max(row_h, h)
        for i, it in enumerate(items):
            r, c = divmod(i, cols)
            x0, y0 = PAD + c * (cw + gap), r * (row_h + gap)
            if d:
                d.rounded_rectangle((x0, y0, x0 + cw, y0 + row_h), radius=16, fill=CARD)
                d.rectangle((x0, y0 + 20, x0 + 6, y0 + row_h - 20), fill=accent)
                d.text((x0 + 28, y0 + 30), it["value"], font=vf, fill=LIME)
            text_block(d, x0 + 28, y0 + 40 + 70, it["label"], lf, cw - 48, WHITE, 34)
        rows = (n + cols - 1) // cols
        y = rows * row_h + (rows - 1) * gap
    elif kind == "compare":
        heads, rows = spec["headers"], spec["rows"]
        cols = len(heads)
        cw = inner // cols
        hf, bf = font(800, 26), font(600, 24)
        if d:
            d.rounded_rectangle((PAD, 0, PAD + inner, 60), radius=12, fill=accent)
        for c, h in enumerate(heads):
            if d:
                d.text((PAD + c * cw + 24, 14), h, font=hf, fill=WHITE)
        y = 72
        for i, row in enumerate(rows):
            h = max(len(wrap(cell, bf, cw - 48)) for cell in row) * 34 + 28
            if d:
                d.rounded_rectangle((PAD, y, PAD + inner, y + h), radius=10, fill=CARD if i % 2 == 0 else INK)
                for c in range(1, cols):
                    d.line((PAD + c * cw, y + 10, PAD + c * cw, y + h - 10), fill=LINE, width=2)
            for c, cell in enumerate(row):
                text_block(d, PAD + c * cw + 24, y + 14, cell, bf, cw - 48, LIME if c == cols - 1 else WHITE, 34)
            y += h + 8
    elif kind == "steps":
        sf, nf = font(600, 26), font(800, 26)
        for i, s in enumerate(spec["steps"], 1):
            lines = wrap(s, sf, inner - 110)
            h = max(64, len(lines) * 36 + 28)
            if d:
                d.rounded_rectangle((PAD, y, PAD + inner, y + h), radius=12, fill=CARD)
                d.ellipse((PAD + 20, y + h // 2 - 22, PAD + 64, y + h // 2 + 22), fill=LIME)
                d.text((PAD + 42, y + h // 2), str(i), font=nf, fill=INK, anchor="mm")
            text_block(d, PAD + 90, y + (h - len(lines) * 36) // 2 - 2, s, sf, inner - 110, WHITE, 36)
            y += h + 12
        y -= 12
    else:
        sys.exit("unknown type: " + kind)
    return y


def main(path):
    spec = json.load(open(path))
    blob = json.dumps(spec, ensure_ascii=False)
    if any(ch in blob for ch in DASHES):
        sys.exit("FAIL: spec contains an em dash or en dash")
    accent = ACCENTS.get(spec.get("section", ""), GREEN)
    tf = font(800, 40)
    title_lines = wrap(spec["title"], tf, W - 2 * PAD)
    top = 56 + 44 + len(title_lines) * 52 + 32
    body_h = render(spec, None, accent)
    H = top + body_h + 40 + 90
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 8), fill=accent)
    kf = font(800, 20)
    label = spec.get("section", "Brandella Journal").upper()
    tw = d.textlength(label, font=kf)
    d.rounded_rectangle((PAD, 40, PAD + tw + 28, 76), radius=18, fill=LIME)
    d.text((PAD + 14, 45), label, font=kf, fill=INK)
    y = 96
    for line in title_lines:
        d.text((PAD, y), line, font=tf, fill=WHITE)
        y += 52
    body = Image.new("RGB", (W, body_h + 2), INK)
    render(spec, ImageDraw.Draw(body), accent)
    img.paste(body, (0, top))
    fy = H - 70
    d.line((PAD, fy - 18, W - PAD, fy - 18), fill=LINE, width=2)
    d.text((PAD, fy), spec.get("source", ""), font=font(600, 20), fill=GREY)
    brand = "Brandella Journal"
    d.text((W - PAD, fy), brand, font=font(800, 22), fill=GREEN, anchor="ra")
    name = spec["name"] if spec["name"].startswith("ig-") else "ig-" + spec["name"]
    out_dir = os.path.join(ROOT, "public/images/infographics")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, name + ".webp"), "WEBP", quality=86, method=6)
    print("/images/infographics/%s.webp" % name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
