const fs = require('fs');
const path = require('path');

const DATA = 'C:/Users/dt7396/AppData/Local/Temp/ek/full/data';
const OUT = 'C:/Games/Exiled Kingdoms-build11985424/_zh/docs';
fs.mkdirSync(OUT, { recursive: true });

const readLines = (p) => fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/).filter(l => l.trim());
const cells = (line) => line.split('\t');

// ---------- structured sources: [file, nameCol, descCol] ----------
const termFreq = new Map();
const bump = (phrase) => {
  phrase = phrase.trim();
  if (phrase.length < 3) return;
  termFreq.set(phrase, (termFreq.get(phrase) || 0) + 1);
};

// extract Capitalized word sequences (potential proper nouns) from English text
const extractTerms = (text) => {
  if (!text) return;
  const clean = text.replace(/\[[^\]]*\]/g, ' ').replace(/<[^>]*>/g, ' ');
  for (const m of clean.matchAll(/\b([A-Z][a-zA-ZäöüßÄÖÜéèêáíóúñçö']*(?:\s+[A-Z][a-zA-ZäöüßÄÖÜéèêáíóúñçö']*){0,3})\b/g)) {
    bump(m[1]);
  }
};

const pools = {};

// conversations: col3 = english text
pools.conversations = [];
const convDir = path.join(DATA, 'conversations');
for (const f of fs.readdirSync(convDir).filter(f => f.endsWith('.txt')).sort()) {
  const lines = readLines(path.join(convDir, f));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[2] && c[2].trim()) {
      pools.conversations.push({ file: f.replace('.txt',''), line: i, text: c[2].trim() });
      extractTerms(c[2]);
    }
  }
}

// quests: col2 = description (progress stages); first non-numeric-progress row = title
pools.quests = [];
const qDir = path.join(DATA, 'quests');
const questFiles = fs.readdirSync(qDir).filter(f => f.endsWith('.txt') && f !== 'list.txt').sort();
for (const f of questFiles) {
  const lines = readLines(path.join(qDir, f));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[1] && c[1].trim()) {
      pools.quests.push({ file: f.replace('.txt',''), line: i, progress: c[0], text: c[1].trim() });
      extractTerms(c[1]);
    }
  }
}

// items_text: name=col2, desc=col3
pools.items = [];
{
  const lines = readLines(path.join(DATA, 'rules/items_text.txt'));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if ((c[1] && c[1].trim()) || (c[2] && c[2].trim())) {
      pools.items.push({ id: c[0], name: (c[1]||'').trim(), desc: (c[2]||'').trim() });
      extractTerms(c[1]); extractTerms(c[2]);
    }
  }
}

// bestiary_names: col2 name
pools.bestiary = [];
{
  const lines = readLines(path.join(DATA, 'rules/bestiary_names.txt'));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[1] && c[1].trim()) { pools.bestiary.push({ id: c[0], name: c[1].trim() }); extractTerms(c[1]); }
  }
}

// factions_text: name=col2, desc=col3
pools.factions = [];
{
  const lines = readLines(path.join(DATA, 'world/factions_text.txt'));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[1] || c[2]) { pools.factions.push({ id: c[0], name: (c[1]||'').trim(), desc: (c[2]||'').trim() }); extractTerms(c[2]); }
  }
}

// regions / areas names
pools.world_names = [];
{
  for (const [file, nameCol, idCol] of [['world/regions.txt', 1, 0], ['world/areas.txt', 5, 0]]) {
    const lines = readLines(path.join(DATA, file));
    for (let i = 1; i < lines.length; i++) {
      const c = cells(lines[i]);
      if (c[nameCol] && c[nameCol].trim()) { pools.world_names.push({ src: file, id: c[idCol], name: c[nameCol].trim() }); extractTerms(c[nameCol]); }
    }
  }
}

// castles (name col6) + castles_desc (desc col2)
pools.castles = [];
{
  const lines = readLines(path.join(DATA, 'world/castles.txt'));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[5] && c[5].trim()) { pools.castles.push({ id: c[0], name: c[5].trim() }); extractTerms(c[5]); }
  }
  const dlines = readLines(path.join(DATA, 'world/castles_desc.txt'));
  for (let i = 1; i < dlines.length; i++) {
    const c = cells(dlines[i]);
    if (c[1] && c[1].trim()) { pools.castles.push({ id: 'desc_' + c[0], desc: c[1].trim() }); extractTerms(c[1]); }
  }
}

// npc display names: names.txt/names2.txt col2
pools.npc_names = [];
for (const nf of ['ui/strings/names.txt', 'ui/strings/names2.txt']) {
  const lines = readLines(path.join(DATA, nf));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[1] && c[1].trim()) { pools.npc_names.push({ tag: c[0].trim(), name: c[1].trim(), src: nf }); extractTerms(c[1]); }
  }
}

// skills (name col1, desc col6; level rows are blank-name bonus rows)
pools.skills = [];
{
  for (const sf of ['rules/skills.txt','rules/skills2.txt','rules/skills3.txt','rules/skills_advanced.txt','rules/skills_advanced2.txt','rules/skills_advanced3.txt']) {
    const lines = readLines(path.join(DATA, sf));
    for (let i = 1; i < lines.length; i++) {
      const c = cells(lines[i]);
      if (c[0] && c[0].trim()) { pools.skills.push({ src: sf, line: i+1, name: c[0].trim(), desc: (c[5]||'').trim() }); extractTerms(c[5]); }
      else if (c[5] && c[5].trim()) { pools.skills.push({ src: sf, line: i+1, name: '', desc: c[5].trim() }); }
    }
  }
}

// rumors (col1 RU-col etc; english col0)
pools.rumors = [];
{
  const lines = readLines(path.join(DATA, 'world/rumors.txt'));
  for (let i = 1; i < lines.length; i++) {
    const c = cells(lines[i]);
    if (c[0] && c[0].trim()) { pools.rumors.push({ line: i+1, text: c[0].trim() }); extractTerms(c[0]); }
  }
}

// write pools
for (const [k, v] of Object.entries(pools)) {
  fs.writeFileSync(path.join(OUT, `pool_${k}.json`), JSON.stringify(v, null, 1));
}

// term frequency table
const terms = [...termFreq.entries()].filter(([t, n]) => n >= 3 && /[A-Z]/.test(t[0]))
  .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
fs.writeFileSync(path.join(OUT, 'terms_freq.txt'), terms.map(([t, n]) => `${n}\t${t}`).join('\n'));

const stats = Object.fromEntries(Object.entries(pools).map(([k, v]) => [k, v.length]));
console.log(JSON.stringify(stats, null, 1));
console.log('term candidates (freq>=3):', terms.length);
