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


def make_image(slug, title, board, cover):
    img = Image.new("RGB", (W, H), DARK)
    top_h = 600
    if cover and os.path.exists(cover):
        c = Image.open(cover).convert("RGB")
        r = W / c.width
        ch = int(c.height * r)
        if ch >= 450:  # fit full width, no side crop
            c = c.resize((W, ch), Image.LANCZOS)
            top_h = min(ch, 760)
            y = (ch - top_h) // 2
            img.paste(c.crop((0, y, W, y + top_h)), (0, 0))
        else:
            r = max(W / c.width, top_h / c.height)
            c = c.resize((int(c.width * r) + 1, int(c.height * r) + 1), Image.LANCZOS)
            x, y = (c.width - W) // 2, (c.height - top_h) // 2
            img.paste(c.crop((x, y, x + W, y + top_h)), (0, 0))
    else:
        ImageDraw.Draw(img).rectangle([0, 0, W, top_h], fill=(36, 72, 14))
    d = ImageDraw.Draw(img)
    d.rectangle([0, top_h, W, top_h + 12], fill=GREEN)
    pad = 70
    lab = LABEL[board]
    lf = font(800, 30)
    avail_top, avail_bot = top_h + 12, H - 150
    room = avail_bot - avail_top - 70 - 58 - 40  # margins, label, gap
    for size in (78, 72, 66, 60, 54, 48, 44):
        tf = font(800, size)
        lines = wrap(d, title, tf, W - 2 * pad)
        lh = int(size * 1.22)
        if len(lines) * lh <= room:
            break
    block = 58 + 40 + len(lines) * lh
    y0 = avail_top + max(50, (avail_bot - avail_top - block) // 2)
    lw = d.textlength(lab, font=lf)
    d.rounded_rectangle([pad, y0, pad + lw + 44, y0 + 58], radius=29, fill=LIME)
    d.text((pad + 22, y0 + 5), lab, font=lf, fill=DARK)
    y = y0 + 58 + 40
    for ln in lines:
        d.text((pad, y), ln, font=tf, fill=WHITE)
        y += lh
    # footer
    d.rectangle([0, H - 150, W, H], fill=(16, 32, 7))
    d.text((pad, H - 118), "Read the full guide", font=font(600, 32), fill=SOFT)
    d.text((pad, H - 76), "brandella.in", font=font(800, 40), fill=LIME)
    bj = "BRANDELLA JOURNAL"
    bf = font(800, 26)
    d.text((W - pad - d.textlength(bj, font=bf), H - 70), bj, font=bf, fill=SOFT)
    os.makedirs(OUT_IMG, exist_ok=True)
    img.save(os.path.join(OUT_IMG, slug + ".jpg"), "JPEG", quality=78, optimize=True, progressive=True)


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
            "slug": fm(raw, "slug") or os.path.basename(f)[:-3],
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
                make_image(p["slug"], clean(p["title"]), board, cover)
                desc = clean(p["desc"] + " Read the full guide on Brandella Journal.")[:500]
                kws = ", ".join(x for x in [p["kw"], board, "Brandella Journal"] if x)
                w.writerow([clean(p["title"])[:100], "https://brandella.in/pins/%s.jpg" % p["slug"], board, "", desc,
                            "https://brandella.in/%s/" % p["slug"], "%sT%s" % (day, TIMES[n % PER_DAY]), kws])
        print(name, len(chunk))
    print("pins:", len(old))


if __name__ == "__main__":
    main()
