import hashlib

def pick(seed, variants):
    """Deterministically choose one variant based on a seed string."""
    h = int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16)
    return variants[h % len(variants)]

def pick_n(seed, variants, n):
    """Deterministically choose n distinct variants, order stable per seed."""
    h = int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16)
    idxs = list(range(len(variants)))
    out = []
    for i in range(n):
        j = (h >> (i * 5)) % len(idxs)
        out.append(idxs.pop(j % len(idxs)))
    return [variants[i] for i in out]

# ---------------------------------------------------------------------------
# Full-tier, per-service content blocks. Each block is a list of variants.
# Placeholders filled via str.format(**ctx).
# ---------------------------------------------------------------------------

SERVICE_CONTENT = {

"raccoon-removal": {
"intro": [
"Raccoons in {city} treat attics, chimneys, and crawlspaces like ready-made dens, especially once a female is looking for a quiet spot to raise a litter. We've pulled them out of soffits, insulation, and duct chases all over {county}, and the damage is rarely limited to noise overhead.",
"If you've heard heavy footsteps or scratching in the ceiling after dark in {city}, that's the classic raccoon pattern -- they're nocturnal, they're strong, and they don't leave quietly. We handle raccoon calls across {county} year-round, not just in spring den season.",
"Raccoons are one of the most common wildlife calls we get in {city}. They're smart enough to pry open vents and roof gaps that would keep out most other animals, which is why DIY exclusion attempts here so often fail.",
"A raccoon that's moved into a {city} attic or chimney isn't going to leave on its own, and it will keep tearing at insulation and duct work until it's physically removed. We deal with this pattern constantly in {county}.",
],
"why_here": [
"{climate_sentence} That combination keeps raccoons active on a near year-round schedule here, with the sharpest spike in activity when females den up to have young and again in fall when juveniles disperse and look for their own territory.",
"With {climate}, {city} rarely gives raccoons a reason to fully den down for winter the way they might farther north, so we see steady calls across most of the year rather than one short season.",
"Raccoon pressure in {city} tracks closely with food and shelter access -- open trash, pet food left outside, and older homes with roof gaps all raise the odds. {climate_sentence}",
],
"process": [
"Our process starts with a full exterior inspection to find every entry point -- roof valleys, gable vents, plumbing stacks, and gaps where siding meets the roofline are the usual suspects. We set humane one-way exclusion devices or cage traps depending on the situation, confirm the attic or den space is empty (critical if there are young raccoons involved), then seal every opening with metal flashing or hardware cloth that a raccoon can't tear through.",
"We inspect the roofline, attic, and foundation for access points first, since sealing a home before confirming raccoons are out just traps them inside. Once we've verified the space is clear, we exclude and seal with materials sized to actually stop a raccoon -- not the thin patch jobs that get torn open again within a week.",
"Every job starts the same way: find how they're getting in, check whether there's a litter present, and only then move to trapping or one-way exclusion. After removal we seal entry points with heavy-gauge material and do a final walk of the roof and foundation so there isn't a second way back in.",
],
"signs": [
"Common signs include heavy thumping or rolling sounds in the ceiling at night, matted-down insulation, a strong ammonia smell from urine buildup, torn roof vents or soffits, and raccoon droppings (dark, tubular, often on a roof edge or in a corner of the attic) that should not be handled bare-handed.",
"Homeowners usually notice it first at night -- footsteps overhead, chewing sounds, or a raccoon peering out of a roof gap at dusk. Inside, look for flattened insulation, a strong urine odor, and droppings collected in one latrine spot rather than scattered.",
],
"why_choose_us": [
"We're a local crew that actually climbs the roof and gets into the attic -- not a call center that dispatches a subcontractor. You'll get a real inspection, a clear price before any work starts, and a repair that's built to keep the same raccoon (or the next one) from getting back in.",
"Because we work {county} regularly, we already know which rooflines and building styles tend to give raccoons an opening. That means a faster, more accurate inspection and exclusion work that holds up.",
],
"faq": [
[("Is it legal to remove raccoons myself in {city}?", "Trapping and relocating wildlife is regulated at the state level, and rules on where a raccoon can legally be released vary. Most homeowners are better served by a licensed technician who handles the trapping, transport, and exclusion correctly the first time."),
("Will sealing the entry point trap a raccoon inside?", "It can, if the space isn't checked first -- which is why we always confirm an attic or den is empty (including any young) before we close off the last opening."),
("How fast can you get to a raccoon-in-the-attic call?", "Most {city} calls are scheduled within a day or two; a raccoon actively denning with young sometimes needs a same-week visit to avoid additional attic damage."),
("Do raccoons come back after removal?", "Not through the same opening if it's sealed properly. That's why exclusion material matters as much as the trapping itself.")],
[("What attracts raccoons to homes in {city}?", "Unsecured trash cans, pet food left outdoors overnight, and roof or soffit gaps that offer a dry, quiet den site are the biggest draws we see."),
("Can raccoons cause real damage, or is it just noise?", "Beyond noise, raccoons compress and soil attic insulation, chew wiring and duct work, and their droppings can pose a health risk, so it's worth treating as more than a nuisance."),
("Do you handle raccoons in chimneys too?", "Yes -- chimneys are one of the most common raccoon den sites we find in {city}, especially uncapped ones."),
("Is a single visit usually enough?", "Trapping can take a few days depending on the animal's schedule, but most jobs wrap up with one exclusion and follow-up visit once the space is confirmed empty.")],
],
},

"skunk-removal": {
"intro": [
"Skunks in {city} usually show up under a porch, deck, or shed rather than in the attic, and most calls come in after a homeowner smells them before ever seeing one. We handle skunk removal across {county} with an emphasis on not triggering a spray in the process.",
"A skunk denning under a {city} home is a different job than most wildlife calls -- move too fast or corner the animal wrong, and you get sprayed. We've built our process around avoiding that outcome for both the technician and the property.",
"Skunks are burrowers, so in {city} we find them most often under concrete slabs, decks, and sheds with an open gap underneath rather than up in a roofline. The smell is usually what brings people to call us.",
],
"why_here": [
"{climate_sentence} Skunks don't fully hibernate in conditions like this, so we see activity most of the year, with a clear uptick in late winter and spring when females are denning to have young.",
"Given {climate}, skunk activity in {city} rarely stops completely for the season -- it just slows down. Spring denning and fall dispersal of young are the two periods we get the most calls.",
],
"process": [
"We locate the den entrance first (usually a single hole under a structure, often with disturbed dirt and a musky smell at the opening), then set a covered cage trap positioned to avoid triggering a spray response. Once the animal is out, we close off the gap with buried hardware cloth so nothing digs back in.",
"Because a spooked skunk will spray, our approach favors calm, covered trap sets over anything that corners the animal. After trapping, we seal the den opening below grade with mesh a skunk can't dig through, which is the step most DIY fixes skip.",
],
"signs": [
"The strongest sign is the smell itself, especially at night when skunks are most active, along with small cone-shaped holes in the lawn where they've dug for grubs. A single, larger burrow opening under a deck or shed usually marks the den.",
"Look for a musky odor near a porch or shed, small digging holes across the yard, and -- if pets go outside at night -- a spray incident, which is often the first real clue something has denned nearby.",
],
"why_choose_us": [
"We carry the equipment and experience to trap and remove a skunk without a spray incident on your property, which is the part most homeowners are (understandably) worried about.",
"Skunk jobs reward experience -- knowing how to trap without spooking the animal saves everyone the smell. That's the whole basis of how we run these calls in {city}.",
],
"faq": [
[("How do you remove a skunk without getting sprayed?", "Slow, covered trap sets and giving the animal a clear, calm path into the trap are the keys -- we avoid cornering or startling it."),
("Where do skunks usually den in {city}?", "Under decks, sheds, porches, and concrete slabs with a gap underneath are the most common spots we find."),
("Will sealing the den entrance solve the smell?", "Once the skunk is removed and the entrance is sealed with buried mesh, the odor fades over days to a couple of weeks as it airs out."),
("Are skunks dangerous?", "They're not aggressive, but they can carry rabies, so any skunk acting disoriented or approaching people should be treated as a health risk and not handled directly.")],
],
},

"mosquito-control": {
"intro": [
"Mosquito calls in {city} almost always trace back to standing water somewhere on or near the property -- a clogged gutter, a forgotten bucket, a low spot in the yard that holds rain. We treat the yard and hunt down that water source, because spraying alone without removing breeding sites just means retreating every few weeks.",
"If evenings outside in {city} have become unbearable, it's usually a breeding-site problem more than a one-time invasion. Our mosquito control combines yard treatment with identifying the standing water that's producing new mosquitoes every 7 to 10 days.",
"Mosquitoes only need about a bottle cap of standing water to breed, which is why {city} yards with gutters, drainage issues, or nearby low ground stay problem spots season after season without ongoing treatment.",
],
"why_here": [
"{climate_sentence} That kind of warmth and moisture is close to ideal for mosquito breeding cycles, which is why {city} properties often need control from spring through fall rather than a single treatment.",
"Given {climate}, mosquito populations in {city} can rebound quickly after rain, since eggs laid in damp soil can hatch as soon as the area floods again.",
],
"process": [
"We start with a property walk to find standing water -- gutters, drainage low spots, plant saucers, tarps, anything holding water for more than a few days -- and address what we can directly. Then we apply a barrier treatment to vegetation, mulch beds, and shaded resting areas where adult mosquitoes hide during the day, which knocks down the existing population and keeps new ones from settling in.",
"Treatment targets two things: the adult mosquitoes resting in shrubs and shaded areas, and the standing water producing the next generation. We treat foliage and moisture-holding areas around the yard on a recurring schedule through the season, since a single visit won't hold against new rainfall.",
],
"signs": [
"The obvious sign is getting bitten within minutes of stepping outside, especially at dawn and dusk. Standing water anywhere on the property -- even small amounts -- is the underlying cause worth checking for.",
],
"why_choose_us": [
"We treat mosquito control as a season-long program, not a single spray, because that's what actually holds up against {city}'s conditions. Recurring visits are built around your yard's specific water and shade patterns.",
],
"faq": [
[("How often do you need to treat for mosquitoes in {city}?", "Most properties here do best on a recurring schedule through the warm months -- typically every 21 to 30 days -- since new eggs keep hatching after rain."),
("Is mosquito treatment safe for pets and kids?", "We use products labeled for residential use and let treated areas dry before pets or kids go back outside, which is a short window on most visits."),
("Can you get rid of mosquitoes completely?", "No treatment eliminates every mosquito that flies in from a neighboring property, but a barrier treatment plus water reduction cuts the population dramatically in the treated yard."),
("What can I do between visits?", "Dump standing water weekly -- gutters, saucers, buckets, tarps -- since that alone removes a big share of local breeding sites.")],
],
},

"rat-control": {
"intro": [
"Rats in {city} are drawn to homes with easy food access and a way inside -- a gap under a door, a vent without a screen, a roofline seam. Once they're in a wall void or attic, they multiply fast, so we treat rat calls as a race against the breeding cycle, not just a baiting job.",
"A rat problem in {city} is rarely just one rat. Hearing scratching in the walls at night usually means there's already an active nest, and we build our approach around finding it rather than just placing bait and hoping.",
"We get steady rat and mouse calls in {county}, particularly in older homes and anywhere food waste is accessible outside. Exclusion matters as much as baiting here -- a rat can squeeze through a gap the size of a quarter.",
],
"why_here": [
"{climate_sentence} Rats don't need much of a break from the cold to stay active outdoors, and {city}'s conditions rarely force them to shelter indoors the way harsher winters elsewhere might.",
"Rodent pressure in {city} tends to rise whenever outdoor food sources -- trash, pet food, bird feeders -- are easy to reach, which is a bigger driver here than the season itself.",
],
"process": [
"We start with an inspection for entry points, droppings, gnaw marks, and grease trails along baseboards or beams, which tell us where rats are traveling. Exclusion work seals gaps with steel wool, hardware cloth, or metal flashing (never anything a rat can chew through), and we place tamper-resistant bait stations or snap traps based on the level of activity.",
"Because rats reuse the same paths, tracking grease marks and droppings usually leads us straight to the entry point and nest area. We combine sealing that access with traps or bait stations, then follow up to confirm activity has actually stopped -- not just quieted down.",
],
"signs": [
"Look for droppings (dark, rice-grain sized, often along walls or in cabinets), gnaw marks on wood or wiring, greasy rub marks along baseboards, and scratching sounds in walls or the attic at night.",
],
"why_choose_us": [
"We don't just drop bait and leave -- we find and seal the entry point, because bait alone doesn't stop new rats from replacing the ones that die off.",
],
"faq": [
[("How do I know if it's rats or mice in my {city} home?", "Rat droppings are noticeably larger (about the size of a raisin vs. a grain of rice for mice), and rats tend to be louder and bolder in their movement through walls and attics."),
("How long does rat control take to work?", "Exclusion stops new entry immediately; clearing an existing population with traps or bait typically takes one to three weeks depending on how established the nest is."),
("Is rat bait safe around pets?", "We use tamper-resistant, lockable bait stations specifically to keep pets and children away from the bait itself."),
("Can rats really fit through small gaps?", "Yes -- an adult rat can squeeze through an opening about the size of a quarter, which is why sealing gaps is as important as trapping.")],
],
},

"roach-control": {
"intro": [
"Roach calls in {city} almost always start in the kitchen or bathroom, and by the time they're visible during the day, the population is usually well established behind walls and under appliances. We treat with gel bait and targeted crack-and-crevice application rather than a visible spray, because that's what actually breaks the breeding cycle.",
"If you're seeing roaches in daylight in {city}, that's a sign of a larger population than what's visible -- German roaches especially hide deep in cracks and only come out at night under normal conditions. Our treatment focuses on where they're actually breeding, not just where they're seen.",
],
"why_here": [
"{climate_sentence} Roaches thrive in that kind of warmth and humidity, and they don't need much of it -- moisture behind a leaking pipe or under a dishwasher is often enough to sustain an infestation indoors regardless of the season outside.",
"German roaches in particular can maintain an indoor population in {city} year-round once established, since they rely on warm, moist indoor microclimates rather than outdoor conditions.",
],
"process": [
"We inspect kitchens, bathrooms, and appliance motor compartments (refrigerators, dishwashers) first, since that's where German roaches concentrate. Treatment is targeted gel bait placed in cracks and voids plus a growth regulator to break the egg cycle, rather than a visible perimeter spray that pushes roaches deeper into walls.",
"Because roaches avoid open, treated surfaces, effective control means getting bait into the cracks, hinges, and voids where they actually live. We follow up to confirm the egg cycle has broken, since one visit often isn't enough for an established population.",
],
"signs": [
"Signs include a musty odor in cabinets, small dark droppings resembling coffee grounds or pepper, egg cases (oothecae) tucked into cracks, and roaches spotted in daylight -- a sign the hidden population is significant.",
],
"why_choose_us": [
"Roach control is about precision, not volume -- we place bait exactly where roaches travel and breed, which gets faster, more lasting results than a broad spray.",
],
"faq": [
[("Why do I still see roaches after spraying myself?", "Store-bought sprays often push roaches deeper into wall voids instead of eliminating the colony; gel bait placed directly in cracks and harborage areas is far more effective."),
("How long does roach treatment take to work?", "Most {city} homes see a significant drop within one to two weeks as roaches feed on bait and carry it back to the colony; a follow-up visit confirms the egg cycle is broken."),
("Are roaches a health concern, not just gross?", "Yes -- roaches can trigger asthma and allergies and contaminate food surfaces, which is part of why we treat infestations as more than a cosmetic issue."),
("Do I need to throw everything out of my cabinets?", "Usually not -- we can treat around stored food and dishes; we'll tell you specifically what to clear if a particular area needs it.")],
],
},

"bed-bug-treatment": {
"intro": [
"Bed bugs in {city} don't care how clean a home is -- they travel in luggage, used furniture, and shared laundry facilities, which is why we see them in every part of {county}, not just older housing. Our treatment combines heat and targeted chemical application because bed bugs have grown resistant to many sprays used alone.",
"A bed bug call in {city} usually starts with bites that appeared overnight and small blood spots on sheets. Because bed bugs hide deep in seams, frames, and baseboards, effective treatment has to reach those hiding spots directly, not just the mattress surface.",
],
"why_here": [
"{climate_sentence} Bed bugs are actually less dependent on outdoor climate than most pests since they live entirely indoors, which is why we treat bed bug calls in {city} on a year-round basis with no real seasonal dip.",
],
"process": [
"We start with a room-by-room inspection using a flashlight and inspection tools to check mattress seams, box springs, bed frames, baseboards, and nearby furniture -- bed bugs hide within a few feet of where people sleep. Depending on the level of infestation, we use targeted heat treatment (which kills bugs and eggs in a single pass) or a combination of residual and contact insecticide applied directly into cracks and seams.",
"Because bed bugs and their eggs hide in tight seams and voids, inspection has to be thorough before treatment starts. We treat mattress and furniture seams, baseboards, outlet covers, and any adjoining rooms with activity, then schedule a follow-up to confirm the population is gone.",
],
"signs": [
"Look for small rust-colored spots on sheets (crushed bugs or fecal spots), tiny pale eggshells in mattress seams, a sweet musty odor in heavy infestations, and bites that appear in a line or cluster after sleeping.",
],
"why_choose_us": [
"Bed bugs require thorough, methodical treatment -- cutting corners here just means they come back in a few weeks. We inspect and treat every adjoining space where they could be hiding, not just the bed itself.",
],
"faq": [
[("How do I know if it's bed bugs and not another bug?", "Rust-colored spots on sheets, small pale eggshells in mattress seams, and bites appearing in a line are the clearest signs; we can confirm with an in-person inspection."),
("Does heat treatment really kill bed bugs and eggs?", "Yes -- raising a room to the right sustained temperature kills bed bugs at every life stage, including eggs, which chemical treatment alone can struggle with."),
("Do I need to throw away my mattress?", "Usually not -- a properly treated mattress (often with an encasement afterward) can be kept; replacement is rarely necessary."),
("How many visits does bed bug treatment take?", "Most {city} cases need an initial treatment plus a follow-up 10 to 14 days later to catch any bugs that hatched after the first visit.")],
],
},
}

