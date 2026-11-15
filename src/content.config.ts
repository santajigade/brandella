import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import type { Loader } from 'astro/loaders';
import { readdir, readFile } from 'node:fs/promises';
import { parse as parseYaml } from 'yaml';

/**
 * Markdown files with front matter. Migrated WordPress posts use `format: html`
 * and their body is raw HTML (BX FORMAT with its own CSS and scripts), which is
 * passed through untouched. New posts can use normal Markdown (`format: md`).
 */
function contentDir(dir: string): Loader {
  return {
    name: 'brandella-content',
    load: async ({ store, parseData, renderMarkdown, generateDigest, logger }) => {
      store.clear();
      const base = new URL(`./src/content/${dir}/`, `file://${process.cwd()}/`);
      const files = (await readdir(base)).filter((f) => f.endsWith('.md'));
      for (const file of files) {
        const raw = await readFile(new URL(file, base), 'utf-8');
        const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
        if (!m) {
          logger.warn(`No front matter in ${dir}/${file}`);
          continue;
        }
        const fm = parseYaml(m[1]) ?? {};
        const body = m[2];
        const id = String(fm.slug || file.replace(/\.md$/, ''));
        const data = await parseData({ id, data: fm });
        const html = (fm.format ?? 'md') === 'html' ? body : (await renderMarkdown(body)).html;
        store.set({ id, data, body, digest: generateDigest(raw), rendered: { html } });
      }
    },
  };
}

const posts = defineCollection({
  loader: contentDir('posts'),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    author: z.string().default('santajigade'),
    categories: z.array(z.string()).default(['uncategorized']),
    primaryCategory: z.string().optional(),
    tags: z.array(z.string()).default([]),
    description: z.string().default(''),
    focusKeyword: z.string().optional(),
    takeaways: z.array(z.string()).optional(),
    nextRead: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    words: z.number().optional(),
    views: z.number().default(0),
    format: z.enum(['html', 'md']).default('md'),
    draft: z.boolean().default(false),
  }),
});

const pages = defineCollection({
  loader: contentDir('pages'),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string().default(''),
    updated: z.coerce.date().optional(),
    format: z.enum(['html', 'md']).default('md'),
  }),
});

export const collections = { posts, pages };
