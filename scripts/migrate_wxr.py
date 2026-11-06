#!/usr/bin/env python3
"""Convert the brandella.in WordPress export (WXR) into Astro content files.

Usage: python3 scripts/migrate_wxr.py path/to/export.xml

Writes:
  src/content/posts/<slug>.md   (front matter + HTML body)
  src/content/pages/<slug>.md
  src/data/categories.json      (category tree with descriptions)
  src/data/authors.json
  scripts/wp_images.txt         (every /wp-content/uploads/ file actually used)

Source of truth per post:
  * Elementor builder posts: the Elementor widget HTML (keeps BX FORMAT
    classes, styles and scripts intact).
  * Classic posts: post_content, cleaned and run through a safe wpautop.
"""
import html as htmllib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from category_descriptions import DESCRIPTIONS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
}
KEEP_PAGES = {"about-us", "contact-page", "privacy-policy", "terms-and-conditions", "disclaimer"}
GENERIC_HEADINGS = {"conclusion", "final takeaway", "final takeaways", "final thoughts",
                    "summary", "wrapping up", "in conclusion", "the bottom line"}
CANONICAL_AUTHOR = "santajigade"

BLOCK_TAGS = ("h1|h2|h3|h4|h5|h6|ul|ol|li|table|thead|tbody|tfoot|tr|td|th|blockquote|pre|div|"
              "figure|figcaption|p|iframe|hr|section|style|script|form|details|summary|dl|dt|dd|"
              "nav|aside|header|footer|article|svg|select|option|caption|colgroup|col|button|ins|link|noscript")
BLOCK_START = re.compile(r"^\s*</?(%s)[\s>/]" % BLOCK_TAGS, re.I)
BLOCK_END = re.compile(r"</(%s)>\s*$|<(hr|br|img|link)[^>]*/?>\s*$" % BLOCK_TAGS, re.I)


def t(el, path):
    return el.findtext(path, namespaces=NS) or ""


def meta_of(item):
    return {t(m, "wp:meta_key"): t(m, "wp:meta_value") for m in item.findall("wp:postmeta", NS)}


def slugify(text):
    text = htmllib.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:70] or "section"


# ---------------------------------------------------------------- helpers
PROTECT = re.compile(r"(<(script|style|pre|textarea)\b.*?</\2>)", re.S | re.I)


def protect(html, fn):
    """Apply fn only outside <script>, <style>, <pre>, <textarea> blocks."""
    parts = PROTECT.split(html)
    out = []
    i = 0
    while i < len(parts):
        out.append(fn(parts[i]))
        if i + 1 < len(parts):
            out.append(parts[i + 1])
        i += 3
    return "".join(out)


LINK_FIXES = json.load(open(os.path.join(ROOT, "scripts/link_fixes.json")))


def rewrite_urls(html):
    html = re.sub(r"https?://(www\.)?brandella\.in/wp-content/uploads/", "/wp-content/uploads/", html)
    html = re.sub(r'(href=["\'])https?://(www\.)?brandella\.in/', r"\1/", html)

    def fix(m):
        slug = m.group(2)
        if slug in LINK_FIXES:
            return '%s/%s/%s' % (m.group(1), LINK_FIXES[slug], m.group(3))
        return m.group(0)
    # internal links to slugs that never existed: point them at the real article
    html = re.sub(r'(href=["\'])/([^"\'#?/]+)/?([#?"\'])', fix, html)
    return html


def strip_srcset(html):
    return re.sub(r'\s(srcset|sizes)=("[^"]*"|\'[^\']*\')', "", html)


def clean_classic(html):
    def f(s):
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        s = re.sub(r'\s(class|style|data-[\w-]+|srcset|sizes)=("[^"]*"|\'[^\']*\')', "", s)
        s = re.sub(r"<span>(.*?)</span>", r"\1", s, flags=re.S)
        return s
    return protect(html, f)


