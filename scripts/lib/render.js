'use strict';
const {
  hash, pick, pickN, compose, THEMES, HERO_STYLES, HEADER_STYLES, SERVICE_STYLES, FOOTER_STYLES,
  HERO_KICKERS, HERO_HEADLINES, HERO_SUBS,
  INTRO_OPENERS, INTRO_DETAILS, INTRO_CLOSERS,
  SIGNS, WHY_US, SERVICES, FAQS, CTA_LINES,
  SERVICES_INTRO_LINES, SERVICE_AREA_LEADS, FAQ_INTRO_LINES,
  EYEBROW_WHY, EYEBROW_SERVICES, EYEBROW_AREA, EYEBROW_FAQ, EYEBROW_CONTACT, EYEBROW_WHYUS,
  H2_INTRO, H2_SERVICES_PREVIEW, H2_AREA_INDEX, H1_SERVICES, H1_SERVICE_AREA,
  H2_AREA_LOCAL, H1_FAQ, H1_CONTACT, H3_SIGNS, H2_CTA, H2_WHYUS_DIFF,
} = require('./content');
const { PHONE_RAW, PHONE_DISPLAY } = require('./data');

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function fill(tpl, loc, biz) {
  return tpl.replace(/\{LOC\}/g, loc).replace(/\{PHONE\}/g, PHONE_DISPLAY).replace(/\{BIZ\}/g, biz || '');
}

function buildSiteCtx(record, domain) {
  const slug = record.slug;
  const theme = pick(slug + 'theme', THEMES);
  const heroStyle = pick(slug + 'hero', HERO_STYLES);
  const headerStyle = pick(slug + 'header', HEADER_STYLES);
  const serviceStyle = pick(slug + 'svc', SERVICE_STYLES);
  const footerStyle = pick(slug + 'foot', FOOTER_STYLES);

  const loc = record.localityDisplay + (record.stateAbbr ? `, ${record.stateAbbr.toUpperCase()}` : '');
  const locNoState = record.localityDisplay;
  const stateFull = record.stateInfo ? record.stateInfo.name : '';
  const region = record.stateInfo ? record.stateInfo.region : 'your area';
  const climate = record.stateInfo ? record.stateInfo.climate : 'seasonal weather swings that push wildlife to seek shelter indoors';
  const areaNoun = record.isCounty ? 'county' : 'area';

  const businessName = `${loc} Raccoon Removal`;
  const mapQuery = encodeURIComponent(`${loc}`);

  const hero = {
    kicker: pick(slug + 'k', HERO_KICKERS),
    headline: fill(pick(slug + 'h', HERO_HEADLINES), loc),
    sub: fill(pick(slug + 's', HERO_SUBS), loc),
  };
  const intro = fill(compose(slug + 'intro', [INTRO_OPENERS, INTRO_DETAILS, INTRO_CLOSERS]), loc);
  const signs = pickN(slug + 'signs', SIGNS, 6);
  const whyUs = pickN(slug + 'why', WHY_US, 5).map((w) => ({ t: w.t, d: fill(w.d, loc) }));
  const services = pickN(slug + 'svcs', SERVICES, 8);
  const faqs = pickN(slug + 'faq', FAQS, 6).map((f) => ({ q: fill(f.q, loc), a: fill(f.a, loc) }));
  const cta = fill(pick(slug + 'cta', CTA_LINES), loc);
  const servicesIntro = fill(pick(slug + 'svcintro', SERVICES_INTRO_LINES), loc);
  const serviceAreaLead = fill(pick(slug + 'arealead', SERVICE_AREA_LEADS), loc);
  const faqIntro = fill(pick(slug + 'faqintro', FAQ_INTRO_LINES), loc);

  const heads = {
    eyebrowWhy: pick(slug + 'ew', EYEBROW_WHY),
    eyebrowServices: pick(slug + 'es', EYEBROW_SERVICES),
    eyebrowArea: pick(slug + 'ea', EYEBROW_AREA),
    eyebrowFaq: pick(slug + 'ef', EYEBROW_FAQ),
    eyebrowContact: pick(slug + 'ec', EYEBROW_CONTACT),
    eyebrowWhyUs: pick(slug + 'ewu', EYEBROW_WHYUS),
    h2Intro: fill(pick(slug + 'h2i', H2_INTRO), loc),
    h2ServicesPreview: pick(slug + 'h2sp', H2_SERVICES_PREVIEW),
    h2AreaIndex: fill(pick(slug + 'h2ai', H2_AREA_INDEX), loc),
    h1Services: fill(pick(slug + 'h1s', H1_SERVICES), loc),
    h1ServiceArea: fill(pick(slug + 'h1sa', H1_SERVICE_AREA), loc),
    h2AreaLocal: fill(pick(slug + 'h2al', H2_AREA_LOCAL), loc),
    h1Faq: fill(pick(slug + 'h1f', H1_FAQ), loc),
    h1Contact: fill(pick(slug + 'h1c', H1_CONTACT), loc, businessName),
    h3Signs: pick(slug + 'h3s', H3_SIGNS),
    h2Cta: pick(slug + 'h2c', H2_CTA),
    h2WhyUsDiff: fill(pick(slug + 'h2wd', H2_WHYUS_DIFF), loc),
  };
  // Structural variation: swap column order on a few two-column sections so
  // the DOM/reading order differs, not just the wording.
  const flipIntroCols = hash(slug + 'flip1') % 2 === 0;
  const flipAreaCols = hash(slug + 'flip2') % 2 === 0;
  const flipIndexAreaCols = hash(slug + 'flip3') % 2 === 0;

  return {
    slug, domain, theme, heroStyle, headerStyle, serviceStyle, footerStyle,
    loc, locNoState, stateFull, region, climate, areaNoun, businessName, mapQuery,
    hero, intro, signs, whyUs, services, faqs, cta, servicesIntro, serviceAreaLead, faqIntro,
    heads, flipIntroCols, flipAreaCols, flipIndexAreaCols,
    record,
  };
}

