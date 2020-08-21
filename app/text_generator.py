'''
Module to handle all the python processes used in the app.py script to generate the web app.
'''
import pickle as pkl
# from nltk.tokenize import word_tokenize
# from nltk import download
# download('punkt')
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.models import load_model
from re import findall

# model = load_model('whatever its called')
#
# with open('models/tokenizer.pkl') as f:
#     tokenizer = pkl.load(f)
#
# with open('models/word_decoder.pkl') as f:
#     word_decoder = pkl.load(f)
import markov
from random import randint, sample
mk = markov.load('models/markov.pkl', randint(0, 1000))

proper_noun_types = {'-LNG-':('Give me a language',
                              ['Swahili', 'Spanish', 'German', 'Tagalog']),
                     '-NTL-':('Give me a nationality',
                              ['American', 'Scottish', 'South African', 'Filipino']),
                     '-CNT-':('Give me a country',
                              ['Wales', 'Japan', 'Australia', 'the Vatican']),
                     '-MTH-':('Give me a month',
                              ['July', 'Harvest Month', 'Wolf Month', 'August']),
                     '-WKD-':('Give me a weekday',
                              ['Friday', 'Thor\'s Day', 'Hump Day', 'Tuesday']),
                     '-HLD-':('Give me a holiday',
                              ['Christmas', 'National Pancake Day', 'Pi Day', '4/20']),
                     '-WTR-':('Give me a body of water',
                              ['the Atlantic Ocean', 'the Nile River', 'the pond in your backyard', 'Loch Ness']),
                     '-BTS-':('Give me a name for a ship!',
                              ['HMS Gallifrey', 'The Black Pearl', 'A UFO', 'The Flying Dutchman']),
                     '-AUT-':('Give me an author',
                              ['JRR Tolkien', 'Shakespeare', 'your friend who writes fanfiction', 'Homer', 'Mary Shelley', 'H.P. Lovecraft']),
                     '-LTR-':('Give me a name for a written work',
                              ['Hamlet', 'Harry Potter', 'My Immortal', 'Hamilton', 'your favorite fanfiction']),
                     '-NPP-':('Give me the name of a news source',
                              'The New York Times', 'The Onion', 'Twitter'),
                     '-PLC-':('Give me a city or place name',
                              ['San Francisco', 'Timbuktu', 'the Moon', 'Atlantis', 'Oz', 'Yosemite', ]),
                     '-LNM-':('Give me a last name',
                              ['McGonagall', 'Weasley', 'Potter', 'Obama', 'Stark', 'Lovelace', 'Caesar', 'Churchill', 'Armstrong', 'Darcy']),
                     '-MNM-':('Give me a male name',
                              ['Steve', 'Thor', 'T\'Challa', 'Achilles', 'Plato', 'Xavier', 'Alexander the Great', 'Odyssius', 'Oedipus', 'Socrates']),
                     '-FNM-':('Give me a female name',
                              ['Arya', 'Daenerys', 'Sansa', 'Beyonce', 'Kesha', 'Adele', 'Alice', 'Eveline', 'Hermione', 'Francesca'])}

def gen_text():
    '''
    Generate string of text.
    '''
    output_str = mk.generate_all()
    return output_str

'''
This stuff is for the neural net text generator but was unable to get a model working in time to implement it.
'''
# def gen_text(args):
#
#     word_tokens = ['-BGP-']*10
#     ending = tokenizer.tokenize('-ENP-')
#     sent = tokenizer.texts_to_sequences(word_tokens)[0]
#     max_len = 200 + len(word_tokens)

    # while len(sent) < max_len and new_word != ending:
    #     padded_sentence = pad_sequences(sent[-19:], maxlen=19)
    #     new_word = model.predict(np.asarray(padded_sentence).reshape(1,-1))
    #     sent.append(new_word.argmax()+1)
#     output_str = _stitch_string(_decode_words(sent))
#     return output_str

# def _decode_words(words):
#     return map(lambda x : reverse_word_map[x], words)
#
# def _stitch_string(tokens_list):
#     output_str = ''
#     for token in tokens_list:
#         if token == '-BGP-':
#             continue
#         elif token == '-ENP-':
#             break
#         elif isalnum(token) or token in proper_noun_types.keys():
#             output_str += ' ' + token
#         else:
#             output_str += token
#     return output_str



def get_ppns():
    '''
    Find out which, and how many proper nouns are in the generated text.
    '''
    text = gen_text()
    ppns = []
    for i, key in enumerate(findall('-[A-Z]{3}-', text)):
        k = proper_noun_types[key]
        ppns.append((f'{key}_{i}', k[0], 'Eg. ' + ' or '.join(sample(k[1], 2))))
    if len(ppns) < 3 or len(ppns) > 8 or len(text) > 500:
        text, ppns = get_ppns()
    return text, ppns

def replace_ppn_keys(text, user_defined_nouns):
    '''
    Replace proper noun keys with user-given names.
    '''
    for (noun_key, noun) in user_defined_nouns:
        start = text.find(noun_key[:-2])
        text = text[:start] + noun + text[start+5:]
    return text
