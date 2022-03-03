from flask import Flask, render_template, request

# from app.utils.Database import get_data
from app.utils.boolean_query import get_search_res


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    res = []
    prefix = '\t'
    error = ''
    if request.method == 'POST':
        prefix = request.form.get('searchterm')
        if prefix == '' or prefix == '/':
            error = 'Please enter a valid string to search'
        else:
            data, query_tokens = get_search_res(prefix)
            tag = ''
            for q in query_tokens:
                tag += ' #' + q

            for url, tfidf in data:
                res.append({
                    'title': url,
                    'tags': tag,
                    'url': url,
                    'score': tfidf
                })
                

    return render_template('index.html', results=res, prefix=prefix, error=error)