function styleSheet(ctx) {
  const t = ctx.theme;
  const fonts = [t.headingFont, t.bodyFont].join('|');
  const googleFontFamilies = [...new Set([t.headingFont, t.bodyFont])]
    .map((f) => f.split(',')[0].replace(/'/g, '').trim())
    .filter((f) => !['Arial', 'Georgia'].includes(f));
  const fontLink = googleFontFamilies.length
    ? `https://fonts.googleapis.com/css2?${googleFontFamilies.map((f) => `family=${f.replace(/ /g, '+')}:wght@400;600;700;800`).join('&')}&display=swap`
    : null;

  return { fontLink, css: `
:root{
  --bg:${t.bg}; --surface:${t.surface}; --ink:${t.ink}; --accent:${t.accent}; --accent2:${t.accent2}; --radius:${t.radius};
  --ink-soft:${t.dark ? 'rgba(241,244,247,.72)' : 'rgba(40,32,24,.68)'};
  --border:${t.dark ? 'rgba(255,255,255,.12)' : 'rgba(0,0,0,.08)'};
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:${t.bodyFont};line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:${t.headingFont};line-height:1.15;margin:0 0 .5em}
h1{font-size:clamp(2rem,5vw,3.2rem)}
h2{font-size:clamp(1.5rem,3vw,2.2rem)}
p{margin:0 0 1em}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.section{padding:64px 0}
.section-tight{padding:40px 0}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-weight:700;font-size:.78rem;color:var(--accent)}
.btn{display:inline-flex;align-items:center;gap:.5em;background:var(--accent);color:#fff;padding:14px 26px;border-radius:var(--radius);font-weight:700;text-decoration:none;box-shadow:0 8px 22px -8px ${t.accent}99}
.btn.secondary{background:transparent;border:2px solid var(--accent);color:var(--ink)}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:26px}
.grid{display:grid;gap:22px}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}

header.site{position:sticky;top:0;z-index:40;background:${t.dark ? t.surface : t.surface}ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--border)}
header.site .bar{display:flex;align-items:center;justify-content:space-between;padding:16px 0}
header.site.stacked .bar{flex-direction:column;text-align:center;gap:10px;padding:22px 0}
.brand{font-family:${t.headingFont};font-weight:800;font-size:1.15rem;text-decoration:none;color:var(--ink)}
nav.main a{margin-left:22px;text-decoration:none;font-weight:600;color:var(--ink-soft);font-size:.95rem}
header.site.stacked nav.main a{margin:0 10px}
.header-call{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:999px;font-weight:800;text-decoration:none;white-space:nowrap}

.hero{position:relative;overflow:hidden}
.hero-banner{background:linear-gradient(135deg,var(--accent) 0%,var(--accent2) 100%);color:#fff;text-align:center;padding:90px 0}
.hero-banner .eyebrow{color:#fff;opacity:.85}
.hero-banner .hero-sub{color:rgba(255,255,255,.9)}
.hero-centered{padding:90px 0 60px;text-align:center}
.hero-centered .hero-sub{max-width:680px;margin:0 auto 1.4em}
.hero-split{padding:80px 0}
.hero-split .grid-2{align-items:center}
.hero-art{aspect-ratio:4/3;border-radius:calc(var(--radius) + 6px);background:radial-gradient(circle at 30% 30%,${t.accent}33,transparent 60%),radial-gradient(circle at 70% 70%,${t.accent2}33,transparent 60%),var(--surface);border:1px solid var(--border);display:flex;align-items:center;justify-content:center}
.hero-sub{font-size:1.15rem;color:var(--ink-soft);max-width:560px}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap;margin-top:1.6em}
.hero-centered .hero-actions{justify-content:center}

.signs-list, .why-list{list-style:none;margin:0;padding:0;display:grid;gap:16px}
.signs-list li, .why-list li{display:flex;gap:14px;align-items:flex-start}
.dot{flex:none;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.9rem}

.services-grid .card{transition:transform .15s ease}
.services-list .svc-row{display:flex;gap:18px;padding:18px 0;border-bottom:1px solid var(--border)}
.services-list .svc-row:last-child{border-bottom:none}
.svc-num{font-family:${t.headingFont};font-weight:800;color:var(--accent);font-size:1.3rem;flex:none;width:44px}

.map-frame{border-radius:var(--radius);overflow:hidden;border:1px solid var(--border);aspect-ratio:16/9;width:100%}
.map-frame iframe{width:100%;height:100%;border:0}

.faq details{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;margin-bottom:12px}
.faq summary{font-weight:700;cursor:pointer;list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq summary:before{content:'+ ';color:var(--accent);font-weight:800}
.faq details[open] summary:before{content:'– '}
.faq p{margin-top:12px;color:var(--ink-soft)}

.cta-band{background:${t.dark ? t.surface : '#1c2432'};color:#fff;text-align:center;padding:54px 0;border-radius:calc(var(--radius) + 4px);margin:0 20px}
.cta-band h2{color:#fff}
.cta-band .btn{background:var(--accent)}

footer.site{border-top:1px solid var(--border);padding:50px 0 30px;color:var(--ink-soft);font-size:.92rem}
footer.site .grid-4{display:grid;gap:26px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
footer.site h4{color:var(--ink);font-size:.95rem;margin:0 0 10px}
footer.site .brand-block{max-width:340px}
.legal-line{margin-top:30px;padding-top:20px;border-top:1px solid var(--border);font-size:.82rem}

.float-call{position:fixed;right:18px;bottom:18px;z-index:100;display:flex;align-items:center;gap:10px;background:var(--accent);color:#fff;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:800;box-shadow:0 10px 28px -6px rgba(0,0,0,.4);animation:floatPulse 2.4s ease-in-out infinite}
.float-call svg{flex:none}
@keyframes floatPulse{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.top-callbar{background:${t.accent};color:#fff;text-align:center;font-weight:700;font-size:.88rem;padding:8px 12px}
.top-callbar a{color:#fff;text-decoration:underline}

@media (max-width:640px){
  nav.main{display:none}
  .float-call span.long{display:none}
  .cta-band{margin:0}
}
`};
}

function svgRaccoon() {
  return `<svg width="86" height="86" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="12" cy="12" r="11" fill="currentColor" opacity=".12"/>
  <path d="M7 9c-1.5 0-2.5 1.2-2.5 2.6 0 1 .5 1.8 1.3 2.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
  <path d="M17 9c1.5 0 2.5 1.2 2.5 2.6 0 1-.5 1.8-1.3 2.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
  <path d="M6.5 12.5c0-3.6 2.6-6.2 5.5-6.2s5.5 2.6 5.5 6.2c0 3.1-2.2 5.6-5.5 5.6s-5.5-2.5-5.5-5.6Z" fill="currentColor" opacity=".2" stroke="currentColor" stroke-width="1.2"/>
  <path d="M9 11.2c.5-1 1.7-1 2.2 0M13 11.2c.5-1 1.7-1 2.2 0" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
  <circle cx="10" cy="13" r=".9" fill="currentColor"/>
  <circle cx="14" cy="13" r=".9" fill="currentColor"/>
  <path d="M11 14.6c.4.5 1.6.5 2 0" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
</svg>`;
}

function phoneIcon() {
  return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.9 21 3 13.1 3 3.5c0-.6.4-1 1-1H7.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1L6.6 10.8Z" fill="currentColor"/></svg>`;
}

function head(ctx, page) {
  const s = styleSheet(ctx);
  const canonical = `https://${ctx.domain}/${page.path}`;
  return `<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(page.title)}</title>
<meta name="description" content="${esc(page.description)}">
<link rel="canonical" href="${canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="${esc(page.title)}">
<meta property="og:description" content="${esc(page.description)}">
<meta property="og:url" content="${canonical}">
<meta name="twitter:card" content="summary">
${s.fontLink ? `<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="${s.fontLink}" rel="stylesheet">` : ''}
<link rel="icon" href="data:,">
<style>${s.css}</style>
<script type="application/ld+json">${JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'LocalBusiness',
  name: ctx.businessName,
  telephone: PHONE_RAW,
  url: `https://${ctx.domain}/`,
  areaServed: ctx.loc,
  description: `Humane raccoon removal, attic exclusion, and wildlife damage repair serving ${ctx.loc}.`,
  priceRange: '$$',
})}</script>`;
}

function headerNav(ctx, links) {
  const l = links || { home: 'index.html', services: 'services.html', area: 'service-area.html', faq: 'faq.html', contact: 'contact.html' };
  const cls = ctx.headerStyle === 'stacked' ? 'site stacked' : 'site';
  return `<div class="top-callbar">Raccoon in the attic? Call now: <a href="tel:${PHONE_RAW}">${PHONE_DISPLAY}</a></div>
