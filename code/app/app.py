import datetime
from flask import Flask, render_template, request


webapp = Flask(__name__)


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
            res = [
                {'title': 'T1', 'tags': '#tag1', 'last_updated': '-na-', 'url': 'http://test1.html'},
                {'title': 'T2', 'tags': '#tag2', 'last_updated': '-na-', 'url': 'http://test2.html'},
                {'title': 'T3', 'tags': '#tag3', 'last_updated': '-na-', 'url': 'http://test3.html'},
                {'title': 'T4', 'tags': '#tag4', 'last_updated': '-na-', 'url': 'http://test4.html'}
                ]

    end_time = datetime.datetime.now()

    return render_template('index.html', results=res, prefix=prefix, error=error, qtime=end_time - start_time)
