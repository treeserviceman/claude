import csv, os, re, math, shutil, hashlib, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import svg_gen
import templates as T
from content_data import CLIMATE_BY_STATE, SERVICES, SERVICE_BY_SLUG, PHONE_DISPLAY, BRAND
from content_banks import SERVICE_CONTENT, STUB_CONTENT, HUB_WHY_US, HUB_FAQ, hub_prevention_bullets, pick, pick_n
from curated_facts import CURATED

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uscities.csv")
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "site")  # regenerated site lands here; copy its contents to your site root to publish

# ---- config (bump these to extend the pattern to more cities later) -------
TOTAL_CITIES = 10000
FULL_TIER_COUNT = 10000
NEARBY_K = 4
BASE_URL = "https://bayswaterpestcontrol.com"

STATE_ABBR_TO_NAME = {}

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def density_word(density):
    try:
        d = float(density)
    except (TypeError, ValueError):
        return "small-town"
    if d >= 3000:
        return "dense urban"
    if d >= 800:
        return "suburban"
    return "small-town and rural"

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def load_cities():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    cities = []
    for r in rows:
        try:
            pop = int(float(r["population"] or 0))
            lat = float(r["lat"])
            lng = float(r["lng"])
        except (TypeError, ValueError):
            continue
        if pop <= 0:
            continue
        STATE_ABBR_TO_NAME[r["state_id"]] = r["state_name"]
        cities.append({
            "city": r["city_ascii"],
            "state_abbr": r["state_id"],
            "state_name": r["state_name"],
            "county": r["county_name"],
            "lat": lat, "lng": lng,
            "population": pop,
            "density": r["density"],
            "timezone": r["timezone"],
        })
    cities.sort(key=lambda c: -c["population"])
    return cities

def build_universe(cities):
    universe = cities[:TOTAL_CITIES]
    seen_slugs = defaultdict(set)
    for c in universe:
        base = slugify(c["city"])
        slug = base
        n = 2
        while slug in seen_slugs[c["state_abbr"]]:
            slug = f"{base}-{slugify(c['county'])}" if n == 2 else f"{base}-{n}"
            n += 1
        seen_slugs[c["state_abbr"]].add(slug)
        c["slug"] = slug
        c["state_slug"] = slugify(c["state_name"])
    return universe

def compute_nearby(universe):
    by_state = defaultdict(list)
    for c in universe:
        by_state[c["state_abbr"]].append(c)
    for state, lst in by_state.items():
        for c in lst:
            dists = []
            for other in lst:
                if other is c:
                    continue
                d = haversine(c["lat"], c["lng"], other["lat"], other["lng"])
                dists.append((d, other))
            dists.sort(key=lambda x: x[0])
            c["nearby"] = [o for _, o in dists[:NEARBY_K]]

def write_file(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def img_pick(manifest, theme, seed):
    lst = manifest.get(theme) or manifest["shield"]
    h = int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16)
    return "/assets/img/" + lst[h % len(lst)]

def list_join(items):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]

def nearby_txt(city):
    names = [f'{o["city"]}, {o["state_abbr"]}' for o in city.get("nearby", [])[:3]]
    return list_join(names) if names else f'the {city["county"]} area'

def county_label(state_abbr, county):
    if state_abbr == "LA":
        return f"{county} Parish"
    if state_abbr == "AK":
        return f"{county} Borough/Census Area"
    return f"{county} County"

def make_ctx(city):
    abbr = city["state_abbr"]
    climate = CLIMATE_BY_STATE.get(abbr, "a mix of seasonal weather conditions")
    clabel = county_label(abbr, city["county"])
    ctx = {
        "city": city["city"],
        "county": clabel,
        "county_label": clabel,
        "state_name": city["state_name"],
        "state_abbr": abbr,
        "climate": climate,
        "climate_sentence": f'{city["city"]} sees {climate}.',
        "nearby_txt": nearby_txt(city),
        "phone": PHONE_DISPLAY,
        "density_word": density_word(city["density"]),
    }
    return ctx