<header class="${cls}">
  <div class="wrap bar">
    <a class="brand" href="${l.home}">${esc(ctx.businessName)}</a>
    <nav class="main">
      <a href="${l.home}">Home</a>
      <a href="${l.services}">Services</a>
      <a href="${l.area}">Service Area</a>
      <a href="${l.faq}">FAQ</a>
      <a href="${l.contact}">Contact</a>
    </nav>
    <a class="header-call" href="tel:${PHONE_RAW}">${phoneIcon()} ${PHONE_DISPLAY}</a>
  </div>
</header>`;
}

function floatCall() {
  return `<a class="float-call" href="tel:${PHONE_RAW}" aria-label="Call ${PHONE_DISPLAY}">${phoneIcon()}<span class="long">Call Now:</span> ${PHONE_DISPLAY}</a>`;
}

function footer(ctx, links) {
  const l = links || { home: 'index.html', services: 'services.html', area: 'service-area.html', faq: 'faq.html', contact: 'contact.html' };
  return `<footer class="site">
  <div class="wrap">
    <div class="grid-4">
      <div class="brand-block">
        <h4>${esc(ctx.businessName)}</h4>
        <p>Humane raccoon trapping, attic exclusion, and damage repair serving homeowners and businesses throughout ${esc(ctx.loc)}.</p>
        <p><a class="btn secondary" href="tel:${PHONE_RAW}">${phoneIcon()} ${PHONE_DISPLAY}</a></p>
      </div>
      <div>
        <h4>Services</h4>
        <p><a href="${l.services}">Raccoon Trapping &amp; Removal</a><br>
        <a href="${l.services}">Attic Exclusion</a><br>
        <a href="${l.services}">Damage Repair</a><br>
        <a href="${l.services}">Chimney &amp; Crawl Space Removal</a></p>
      </div>
      <div>
        <h4>Company</h4>
        <p><a href="${l.area}">Service Area</a><br>
        <a href="${l.faq}">FAQ</a><br>
        <a href="${l.contact}">Contact</a></p>
      </div>
      <div>
        <h4>Hours</h4>
        <p>Mon–Sat 7am–7pm<br>24/7 Emergency Line<br>${esc(ctx.loc)} &amp; surrounding ${esc(ctx.areaNoun)}</p>
      </div>
    </div>
    <div class="legal-line">© ${new Date().getFullYear()} ${esc(ctx.businessName)}. Licensed &amp; insured wildlife control. Humane methods only.</div>
  </div>
