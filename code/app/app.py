import os.path
import datetime
import json
from flask import Flask, render_template, request
from app.utils.Database import get_data
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
                with open(r[0], 'r') as f:
                    web_dict_data = json.load(f)
                    url = web_dict_data['url']
                    encoding = web_dict_data['encoding']

                    result.append({
                        'title': url, 'tags': str(r[0][r[0].index('\\') + 1:]), 'last_updated': '10', 'url': url
                    })
            res = result
    end_time = datetime.datetime.now()

    return render_template('index.html', results=res, prefix=prefix, error=error, qtime=end_time - start_time)
