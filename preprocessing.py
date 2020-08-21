import pandas as pd
import numpy as np
import re
import pickle as pkl

def save_data(data, name):
    with open(f'./datasets/{name}.pkl', 'wb') as f:
        pkl.dump(data, f)
    return

def load_data(name):
    with open(f'./datasets/{name}.pkl', 'rb') as f:
        return pkl.load(f)


def clean(s, split=True, remove_ppn=False, min_clean=False, par_len=50):

    if isinstance(s, list):
        s_all = []
        for s_i in s:
            s_all.append(clean(s_i, split, remove_ppn, min_clean, par_len))
        if split:
            return [par for s_i in s_all for par in s_i]
        else:
            return ' '.join(s_all)

    #list for replacing/removing substrings
    #remove opening and closing text, define regex
    opening = re.search('(?i)CHAPTER \S+\s+', s)
    closing = re.search('(?sim)^\S*End of (the|this) Project Gutenberg.*', s)
    s = s[opening.end(): closing.start()]

    #replace/remove substrings
    replacements = [('(?i)\sVOLUME [I\d]+\W\s', ''), ('\d', '1'),
                    ('_', ''), ('--{1,}', ' - '), ('(?<=\S)\n(?=\S)', ' ')]
    if not min_clean:
        replacements.extend([('"', ''), ('\'s?', '')])
    if not split:
        replacements[1:1] = [('(?i)\sCHAPTER [IVXL\d]+\W\s', '')]
        replacements.append(('\s{1,}', ' '))
    for find, repl in replacements:
        s = re.sub(find, repl, s)

    if remove_ppn:
        s = proper_nouns(s)[0]

    #split into docs
    if split:
        chapters = re.split('(?i)\sCHAPTER [IVXL\d]+\W\s', s)
        split_regex = f'((?:(?:\S+?\s+?){{{par_len},}}?\S*)(?=\n\n))'
        paragraphs = []

        for chapter in chapters:
            chapter_pars = re.split(split_regex, chapter)
            if not re.search(split_regex, chapter_pars[-1]):
                chapter_pars[-2] = ' '.join(chapter_pars[-2:])
                chapter_pars = chapter_pars[:-1]
            paragraphs.extend(chapter_pars)

        split_regex_2 = f'((?:(?:\S+?\s+?){{{par_len*2},}}?\S*)[\.\!\?]"?)'
        for i, par in enumerate(paragraphs):
            if len(re.findall('\w+\W+', par)) > par_len * 5:
                paragraphs[i:i+1] = re.split(split_regex_2, par)

        if remove_ppn:
            remove_place_holder = lambda x: x.replace('insert_name', '')
            paragraphs = list(map(remove_place_holder, paragraphs))

        new_space = lambda x: re.sub('\s{1,}', ' ', x)
        paragraphs = list(map(new_space,paragraphs))

        paragraphs = [par.strip() for par in paragraphs if len(par)>2
                        and re.search('\w', par)]

        for i, par in enumerate(paragraphs):
            if len(re.findall('\w+\W+', par)) > par_len * 5:
                paragraphs[i:i+1] = re.split(f'((?:(?:\S+?\s+?){{{par_len*2},}}?\S*)[\.\!\?]"?)', par)
        return paragraphs
    else:
        return s

def proper_nouns(s, replace=True, return_nouns=False):

    #Find as many proper nouns as possible
    replacements = set()
    replacements.update(set(r for r in re.findall('(?:(?:Mr\. )|(?:Mrs\. )|(?:St\. )|(?:Hon\. ))([A-Z][-a-z]+)', s)))
    regex2 = '''(?x)(?<!\A)(?<!\A\s)(?<!\S)
                (?:Mr\.\s|Mrs\.\s|St\.\s|Miss\s|Sir\s|Captain\s|Colonel\s|
                (?<!\W\s))
                (?!Dear)(?!God)(?!Church)(?!Heaven)(?!Miss\w)(?!No\.)
                (?:[A-Z][-a-z]+(?:\s(?=[A-Z][-a-z]+))?)+'''
    replacements.update(set(re.findall(regex2, s)))

    #remove any pieces of compound proper nouns that were accidentally picked up
    ## eg remove 'End' because it's only a proper noun when paired with South in South End
    pre_suf = {}
    for noun_1 in replacements.copy():
        for noun_2 in replacements.copy():
            if f' {noun_1} ' in f'{noun_2} ':
                suf = pre_suf.get(noun_1)
                regex_str = f'(?<!{noun_2.replace(noun_1,"")})'
                regex_str_2 = f'(?!\s{noun_2.replace(noun_1,"")})'
                if suf:
                    suf[0] += regex_str
                    suf[1] += regex_str
                else:
                    suf = [regex_str, regex_str_2]
                pre_suf[noun_1] = suf

    regex_prefix = '(?i)(?:(?<!\A)(?<!\A\s)(?<!\S)(?<!\W\s)(?<!\W\s\s)'
    for k, v in pre_suf.items():
        if not re.search(f'{regex_prefix}{v[0]}){k}(?:{v[1]})', s):
            replacements.remove(k)


    if replace:
        place_holder = 'insert_name'

        for proper_noun in sorted(list(replacements))[::-1]:
            if ' ' not in proper_noun:
                s = re.sub(f'(?<=\W){proper_noun}\'?s?(?=\W)', place_holder, s)
            else:
                num_words = len(re.findall('\s', proper_noun)) + 1
                s = re.sub(f'(?<=\W){proper_noun}\'?s?(?=\W)', ' '.join([place_holder]*num_words), s)
        return s, replacements if return_nouns else s
    else:
        return replacements
