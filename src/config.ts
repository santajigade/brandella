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
export const TOOL_CATEGORIES = [
  { slug: 'seo-tools', name: 'SEO Tools' },
  { slug: 'schema-generators', name: 'Schema Generators' },
  { slug: 'ppc-calculators', name: 'PPC Calculators' },
  { slug: 'analytics-tools', name: 'Analytics Tools' },
  { slug: 'social-media-tools', name: 'Social Media Tools' },
  { slug: 'technical-seo-tools', name: 'Technical SEO Tools' },
  { slug: 'google-ads-tools', name: 'Google Ads Tools' },
  { slug: 'ai-tools', name: 'AI Tools' },
].map((t) => ({ ...t, url: `${TOOLS_URL}${t.slug}/` }));
