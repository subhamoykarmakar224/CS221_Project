from flask import Flask, render_template, request

from app.utils.Database import get_data

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
            res = get_data(prefix)

    return render_template('index.html', results=res, prefix=prefix, error=error)

