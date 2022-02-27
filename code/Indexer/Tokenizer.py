from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.stem import PorterStemmer
from nltk.metrics.distance import jaccard_distance
from nltk.corpus import words

# TODO: Clean up text from unwanted punctuations and charecters
class NLP:
    def __init__(self):
        # self.stop_words = set(stopwords.words('english'))
        self.correct_words = words.words()
        self.ps = PorterStemmer()

    def word_tokenizer_count(self, lines):
        word_tokens = word_tokenize(lines)
        word_count = dict()
        for i in range(len(word_tokens)):
            word = word_tokens[i]
            word = self.ps.stem(word.lower())
            if word not in word_count:
                word_count[word] = [0, []]
            word_count[word][0] += 1
            word_count[word][1].append(i)
        
        word_count = sorted(word_count.items(), key= lambda x : x[1][0], reverse=True)

        return word_count

    def correct_spelling(self, incorrect_word):
        patemp = [(jaccard_distance(set(ngrams(incorrect_word, 2)),
                                    set(ngrams(w, 2))), w)
                  for w in self.correct_words if w[0] == incorrect_word[0]]
        return sorted(patemp, key=lambda val: val[0])[0][1]


a = '''
The oldest classical Greek and Latin writing had little or no space between words and could be written 
in boustrophedon (alternating directions). Over time, text direction (left to right) became standardized, 
and word dividers and terminal punctuation became common.
'''
# n = NLP()
# res = n.word_tokenizer_count(a)
# for r in res:
#     print(r)

"""
('and', [4, [4, 14, 38, 41]])
('word', [2, [13, 39]])
('(', [2, [20, 30]])
('direct', [2, [22, 29]])
(')', [2, [23, 34]])
('.', [2, [24, 46]])
(',', [2, [27, 37]])
('becam', [2, [35, 44]])
('the', [1, [0]])
('oldest', [1, [1]])
('classic', [1, [2]])
('greek', [1, [3]])
('latin', [1, [5]])
('write', [1, [6]])
('had', [1, [7]])
('littl', [1, [8]])
('or', [1, [9]])
('no', [1, [10]])
('space', [1, [11]])
('between', [1, [12]])
('could', [1, [15]])
('be', [1, [16]])
('written', [1, [17]])
('in', [1, [18]])
('boustrophedon', [1, [19]])
('altern', [1, [21]])
('over', [1, [25]])
('time', [1, [26]])
('text', [1, [28]])
('left', [1, [31]])
('to', [1, [32]])
('right', [1, [33]])
('standard', [1, [36]])
('divid', [1, [40]])
('termin', [1, [42]])
('punctuat', [1, [43]])
('common', [1, [45]])

"""