#!/usr/bin/env python3
"""Render icon-192.png, icon-512.png, favicon.ico and og-default.png from the SVGs."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
fav = open(os.path.join(PUB, "favicon.svg")).read()
logo = open(os.path.join(PUB, "logo.svg")).read()
og = f"""<html><body style="margin:0;width:1200px;height:630px;background:#111;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box;font-family:sans-serif;background-image:radial-gradient(circle at 100% 0,rgba(166,239,57,.35),transparent 55%)">
<div style="background:#fff;border-radius:18px;padding:26px 34px;display:inline-block;align-self:flex-start">{logo.replace('width="286" height="44"','width="572" height="88"')}</div>
<div style="color:#fff;font-size:44px;font-weight:700;margin-top:44px;line-height:1.3">SEO, paid media, AI search and<br>web development, explained.</div>
<div style="width:120px;height:8px;background:#6cc82a;border-radius:4px;margin-top:34px"></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for size in (192, 512):
        pg = b.new_page(viewport={"width": size, "height": size})
        pg.set_content(f'<html><body style="margin:0">{fav.replace("<svg ", f"<svg width={size} height={size} ")}</body></html>')
        pg.screenshot(path=os.path.join(PUB, f"icon-{size}.png"), omit_background=True)
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(og)
    pg.screenshot(path=os.path.join(PUB, "og-default.png"))
    b.close()
Image.open(os.path.join(PUB, "icon-192.png")).save(os.path.join(PUB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("icons done")