def local_notes(city, ctx):
    curated = CURATED.get((city["state_abbr"], city["city"]))
    seed = f'{city["state_abbr"]}|{city["city"]}|local'
    if curated:
        neigh, land = curated
        neigh_txt = list_join(neigh)
        land_txt = list_join(land)
        variants = [
            f'We regularly work in and around {neigh_txt}, and near {land_txt}, so we know the housing stock and terrain here well.',
            f'From {neigh_txt} out toward {land_txt}, our crews cover {ctx["city"]} block by block, not just the main corridors.',
            f'{ctx["city"]}’s mix of neighborhoods -- including {neigh_txt} -- and landmarks like {land_txt} shape where we typically find activity.',
        ]
    else:
        variants = [
            f'We cover {ctx["city"]} and the surrounding {ctx["county"]}, including nearby {ctx["nearby_txt"]}.',
            f'Our {ctx["city"]} routes extend across {ctx["county"]}, with regular calls in nearby {ctx["nearby_txt"]} as well.',
            f'{ctx["city"]} sits in a {ctx["density_word"]} stretch of {ctx["county"]}, not far from {ctx["nearby_txt"]}, and we work the whole area.',
        ]
    return pick(seed, variants)

# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------

def render_full_service_page(city, service, img_manifest):
    ctx = make_ctx(city)
    bank = SERVICE_CONTENT[service["slug"]]
    seed_base = f'{city["state_abbr"]}|{city["city"]}|{service["slug"]}'
    intro = pick(seed_base + "|intro", bank["intro"]).format(**ctx)
    why_here = pick(seed_base + "|why", bank["why_here"]).format(**ctx)
    notes = local_notes(city, ctx)
    biology = pick(seed_base + "|bio", bank["biology"]).format(**ctx)
    health_risks = pick(seed_base + "|health", bank["health_risks"]).format(**ctx)
    process = pick(seed_base + "|proc", bank["process"]).format(**ctx)
    signs = pick(seed_base + "|signs", bank["signs"]).format(**ctx)
    prevention_tips = [t.format(**ctx) for t in pick_n(seed_base + "|prev", bank["prevention"], min(5, len(bank["prevention"])))]
    diy_vs_pro = pick(seed_base + "|diy", bank["diy_vs_pro"]).format(**ctx)
    seasonal = pick(seed_base + "|season", bank["seasonal_timing"]).format(**ctx)
    why_us = pick(seed_base + "|whyus", bank["why_choose_us"]).format(**ctx)
    faq_pairs = [(q.format(**ctx), a.format(**ctx)) for q, a in bank["faq"]]

    title = f'{service["name"]} {city["city"]} {city["state_abbr"]}'
    description = f'{service["name"]} in {city["city"]}, {city["state_abbr"]} -- licensed local technicians, same-week scheduling, and exclusion work built to last. Call {PHONE_DISPLAY}.'
    path = f'/locations/{city["state_slug"]}/{city["slug"]}/{service["slug"]}/'

    hero_img = img_pick(img_manifest, service["svg_theme"], seed_base + "|hero")

    other_services = [s for s in SERVICES if s["slug"] != service["slug"]]
    other_html = "".join(
        f'<a class="card" href="/locations/{city["state_slug"]}/{city["slug"]}/{s["slug"]}/">'
        f'<img src="{img_pick(img_manifest, s["svg_theme"], seed_base+"|other|"+s["slug"])}" alt="{T.esc(s["name"])} in {T.esc(city["city"])}, {T.esc(city["state_abbr"])}" loading="lazy">'
        f'<div class="card-body"><span class="tag">{T.esc(s["category"].title())}</span><h3>{T.esc(s["name"])}</h3>'
        f'<p class="small">{T.esc(s["short"])}</p></div></a>'
        for s in other_services
    )

    def _nearby_href(o):
        if o.get("tier") == "full":
            return f'/locations/{o["state_slug"]}/{o["slug"]}/{service["slug"]}/'
        return f'/locations/{o["state_slug"]}/{o["slug"]}/'
    nearby_links = "".join(
        f'<a class="pill" href="{_nearby_href(o)}">{T.esc(service["name"])} in {T.esc(o["city"])}, {T.esc(o["state_abbr"])}</a>'
        for o in city.get("nearby", [])[:4]
    )

    body = f"""
<div class="container">
{T.breadcrumb([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], f'/locations/{city["state_slug"]}/{city["slug"]}/'), (service["name"], None)])}
</div>
<section class="hero">
  <div class="container grid">
    <div>
      <h1>{T.esc(title)}</h1>
      <p class="lead">{T.esc(intro)}</p>
      <div class="badge-row">
        <span>&#9989; Licensed &amp; insured</span>
        <span>&#9989; Same-week scheduling</span>
        <span>&#9989; Serving all of {T.esc(ctx["county_label"])}</span>
      </div>
      <a class="header-call" style="font-size:1.1rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
    </div>
    <div><img src="{hero_img}" alt="{T.esc(service['name'])} illustration"></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Why {T.esc(service["animal"])} are a problem in {T.esc(city["city"])}</h2>
    <p>{T.esc(why_here)}</p>
    <p>{T.esc(notes)}</p>
    {T.cta_block(f'Dealing with {service["animal"]} in {city["city"]} right now?', f'Licensed technicians serving {city["city"]}, {city["state_abbr"]} and {ctx["county_label"]}.')}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>{T.esc(service["animal"].capitalize())}: biology and behavior</h2>
    <p>{T.esc(biology)}</p>
    {T.cta_block(f'Know what you are dealing with in {city["city"]}?', "Talk to a technician who handles this species every week.")}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Health and property risks</h2>
    <p>{T.esc(health_risks)}</p>
    {T.cta_block("Don't wait on a health or property risk.")}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>Our {T.esc(service["name"])} process</h2>
    <p>{T.esc(process)}</p>
    {T.cta_block(f'Ready to schedule {service["name"].lower()} in {city["city"]}?')}
  </div>
</section>

<section class="section">
  <div class="container">
    <h3>Signs you need {T.esc(service["name"].lower())}</h3>
    <p>{T.esc(signs)}</p>
    {T.cta_block("Seeing these signs at your property?", f'We serve {city["city"]}, {city["state_abbr"]} and all of {ctx["county_label"]}.')}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>Prevention: what {T.esc(city["city"])} homeowners can do</h2>
    <ul>{"".join(f"<li>{T.esc(t)}</li>" for t in prevention_tips)}</ul>
    {T.cta_block("Already past prevention?", "Skip straight to removal -- call now.")}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>DIY vs. professional {T.esc(service["name"].lower())}</h2>
    <p>{T.esc(diy_vs_pro)}</p>
    {T.cta_block("Let a professional handle it right the first time.")}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>Best time to treat in {T.esc(city["city"])}</h2>
    <p>{T.esc(seasonal)}</p>
    {T.cta_block(f'Whatever the season, we are available in {city["city"]}.')}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Why {T.esc(city["city"])} homeowners call us</h2>
    <p>{T.esc(why_us)}</p>
    {T.cta_block(f'Same-week {service["name"].lower()} in {city["city"]}, {city["state_abbr"]}')}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>{T.esc(service["name"])} service area: {T.esc(city["city"])}, {T.esc(city["state_abbr"])}</h2>
    {T.map_embed(city["lat"], city["lng"])}
    <p class="small" style="margin-top:10px">Serving {T.esc(city["city"])} and nearby {T.esc(ctx["nearby_txt"])}.</p>
    {T.cta_block(f'In the {city["city"]} service area?')}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Frequently asked questions</h2>
    {T.faq_html(faq_pairs)}
    {T.cta_block("Still have questions?", "Call us and talk to a real local technician.")}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-title-row"><h2>Other services in {T.esc(city["city"])}</h2>
    <a class="view-all" href="/locations/{city["state_slug"]}/{city["slug"]}/">View all {T.esc(city["city"])} services &rarr;</a></div>
    <div class="grid-3">{other_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>{T.esc(service["name"])} near {T.esc(city["city"])}</h2>
    <div class="pill-row">{nearby_links}</div>
  </div>
</section>
"""
    schemas = [
        T.breadcrumb_schema([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], f'/locations/{city["state_slug"]}/{city["slug"]}/'), (service["name"], path)], BASE_URL),
        T.service_schema(BASE_URL, path, service["name"], description, city["city"], city["state_name"], city["state_abbr"], city["lat"], city["lng"]),
        T.faq_schema(faq_pairs),
    ]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)
    return path

