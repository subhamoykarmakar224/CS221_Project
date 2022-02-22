from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.metrics.distance import jaccard_distance
from nltk.corpus import words


class NLP:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.correct_words = words.words()

    def word_tokenizer_count(self, lines):
        word_tokens = word_tokenize(lines)
        word_count = dict()
        for word in word_tokens:
            word = word.lower()
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1

        return word_count

    def correct_spelling(self, incorrect_word):
        patemp = [(jaccard_distance(set(ngrams(incorrect_word, 2)),
                                    set(ngrams(w, 2))), w)
                  for w in self.correct_words if w[0] == incorrect_word[0]]
        return sorted(patemp, key=lambda val: val[0])[0][1]
