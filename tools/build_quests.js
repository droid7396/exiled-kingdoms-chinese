const fs = require('fs');
const path = require('path');

// usage: node build_quests.js <translations.json> [srcDir] [outDir]
// translations.json: { "questfile": { "lineNo": "chinese" } }  (lineNo = physical row, header row 1 skipped/always "translation")
const SRC = process.argv[3] || 'C:/Users/dt7396/AppData/Local/Temp/ek/full/data/quests';
const OUT = process.argv[4] || 'C:/Games/Exiled Kingdoms-build11985424/_zh/data/quests/RU';
const trans = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

fs.mkdirSync(OUT, { recursive: true });

let files = 0, lines = 0, warnings = [];
for (const [name, map] of Object.entries(trans)) {
  const srcPath = path.join(SRC, name + '.txt');
  if (!fs.existsSync(srcPath)) { warnings.push(`MISSING SOURCE: ${name}`); continue; }
  const src = fs.readFileSync(srcPath, 'utf8').replace(/^\uFEFF/, '');
  const srcLines = src.split(/\r?\n/);
  if (srcLines[srcLines.length - 1] === '') srcLines.pop();

  const outLines = ['translation'];
  for (let i = 1; i < srcLines.length; i++) {
    const cols = srcLines[i].split('\t');
    const en = (cols[1] || '').trim();
    if (!en) { outLines.push(''); continue; } // structural line: keep empty
    const zh = map[i + 1];
    if (zh === undefined) { warnings.push(`${name}:${i + 1} UNTRANSLATED, keeping empty`); outLines.push(''); continue; }
    if (zh.includes('\t')) { warnings.push(`${name}:${i} TAB IN TRANSLATION`); }
    if (zh.trim() === '') { outLines.push(''); continue; }
    outLines.push(zh.replace(/\r?\n/g, ' '));
    lines++;
  }
  let content = outLines.join('\r\n') + '\r\n';
  const buf = Buffer.concat([Buffer.from([0xFF, 0xFE]), Buffer.from(content, 'utf16le')]);
  fs.writeFileSync(path.join(OUT, name + '.txt'), buf);
  files++;
}

console.log(`generated ${files} files, ${lines} translated lines`);
if (warnings.length) { console.log('WARNINGS:'); warnings.slice(0, 30).forEach(w => console.log(' ', w)); }