</footer>`;
}

function heroSection(ctx, contactHref) {
  contactHref = contactHref || 'contact.html';
  if (ctx.heroStyle === 'banner') {
    return `<section class="hero hero-banner" id="top">
  <div class="wrap">
    <div class="eyebrow">${esc(ctx.hero.kicker)}</div>
    <h1>${esc(ctx.hero.headline)}</h1>
    <p class="hero-sub" style="margin:0 auto">${esc(ctx.hero.sub)}</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn" style="background:#fff;color:var(--accent)" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY}</a>
      <a class="btn secondary" style="border-color:#fff;color:#fff" href="${contactHref}">Request Inspection</a>
    </div>
  </div>
</section>`;
  }
  if (ctx.heroStyle === 'centered') {
    return `<section class="hero hero-centered" id="top">
  <div class="wrap">
    <div class="eyebrow">${esc(ctx.hero.kicker)}</div>
    <h1>${esc(ctx.hero.headline)}</h1>
    <p class="hero-sub">${esc(ctx.hero.sub)}</p>
    <div class="hero-actions">
      <a class="btn" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY}</a>
      <a class="btn secondary" href="${contactHref}">Request Inspection</a>
    </div>
  </div>
</section>`;
  }
  return `<section class="hero hero-split" id="top">
  <div class="wrap grid grid-2">
    <div>
      <div class="eyebrow">${esc(ctx.hero.kicker)}</div>
      <h1>${esc(ctx.hero.headline)}</h1>
      <p class="hero-sub">${esc(ctx.hero.sub)}</p>
      <div class="hero-actions">
        <a class="btn" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY}</a>
        <a class="btn secondary" href="${contactHref}">Request Inspection</a>
      </div>
    </div>
    <div class="hero-art" style="color:var(--accent)">${svgRaccoon()}</div>
  </div>
