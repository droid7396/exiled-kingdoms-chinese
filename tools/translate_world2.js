const fs = require('fs');
const ev = {
  'near the river, east of the area':'在区域东部，靠近河边',
  'by the hills to the west':'在西侧丘陵旁',
  'northeast of the area, into the mountains':'在区域东北，深入群山',
  'north of the area':'在区域北部',
  'to the southeast':'在东南方',
  'in the south foothills':'在南部山麓',
  'deep into the forest':'在森林深处',
  'to the northeast':'在东北方',
  'to the southwest':'在西南方',
  'to the west, near the hills':'在西方，靠近丘陵',
  'in the middle of the area':'在区域中央',
  'to the west near the hills':'在西侧丘陵旁',
  'near the middle of the hills area':'在丘陵地带中部附近',
  'by the mountain pass in the southwest':'在西南方的山口旁',
  'to the northwest':'在西北方',
  'in a secret chamber':'在一间密室里',
  'in the the shrine':'在神龛里',
  'in the shrine':'在神龛里',
  'in one of the eastern cells':'在东侧的一间牢房里',
  'to the north':'在北方',
};
const rumors = [
  '据说有个叫格里森达的年轻女战士立誓要找回一件传家宝物。最后一次有人见到她，是在北蓝雾河探索一处废墟。',
  '瓦西利亚是个富庶的王国，但路上不太平。有传闻说，王桥镇附近有强盗绑走了一个女人，拖进了山洞。',
  '多年前，新加兰德的一位寻知者只身进入枯木林，从此再无人见过她。',
  '有些怪物，比如亡灵，在夜里会强大得多。',
  '梅尔西亚存在奴隶贸易，这让其他王国颇为不安。不过他们不奴役"文明人"，只奴役瓦兰纳里野人或罪犯。',
  '一群瓦兰纳里猎人如今在萨加尔森林南扎营。他们可能有危险，不过通常各过各的，有时还能跟他们做点买卖。',
  '据说贾巴尔有个宝石商人收购绿宝石的价钱比平常高得多。也许他是个法师，拿它们当炼金材料？',
  '哥布林看起来瘦小羸弱，但他们一拥而上就很可怕。而且据说深山里的哥布林更大更强，当心！',
  '好消息听说了吗？有位英雄杀进兰尼加矿洞，打垮了哥布林，连他们的火焰舞者头目也不例外。矿洞重新开放啦！',
  '新加兰德的街头游荡着一个怪人……他块头巨大，脸孔扭曲，似乎疯了。卫兵应该把他关起来。',
  '据说远古时代哥布林崇拜火龙和红龙。有人甚至相信这样的生物至今仍藏在兰尼加北边的戈克斯巢穴深处。',
  '"弗加斯来的旅人说，有一只裹着魔法火焰的疯狂蜜尔梅克，把伊罗斯高地的森林夷为平地，然后躲进了那里的某个山洞。"',
  '巨魔是狰狞的野兽，非常难杀。想让他们停止再生，唯一的办法是用火烧。',
  '几天前的夜里，新加兰德好不热闹。巡夜人追捕几个飞贼，却让他们跑了。许多人说他们钻进了下水道。',
  '据说新加兰德有些走私犯不买第七之家的账，敢绕开他们的控制。他们大概是疯了，虽然多半躲 在城外。',
  '一个弗里古德巡回剧团正在新安瑟演出。他们的台柱雷欧提斯是观众的宠儿。',
  '三神教会派出一支圣战士远征队，讨伐大伊诺里的亡灵，领队是一位名叫赫尔嘉的年轻女祭司。',
  '尼瓦里安最出色的药剂师之一，"火酿"马洛，最近歇业了。据说他想重振生意，正寻找帮他收集药材的冒险者。',
  '一伙冒险者屠龙之后捡到一块奇怪的黑色碎片。他们把它高价卖给了弗里古德总督，如今就锁在金湾银行的金库里。',
  '冰雾镇有点不对劲。奥术队长托登失踪了，还有传闻说每晚都有人失踪。',
  '自由镇大竞技场开门了！他们正在招募渴望成名发财的角斗士。',
];
const castles = {
  'Lannegar Town Hall':'兰尼加市政厅','Kingsbridge Town Hall':'王桥镇市政厅','Rhöneis Town Hall':'罗内斯市政厅','Jabal Town Hall':'贾巴尔市政厅','New Garand Town Hall':'新加兰德市政厅','Sydarun Town Hall':'西达伦市政厅','Freetown Town Hall':'自由镇市政厅','New Anthur Town Hall':'新安瑟市政厅','Nivarian Town Hall':'尼瓦里安市政厅','Fögas Town Hall':'弗加斯市政厅','Whitetower Town Hall':'白塔镇市政厅','Icemist Town Hall':'冰雾镇市政厅','Port Malan Town Hall':'马兰港市政厅','Solliga Town Hall':'索利加市政厅',
};

function fillByEN(path, enCol, ruCol, map) {
  let text = fs.readFileSync(path, 'utf8').replace(/^\uFEFF/, '');
  const lines = text.split(/\r?\n/);
  let changed = 0, missed = 0;
  const out = lines.map((line, idx) => {
    if (idx === 0 || !line.trim()) return line;
    const cols = line.split('\t');
    const zh = map[(cols[enCol] || '').trim()];
    if (zh !== undefined && zh !== '') { cols[ruCol] = zh; changed++; return cols.join('\t'); }
    if ((cols[enCol] || '').trim() !== '') missed++;
    return line;
  });
  fs.writeFileSync(path, out.join('\r\n'), 'utf8');
  console.log(path.split('/').pop(), 'changed:', changed, 'missed:', missed);
}

function fillRumors(path, enCol, ruCol, arr) {
  let text = fs.readFileSync(path, 'utf8').replace(/^\uFEFF/, '');
  const lines = text.split(/\r?\n/);
  let changed = 0;
  const out = lines.map((line, idx) => {
    if (idx === 0 || !line.trim()) return line;
    const cols = line.split('\t');
    const zh = arr[idx - 1];
    if (zh) { cols[ruCol] = zh; changed++; return cols.join('\t'); }
    return line;
  });
  fs.writeFileSync(path, out.join('\r\n'), 'utf8');
  console.log('rumors.txt changed:', changed);
}

const base = process.argv[2];
fillByEN(base + '/event_locations.txt', 1, 3, ev);
fillRumors(base + '/rumors.txt', 0, 5, rumors);
fillByEN(base + '/castles.txt', 5, 7, castles);
