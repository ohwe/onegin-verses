# -*- coding: utf-8 -*-

import re
from pprint import pprint
import random

# to reduce line to vowels only
vowels = u'аеёиоуыэюя'
def vowelize(line):
    return "".join([c for c in line.lower() if c in vowels])

# to remove punctuation and reduce prononciation
def simplify_line(line):
    line = " "+line.strip(",.;\"\n")+" "
    replaces = [
        (r'далеком', 'далёком'),
        (r'(\W)лед(\W)', '\\1лёд\\2'),
        (r'(\W)(раст|плет|по|зов|влеч|клад|жив|жд|вста|дохн|ид|нес|бер|пойм|вед|прид|прида|грыз|бь|разовь|найд)ет(\W)', '\\1\\2ёт\\3'),
        (r'\{[0-9]+\}', '')
        ]
    for pattern, repl in replaces:
        line = re.sub(pattern, repl, line, flags=re.I)
    return line.strip()

# to find rhyming tail of male line
def male_tail(line):
    m = re.search(ur'([^аеёиоуыэюя]?[аеёиоуыэюя][^аеёиоуыэюя]*)$', line, flags=re.I or re.U)
    if m:
        result = re.sub(ur'[\W]*',u'', m.group(1), flags=re.U)
        result = re.sub(ur'го',u'во', result, flags=re.I or re.U)
        result = re.sub(ur'^ь',u'', result, flags=re.I or re.U)
        result = re.sub(ur'^[^аеёиоуыэюя]([еёюя][^аеёиоуыэюя]+)',u'\\1', result, flags=re.I or re.U)
        return result
    return None 

# to find rhyming tail of female line
def female_tail(line):
    m = re.search(ur'([аеёиоуыэюя][^аеёиоуыэюя]*[аеёиоуыэюя][^аеёиоуыэюя]*)$', line, flags=re.I or re.U)
    if m:
        result = re.sub(ur'[\W]*',u'', m.group(1), flags=re.U)
        result = re.sub(ur'стн',u'сн', result, flags=re.I or re.U)
        result = re.sub(ur'^я',u'а', result, flags=re.I or re.U)
        result = re.sub(ur'^ё',u'о', result, flags=re.I or re.U)
        result = re.sub(ur'^ю',u'у', result, flags=re.I or re.U)
        result = re.sub(ur'^е',u'э', result, flags=re.I or re.U)
        result = re.sub(ur'([оа])([^аеёиоуыэюя]*)$',u'ОА\\2', result, flags=re.I or re.U)
        result = re.sub(ur'([ияе])([^аеёиоуыэюя]*)$',u'ИЯЕ\\2', result, flags=re.I or re.U)
        return result
    return None 

# to gather rhyming lines in one group for each rhyming tail
def make_groups(lines):
    groups = dict()
    for line, tail in lines:
        if tail in groups:
            groups[tail]['lines'].append(line)
        else:
            groups[tail] = dict(lines=[line], tail=tail, is_used = False)
    return groups

# ================================================================================
# ================================================================================
# ================================================================================

# 1. Prepare Onegin source: break into male/female lines, calculate tails
f = open("evgeny.txt", 'r') #mode="r", encoding="utf-8")
s = [line.decode('utf-8') for line in f]


s = [simplify_line(c) for c in s]
s_vowelized = [(line,len(vowelize(line))) for line in s]

s_female = [(line, female_tail(line)) for line, size in s_vowelized if size == 9]
s_male   = [(line, male_tail(line)) for line, size in s_vowelized if size == 8]


groups = [
    [v for v in make_groups(s_female).values() if len(v["lines"]) > 7],
    [v for v in make_groups(s_male).values() if len(v["lines"]) > 7]
]
[g.sort(key=lambda a: len(a["lines"])) for g in groups]


# 2. Get verse structure
style = raw_input('Verse structure (AA11BB22)-> ') 

# 3. Arrange most frequent rhymes to be counted first
letters = dict()
for letter in style:
    if letter in letters:
        letters[letter]['count'] += 1
    else:
        letters[letter] = dict(letter=letter, count=1, pos=0)

letterslist = [v for v in letters.values()]
letterslist.sort(key = lambda a: -a["count"])

# 4. Build up verse
letters = dict()
for item in letterslist:
    if item["letter"] in "0123456789":
        index = 0
    else:
        index = 1
    sequence = [g for g in groups[index] if len(g["lines"]) >= item["count"] and not g["is_used"]]
    sample = random.sample(sequence, 1)
    sample[0]["is_used"] = True
    item["lines"] = random.sample(sample[0]["lines"], item["count"])
    letters[ item["letter"] ] = item


# 5. Print verse
for letter in style:
    print letters[letter]["lines"][ letters[letter]["pos"] ]
    letters[letter]["pos"]+=1


