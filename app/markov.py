'''
Class to generate Markov chains.
To use:
First initialize, then input a list of strings using addDocList, or a single string using addDoc. Both can be called as many times as desired. To generate chain, use generate to generate a string of fixed length, or if number of input string >> length of strings, use generate_all to generate a string with a beginning and end.
'''
from random import seed, choice, choices
from re import findall

def load(filename, new_random = None):
    '''
    Load saved markov chain generator and reinstantiate.
    Arguments:
    - filename: location of saved file
    - new_random: optional, can be used to ensure that same text is not generated every time the model is loaded
    '''
    import pickle as pkl
    with open(filename, 'rb') as f:
        chain_map, type, order, random_state = pkl.load(f)
        if new_random:
            random_state = new_random
        c = chain(type = type, order=order, random_state=random_state)
        c.chain_map = chain_map
        return c

class chain():

    def __init__(self, type='word', order=3, random_state=42):
        '''
        Arguments:
        - type: what to use to create the Markov chain. Accepts 'word' or 'char'
        - order: number of type to use in the Markov chain prefixes any       positive int will work, but ideal values are somewhere around the range
            for type = word: [2-4]
            for type = char: [8-12]
        Less than that will generate uninterpretable chains, and more than that will reproduce input text too exactly, although there's more wiggle room for type = char. Accepts positive int
        - random_state: int
        '''
        self.order = order
        self.type = type
        if type=='word':
            self.regex = '\W?\w+\W+'
        elif type=='char':
            self.regex = '(?s).'
        else:
            raise ValueError('Unknown type')
        self.random_state = random_state
        seed(random_state)
        self.chain_map = {}

    def addDocList(self, docs):
        '''
        Input a list of strings to Markov chain.

        Arguments:
        - docs: list of strings with which to build Markov chain
        Returns: None
        '''
        for doc in docs:
            self.addDoc(doc)

    def addDoc(self, doc):
        '''
        Input a string to Markov chain.

        Arguments:
        - doc: string with which to build Markov chain
        Returns: None
        '''
        doc_words = findall(self.regex, doc)
        #set empty chain as initializing prefix
        ##this helps the chain to 'reboot' if it gets stuck
        ###which can happen if most recently generated words aren't in the dict
        prefix = tuple(['']*self.order)
        num_words = len(doc_words)
        for i in range(num_words+self.order):
            if i < num_words:
                word = doc_words[i]
            else:
                word = 'END_CHAIN'
            suffix = self.chain_map.get(prefix)
            if not suffix:
                suffix = []
            suffix.append(word)
            self.chain_map[prefix] = suffix
            prefix = (*prefix[1:], word)
        return

    def generate(self, output):
        '''
        Return a generated Markov chain string of length output.
        Use this function to generate output if size of input strings >> number of input strings.

        Arguments:
        - output: number of type to return in generated string
        Returns:
        - Generated string of length output
        '''

        output_str = ''
        #Start at random set of words
        prefix = choice(self.chain_map.keys())

        #Raise error if no strings were input into chain
        if self.chain_map == {}:
            raise Error('Call addDoc or addDocList before generate')

        #iteratively generate output string
        for i in range(output):
            suffix = self.chain_map.get(prefix)
            if suffix:
                new_word = choice(suffix)
            else:
                #if there's no suffix, that means this specific combination of
                ##prefix words isn't in the dict, so let's add '' instead
                new_word = ''

            #If we hit an END_CHAIN in the middle of iterating, don't output
            ## and add an empty string to prefix instead
            if new_word != 'END_CHAIN':
                output_str += new_word
                prefix = (*prefix[1:], new_word)
            else:
                prefix = (*prefix[1:], '')
        return output_str

    def generate_all(self, max_iter=1000):
        '''
        Return a generated Markov chain string that stops at END_CHAIN.
        Use this function to generate output if and only if size of input strings << number of input strings. Otherwise, there's a good chance of an infinite loop. While max_iter will prevent a neverending loop, it's better to just call generate instead.

        Arguments:
        - max_iter: maximum
        Returns:
        - Generated string. Length will vary as it won't stop generating until either it generates END_CHAIN or it hits max_iter
        '''

        output_str, new_word, i = '', '', 0
        #Since there's more choices of string starts, we can start at beginning
        prefix = tuple(['']*self.order)

        #Raise error if no strings were input into chain
        if self.chain_map == {}:
            raise Error('Call addDoc or addDocList before generate_all')

        while new_word!='END_CHAIN' and i < max_iter:
            suffix = self.chain_map.get(prefix)
            if suffix:
                new_word = choice(suffix)
            else:
                #if there's no suffix, that means this specific combination of
                ##prefix words isn't in the dict, so let's add '' instead
                new_word = ''
            prefix = (*prefix[1:], new_word)

            #Don't want to print END_CHAIN
            if new_word != 'END_CHAIN':
                output_str += new_word
            i += 1
        return output_str

    def save(self, filename):
        import pickle as pkl
        with open(filename, 'wb') as f:
            pkl.dump((self.chain_map, self.type, self.order,
                      self.random_state), f)