def shortcode_captions(html):
    def rep(m):
        inner = m.group(1)
        img = re.search(r"(<a[^>]*>\s*)?<img[^>]*>(\s*</a>)?", inner)
        if not img:
            return inner
        cap = inner.replace(img.group(0), "").strip()
        return "<figure>%s<figcaption>%s</figcaption></figure>" % (img.group(0), cap)
    return re.sub(r"\[caption[^\]]*\](.*?)\[/caption\]", rep, html, flags=re.S)


def wpautop(text):
    """Safe wpautop: wrap only runs of plain inline lines in <p>."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, buf = [], []
    raw_until = None

    def flush():
        if buf:
            out.append("<p>" + "<br>\n".join(buf) + "</p>")
            buf.clear()

    for line in lines:
        if raw_until:
            out.append(line)
            if re.search(r"</%s>" % raw_until, line, re.I):
                raw_until = None
            continue
        s = line.strip()
        m = re.match(r"<(pre|script|style|table|ul|ol|blockquote|figure|iframe|svg|div|form)\b", s, re.I)
        if m and not re.search(r"</%s>" % m.group(1), s, re.I):
            flush()
            out.append(line)
            raw_until = m.group(1)
            continue
        if not s:
            flush()
        elif BLOCK_START.match(s) or BLOCK_END.search(s):
            flush()
            out.append(s)
        else:
            buf.append(s)
    flush()
    return "\n".join(out)


def fix_headings(html, title, keyword):
    title_norm = slugify(title)
    used = set()

    def h1(m):
        inner = m.group(2)
        if slugify(inner) == title_norm:
            return ""
        return "<h2%s>%s</h2>" % (m.group(1), inner)

    def generic(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        plain = htmllib.unescape(re.sub(r"<[^>]+>", "", inner)).strip().rstrip(":").lower()
        if plain in GENERIC_HEADINGS:
            topic = keyword.strip() or title
            topic = topic[:1].upper() + topic[1:]
            inner = "Key Takeaways on %s" % topic
        return "<%s%s>%s</%s>" % (tag, attrs, inner, tag)

    def add_id(m):
        attrs, inner = m.group(1), m.group(2)
        idm = re.search(r'\sid=["\']([^"\']+)', attrs)
        if idm:
            used.add(idm.group(1))
            return m.group(0)
        base = slugify(inner)
        hid, n = base, 2
        while hid in used:
            hid, n = "%s-%d" % (base, n), n + 1
        used.add(hid)
        return '<h2%s id="%s">%s</h2>' % (attrs, hid, inner)

    def f(s):
        s = re.sub(r"<h1([^>]*)>(.*?)</h1>", h1, s, flags=re.S | re.I)
        s = re.sub(r"<(h2|h3)([^>]*)>(.*?)</\1>", generic, s, flags=re.S | re.I)
        s = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, s, flags=re.S | re.I)
        return s
    return protect(html, f)


def elementor_html(data):
    parts = []

    def walk(els):
        for e in els:
            if e.get("elType") == "widget":
                s = e.get("settings", {})
                w = e.get("widgetType")
                if w == "html":
                    parts.append(s.get("html", ""))
                elif w == "text-editor":
                    ed = s.get("editor", "")
                    parts.append(ed if "<p" in ed else wpautop(ed))
                elif w == "heading":
                    tag = s.get("header_size") or "h2"
                    parts.append("<%s>%s</%s>" % (tag, s.get("title", ""), tag))
                elif w == "image":
                    img = s.get("image") or {}
                    if img.get("url"):
                        parts.append('<p><img src="%s" alt="%s"></p>' % (img["url"], htmllib.escape(img.get("alt", ""))))
            walk(e.get("elements", []))
    walk(data)
    return "\n".join(parts)


def plain_text(html):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", htmllib.unescape(s)).strip()


def yaml_val(v):
    return json.dumps(v, ensure_ascii=False)


def write_entry(path, fm, body):
    lines = ["---"]
    for k, v in fm.items():
        if v is None or v == "" or v == []:
            continue
        lines.append("%s: %s" % (k, yaml_val(v)))
    lines.append("---")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n" + body.strip() + "\n")


UPLOAD_RE = re.compile(r"/wp-content/uploads/[^\s\"'<>()?#\\]+?\.(?:jpe?g|png|gif|webp|avif|svg|mp4|webm|pdf)", re.I)


def main(src):
    data = open(src, "rb").read().replace(b"\x00", b"%00")
    channel = ET.fromstring(data).find("channel")

    # categories
    cats = {}
    by_id = {}
    for c in channel.findall("wp:category", NS):
        slug = t(c, "wp:category_nicename")
        cats[slug] = {"slug": slug, "name": htmllib.unescape(t(c, "wp:cat_name")),
                      "parent": t(c, "wp:category_parent") or None,
                      "description": DESCRIPTIONS.get(slug, "")}
        by_id[t(c, "wp:term_id")] = slug
    for c in cats.values():
        c["path"] = (c["parent"] + "/" if c["parent"] else "") + c["slug"]

    authors = {}
    for a in channel.findall("wp:author", NS):
        authors[t(a, "wp:author_login")] = t(a, "wp:author_display_name")

    items = channel.findall("item")
    attachments = {}
    for it in items:
        if t(it, "wp:post_type") == "attachment":
            m = meta_of(it)
            attachments[t(it, "wp:post_id")] = {"url": t(it, "wp:attachment_url"),
                                                "alt": m.get("_wp_attachment_image_alt", "")}

    images = set()
    used_cats = {}
    os.makedirs(os.path.join(ROOT, "src/content/posts"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "src/content/pages"), exist_ok=True)
    count = {"post": 0, "page": 0}

    for it in items:
        ptype, status = t(it, "wp:post_type"), t(it, "wp:status")
        slug = t(it, "wp:post_name")
        if status != "publish" or ptype not in ("post", "page"):
            continue
        if ptype == "page" and slug not in KEEP_PAGES:
            continue
        m = meta_of(it)
        title = htmllib.unescape(t(it, "title")).strip()
        keyword = (m.get("rank_math_focus_keyword") or m.get("_yoast_wpseo_focuskw") or "").split(",")[0].strip()

        body = None
        if m.get("_elementor_edit_mode") == "builder" and m.get("_elementor_data") not in (None, "", "[]"):
            try:
                body = elementor_html(json.loads(m["_elementor_data"]))
            except ValueError:
                body = None
        classic = body is None or not body.strip()
        if classic:
            body = t(it, "content:encoded")
            body = shortcode_captions(body)
            body = clean_classic(body)
            body = wpautop(body)
            body = re.sub(r"<p>\s*(&nbsp;| )?\s*</p>", "", body)
        body = strip_srcset(body)
        body = rewrite_urls(body)
        body = fix_headings(body, title, keyword)
        body = re.sub(r"\n{2,}", "\n", body)

        for u in UPLOAD_RE.findall(body):
            images.add(u)

        image = alt = ""
        thumb = attachments.get(m.get("_thumbnail_id", ""))
        if thumb and thumb["url"]:
            image = rewrite_urls(thumb["url"])
            alt = thumb["alt"] or title
            if image.startswith("/wp-content/uploads/"):
                images.add(image)

        desc = m.get("rank_math_description") or m.get("_yoast_wpseo_metadesc") or ""
        excerpt = plain_text(t(it, "excerpt:encoded"))
        text = plain_text(body)
        if not desc:
            desc = excerpt or text[:155].rsplit(" ", 1)[0]
        words = len(text.split())

        if ptype == "post":
            post_cats = [c.get("nicename") for c in it.findall("category") if c.get("domain") == "category"]
            post_tags = [htmllib.unescape(c.text or "") for c in it.findall("category") if c.get("domain") == "post_tag"]
            primary = by_id.get(m.get("rank_math_primary_category", ""), "")
            if primary not in post_cats:
                # prefer a child category, it gives the most specific breadcrumb
                kids = [c for c in post_cats if cats.get(c, {}).get("parent")]
                primary = (kids or post_cats or ["uncategorized"])[0]
            for c in post_cats:
                used_cats[c] = used_cats.get(c, 0) + 1
            try:
                views = int(m.get("frenify_post_views_count") or 0)
            except ValueError:
                views = 0
            fm = {
                "title": title,
                "slug": slug,
                "date": t(it, "wp:post_date").replace(" ", "T"),
                "updated": t(it, "wp:post_modified").replace(" ", "T"),
                "author": CANONICAL_AUTHOR,
                "categories": post_cats,
                "primaryCategory": primary,
                "tags": post_tags,
                "description": htmllib.unescape(desc).strip(),
                "focusKeyword": keyword,
                "image": image,
                "imageAlt": htmllib.unescape(alt),
                "words": words,
                "views": views,
                "format": "html",
            }
            write_entry(os.path.join(ROOT, "src/content/posts", slug + ".md"), fm, body)
        else:
            if slug == "about-us":
                # drop the theme demo gallery that points at frenify.com
                body = re.sub(r"<ul>\s*(<li>\s*<img[^>]*frenify[^>]*>\s*</li>\s*)+</ul>", "", body)
            fm = {"title": title, "slug": slug, "description": htmllib.unescape(desc).strip(),
                  "updated": t(it, "wp:post_modified").replace(" ", "T"), "format": "html"}
            write_entry(os.path.join(ROOT, "src/content/pages", slug + ".md"), fm, body)
        count[ptype] += 1

    # 301 redirects: old WordPress slugs and link variants that never existed
    redirects = {}
    for it in items:
        if t(it, "wp:post_type") == "post" and t(it, "wp:status") == "publish":
            for mm in it.findall("wp:postmeta", NS):
                if t(mm, "wp:meta_key") == "_wp_old_slug":
                    old = t(mm, "wp:meta_value")
                    if old and not os.path.exists(os.path.join(ROOT, "src/content/posts", old + ".md")):
                        redirects[old] = t(it, "wp:post_name")
    for old, new in LINK_FIXES.items():
        if "." not in old:
            redirects.setdefault(old, new)
    lines = ["  RewriteRule ^%s/?$ /%s/ [R=301,L]" % (re.escape(o), n) for o, n in sorted(redirects.items())]
    ht = os.path.join(ROOT, "public/.htaccess")
    if os.path.exists(ht):
        src_ht = open(ht).read()
        block = "  # BEGIN post redirects (generated by scripts/migrate_wxr.py)\n" + "\n".join(lines) + "\n  # END post redirects\n"
        src_ht = re.sub(r"  # BEGIN post redirects.*?# END post redirects\n", lambda _m: block, src_ht, flags=re.S)
        open(ht, "w").write(src_ht)
    print("redirects", len(redirects))

    for c in cats.values():
        c["count"] = used_cats.get(c["slug"], 0)
    os.makedirs(os.path.join(ROOT, "src/data"), exist_ok=True)
    with open(os.path.join(ROOT, "src/data/categories.json"), "w", encoding="utf-8") as fh:
        json.dump(list(cats.values()), fh, indent=2, ensure_ascii=False)
    with open(os.path.join(ROOT, "src/data/authors.json"), "w", encoding="utf-8") as fh:
        json.dump([{"slug": CANONICAL_AUTHOR, "name": "Santaji Gadepatil",
                    "role": "Founder and Editor, Brandella Journal",
                    "bio": "Marketing manager and B.E. Electronics and Telecommunication engineer. Santaji writes practical, tested guides on SEO, paid media, AI search and web development, so marketers can turn ideas into results.",
                    "photo": "/images/authors/santajigade-200.webp",
                    "photoSmall": "/images/authors/santajigade-96.webp",
                    "expertise": ["SEO", "Google Ads", "AI Search", "Web Development"],
                    "linkedin": "https://www.linkedin.com/in/santaji-gadepatil6680/"}], fh, indent=2)
    with open(os.path.join(ROOT, "scripts/wp_images.txt"), "w") as fh:
        fh.write("\n".join(sorted(images)) + "\n")
    print("posts", count["post"], "pages", count["page"], "images", len(images), "authors in WXR", authors)


if __name__ == "__main__":
    main(sys.argv[1])
