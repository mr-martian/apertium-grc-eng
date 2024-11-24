#!/usr/bin/env python3

import re
import sys

TAGS = {}
def add_tag(name, vals):
    TAGS[name] = (re.compile(f'{name}=(\\w+)'), vals)
add_tag('Gender', {'Fem': 'f', 'Masc': 'm', 'Neut': 'nt'})
add_tag('Number', {'Sing': 'sg', 'Dual': 'du', 'Plur': 'pl'})
add_tag('Case', {'Nom': 'nom', 'Gen': 'gen', 'Dat': 'dat', 'Acc': 'acc', 'Voc': 'voc'})
add_tag('Degree', {'Cmp': 'cmp', 'Sup': 'sup'})
add_tag('Mood', {'Ind': 'ind', 'Imp': 'imp', 'Sub': 'subj', 'Opt': 'opt'})
add_tag('Voice', {'Act': 'actv', 'Pass': 'passv', 'Mid': 'midv'})
add_tag('Aspect', {'Perf': 'perf', 'Imp': 'impf'})
add_tag('Tense', {'Past': 'past', 'Pres': 'pres', 'Fut': 'fut',
                  'Pqp': 'past'}) # TODO?
add_tag('VerbForm', {'Part': 'part', 'Fin': '', 'Inf': 'inf'})
add_tag('Person', {'1': 'p1', '2': 'p2', '3': 'p3'})
add_tag('PronType', {'Dem': 'dem', 'Art': 'def', 'Rel': 'rel', 'Prs': 'pers', 'Int': 'int', 'Rcp': 'ref', 'Ind': 'ind'})
add_tag('NumType', {'Card': '', 'Ord': 'ord'})

BYPOS = {
    'NOUN': ('n', ['Gender', 'Number', 'Case']),
    'PROPN': ('np', ['Gender', 'Number', 'Case']),
    'ADJ': ('adj', ['Degree', 'Gender', 'Number', 'Case']),
    'VERB': ('v', ['Mood', 'Voice', 'Aspect', 'Tense',
                   'VerbForm', 'Gender', 'Person', 'Number', 'Case']),
    'AUX': ('vbser', ['Mood', 'Voice', 'Aspect', 'Tense',
                      'VerbForm', 'Gender', 'Person', 'Number', 'Case']),
    'DET': ('det', ['PronType', 'Person', 'Gender', 'Number', 'Case']),
    'PRON': ('prn', ['PronType', 'Person', 'Gender', 'Number', 'Case']),
    'CCONJ': ('conjcoo', []),
    'SCONJ': ('conjsub', []),
    'ADP': ('pr', []),
    'ADV': ('adv', ['PronType']),
    'NUM': ('num', ['NumType', 'Gender', 'Case']),
    'PART': ('part', []),
    'INTJ': ('ij', []),
    'PUNCT': ('sent', []),
}

for line in sys.stdin:
    if not line.strip():
        sys.stdout.write('\n\0')
        sys.stdout.flush()
        continue
    elif line.startswith('#'):
        if 'sent_id =' in line:
            sys.stdout.write('['+line.split('=')[1].strip()+']')
        continue
    cols = line.strip().split('\t')
    if len(cols) != 10:
        continue
    if '-' in cols[0]:
        continue
    idx = cols[0]
    lem = cols[2]
    upos = cols[3]
    feats = cols[5]
    head = cols[6]
    rel = cols[7]
    spaceafter = ('' if 'SpaceAfter=No' in cols[9] else ' ')
    tags = []
    apos, cats = BYPOS[upos]
    if upos == 'PUNCT' and lem == ',':
        apos = 'cm'
    tags.append(apos)
    for cat in cats:
        pat, vals = TAGS[cat]
        if m := pat.search(feats):
            tags.append(vals[m.group(1)])
    ts = ''.join(f'<{t}>' for t in tags if t)
    sys.stdout.write(f'^{lem}{ts}<@{rel}><#{idx}→{head}>${spaceafter}')
sys.stdout.flush()
