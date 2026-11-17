import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import { getPosts, postUrl, primaryCat } from '../lib/site';
import { SITE } from '../config';

// Each item carries its cover image (enclosure + media:content) so Pinterest and
// other feed readers can show a picture for every article.
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
const typeOf = (u: string) => (/\.png$/i.test(u) ? 'image/png' : /\.jpe?g$/i.test(u) ? 'image/jpeg' : 'image/webp');

export async function GET(context: APIContext) {
  const posts = (await getPosts()).slice(0, 50);
  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site!,
    xmlns: { media: 'http://search.yahoo.com/mrss/' },
    items: posts.map((p) => {
      const img = p.data.image as string | undefined;
      const abs = img ? new URL(img, context.site).href : undefined;
      let length = 0;
      if (img && img.startsWith('/')) {
        try { length = fs.statSync(path.join('public', img)).size; } catch { length = 0; }
      }
      return {
        title: p.data.title,
        link: postUrl(p),
        pubDate: p.data.date,
        description: p.data.description,
        categories: [primaryCat(p).name],
        ...(abs ? {
          enclosure: { url: abs, length, type: typeOf(abs) },
          customData: `<media:content url="${esc(abs)}" medium="image" type="${typeOf(abs)}"><media:title>${esc(p.data.imageAlt || p.data.title)}</media:title></media:content>`,
        } : {}),
      };
    }),
    customData: '<language>en</language>',
  });
}
