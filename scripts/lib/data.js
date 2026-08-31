'use strict';

const PHONE_RAW = '+18339013895';
const PHONE_DISPLAY = '(833) 901-3895';

const STATE_INFO = {
  tx: { name: 'Texas', region: 'Texas', climate: 'hot summers and mild winters that keep raccoons active nearly year-round' },
  fl: { name: 'Florida', region: 'Florida', climate: 'warm, humid conditions that give raccoons easy access to attics and crawl spaces all year' },
  md: { name: 'Maryland', region: 'the Mid-Atlantic', climate: 'four distinct seasons that push raccoons to seek shelter indoors every fall' },
  de: { name: 'Delaware', region: 'the Mid-Atlantic', climate: 'coastal humidity and cold snaps that send wildlife looking for warm attics' },
  va: { name: 'Virginia', region: 'the Mid-Atlantic', climate: 'wooded neighborhoods that back right up to prime raccoon habitat' },
  or: { name: 'Oregon', region: 'the Pacific Northwest', climate: 'wet winters that drive raccoons toward dry, sheltered rooflines' },
  oh: { name: 'Ohio', region: 'the Midwest', climate: 'cold winters that make attics and chimneys prime real estate for denning raccoons' },
  nv: { name: 'Nevada', region: 'the Southwest', climate: 'desert heat that pushes raccoons toward shaded attics and irrigated yards' },
  wy: { name: 'Wyoming', region: 'the Mountain West', climate: 'harsh winters that make insulated attics irresistible to local wildlife' },
  al: { name: 'Alabama', region: 'the Deep South', climate: 'long warm seasons that keep raccoon activity high most of the year' },
  ny: { name: 'New York', region: 'the Northeast', climate: 'cold winters that push raccoons to den up in attics, chimneys and garages' },
};

const WORD_FIX = {
  st: 'St.',
  ft: 'Fort',
  georges: "George's",
  deleware: 'Delaware',
};

const STOPWORDS = new Set(['raccoon', 'removal', 'in', 'attic', 'humane', 'emergency', 'service', 'near', 'me']);

function titleCaseWord(w) {
  if (WORD_FIX[w]) return WORD_FIX[w];
  if (w.length <= 3 && w === w.toLowerCase() && /^[a-z]+$/.test(w) === false) return w;
  return w.charAt(0).toUpperCase() + w.slice(1);
}

module.exports = { PHONE_RAW, PHONE_DISPLAY, STATE_INFO, WORD_FIX, STOPWORDS, titleCaseWord };
