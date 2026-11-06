import type { APIRoute } from 'astro';
import { getPosts, postUrl, primaryCat, thumb } from '../lib/site';

export const GET: APIRoute = async () => {
  const posts = await getPosts();
  const data = posts.map((p) => ({
    t: p.data.title,
    u: postUrl(p),
    d: p.data.description,
    c: primaryCat(p).name,
    k: [p.data.focusKeyword, ...p.data.tags].filter(Boolean).join(' '),
    i: thumb(p.data.image),
    dt: p.data.date.toISOString().slice(0, 10),
  }));
  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } });
};
