#!/usr/bin/env python3
"""List posts for duplicate checks and internal linking.

python3 scripts/list_posts.py recent 40      newest 40 posts (date, slug, title)
python3 scripts/list_posts.py cat seo        every post in a category (and its children)
python3 scripts/list_posts.py find <words>   posts whose title or slug contains all words
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "src/content/posts")
CATS = json.load(open(os.path.join(ROOT, "src/data/categories.json")))
rows = []
for f in os.listdir(POSTS):
    if not f.endswith(".md"):
        continue
    head = open(os.path.join(POSTS, f), encoding="utf-8").read(3000)
    g = lambda k: (re.search(r'^%s:\s*"?(.*?)"?\s*$' % k, head, re.M) or [None, ""])[1]
    cats = re.findall(r'"([a-z0-9_-]+)"', (re.search(r"^categories:(.*)$", head, re.M) or [None, ""])[1])
    rows.append((g("date")[:10], f[:-3], g("title"), cats))
rows.sort(reverse=True)
cmd = sys.argv[1] if len(sys.argv) > 1 else "recent"
if cmd == "recent":
    for r in rows[: int(sys.argv[2]) if len(sys.argv) > 2 else 40]:
        print(r[0], "/%s/" % r[1], r[2])
elif cmd == "cat":
    fam = {sys.argv[2]} | {c["slug"] for c in CATS if c["parent"] == sys.argv[2]}
    for r in rows:
        if fam & set(r[3]):
            print(r[0], "/%s/" % r[1], r[2])
elif cmd == "find":
    words = [w.lower() for w in sys.argv[2:]]
    for r in rows:
        hay = (r[1] + " " + r[2]).lower()
        if all(w in hay for w in words):
            print(r[0], "/%s/" % r[1], r[2])