</section>`;
}

function ctaBand(ctx) {
  return `<section class="section-tight"><div class="wrap"><div class="cta-band"><h2>${esc(ctx.heads.h2Cta)}</h2><p style="color:rgba(255,255,255,.85)">${esc(ctx.cta)}</p><a class="btn" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY} Now</a></div></div></section>`;
}

function mapEmbed(ctx) {
  return `<div class="map-frame"><iframe src="https://maps.google.com/maps?q=${ctx.mapQuery}&t=&z=10&ie=UTF8&iwloc=&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of ${esc(ctx.loc)}"></iframe></div>`;
}

function pageShell(ctx, page, bodyHtml) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
${head(ctx, page)}
</head>
<body>
${headerNav(ctx)}
${bodyHtml}
${footer(ctx)}
${floatCall()}
</body>
</html>`;
}

function renderIndex(ctx) {
  const signsHtml = ctx.signs.map((s, i) => `<li><span class="dot">${i + 1}</span><div><strong>${esc(s.t)}</strong><p style="margin:.2em 0 0">${esc(s.d)}</p></div></li>`).join('');
  const whyHtml = ctx.whyUs.map((w) => `<li><span class="dot">✓</span><div><strong>${esc(w.t)}</strong><p style="margin:.2em 0 0">${esc(w.d)}</p></div></li>`).join('');
  const svcPreview = ctx.services.slice(0, 6).map((s) => `<div class="card"><h3 style="font-size:1.1rem">${esc(s.t)}</h3><p style="color:var(--ink-soft)">${esc(s.d)}</p></div>`).join('');

  const introCol = `<div>
      <div class="eyebrow">${esc(ctx.heads.eyebrowWhy)}</div>
      <h2>${esc(ctx.heads.h2Intro)}</h2>
      <p>${esc(ctx.intro)}</p>
      <p>Homes and businesses across ${esc(ctx.loc)} deal with ${esc(ctx.climate)} — exactly the conditions that send raccoons looking for a warm, dry attic to den in.</p>
    </div>`;
  const signsCol = `<div class="card">
      <h3>${esc(ctx.heads.h3Signs)}</h3>
      <ul class="signs-list">${signsHtml}</ul>
    </div>`;

  const areaCol = `<div>
      <div class="eyebrow">${esc(ctx.heads.eyebrowArea)}</div>
      <h2>${esc(ctx.heads.h2AreaIndex)}</h2>
      <p>We respond to homes and businesses throughout ${esc(ctx.loc)} and the surrounding ${esc(ctx.areaNoun)}.</p>
      ${mapEmbed(ctx)}
      <p style="margin-top:14px"><a class="btn secondary" href="service-area.html">Full Service Area</a></p>
    </div>`;
  const whyCol = `<ul class="why-list">${whyHtml}</ul>`;

  const body = `
${heroSection(ctx)}
<section class="section">
  <div class="wrap grid grid-2" style="align-items:center">
    ${ctx.flipIntroCols ? signsCol + introCol : introCol + signsCol}
  </div>
</section>

<section class="section" style="background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="wrap">
    <div class="eyebrow">${esc(ctx.heads.eyebrowServices)}</div>
    <h2>${esc(ctx.heads.h2ServicesPreview)}</h2>
    <div class="grid grid-3" style="margin-top:26px">${svcPreview}</div>
    <p style="margin-top:24px"><a class="btn secondary" href="services.html">See All Services</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-2" style="align-items:center">
    ${ctx.flipIndexAreaCols ? areaCol + whyCol : whyCol + areaCol}
  </div>
</section>
${ctaBand(ctx)}
`;
  return pageShell(ctx, { path: '', title: `Raccoon Removal ${ctx.loc} | ${ctx.businessName}`, description: `Humane raccoon removal in ${ctx.loc}. Attic exclusion, trapping, and damage repair. Call ${PHONE_DISPLAY} for fast, licensed service.` }, body);
}

