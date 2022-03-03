import pickle
import math
from pydoc import doc
from secrets import token_hex

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def get_search_res(search_term):
    inverted_index = None
    aux_map = None
    document_frequencies = None

    with open('./simple_attempt/indexer/pickles/auxiliary_map', 'rb') as aux_file:
        aux_map = pickle.load(aux_file, encoding="bytes")
    N = len(aux_map)

    with open('./simple_attempt/indexer/pickles/inverted_index', 'rb') as index_file:
        inverted_index = pickle.load(index_file, encoding="bytes")

    stop_list = set(stopwords.words('english'))
    ps = PorterStemmer()

    #query_tokens = word_tokenize(input("Search Query: "))
    query_tokens = word_tokenize(search_term)
    query_tokens = [ps.stem(t) for t in query_tokens if (t not in stop_list and len(t) > 1)]


    # get all the term frequencies for each query token
    term_freqs = dict()

    for token in query_tokens:
        term_freqs[token] = dict()

        if token in inverted_index:

            m = len(inverted_index[token])

            for docId in inverted_index[token]:
                tf = 1 + math.log(inverted_index[token][docId])
                idf = math.log(N / m)
                term_freqs[token][docId] = tf * idf


    # limit found documents to those that contain ALL the query tokens
    intersection = term_freqs[query_tokens[0]].keys()

    for i in range(1, len(query_tokens)):
        intersection = intersection & term_freqs[ query_tokens[i] ].keys()


    # gather total tf-idf scores by combining individual tf-idf scores for each query token 
    tf_idfs = dict()

    for docId in intersection:
        tf_idfs[docId] = 0

        for token in query_tokens:
            tf_idfs[docId] += term_freqs[token][docId]


    # output top 5 URLs sorted by tf-idf score
    found_docs = []

    for docId in sorted(tf_idfs, key = lambda t: -tf_idfs[t]):
        found_docs.append((aux_map[docId], tf_idfs[docId]))

        if len(found_docs) == 5:
            break

    for url, tfidf in found_docs:
        print(f'{url}, tf-idf: {tfidf :.3f}')
    
    return (found_docs, query_tokens)