def render_full_city_hub(city, img_manifest):
    ctx = make_ctx(city)
    title = f'Pest Control {city["city"]} {city["state_abbr"]}'
    description = f'Wildlife and pest control services in {city["city"]}, {city["state_abbr"]}: raccoon, skunk, mosquito, rat, roach, and bed bug removal. Call {PHONE_DISPLAY}.'
    path = f'/locations/{city["state_slug"]}/{city["slug"]}/'
    hub_seed = f'{city["state_abbr"]}|{city["city"]}|hub'
    intro_variants = [
        f'{city["city"]} homes deal with a real mix of wildlife and pest pressure -- {ctx["climate"]} keeps insects active most of the year, while attics, sheds, and crawlspaces around {ctx["county"]} give wildlife plenty of places to den. We run six dedicated services here, each handled by technicians who know the area, and each with its own full guide linked below.',
        f'Between the local climate and the housing stock across {ctx["county"]}, {city["city"]} sees steady calls across wildlife, rodents, and insects alike. We cover all six services below for the {city["city"]} area, and this page walks through what each one covers before you call.',
    ]
    intro = pick(hub_seed + "|intro", intro_variants)
    notes = local_notes(city, ctx)
    hub_why_us = pick(hub_seed + "|whyus", HUB_WHY_US).format(**ctx)
    hub_faq_pairs = [(q.format(**ctx), a.format(**ctx)) for q, a in HUB_FAQ]
    prevention_bullets = hub_prevention_bullets(SERVICE_CONTENT, ctx, hub_seed)
    prevention_html = "".join(
        f'<li><strong>{T.esc(SERVICE_BY_SLUG[slug]["name"])}:</strong> {T.esc(tip)}</li>'
        for slug, tip in prevention_bullets
    )

    service_overviews = ""
    for s in SERVICES:
        seed_base = f'{city["state_abbr"]}|{city["city"]}|{s["slug"]}'
        bank = SERVICE_CONTENT[s["slug"]]
        overview = pick(seed_base + "|intro", bank["intro"]).format(**ctx) + " " + pick(seed_base + "|why", bank["why_here"]).format(**ctx)
        img = img_pick(img_manifest, s["svg_theme"], city["slug"] + s["slug"])
        service_overviews += f"""
<div class="grid-2" style="align-items:center;margin-bottom:24px">
  <div><img src="{img}" alt="{T.esc(s['name'])} {T.esc(city['city'])} {T.esc(city['state_abbr'])}" loading="lazy" style="border-radius:14px"></div>
  <div>
    <span class="tag">{T.esc(s["category"].title())}</span>
    <h3>{T.esc(s["name"])} in {T.esc(city["city"])}, {T.esc(city["state_abbr"])}</h3>
    <p>{T.esc(overview)}</p>
    <a class="pill" href="/locations/{city["state_slug"]}/{city["slug"]}/{s["slug"]}/">Full {T.esc(s["name"])} guide for {T.esc(city["city"])} &rarr;</a>
  </div>
</div>
"""

    nearby_links = "".join(
        f'<a class="pill" href="/locations/{o["state_slug"]}/{o["slug"]}/">{T.esc(o["city"])}, {T.esc(o["state_abbr"])}</a>'
        for o in city.get("nearby", [])[:4]
    )
    hero_img = img_pick(img_manifest, "house", city["slug"] + "hub")

    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], None)])}</div>
