import os
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


def make_index():
    stop_list = set(stopwords.words('english'))

    # TODO: modify start directory as needed for your machines
    start_directory = "../../../ANALYST"

    # structure of index is: {term : {docId :  frequency of term in doc} }
    # TODO: change to use the Posting class to store more metadata for each term
    inverted_index = dict()

    # mapping between docId (int) and url (string)
    aux_map = dict()
    docId = 0

    # TODO: process documents in batches and dump to disk as we go

    for subdir, dirs, files in os.walk(start_directory):

        for file in files:
            filename = os.path.join(subdir, file)
            
            try:
                with open(filename, 'r') as f:

                    data = json.load(f)

                    url = data['url']
                    aux_map[docId] = url

                    soup = BeautifulSoup(data["content"], 'html.parser')

                    tokens = word_tokenize(soup.get_text(separator="\n", strip=True))
                    tokens = [t for t in tokens if (t not in stop_list and len(t) > 1)]

                    for token in tokens:
                        if token not in inverted_index:
                            inverted_index[token] = dict()
                        
                        if docId not in inverted_index[token]:
                            inverted_index[token][docId] = 0
                        
                        inverted_index[token][docId] += 1

                    docId += 1

                    # can track progress or return early to see indexer working as expected
                    if docId % 50 == 0:
                        print(inverted_index)
                        print(aux_map)
                        # return
    
            except Exception as e:
                print(e)
       

if __name__ == '__main__':
    make_index()
