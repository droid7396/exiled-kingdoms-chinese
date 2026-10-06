# -*- coding: utf-8 -*-
import io, json

BASE = r'C:\Games\Exiled Kingdoms-build11985424\_zh\docs'

bounty = {
'Centurion Lesane':'百夫长勒桑','Centurion Rannir':'百夫长兰尼尔',
'Decurion Chogga':'什长乔加','Decurion Gracim':'什长格拉西姆','Decurion Kamzin':'什长卡姆津',
'Decurion Ogglo':'什长奥格洛','Decurion Roikan':'什长罗伊坎','Decurion Samzu':'什长萨姆祖','Decurion Tharim':'什长塔里姆',
'Druid Elder Wind':'德鲁伊"风之长老"','Druid Emerald Mist':'德鲁伊"翠雾"',
'Goblin Beastmaster Grick':'哥布林兽王格里克','Goblin Beastmaster Ixuz':'哥布林兽王克苏兹','Goblin Beastmaster Izzo':'哥布林兽王伊佐',
"Goblin Beastmaster R'n'z":'哥布林兽王阿恩兹','Goblin Beastmaster Raz':'哥布林兽王拉兹','Goblin Beastmaster Sgaar':'哥布林兽王斯加尔',
'Goblin Chief Rangli':'哥布林头目兰格利','Goblin Chief Uddo':'哥布林头目乌多','Goblin Chief Ujfo':'哥布林头目乌吉佛',
'Goblin Firedancer Kakku':'哥布林舞焰者卡库','Goblin Firedancer Sliko':'哥布林舞焰者斯利科',
'Goblin Firelord Bligo':'哥布林焰主布利戈','Goblin Firelord Elmo':'哥布林焰主埃尔莫',
'Goblin Sergeant Aazi':'哥布林军士阿兹','Goblin Sergeant Grech':'哥布林军士格雷奇','Goblin Sergeant Hirr':'哥布林军士希尔',
'Goblin Sergeant Hoor':'哥布林军士胡尔','Goblin Sergeant Iogch':'哥布林军士约格奇','Goblin Sergeant Lirxis':'哥布林军士利尔克西',
'Goblin Sergeant Tzion':'哥布林军士齐翁',"Goblin Sergeant U'uag":'哥布林军士乌阿格','Goblin Sergeant Xitil':'哥布林军士克西蒂尔',
'Hag Aggra':'老巫婆阿格拉','Hag Rilwa':'老巫婆莉尔娃','Hag Silgye':'老巫婆西尔吉耶',
'Hunter Bear Fang':'猎手"熊牙"','Hunter High Sky':'猎手"高天"','Hunter One Ear':'猎手"独耳"',
'Hunter Windsong':'猎手"风歌"','Hunter Wolf Eye':'猎手"狼眼"','Hunter Wolf Shadow':'猎手"狼影"',
'Joanne the Bloody':'嗜血的乔安妮',
'Legionnaire Felco':'军团兵费尔科','Legionnaire Garin':'军团兵加林','Legionnaire Mirdo':'军团兵米尔多',
'Orc Captain Imzûr':'兽人队长伊姆祖尔','Orc Captain Kazhu':'兽人队长卡祖','Orc Captain Okkud':'兽人队长奥库德',
'Orc Captain Rurgoz':'兽人队长鲁尔戈兹','Orc Captain Skurnah':'兽人队长斯库尔纳','Orc Captain Suraa':'兽人队长苏拉',
'Orc Captain Tarrju':'兽人队长塔尔朱',
'Orc Commander Gargath':'兽人指挥官加尔加斯','Orc Commander Torkûn':'兽人指挥官托尔昆',
'Orc Sergeant Erund':'兽人军士厄伦德','Orc Sergeant Gurshagar':'兽人军士古尔沙加','Orc Sergeant Isk-Hor':'兽人军士伊斯克-霍尔',
'Orc Sergeant Kolang':'兽人军士科朗','Orc Sergeant Korzog':'兽人军士科尔佐格','Orc Sergeant Morog':'兽人军士莫罗格',
'Orc Sergeant Norok':'兽人军士诺罗克','Orc Sergeant Ordak':'兽人军士奥尔达克','Orc Sergeant Ufang':'兽人军士乌方',
'Orc Sergeant Urkaz':'兽人军士乌尔卡兹','Orc Sergeant Urki':'兽人军士乌尔基',
'Outlaw Natalia Rirz':'法外之徒娜塔莉娅·里尔兹','Outlaw Neroos Ahir':'法外之徒尼鲁斯·阿希尔','Outlaw Radz Assar':'法外之徒拉德兹·阿萨尔',
'Skeleton of General Tarih':'塔里赫将军的骸骨','Skeleton of Lady Arish':'阿里什夫人的骸骨',
'Skeleton of Lady Irda':'伊尔达夫人的骸骨','Skeleton of Lady Lessa':'蕾莎夫人的骸骨',
'Skeleton of Lord Migar':'米加尔领主的骸骨','Skeleton of Sir Dagosh':'达戈什爵士的骸骨',
'Slave Clea':'奴隶克莉娅','Slave Kligan':'奴隶克利根','Slave Milo':'奴隶米洛','Slave Rana':'奴隶拉娜',
'Slave Rume':'奴隶露梅','Slave Tadir':'奴隶塔迪尔','Slave Tadnesh':'奴隶塔德内什','Slave Tiglo':'奴隶蒂格洛',
'Slave Togio':'奴隶托吉奥','Slave Zemi':'奴隶泽米',
'Thief Al Corcon':'盗贼阿尔·科尔孔','Thief Annor Ifargash':'盗贼安诺·伊法加什','Thief Djone Aego':'盗贼琼妮·艾戈',
'Thief Edill Niosme':'盗贼埃迪尔·尼奥斯梅','Thief Holler Hinch':'盗贼霍勒·欣奇','Thief Jorg Undran':'盗贼约格·翁德兰',
'Thief Moxto Les':'盗贼莫克斯托·莱斯','Thief Sajtin Torass':'盗贼萨金·托拉斯','Thief Terence Essei':'盗贼特伦斯·艾赛',
'Tolassian Champion Dalena':'托拉西亚勇士达莲娜','Tolassian Champion Gradis':'托拉西亚勇士格拉迪斯',
'Tolassian Champion Mutzug':'托拉西亚勇士穆祖格','Tolassian Champion Mygga':'托拉西亚勇士米加',
'Tolassian Champion Ogdor':'托拉西亚勇士奥格多','Tolassian Champion Soffru':'托拉西亚勇士索弗鲁',
'Tolassian Champion Ulzzu':'托拉西亚勇士乌尔祖',
'Tolassian Mummy Ge\'erth':'托拉西亚木乃伊盖尔斯','Tolassian Mummy Remmur':'托拉西亚木乃伊雷穆尔',
'Tolassian Mummy Ugalie':'托拉西亚木乃伊乌加莉',
'Tolassian Noble Tuarth':'托拉西亚贵族图阿尔斯','Tolassian Noble Urdemg':'托拉西亚贵族乌尔德姆格',
'Witch Exloe':'女巫克丝洛埃','Witch Gamed':'女巫加梅德','Witch Groofe':'女巫格鲁菲',"Witch Gyw'da":'女巫吉薇达',
'Witch Gyywe':'女巫吉薇',"Witch Il'ex":'女巫伊尔埃克斯','Witch Lixxa':'女巫莉克萨','Witch Loddri':'女巫洛德里',
'Witch Rexea':'女巫蕾克茜娅',
}
locs = {
'I8_1':'在区域西北方的一处营地','I8_2':'在海岸边的一处营地，位于西南方',
'I11_1':'在河南岸，偏西','I11_2':'在河北岸，位于西北',
'H11_1':'在河北岸，偏西','H11_2':'在河北面的丘陵中，位于东侧',
'H10_1':'紧邻兰尼加村的西侧','H10_2':'在兰尼加谷地的中部',
'G10_1':'在沼泽附近','G10_2':'在南侧丘陵中',
'H9_1':'紧邻河南岸','H9_2':'在东北面的丘陵附近',
'G9_1':'在王桥区域的东北边缘','G9_2':'紧邻城镇北侧','G9_3':'在蓝雾河的南岸',
'H8_1':'在城北的河畔附近','H8_2':'在海边附近',
'H10_mine_1':'在东北方的一处深穴中','H10_mine_2':'在西北方的一处深穴中',
'H11_cave_1_1':'在西南方的一处洞室中','H11_cave_1_2':'在西北方的一处洞室中','H11_cave_1_3':'在地城中部附近的一处洞室中',
'F9_1':'在区域的西北方','F9_2':'在森林深处，偏西',
'G11_1':'在区域的西南方','G11_2':'在区域中部、河的南面',
'G9_cave_1':'在西北方的深室中','G9_cave_2':'在东北方的一间储藏室里',
'H9_lair_1':'在东北方的一处深穴中','H9_lair_2':'在巢穴中央的王者大厅里','H9_lair_3':'在西南方的一处洞室中',
'I10_1':'在道路旁、区域中部','I10_2':'在道路旁，位于西北',
'F10_1':'在城镇东侧、河边','F10_2':'在城镇南面，延伸至丘陵',
'H10_tomb_1':'在西南方的一处墓室中','H10_tomb_2':'在东南方的一处墓室中','H10_tomb_3':'在东北方的一处墓室中',
'H8_tomb_1':'在东南方的一处墓室中','H8_tomb_2':'在东北方的一处墓室中','H8_tomb_3':'在西北方的一处墓室中',
'G10_tomb_1':'在东北方的一处墓室中','G10_tomb_2':'在东南方的一处墓室中','G10_tomb_3':'在西北方的一处墓室中',
'F8_1':'在东南方','F8_2':'在城镇南面',
'E8_1':'在东南方的一处营地','E8_2':'在南面山区附近的一处营地','E8_3':'在西北方的一处营地',
'E9_1':'在西北方的一处营地','E9_2':'在东南方的一处营地','E9_3':'在东北方的一处营地',
'D10_1':'在西南方','D10_2':'在东面、山脉旁',
'D9_1':'在西南方','D9_2':'在西北方',
'D8_1':'在南面、山脉旁','D8_2':'在东北方的一处营地','D8_3':'在西北方的一处营地',
'D8_castle_1':'在靠近入口的一间厅室中','D8_castle_2':'在西南方的一间厅室中',
'F11_1':'在西南方','F11_2':'在南岸，位于东侧','F11_3':'在西北方',
'E11_1':'在东南方','E11_2':'在西北方','E11_3':'在西南方',
'D11_1':'在东南方','D11_2':'在西北方','D11_3':'在西南方',
'D12_1':'在东南方','D12_2':'在西北方','D12_3':'在西南方',
'E12_1':'在北面','E12_2':'在东南方',
'F11_tomb_1':'在西北方的一处墓室中','F11_tomb_2':'在东北方的一处墓室中',
'D11_abbey_1':'在西北方的食堂里','D11_abbey_2':'在东北方的一间小僧房里','D11_abbey_3':'在靠近入口西侧的一间房里',
}

# 覆盖校验
src_t = set(io.open(BASE + r'\_dump_bounty_targets.txt', encoding='utf-8').read().split('\n'))
src_t.discard('')
assert src_t == set(bounty), ('missing:', src_t - set(bounty), 'extra:', set(bounty) - src_t)
src_l = set()
for r in io.open(r'C:\Users\dt7396\AppData\Local\Temp\ek\full\data\quests\variations\quest_locations.txt', encoding='utf-8-sig', newline='').read().split('\r\n')[1:]:
    if r.strip():
        src_l.add(r.split('\t')[0])
assert src_l == set(locs), ('missing:', src_l - set(locs), 'extra:', set(locs) - src_l)

io.open(BASE + r'\trans_bounty_targets.json', 'w', encoding='utf-8').write(json.dumps(bounty, ensure_ascii=False, indent=0))
io.open(BASE + r'\trans_questlocs.json', 'w', encoding='utf-8').write(json.dumps(locs, ensure_ascii=False, indent=0))
print('bounty:', len(bounty), 'locs:', len(locs))