<section class="hero">
  <div class="container grid">
    <div>
      <h1>{T.esc(title)}</h1>
      <p class="lead">{T.esc(intro)}</p>
      <a class="header-call" style="font-size:1.1rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
    </div>
    <div><img src="{hero_img}" alt="Pest control in {T.esc(city['city'])}"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Services we provide in {T.esc(city["city"])}, {T.esc(city["state_abbr"])}</h2>
    {service_overviews}
    {T.cta_block(f'Not sure which service you need in {city["city"]}?', "Tell us what you're seeing and we'll point you to the right fix.")}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Local coverage in {T.esc(city["city"])}</h2>
    <p>{T.esc(notes)}</p>
    {T.map_embed(city["lat"], city["lng"])}
    {T.cta_block(f'In the {city["city"]} service area?')}
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Prevention checklist for {T.esc(city["city"])} homes</h2>
    <p>One quick habit for each pest we cover here -- the full guide for each service has a longer checklist.</p>
    <ul>{prevention_html}</ul>
    {T.cta_block("Already seeing signs of a problem?", "Skip prevention -- call now.")}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Why {T.esc(city["city"])} homeowners choose us</h2>
    <p>{T.esc(hub_why_us)}</p>
    {T.cta_block(f'Ready to schedule service in {city["city"]}?')}
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Frequently asked questions</h2>
    {T.faq_html(hub_faq_pairs)}
    {T.cta_block("Still have questions?", "Call and talk to a real local technician.")}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Nearby cities we serve</h2>
    <div class="pill-row">{nearby_links}</div>
  </div>
</section>
"""
    schemas = [
        T.breadcrumb_schema([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], path)], BASE_URL),
        T.localbusiness_schema(BASE_URL, path, city["city"], city["state_name"], city["state_abbr"], city["lat"], city["lng"]),
        T.faq_schema(hub_faq_pairs),
    ]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)
    return path

def render_stub_city_page(city, img_manifest):
    ctx = make_ctx(city)
    title = f'Pest Control {city["city"]} {city["state_abbr"]}'
    description = f'Raccoon, skunk, mosquito, rat, roach, and bed bug control for {city["city"]}, {city["state_abbr"]}. Licensed technicians, call {PHONE_DISPLAY}.'
    path = f'/locations/{city["state_slug"]}/{city["slug"]}/'
    notes = local_notes(city, ctx)
    intro_variants = [
        f'{city["city"]} sits in {ctx["county"]}, {ctx["state_abbr"]}, where {ctx["climate"]}. We provide wildlife and pest control across town, from {ctx["density_word"]} residential blocks to properties bordering nearby {ctx["nearby_txt"]}.',
        f'Homes in {city["city"]} deal with the same pest pressure common across {ctx["county"]} -- {ctx["climate"]}. Our technicians cover {city["city"]} and the surrounding area for all six services below.',
    ]
    intro = pick(f'{city["state_abbr"]}|{city["city"]}|stubintro', intro_variants)

    sections = ""
    for s in SERVICES:
        blurb = pick(f'{city["state_abbr"]}|{city["city"]}|{s["slug"]}|stub', STUB_CONTENT[s["slug"]]).format(**ctx)
        img = img_pick(img_manifest, s["svg_theme"], city["slug"] + s["slug"] + "stub")
        sections += f"""
