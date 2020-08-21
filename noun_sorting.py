import re
import pickle as pkl

def load(filename):
    with open(f'datasets/{filename}.pkl', 'rb') as f:
        vals = pkl.load(f)
    ppn_list, text, person_titles,place_terms, not_classified, ppn_types = vals
    pn = ProperNouns(text, person_titles, place_terms, ppn_list)
    pn.not_classified = not_classified
    pn.ppn_types = ppn_types
    return pn

def input_placeholders(ppn_types, s):
    placeholders = {'languages':'-LNG-', 'nationalities':'-NTL-',
                   'countries':'-CNT-', 'months':'-MTH-', 'weekdays':'-WKD-',
                   'holidays':'-HLD-', 'bodies_of_water':'-WTR-',
                   'boats':'-BTS-', 'authors':'-AUT-', 'literature':'-LTR-',
                   'newspapers':'-NPP-', 'places':'-PLC-',
                   'last_names':'-LNM-', 'male_names':'-MNM-',
                   'female_names':'-FNM-'}

    ppn_types = ProperNouns().escape(ppn_types)
    for k, v in ppn_types.items():
        placeholder = proper_noun_placeholders[k]
        regex_prefix = '(?<=\W)(?:the\s|The\s)?' if k in ['countries', 'literature'] else '(?<=\W)'
        regex_suffix = '(?=\W|s)' if k in ['weekdays', 'last_names', 'male_names', 'female_names'] else '(?=\W)'
        for r in sorted(v)[::-1]:
            regex = regex_prefix + r + regex_suffix
            s = re.sub(regex, placeholder, s)
    return s

