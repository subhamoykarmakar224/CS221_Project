from socketserver import ThreadingUDPServer
from simple_attempt.search.boolean_query import BooleanQuery


def get_data(prefix=''):
    BQ = BooleanQuery()
    found_docs = BQ.search(prefix)

    res = []
    tags = ''
    for token in prefix.split(' '):
        if len(token) > 2:
            tags += ' #' + token

    for i in range(len(found_docs)):
        res.append({ 'title': i+1, 'tags': tags, 'last_updated': 'XX', 'url': found_docs[i][0] })

    return res
