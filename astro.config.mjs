import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';

// Last modified date for each post, read from front matter, so the sitemap can tell Google what changed.
const postDir = path.resolve('src/content/posts');
const lastmod = {};
for (const f of fs.readdirSync(postDir).filter((x) => x.endsWith('.md'))) {
  const txt = fs.readFileSync(path.join(postDir, f), 'utf8').slice(0, 2000);
  const get = (k) => (txt.match(new RegExp(`^${k}:\\s*"?([^"\\r\\n]+)"?`, 'm')) || [])[1];
  const slug = get('slug');
  const date = get('updated') || get('date');
  if (slug && date && !Number.isNaN(Date.parse(date))) lastmod[`https://brandella.in/${slug}/`] = new Date(date).toISOString();
}
const newest = Object.values(lastmod).sort().pop();

// SEO assets library: assets without a YAML file are "coming soon" placeholders (noindex), keep them out of the sitemap.
const assetDir = path.resolve('src/data/seo-assets');
const comingSoon = JSON.parse(fs.readFileSync(path.join(assetDir, 'index.json'), 'utf8')).assets
  .filter((a) => !fs.existsSync(path.join(assetDir, `${a.slug}.yaml`)))
  .map((a) => `https://brandella.in/resources/seo-aeo-assets/${a.slug}/`);

export default defineConfig({
  site: 'https://brandella.in',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  integrations: [
    sitemap({
      // Keep search, 404, helper pages and paginated archives (/page/2/ and up) out of the sitemap.
      filter: (page) =>
        !page.includes('/search/') && !page.includes('/404') && !page.includes('/shared-chrome/') && !comingSoon.includes(page) && !/\/page\/\d+\/$/.test(page),
      serialize(item) {
        const d = lastmod[item.url] || (item.url === 'https://brandella.in/' ? newest : undefined);
        if (d) item.lastmod = d;
        return item;
      },
    }),
  ],
});
