const fs = require('fs');

const path = process.argv[2];
let text = fs.readFileSync(path, 'utf8');
const lines = text.split('\r\n');

const zh = {
  LOADING: '加载中，请稍候...',
  SAVING: '保存中，请稍候...',
  EXIT: '退出',
  START_NEW_GAME: '开始新游戏',
  CONTINUE_GAME: '继续游戏',
  CANCEL: '取消',
};

let changed = 0;
const out = lines.map((line) => {
  if (!line.trim()) return line;
  const cols = line.split('\t');
  if (zh[cols[0]] !== undefined) {
    cols[3] = zh[cols[0]];
    changed++;
    return cols.join('\t');
  }
  return line;
});

fs.writeFileSync(path, out.join('\r\n'), 'utf8');
console.log(`updated ${changed} tags`);