<div class="grid-2" style="align-items:center;margin-bottom:20px">
  <div><img src="{img}" alt="{T.esc(s['name'])} in {T.esc(city['city'])}, {T.esc(city['state_abbr'])}" loading="lazy" style="border-radius:14px"></div>
  <div>
    <span class="tag">{T.esc(s["category"].title())}</span>
    <h3>{T.esc(s["name"])} in {T.esc(city["city"])}, {T.esc(city["state_abbr"])}</h3>
    <p>{T.esc(blurb)}</p>
    <a class="pill" href="{T.tel_href()}">&#9742; Call about {T.esc(s["name"])}</a>
  </div>
</div>
"""
    nearby_links = "".join(
        f'<a class="pill" href="/locations/{o["state_slug"]}/{o["slug"]}/">{T.esc(o["city"])}, {T.esc(o["state_abbr"])}</a>'
        for o in city.get("nearby", [])[:4]
    )
    hero_img = img_pick(img_manifest, "shield", city["slug"] + "stubhero")

    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], None)])}</div>
<section class="hero">
  <div class="container grid">
    <div>
      <h1>{T.esc(title)}</h1>
      <p class="lead">{T.esc(intro)}</p>
      <a class="header-call" style="font-size:1.1rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
    </div>
    <div><img src="{hero_img}" alt="Pest control in {T.esc(city['city'])}"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    {sections}
    {T.cta_block(f'Serving {city["city"]}, {city["state_abbr"]} and all of {ctx["county_label"]}')}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Where we work in {T.esc(city["city"])}</h2>
    <p>{T.esc(notes)}</p>
    {T.map_embed(city["lat"], city["lng"])}
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Nearby cities we serve</h2>
    <div class="pill-row">{nearby_links}</div>
  </div>
</section>
"""
    schemas = [
        T.breadcrumb_schema([("Home","/"), (city["state_name"], f'/locations/{city["state_slug"]}/'), (city["city"], path)], BASE_URL),
        T.localbusiness_schema(BASE_URL, path, city["city"], city["state_name"], city["state_abbr"], city["lat"], city["lng"]),
    ]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)
    return path

def render_state_page(state_abbr, state_name, state_slug, full_cities, stub_cities, img_manifest):
    title = f'Pest Control {state_name}'
    description = f'Wildlife and pest control coverage across {state_name}: raccoon, skunk, mosquito, rat, roach, and bed bug removal in {len(full_cities)+len(stub_cities)} cities. Call {PHONE_DISPLAY}.'
    path = f'/locations/{state_slug}/'
    climate = CLIMATE_BY_STATE.get(state_abbr, "a mix of seasonal weather conditions")

    featured = "".join(
        f'<a class="card" href="/locations/{state_slug}/{c["slug"]}/">'
        f'<img src="{img_pick(img_manifest, "house", state_slug+c["slug"])}" alt="Pest control {T.esc(c["city"])} {T.esc(state_abbr)}" loading="lazy">'
        f'<div class="card-body"><span class="tag">Full coverage</span><h3>{T.esc(c["city"])}, {T.esc(state_abbr)}</h3>'
        f'<p class="small">Pop. {c["population"]:,} &middot; {T.esc(c["county"])}</p></div></a>'
        for c in sorted(full_cities, key=lambda c: -c["population"])[:12]
    )
    all_full_links = "".join(
        f'<li><a href="/locations/{state_slug}/{c["slug"]}/">{T.esc(c["city"])}</a></li>'
        for c in sorted(full_cities, key=lambda c: c["city"])
    )
    all_stub_links = "".join(
        f'<li><a href="/locations/{state_slug}/{c["slug"]}/">{T.esc(c["city"])}</a></li>'
        for c in sorted(stub_cities, key=lambda c: c["city"])
    )
    service_cards = "".join(
        f'<a class="card" href="/services/{s["slug"]}/">'
        f'<img src="{img_pick(img_manifest, s["svg_theme"], state_slug+s["slug"])}" alt="{T.esc(s["name"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(s["name"])}</h3><p class="small">{T.esc(s["short"])}</p></div></a>'
        for s in SERVICES
    )

    dont_see_cta = T.cta_block("Don't see your city listed?", "Call us -- we cover areas beyond this list too.")
    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), (state_name, None)])}</div>
