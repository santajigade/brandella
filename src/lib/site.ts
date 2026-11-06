import { getCollection, type CollectionEntry } from 'astro:content';
import categoriesJson from '../data/categories.json';
import authorsJson from '../data/authors.json';
import { SITE } from '../config';
import { existsSync } from 'node:fs';

export type Post = CollectionEntry<'posts'>;
export interface Category {
  slug: string;
  name: string;
  parent: string | null;
  description: string;
  path: string;
  count: number;
}

export const categories: Category[] = categoriesJson as Category[];
export const authors = authorsJson as {
  slug: string; name: string; role: string; bio: string; linkedin: string;
  photo?: string; photoSmall?: string; expertise?: string[];
}[];

export const catBySlug = new Map(categories.map((c) => [c.slug, c]));
export const childrenOf = (slug: string) =>
  categories.filter((c) => c.parent === slug).sort((a, b) => a.name.localeCompare(b.name));

export const catUrl = (slug: string) => {
  const c = catBySlug.get(slug);
  return c ? `/category/${c.path}/` : '/';
};
export const postUrl = (p: Post) => `/${p.data.slug}/`;
export const authorOf = (p: Post) => authors.find((a) => a.slug === p.data.author) ?? authors[0];
export const authorUrl = (slug: string) => `/author/${slug}/`;

let cache: Post[] | null = null;
export async function getPosts(): Promise<Post[]> {
  if (cache) return cache;
  const all = await getCollection('posts', (p) => !p.data.draft);
  cache = all.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  return cache;
}

/** Posts in a category, including posts filed only in its children (WordPress behaviour). */
export function inCategory(posts: Post[], slug: string) {
  const family = new Set([slug, ...childrenOf(slug).map((c) => c.slug)]);
  return posts.filter((p) => p.data.categories.some((c) => family.has(c)));
}

export function primaryCat(p: Post): Category {
  return (
    catBySlug.get(p.data.primaryCategory ?? '') ??
    catBySlug.get(p.data.categories[0]) ??
    catBySlug.get('uncategorized')!
  );
}

export function topCat(p: Post): Category {
  const c = primaryCat(p);
  return c.parent ? catBySlug.get(c.parent) ?? c : c;
}

export function readTime(p: Post) {
  const words = p.data.words ?? (p.body ?? '').replace(/<[^>]+>/g, ' ').split(/\s+/).length;
  return Math.max(1, Math.round(words / 220));
}

const fmt = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
export const formatDate = (d: Date) => fmt.format(d);

/** Small WebP thumbnail made by the image workflow, falls back to the original. */
export function thumb(src?: string) {
  if (!src) return '/og-default.png';
  if (src.startsWith('/wp-content/uploads/')) {
    const t = '/thumbs/' + src.slice('/wp-content/uploads/'.length).replace(/\.[a-z0-9]+$/i, '.webp');
    // thumbnails are made by the "Fetch WordPress images" workflow; use the original until then
    return existsSync(`public${t}`) ? t : src;
  }
  return src;
}

export const absolute = (path: string) => new URL(path, SITE.url).toString();

export function popular(posts: Post[], n: number) {
  return [...posts].sort((a, b) => b.data.views - a.data.views).slice(0, n);
}

export function related(posts: Post[], p: Post, n: number) {
  const cat = primaryCat(p).slug;
  const top = topCat(p).slug;
  const same = posts.filter((x) => x.id !== p.id && x.data.categories.includes(cat));
  const near = inCategory(posts, top).filter((x) => x.id !== p.id && !same.includes(x));
  return [...same, ...near].slice(0, n);
}

/** Next articles for infinite scroll: older posts in the same section first. */
export function nextUp(posts: Post[], p: Post, n: number) {
  const top = topCat(p).slug;
  const idx = posts.findIndex((x) => x.id === p.id);
  const older = posts.slice(idx + 1);
  const newer = posts.slice(0, idx);
  const pool = [...older, ...newer];
  const sameTop = pool.filter((x) => inCategory([x], top).length);
  const rest = pool.filter((x) => !sameTop.includes(x));
  return [...sameTop, ...rest].slice(0, n);
}

export function headings(html: string) {
  const out: { id: string; text: string }[] = [];
  const clean = html.replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, '');
  for (const m of clean.matchAll(/<h2\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h2>/gi)) {
    const text = m[2].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&#0?39;|&rsquo;/g, '’').replace(/&nbsp;/g, ' ').trim();
    if (text) out.push({ id: m[1], text });
  }
  return out;
}

export function paginate<T>(items: T[], size: number) {
  const pages: T[][] = [];
  for (let i = 0; i < items.length; i += size) pages.push(items.slice(i, i + size));
  return pages.length ? pages : [[]];
}