class ProperNouns():

    def __init__(self, text, person_titles, place_terms,
                 proper_nouns_list=None, noun_types=None):
        '''
        Class to find and store proper nouns by type
        Arguments:
        - text: string or list of strings from which to generate proper nouns
        '''
        if not proper_nouns_list:
            import preprocessing as pp
            if 'Project Gutenberg' in text:
                text = pp.clean(text, split = False)
            self.ppn_list = pp.proper_nouns(text, replace=False, return_nouns=True)
        else:
            self.ppn_list = set(proper_nouns_list)

        self.text = text
        self.ppn_types = {}
        if noun_types:
            for type in noun_types:
                self.ppn_types[type] = set()
        self.person_titles = set(person_titles)
        self.place_terms = set(place_terms)
        self.not_classified = set()

    def check_type(self, type):
        try:
            return self.ppn_types[type]
        except:
            raise ValueError(f'Proper noun type {type} does not exist')

    def add(self, type, nouns=None):
        if nouns and not isinstance(nouns, list):
            nouns = set(nouns)
        if type == 'not classified':
            self.not_classified.update(nouns)
        else:
            try:
                self.ppn_types[type].update(nouns)
                if nouns:
                    [self.not_classified.discard(noun) for noun in nouns]
            except:
                self.ppn_types[type] = set(nouns) if nouns else set()
        return

    def remove(self, type, nouns):
        if type == 'not classified':
            [self.not_classified.discard(noun) for noun in nouns]
        else:
            try:
                [self.ppn_types[type].discard(noun) for noun in nouns]
                self.not_classified.update(set(nouns))
            except:
                raise ValueError(f'Proper noun type {type} does not exist')

    def save(filename):
        with open(f'datasets/{filename}.pkl', 'wb') as f:
            pkl.dump((self.ppn_list, self.text, self.person_titles,
                      self.place_terms, self.not_classified, self.ppn_types), f)

    def save_types(filename):
        with open(f'datasets/{filename}.pkl', 'wb') as f:
            pkl.dump(self.ppn_types, f)

    def show_context(self, nouns, context_width=50, text=None,
                     left_regex='\W', right_regex='\W', prefix = '',
                     suffix = ''):
        if not text: text = self.text
        for word in list(nouns):
            regex = f'{prefix}{left_regex}{word}{right_regex}{suffix}'
            print(word.upper(), ':\n')
            r = re.search(regex, text)
            start = 0
            while r:
                print(text[start + r.start() - context_width:
                                start + r.end() + context_width], '\n')
                start += r.end()
                r = re.search(regex, text[start:])

    def sort_basic_ppns(self, months=None, weekdays=None, ppns=None):
        months = self.check_type('months')
        weekdays = self.check_type('weekdays')
        if not ppns:
            ppns = list(self.ppn_list)
        self.add('people', set())
        self.add('places', set())

        # Find some people and place names
        names, place_names = set(), set()
        for ppn in ppns:
            found = False
            for title in self.person_titles:
                # If the proper noun has a person title (eg Mr) the rest of
                ## the term must be a person's name
                if f' {title} ' in f' {ppn} ':
                    no_title = ppn.replace(title, '').strip()
                    if no_title:
                        self.add('people', ppn)
                        names.update({*no_title.split()})
                    found = True
                    break
            if found:
                continue
            for term in self.place_terms:
                # Similarly if the proper noun has a place term (eg Street)
                ## the rest of the term must be a place name
                if f' {term} ' in f' {ppn} ' or f' {term}s ' in f' {ppn} ':
                    no_term = ppn.replace(term, '').strip()
                    if no_term:
                        self.add('places', ppn)
                        place_names.add(no_term)
                    found = True
                    break

        places = self.ppn_types['places']
        people = self.ppn_types['people']

        for ppn in ppns:
            if ppn in places or ppn in people:
                continue
            if any([f' {month} ' in f' {ppn} ' for month in months]):
                continue
            if any([f' {day} ' in f' {ppn} ' for day in weekdays]):
                continue
            found = False
            for name in names:
                if f' {name} ' in f' {ppn} ' or f' {name}s ' in f' {ppn} ':
                    self.add('people', ppn)
                    found = True
                    break
            if found: continue
            for name in place_names:
                if f' {name} ' in f' {ppn} ' or f' {name}s ' in f' {ppn} ':
                    self.add('places', ppn)
                    found = True
                    break
            if found: continue
            else:
                if any(suffix in f'{ppn} ' for suffix in ['shire ', 'side ', 'ton ', 'ham ', 'ford ', 'bury ']):
                    self.add('places', ppn)
                else:
                    self.not_classified.add(ppn)
        return

    def find_compound_places(self):
        place_terms = self.place_terms.copy()
        dont_keep = ['North', 'South', 'East', 'West', 'Northern', 'Southern',
                    'Eastern', 'Western']
        [place_terms.discard(term) for term in dont_keep]
        compound_places = {}
        for place in places:
            for term in sorted(list(place_terms))[::-1]:
                if f' {term} ' in f' {place} ' or \
                   f' {term}s ' in f' {place} ' and ' ' in place:
                    name = place.replace(term, '').strip()
                    if ' s ' in f'{name} ':
                        name = name.replace(' s', '').strip()
                    if name not in [*places, '']:
                        compound_places[place] = name
                    break
        return compound_places

    def replace_compound_places(self, compound_places):
        for (k, v) in compound_places.items():
            self.remove('places', k)
            self.add('places', v + f'(?=\s{k.replace(v, "").strip()})')

    def find_people_with_titles(self):
        people_with_titles = {}
        for person in self.ppn_types['people']:
            for term in sorted(self.person_titles)[::-1]:
                if f' {term} ' in f' {person} ' or \
                  f' {term}s ' in f' {person} ' and ' ' in person:
                    name = person.replace(term, '').strip()
                    if name:
                        if ' s ' in f'{name} ':
                            name = name.replace(' s', '').strip()
                        people_with_titles[person] = name
                    break
        return people_with_titles


    def sort_people_names(self, people_with_titles=None):
        last_names, male_names, female_names = {}, {}, {}
        person_title_female = {'Lady', 'Mrs', 'Mrs.', 'Miss', 'Nurse',
                                'Dowager Viscountess', 'Madam', 'Mistress'}
        person_title_both = {'Hon.', 'Right Hon.', 'Honourable',
                                'Right Honourable'}
        person_title_male = set(person_title).difference(
                                person_title_female).difference(
                                person_title_both)
        if not people_with_titles:
            people_with_titles = find_people_with_titles()
        #first iteration - find the names based on titles
        for k, v in people_with_titles.items():
            if any(p in k for p in person_title_male):
                if k.count(' ') == 1 and 'Sir' not in k:
                    if 'Edmund' in k:
                        male_names[k] = v
                    else:
                        last_names[k] = v
                        del people_with_titles[k]
                elif k.count(' ') == 2 and 'Lord' not in k:
                    name = v.split()
                    last_names[k] = name[1]
                    if 'Mrs' not in k and 'Rev' not in k:
                        male_names[k] = name[0]
                    del people_with_titles[k]
                elif (k.count(' ') > 2 and 'Sir' in k) or (k.count(' ') == 2 and 'Lord' in k):
                    name = v.split()
                    last_names[k] = ' '.join(name[1:])
                    del people_with_titles[k]
                elif 'Sir' in k:
                    male_names[k] = v
            elif any(p in k for p in person_title_female.\
              difference({'Mrs', 'Mrs.'})):
                if k.count(' ') > 1 and 'Hon' not in k:
                    if 'Bourgh' in k:
                        name = v.split()
                        last_names[k] = ' '.join(name[-2:])
                        if name[0].lower() != 'de':
                            female_names[k] = name[0]
                        del people_with_titles[k]
                    elif 'Dalrymple' in k:
                        last_names[k] = v
                        del people_with_titles[k]
                    else:
                        name = v.split()
                        last_names[k] = name[1]
                        female_names[k] = name[0]
                        del people_with_titles[k]
        # second iteration: use the found names to find more
        for k, v in people_with_titles.items():
            if any(p in k for p in person_title_female.\
              difference({'Mrs', 'Mrs.'})):
                if any(v_thing in last_names.values() \
                  for v_thing in [v, v.split()[-1], v[:-1], v[:-2]]):
                    if k.count(' ') == 1:
                        last_names[k] = v
                    elif 'Bourgh' in k:
                        name = v.split()
                        last_names[k] = ' '.join(name[-2:])
                        if name[0].lower() != 'de':
                            female_names[k] = name[0]
                    else:
                        name = v.split()
                        last_names[k] = name[1]
                        if 'Hon' not in k:
                            female_names[k] = name[0]
                elif any(v_thing in second_word \
                  for v_thing in [v, v.split()[-1], v[:-1], v[:-2]]):
                    if 'Bourgh' not in k:
                        last_names[k] = v
                elif v in ['Lascelle', 'Prescott', 'Atkinson', 'Andrews',
                            'Larolles', 'Nash', 'Watson', 'Lee', 'Grantley',
                            'Pope', 'Metcalfe', 'Walker', 'Godby', 'Prince',
                            'Webbs', 'Bickerton', 'Grey', 'Sparks', 'Hamilton',
                            'Careys']:
                    last_names[k] = v
                else:
                    female_names[k] = v
        self.add('last_names', last_names.values())
        self.add('male_names', male_names.values())
        self.add('female_names', female_names.values())
        for name in last_names.keys(): del people_with_titles[name]
        for name in male_names.keys(): del people_with_titles[name]
        for name in female_names.keys(): del people_with_titles[name]

        return people_with_titles

    def unclassified_people(self, partial_match=True):
        unclassified_names  = []
        classified_names = set(*self.ppn_types['last_names'],
                               *self.ppn_types['male_names'],
                               *self.ppn_types['female_names'])

        if partial_match:
            condition = lambda x: any(n in classified_names for n in x)
        else:
            condition = lambda x: all(n not in classified_names for n in x)
        for words in people:
            if words not in classified_names:
                names = words.split()
                if condition(names):
                    unclassified_names.extend(names)
        unclassified_names = list(set(unclassified_names))
        #some names have an s at the end because of a possessive 's
        unclassified_names = [n for n in unclassified_names \
                              if condition([n[:-1]])]
        return unclassified_names

    def check_overlap(self):
        overlap = []
        for noun_type, nouns in self.ppn_types.items():
            for noun_type2, nouns2 in self.ppn_types.items():
                if noun_type != noun_type2:
                    for noun in nouns:
                        if noun in nouns or noun[:-1] in nouns2:
                            overlap.append(noun)
        return overlap

    def escape(self, ppn_types=None):
        if not ppn_types:
            ppn_types = self.ppn_types
        for type, names in ppn_types.items():
            for word in names:
                new_word = word.replace(' ', '\s')
                if '.' in word and '\\' not in word:
                    new_word = new_word.replace('.', '\.')
                self.remove(type, word)
                self.add(type, new_word)
        return ppn_types

    def input_placeholders(self, s):
        return input_placeholders(self.ppn_types, s)
