import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts, postUrl, primaryCat } from '../lib/site';
import { SITE } from '../config';

export async function GET(context: APIContext) {
  const posts = (await getPosts()).slice(0, 50);
  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site!,
    items: posts.map((p) => ({
      title: p.data.title,
      link: postUrl(p),
      pubDate: p.data.date,
      description: p.data.description,
      categories: [primaryCat(p).name],
    })),
    customData: '<language>en</language>',
  });
}
