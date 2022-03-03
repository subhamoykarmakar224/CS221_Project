from socketserver import ThreadingUDPServer
from simple_attempt.search.boolean_query import BooleanQuery


def get_data(prefix=''):
    BQ = BooleanQuery()
    found_docs, query_tokens = BQ.search(prefix)

    res = []
    tags = ''
    for token in query_tokens:
        tags += ' #' + token

    for i in range(len(found_docs)):
        res.append({ 'title': i+1, 'tags': tags, 'score': found_docs[i][1], 'url': found_docs[i][0] })

    return res
