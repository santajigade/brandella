#!/usr/bin/env python3
"""Make 640px wide WebP thumbnails in public/thumbs/ for every image in public/wp-content/uploads/."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public/wp-content/uploads")
DST = os.path.join(ROOT, "public/thumbs")
made = 0
for dirpath, _, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
            continue
        src = os.path.join(dirpath, f)
        rel = os.path.relpath(src, SRC)
        dst = os.path.join(DST, os.path.splitext(rel)[0] + ".webp")
        if os.path.exists(dst):
            continue
        try:
            im = Image.open(src)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            if im.width > 640:
                im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im.save(dst, "WEBP", quality=78, method=6)
            made += 1
        except Exception as e:  # noqa: BLE001
            print("skip", rel, e)
print("thumbnails made:", made)
