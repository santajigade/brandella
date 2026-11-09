#!/usr/bin/env python3
"""Check new Markdown news posts before publishing.

Usage: python3 scripts/check_post.py <slug> [<slug> ...]
Exit code 1 if any post has a FAIL. Warnings do not block.
"""
import difflib
import json
import os
import re
import sys

import yaml  # pip install pyyaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "src/content/posts")
CATS = {c["slug"]: c for c in json.load(open(os.path.join(ROOT, "src/data/categories.json")))}
AUTHORS = {a["slug"] for a in json.load(open(os.path.join(ROOT, "src/data/authors.json")))}
PAGES = {"about-us", "contact-page", "privacy-policy", "terms-and-conditions", "search"}
GENERIC = {"conclusion", "final thoughts", "final takeaway", "summary", "wrapping up", "in conclusion",
           "the bottom line", "introduction", "overview"}
REQUIRED = ["title", "slug", "date", "author", "categories", "primaryCategory", "description",
            "focusKeyword", "image", "imageAlt", "format"]


def load(slug):
    raw = open(os.path.join(POSTS, slug + ".md"), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    return raw, yaml.safe_load(m.group(1)), m.group(2)


def plain(md):
    s = re.sub(r"```.*?```", " ", md, flags=re.S)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[#>*_`|]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def internal_ok(path):
    p = path.split("#")[0].split("?")[0]
    if not p.endswith("/"):
        return False
    parts = [x for x in p.split("/") if x]
    if not parts:
        return True
    if parts[0] == "category":
        return parts[-1] in CATS
    if parts[0] in ("author", "tools"):
        return True
    return len(parts) == 1 and (os.path.exists(os.path.join(POSTS, parts[0] + ".md")) or parts[0] in PAGES)


def check(slug):
    fails, warns = [], []
    raw, fm, body = load(slug)
    for k in REQUIRED:
        if not fm.get(k):
            fails.append("missing front matter: " + k)
    if fm.get("slug") != slug:
        fails.append("slug does not match file name")
    if len(slug) > 60 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        fails.append("slug must be lowercase words joined by hyphens, max 60 chars")
    if re.search("[\u2013\u2014]", raw):
        fails.append("contains an em dash or en dash")
    if fm.get("format") != "md":
        fails.append("format must be md")
    cats = fm.get("categories") or []
    for c in cats:
        if c not in CATS or c == "uncategorized":
            fails.append("unknown category: %s" % c)
    if fm.get("primaryCategory") not in cats:
        fails.append("primaryCategory must be one of categories")
    want_author = "ankush-guleria" if "digital-marketing" in cats else "santajigade"
    if fm.get("author") != want_author:
        fails.append("author must be %s" % want_author)
    if fm.get("author") not in AUTHORS:
        fails.append("unknown author")
    img = fm.get("image", "")
    if img and not os.path.exists(os.path.join(ROOT, "public", img.lstrip("/"))):
        fails.append("image file missing: " + img)
    for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)\s]+)\)", body):
        if src.startswith("/") and not os.path.exists(os.path.join(ROOT, "public", src.lstrip("/"))):
            fails.append("body image missing: " + src)
        if len(alt.strip()) < 10:
            fails.append("body image needs descriptive alt text: " + src)
    title, desc, kw = fm.get("title", ""), fm.get("description", ""), (fm.get("focusKeyword") or "").lower()
    if not 35 <= len(title) <= 70:
        warns.append("title length %d (aim 45 to 65)" % len(title))
    if not 120 <= len(desc) <= 160:
        fails.append("description must be 120 to 160 chars (is %d)" % len(desc))
    text = plain(body)
    words = len(text.split())
    if not 800 <= words <= 1400:
        fails.append("body must be 800 to 1400 words (is %d)" % words)
    if kw:
        if kw not in title.lower():
            fails.append("focus keyword not in title")
        if kw not in desc.lower():
            fails.append("focus keyword not in description")
        if kw not in text[: max(400, len(text) // 8)].lower():
            fails.append("focus keyword not in the first part of the body")
        if kw.replace(" ", "-") not in slug and not all(w in slug for w in kw.split()[:2]):
            warns.append("slug does not contain the focus keyword")
    heads = re.findall(r"^(#{2,3})\s+(.+)$", body, re.M)
    h2 = [h for lvl, h in heads if lvl == "##"]
    if len(h2) < 4:
        fails.append("needs at least 4 H2 sections (has %d)" % len(h2))
    if re.search(r"^#\s", body, re.M):
        fails.append("do not use H1 in the body")
    for _, h in heads:
        if h.strip().rstrip(":").lower() in GENERIC:
            fails.append("generic heading: " + h)
    if kw and not any(kw in h.lower() for _, h in heads):
        warns.append("focus keyword not in any H2 or H3")
    links = re.findall(r"\]\(([^)\s]+)", re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body))
    internal = [u for u in links if u.startswith("/")]
    external = [u for u in links if u.startswith("http")]
    for u in internal:
        if not internal_ok(u):
            fails.append("broken internal link: " + u)
    if len([u for u in internal if not u.startswith(("/category/", "/author/", "/tools/"))]) < 3:
        fails.append("needs at least 3 internal links to existing articles")
    if any("brandella.in" in u for u in external):
        fails.append("use relative links (/slug/) for brandella.in")
    if len(external) < 3:
        fails.append("needs at least 3 external links to official or authoritative sources")
    if re.search(r"(?im)^#{2,3}\s+(sources|references)\b", body):
        fails.append("no Sources or References section, link inside the text instead")
    others = [f[:-3] for f in os.listdir(POSTS) if f.endswith(".md") and f[:-3] != slug]
    # near-duplicate content check against every other Markdown post (scaled content guard)
    def shingles(t):
        w = re.findall(r"[a-z0-9]+", t.lower())
        return {" ".join(w[i:i + 5]) for i in range(max(0, len(w) - 4))}
    mine = shingles(text)
    for o in others:
        oraw = open(os.path.join(POSTS, o + ".md"), encoding="utf-8").read()
        if 'format: "md"' not in oraw[:3000] and "format: md" not in oraw[:3000]:
            continue
        theirs = shingles(plain(oraw.split("---", 2)[-1]))
        if mine and theirs:
            overlap = len(mine & theirs) / len(mine)
            if overlap > 0.25:
                fails.append("%.0f%% of the text overlaps with /%s/ (near duplicate)" % (overlap * 100, o))
            elif overlap > 0.12:
                warns.append("%.0f%% text overlap with /%s/" % (overlap * 100, o))
    if re.search(r"\b[A-Z]{5,}\b", title) and not re.search(r"\b(GA4|SEO|PPC|LLMS|HTML|JSON)\b", title):
        warns.append("title has ALL CAPS words, avoid clickbait style")
    if re.search(r"(?i)\b(shocking|you won.t believe|insane|secret trick|must see)\b", title):
        fails.append("clickbait wording in title")
    for o in others:
        if difflib.SequenceMatcher(None, slug, o).ratio() > 0.85:
            warns.append("slug very close to existing post: " + o)
    return words, fails, warns


def main(slugs):
    bad = 0
    for s in slugs:
        words, fails, warns = check(s)
        status = "FAIL" if fails else "OK"
        print("%s %s (%d words)" % (status, s, words))
        for f in fails:
            print("   FAIL", f)
        for w in warns:
            print("   warn", w)
        bad += bool(fails)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