function renderServices(ctx) {
  const items = ctx.serviceStyle === 'list'
    ? `<div class="services-list">${ctx.services.map((s, i) => `<div class="svc-row"><div class="svc-num">${String(i + 1).padStart(2, '0')}</div><div><h3 style="margin:0 0 .3em">${esc(s.t)}</h3><p style="color:var(--ink-soft);margin:0">${esc(s.d)}</p></div></div>`).join('')}</div>`
    : `<div class="grid grid-3 services-grid">${ctx.services.map((s) => `<div class="card"><h3 style="font-size:1.15rem">${esc(s.t)}</h3><p style="color:var(--ink-soft)">${esc(s.d)}</p></div>`).join('')}</div>`;

  const body = `
<section class="section-tight"><div class="wrap"><div class="eyebrow">${esc(ctx.heads.eyebrowServices)}</div><h1>${esc(ctx.heads.h1Services)}</h1><p class="hero-sub">${esc(ctx.servicesIntro)}</p></div></section>
<section class="section"><div class="wrap">${items}</div></section>
${ctaBand(ctx)}
`;
  return pageShell(ctx, { path: 'services.html', title: `Raccoon Removal Services | ${ctx.businessName}`, description: `Trapping, attic exclusion, chimney removal, and damage repair for raccoon problems in ${ctx.loc}. Licensed & insured.` }, body);
}

function renderServiceArea(ctx) {
  const textCol = `<div>
      <h2>${esc(ctx.heads.h2AreaLocal)}</h2>
      <p>${esc(ctx.stateFull ? `Homes and businesses across ${esc(ctx.stateFull)}` : `Properties across ${esc(ctx.loc)}`)} deal with ${esc(ctx.climate)}. That means raccoon activity picks up every year as the weather turns, and attics, chimneys, and crawl spaces in ${esc(ctx.loc)} become prime denning spots.</p>
      <p>${esc(ctx.serviceAreaLead)}</p>
      <ul class="why-list">
        <li><span class="dot">✓</span><div><strong>Residential service</strong><p style="margin:.2em 0 0">Single-family homes, townhomes, and condos throughout ${esc(ctx.loc)}.</p></div></li>
        <li><span class="dot">✓</span><div><strong>Commercial service</strong><p style="margin:.2em 0 0">Retail, restaurants, warehouses, and multi-family buildings.</p></div></li>
        <li><span class="dot">✓</span><div><strong>Emergency response</strong><p style="margin:.2em 0 0">Same-day and next-day appointments for active attic intrusions.</p></div></li>
      </ul>
    </div>`;
  const mapCol = `<div>${mapEmbed(ctx)}</div>`;
  const body = `
<section class="section-tight"><div class="wrap"><div class="eyebrow">${esc(ctx.heads.eyebrowArea)}</div><h1>${esc(ctx.heads.h1ServiceArea)}</h1><p class="hero-sub">We provide raccoon removal and wildlife exclusion throughout ${esc(ctx.loc)} and the surrounding ${esc(ctx.areaNoun)}, for both residential and commercial properties.</p></div></section>
<section class="section">
  <div class="wrap grid grid-2" style="align-items:start">
    ${ctx.flipAreaCols ? mapCol + textCol : textCol + mapCol}
  </div>
</section>
${ctaBand(ctx)}
`;
  return pageShell(ctx, { path: 'service-area.html', title: `${ctx.loc} Service Area | ${ctx.businessName}`, description: `We provide raccoon removal throughout ${ctx.loc} and the surrounding ${ctx.areaNoun}. Residential and commercial wildlife control.` }, body);
}

