const fs = require('fs');
const zhAreas = {
E9:"南贾巴尔丘陵",E10:"北贾巴尔丘陵",F8:"西达伦绿洲",F9:"枯木林",F10:"罗内斯平原",G8:"北伊诺里",G9:"王桥镇",G10:"北蓝雾河",H8:"新加兰德农田",H9:"南蓝雾河",H10:"兰尼加谷地",H11:"萨加尔森林西北",I8:"帝国海岸",I9:"斯托姆山",I10:"萨加尔森林南",I11:"萨加尔森林北",NG:"新加兰德",FT:"自由镇",NI:"尼瓦里安",G11:"绯红丘陵",D10:"涅哈尔谷",D9:"铁谷",D8:"扎莫尔山脉",E8:"巨魔沼泽",I12:"双足飞龙山脉",J11:"飞龙尾谷",J10:"新安瑟湾",J9:"钢铁海岸",J8:"尼洛马尔角",G7:"大伊诺里",D11:"弗加斯森林",E11:"大平原",F11:"尼瓦尔湿地",E12:"瑟尔山脊",D12:"伊罗斯高地",H7:"东伊诺里",H6:"金湾",G6:"翡翠谷",H5:"巨龙海岸",H4:"南方龙脊山脉",H3:"灰烬荒原",I3:"灰烬岬",I13:"冰雾峡湾",H13:"白原",G13:"深霜冰川",H12:"白塔谷",IM:"冰雾镇",D13:"圣所峰",C13:"奥罗格山",J7:"西科恩",K7:"东科恩",K11:"索利加地带",J12:"东部双足飞龙山脉",F6:"沉默君王峡谷",C10:"瓦兰林地",C11:"长老森林",C12:"边野女巫团",
H10_mine:"兰尼加矿洞",G11_tower:"废弃高塔",D11_abbey:"圣阿德穆斯修道院",D8_castle:"蓝岩城堡",E12_cave:"回声洞窟",E10_tower:"特雷马丹之塔",G10_cave:"深掘洞窟",D11_abbey_cave:"地狱洞窟",FT_seventh:"第七之家",F11_tomb:"阿扎古尔之墓",D12_cave:"拉姆巴洞窟",G7_tomb:"伊拉祖尔之墓",NG_sewers:"新加兰德下水道",D9_crypt:"梅尔西亚皇家墓穴",F9_mausoleum:"陵墓",E11_tower:"大平原飞地",I12_cave:"夏尔达洞窟",NG_temple:"新加兰德神殿",G10_tomb:"克莱尤之墓",E10_maze_1:"兰斯迷宫",E10_maze_2:"兰斯迷宫二层",FT_library:"灰图书馆",NG_loreseekers:"大图书馆",FT_warriors:"战士公会",J8_cave:"血爪洞窟",D8_cave1:"尼洛斯洞窟",F8_cave:"深沙洞窟",H8_tomb:"纳亚乌之墓",H11_cave_1:"戈克斯巢穴",J9_castle:"帝国要塞",J10_island:"小孤岛",J9_cave:"阿斯卡提矿洞",I12_cauldron:"深渊大锅",J11_tower:"飞龙尾建筑群",E9_cave:"贾巴尔岩窟",H10_tomb:"伊达亚之墓",G9_cave:"强盗藏身处",F10_cave:"罗纳塔洞窟",NG_house:"新加兰德宅邸",H9_lair:"乌尔祖加纳尔巢穴",NG_castle:"王堡庭院",I10_tutorial:"林间道路",NG_dungeon:"未知地牢",NG_warriors:"战士公会",I11_cave:"梅尔达克斯洞窟",E10_cave_fire:"火焰坑",E8_cave:"古尔古斯洞窟",D9_tower:"铁之飞地",NG_house_1:"施泰因茨法官宅",I10_tower:"萨加尔飞地",G8_tower:"伊诺里飞地",G8_hideout:"废弃走私者藏窝",NI_hall:"智慧圣殿",NI_warriors:"战士公会",H7_temple:"遗忘神殿",H6_bank:"金湾银行",H6_manor:"总督官邸",NI_house:"尼瓦里安宅邸",H4_cave:"巴帕萨拉洞窟",H3_cave:"沉没城堡",I3_ark:"洛塔桑方舟",I3_ark2:"洛塔桑方舟·上甲板",I3_ark3:"洛塔桑方舟·反应堆",E10_cave_ice:"冰封深处",IM_sewer:"恐怖下水道",G13_tomb:"被亵渎的遗迹",IM_manor:"灰符庄园",IM_underlevel:"冰雾地下层",IM_planeoffire:"火元素位面",H4_test:"测试区域",I9_castle:"斯托姆城堡",I9_temple:"血神殿",FT_arena:"自由镇竞技场",D13_sanctuary:"伊罗西亚圣所",C13_pits:"禁坑",K7_cave:"科恩之心",K7_observatory:"观星台",J12_castle:"弃民要塞",H10_mine_2:"闹鬼回廊",H10_mine_3:"先民之城",F6_temple:"沉睡者神殿",C12_cave:"地下树丛",
};
const zhRegions = {
w_varsilia:"西瓦西利亚",n_varsilia:"北瓦西利亚",s_varsilia:"南瓦西利亚",e_varsilia:"东瓦西利亚",c_mercia:"梅尔西亚中部",e_mercia:"梅尔西亚东部",c_ilmara:"伊尔玛拉中部",e_ilmara:"伊尔玛拉东部",wild:"蛮荒之地",n_wild:"北蛮荒",e_wild:"东蛮荒",inori:"伊诺里沙漠",s_wild:"南蛮荒",w_thuram:"西图拉姆",e_thuram:"东图拉姆",w_ilmara:"西伊尔玛拉",
};

function fillRU(path, idCol, ruCol, map) {
  let text = fs.readFileSync(path, 'utf8').replace(/^\uFEFF/, '');
  const lines = text.split(/\r?\n/);
  let changed = 0, missed = [];
  const out = lines.map((line, idx) => {
    if (idx === 0 || !line.trim()) return line;
    const cols = line.split('\t');
    const zh = map[cols[idCol]];
    if (zh !== undefined) { cols[ruCol] = zh; changed++; return cols.join('\t'); }
    missed.push(cols[idCol]);
    return line;
  });
  fs.writeFileSync(path, out.join('\r\n'), 'utf8');
  console.log(path, 'changed:', changed, 'missed:', missed.join(', ') || 'none');
}

const base = process.argv[2];
fillRU(base + '/areas.txt', 0, 7, zhAreas);
fillRU(base + '/regions.txt', 0, 3, zhRegions);