<section class="hero">
  <div class="container grid">
    <div>
      <h1>{T.esc(title)}</h1>
      <p class="lead">We provide raccoon, skunk, mosquito, rat, roach, and bed bug control across {T.esc(state_name)}, covering {len(full_cities)+len(stub_cities)} cities and towns. {T.esc(state_name)} generally sees {T.esc(climate)}, which shapes when and how we treat each service.</p>
      <a class="header-call" style="font-size:1.1rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
    </div>
    <div><img src="{img_pick(img_manifest,'shield', state_slug+'hero')}" alt="Pest control {T.esc(state_name)}"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Featured {T.esc(state_name)} service areas</h2>
    <div class="grid-3">{featured}</div>
    {T.cta_block(f'Looking for service in {state_name}?')}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Services offered statewide</h2>
    <div class="grid-3">{service_cards}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>All {T.esc(state_name)} cities we serve</h2>
    <ul class="link-list">{all_full_links}{all_stub_links}</ul>
    {dont_see_cta}
  </div>
</section>
"""
    schemas = [T.breadcrumb_schema([("Home","/"), (state_name, path)], BASE_URL)]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)
    return path

def render_locations_index(states_meta, img_manifest):
    path = "/locations/"
    title = "Wildlife & Pest Control Service Areas"
    description = f"Browse all US states covered by {BRAND}: raccoon, skunk, mosquito, rat, roach, and bed bug control. Call {PHONE_DISPLAY}."
    cards = "".join(
        f'<a class="card" href="/locations/{st["slug"]}/">'
        f'<img src="{img_pick(img_manifest,"house", st["slug"]+"idx")}" alt="Pest control {T.esc(st["name"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(st["name"])}</h3><p class="small">{st["count"]} cities covered</p></div></a>'
        for st in sorted(states_meta, key=lambda s: s["name"])
    )
    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), ("Service Areas", None)])}</div>
<section class="section"><div class="container">
<h1>{T.esc(title)}</h1>
<p>{BRAND} covers {sum(s['count'] for s in states_meta):,} cities across {len(states_meta)} states and territories. Pick a state to see every city, or jump straight to a service.</p>
<div class="grid-3">{cards}</div>
{T.cta_block("Can't find your city?", "Call us directly -- we cover more areas than listed.")}
</div></section>
"""
    schemas = [T.breadcrumb_schema([("Home","/"), ("Service Areas", path)], BASE_URL)]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)

def render_service_hub(service, states_meta, full_cities_by_service, img_manifest):
    path = f'/services/{service["slug"]}/'
    title = service["name"]
    description = f'{service["name"]} available nationwide: {service["short"]} Licensed local technicians, call {PHONE_DISPLAY}.'
    bank = SERVICE_CONTENT[service["slug"]]
    intro = pick(f'servicehub|{service["slug"]}', bank["intro"]).format(
        city="your city", county="your area", state_name="", state_abbr="", climate="typical seasonal conditions",
        climate_sentence="Conditions vary by region.", nearby_txt="surrounding areas", phone=PHONE_DISPLAY, density_word="local",
    )
    featured = sorted(full_cities_by_service, key=lambda c: -c["population"])[:24]
    cards = "".join(
        f'<a class="card" href="/locations/{c["state_slug"]}/{c["slug"]}/{service["slug"]}/">'
        f'<img src="{img_pick(img_manifest, service["svg_theme"], c["slug"]+service["slug"]+"hub")}" alt="{T.esc(service["name"])} {T.esc(c["city"])} {T.esc(c["state_abbr"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(service["name"])} {T.esc(c["city"])} {T.esc(c["state_abbr"])}</h3></div></a>'
        for c in featured
    )
    state_links = "".join(
        f'<li><a href="/locations/{st["slug"]}/">{T.esc(st["name"])}</a></li>' for st in sorted(states_meta, key=lambda s: s["name"])
    )
    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), ("Services", "/services/"), (service["name"], None)])}</div>
