# SEO checklist for every Brandella article

Santaji's standing rule: every article, news or evergreen, new or updated, must follow this list. News runs follow `DAILY_NEWS.md` too; `scripts/check_post.py <slug>` checks most of these automatically for Markdown posts.

## Before writing
- One topic, one page. Run `python3 scripts/list_posts.py find <key words>` first. If an existing post already targets the topic, update that post instead of writing a new one (two pages on one topic compete and both rank worse).
- Pick one focus keyword that no other post uses as its focus keyword.
- Match search intent: look at what ranks on Google for the keyword (guide, list, news, comparison) and use that format.

## Title, slug, description
- Title: focus keyword near the start, 45 to 60 characters before " | Brandella Journal", honest, no clickbait.
- Slug: short, lowercase, contains the focus keyword, max 60 characters. Never change the slug of a published post.
- Description: 120 to 160 characters, contains the focus keyword, says what the reader gets.

## Body
- Focus keyword in the first paragraph and in at least one H2. Use it naturally; never stuff it.
- No H1 in the body (the title is the H1). Clear H2 and H3 headings, never "Conclusion" or "Summary".
- Original value: practical steps, a checklist, a table, examples or our own analysis. Never just restate a source.
- Short paragraphs of 2 or 3 sentences.
- An FAQ section (`## FAQ about <topic>` with `###` questions ending in "?") when readers have real follow up questions. The site turns it into FAQ schema automatically.
- Every fact from a source you opened; link the official source inside the sentence.
- No em dash or en dash characters anywhere.

## Links
- 3 to 5 internal links to genuinely related Brandella posts, with descriptive anchor text (not "click here").
- After publishing, add one contextual link to the new post from one older, related post (one sentence or anchor inside an existing paragraph, no other edits), so no article is orphaned.
- Do not add a "Related Articles" or "Continue Reading" box inside the article; the page template already shows related articles at the bottom.
- 3 to 6 external links to official or authoritative sources. No paid or swapped links.

## Images
- Cover image plus 1 or 2 infographics or real screenshots. Never fake screenshots or stock photos of people.
- Descriptive alt text of at least 10 characters on every image; WebP format.

## Updating an old post
- Keep the slug. Update the `updated` date only when the content really changed.
- Add depth (new sections, FAQ, examples), refresh facts and links, and re-check the focus keyword is unique.
- Merging two posts on the same topic: keep the stronger URL (more impressions or better position), 301 redirect the other in the manual block of `public/.htaccess`, and repoint internal links.

## After publishing
- `npm run build` passes and the page exists in `dist/`.
- Request indexing in Search Console for important new or heavily updated pages.
