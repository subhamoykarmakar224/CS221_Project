import os
import time
import json
from app.indexer.utils.DataCleaner import separate_data
from app.indexer.nlp.Tokenizer import NLP


class Indexer:
    def __init__(self):
        self.npl = NLP()

    # Get list of all file with their full path
    def get_list_of_files(self, url):
        file_list = []
        for path, subdirs, files in os.walk(url):
            for name in files:
                file_list.append(os.path.join(path, name))

        return file_list

    def read_file_tokenize(self, file_uri):
        with open(file_uri, 'r') as f:
            web_dict_data = json.load(f)
            url = web_dict_data['url']
            web_content = web_dict_data['content']
            encoding = web_dict_data['encoding']
            # Generate Data
            separate_data(web_content, url, encoding, self.npl)

    # 1988
    # 55393
    def start_indexing(self, url):
        ts = time.time()
        file_list = self.get_list_of_files(url)
        for i in range(0, len(file_list[:2])):
            self.read_file_tokenize(file_list[i])

        print(f'Time Taken for {len(file_list)} files: {str(time.time() - ts)}')


if __name__ == '__main__':
    ind = Indexer()
    # url_analyst = '../../data/analyst/ANALYST/'
    # ind.start_indexing(url_analyst)
    url_dev = '../../data/developer/DEV/'
    ind.start_indexing(url_dev)
