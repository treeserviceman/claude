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
# Full-tier, per-service content blocks. Each block is a list of variants
# (str.format(**ctx) placeholders). Combined with per-city facts, these
# blocks build a 1,000+ word landing page with no filler -- every block
# carries real, service-specific information a homeowner can act on.
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
"biology": [
"Raccoons are intelligent, dexterous animals -- their front paws work almost like hands, which is how they pry up loose shingles, pop off vent covers, and unlatch anything that isn't fastened down tightly. They're primarily active from dusk to early morning and spend daylight hours denning somewhere dark and enclosed, which is exactly what an attic, chimney, or crawlspace offers. A female typically has one litter of two to five kits a year, most often between March and June, and she won't abandon a newborn litter unless she feels the den is no longer safe -- which is part of why timing and technique matter in a removal. Outside of denning season, raccoons still return nightly to any reliable food and shelter source, so an entry point left unsealed rarely stays unused for long.",
"An adult raccoon can weigh 10 to 20 pounds and is strong enough to bend loose flashing, tear through soffit vents, and widen an existing gap far beyond what it needed to get in the first time. They're also surprisingly good climbers, using downspouts, tree limbs overhanging the roofline, and even brick siding to reach the upper stories of a home. Raccoons are omnivorous and opportunistic, which means an easy food source -- open garbage, compost, pet food -- keeps them circling a property even when they aren't denning there yet. Once a raccoon establishes a den and starts raising young, it treats that space as safe territory and will typically fight to stay rather than relocate on its own.",
"Raccoons don't truly hibernate; in most climates they simply reduce activity during the coldest stretches and rely on stored body fat, which means a den site that's warm and dry -- like an insulated attic -- is especially valuable to them heading into winter. Kits stay in the den for roughly eight to ten weeks before they start following their mother out at night, and during that window the den is at its most active, with near-constant traffic in and out. Raccoons are also known to use more than one den site in rotation, so a property that's hosted a raccoon before is statistically more likely to host one again unless the original entry point was permanently sealed.",
],
"health_risks": [
"Beyond the noise and structural damage, raccoons pose a real health consideration. Raccoon roundworm (Baylisascaris procyonis) can be present in their droppings and remains infectious in soil for a long time, which is why we don't recommend homeowners clean out a raccoon latrine themselves. Raccoons are also a notable rabies vector species in much of the country, and any raccoon that seems disoriented, unusually aggressive, or active in daylight for no clear reason should be treated as a possible health risk rather than approached. On the property side, a denning raccoon compresses and soils attic insulation, and the added weight and moisture from urine can eventually stain drywall ceilings below.",
"The most common health issue we see tied to raccoon activity isn't the animal itself but what it leaves behind -- accumulated droppings in one latrine spot, which can harbor roundworm eggs, and urine-saturated insulation, which loses its effectiveness and can promote mold growth in humid conditions. Raccoons will also chew on wiring and duct work while denning, which is a fire and HVAC-efficiency risk that's easy to miss until a utility bill spikes or an outlet stops working. We treat contaminated insulation removal as a separate step from the trapping itself for exactly this reason.",
"Raccoons carry the potential for rabies, and while most human exposure risk comes from direct contact (a bite or scratch) rather than casual proximity, it's still a reason to avoid handling one directly, even a raccoon that looks sick or orphaned. Their droppings can also carry salmonella and leptospira bacteria in addition to roundworm, so any latrine site in an attic or on a deck should be cleaned up with gloves and proper containment rather than swept aside. Structurally, a raccoon den left in place for a full season can leave behind enough compressed and soiled insulation that a partial re-insulation job is needed after removal.",
],
"process": [
"Our process starts with a full exterior inspection to find every entry point -- roof valleys, gable vents, plumbing stacks, and gaps where siding meets the roofline are the usual suspects. We set humane one-way exclusion devices or cage traps depending on the situation, confirm the attic or den space is empty (critical if there are young raccoons involved), then seal every opening with metal flashing or hardware cloth that a raccoon can't tear through. A final inspection of the whole roofline and foundation follows, since raccoons will test any weak point nearby once their usual entrance is closed off.",
"We inspect the roofline, attic, and foundation for access points first, since sealing a home before confirming raccoons are out just traps them inside. Once we've verified the space is clear -- including checking for a litter, which changes the timeline -- we exclude and seal with materials sized to actually stop a raccoon, not the thin patch jobs that get torn open again within a week. Where insulation has been compressed or soiled by a den, we'll flag it for cleanup so the attic isn't left holding moisture and odor after the animal is gone.",
"Every job starts the same way: find how they're getting in, check whether there's a litter present, and only then move to trapping or one-way exclusion. One-way doors let the adult raccoon leave to feed at night but not re-enter, which is often the fastest and least stressful method when there's no litter involved; a full cage trap is used when the animal needs to be physically relocated. After removal we seal entry points with heavy-gauge material and do a final walk of the roof and foundation so there isn't a second way back in, then follow up to confirm no new activity has started nearby.",
],
"signs": [
"Common signs include heavy thumping or rolling sounds in the ceiling at night, matted-down insulation, a strong ammonia smell from urine buildup, torn roof vents or soffits, and raccoon droppings (dark, tubular, often on a roof edge or in a corner of the attic) that should not be handled bare-handed. A visible paw-shaped track in soft dirt near the foundation, or a torn section of screen on a gable vent, both point to an active entry point worth inspecting before it gets wider.",
"Homeowners usually notice it first at night -- footsteps overhead, chewing sounds, or a raccoon peering out of a roof gap at dusk. Inside, look for flattened insulation, a strong urine odor, and droppings collected in one latrine spot rather than scattered, which is a raccoon habit that differs from most other attic wildlife. Outside, check for smudge marks (body oil trails) around a vent or gap that's being used repeatedly, and any bent or pried-up flashing along the roofline.",
],
"prevention": [
"Trim tree limbs back at least 6-8 feet from the roofline -- raccoons use overhanging branches as a bridge onto the roof.",
"Cap the chimney with a certified chimney cap; an open flue is one of the most common raccoon entry points we find.",
"Install secure lids on trash cans and bring pet food inside at night; easy food access is the single biggest thing that keeps raccoons returning to a property.",
"Cover soffit and gable vents with heavy-gauge hardware cloth, not standard window screen, which a raccoon can tear through in minutes.",
"Check attic access points, roof valleys, and any gap where a utility line enters the house at least once a year, ideally before spring denning season.",
"Keep compost bins secured with a locking lid rather than an open pile, especially if it's within a few feet of the house.",
"Seal gaps around dormers and where additions meet the original roofline -- these transition points are common weak spots on older homes.",
"If a raccoon has denned in the attic before, assume it (or another raccoon) will try the same spot again unless the original entry point was permanently sealed, not just blocked.",
],
"diy_vs_pro": [
"A single raccoon sighting in the yard usually doesn't need professional intervention -- securing trash and pet food is often enough to move it along. Once a raccoon is denning inside a structure, though, DIY trapping gets complicated fast: state regulations govern where trapped wildlife can legally be released, a trap set incorrectly can injure the animal or fail to hold it, and if there's a litter involved, removing the adult without finding the young first leaves kits to die in the wall or attic, which creates an odor and pest problem far worse than the original one. That combination is why most {city} homeowners call a professional once raccoons are confirmed inside rather than after weeks of DIY attempts.",
"Homeowners can reasonably handle prevention -- trimming branches, capping the chimney, securing trash -- without any professional help. Where it gets harder is exclusion and trapping once a raccoon is already established: raccoons are strong enough to defeat store-bought traps not rated for their weight, and one-way exclusion timing has to account for whether young are present, which usually requires an in-person inspection to determine. Attempting removal without confirming the den is empty is the single most common DIY mistake we see, and it's the one most likely to leave a bigger problem behind the walls.",
],
"seasonal_timing": [
"Spring is peak raccoon season in {city} -- females are denning to have young, which means an active den found between March and June likely has kits that need to be accounted for before exclusion work starts. Fall brings a second, smaller wave as juveniles disperse from their mother and look for their own territory, often testing attics and sheds they haven't tried before. Calls do come in year-round, but if you're weighing whether to act now or wait, an active raccoon during either of those two windows is more likely to be denning than just passing through.",
"We get raccoon calls in {city} across every season, but the urgency changes with the calendar. A raccoon found denning in spring is almost certainly a female with young, which changes both the timeline and the method for removal. One found in late summer or fall is more often a juvenile or an adult stocking up before the cold months, which is typically a more straightforward single-animal removal. Winter calls are less frequent but not rare, since a warm attic is valuable shelter regardless of the season.",
],
"why_choose_us": [
"We're a local crew that actually climbs the roof and gets into the attic -- not a call center that dispatches a subcontractor. You'll get a real inspection, a clear price before any work starts, and a repair that's built to keep the same raccoon (or the next one) from getting back in.",
"Because we work {county} regularly, we already know which rooflines and building styles tend to give raccoons an opening. That means a faster, more accurate inspection and exclusion work that holds up.",
],
"faq": [
("Is it legal to remove raccoons myself in {city}?", "Trapping and relocating wildlife is regulated at the state level, and rules on where a raccoon can legally be released vary. Most homeowners are better served by a licensed technician who handles the trapping, transport, and exclusion correctly the first time."),
("Will sealing the entry point trap a raccoon inside?", "It can, if the space isn't checked first -- which is why we always confirm an attic or den is empty (including any young) before we close off the last opening."),
("How fast can you get to a raccoon-in-the-attic call?", "Most {city} calls are scheduled within a day or two; a raccoon actively denning with young sometimes needs a same-week visit to avoid additional attic damage."),
("Do raccoons come back after removal?", "Not through the same opening if it's sealed properly with the right material. That's why exclusion work matters as much as the trapping itself -- a cheap patch job just invites a repeat visit."),
("What attracts raccoons to homes in {city}?", "Unsecured trash cans, pet food left outdoors overnight, and roof or soffit gaps that offer a dry, quiet den site are the biggest draws we see."),
("Can raccoons cause real damage, or is it just noise?", "Beyond noise, raccoons compress and soil attic insulation, chew wiring and duct work, and their droppings can pose a health risk, so it's worth treating as more than a nuisance."),
("Is a single visit usually enough?", "Trapping can take a few days depending on the animal's schedule, but most jobs wrap up with one exclusion visit once the den is confirmed empty, followed by a check-in to verify no new activity has started."),
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
"biology": [
"Skunks are nocturnal, solitary foragers that dig for grubs, insects, and small rodents in lawns, which is why cone-shaped digging holes across a yard are often the first sign of activity before the smell shows up. They're not aggressive by nature and will typically give a warning -- stomping their front feet, raising their tail, sometimes a hissing sound -- before spraying, which only happens as a last resort when a skunk feels cornered or can't retreat. A skunk's spray glands hold enough for five or six sprays before they need time to replenish, and the scent can carry over a mile downwind, which is why even one incident near a home is so noticeable.",
"Skunks are opportunistic diggers rather than climbers, so unlike raccoons they're not typically an attic problem -- their entry point is almost always at ground level, under a structure with a gap they can widen. A female usually has one litter of four to six kits in late spring, and the young stay in the den for about eight weeks before starting to forage alongside her at night. Skunks are also known to reuse den sites across multiple seasons if they aren't disturbed, which is part of why the same yard can have repeat skunk activity year after year.",
"Skunks have poor eyesight and rely heavily on smell and hearing, which means they're often unaware a person is nearby until they're quite close -- part of why surprise encounters happen even when a skunk isn't looking for confrontation. They're omnivorous, eating everything from grubs and beetles to fallen fruit and, when available, pet food left outside. Skunks are also a known rabies vector species, so any skunk that's active during the day, appears disoriented, or seems unusually unafraid of people is a reason to stay back and call a professional rather than assume it's just bold.",
],
"health_risks": [
"Beyond the spray itself, skunks are one of the more commonly reported rabies vector species in much of the country, so any skunk behaving abnormally (daytime activity, stumbling, unusual aggression) should be treated as a potential health risk rather than approached or fed. Skunk spray itself isn't typically dangerous to humans but can cause temporary eye irritation and nausea at close range, and it's genuinely difficult to fully remove from fabric, siding, or pet fur without the right cleaning approach. A den site left under a structure for a season can also leave behind a strong, lingering odor in the soil that takes time to air out even after the animal is gone.",
"The biggest practical risk with skunks is what happens if a pet corners one -- dogs especially tend to investigate rather than avoid, and a spray at close range can cause temporary but significant eye and nasal irritation for the animal. Skunks denning under a deck or porch can also undermine soil stability over time as their burrow network expands, which is a secondary structural concern in addition to the odor. As with other wildlife, we recommend against DIY handling of a skunk den, both for spray risk and the small but real possibility of rabies exposure.",
],
"process": [
"We locate the den entrance first (usually a single hole under a structure, often with disturbed dirt and a musky smell at the opening), then set a covered cage trap positioned to avoid triggering a spray response. Once the animal is out, we close off the gap with buried hardware cloth so nothing digs back in, extending the barrier below grade since skunks will simply dig under a surface-level patch.",
"Because a spooked skunk will spray, our approach favors calm, covered trap sets over anything that corners the animal. We check for young before finalizing removal, since a den with kits needs a different timeline than a single adult. After trapping, we seal the den opening below grade with mesh a skunk can't dig through, which is the step most DIY fixes skip -- a surface patch alone rarely holds.",
],
"signs": [
"The strongest sign is the smell itself, especially at night when skunks are most active, along with small cone-shaped holes in the lawn where they've dug for grubs. A single, larger burrow opening under a deck or shed usually marks the den, often with a well-worn path leading to and from it.",
"Look for a musky odor near a porch or shed, small digging holes across the yard, and -- if pets go outside at night -- a spray incident, which is often the first real clue something has denned nearby. Fresh digging at the edge of a concrete slab or foundation is also worth checking, since that's a common spot for a den entrance to start.",
],
"prevention": [
"Seal gaps under decks, sheds, and porches with buried hardware cloth extending at least 12 inches below grade -- a surface-level patch alone won't stop a skunk from digging under it.",
"Keep pet food and water bowls inside at night; outdoor pet food is one of the most reliable skunk attractants we see.",
"Treat the lawn for grubs if digging holes are widespread -- skunks are foraging for a food source, and removing it makes the yard less attractive.",
"Secure trash cans with tight-fitting lids and avoid leaving bagged garbage out overnight.",
"Install motion-activated lights near common den sites (under decks, sheds); skunks generally avoid well-lit, high-traffic areas.",
"If you see a skunk during the day, keep pets inside and stay back -- daytime activity can (though doesn't always) signal illness.",
],
"diy_vs_pro": [
"Filling in a few grub-digging holes and switching to a covered trash can is reasonable DIY prevention. Actually trapping a skunk yourself is a different story: a spooked skunk in a homemade trap set too close to a doorway or patio can spray the exact area you're trying to protect, and cleaning up spray from siding, decking, or a pet is genuinely difficult without the right products. There's also the rabies-vector consideration -- handling a live skunk carries real risk that a licensed technician is equipped and insured to manage.",
"Most of what keeps skunks away long-term (sealing gaps, securing food sources, treating for grubs) is homeowner-friendly work. Where professional help earns its cost is the trapping and removal step itself, since a poorly placed trap is more likely to result in a spray incident than a successful capture, and confirming whether kits are present changes the entire approach.",
],
"seasonal_timing": [
"Late winter into spring is when we see the most skunk activity in {city}, as females den up to have young; a den found during this window very likely has kits that need to be accounted for. Late summer and fall bring a second wave as juveniles disperse and look for their own territory, often trying yards and outbuildings they haven't used before.",
"Skunk activity in {city} follows a fairly predictable pattern: a spring denning peak, a quieter summer while young are maturing in the den, and a fall dispersal period as juveniles move out on their own. Calls can come in during any season, but knowing which part of that cycle you're in helps set expectations for timeline and technique.",
],
"why_choose_us": [
"We carry the equipment and experience to trap and remove a skunk without a spray incident on your property, which is the part most homeowners are (understandably) worried about.",
"Skunk jobs reward experience -- knowing how to trap without spooking the animal saves everyone the smell. That's the whole basis of how we run these calls in {city}.",
],
"faq": [
("How do you remove a skunk without getting sprayed?", "Slow, covered trap sets and giving the animal a clear, calm path into the trap are the keys -- we avoid cornering or startling it, and we check for a den entrance before setting anything."),
("Where do skunks usually den in {city}?", "Under decks, sheds, porches, and concrete slabs with a gap underneath are the most common spots we find, almost always at ground level rather than up in the roof."),
("Will sealing the den entrance solve the smell?", "Once the skunk is removed and the entrance is sealed with buried mesh, the odor fades over days to a couple of weeks as it airs out; heavily soiled soil near the den can take a bit longer."),
("Are skunks dangerous?", "They're not aggressive, but they can carry rabies, so any skunk acting disoriented or approaching people should be treated as a health risk and not handled directly."),
("How do I get skunk smell off my dog?", "Tomato juice is mostly a myth -- a mix of hydrogen peroxide, baking soda, and dish soap works far better; we're happy to walk you through it if your pet gets sprayed."),
("Do skunks come back to the same den site?", "They can, especially if the burrow isn't sealed below grade. That's why we always extend hardware cloth well under the surface rather than just patching the visible opening."),
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
"biology": [
"A mosquito's full life cycle from egg to biting adult can take as little as 7 to 10 days in warm weather, which is why a yard can go from mosquito-free to unbearable within about a week of a single rainstorm. Female mosquitoes are the ones that bite -- they need a blood meal to develop eggs -- and they lay those eggs directly on or near standing water, sometimes on damp soil that will flood later rather than in water itself. Most species stay within a few hundred feet of where they hatched their whole lives, which is why treating a single neighboring property rarely solves a problem on its own; the source is almost always closer than people expect.",
"Mosquitoes are most active at dawn and dusk for most common species, though some (like the Asian tiger mosquito) will bite aggressively during the day, especially in shaded areas. Adult mosquitoes rest in vegetation, mulch beds, and other shaded, humid spots during the heat of the day, which is exactly where a barrier treatment is aimed. A single female can lay 100 to 300 eggs per batch and multiple batches over her roughly two-to-three-week lifespan, which is how a small amount of standing water turns into a full-yard problem so quickly if it isn't addressed.",
],
"health_risks": [
"Beyond the itch, mosquitoes are a genuine disease vector -- West Nile virus is the most consistently reported mosquito-borne illness across the country, and depending on the region, other viruses can circulate as well. Most bites don't lead to illness, but the risk is real enough that reducing mosquito exposure is a legitimate health measure, not just a comfort one, especially for young children, older adults, and anyone spending significant time outdoors. Standing water on a property is also a shared risk with neighbors, since mosquitoes don't respect property lines once they're airborne.",
"The health concern with mosquitoes scales with how much time people spend outdoors and how close standing water sits to where they gather -- a patio next to a low, damp corner of the yard is a higher-exposure setup than a similar yard without that water source. Mosquito-borne illness risk varies by region and season, but the itching, swelling, and sleep disruption from a heavy mosquito season are a near-universal quality-of-life issue on their own, which is usually what actually drives the call.",
],
"process": [
"We start with a property walk to find standing water -- gutters, drainage low spots, plant saucers, tarps, anything holding water for more than a few days -- and address what we can directly. Then we apply a barrier treatment to vegetation, mulch beds, and shaded resting areas where adult mosquitoes hide during the day, which knocks down the existing population and keeps new ones from settling in. Where standing water can't be eliminated (a low drainage spot, a decorative pond), we use a larvicide that targets the larval stage without harming pets or beneficial insects.",
"Treatment targets two things: the adult mosquitoes resting in shrubs and shaded areas, and the standing water producing the next generation. We treat foliage and moisture-holding areas around the yard on a recurring schedule through the season, since a single visit won't hold against new rainfall. For water sources that can't simply be dumped out -- a rain barrel, a low spot with poor drainage -- we use a targeted larvicide as a second layer of control.",
],
"signs": [
"The obvious sign is getting bitten within minutes of stepping outside, especially at dawn and dusk. Standing water anywhere on the property -- even small amounts in a gutter, saucer, or tarp fold -- is the underlying cause worth checking for, along with visible larvae ('wigglers') if you look closely into any standing water.",
],
"prevention": [
"Empty anything holding water for more than a few days -- plant saucers, buckets, birdbaths, kiddie pools -- at least once a week.",
"Clean gutters regularly; clogged gutters that pool water are one of the most common mosquito breeding sites we find on a property.",
"Store tarps and covers so they don't pool rainwater in the folds; a bunched tarp is a surprisingly common source.",
"Keep grass and shrubs trimmed -- adult mosquitoes rest in shaded, overgrown vegetation during the day.",
"Add or maintain fish in any decorative pond; mosquitofish and many common pond fish eat larvae before they mature.",
"Check for water pooling in tire ruts, low patches of yard, or under AC unit drip lines after it rains.",
"Screen rain barrels with fine mesh if you use one for irrigation, since an open barrel is an ideal breeding site.",
],
"diy_vs_pro": [
"Weekly water dumping and gutter cleaning are genuinely effective DIY steps and worth doing regardless of whether you also treat professionally. Where DIY tends to fall short is barrier treatment coverage and timing -- consumer foggers and sprays knock down what's flying at the moment but don't reach larvae in standing water or resting adults deep in shaded foliage, so the population rebounds within days. A recurring professional treatment schedule timed to the local rain cycle covers both the adult and larval stages, which is the combination that actually holds a yard's population down through the season.",
],
"seasonal_timing": [
"Mosquito season in {city} generally runs from the first sustained warm spell through the first hard frost, though with {climate}, that window can be long. Activity spikes noticeably within about a week of any significant rainfall as new eggs hatch, so treatment scheduled around the local rain pattern -- not just a flat monthly calendar -- tends to hold up better.",
"With {climate}, mosquito pressure in {city} rarely disappears completely for long stretches of the year, even if it dips during the driest or coldest weeks. The practical pattern to plan around is rainfall: expect a population increase roughly a week after any heavy rain, which is when a recurring treatment schedule earns its keep.",
],
"why_choose_us": [
"We treat mosquito control as a season-long program, not a single spray, because that's what actually holds up against {city}'s conditions. Recurring visits are built around your yard's specific water and shade patterns rather than a generic calendar.",
],
"faq": [
("How often do you need to treat for mosquitoes in {city}?", "Most properties here do best on a recurring schedule through the warm months -- typically every 21 to 30 days -- since new eggs keep hatching after rain."),
("Is mosquito treatment safe for pets and kids?", "We use products labeled for residential use and let treated areas dry before pets or kids go back outside, which is a short window on most visits."),
("Can you get rid of mosquitoes completely?", "No treatment eliminates every mosquito that flies in from a neighboring property, but a barrier treatment plus water reduction cuts the population dramatically in the treated yard."),
("What can I do between visits?", "Dump standing water weekly -- gutters, saucers, buckets, tarps -- since that alone removes a big share of local breeding sites."),
("Do you treat for ticks at the same time?", "Many of our mosquito visits can include a tick-focused perimeter treatment on request, since both pests are addressed with a similar yard walk and application approach."),
("Why do I still get bitten right after treatment?", "A barrier treatment knocks down resting adults in vegetation but doesn't affect mosquitoes flying in from untreated areas nearby; the population drop is most noticeable a few days after application, not instantly."),
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
"biology": [
"A single female rat can produce up to six litters a year with six to twelve pups each, and those pups are sexually mature within about five weeks -- which is the math behind how fast a small rat problem becomes a large one if it isn't addressed early. Rats are excellent climbers and can jump surprisingly far both vertically and horizontally, so a gap high on a wall or near a roofline is just as much of a risk as one at ground level. Their teeth grow continuously, which drives near-constant gnawing behavior -- on wood, wiring, plastic, even soft masonry -- not out of hunger but to keep their incisors worn down.",
"Rats are neophobic, meaning they're initially cautious around new objects in their environment, including freshly placed traps or bait stations -- which is why a station left untouched for the first day or two isn't necessarily a sign it's in the wrong spot. They're also creatures of habit once established, reusing the same travel paths along walls and beams night after night, which is why grease marks and droppings cluster along consistent routes rather than spreading randomly. Rats need very little space to enter a structure -- roughly the diameter of a quarter for the common Norway rat -- because their skeletal structure lets them compress their body to fit through gaps that look far too small.",
],
"health_risks": [
"Rats can carry and transmit a number of pathogens through droppings, urine, and bites, including salmonella and, less commonly, hantavirus, which is part of why we recommend against sweeping or vacuuming rodent droppings dry (it can aerosolize particles) in favor of a wet-cleanup approach. Beyond disease, the gnawing behavior is a real property risk -- chewed electrical wiring is a documented cause of house fires, and chewed water lines or gas lines are a less common but more serious risk in an active infestation. A rat population left unchecked also tends to attract secondary pest activity, since food waste and nesting material accumulate along with them.",
"The property damage from rats is often underestimated until it's discovered -- insulation shredded for nesting material, wiring chewed enough to cause an intermittent electrical fault, or a slow leak from a gnawed line that isn't found until a wall or ceiling stain appears. On the health side, droppings and urine buildup in a wall void or attic can affect indoor air quality, especially in enclosed spaces near HVAC returns, and any wet-cleanup of rodent waste should be done with gloves and, ideally, a mask rather than dry sweeping.",
],
"process": [
"We start with an inspection for entry points, droppings, gnaw marks, and grease trails along baseboards or beams, which tell us where rats are traveling. Exclusion work seals gaps with steel wool, hardware cloth, or metal flashing (never anything a rat can chew through), and we place tamper-resistant bait stations or snap traps based on the level of activity. A follow-up visit confirms activity has actually stopped, not just gone quiet for a few days.",
"Because rats reuse the same paths, tracking grease marks and droppings usually leads us straight to the entry point and nest area. We combine sealing that access with traps or bait stations placed along active runs, then follow up to confirm activity has actually stopped -- not just quieted down, which can happen temporarily even with an active population still present elsewhere in the structure.",
],
"signs": [
"Look for droppings (dark, rice-grain sized, often along walls or in cabinets), gnaw marks on wood or wiring, greasy rub marks along baseboards, and scratching sounds in walls or the attic at night. A pet suddenly fixated on a specific wall or cabinet corner is also worth paying attention to.",
],
"prevention": [
"Seal gaps around pipes, vents, and utility lines where they enter the home -- steel wool or hardware cloth, not just caulk, which rats can chew through.",
"Store pet food and birdseed in sealed metal or thick plastic containers rather than the original bag.",
"Trim vegetation and tree limbs away from the house; overgrown shrubs against the foundation give rats cover to approach unseen.",
"Keep outdoor trash in cans with tight-fitting lids, and don't leave bagged garbage out overnight.",
"Address clutter in garages, sheds, and basements -- rats prefer nesting sites with cover, and stacked boxes or stored materials give them exactly that.",
"Fix leaking outdoor faucets or irrigation lines; a reliable water source is as much of a draw as food.",
],
"diy_vs_pro": [
"A single mouse caught in a snap trap doesn't necessarily need a professional call. An established rat infestation is a different scale of problem: finding every entry point on a home's exterior takes a trained eye, store-bought bait often isn't potent enough for a large population, and placing bait or traps in the wrong spots (not along an active travel path) wastes time while the population keeps growing. The exclusion work -- correctly sealing every gap with the right material -- is usually the part that makes the biggest long-term difference and the part most DIY attempts skip or do incompletely.",
],
"seasonal_timing": [
"Rat activity in {city} tends to pick up as outdoor food sources get scarcer, which can happen seasonally, but with {climate}, indoor pressure stays fairly consistent year-round since a warm, dry structure is valuable shelter in any season. We don't see a sharp off-season the way colder climates sometimes do.",
],
"why_choose_us": [
"We don't just drop bait and leave -- we find and seal the entry point, because bait alone doesn't stop new rats from replacing the ones that die off. Our follow-up visit confirms the job actually held.",
],
"faq": [
("How do I know if it's rats or mice in my {city} home?", "Rat droppings are noticeably larger (about the size of a raisin vs. a grain of rice for mice), and rats tend to be louder and bolder in their movement through walls and attics."),
("How long does rat control take to work?", "Exclusion stops new entry immediately; clearing an existing population with traps or bait typically takes one to three weeks depending on how established the nest is."),
("Is rat bait safe around pets?", "We use tamper-resistant, lockable bait stations specifically to keep pets and children away from the bait itself."),
("Can rats really fit through small gaps?", "Yes -- an adult rat can squeeze through an opening about the size of a quarter, because their skeleton lets them compress their body significantly."),
("Why do I still hear noises after the first treatment?", "Established rat populations often take more than one visit to fully clear, especially if there's an active nest with young; a follow-up confirms activity has actually stopped."),
("Do ultrasonic repellers work?", "We don't recommend relying on them -- the evidence for lasting effectiveness is weak, and rats often habituate to the sound within days."),
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
"biology": [
"A German roach egg case (ootheca) holds 30 to 40 eggs, and a female can produce several cases in her lifetime, which is the core reason a small roach sighting can become a full infestation within a couple of months if it isn't treated. Roaches are thigmotactic, meaning they instinctively seek out tight spaces where their body touches surfaces on multiple sides -- cracks, seams, the underside of appliances -- which is exactly why bait placed in open areas is far less effective than bait worked directly into those harborage points. They're mostly nocturnal and photophobic, so seeing roaches in daylight is a specific signal that the hidden population has outgrown the available hiding spots.",
"Roaches can survive for extended periods on very little food and water, which makes starvation-based control (just keeping counters clean) far less effective on its own than most homeowners expect once a population is established. They're also capable of rapid resistance development to certain insecticide classes if the same product is used repeatedly without rotation, which is part of why professional treatment plans typically combine bait, a growth regulator, and, when needed, a different mode of action rather than relying on one product indefinitely.",
],
"health_risks": [
"Roaches are a well-documented asthma and allergy trigger -- their shed skins, droppings, and saliva contain proteins that are a common indoor allergen, particularly relevant for households with children. They also mechanically contaminate food surfaces by walking across them after being in drains, trash, or other unsanitary areas, and are associated with the potential spread of bacteria like salmonella and E. coli, though transmission risk depends heavily on population size and kitchen sanitation. Beyond the health angle, a visible roach problem is one of the fastest ways to lose confidence in a kitchen, which is often the real driving factor behind the call.",
],
"process": [
"We inspect kitchens, bathrooms, and appliance motor compartments (refrigerators, dishwashers) first, since that's where German roaches concentrate. Treatment is targeted gel bait placed in cracks and voids plus a growth regulator to break the egg cycle, rather than a visible perimeter spray that pushes roaches deeper into walls. A follow-up visit two to three weeks later confirms the population is declining, not just hiding better.",
"Because roaches avoid open, treated surfaces, effective control means getting bait into the cracks, hinges, and voids where they actually live. We follow up to confirm the egg cycle has broken, since one visit often isn't enough for an established population -- oothecae that were already laid before treatment will still hatch, so a second visit catches that generation before it can reproduce.",
],
"signs": [
"Signs include a musty odor in cabinets, small dark droppings resembling coffee grounds or pepper, egg cases (oothecae) tucked into cracks, and roaches spotted in daylight -- a sign the hidden population is significant. Smear marks (brown streaks) along baseboards or cabinet edges are another indicator, left behind as roaches travel the same paths repeatedly.",
],
"prevention": [
"Fix leaking pipes and faucets promptly -- roaches need very little water to survive, and a small consistent leak can sustain a population on its own.",
"Store food, including pet food, in sealed containers rather than the original packaging.",
"Take trash out regularly and use a can with a tight-fitting lid, especially in the kitchen.",
"Clean behind and under large appliances periodically -- refrigerators, stoves, and dishwashers trap crumbs and moisture that roaches rely on.",
"Seal cracks around baseboards, cabinets, and where pipes enter walls with caulk to reduce available harborage.",
"Check secondhand appliances and furniture carefully before bringing them inside; roaches (and their egg cases) travel this way more often than people expect.",
],
"diy_vs_pro": [
"Good sanitation -- fixing leaks, sealing food, regular trash removal -- is genuinely effective at slowing a roach population and worth doing regardless. Store-bought sprays, though, often scatter roaches deeper into wall voids rather than eliminating the colony, and a single missed harborage point (behind a fridge motor, inside a cabinet hinge) is enough to let the population rebound. Professional gel bait placement targets those hidden spots specifically, and a growth-regulator component addresses the egg cases that sprays don't reach at all.",
],
"seasonal_timing": [
"German roach populations in {city} are largely indoor and climate-controlled, so unlike outdoor pests, they don't have a strong seasonal on/off pattern -- {climate} means moisture and warmth are available indoors essentially year-round once a population is established. That said, roach activity outdoors (and the odds of one hitching a ride inside) does tend to rise during the warmest, most humid stretches of the year.",
],
"why_choose_us": [
"Roach control is about precision, not volume -- we place bait exactly where roaches travel and breed, which gets faster, more lasting results than a broad spray, plus a follow-up visit to confirm the egg cycle actually broke.",
],
"faq": [
("Why do I still see roaches after spraying myself?", "Store-bought sprays often push roaches deeper into wall voids instead of eliminating the colony; gel bait placed directly in cracks and harborage areas is far more effective."),
("How long does roach treatment take to work?", "Most {city} homes see a significant drop within one to two weeks as roaches feed on bait and carry it back to the colony; a follow-up visit confirms the egg cycle is broken."),
("Are roaches a health concern, not just gross?", "Yes -- roaches can trigger asthma and allergies and contaminate food surfaces, which is part of why we treat infestations as more than a cosmetic issue."),
("Do I need to throw everything out of my cabinets?", "Usually not -- we can treat around stored food and dishes; we'll tell you specifically what to clear if a particular area needs it."),
("Why do I need a follow-up visit?", "Egg cases already laid before treatment will still hatch afterward; the second visit catches that generation before it can reproduce and re-establish the population."),
("Can roaches come back from a neighboring unit?", "In multi-unit buildings, yes -- shared walls and plumbing chases give roaches a path between units, which is why we sometimes recommend coordinating treatment with neighbors in that situation."),
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
"biology": [
"A bed bug can survive for several months without feeding under favorable conditions, which is part of why an empty house or unused guest room doesn't guarantee an infestation has died out on its own. They're attracted primarily by the carbon dioxide and body heat we give off while sleeping, not visible dirt or clutter, which is why bed bugs show up in immaculate homes as readily as anywhere else. A single mated female can lay one to five eggs a day and hundreds over her lifetime, and the eggs are coated in a substance that makes them resistant to many surface-level treatments, which is a major reason a single spray application rarely finishes the job.",
"Bed bugs are flat and can wedge into spaces as thin as a credit card -- mattress seams, headboard joints, baseboard gaps, even behind wallpaper -- which is why a visual inspection has to go well beyond just checking the mattress surface. They don't fly or jump, but they're effective hitchhikers, moving between rooms and buildings via luggage, used furniture, and clothing rather than spreading on their own across long distances. Nymphs (young bed bugs) look like smaller, paler versions of adults and molt through five stages before maturity, needing a blood meal between each molt, which is part of why an active infestation includes bugs at very different visible sizes.",
],
"health_risks": [
"Bed bug bites themselves are generally not known to transmit disease, but they can cause significant itching, welts, and secondary skin infection from scratching, and the psychological toll -- disrupted sleep, anxiety about the home -- is often the more significant impact we see reported. Some people have little to no visible reaction to bites at all, which can delay an infestation being noticed until it's already well established. Because bed bugs travel via belongings, an untreated infestation also carries a real risk of spreading to other rooms, other units in a multi-family building, or a workplace via clothing and bags.",
],
"process": [
"We start with a room-by-room inspection using a flashlight and inspection tools to check mattress seams, box springs, bed frames, baseboards, and nearby furniture -- bed bugs hide within a few feet of where people sleep. Depending on the level of infestation, we use targeted heat treatment (which kills bugs and eggs in a single pass) or a combination of residual and contact insecticide applied directly into cracks and seams, followed by a check 10-14 days later.",
"Because bed bugs and their eggs hide in tight seams and voids, inspection has to be thorough before treatment starts. We treat mattress and furniture seams, baseboards, outlet covers, and any adjoining rooms with activity, then schedule a follow-up to confirm the population is gone -- since any eggs that survive the first treatment will hatch within roughly a week to ten days.",
],
"signs": [
"Look for small rust-colored spots on sheets (crushed bugs or fecal spots), tiny pale eggshells in mattress seams, a sweet musty odor in heavy infestations, and bites that appear in a line or cluster after sleeping. Shed skins from molting nymphs, which look like tiny translucent husks, are another reliable sign when found in seams or crevices.",
],
"prevention": [
"Inspect secondhand furniture, especially mattresses and upholstered pieces, carefully before bringing them into the home.",
"When traveling, check hotel mattress seams and headboards, and keep luggage off the bed and floor when possible.",
"Wash and dry travel clothing on high heat as soon as you get home, even if you don't suspect exposure.",
"Use a protective mattress and box spring encasement, which makes it much easier to spot an early infestation before it spreads.",
"Reduce clutter near the bed -- fewer hiding spots make an early infestation easier to catch and treat before it establishes.",
"If you live in a multi-unit building and suspect an infestation, notify management promptly; shared walls and hallways can let bed bugs spread between units.",
],
"diy_vs_pro": [
"Encasements, laundering, and vigilant inspection after travel are genuinely useful DIY prevention. Actually treating an active infestation without professional equipment is very difficult: over-the-counter sprays rarely penetrate deep enough into seams and voids to reach every life stage, bed bug eggs are resistant to many surface treatments, and a botched DIY attempt often just scatters the population into adjoining rooms, turning a contained problem into a spread-out one. Heat treatment in particular requires equipment most homeowners don't have access to.",
],
"seasonal_timing": [
"Bed bugs live entirely indoors and don't depend on outdoor temperature, so unlike most pests on this site, there's no real seasonal pattern to bed bug calls in {city} -- we see them at a fairly steady rate throughout the year, with a modest uptick tied to travel-heavy periods like summer and the holidays rather than the weather itself.",
],
"why_choose_us": [
"Bed bugs require thorough, methodical treatment -- cutting corners here just means they come back in a few weeks. We inspect and treat every adjoining space where they could be hiding, not just the bed itself, and follow up to confirm the job held.",
],
"faq": [
("How do I know if it's bed bugs and not another bug?", "Rust-colored spots on sheets, small pale eggshells in mattress seams, and bites appearing in a line are the clearest signs; we can confirm with an in-person inspection."),
("Does heat treatment really kill bed bugs and eggs?", "Yes -- raising a room to the right sustained temperature kills bed bugs at every life stage, including eggs, which chemical treatment alone can struggle with."),
("Do I need to throw away my mattress?", "Usually not -- a properly treated mattress (often with an encasement afterward) can be kept; replacement is rarely necessary."),
("How many visits does bed bug treatment take?", "Most {city} cases need an initial treatment plus a follow-up 10 to 14 days later to catch any bugs that hatched after the first visit."),
("Can bed bugs spread to other rooms during treatment?", "It's possible if items are moved carelessly during an active infestation, which is why we treat adjoining rooms with any sign of activity rather than isolating treatment to one room."),
("Will I need to throw out furniture?", "Rarely -- most furniture can be treated and kept. Heavily infested items with structural damage are the main exception."),
],
},
}

# ---------------------------------------------------------------------------
# Stub-tier: short, varied blurbs (2-3 sentences) per service. Only used when
# FULL_TIER_COUNT < TOTAL_CITIES (the default build gives every city full
# treatment, so this bank is inactive but kept for that extensibility path).
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

# ---------------------------------------------------------------------------
# City hub page content: generic (not service-specific) blocks used once per
# city hub, on top of the per-service overview paragraphs pulled from
# SERVICE_CONTENT above.
# ---------------------------------------------------------------------------

HUB_WHY_US = [
"We're a locally-run crew, not a national call center -- every technician who works in {city} also handles the inspection, the treatment, and the follow-up, so nothing gets lost between whoever answers the phone and whoever shows up at the door. Pricing is quoted after a real inspection, not guessed over the phone, and every exclusion or treatment we do is built to hold, not just to pass a quick visual check.",
"Homeowners in {city} call us because we treat the cause, not just the symptom -- an entry point stays sealed, a bait placement stays in the spot that's actually working, and a follow-up visit happens when the job calls for one, not as an upsell. We work {county} regularly enough to know the building stock, which speeds up every inspection we run here.",
"What sets us apart in {city} is follow-through: we don't consider a wildlife or pest job finished until the entry point is sealed or the population is confirmed gone, not just quieter for a few days. That standard applies across all six services we run here, from a one-time raccoon exclusion to a recurring mosquito treatment program.",
]

HUB_FAQ = [
("Do you serve all of {city}, {state_abbr}, not just certain neighborhoods?", "Yes -- we cover all of {city} and the surrounding {county_label}, including the nearby areas listed on this page."),
("Do you charge for an inspection?", "Inspection and quote policies vary by job type and season; call {phone} and we'll give you a straight answer for your specific situation before anything is scheduled."),
("How quickly can someone come out to {city}?", "Most non-emergency calls in {city} are scheduled within a day or two; active wildlife denning or a heavy bed bug or roach infestation is usually prioritized for a faster visit."),
("Are your technicians licensed and insured?", "Yes -- licensing requirements vary by state and service type, and we operate within those requirements for every job we take in {state_name}."),
]

def hub_prevention_bullets(service_content, ctx, seed_prefix):
    """One deterministic prevention tip per service, for the city hub page."""
    out = []
    for slug, bank in service_content.items():
        tip = pick(f"{seed_prefix}|{slug}|hubprev", bank["prevention"]).format(**ctx)
        out.append((slug, tip))
    return out
