import datetime
from flask import Flask, render_template, request
from datetime import datetime
from app.GetData import GetData
from app.util import clean_data

webapp = Flask(__name__)

get_data = GetData()


@webapp.route('/', methods=['POST', 'GET'])
def index():
    res = []
    prefix = '\t'
    error = ''
    qtime = 0
    start_time = datetime.now()
    if request.method == 'POST':
        prefix = request.form.get('searchterm')
        if prefix == '' or prefix == '/':
            error = 'Please enter a valid string to search'
        else:
            res = get_data.get_data(prefix)
            end_time = datetime.now()
            qtime = end_time - start_time
            print('Search Term: ', prefix)
            res = clean_data(res)

    return render_template('index.html', results=res, prefix=prefix, error=error, qtime=qtime)