function renderFaq(ctx) {
  const items = ctx.faqs.map((f) => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join('');
  const body = `
<section class="section-tight"><div class="wrap"><div class="eyebrow">${esc(ctx.heads.eyebrowFaq)}</div><h1>${esc(ctx.heads.h1Faq)}</h1><p class="hero-sub">${esc(ctx.faqIntro)}</p></div></section>
<section class="section"><div class="wrap faq" style="max-width:820px">${items}</div></section>
${ctaBand(ctx)}
`;
  return pageShell(ctx, { path: 'faq.html', title: `Raccoon Removal FAQ | ${ctx.businessName}`, description: `Common questions about humane raccoon removal, cost, and timelines in ${ctx.loc}.` }, body);
}

function renderContact(ctx) {
  const body = `
<section class="section-tight"><div class="wrap"><div class="eyebrow">${esc(ctx.heads.eyebrowContact)}</div><h1>${esc(ctx.heads.h1Contact)}</h1><p class="hero-sub">Call now for a fast inspection, or reach out with details about what you're hearing or seeing.</p></div></section>
<section class="section">
  <div class="wrap grid grid-2" style="align-items:start">
    <div class="card">
      <h3>Call Us</h3>
      <p style="font-size:1.6rem;font-weight:800"><a href="tel:${PHONE_RAW}">${PHONE_DISPLAY}</a></p>
      <p>Mon–Sat 7am–7pm · 24/7 emergency line</p>
      <h3 style="margin-top:22px">Service Area</h3>
      <p>${esc(ctx.loc)} and surrounding ${esc(ctx.areaNoun)}</p>
      <a class="btn" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY}</a>
    </div>
    <div>${mapEmbed(ctx)}</div>
  </div>
</section>
`;
  return pageShell(ctx, { path: 'contact.html', title: `Contact Us | ${ctx.businessName}`, description: `Call ${PHONE_DISPLAY} to reach the ${ctx.loc} raccoon removal team. Fast, humane, licensed service.` }, body);
}

function renderSinglePage(ctx) {
  const links = { home: '#top', services: '#services', area: '#service-area', faq: '#faq', contact: '#contact' };
  const signsHtml = ctx.signs.map((s, i) => `<li><span class="dot">${i + 1}</span><div><strong>${esc(s.t)}</strong><p style="margin:.2em 0 0">${esc(s.d)}</p></div></li>`).join('');
  const whyHtml = ctx.whyUs.map((w) => `<li><span class="dot">✓</span><div><strong>${esc(w.t)}</strong><p style="margin:.2em 0 0">${esc(w.d)}</p></div></li>`).join('');
  const svcHtml = ctx.serviceStyle === 'list'
    ? `<div class="services-list">${ctx.services.map((s, i) => `<div class="svc-row"><div class="svc-num">${String(i + 1).padStart(2, '0')}</div><div><h3 style="margin:0 0 .3em">${esc(s.t)}</h3><p style="color:var(--ink-soft);margin:0">${esc(s.d)}</p></div></div>`).join('')}</div>`
    : `<div class="grid grid-3 services-grid">${ctx.services.map((s) => `<div class="card"><h3 style="font-size:1.15rem">${esc(s.t)}</h3><p style="color:var(--ink-soft)">${esc(s.d)}</p></div>`).join('')}</div>`;
  const faqHtml = ctx.faqs.map((f) => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join('');

  const body = `
${heroSection(ctx, '#contact')}

<section class="section">
  <div class="wrap grid grid-2" style="align-items:center">
    <div>
      <div class="eyebrow">${esc(ctx.heads.eyebrowWhy)}</div>
      <h2>${esc(ctx.heads.h2Intro)}</h2>
      <p>${esc(ctx.intro)}</p>
      <p>Homes and businesses across ${esc(ctx.loc)} deal with ${esc(ctx.climate)} — exactly the conditions that send raccoons looking for a warm, dry attic to den in.</p>
    </div>
    <div class="card">
      <h3>${esc(ctx.heads.h3Signs)}</h3>
      <ul class="signs-list">${signsHtml}</ul>
    </div>
  </div>
</section>

<section class="section" id="services" style="background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="wrap">
    <div class="eyebrow">${esc(ctx.heads.eyebrowServices)}</div>
    <h2>${esc(ctx.heads.h1Services)}</h2>
    <p class="hero-sub" style="max-width:720px">${esc(ctx.servicesIntro)}</p>
    <div style="margin-top:26px">${svcHtml}</div>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-2" style="align-items:center">
    <ul class="why-list">${whyHtml}</ul>
    <div>
      <div class="eyebrow">${esc(ctx.heads.eyebrowWhyUs)}</div>
      <h2>${esc(ctx.heads.h2WhyUsDiff)}</h2>
      <p>We're not a call center dispatching whoever is closest — every technician follows the same humane, full-exclusion process on every job in ${esc(ctx.loc)}.</p>
    </div>
  </div>
</section>

<section class="section" id="service-area" style="background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="wrap grid grid-2" style="align-items:start">
    <div>
      <div class="eyebrow">${esc(ctx.heads.eyebrowArea)}</div>
      <h2>${esc(ctx.heads.h1ServiceArea)}</h2>
      <p>${esc(ctx.stateFull ? `Homes and businesses across ${esc(ctx.stateFull)}` : `Properties across ${esc(ctx.loc)}`)} deal with ${esc(ctx.climate)}. That means raccoon activity picks up every year as the weather turns, and attics, chimneys, and crawl spaces in ${esc(ctx.loc)} become prime denning spots.</p>
      <p>${esc(ctx.serviceAreaLead)}</p>
    </div>
    <div>${mapEmbed(ctx)}</div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap">
    <div class="eyebrow">${esc(ctx.heads.eyebrowFaq)}</div>
    <h2>${esc(ctx.heads.h1Faq)}</h2>
    <div class="faq" style="max-width:820px;margin-top:24px">${faqHtml}</div>
  </div>
</section>

${ctaBand(ctx)}

<section class="section" id="contact">
  <div class="wrap grid grid-2" style="align-items:start">
    <div class="card">
      <div class="eyebrow">${esc(ctx.heads.eyebrowContact)}</div>
      <h2>${esc(ctx.heads.h1Contact)}</h2>
      <p style="font-size:1.6rem;font-weight:800"><a href="tel:${PHONE_RAW}">${PHONE_DISPLAY}</a></p>
      <p>Mon–Sat 7am–7pm · 24/7 emergency line<br>${esc(ctx.loc)} and surrounding ${esc(ctx.areaNoun)}</p>
      <a class="btn" href="tel:${PHONE_RAW}">${phoneIcon()} Call ${PHONE_DISPLAY}</a>
    </div>
    <div>${mapEmbed(ctx)}</div>
  </div>
</section>
`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
${head(ctx, { path: '', title: `Raccoon Removal ${ctx.loc} | ${ctx.businessName}`, description: `Humane raccoon removal in ${ctx.loc}. Attic exclusion, trapping, and damage repair. Call ${PHONE_DISPLAY} for fast, licensed service.` })}
</head>
<body>
${headerNav(ctx, links)}
${body}
${footer(ctx, links)}
${floatCall()}
</body>
</html>`;
}

module.exports = { buildSiteCtx, renderIndex, renderServices, renderServiceArea, renderFaq, renderContact, renderSinglePage };
