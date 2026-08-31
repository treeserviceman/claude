'use strict';
const fs = require('fs');
const path = require('path');
const { buildSiteCtx, renderIndex, renderServices, renderServiceArea, renderFaq, renderContact, renderSinglePage } = require('./lib/render');

const records = require('../data/sites.json');
const sitesDir = path.join(__dirname, '..', 'sites');

const onlySlug = process.argv[2]; // optional: regenerate a single site by slug
const domainOverridesPath = path.join(__dirname, '..', 'data', 'domain-overrides.json');
const domainOverrides = fs.existsSync(domainOverridesPath) ? JSON.parse(fs.readFileSync(domainOverridesPath, 'utf8')) : {};

let count = 0;
for (const record of records) {
  if (onlySlug && record.slug !== onlySlug) continue;
  const domain = domainOverrides[record.slug] || `${record.slug}.netlify.app`;
  const ctx = buildSiteCtx(record, domain);
  const dir = path.join(sitesDir, record.slug);
  fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(path.join(dir, 'index.html'), renderIndex(ctx));
  fs.writeFileSync(path.join(dir, 'services.html'), renderServices(ctx));
  fs.writeFileSync(path.join(dir, 'service-area.html'), renderServiceArea(ctx));
  fs.writeFileSync(path.join(dir, 'faq.html'), renderFaq(ctx));
  fs.writeFileSync(path.join(dir, 'contact.html'), renderContact(ctx));
  // Single-file bundle: the deployable artifact (see DEPLOY_NOTES). Multi-page files above are kept as source/reference.
  fs.writeFileSync(path.join(dir, 'bundle.html'), renderSinglePage(ctx));

  fs.writeFileSync(path.join(dir, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: https://${domain}/sitemap.xml\n`);

  const pages = ['', 'services.html', 'service-area.html', 'faq.html', 'contact.html'];
  const now = new Date().toISOString().slice(0, 10);
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((p) => `  <url><loc>https://${domain}/${p}</loc><lastmod>${now}</lastmod></url>`).join('\n')}\n</urlset>\n`;
  fs.writeFileSync(path.join(dir, 'sitemap.xml'), sitemap);

  fs.writeFileSync(path.join(dir, 'netlify.toml'), `[build]\n  publish = "."\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Robots-Tag = "index, follow"\n`);

  count++;
}
console.log(`Generated ${count} site(s) into ${sitesDir}`);
