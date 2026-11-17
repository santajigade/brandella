// SEO and AEO Growth Assets library (/resources/seo-aeo-assets/).
// index.json lists all 36 assets. An asset goes live when src/data/seo-assets/<slug>.yaml exists.
import { parse as parseYaml } from 'yaml';
import indexJson from '../data/seo-assets/index.json';

export const LIBRARY = {
  url: '/resources/seo-aeo-assets/',
  name: 'SEO and AEO Growth Assets',
  downloads: '/resources/seo-aeo-assets/downloads/',
};

export interface AssetMeta { n: number; slug: string; name: string; group: string; short: string; formats: string[] }
export interface Asset extends AssetMeta {
  seoTitle: string;
  h1: string;
  focusKeyword: string;
  description: string;
  published: string;
  updated: string;
  time: string;
  level: string;
  intro: string[];
  template?: { name: string; intro?: string; columns: string[]; formulas?: Record<string, string>; rows: (string | number)[][]; note?: string };
  steps: { t: string; d: string }[];
  sections?: { h: string; html: string }[];
  prompts: { t: string; p: string }[];
  checklist: string[];
  faq: { q: string; a: string }[];
  related: string[];
  reads: { t: string; url: string }[];
  tools: { t: string; url: string }[];
  sources: { t: string; url: string }[];
}

export const groups: { id: string; name: string }[] = indexJson.groups;
export const allAssets: AssetMeta[] = indexJson.assets;

const files = import.meta.glob('../data/seo-assets/*.yaml', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;
const content = new Map<string, any>();
for (const [path, raw] of Object.entries(files)) {
  const data = parseYaml(raw);
  const slug = path.split('/').pop()!.replace(/\.yaml$/, '');
  content.set(slug, data);
}

export const liveAssets: Asset[] = allAssets
  .filter((a) => content.has(a.slug))
  .map((a) => ({ ...a, ...content.get(a.slug) }));

export const isLive = (slug: string) => content.has(slug);
export const assetUrl = (slug: string) => `${LIBRARY.url}${slug}/`;
export const groupName = (id: string) => groups.find((g) => g.id === id)?.name ?? id;
export const pad = (n: number) => String(n).padStart(2, '0');

/** Cell value for the CSV: formulas are written with the real spreadsheet row number. */
export function csvFor(a: Asset) {
  const t = a.template!;
  const esc = (v: string | number) => {
    const s = String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [t.columns.map(esc).join(',')];
  t.rows.forEach((row, i) => {
    const r = i + 2;
    lines.push(row.map((v, c) => {
      const f = t.formulas?.[String(c)];
      return esc(f ? `=${f.replaceAll('{r}', String(r))}` : v);
    }).join(','));
  });
  // BOM so Excel opens UTF-8 correctly
  return '﻿' + lines.join('\r\n') + '\r\n';
}

export function promptsTxt(a: Asset) {
  const out = [
    `${a.h1}: AI prompts and checklist`,
    `From Brandella Journal, free to use: https://brandella.in${assetUrl(a.slug)}`,
    '',
    'Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini.',
    '',
  ];
  a.prompts.forEach((p, i) => out.push(`${i + 1}. ${p.t}`, '', p.p.trim(), '', ''));
  out.push('CHECKLIST', '');
  a.checklist.forEach((c) => out.push(`[ ] ${c}`));
  return out.join('\r\n') + '\r\n';
}

export const fileNames = (slug: string) => ({ csv: `${slug}-template.csv`, txt: `${slug}-prompts-checklist.txt` });
