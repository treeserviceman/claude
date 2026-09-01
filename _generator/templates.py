import json, html
from content_data import PHONE_DISPLAY, PHONE_TEL, BRAND, SERVICES

def esc(s):
    return html.escape(str(s), quote=True)

def tel_href():
    return f"tel:{PHONE_TEL}"

def floating_call():
    return f"""
<a class="float-call" href="{tel_href()}"><span class="ico">&#9742;</span> Call {PHONE_DISPLAY}</a>
<div class="mobile-call-bar"><a href="{tel_href()}">&#9742; Call Now: {PHONE_DISPLAY}</a></div>
"""

def cta_block(headline, sub=""):
    sub_html = f'<div class="small" style="color:#cfe0d8">{esc(sub)}</div>' if sub else ""
    return f"""
<div class="cta-block">
  <div><h3>{esc(headline)}</h3>{sub_html}</div>
  <a class="btn" href="{tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
</div>
"""

def breadcrumb(items):
    """items: list of (label, href_or_None). Last item has href None (current page)."""
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        else:
            parts.append(f"<span>{esc(label)}</span>")
    return f'<nav class="breadcrumb">{" &rsaquo; ".join(parts)}</nav>'

def header():
    service_links = "".join(
        f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES
    )
    return f"""
<header class="site-header">
  <div class="container">
    <a class="brand" href="/"><span class="brand-mark">&#128737;</span> {esc(BRAND)}</a>
    <a class="header-call" href="{tel_href()}">&#9742; {PHONE_DISPLAY}</a>
  </div>
</header>
"""

def footer(state_links_html, extra_city_links_html=""):
    service_cols = "".join(
        f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>{esc(BRAND)}</h4>
        <p class="small">Licensed wildlife and pest control coverage across the United States. Call {PHONE_DISPLAY} for same-day scheduling in most service areas.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul style="list-style:none;padding:0">{service_cols}</ul>
      </div>
      <div>
        <h4>Coverage</h4>
        <ul style="list-style:none;padding:0">
          <li><a href="/locations/">All States</a></li>
          <li><a href="/services/">All Services</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Call Us</h4>
        <p><a href="{tel_href()}" style="font-weight:800;font-size:1.15rem;color:#fff">{PHONE_DISPLAY}</a></p>
        <p class="small">Available for wildlife and pest emergencies nationwide.</p>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; {esc(BRAND)}. Content is provided for general informational purposes for each listed service area.
    </div>
  </div>
</footer>
"""

def schema_script(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

def breadcrumb_schema(items, base_url):
    els = []
    for i, (label, href) in enumerate(items, start=1):
        item = {"@type": "ListItem", "position": i, "name": label}
        if href:
            item["item"] = base_url.rstrip("/") + href
        els.append(item)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}

def localbusiness_schema(base_url, page_path, city, state_name, state_abbr, lat, lng):
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "PestControlService"],
        "name": f"{BRAND} - {city}, {state_abbr}",
        "url": base_url.rstrip("/") + page_path,
        "telephone": PHONE_TEL,
        "priceRange": "$$",
        "areaServed": {"@type": "City", "name": f"{city}, {state_name}"},
        "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": state_abbr, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
    }

def service_schema(base_url, page_path, service_name, description, city, state_name, state_abbr, lat, lng):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": service_name,
        "name": f"{service_name} {city}, {state_abbr}",
        "url": base_url.rstrip("/") + page_path,
        "description": description,
        "areaServed": {
            "@type": "City", "name": f"{city}, {state_name}",
            "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        },
        "provider": {
            "@type": ["LocalBusiness", "PestControlService"],
            "name": BRAND,
            "telephone": PHONE_TEL,
        },
    }

def faq_schema(qa_pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa_pairs
        ],
    }

def faq_html(qa_pairs):
    items = "".join(
        f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in qa_pairs
    )
    return f'<div class="faq">{items}</div>'

def map_embed(lat, lng, zoom=11):
    src = f"https://www.google.com/maps?q={lat},{lng}&z={zoom}&output=embed"
    return f"""<div class="map-wrap"><iframe src="{src}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Service area map"></iframe></div>"""

def page(title, description, canonical_path, body_html, schemas, base_url="https://example-pestsite.com"):
    schema_html = "\n".join(schema_script(s) for s in schemas)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{base_url.rstrip('/')}{canonical_path}">
<link rel="stylesheet" href="/assets/style.css">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta name="robots" content="index, follow">
{schema_html}
</head>
<body>
{header()}
<main>
{body_html}
</main>
{footer("")}
{floating_call()}
</body>
</html>"""
