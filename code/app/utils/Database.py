from simple_attempt.search.boolean_query import BooleanQuery


def get_data(prefix=''):
    BQ = BooleanQuery()
    found_docs = BQ.search(prefix)

    res = []
    for i in range(len(found_docs)):
        res.append({ 'title': i+1, 'tags': '', 'last_updated': '', 'url': found_docs[i][0] })

    return res
