#!/usr/bin/env python3
"""Make 1000x1500 Pinterest pin images for older posts and Pinterest bulk upload CSVs.

Images: public/pins/<slug>.jpg (served at https://brandella.in/pins/<slug>.jpg)
CSVs:   pinterest/pins-01_<start>_to_<end>.csv ... (14 days x 4 pins = 56 rows per file,
        because Pinterest only accepts publish dates within the next 14 days)

Posts in the 50 newest (already in rss.xml, auto pinned from the feed) are skipped.
Order: most viewed first.

Usage: python3 scripts/make_pins.py --start 2026-11-18
"""
import argparse, csv, datetime, glob, json, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "scripts/fonts")
OUT_IMG = os.path.join(ROOT, "public/pins")
OUT_CSV = os.path.join(ROOT, "pinterest")
W, H = 1000, 1500
DARK, GREEN, LIME, WHITE, SOFT = (24, 48, 10), (108, 200, 42), (166, 239, 57), (255, 255, 255), (227, 240, 216)
TIMES = ["09:30:00", "13:30:00", "17:30:00", "20:30:00"]
PER_DAY, DAYS_PER_FILE = 4, 14

BOARDS = {
    "SEO Tips and Strategies": ["seo", "technical-seo", "link-building", "local-seo", "seo-tools", "google-search-console",
                                "mobile-seo", "seo-basics", "off-page-seo", "keyword-research", "on-page-seo", "core-web-vitals"],
    "Google Ads and PPC": ["google-ads", "paid-media", "ppc-strategy", "paid-media-analytics", "display-advertising",
                           "linkedin-ads", "meta-ads", "gtm"],
    "AI in Marketing": ["artificial-intelligence"],
    "Digital Marketing and Content": ["digital-marketing", "content", "social"],
    "Web Development Tips": ["development", "javascript", "html", "html_css", "php"],
}
BOARD_OF = {c: b for b, cs in BOARDS.items() for c in cs}
LABEL = {"SEO Tips and Strategies": "SEO", "Google Ads and PPC": "GOOGLE ADS AND PPC", "AI in Marketing": "AI IN MARKETING",
         "Digital Marketing and Content": "DIGITAL MARKETING", "Web Development Tips": "WEB DEVELOPMENT"}


def font(w, s):
    return ImageFont.truetype(os.path.join(FONTS, "OpenSans-%d.ttf" % w), s)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def clean(t):
    return re.sub(r"\s+", " ", t.replace("\u2014", ", ").replace("\u2013", " to ")).replace(" ,", ",").strip()


def fm(raw, key):
    m = re.search(r'^%s:\s*(.*)$' % key, raw, re.M)
    if not m:
        return ""
    v = m.group(1).strip().rstrip("\r")
    if v.startswith('"'):
        try:
            return json.loads(v)
        except Exception:
            return v.strip('"')
    return v


ACCENT = {"SEO Tips and Strategies": (166, 239, 57), "Google Ads and PPC": (255, 184, 48), "AI in Marketing": (176, 150, 255),
          "Digital Marketing and Content": (255, 128, 96), "Web Development Tips": (80, 200, 250)}
SKIP_H = re.compile(r"faq|frequently|learn today|watch|score|workflow|stepper|calculator|generator|quiz|related|continue|"
                    r"build a complete|common questions|glossary|key terms|try it|conclusion|summary|final|checklist$", re.I)


def headings(path):
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<(script|style)\b.*?</\1>", "", raw, flags=re.S | re.I)
    hs = re.findall(r"<h2\b[^>]*>(.*?)</h2>", raw, re.S | re.I) or re.findall(r"(?m)^##\s+(.+)$", raw)
    out = []
    for h in hs:
        h = clean(re.sub(r"<[^>]+>", "", h))
        h = re.sub(r"^(\d{1,2}[.):]?\s+|step\s*\d+\s*[:.]\s*|tip\s*\d+\s*[:.]\s*)", "", h, flags=re.I)
        h = re.sub(r"\s*\(.*?\)\s*$", "", h).strip(" :")
        if not h or SKIP_H.search(h) or len(h) > 62 or h.lower() in (x.lower() for x in out):
            continue
        out.append(h)
        if len(out) == 4:
            break
    return out


