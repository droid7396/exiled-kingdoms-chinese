# -*- coding: utf-8 -*-
import io, json

tr = {}
def add(tid, pairs):
    for en, zh in pairs:
        tr[tid + '|' + en] = zh

add('male_first', [
    ('Trace','特雷斯'),('Shep','谢泼德'),('Abel','亚伯'),('Nedes','内德斯'),('Horton','霍顿'),
    ('Austyn','奥斯汀'),('Whit','惠特'),('Clifford','克利福德'),('Rudy','鲁迪'),('Dale','戴尔'),
    ('Johann','约翰'),('Peter','彼得'),('Jorah','乔拉'),('Xort','克索特'),('Deren','德伦'),
    ('Xarryl','克萨里尔'),('Machian','马基安'),('Asherun','阿瑟伦'),('Kudaze','库达泽'),('Jizar','吉扎尔'),
    ('Rahun','拉胡恩'),('Konrad','康拉德'),('Don','唐'),('Uther','乌瑟'),('Dagor','达戈尔'),
    ('Rogard','罗加德'),('Soemon','索蒙'),('Grem','格伦'),('Wyan','怀恩'),('Fiorr','菲奥尔'),
    ('Boro','博罗'),('Imtun','因顿'),('Tordak','托达克'),('Jutam','朱塔姆'),('Anton','安东'),
    ('Klaus','克劳斯'),('Markus','马库斯'),('Gustav','古斯塔夫'),('Patrick','帕特里克'),('Korg','科格'),
    ('Arthur','亚瑟'),
])
add('female_first', [
    ('April','艾普莉'),('Mya','米娅'),('Lysette','莉塞特'),('Johanna','约翰娜'),('Mariella','玛丽埃拉'),
    ('Jeanette','珍妮特'),('Constanz','康斯坦茨'),('Xoa','克索娅'),('Mara','玛拉'),('Ryella','莉艾拉'),
    ('Amber','安珀'),('Akia','阿琪雅'),('Ilene','艾琳'),('Niraya','妮拉雅'),('Teresse','特蕾丝'),
    ('Mera','梅拉'),('Arelle','艾蕾尔'),('Ethane','伊珊'),('Grea','格蕾雅'),('Martha','玛莎'),
    ('June','琼'),('Sella','塞拉'),('Medea','美狄亚'),('Hilga','希尔加'),('Jemm','杰姆'),
    ('Jasmine','贾斯敏'),('Dharme','达尔梅'),('Ingara','英加拉'),('Zilma','齐尔玛'),('Anna','安娜'),
])
alias = [
    ('the Brave','勇者'),('the Fast','快手'),('the Strong','壮汉'),('Longstrides','长步者'),
    ('Brightblade','亮刃'),('Orc-slayer','屠兽人者'),('the Thirsty','渴酒鬼'),('Bighands','大手'),
    ('the Snake','毒蛇'),('the Shadow','暗影'),('Longfingers','长指'),('BrokenAxe','断斧'),
    ('Beermaster','啤酒大师'),('Inn-burner','烧酒馆的'),('the Humorous','乐天派'),('the Damp','湿漉漉'),
    ('the Swift','疾风'),('the Traveller','旅人'),('the Easterner','东方人'),('the Red','红发'),
]
add('alias_male', alias)
add('alias_female', alias)
add('human_second', [
    ('Vivet','维维特'),('Heyne','海因'),('Alls','奥尔斯'),('Dillworth','迪尔沃斯'),('Cabanes','卡巴内斯'),
    ('Witts','威茨'),('Burlot','布洛特'),('da Cruz','达克鲁兹'),('Banton','班顿'),('Sauvetre','索维特'),
    ('Sossar','索萨尔'),('Azoun','阿祖恩'),('Leeds','利兹'),('Waterworth','沃特沃斯'),('Onathe','奥纳丝'),
    ('Quasee','奎西'),('Zephale','泽法尔'),('Orhaur','奥豪尔'),('Greengate','格林盖特'),('Desini','德西尼'),
    ('Dozer','多泽'),('Flonwe','弗隆薇'),('Izerra','伊泽拉'),('Maslyc','马斯利克'),('Xeffar','克塞法'),
    ('Dearot','迪亚罗特'),('Tonherai','通赫莱'),('Risso','里索'),('Xtole','克斯托尔'),('Croc','克洛克'),
    ('Gurtam','古尔塔姆'),('Xaltabar','克萨尔塔巴'),('Themeder','塞梅德'),('Jabru','贾布鲁'),('Mert','默特'),
    ('Legran','勒格朗'),('Kamlavi','卡姆拉维'),('Dent','登特'),('Vundavar','文达瓦'),('Fonterasu','方特拉苏'),
    ('Karamas','卡拉马斯'),('Tilgo','蒂尔戈'),('Frammz','弗拉姆兹'),('Glimte','格林特'),('Storba','斯托尔巴'),
    ('Nurthagax','努尔萨加克斯'),('Paldasar','帕尔达萨'),('Xaatul','克萨图尔'),('Xojei','克索杰'),
])
add('humanoid_first', [
    ('Gumku','冈姆库'),('Xongor','宗戈尔'),('Thukpe','苏克佩'),('Bartug','巴图格'),('Orgash','奥尔加什'),
    ('Morog','莫罗格'),('Lofdar','洛夫达'),('Ximbair','辛贝尔'),('Dorthog','多索格'),('Kurtag','库尔塔格'),
    ('Omdu','奥姆杜'),('Niithul','尼苏尔'),('Uurda','乌尔达'),('Knedur','克内杜尔'),('Thulgash','苏尔加什'),
    ('Radabur','拉达布尔'),('Tromkah','特罗姆卡'),('Duuguth','杜古斯'),
])
add('humanoid_second', [
    ('the Scourge','祸祟'),('the Devourer','吞噬者'),('Bone-eater','噬骨者'),('Bloodfangs','血牙'),
    ('the Vile','卑劣者'),('of the North','北境的'),('the Sacrilegous','渎神者'),('the Tormentor','折磨者'),
    ('Skin-peeler','剥皮者'),('the Dark','黑暗者'),('the Horned One','角冠者'),('the Nightmare','梦魇'),
    ('the Destroyer','毁灭者'),('Deathspawn','死亡裔'),('the Reckless','莽撞者'),('the Crusher','碾碎者'),
    ('Smallhead','小头'),('the Cannibal','食人者'),
])
add('dragon', [
    ('Baliarthix','巴利亚尔提克斯'),('Tesselthadyr','泰塞尔萨迪尔'),('Kaledrath','卡莱德拉斯'),
    ('Kelorthigax','凯洛尔希加克斯'),('Nivafraxis','尼瓦弗拉克西斯'),('Ursiladaryn','乌尔西拉达林'),
    ('Tarrdynaxyl','塔尔迪纳克西尔'),('Gronidartur','格罗尼达图尔'),('Thelkumassar','塞尔库玛萨尔'),
    ('Saddanilakamir','萨达尼拉卡米尔'),('Soradarth','索拉达斯'),('Grikanamon','格里卡纳蒙'),
    ('Dekalatroth','德卡拉洛斯'),('Forzarhyntar','福尔扎林塔尔'),('Okardaxys','奥卡达克西斯'),
    ('Yntolarzos','因托拉尔佐斯'),('Xyldaraknamis','克西尔达拉克纳米斯'),('Glotandaran','格洛坦达兰'),
    ('Durstandavyr','杜尔斯坦达维尔'),('Waroklys','瓦罗克利斯'),
])
add('lich', [
    ('Gillorg','吉尔戈格'),('Mazdhu','马兹杜'),('Occno','奥克诺'),('Blofix','布洛菲克斯'),
    ('Gridorg','格里多格'),('Ursun','乌尔松'),('Glibra','格利布拉'),('Dexxor','德克索尔'),
    ('Xedoc','克西多克'),('Komg','孔格'),
])
add('beast', [
    ('Gloop','格卢普'),('Murdax','穆尔达克斯'),('Nemto','内姆托'),('Lortw','洛尔特'),
    ('Xumua','克苏穆娅'),('Rauze','罗泽'),('Kleeho','克利霍'),('Jamru','贾姆鲁'),
    ('Keena','基纳'),('Afurt','阿弗特'),
])

# 覆盖校验
src = io.open(r'C:\Games\Exiled Kingdoms-build11985424\_zh\docs\_dump_randnames.txt', encoding='utf-8').read().splitlines()
missing = []
for ln in src:
    tid, en = ln.split('\t')
    if tid + '|' + en not in tr:
        missing.append(tid + '|' + en)
assert not missing, missing
assert len({tid + '|' + en for tid, en in (ln.split('\t') for ln in src)}) == len(tr), (len(src), len(tr))
io.open(r'C:\Games\Exiled Kingdoms-build11985424\_zh\docs\trans_randnames.json', 'w',
        encoding='utf-8').write(json.dumps(tr, ensure_ascii=False, indent=0))
print('written', len(tr))
