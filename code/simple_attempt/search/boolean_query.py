import pickle

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


if __name__ == '__main__':
    inverted_index = None
    aux_map = None
    document_frequencies = None

    with open('../indexer/pickles/auxiliary_map', 'rb') as aux_file:
        aux_map = pickle.load(aux_file, encoding="bytes")

    with open('../indexer/pickles/inverted_index', 'rb') as index_file:
        inverted_index = pickle.load(index_file, encoding="bytes")
    
    with open('../indexer/pickles/document_frequency', 'rb') as index_file:
        document_frequencies = pickle.load(index_file, encoding="bytes")

    stop_list = set(stopwords.words('english'))
    ps = PorterStemmer()

    query_tokens = tokens = word_tokenize(input("Search Query: "))
    print()
    query_tokens = [ps.stem(t) for t in query_tokens if (t not in stop_list and len(t) > 1)]

    tf_idfs = dict()

    for token in query_tokens:
        if token in inverted_index:

            for docId in inverted_index[token]:
                if docId not in tf_idfs:
                    tf_idfs[docId] = 0

                tf_idfs[docId] += inverted_index[token][docId] / document_frequencies[docId]

    found_docs = []

    for docId in sorted(tf_idfs, key = lambda t: -tf_idfs[t]):
        found_docs.append((aux_map[docId], tf_idfs[docId]))

        if len(found_docs) == 5:
            break

    for url, tfidf in found_docs:
        print(f'{url}, tf-idf: {tfidf}')
    print()