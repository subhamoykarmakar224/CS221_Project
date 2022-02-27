import datetime
from flask import Flask, render_template, request
from app.indexer.ds.TrieController import TrieController

webapp = Flask(__name__)
trie_controller = TrieController()


@webapp.route('/', methods=['POST', 'GET'])
def index():
    res = []
    prefix = '\t'
    error = ''
    start_time = datetime.datetime.now()
    if request.method == 'POST':
        prefix = request.form.get('searchterm')
        if prefix == '' or prefix == '/':
            error = 'Please enter a valid string to search'
        else:
            res = trie_controller.search_prefix(str(prefix).lower())
            res = sorted(res, key=lambda x: x[1], reverse=True)
            res = res[:50]

            result = []
            for r in res:
                result.append({
                    'title': r[2], 'tags': str(r[0][r[0].index('\\') + 1:]), 'last_updated': '-na-', 'url': r[2]
                })
            res = result
    end_time = datetime.datetime.now()

    return render_template('index.html', results=res, prefix=prefix, error=error, qtime=end_time - start_time)
