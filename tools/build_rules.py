# -*- coding: utf-8 -*-
"""Build items/bestiary/castles column files + RU skills override files."""
import io, json, os, sys

SRC = r'C:\Users\dt7396\AppData\Local\Temp\ek\full\data'
OUT = r'C:\Games\Exiled Kingdoms-build11985424\_zh\data'
DOCS = r'C:\Games\Exiled Kingdoms-build11985424\_zh\docs'

def load_json(name):
    return json.load(io.open(os.path.join(DOCS, name), encoding='utf-8'))

def write_bytes(path, data):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(path, 'wb') as f:
        f.write(data)
    print('wrote', path, len(data), 'bytes')

def build_items():
    items = {}
    for f in ('trans_items1.json', 'trans_items2.json'):
        items.update(load_json(f))
    lines = io.open(os.path.join(SRC, 'rules/items_text.txt'), encoding='utf-8-sig', newline='').read()
    rows = lines.split('\r\n')
    assert rows[-1] == ''
    rows = rows[:-1]
    n = 0
    hit = set()
    for i, r in enumerate(rows):
        c = r.split('\t')
        if c[0] == 'item_ID':
            continue
        if c[0] in items:
            name, desc = items[c[0]]
            has_name = len(c) > 1 and c[1].strip()
            has_desc = len(c) > 2 and c[2].strip()
            if has_name:
                c[5] = name
            if has_desc:
                c[6] = desc
            rows[i] = '\t'.join(c)
            n += 1
            hit.add(c[0])
    print('items rows translated:', n, 'unique ids:', len(hit), '/', len(items))
    assert len(hit) == len(items)
    write_bytes(os.path.join(OUT, 'rules/items_text.txt'),
                ('\ufeff' + '\r\n'.join(rows) + '\r\n').encode('utf-8'))

def build_bestiary():
    tr = load_json('trans_bestiary.json')
    rows = io.open(os.path.join(SRC, 'rules/bestiary_names.txt'), encoding='utf-8-sig', newline='').read()
    rows = rows.split('\r\n')[:-1]
    for i, r in enumerate(rows):
        if i == 0:
            continue
        c = r.split('\t')
        v = tr[str(i - 1)]
        if v:
            c[3] = v
        rows[i] = '\t'.join(c)
    write_bytes(os.path.join(OUT, 'rules/bestiary_names.txt'),
                ('\ufeff' + '\r\n'.join(rows) + '\r\n').encode('utf-8'))

def build_castles():
    tr = load_json('trans_castles.json')
    rows = io.open(os.path.join(SRC, 'world/castles_desc.txt'), encoding='utf-8-sig', newline='').read()
    rows = rows.split('\r\n')[:-1]
    for i, r in enumerate(rows):
        if i == 0:
            continue
        c = r.split('\t')
        c[3] = tr[str(i)]
        rows[i] = '\t'.join(c)
    write_bytes(os.path.join(OUT, 'world/castles_desc.txt'),
                ('\ufeff' + '\r\n'.join(rows) + '\r\n').encode('utf-8'))

SKILL_FILES = ['skills.txt', 'skills2.txt', 'skills3.txt',
               'skills_advanced.txt', 'skills_advanced2.txt', 'skills_advanced3.txt']

def build_skills():
    tr = load_json('trans_skills.json')
    for f in SKILL_FILES:
        src_rows = io.open(os.path.join(SRC, 'rules/RU/' + f), encoding='utf-16', newline='').read()
        src_rows = src_rows.split('\r\n')
        if src_rows[-1] == '':
            src_rows = src_rows[:-1]
        en_rows = io.open(os.path.join(SRC, 'rules/' + f), encoding='utf-8-sig').read().splitlines()
        assert len(src_rows) == len(en_rows), (f, len(src_rows), len(en_rows))
        n = 0
        for i in range(1, len(src_rows)):
            c = src_rows[i].split('\t')
            name, desc = tr[f + '#' + str(i)]
            c[0] = name
            if len(c) > 1:
                c[1] = desc
            else:
                c.append(desc)
            src_rows[i] = '\t'.join(c)
            n += 1
        print('skills', f, 'rows:', n)
        write_bytes(os.path.join(OUT, 'rules/RU/' + f),
                    ('\ufeff' + '\r\n'.join(src_rows) + '\r\n').encode('utf-16'))

def build_factions():
    tr = load_json('trans_factions.json')
    rows = io.open(os.path.join(SRC, 'world/factions_text.txt'), encoding='utf-8-sig', newline='').read()
    rows = rows.split('\r\n')[:-1]
    n = 0
    for i, r in enumerate(rows):
        if i == 0:
            continue
        c = r.split('\t')
        if c[0] in tr:
            name, desc = tr[c[0]]
            c[5] = name
            c[6] = desc
            rows[i] = '\t'.join(c)
            n += 1
    print('factions translated:', n, '/', len(tr))
    assert n == len(tr)
    write_bytes(os.path.join(OUT, 'world/factions_text.txt'),
                ('\ufeff' + '\r\n'.join(rows) + '\r\n').encode('utf-8'))

def build_randnames():
    tr = load_json('trans_randnames.json')
    rows = io.open(os.path.join(SRC, 'world/random_names.txt'), encoding='utf-8-sig', newline='').read()
    rows = rows.split('\r\n')[:-1]
    n = 0
    for i, r in enumerate(rows):
        if i == 0:
            continue
        c = r.split('\t')
        key = c[0] + '|' + c[1]
        if key in tr:
            c[1] = tr[key]
            rows[i] = '\t'.join(c)
            n += 1
    print('random names translated:', n, '/', len(tr))
    assert n >= len(tr) - 1
    # 无参 readString()（平台默认编码 GBK）读取，中文必须 GBK 写入；原文件无 BOM
    body = '\r\n'.join(rows) + '\r\n'
    write_bytes(os.path.join(OUT, 'world/random_names.txt'),
                body.encode('gbk'))

def build_questvars():
    targets = load_json('trans_bounty_targets.json')
    locs = load_json('trans_questlocs.json')
    vdir = os.path.join(SRC, 'quests/variations')
    for f in os.listdir(vdir):
        if not f.endswith('.txt'):
            continue
        rows = io.open(os.path.join(vdir, f), encoding='utf-8-sig', newline='').read()
        rows = rows.split('\r\n')[:-1]
        n = 0
        for i, r in enumerate(rows):
            if i == 0:
                continue
            if not r.strip():
                continue
            c = r.split('\t')
            if f.startswith('bounty') and len(c) > 6 and c[6].strip() and c[6] in targets:
                c[6] = targets[c[6]]
                rows[i] = '\t'.join(c)
                n += 1
            elif f == 'quest_locations.txt' and c[0] in locs:
                c[1] = locs[c[0]]
                rows[i] = '\t'.join(c)
                n += 1
        print('questvars', f, 'rows:', n)
        if n:
            # 无参 readString() 用平台默认编码（GBK）读取：中文必须 GBK 写入，
            # 原版西语列的 ó/á/ñ/û 无法 GBK 编码，NFD 去变音 ASCII 化（仅西语模式显示用）
            import unicodedata
            body = '\r\n'.join(rows) + '\r\n'
            body = ''.join(ch for ch in unicodedata.normalize('NFD', body)
                           if unicodedata.category(ch) != 'Mn')
            write_bytes(os.path.join(OUT, 'quests/variations/' + f),
                        body.encode('gbk'))

build_items()
build_bestiary()
build_castles()
build_factions()
build_randnames()
build_questvars()
build_skills()
print('ALL OK')
