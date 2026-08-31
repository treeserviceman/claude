'use strict';

// Deterministic pseudo-random helpers so the same slug always produces the same site (repeatable builds).
function hash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}
function pick(seedStr, arr) {
  return arr[hash(seedStr) % arr.length];
}
function pickN(seedStr, arr, n) {
  const idx = arr.map((_, i) => i);
  let seed = hash(seedStr);
  for (let i = idx.length - 1; i > 0; i--) {
    seed = (seed * 1103515245 + 12345) >>> 0;
    const j = seed % (i + 1);
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  return idx.slice(0, n).map((i) => arr[i]);
}
// Joins several independently-seeded fragment picks into one passage, so the
// combination space is the product of the bank sizes rather than the sum.
function compose(seedStr, banks) {
  return banks.map((bank, i) => pick(seedStr + '#' + i, bank)).join(' ');
}

const THEMES = [
  { key: 'autumn', name: 'Autumn Woods', bg: '#fbf6ee', surface: '#ffffff', ink: '#2b1c12', accent: '#b5541c', accent2: '#5c7a4a', headingFont: "'Bitter', Georgia, serif", bodyFont: "'Inter', sans-serif", radius: '14px' },
  { key: 'midnight', name: 'Midnight Alert', bg: '#0e1420', surface: '#161f30', ink: '#eef1f7', accent: '#ef4b3f', accent2: '#3ea6ff', headingFont: "'Archivo Black', Arial, sans-serif", bodyFont: "'Inter', sans-serif", radius: '6px', dark: true },
  { key: 'forest', name: 'Forest Canopy', bg: '#f3f7f0', surface: '#ffffff', ink: '#1c2b1a', accent: '#3f7d3a', accent2: '#c98a2c', headingFont: "'Fraunces', Georgia, serif", bodyFont: "'Nunito Sans', sans-serif", radius: '22px' },
  { key: 'slate', name: 'Slate & Amber', bg: '#f2f2f0', surface: '#ffffff', ink: '#20211f', accent: '#c9820c', accent2: '#3a3f47', headingFont: "'Oswald', Arial, sans-serif", bodyFont: "'Source Sans 3', sans-serif", radius: '4px' },
  { key: 'coastal', name: 'Coastal Clay', bg: '#fff7f1', surface: '#ffffff', ink: '#2c231c', accent: '#c1562f', accent2: '#1f8a8a', headingFont: "'Zilla Slab', Georgia, serif", bodyFont: "'Mulish', sans-serif", radius: '18px' },
  { key: 'prairie', name: 'Prairie Gold', bg: '#faf3e3', surface: '#ffffff', ink: '#332711', accent: '#a86a1f', accent2: '#6b4226', headingFont: "'Roboto Slab', Georgia, serif", bodyFont: "'Karla', sans-serif", radius: '10px' },
  { key: 'urban', name: 'Urban Steel', bg: '#12161c', surface: '#1b212a', ink: '#f1f4f7', accent: '#2fd0c8', accent2: '#f2a33d', headingFont: "'Space Grotesk', Arial, sans-serif", bodyFont: "'Inter', sans-serif", radius: '8px', dark: true },
  { key: 'heritage', name: 'Heritage Brick', bg: '#f7f1e8', surface: '#ffffff', ink: '#2a201a', accent: '#8c2f1c', accent2: '#2c4a34', headingFont: "'Playfair Display', Georgia, serif", bodyFont: "'PT Sans', sans-serif", radius: '2px' },
];

const HERO_STYLES = ['split', 'centered', 'banner'];
const HEADER_STYLES = ['bar', 'stacked'];
const SERVICE_STYLES = ['grid', 'list'];
const FOOTER_STYLES = ['four-col', 'brand'];

const HERO_KICKERS = [
  'Licensed Wildlife Control',
  'Fast, Humane Raccoon Removal',
  '24/7 Emergency Wildlife Response',
  'Trusted Local Wildlife Specialists',
  'Same-Day Inspections Available',
  'Attic & Chimney Wildlife Experts',
  'Locally Operated Trapping Crew',
  'Insured Nuisance Wildlife Control',
  'Full-Service Exclusion & Repair',
  'Raccoon Damage Specialists',
  'Rapid-Response Wildlife Techs',
  'Wildlife Control Done Right',
  'No-Poison, Humane-First Removal',
  'Residential & Commercial Wildlife Control',
];

const HERO_HEADLINES = [
  'Raccoon Removal in {LOC} Done Right',
  '{LOC} Raccoon Removal You Can Trust',
  'Fast, Humane Raccoon Removal Serving {LOC}',
  'Got Raccoons? {LOC}’s Wildlife Team Is Ready',
  'Professional Raccoon Removal for {LOC}',
  'Raccoons in Your Attic? {LOC} Help Is One Call Away',
  '{LOC}’s Go-To Team for Raccoon Problems',
  'Stop Attic Raccoons Fast — {LOC} Service',
  'Humane Raccoon Trapping Across {LOC}',
  'Wildlife in the Attic? We Fix It — {LOC}',
  '{LOC} Homeowners Trust Us for Raccoon Removal',
  'Raccoon Exclusion & Repair for {LOC} Properties',
  'Licensed Raccoon Control Serving {LOC}',
  'End Your Raccoon Problem — {LOC} Team Ready Now',
  '{LOC} Attic Raccoon Removal, Start to Finish',
  'Real Raccoon Solutions for {LOC} Homes & Businesses',
];

const HERO_SUBS = [
  'Scratching in the attic, torn-up soffits, or a raccoon in your chimney — our licensed technicians handle it safely, humanely, and fast.',
  'From attic entry points to full exclusion and cleanup, we solve raccoon problems for homeowners and businesses throughout the {LOC} area.',
  'Raccoons cause real damage fast. Our {LOC} crew inspects, traps, excludes, and repairs so the problem doesn’t come back.',
  'One call gets you a real inspection, a clear plan, and a humane resolution — no guesswork, no scare tactics.',
  'We remove raccoons the right way: humane trapping, one-way exclusion, and permanent entry-point repair.',
  'Noises overhead, a torn vent screen, or a raccoon denning in your chimney — we handle every stage of the problem for {LOC} properties.',
  'Our {LOC} technicians inspect first, explain what they find, then trap, exclude, and repair so raccoons don’t come back next season.',
  'A raccoon problem rarely fixes itself. We bring the equipment, the permits, and the follow-through to close it out for good.',
  'Licensed, insured, and local — we handle raccoon calls across {LOC} with the same humane process every time.',
  'Whether it’s one raccoon or a full litter, our {LOC} crew has the trapping and exclusion experience to resolve it cleanly.',
  'We inspect the whole structure, not just the noisy spot — so every entry point in {LOC} gets sealed, not just the obvious one.',
  'Same process every time: inspect, trap humanely, exclude permanently, repair the damage. No shortcuts.',
  'Raccoons don’t wait for business hours, and neither do we — {LOC} emergency inspections available.',
  'From the first inspection call to the final repair, our {LOC} team keeps you informed at every step.',
];

// Composed from three independently-seeded fragments so the combination
// space (openers × details × closers) is far larger than the number of sites.
const INTRO_OPENERS = [
  'Raccoons are smart, strong, and surprisingly good at finding the weakest point in a roofline, soffit, or chimney cap in {LOC}.',
  'A raccoon looking for shelter in {LOC} will test soffit vents, roof returns, chimney caps, and gable louvers until it finds a way in.',
  'It doesn’t take much for a raccoon to get into a home in {LOC} — a loose vent screen or a gap under a roof edge is usually all it needs.',
  'Raccoons in {LOC} are opportunistic denners, and an attic offers exactly what they’re looking for: warmth, height, and safety from predators.',
  'Once a raccoon finds a way into a structure in {LOC}, it rarely stays hidden for long — the signs show up fast.',
  'Homeowners in {LOC} are often surprised how much damage a single raccoon can do in just a few nights of denning.',
  'Raccoon activity around {LOC} tends to spike as the weather shifts and wild denning spots get harder to find.',
  'A raccoon in an attic in {LOC} isn’t a one-time visitor — once it finds a warm, dry spot, it settles in.',
  'In {LOC}, raccoons commonly target attics, chimneys, and crawl spaces because they mimic the hollow trees raccoons naturally den in.',
  'Attics in {LOC} make ideal raccoon dens: dark, insulated, elevated, and usually quiet during the day.',
];

const INTRO_DETAILS = [
  'Once one gets into an attic, it rarely stays alone for long — mothers den up with litters, and what starts as a scratching noise at night can turn into torn insulation, chewed wiring, and a lingering odor problem within weeks.',
  'If you’ve heard heavy footsteps overhead, found displaced insulation, or noticed a strong, musky smell near your attic vents, you likely have raccoons denning on your property.',
  'A raccoon in the attic is more than a nuisance — their droppings can carry roundworm and other parasites, and their claws tear ductwork and insulation.',
  'A female raccoon will happily raise a litter of kits in your soffit if given the chance, and the noise and mess only grow from there.',
  'What starts as occasional noise at dusk can escalate quickly into torn vents, stained ceilings, and a den full of kits by spring.',
  'Left alone, a denning raccoon will keep widening its entry point, which turns a small repair into a much bigger one.',
  'Raccoon waste accumulates fast in a den site, and the smell alone is often the first thing homeowners notice.',
  'Beyond the noise, raccoons chew wiring and ductwork, which creates real fire and HVAC risks if the problem sits too long.',
  'A single entry point rarely stays single for long — raccoons will widen a gap or open a second one nearby once they’re established.',
  'The longer a raccoon dens undisturbed, the more insulation, wiring, and drywall ends up needing repair afterward.',
];

const INTRO_CLOSERS = [
  'Our team handles raccoon removal throughout {LOC} using humane, code-compliant methods — not poison, not guesswork.',
  'We’ve built our {LOC} raccoon removal process around solving the problem completely: inspect, remove, exclude, repair.',
  'Our {LOC} crew starts with a full inspection so you know exactly what’s going on before any trapping begins.',
  'We handle the entire process for {LOC} properties — humane trapping, permanent exclusion, and the repair work that follows.',
  'Every {LOC} job follows the same standard: locate every entry point, resolve it humanely, then seal it for good.',
  'Our licensed {LOC} technicians document what they find, walk you through the plan, and follow through until it’s fixed.',
  'We treat every {LOC} call as a full job, not a quick trap-and-go — inspection, removal, exclusion, and repair.',
  'For {LOC} homeowners and businesses, that means one team handling inspection through final repair, start to finish.',
  'Our approach in {LOC} focuses on permanent results: seal what let the raccoon in, not just remove the one that’s there now.',
  'We keep {LOC} customers informed at every stage — what we found, what it takes to fix it, and what it costs.',
];

const SIGNS = [
  { t: 'Heavy footsteps or scratching overhead', d: 'Raccoons are large and noisy compared to squirrels or mice — you’ll usually hear movement in the evening and early morning.' },
  { t: 'Torn soffits, vents, or roof edges', d: 'Raccoons use their strength and dexterity to rip open weak points around rooflines and gable vents to get inside.' },
  { t: 'A strong, musky odor', d: 'Urine and droppings build up quickly in a den site and produce a distinct, unpleasant smell you can often notice from inside the home.' },
  { t: 'Visible entry or exit holes', d: 'Chewed fascia boards, pulled-back flashing, or a gap at the chimney cap are all common raccoon access points.' },
  { t: 'Flattened insulation or stained ceiling spots', d: 'Denning raccoons compress insulation and their waste can eventually stain drywall or ceiling tile.' },
  { t: 'Raccoons seen at dusk near the roofline', d: 'Repeated sightings of a raccoon climbing your home in the same spot usually means it already has a way inside.' },
  { t: 'Chewed or displaced roof vent covers', d: 'Raccoons will pry loose or chew through plastic and metal vent covers to widen an opening into the attic.' },
  { t: 'Rustling sounds after dark', d: 'Raccoons are nocturnal, so most activity — and most noise — happens once the house has gone quiet for the night.' },
  { t: 'Paw prints in dust, snow, or mud near the roofline', d: 'Distinct five-toed tracks around downspouts, decks, or roof access points are a strong indicator of raccoon traffic.' },
  { t: 'Trash cans knocked over or raided repeatedly', d: 'Raccoons denning nearby will often forage close to home, and unsecured trash is an easy target.' },
  { t: 'A sagging or stained section of ceiling drywall', d: 'Urine soaking into insulation over time can eventually seep through drywall, leaving a visible stain.' },
  { t: 'Grease marks or smudges around roof entry points', d: 'Raccoons squeezing through tight gaps repeatedly leave dark, oily smudges around the edges of the opening.' },
  { t: 'Unusual pet behavior near a wall or vent', d: 'Dogs and cats will often bark, whine, or stare fixedly at a wall, ceiling, or vent where wildlife is denning nearby.' },
  { t: 'Damaged chimney caps or spark arrestors', d: 'A bent, missing, or pried-open chimney cap is one of the most common raccoon access points in older homes.' },
  { t: 'Loud thumping or rolling sounds during the day', d: 'A litter of kits moving around while the mother is out foraging often sounds like rolling or thumping overhead.' },
  { t: 'A persistent buzzing of flies near the attic', d: 'Flies gathering near soffits or vents can indicate a den site — or, in worse cases, a deceased animal nearby.' },
  { t: 'Visible nesting material pulled through vents', d: 'Shredded insulation, leaves, or debris protruding from a vent or gap is a sign a den is already established.' },
  { t: 'New gaps appearing around existing roof repairs', d: 'A raccoon that finds a previously repaired weak spot will often reopen it rather than search for a brand-new one.' },
  { t: 'Water stains that appear without recent rain', d: 'Urine saturation in insulation can mimic a roof leak, showing up as a ceiling stain with no storm to explain it.' },
  { t: 'A raccoon seen carrying food toward the roofline', d: 'A raccoon repeatedly hauling food up toward the same spot on the roof is very likely feeding kits in an active den.' },
];

const WHY_US = [
  { t: 'Humane methods, every time', d: 'We use one-way exclusion devices and humane live-trapping — never poison, and never anything that leaves orphaned kits trapped inside.' },
  { t: 'Full exclusion, not just trapping', d: 'We seal and reinforce every entry point we find so the next raccoon in the neighborhood can’t just move back in.' },
  { t: 'Licensed & insured technicians', d: 'Our crews follow state wildlife handling regulations and carry insurance for your protection.' },
  { t: 'Attic cleanup & repair', d: 'Beyond removal, we handle contaminated insulation removal, sanitation, and structural repair so your attic is livable again.' },
  { t: 'Real inspections, real answers', d: 'We show you exactly where raccoons are getting in and what it will take to fix it — no upsells, no scare tactics.' },
  { t: 'Local response times', d: 'Our teams are positioned to reach homes and businesses in and around {LOC} quickly, including emergency same-day visits.' },
  { t: 'Clear, written estimates', d: 'You get a documented estimate after the inspection, before any work begins — no surprise charges later.' },
  { t: 'Litter-aware trapping', d: 'When kits are involved, we time exclusion to keep families together and avoid orphaning young raccoons in a sealed attic.' },
  { t: 'Warrantied exclusion work', d: 'The entry points we seal are backed by a workmanship warranty, so a repeat visit for the same spot costs you nothing.' },
  { t: 'One point of contact', d: 'The technician who inspects your property is the same one who handles trapping, exclusion, and repair.' },
  { t: 'Straight talk, no scare tactics', d: 'We explain what we find in plain terms and only recommend work that’s actually needed.' },
  { t: 'Equipped for every access point', d: 'From steep rooflines to tight crawl spaces, our crews carry the equipment to reach every entry point safely.' },
  { t: 'Documented before-and-after photos', d: 'We photograph entry points and completed repairs so you have a clear record of the work performed.' },
  { t: 'Experience with older and historic homes', d: 'We know how to exclude and repair raccoon damage without cutting corners on older roofing, masonry, or trim.' },
  { t: 'Commercial-property experience', d: 'We handle wildlife issues at warehouses, restaurants, and multi-family buildings, not just single-family homes.' },
  { t: 'Follow-up inspections included', d: 'After exclusion work is complete, we check back to confirm the entry point is holding and the raccoon hasn’t returned.' },
  { t: 'Transparent about timelines', d: 'We tell you upfront if a litter means exclusion has to wait, instead of promising a same-day fix that isn’t realistic.' },
  { t: 'Respectful of your property', d: 'Our crews work cleanly, protect landscaping and gutters during roof access, and leave the site as they found it.' },
];

const SERVICES = [
  { t: 'Raccoon Trapping & Removal', d: 'Humane, code-compliant live trapping and removal of adult raccoons and litters from attics, crawl spaces, and yards.' },
  { t: 'Attic Entry Point Exclusion', d: 'One-way doors and permanent sealing of soffits, vents, fascia gaps, and roof returns so raccoons can leave but not re-enter.' },
  { t: 'Attic Damage Restoration', d: 'Contaminated insulation removal, sanitation, deodorizing, and re-insulation after a raccoon has denned in your attic.' },
  { t: 'Chimney Raccoon Removal', d: 'Safe removal of raccoons denning in chimneys, followed by professional chimney cap installation to prevent repeat visits.' },
  { t: 'Dead Raccoon Removal & Odor Control', d: 'Locating and removing deceased animals from wall cavities, crawl spaces, and attics, plus odor remediation.' },
  { t: 'Crawl Space Wildlife Removal', d: 'Removal and exclusion services for raccoons denning under decks, porches, sheds, and crawl spaces.' },
  { t: 'Commercial Wildlife Control', d: 'Raccoon removal and exclusion for warehouses, restaurants, office buildings, and multi-family properties.' },
  { t: 'Preventive Inspections', d: 'Seasonal inspections to catch weak entry points before raccoons find them first.' },
  { t: 'Litter Removal & Reunification', d: 'Careful, humane relocation of raccoon kits and mothers that keeps families together and avoids orphaning young animals.' },
  { t: 'Roof Vent & Soffit Repair', d: 'Reinforced vent screens, soffit panels, and fascia repair built to withstand a raccoon’s strength, not just cosmetic patches.' },
  { t: 'One-Way Door Installation', d: 'Specialized doors that let denning raccoons exit on their own schedule while blocking re-entry from outside.' },
  { t: 'Insulation Removal & Replacement', d: 'Removal of urine- and feces-contaminated insulation followed by professional-grade re-insulation.' },
  { t: 'Trash & Yard Deterrent Consultation', d: 'Practical recommendations for securing trash, pet food, and yard access points that attract raccoons in the first place.' },
  { t: 'Emergency Same-Day Response', d: 'Priority scheduling for active intrusions, exposed entry points, or raccoons trapped inside living spaces.' },
  { t: 'Garage & Outbuilding Removal', d: 'Trapping and exclusion for raccoons denning in garages, sheds, barns, and detached structures.' },
  { t: 'Wildlife Damage Documentation', d: 'Photo-documented inspection reports that homeowners can use for insurance or landlord claims.' },
  { t: 'Deck & Porch Exclusion', d: 'Sealing and reinforcing gaps under decks and porches where raccoons commonly den close to the ground.' },
  { t: 'Multi-Unit Property Inspections', d: 'Building-wide wildlife inspections for apartment complexes and condo associations, coordinated with property managers.' },
  { t: 'Post-Exclusion Verification Visits', d: 'A follow-up visit after exclusion work to confirm the entry point is holding and no raccoon re-entered.' },
  { t: 'Fascia & Roofline Reinforcement', d: 'Structural repair of chewed or torn fascia boards and roof edges to remove weak points raccoons exploit.' },
];

const FAQS = [
  { q: 'Is raccoon removal humane?', a: 'Yes. We use one-way exclusion devices and live traps, checked regularly, and never use poison. Litters are handled carefully to keep families together during relocation or reunification.' },
  { q: 'How much does raccoon removal cost in {LOC}?', a: 'Cost depends on the number of entry points, whether there’s a litter involved, and how much attic repair is needed. We provide a clear, written estimate after a full inspection — call {PHONE} for a quote.' },
  { q: 'How long does the process take?', a: 'A single adult raccoon can often be excluded within a few days. If a litter is denning in the attic, we wait for the kits to be mobile before completing exclusion, which can take one to a few weeks.' },
  { q: 'Can I just seal the entry point myself?', a: 'Not until the raccoon is confirmed out — sealing an active den traps the animal inside, which usually leads to a much worse problem (and a bigger odor issue) than the original one.' },
  { q: 'Do you repair the damage afterward?', a: 'Yes. We offer attic insulation removal and replacement, sanitation, and structural repair for soffits, vents, and fascia after the raccoons are safely excluded.' },
  { q: 'Are raccoons dangerous?', a: 'Raccoons can carry rabies and their droppings can contain roundworm eggs, so direct contact should always be avoided. Our technicians handle wildlife and cleanup safely so you don’t have to.' },
  { q: 'What if there’s a litter of kits in the attic?', a: 'We locate the den, confirm the kits are mobile, and use a one-way door timed so the mother can move them out on her own before we seal the entry point.' },
  { q: 'Do you serve businesses as well as homes?', a: 'Yes. We handle raccoon removal and exclusion for warehouses, restaurants, retail buildings, and multi-family properties in and around {LOC}.' },
  { q: 'Will the raccoon come back after removal?', a: 'Not if the entry point is properly sealed. That’s why exclusion — not just trapping — is the core of our process; a trapped raccoon with an open entry point just gets replaced by the next one.' },
  { q: 'What does an inspection actually involve?', a: 'We check the roofline, soffits, vents, chimney, and foundation for entry points and signs of activity, then walk you through exactly what we found before any work begins.' },
  { q: 'Do you offer emergency service?', a: 'Yes, we prioritize active intrusions and exposed entry points with same-day or next-day emergency appointments where available.' },
  { q: 'Is there a warranty on the repair work?', a: 'Sealed entry points are backed by a workmanship warranty — if a raccoon reopens the same spot, we return to fix it at no extra charge.' },
  { q: 'What smell will I notice, and does it go away?', a: 'A musky, ammonia-like odor from urine and droppings is common with an active den. It fades once contaminated insulation is removed and the area is sanitized.' },
  { q: 'Can raccoons damage electrical wiring?', a: 'Yes, chewed wiring is a common and serious risk with attic denning, which is one more reason to address a raccoon problem quickly rather than wait.' },
  { q: 'Do you use poison?', a: 'No. Poison is not humane, not legal for wildlife control in most jurisdictions, and risks a raccoon dying inside a wall or attic cavity — we don’t use it.' },
  { q: 'How do I know if it’s a raccoon and not a squirrel?', a: 'Raccoons are noticeably heavier and louder overhead than squirrels, and tend to be active mainly at night rather than during the day.' },
  { q: 'What areas around {LOC} do you cover?', a: 'We serve homes and businesses throughout {LOC} and the surrounding area — call {PHONE} to confirm service at your address.' },
  { q: 'Do I need to be home for the inspection?', a: 'It helps, but isn’t always required — we can often complete an exterior inspection and discuss findings with you by phone.' },
];

const CTA_LINES = [
  'Don’t wait for a raccoon problem in {LOC} to get worse — call {PHONE} for a same-day inspection.',
  'One call gets your {LOC} raccoon problem solved for good. Reach us at {PHONE}.',
  'Hear something in the attic? Call {PHONE} and we’ll have a technician out to your {LOC} property fast.',
  'Get a straight answer and a real plan — call our {LOC} raccoon removal team at {PHONE}.',
  'The longer a raccoon dens, the more it costs to fix — call {PHONE} before the damage spreads.',
  'Ready when you are — call {PHONE} for a straightforward inspection of your {LOC} property.',
  'Skip the guesswork. Call {PHONE} and get a licensed technician out to {LOC} fast.',
  'From inspection to repair, we handle it all — call {PHONE} to get started in {LOC}.',
  'Noises overhead shouldn’t wait until they get worse — call {PHONE} today.',
  'Serving {LOC} with humane, permanent raccoon solutions — call {PHONE} now.',
  'Let’s fix it right the first time — call {PHONE} for your {LOC} inspection.',
  'One team, start to finish — call {PHONE} for raccoon removal in {LOC}.',
  'Fast scheduling, real answers — call {PHONE} to book your {LOC} inspection.',
  'A raccoon problem doesn’t fix itself — call {PHONE} and let our {LOC} crew handle it.',
];

const SERVICES_INTRO_LINES = [
  'Every job starts with a full inspection so we can tell you exactly where raccoons are getting in and what it will take to fix it for good.',
  'We don’t quote sight-unseen — every service starts with a real inspection of your {LOC} property.',
  'From the first noise complaint to the final repair, these are the services that get your {LOC} property raccoon-free.',
  'Each of these services can stand alone or combine into a full removal-and-repair job, depending on what our {LOC} inspection finds.',
  'No two raccoon jobs look exactly alike, which is why we scope every {LOC} visit around what’s actually happening at your property.',
];

const SERVICE_AREA_LEADS = [
  'Whether you’re in a dense residential neighborhood or a more rural stretch of {LOC}, our technicians carry the same humane trapping and exclusion equipment to every call.',
  'From tightly packed subdivisions to properties on the edge of {LOC}, our crews bring the same inspection standard and the same equipment to every visit.',
  'Property type doesn’t change our process — homes, townhomes, and commercial buildings across {LOC} all get the same full inspection and exclusion approach.',
  'Older homes, new construction, and everything in between across {LOC} — our technicians adjust the equipment, not the standard.',
  'Whether it’s a single-family home or a multi-unit building in {LOC}, the inspection and exclusion process stays the same.',
];

const FAQ_INTRO_LINES = [
  'Answers to the questions we hear most from {LOC} homeowners and businesses.',
  'The questions {LOC} customers ask before booking an inspection, answered plainly.',
  'Straight answers to the most common raccoon questions we get from {LOC} callers.',
  'What {LOC} homeowners want to know before we show up.',
];

// Heading/eyebrow variants — keeps H1/H2/eyebrow text (not just body copy) from
// repeating verbatim across sites. Every variant keeps the core keyword intact.
const EYEBROW_WHY = ['Why It Happens', 'Understanding the Problem', 'The Root Cause', 'Why Raccoons Get In', "What's Going On", 'Behind the Noise'];
const EYEBROW_SERVICES = ['Our Services', 'What We Do', 'How We Help', 'Services We Offer', 'Full-Service Removal'];
const EYEBROW_AREA = ['Service Area', 'Where We Work', 'Who We Serve', 'Coverage Area', 'Local Coverage'];
const EYEBROW_FAQ = ['Common Questions', 'Frequently Asked', 'Questions & Answers', 'What People Ask'];
const EYEBROW_CONTACT = ['Get In Touch', 'Contact Us', 'Reach Out', 'Talk to Our Team'];
const EYEBROW_WHYUS = ['Why Choose Us', 'The Difference', 'What Sets Us Apart', 'Our Approach'];

const H2_INTRO = [
  'Raccoon Removal in {LOC}',
  '{LOC} Raccoon Problems, Solved',
  'Understanding Raccoon Activity in {LOC}',
  'Why {LOC} Homes Get Raccoons',
  'The {LOC} Raccoon Problem',
  'Raccoons in {LOC}: What to Know',
];
const H2_SERVICES_PREVIEW = [
  'Complete Raccoon & Wildlife Removal',
  'Full-Service Wildlife Solutions',
  'Everything You Need, One Call',
  'Raccoon & Wildlife Services',
  'Removal, Exclusion & Repair',
];
const H2_AREA_INDEX = ['Serving {LOC}', '{LOC} Coverage', 'We Cover {LOC}', 'Proudly Serving {LOC}', 'Working Throughout {LOC}'];
const H1_SERVICES = [
  'Raccoon Removal Services in {LOC}',
  '{LOC} Raccoon Removal Services',
  'Our Raccoon Removal Services',
  'Complete Services for {LOC}',
  'Raccoon & Wildlife Services in {LOC}',
];
const H1_SERVICE_AREA = ['{LOC} Service Area', 'Where We Serve: {LOC}', 'Serving {LOC} and Beyond', '{LOC} Coverage Area', 'Areas We Serve Near {LOC}'];
const H2_AREA_LOCAL = ['Local Response Across {LOC}', 'Fast Response in {LOC}', 'On the Ground in {LOC}', '{LOC} Response Times', 'Local Crews, Local Knowledge'];
const H1_FAQ = ['Raccoon Removal FAQ', 'Frequently Asked Questions', '{LOC} Raccoon Removal FAQ', 'Questions About Raccoon Removal', 'Raccoon Removal: Common Questions'];
const H1_CONTACT = ['Contact {BIZ}', 'Get in Touch With {BIZ}', 'Reach {BIZ}', 'Talk to {BIZ}', 'Contact Our {LOC} Team'];
const H3_SIGNS = ['Signs You Have Raccoons', 'Common Warning Signs', 'How to Tell You Have Raccoons', 'Signs of a Raccoon Problem', 'Is It Raccoons? Look For This'];
const H2_CTA = ['Ready to solve your raccoon problem?', 'Ready to get started?', "Let's fix your raccoon problem", 'Ready when you are', 'One call away from a fix'];
const H2_WHYUS_DIFF = ['The {LOC} Difference', 'Why {LOC} Trusts Us', 'What Makes Us Different', 'Our {LOC} Standard'];

module.exports = {
  hash, pick, pickN, compose,
  THEMES, HERO_STYLES, HEADER_STYLES, SERVICE_STYLES, FOOTER_STYLES,
  HERO_KICKERS, HERO_HEADLINES, HERO_SUBS,
  INTRO_OPENERS, INTRO_DETAILS, INTRO_CLOSERS,
  SIGNS, WHY_US, SERVICES, FAQS, CTA_LINES,
  SERVICES_INTRO_LINES, SERVICE_AREA_LEADS, FAQ_INTRO_LINES,
  EYEBROW_WHY, EYEBROW_SERVICES, EYEBROW_AREA, EYEBROW_FAQ, EYEBROW_CONTACT, EYEBROW_WHYUS,
  H2_INTRO, H2_SERVICES_PREVIEW, H2_AREA_INDEX, H1_SERVICES, H1_SERVICE_AREA,
  H2_AREA_LOCAL, H1_FAQ, H1_CONTACT, H3_SIGNS, H2_CTA, H2_WHYUS_DIFF,
};