<section class="hero">
  <div class="container grid">
    <div><h1>{T.esc(title)}</h1><p class="lead">{T.esc(intro)}</p>
    <a class="header-call" style="font-size:1.1rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a></div>
    <div><img src="{img_pick(img_manifest, service['svg_theme'], service['slug']+'hub')}" alt="{T.esc(service['name'])}"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Featured {T.esc(service["name"])} service areas</h2>
    <div class="grid-3">{cards}</div>
    {T.cta_block(f'Need {service["name"].lower()} near you?')}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Browse {T.esc(service["name"])} by state</h2>
    <ul class="link-list">{state_links}</ul>
  </div>
</section>
"""
    schemas = [T.breadcrumb_schema([("Home","/"), ("Services", "/services/"), (service["name"], path)], BASE_URL)]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)

def render_services_index(img_manifest):
    path = "/services/"
    title = "Wildlife & Pest Control Services"
    description = f"All services offered by {BRAND}: raccoon removal, skunk removal, mosquito control, rat control, roach control, and bed bug treatment."
    cards = "".join(
        f'<a class="card" href="/services/{s["slug"]}/">'
        f'<img src="{img_pick(img_manifest, s["svg_theme"], s["slug"]+"idx")}" alt="{T.esc(s["name"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(s["name"])}</h3><p class="small">{T.esc(s["short"])}</p></div></a>'
        for s in SERVICES
    )
    body = f"""
<div class="container">{T.breadcrumb([("Home","/"), ("Services", None)])}</div>
<section class="section"><div class="container">
<h1>{T.esc(title)}</h1>
<div class="grid-3">{cards}</div>
{T.cta_block("Ready to book service?")}
</div></section>
"""
    schemas = [T.breadcrumb_schema([("Home","/"), ("Services", path)], BASE_URL)]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)

def render_home(states_meta, top_full_cities, img_manifest):
    path = "/"
    title = "Nationwide Wildlife & Pest Control"
    description = f"Raccoon removal, skunk removal, mosquito control, rat control, roach control, and bed bug treatment in {sum(s['count'] for s in states_meta):,}+ US cities. Call {PHONE_DISPLAY}."
    service_cards = "".join(
        f'<a class="card" href="/services/{s["slug"]}/">'
        f'<img src="{img_pick(img_manifest, s["svg_theme"], "home"+s["slug"])}" alt="{T.esc(s["name"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(s["name"])}</h3><p class="small">{T.esc(s["short"])}</p></div></a>'
        for s in SERVICES
    )
    city_cards = "".join(
        f'<a class="card" href="/locations/{c["state_slug"]}/{c["slug"]}/">'
        f'<img src="{img_pick(img_manifest,"house","home"+c["slug"])}" alt="Pest control {T.esc(c["city"])} {T.esc(c["state_abbr"])}" loading="lazy">'
        f'<div class="card-body"><h3>{T.esc(c["city"])}, {T.esc(c["state_abbr"])}</h3></div></a>'
        for c in top_full_cities[:12]
    )
    state_pills = "".join(
        f'<a class="pill" href="/locations/{st["slug"]}/">{T.esc(st["name"])}</a>' for st in sorted(states_meta, key=lambda s: s["name"])
    )
    total_cities = sum(s["count"] for s in states_meta)
    body = f"""
<section class="hero">
  <div class="container grid">
    <div>
      <h1>{T.esc(title)}</h1>
      <p class="lead">Licensed raccoon, skunk, mosquito, rat, roach, and bed bug control serving {total_cities:,}+ cities across all 50 states. Same-week scheduling, real local technicians.</p>
      <a class="header-call" style="font-size:1.15rem" href="{T.tel_href()}">&#9742; Call {PHONE_DISPLAY}</a>
    </div>
    <div><img src="{img_pick(img_manifest,'shield','homehero')}" alt="Nationwide pest control"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="stat-row">
      <div class="stat"><b>{total_cities:,}</b>Cities served</div>
      <div class="stat"><b>{len(states_meta)}</b>States &amp; territories</div>
      <div class="stat"><b>6</b>Core services</div>
    </div>
    <h2>Our services</h2>
    <div class="grid-3">{service_cards}</div>
    {T.cta_block("Not sure what's in your attic or walls?", "Describe what you're seeing and we'll tell you what to do next.")}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>Popular service areas</h2>
    <div class="grid-3">{city_cards}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>Find pest control by state</h2>
    <div class="pill-row">{state_pills}</div>
    {T.cta_block("We're ready when you are.")}
  </div>
