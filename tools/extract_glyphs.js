const fs = require('fs');
const path = require('path');

const fontsDir = process.argv[2];
const outChars = process.argv[3];
const outSizes = process.argv[4];

const names = ['default','tahoma16white','tahoma20bold','tahoma20white','tahoma22bold','tahoma22outline','tahoma23white','tahoma24bold','tahoma25white','tahoma26bold','tahoma27bold','tahoma27outline','tahoma27white','tahoma31outline','tahoma32','tahoma32bold','tahoma38outline','arialnarrow40bold'];

const ids = new Set();
const sizes = {};
for (const n of names) {
  const text = fs.readFileSync(path.join(fontsDir, n + '.fnt'), 'utf8');
  const sizeM = text.match(/^info [^\n]*size=(-?\d+)/m);
  sizes[n] = sizeM ? Math.abs(parseInt(sizeM[1])) : null;
  for (const m of text.matchAll(/^char id=(\d+)/gm)) ids.add(parseInt(m[1]));
}

// exclude control chars 0-31 and 127 (id 10 newline etc. have no glyph), keep 32-126 explicit
const sorted = [...ids].filter(i => i >= 32).sort((a, b) => a - b);
const charsParam = sorted.join(',');

fs.writeFileSync(outChars, charsParam);
fs.writeFileSync(outSizes, JSON.stringify(sizes, null, 2));
console.log('unique ids:', sorted.length);
console.log('sizes:', JSON.stringify(sizes));
