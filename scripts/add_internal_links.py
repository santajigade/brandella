"""Add contextual internal links pointing to priority pages.

Usage: python3 scripts/add_internal_links.py [--apply]
Without --apply it only prints the plan.

Rules: links go only inside <p> text (never headings, existing links, code, scripts or styles),
first match only, one link per source post per target, sources that already link to the target
are skipped, at most MAX_PER_TARGET new links per target and MAX_PER_SOURCE per source post.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_PER_TARGET = 5
MAX_PER_SOURCE = 2

TARGETS = {
    "what-is-search-intent-practical-guide": ["intent-based search", "search intent", "user intent"],
    "what-is-google-ai-mode": ["Google AI Mode", "AI Mode"],
    "linkedin-ads-targeting": ["LinkedIn Ads targeting", "LinkedIn targeting", "LinkedIn advertising", "LinkedIn Ads"],
    "meta-robots-tags-explained-2": ["meta robots tags", "meta robots tag", "robots meta tag", "noindex tag"],
    "link-rel-attribute-explained": ["link rel attribute", "rel attributes", "rel attribute"],
    "august-2026-spam-update": ["August 2026 spam update", "August spam update"],
    "social-media-listening": ["social media listening", "social listening"],
    "nofollow-vs-dofollow-links": ["dofollow and nofollow", "nofollow and dofollow", "dofollow links", "nofollow links"],
    "branded-queries-filter-in-search-console": ["branded and non-branded", "branded queries", "branded traffic"],
    "ai-search-vs-traditional-search": ["AI search vs traditional search", "traditional search", "AI search engines"],
}

# Posts Search Console reported as "Crawled - currently not indexed" (Nov 2026). Run with --set=2
TARGETS_2 = {
    "chatgpt-ads-vs-google-search-ads": ["ChatGPT ads", "ads in ChatGPT"],
    "python-and-pandas-seo-reporting": ["SEO reporting", "Pandas"],
    "copy-to-clipboard-button-javascript": ["copy to clipboard", "clipboard"],
    "migrate-from-http-to-https": ["HTTP to HTTPS", "migrate to HTTPS", "HTTPS migration", "SSL certificate"],
    "understanding-digital-marketing": ["what is digital marketing", "digital marketing basics", "digital marketing"],
    "ai-for-seo-artificial-intelligence": ["AI for SEO", "AI in SEO"],
    "ai-in-ppc-should-advertisers-be-worried": ["AI in PPC", "PPC automation", "AI bidding"],
}

P_RE = re.compile(r"<p\b[^>]*>(?:(?!</p>).)*?</p>", re.S | re.I)
SKIP_RE = re.compile(r"<(script|style|code|pre)\b.*?</\1>", re.S | re.I)


def link_in_p(p, phrases, href):
    """Return (new_p, anchor) with the first phrase linked, or None."""
    parts = re.split(r"(<[^>]+>)", p)
    depth_a = 0
    for i, part in enumerate(parts):
        if part.startswith("<"):
            t = part.lower()
            if re.match(r"<a\b", t): depth_a += 1
            elif t.startswith("</a"): depth_a = max(0, depth_a - 1)
            elif re.match(r"<(code|strong|b|em)\b", t) and False: pass
            continue
        if depth_a or i == 0 and False:
            continue
        for ph in phrases:
            m = re.search(r"(?<![\w-])" + re.escape(ph) + r"(?![\w-])", part, re.I)
            if m:
                parts[i] = part[:m.start()] + f'<a href="{href}">{m.group(0)}</a>' + part[m.end():]
                return "".join(parts), m.group(0)
    return None


def main(apply):
    files = sorted(glob.glob(os.path.join(ROOT, "src/content/posts/*.md")))
    docs = {}
    for f in files:
        txt = open(f, encoding="utf-8", newline="").read()
        slug = re.search(r'^slug:\s*"?([^"\r\n]+)', txt, re.M).group(1)
        fmt = (re.search(r'^format:\s*"?(\w+)', txt, re.M) or [None, "html"])[1]
        end = txt.index("\n---", 3) + 4
        docs[slug] = {"file": f, "head": txt[:end], "body": txt[end:], "fmt": fmt, "added": 0}

    plan = []
    targets = TARGETS_2 if "--set=2" in sys.argv else TARGETS
    for target, phrases in targets.items():
        href = f"/{target}/"
        cands = []
        for slug, d in docs.items():
            if slug == target or d["fmt"] != "html" or href in d["body"]:
                continue
            visible = SKIP_RE.sub("", d["body"])
            score = sum(len(re.findall(r"(?<![\w-])" + re.escape(ph) + r"(?![\w-])", visible, re.I)) for ph in phrases)
            if score:
                cands.append((score, slug))
        cands.sort(reverse=True)
        n = 0
        for score, slug in cands:
            if n >= MAX_PER_TARGET:
                break
            d = docs[slug]
            if d["added"] >= MAX_PER_SOURCE:
                continue
            body = d["body"]
            # protect script/style/code blocks
            keep = {}
            def stash(m):
                k = f"\x00{len(keep)}\x00"; keep[k] = m.group(0); return k
            safe = SKIP_RE.sub(stash, body)
            done = None
            for pm in P_RE.finditer(safe):
                if "\x00" in pm.group(0):
                    continue
                r = link_in_p(pm.group(0), phrases, href)
                if r:
                    safe = safe[:pm.start()] + r[0] + safe[pm.end():]
                    done = r[1]
                    break
            if not done:
                continue
            for k, v in keep.items():
                safe = safe.replace(k, v)
            d["body"] = safe
            d["added"] += 1
            d["changed"] = True
            n += 1
            plan.append((target, slug, done))

    for t, s, a in plan:
        print(f"{t:45} <- {s:55} [{a}]")
    print(f"{len(plan)} links")
    if apply:
        for d in docs.values():
            if d.get("changed"):
                open(d["file"], "w", encoding="utf-8", newline="").write(d["head"] + d["body"])


if __name__ == "__main__":
    main("--apply" in sys.argv)