def number_badge(title):
    m = re.search(r"\b(\d{1,2})\s+(proven|essential|ways|steps|tips|mistakes|best|simple|easy|key|rules|properties|picks|ai)\b", title, re.I)
    return m.group(1) if m else None


def make_image(slug, title, board, cover, items=(), style=0, fallback=""):
    acc = ACCENT[board]
    if style == 0:      # dark
        bg, ink, sub, chip_bg, chip_ink, panel = (14, 30, 8), (255, 255, 255), (205, 228, 190), acc, (14, 30, 8), (26, 50, 14)
    elif style == 1:    # light
        bg, ink, sub, chip_bg, chip_ink, panel = (246, 250, 240), (17, 24, 12), (70, 86, 60), (14, 30, 8), acc, (255, 255, 255)
    else:               # accent band
        bg, ink, sub, chip_bg, chip_ink, panel = (20, 22, 26), (255, 255, 255), (210, 214, 220), (255, 255, 255), (20, 22, 26), (34, 37, 44)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    pad = 72
    # decorative shapes
    if style == 2:
        ink_top, chip_bg, chip_ink = (20, 22, 26), (20, 22, 26), acc
    else:
        ink_top = ink
        d.ellipse([W - 330, -170, W + 170, 330], outline=acc, width=14)
        d.ellipse([W - 230, -70, W + 70, 230], outline=acc, width=6)
        d.rectangle([0, 0, 18, H], fill=acc)
    # chip + kicker
    lab, lf = LABEL[board], font(800, 28)
    lw = d.textlength(lab, font=lf)
    d.rounded_rectangle([pad, 90, pad + lw + 44, 146], radius=28, fill=chip_bg)
    d.text((pad + 22, 96), lab, font=lf, fill=chip_ink)
    nb = number_badge(title)
    # title
    title_top = 190
    maxw = W - 2 * pad - (0 if style == 2 else 40)
    title_room = 470
    for size in (84, 76, 70, 64, 58, 52, 48):
        tf = font(800, size)
        lines = wrap(d, title, tf, maxw)
        lh = int(size * 1.18)
        if len(lines) * lh <= title_room:
            break
    if style == 2:
        d.rectangle([0, 0, W, title_top + len(lines) * lh + 70], fill=acc)
        d.rounded_rectangle([pad, 90, pad + lw + 44, 146], radius=28, fill=chip_bg)
        d.text((pad + 22, 96), lab, font=lf, fill=chip_ink)
    y = title_top
    for ln in lines:
        d.text((pad, y), ln, font=tf, fill=ink_top if style == 2 else ink)
        y += lh
    y = y + (120 if style == 2 else 60)
    # inside this guide panel
    rows = []
    if items:
        pf, it, LH, GAP = font(800, 32), font(600, 42), 54, 34
        rows = [wrap(d, t, it, W - 2 * pad - 130)[:2] for t in items]
        def height(rs): return 100 + sum(len(r) * LH + GAP for r in rs) + 10
        bottom = H - 200
        while rows and y + height(rows) > bottom:
            rows = rows[:-1]
        if len(rows) >= 2:
            ph = height(rows)
            y = y + max(0, (bottom - y - ph) // 2)
            d.rounded_rectangle([pad - 10, y, W - pad + 10, y + ph], radius=28, fill=panel)
            d.text((pad + 28, y + 32), "WHAT'S INSIDE", font=pf, fill=acc if style != 1 else (40, 90, 10))
            yy = y + 100
            for i, r in enumerate(rows, 1):
                d.ellipse([pad + 26, yy + 2, pad + 78, yy + 54], fill=acc)
                nf = font(800, 30)
                nw = d.textlength(str(i), font=nf)
                d.text((pad + 52 - nw / 2, yy + 7), str(i), font=nf, fill=(14, 30, 8))
                for ln in r:
                    d.text((pad + 102, yy), ln, font=it, fill=ink if style != 1 else (17, 24, 12))
                    yy += LH
                yy += GAP
    if not items or len(rows) < 2:
        desc = clean(fallback or "")
        if desc:
            qf = font(600, 44)
            lines2 = wrap(d, desc, qf, W - 2 * pad - 60)[:7]
            ph = 110 + len(lines2) * 60 + 30
            bottom = H - 200
            y = y + max(0, (bottom - y - ph) // 2)
            d.rounded_rectangle([pad - 10, y, W - pad + 10, y + ph], radius=28, fill=panel)
            d.text((pad + 28, y + 32), "IN THIS GUIDE", font=font(800, 32), fill=acc if style != 1 else (40, 90, 10))
            yy = y + 100
            for ln in lines2:
                d.text((pad + 28, yy), ln, font=qf, fill=ink if style != 1 else (17, 24, 12))
                yy += 60
    # number badge
    if nb and style != 2 and not items:
        bf = font(800, 120)
        d.text((W - pad - d.textlength(nb, font=bf), H - 360), nb, font=bf, fill=acc)
    # footer
    d.line([pad, H - 170, W - pad, H - 170], fill=acc, width=4)
    d.text((pad, H - 140), "Free guide at", font=font(600, 32), fill=sub)
    d.text((pad, H - 96), "brandella.in", font=font(800, 46), fill=acc if style != 1 else (40, 110, 10))
    bj, bf2 = "BRANDELLA JOURNAL", font(800, 26)
    d.text((W - pad - d.textlength(bj, font=bf2), H - 84), bj, font=bf2, fill=sub)
    os.makedirs(OUT_IMG, exist_ok=True)
    img.save(os.path.join(OUT_IMG, slug + ".jpg"), "JPEG", quality=86, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="first publish day, YYYY-MM-DD")
    a = ap.parse_args()
    posts = []
    for f in glob.glob(os.path.join(ROOT, "src/content/posts/*.md")):
        raw = open(f, encoding="utf-8").read(6000)
        if re.search(r"^draft:\s*true", raw, re.M):
            continue
        posts.append({
            "slug": fm(raw, "slug") or os.path.basename(f)[:-3], "file": os.path.basename(f),
            "title": fm(raw, "title"), "desc": fm(raw, "description"), "kw": fm(raw, "focusKeyword"),
            "cat": fm(raw, "primaryCategory"), "date": fm(raw, "date"), "image": fm(raw, "image"),
            "views": int(re.sub(r"\D", "", fm(raw, "views") or "0") or 0),
        })
    newest = {p["slug"] for p in sorted(posts, key=lambda p: p["date"], reverse=True)[:50]}
    old = [p for p in posts if p["slug"] not in newest]
    old.sort(key=lambda p: (-p["views"], p["slug"]))
    start = datetime.date.fromisoformat(a.start)
    os.makedirs(OUT_CSV, exist_ok=True)
    for f in glob.glob(os.path.join(OUT_CSV, "pins-*.csv")):
        os.remove(f)
    per_file = PER_DAY * DAYS_PER_FILE
    head = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
    for fi in range(0, len(old), per_file):
        chunk = old[fi:fi + per_file]
        d0 = start + datetime.timedelta(days=(fi // PER_DAY))
        d1 = d0 + datetime.timedelta(days=(len(chunk) - 1) // PER_DAY)
        name = "pins-%02d_upload-on-%s_runs-%s-to-%s.csv" % (fi // per_file + 1, d0, d0, d1)
        with open(os.path.join(OUT_CSV, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, quoting=csv.QUOTE_ALL)
            w.writerow(head)
            for i, p in enumerate(chunk):
                n = fi + i
                day = start + datetime.timedelta(days=n // PER_DAY)
                board = BOARD_OF.get(p["cat"], "Digital Marketing and Content")
                cover = os.path.join(ROOT, "public", p["image"].lstrip("/")) if p["image"] else ""
                items = headings(os.path.join(ROOT, "src/content/posts", p["file"]))
                make_image(p["slug"], clean(p["title"]), board, cover, items, n % 3, p["desc"])
                desc = clean(p["desc"] + " Read the full guide on Brandella Journal.")[:500]
                kws = ", ".join(x for x in [p["kw"], board, "Brandella Journal"] if x)
                w.writerow([clean(p["title"])[:100], "https://brandella.in/pins/%s.jpg" % p["slug"], board, "", desc,
                            "https://brandella.in/%s/" % p["slug"], "%sT%s" % (day, TIMES[n % PER_DAY]), kws])
        print(name, len(chunk))
    print("pins:", len(old))


if __name__ == "__main__":
    main()
