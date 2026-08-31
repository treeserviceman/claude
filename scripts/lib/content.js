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
];

const HERO_HEADLINES = [
  'Raccoon Removal in {LOC} Done Right',
  '{LOC} Raccoon Removal You Can Trust',
  'Fast, Humane Raccoon Removal Serving {LOC}',
  'Got Raccoons? {LOC}’s Wildlife Team Is Ready',
  'Professional Raccoon Removal for {LOC}',
  'Raccoons in Your Attic? {LOC} Help Is One Call Away',
];

const HERO_SUBS = [
  'Scratching in the attic, torn-up soffits, or a raccoon in your chimney — our licensed technicians handle it safely, humanely, and fast.',
  'From attic entry points to full exclusion and cleanup, we solve raccoon problems for homeowners and businesses throughout the {LOC} area.',
  'Raccoons cause real damage fast. Our {LOC} crew inspects, traps, excludes, and repairs so the problem doesn’t come back.',
  'One call gets you a real inspection, a clear plan, and a humane resolution — no guesswork, no scare tactics.',
  'We remove raccoons the right way: humane trapping, one-way exclusion, and permanent entry-point repair.',
];

const INTRO_PARAS = [
  'Raccoons are smart, strong, and surprisingly good at finding the weakest point in a roofline, soffit, or chimney cap. Once one gets into an attic in {LOC}, it rarely stays alone for long — mothers den up with litters, and what starts as a scratching noise at night can turn into torn insulation, chewed wiring, and a lingering odor problem within weeks.',
  'If you’ve heard heavy footsteps overhead, found displaced insulation, or noticed a strong, musky smell near your attic vents, you likely have raccoons denning on your property. Our team handles raccoon removal throughout {LOC} using humane, code-compliant methods — not poison, not guesswork.',
  'A raccoon in the attic is more than a nuisance. Their droppings can carry roundworm and other parasites, their claws tear ductwork and insulation, and a female raccoon will happily raise a litter of kits in your soffit if given the chance. We’ve built our {LOC} raccoon removal process around solving the problem completely: inspect, remove, exclude, repair.',
];

const SIGNS = [
  { t: 'Heavy footsteps or scratching overhead', d: 'Raccoons are large and noisy compared to squirrels or mice — you’ll usually hear movement in the evening and early morning.' },
  { t: 'Torn soffits, vents, or roof edges', d: 'Raccoons use their strength and dexterity to rip open weak points around rooflines and gable vents to get inside.' },
  { t: 'A strong, musky odor', d: 'Urine and droppings build up quickly in a den site and produce a distinct, unpleasant smell you can often notice from inside the home.' },
  { t: 'Visible entry or exit holes', d: 'Chewed fascia boards, pulled-back flashing, or a gap at the chimney cap are all common raccoon access points.' },
  { t: 'Flattened insulation or stained ceiling spots', d: 'Denning raccoons compress insulation and their waste can eventually stain drywall or ceiling tile.' },
  { t: 'Raccoons seen at dusk near the roofline', d: 'Repeated sightings of a raccoon climbing your home in the same spot usually means it already has a way inside.' },
];

const WHY_US = [
  { t: 'Humane methods, every time', d: 'We use one-way exclusion devices and humane live-trapping — never poison, and never anything that leaves orphaned kits trapped inside.' },
  { t: 'Full exclusion, not just trapping', d: 'We seal and reinforce every entry point we find so the next raccoon in the neighborhood can’t just move back in.' },
  { t: 'Licensed & insured technicians', d: 'Our crews follow state wildlife handling regulations and carry insurance for your protection.' },
  { t: 'Attic cleanup & repair', d: 'Beyond removal, we handle contaminated insulation removal, sanitation, and structural repair so your attic is livable again.' },
  { t: 'Real inspections, real answers', d: 'We show you exactly where raccoons are getting in and what it will take to fix it — no upsells, no scare tactics.' },
  { t: 'Local response times', d: 'Our teams are positioned to reach homes and businesses in and around {LOC} quickly, including emergency same-day visits.' },
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
];

const FAQS = [
  { q: 'Is raccoon removal humane?', a: 'Yes. We use one-way exclusion devices and live traps, checked regularly, and never use poison. Litters are handled carefully to keep families together during relocation or reunification.' },
  { q: 'How much does raccoon removal cost in {LOC}?', a: 'Cost depends on the number of entry points, whether there’s a litter involved, and how much attic repair is needed. We provide a clear, written estimate after a full inspection — call {PHONE} for a quote.' },
  { q: 'How long does the process take?', a: 'A single adult raccoon can often be excluded within a few days. If a litter is denning in the attic, we wait for the kits to be mobile before completing exclusion, which can take one to a few weeks.' },
  { q: 'Can I just seal the entry point myself?', a: 'Not until the raccoon is confirmed out — sealing an active den traps the animal inside, which usually leads to a much worse problem (and a bigger odor issue) than the original one.' },
  { q: 'Do you repair the damage afterward?', a: 'Yes. We offer attic insulation removal and replacement, sanitation, and structural repair for soffits, vents, and fascia after the raccoons are safely excluded.' },
  { q: 'Are raccoons dangerous?', a: 'Raccoons can carry rabies and their droppings can contain roundworm eggs, so direct contact should always be avoided. Our technicians handle wildlife and cleanup safely so you don’t have to.' },
];

const CTA_LINES = [
  'Don’t wait for a raccoon problem in {LOC} to get worse — call {PHONE} for a same-day inspection.',
  'One call gets your {LOC} raccoon problem solved for good. Reach us at {PHONE}.',
  'Hear something in the attic? Call {PHONE} and we’ll have a technician out to your {LOC} property fast.',
  'Get a straight answer and a real plan — call our {LOC} raccoon removal team at {PHONE}.',
];

module.exports = {
  hash, pick, pickN,
  THEMES, HERO_STYLES, HEADER_STYLES, SERVICE_STYLES, FOOTER_STYLES,
  HERO_KICKERS, HERO_HEADLINES, HERO_SUBS, INTRO_PARAS,
  SIGNS, WHY_US, SERVICES, FAQS, CTA_LINES,
};