</section>
"""
    org_schema = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "PestControlService"],
        "name": BRAND,
        "url": BASE_URL,
        "telephone": T.__dict__.get("PHONE_TEL", None) or None,
        "areaServed": {"@type": "Country", "name": "United States"},
    }
    from content_data import PHONE_TEL
    org_schema["telephone"] = PHONE_TEL
    schemas = [org_schema, T.breadcrumb_schema([("Home", path)], BASE_URL)]
    html = T.page(title, description, path, body, schemas, BASE_URL)
    write_file(path + "index.html", html)

# ---------------------------------------------------------------------------
# Sitemap / robots
# ---------------------------------------------------------------------------

def write_sitemaps(all_paths):
    CHUNK = 45000
    chunks = [all_paths[i:i+CHUNK] for i in range(0, len(all_paths), CHUNK)]
    sitemap_files = []
    for idx, chunk in enumerate(chunks, start=1):
        fname = f"sitemap-{idx}.xml"
        urls = "".join(f"<url><loc>{BASE_URL}{p}</loc></url>" for p in chunk)
        xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
        write_file("/" + fname, xml)
        sitemap_files.append(fname)
    if len(sitemap_files) == 1:
        os.rename(os.path.join(OUT, sitemap_files[0]), os.path.join(OUT, "sitemap.xml"))
        sitemap_files = ["sitemap.xml"]
    else:
        idx_entries = "".join(f"<sitemap><loc>{BASE_URL}/{f}</loc></sitemap>" for f in sitemap_files)
        xml = f'<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{idx_entries}</sitemapindex>'
        write_file("/sitemap.xml", xml)
    write_file("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    print("Loading cities...")
    cities = load_cities()
    universe = build_universe(cities)
    print(f"Universe: {len(universe)} cities")

    print("Computing nearby cities...")
    compute_nearby(universe)

    full_tier = universe[:FULL_TIER_COUNT]
    stub_tier = universe[FULL_TIER_COUNT:]
    for c in full_tier:
        c["tier"] = "full"
    for c in stub_tier:
        c["tier"] = "stub"

    print("Generating images...")
    img_manifest = svg_gen.build_all(os.path.join(OUT, "assets", "img"))

    shutil.copyfile(os.path.join(HERE, "style.css"), os.path.join(OUT, "assets", "style.css"))

    all_paths = ["/", "/services/", "/locations/"]

    # group by state
    by_state = defaultdict(lambda: {"full": [], "stub": []})
    for c in full_tier:
        by_state[c["state_abbr"]]["full"].append(c)
    for c in stub_tier:
        by_state[c["state_abbr"]]["stub"].append(c)

    states_meta = []
    for abbr, groups in by_state.items():
        name = STATE_ABBR_TO_NAME[abbr]
        slug = slugify(name)
        count = len(groups["full"]) + len(groups["stub"])
        states_meta.append({"abbr": abbr, "name": name, "slug": slug, "count": count})

    print("Rendering full-tier city + service pages...")
    full_cities_by_service = defaultdict(list)
    for i, c in enumerate(full_tier, start=1):
        render_full_city_hub(c, img_manifest)
        all_paths.append(f'/locations/{c["state_slug"]}/{c["slug"]}/')
        for s in SERVICES:
            p = render_full_service_page(c, s, img_manifest)
            all_paths.append(p)
            full_cities_by_service[s["slug"]].append(c)
        if i % 100 == 0:
            print(f"  {i}/{len(full_tier)} full-tier cities done")

    print("Rendering stub-tier city pages...")
    for i, c in enumerate(stub_tier, start=1):
        render_stub_city_page(c, img_manifest)
        all_paths.append(f'/locations/{c["state_slug"]}/{c["slug"]}/')
        if i % 1000 == 0:
            print(f"  {i}/{len(stub_tier)} stub-tier cities done")

    print("Rendering state hub pages...")
    for abbr, groups in by_state.items():
        name = STATE_ABBR_TO_NAME[abbr]
        slug = slugify(name)
        render_state_page(abbr, name, slug, groups["full"], groups["stub"], img_manifest)
        all_paths.append(f"/locations/{slug}/")

    print("Rendering service hub pages + index pages...")
    for s in SERVICES:
        render_service_hub(s, states_meta, full_cities_by_service[s["slug"]], img_manifest)
        all_paths.append(f'/services/{s["slug"]}/')
    render_services_index(img_manifest)
    render_locations_index(states_meta, img_manifest)
    render_home(states_meta, sorted(full_tier, key=lambda c: -c["population"]), img_manifest)

    print("Writing sitemap + robots.txt...")
    write_sitemaps(sorted(set(all_paths)))

    total_files = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"Done. {total_files} files written to {OUT}")
    print(f"Full-tier cities: {len(full_tier)}, Stub-tier cities: {len(stub_tier)}, States: {len(states_meta)}")

if __name__ == "__main__":
    main()
