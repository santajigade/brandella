// Site wide settings. Never use em dash or en dash characters in site text.
export const SITE = {
  name: 'Brandella Journal',
  url: 'https://brandella.in',
  tagline: 'SEO, paid media, AI search and web development, explained.',
  description:
    'Brandella Journal publishes practical guides on SEO, paid media, content, social, AI search and web development for marketers.',
  locale: 'en_IN',
  postsPerPage: 12,
  // AdSense publisher id (leave empty to switch every ad slot off)
  adsenseClient: 'ca-pub-3931314195561246',
  adsenseSlot: '4249015278',
  social: {
    linkedin: 'https://www.linkedin.com/in/santaji-gadepatil6680/',
  },
  // Brand profiles, shown in the header and footer (also on /tools/)
  profiles: [
    { name: 'LinkedIn', url: 'https://www.linkedin.com/company/brandellajournal/' },
    { name: 'Facebook', url: 'https://www.facebook.com/brandellajournal/' },
    { name: 'Instagram', url: 'https://www.instagram.com/brandellajournal/' },
    { name: 'Pinterest', url: 'https://www.pinterest.com/brandellajournal/' },
  ],
  email: 'admin@brandella.in',
};

// Top menu order, by category slug
export const MENU = [
  'seo',
  'paid-media',
  'content',
  'social',
  'digital-marketing',
  'artificial-intelligence',
  'development',
];

// Free tools live at /tools/ and are deployed by the brandella-tools repo.
// Never generate any page under /tools/ from this site.
export const TOOLS_URL = 'https://brandella.in/tools/';
// Tool categories come from the tools site (tools/categories.json, written by the
// brandella-tools build) so new categories show in this menu at the next build.
// The list below is the fallback when that file cannot be fetched.
const FALLBACK_TOOL_CATEGORIES = [
  { slug: 'seo-tools', name: 'SEO Tools' },
  { slug: 'schema-generators', name: 'Schema Generators' },
  { slug: 'ppc-calculators', name: 'PPC Calculators' },
  { slug: 'analytics-tools', name: 'Analytics Tools' },
  { slug: 'social-media-tools', name: 'Social Media Tools' },
  { slug: 'technical-seo-tools', name: 'Technical SEO Tools' },
  { slug: 'google-ads-tools', name: 'Google Ads Tools' },
  { slug: 'ai-tools', name: 'AI Tools' },
  { slug: 'developer-tools', name: 'Developer Tools' },
];
async function loadToolCategories(): Promise<{ slug: string; name: string }[]> {
  try {
    const res = await fetch(`${TOOLS_URL}categories.json`, { signal: AbortSignal.timeout(8000) });
    if (!res.ok) throw new Error(String(res.status));
    const list = await res.json();
    const ok = Array.isArray(list) && list.length > 0 && list.every((c) => typeof c?.slug === 'string' && /^[a-z0-9-]+$/.test(c.slug) && typeof c?.name === 'string');
    return ok ? list.map((c) => ({ slug: c.slug, name: c.name })) : FALLBACK_TOOL_CATEGORIES;
  } catch {
    return FALLBACK_TOOL_CATEGORIES;
  }
}
export const TOOL_CATEGORIES = (await loadToolCategories()).map((t) => ({ ...t, url: `${TOOLS_URL}${t.slug}/` }));
