'use strict';
const fs = require('fs');
const path = require('path');
const { STATE_INFO, STOPWORDS, titleCaseWord } = require('./lib/data');

const rawPath = path.join(__dirname, '..', 'data', 'keywords_raw.csv');
const lines = fs.readFileSync(rawPath, 'utf8').trim().split('\n').slice(1);

const rows = lines.map((line) => {
  const idx = line.indexOf(',');
  const id = parseInt(line.slice(0, idx), 10);
  const keyword = line.slice(idx + 1).trim();
  return { id, keyword };
});

function normalizeBag(keyword) {
  const words = keyword.toLowerCase().split(/\s+/);
  return words.slice().sort().join(' ');
}

const seenBags = new Map(); // bag -> record
const records = [];

for (const row of rows) {
  const bag = normalizeBag(row.keyword);
  if (seenBags.has(bag)) {
    seenBags.get(bag).mergedIds.push(row.id);
    seenBags.get(bag).mergedKeywords.push(row.keyword);
    continue;
  }
  const words = row.keyword.toLowerCase().split(/\s+/);
  let stateAbbr = null;
  for (const w of words) {
    if (STATE_INFO[w]) stateAbbr = w;
  }

  const localityWords = [];
  let isCounty = false;
  let isNearMe = false;
  let isEmergency = false;
  let isHumane = false;
  let isAttic = false;
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    if (w === 'county') { isCounty = true; localityWords.push('county'); continue; }
    if (w === 'near' || w === 'me') { isNearMe = true; continue; }
    if (w === 'emergency') { isEmergency = true; continue; }
    if (w === 'humane') { isHumane = true; continue; }
    if (w === 'attic') { isAttic = true; continue; }
    if (stateAbbr && w === stateAbbr) continue;
    if (STOPWORDS.has(w)) continue;
    localityWords.push(w);
  }
  const localityDisplay = localityWords.map(titleCaseWord).join(' ');

  const record = {
    id: row.id,
    keyword: row.keyword,
    slugWords: words.filter((w) => true),
    localityWords,
    localityDisplay,
    stateAbbr,
    stateInfo: stateAbbr ? STATE_INFO[stateAbbr] : null,
    isCounty,
    isNearMe,
    isEmergency,
    isHumane,
    isAttic,
    mergedIds: [row.id],
    mergedKeywords: [row.keyword],
  };
  seenBags.set(bag, record);
  records.push(record);
}

// slug generation, preserving original word order for readability, ensuring global-ish uniqueness
const usedSlugs = new Set();
for (const r of records) {
  let base = r.slugWords.join('').replace(/[^a-z0-9]/g, '');
  let slug = base;
  let n = 2;
  while (usedSlugs.has(slug)) {
    slug = `${base}${n}`;
    n++;
  }
  usedSlugs.add(slug);
  r.slug = slug;
}

fs.writeFileSync(
  path.join(__dirname, '..', 'data', 'sites.json'),
  JSON.stringify(records, null, 2)
);

console.log(`Total rows: ${rows.length}`);
console.log(`Unique sites after dedupe: ${records.length}`);
console.log(`Merged/duplicate rows collapsed: ${rows.length - records.length}`);