# ---------------------------------------------------------------------------
# Stub-tier: short, varied blurbs (2-3 sentences) per service, used on the
# lightweight combined city page for cities outside the full-content tier.
# ---------------------------------------------------------------------------

STUB_CONTENT = {
"raccoon-removal": [
"Raccoons around {city} den in attics, chimneys, and crawlspaces, and once inside they tear at insulation and duct work until they're physically removed. We handle trapping, humane exclusion, and entry-point sealing for homes throughout {county}.",
"A raccoon in the attic doesn't leave on its own -- it takes trapping or one-way exclusion plus sealing the entry point with material it can't tear through. We cover raccoon removal for {city} and the surrounding {county} area.",
"Heavy footsteps overhead after dark, torn roof vents, and matted attic insulation are the usual signs of raccoons in {city} homes. We inspect, trap or exclude, and seal the opening for good.",
],
"skunk-removal": [
"Skunks in {city} typically den under decks, sheds, and porches, and most calls start with the smell before anyone spots the animal. We trap carefully to avoid a spray incident, then seal the den entrance.",
"A skunk denning under a structure in {county} needs a slow, careful trap set -- corner it wrong and you get sprayed. We handle removal and entry sealing for homes around {city}.",
"If you're noticing a musky odor near a porch or shed in {city}, a skunk has likely denned nearby. We remove the animal without triggering a spray and close off the burrow afterward.",
],
"mosquito-control": [
"Mosquito problems in {city} almost always trace back to standing water on the property. We treat yards and target breeding sites so evenings outside are actually usable again.",
"With {climate}, mosquito breeding can restart within days of any rainfall in {county}. Our treatment combines a yard barrier spray with hunting down standing water sources.",
"A single mosquito treatment rarely holds for a full season in {city} -- we run recurring visits timed to the local rain and breeding cycle.",
],
"rat-control": [
"Rats get into {city} homes through gaps as small as a quarter and multiply fast once inside a wall void or attic. We seal entry points and combine trapping or baiting to clear an active population.",
"Scratching in the walls at night in {county} usually means an active rat nest, not just a single animal passing through. We track entry points and treat accordingly.",
"Rodent pressure in {city} rises wherever outdoor food access is easy. We handle both the exclusion work and the trapping or baiting needed to stop an active infestation.",
],
"roach-control": [
"Seeing roaches during the day in a {city} home usually means the hidden population is significant. We use targeted gel bait in cracks and voids rather than a visible spray that just scatters them.",
"German roaches concentrate around kitchens and bathrooms in {county} homes, feeding off warmth and moisture indoors. Our treatment targets those harborage points directly.",
"Roach control that actually works means bait exactly where they travel and breed -- we handle that precisely for homes throughout {city}.",
],
"bed-bug-treatment": [
"Bed bugs travel in luggage and used furniture, so they show up throughout {city} regardless of how clean a home is. We treat mattress seams, frames, and baseboards with heat and targeted application.",
"Rust-colored spots on sheets and bites in a cluster after sleeping are the classic signs of bed bugs in {county} homes. We inspect thoroughly and treat every hiding spot, not just the mattress.",
"Because bed bugs hide deep in seams and voids, a full room inspection matters as much as the treatment itself. We handle both for {city} homes.",
],
}
