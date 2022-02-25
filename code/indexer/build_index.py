import os
import json
import pickle
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# builds the inverted index in memory
def make_index():
    stop_list = set(stopwords.words('english'))
    ps = PorterStemmer()

    # TODO: modify start directory as needed for your machines and/or change to DEV
    start_directory = "../../../DEV"

    # structure of index is: {term : {docId :  frequency of term in doc} }
    # TODO: change to use the Posting class to store more metadata for each term
    inverted_index = dict()

    # mapping between docId (int) and url (string)
    aux_map = dict()
    docId = 0

    # TODO: process documents in batches and dump to disk as we go instead of just at the end

    for subdir, dirs, files in os.walk(start_directory):

        for file in files:
            filename = os.path.join(subdir, file)
            
            try:
                with open(filename, 'r') as f:

                    # load the data as json to separate content from url
                    data = json.load(f)

                    url = data['url']
                    aux_map[docId] = url

                    soup = BeautifulSoup(data["content"], 'html.parser')

                    # tokenize just the text from the page
                    tokens = word_tokenize(soup.get_text(separator="\n", strip=True))

                    # remove stopwords and do stemming
                    tokens = [ps.stem(t) for t in tokens if (t not in stop_list and len(t) > 1)]

                    for token in tokens:
                        if token not in inverted_index:
                            inverted_index[token] = dict()
                        
                        if docId not in inverted_index[token]:
                            inverted_index[token][docId] = 0
                        
                        inverted_index[token][docId] += 1

                    docId += 1

                    # track progress to see indexer working as expected
                    if docId % 1000 == 0:
                        print(len(inverted_index))
                        print(docId)
           
            except Exception as e:
                print(e)

    # write inverted_index and aux_map to disk as pickle files
    with open('index_pickle', 'ab') as index_file:
        pickle.dump(inverted_index, index_file, protocol=-1)                     
    
    with open('auxMap_pickle', 'ab') as aux_file:
        pickle.dump(aux_map, aux_file, protocol=-1)   


# print the index and auxiliary map to ensure they were built correctly
def print_index():
    with open('auxMap_pickle', 'rb') as aux_file:
        aux_map = pickle.load(aux_file)
        print(f'{len(aux_map)} documents')
    
        # for docId in aux_map:
        #     print(f'{docId} : {aux_map[docId]}')
        #     if docId == 100:
        #         break
    
    with open('index_pickle', 'rb') as index_file:
        inverted_index = pickle.load(index_file, encoding="bytes")
        print(f'{len(inverted_index)} terms')

        # for term in sorted(inverted_index, key = lambda t: -len(inverted_index[t])):
        #     print(f'{term} : {inverted_index[term]}')   


if __name__ == '__main__':
    make_index()
    print_index()



