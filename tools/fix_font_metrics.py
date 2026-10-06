# -*- coding: utf-8 -*-
"""Post-process Source-Han fnt: clamp glyph extent into SimHei lineHeight, CRLF output.
Formula per glyph: if height + yoffset > simLH  ->  yoffset = simLH - height
common lineHeight/base = SimHei values. Output CRLF, UTF-8."""
import os, re

GEN = r'C:\Games\Exiled Kingdoms-build11985424\_zh\gen'
SIM = r'C:\Games\Exiled Kingdoms-build11985424\_zh\data\ui\fonts_simhei_bak'
OUT = r'C:\Games\Exiled Kingdoms-build11985424\_zh\data\ui\fonts'
sizes = {'default':17,'tahoma16white':16,'tahoma20bold':20,'tahoma20white':20,
 'tahoma22bold':22,'tahoma22outline':22,'tahoma23white':23,'tahoma24bold':24,'tahoma25white':25,
 'tahoma26bold':26,'tahoma27bold':27,'tahoma27outline':27,'tahoma27white':27,'tahoma31outline':31,
 'tahoma32':32,'tahoma32bold':32,'tahoma38outline':38,'arialnarrow40bold':40}

for name, size in sizes.items():
    gen_t = open(os.path.join(GEN, 'size%d.fnt' % size), encoding='utf-8').read()
    sim_t = open(os.path.join(SIM, name + '.fnt'), encoding='utf-8').read()
    sim_lh = int(re.search(r'lineHeight=(\d+)', sim_t).group(1))
    sim_base = int(re.search(r'base=(\d+)', sim_t).group(1))
    out_lines = []
    clamped = 0
    for ln in gen_t.splitlines():
        if ln.startswith('common '):
            ln = re.sub(r'lineHeight=\d+ base=\d+',
                        'lineHeight=%d base=%d' % (sim_lh, sim_base), ln, count=1)
        elif ln.startswith('char '):
            d = dict(x.split('=', 1) for x in ln.split()[1:] if '=' in x)
            h = int(d['height']); yoff = int(d['yoffset'])
            if h + yoff > sim_lh:
                new_y = sim_lh - h
                ln = re.sub(r'yoffset=-?\d+', 'yoffset=' + str(new_y), ln)
                clamped += 1
        out_lines.append(ln)
    data = '\r\n'.join(out_lines) + '\r\n'
    open(os.path.join(OUT, name + '.fnt'), 'w', encoding='utf-8', newline='').write(data)
    print(name, 'size', size, 'simLH', sim_lh, 'clamped', clamped)
print('ALL DONE')
